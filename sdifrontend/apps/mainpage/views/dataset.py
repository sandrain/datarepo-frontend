# -*- coding: utf-8 -*-
"""
    Dataset View
"""

import logging
import os

from django.shortcuts import redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from django import forms
from django.views.generic import View, DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from sdifrontend.apps.mainpage.models import SysDataset, SysUser, SysFile, Category

from .. import sidebar

# we only need thos for testing
from .utils import generate_fake_dataset_properties, generate_fake_dataset_files


class FileForm(forms.Form):
    files = forms.FileField()


class BasicUploadView(View):
    def post(self, request):

        print("Post: {}".format(self.request.POST))
        print("Files: {}".format(self.request.FILES['files']))
        print("session key: {}".format(self.request.session.session_key))

        form = FileForm(self.request.POST, self.request.FILES)

        fs = FileSystemStorage(os.path.join(
            settings.MEDIA_ROOT, self.request.session.session_key))
        filename = fs.save(
            request.FILES['files'].name, request.FILES['files'].file)
        uploaded_file_url = fs.url(filename)

        # if form.is_valid():
        data = {'is_valid': True, 'name': "{}".format(
                self.request.FILES['files']), 'url': uploaded_file_url}

        # else:
        #    data = {'is_valid': False}

        return JsonResponse(data)


class DatasetForm(forms.ModelForm):
    """
    Form to create / update a dataset
    """
    class Meta:
        model = SysDataset
        fields = ['categories', 'properties']

    class MyModelMultipleChoiceField(forms.ModelMultipleChoiceField):
        """
        Helper class to display the name of the categories
        """
        def label_from_instance(self, obj):
            return obj.name

    is_multipart = True

    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-1', 'placeholder': 'Enter Dataset Title'}))
    subtitle = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm mb-1',
               'placeholder': 'Enter Dataset Subtitle'}))
    description = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control form-control-sm mb-1',
               'placeholder': 'Please add your description for this dataset.', 'rows': '3'}))
    keywords = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm mb-1',
               'placeholder': "Enter keywords separated by commas (e.g., 'climate, simulation, forecasting' )"}))
    type = forms.ChoiceField(choices=sidebar.get_ds_types(
        None), widget=forms.Select(attrs={'class': 'form-control'}))
    categories = MyModelMultipleChoiceField(queryset=Category.objects.all(),
                                            widget=forms.SelectMultiple(attrs={'class': 'form-control'}))

    files = forms.FileField(required=False, widget=forms.ClearableFileInput(
        attrs={'multiple': True, 'data-url': reverse_lazy('mainpage:upload')}))

class DataSetsListView(ListView):
    """
        Listview for Datasets
    """
    template_name = 'mainpage/index.html'
    context_object_name = "datasets"
    type = None
    paginate_by = 10

    form = None

    def get_context_data(self, **kwargs):
        context = super(DataSetsListView, self).get_context_data(**kwargs)
        if not self.form:
            self.form = DatasetForm
        context.update({
            'form': self.form
        })

        return context

    def get_queryset(self):
        try:
            search = self.kwargs['search']
            print("search is:", search)
        except KeyError:
            search = None

        try:
            categories = self.kwargs['category']
        except KeyError:
            categories = None

        try:
            _type = self.kwargs['type']
        except KeyError:
            _type = None

        if search is not None:

            print("--- implement your search logic here --")

            ## to test
            ## http://localhost:8000/?search=oxidation%20data
            ## above url represents 'querying with keywords: oxidation data'

            keywords = search.split()

            print("Received {} search keywords: {}".format(len(keywords), keywords))

            ##

            qs = SysDataset.objects
            for key_id in range(0, len(keywords)):
                print('chaining search keywords: {}'.format(keywords[key_id]))
                qs = qs.filter(searchindex__value=keywords[key_id])

            qs = qs.annotate(rank=SearchRank(SearchVector('properties'),
                                             SearchQuery(' '.join(keywords)))
                            ).order_by('-rank', '-created')

            print('result set size: {}'.format(len(qs)))
            ## get the correct dataset with the given keywords

            ##

        else: ## search is None
            if categories is not None:
                return SysDataset.objects.filter(categories=categories)
            elif _type is not None:
                return SysDataset.objects.filter(type=_type)
            else:
                return SysDataset.objects.order_by('-created')
        
        return qs

class DatasetView(DetailView):
    """
        List Details of a Dataset
    """
    template_name = 'mainpage/dataset/detail.html'
    model = SysDataset


class DatasetCreate(CreateView):
    form_class = DatasetForm
    template_name = 'mainpage/dataset/edit.html'
    success_url = reverse_lazy('mainpage:dataset-detail')

    def form_valid(self, form):
        # TODO: make this a class variable?
        logger = logging.getLogger("django")

        # make sure the owner is in the db
        try:
            owner = SysUser.objects.get(username=self.request.user.username)
        except ObjectDoesNotExist:
            # We have no dataset for this user yet
            # login trough globus
            logger.info('Creating new user: %s', self.request.user.username)
            owner = SysUser.objects.create(username=self.request.user.username,
                                           email=self.request.user.email)

        # getting the cleaned data
        title = form.cleaned_data['title']
        subtitle = form.cleaned_data['subtitle']
        description = form.cleaned_data['description']
        keywords = form.cleaned_data['keywords']

        dataset_type = form.cleaned_data['type']
        categories = form.cleaned_data['categories']

        # TODO: make this a little more elegant

        _keywords = []

        keywords_cleaned = []
        for keyword in keywords.split(","):
            if keyword.strip() != '':
                # deal with many commas and empty keywords
                keywords_cleaned.append(keyword.strip())
        keywords_cleaned = list(set(keywords_cleaned))  # remove duplicates
        _keywords.append(", ".join(keywords_cleaned))

        # currently we are generating fake fields other than the title
        properties = generate_fake_dataset_properties(
            title,
            subtitle=subtitle,
            description=description,
            keywords=_keywords)

        # TODO: handle the uploaded files
        files = generate_fake_dataset_files()
        structure = json.dumps({'data': files})
        size = sum(f['size'] for f in files)

        _uuid = str(uuid.uuid1())
        print("uuid: {}".format(_uuid))

        data_set = SysDataset.objects.create(properties=properties,
                                             uuid=_uuid,
                                             owner=owner,
                                             size=size,
                                             structure=structure,
                                             type=dataset_type)

        # TODO: Handle all the data in a transaction
        data_set.save()

        # Add categories
        for category in categories.all():
            data_set.categories.add(category)

        data_set.create_index()  # create index

        # populate dataset files
        for _f in files:
            _r = SysFile(dataset=data_set,
                         name=_f['name'],
                         size=_f['size'])
            _r.save()

        return redirect('mainpage:dataset-detail', data_set.id)


class DatasetUpdate(UpdateView):
    form_class = DatasetForm
    template_name = 'mainpage/dataset/update.html'
    success_url = reverse_lazy('mainpage:dataset-detail')
    model = SysDataset
    queryset = SysDataset.objects.all()

    form = None

    def get_context_data(self, **kwargs):
        print("get_context_data")
        context = super(DatasetUpdate, self).get_context_data(**kwargs)

        print(context)

        obj = context['object']
        print(obj.title)

        if not self.form:
            print("create form")
            # fill the form with the data
            self.form = DatasetForm(obj)

        context.update({
            'form': self.form
        })

        return context

class DatasetDelete(DeleteView):
    """
        Delete a dataset
    """
    template_name = 'mainpage/dataset/delete.html'
    model = SysDataset
    success_url = reverse_lazy('mainpage:dataset-index')

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super().get_object()
        user = SysUser.objects.get(username=self.request.user.username)
        print("obj: {}".format(obj.owner))
        print("user: {}".format(user))

        # if not obj.owner == user:
        #    raise PermissionDenied
        return obj

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
