# -*- coding: utf-8 -*-
"""
    Dataset View
"""

import logging

from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.core import validators

from django import forms
from django.views.generic import View, DetailView, ListView, FormView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from sdifrontend.apps.mainpage.models import SysDataset, SysUser, SysFile
from .. import sidebar

from .utils import (unpack_dataset_json, clean_recieved_val,
                    clean_keywords, uuid, json, make_keywords_list)

# we only need thos for testing
from .utils import generate_fake_dataset_properties, generate_fake_dataset_files


class BasicUploadView(View):
    def post(self, request):

        print("Post: {}".format(self.request.POST))
        print("Files: {}".format(self.request.FILES['file']))

        form = FileForm(self.request.POST, self.request.FILES)

        print(form)

        if form.is_valid():
            data = {'is_valid': True, 'file': "{}".format(
                self.request.FILES['file'])}

        else:
            data = {'is_valid': False}

        return JsonResponse(data)


class DatasetForm(forms.ModelForm):
    """
    Form to create / update a dataset
    """
    class Meta:
        model = SysDataset
        fields = []

    is_multipart = True

    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-1', 'placeholder': 'Enter Dataset Title'}))
    subtitle = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm mb-1', 'placeholder': 'Enter Dataset Subtitle'}))
    description = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control form-control-sm mb-1', 'placeholder': 'Please add your description for this dataset.', 'rows': '3'}))
    keywords = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm mb-1', 'placeholder': "Enter keywords separated by commas (e.g., 'climate, simulation, forecasting' )"}))
    type = forms.ChoiceField(choices=sidebar.get_ds_types(
        None), widget=forms.Select(attrs={'class': 'form-control'}))
    #subject = forms.MultipleChoiceField(choices=sidebar.get_ds_subjects(
    #    None), widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
    subject = forms.ChoiceField(choices=sidebar.get_ds_subjects(
        None), widget=forms.Select(attrs={'class': 'form-control'}))

    files = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}))


class DataSetsTypeView(ListView):
    """
        List Datasets by type
    """
    template_name = 'mainpage/index.html'
    context_object_name = "datasets"
    category = None

    def get_queryset(self):
        self.category = self.kwargs['category']
        return SysDataset.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Might want to do this differently
        for data_set in context['object_list']:
            data_set = unpack_dataset_json(data_set)

        return context


class DatasetView(DetailView):
    """
        List Details of a Dataset
    """
    template_name = 'mainpage/dataset/detail.html'
    queryset = SysDataset.objects.all()

    def get_object(self, queryset=None):
        _id = self.kwargs.get(self.pk_url_kwarg)
        tmp = get_object_or_404(SysDataset.objects.select_related(), id=_id)
        try:
            obj = unpack_dataset_json(tmp)
        except:
            obj = tmp

        print("obj: {}".format(obj))

        return obj


class DatasetCreate(CreateView):
    form_class = DatasetForm
    template_name = 'mainpage/dataset/edit.html'
    success_url = reverse_lazy('mainpage:dataset-detail')

    # def post(self, request, *args, **kwargs):
    #     form = DatasetForm(self.request.POST, self.request.FILES)

    #     print("Post: {}".format(request.POST))

    #     if form.is_valid():
    #         # call model create dataset
    #         print ("Form is Valid")
    #     else:
    #         print ("Form is invalid: {}".format(form.errors))

    #     return render(request, self.template_name, {'form': form})

    def form_valid(self, form):
        print(form)

        self.object = form.save()

        # TODO: make this a class variable?
        logger = logging.getLogger("django")

        # make sure the owner is in the db
        try:
            owner = SysUser.objects.get(
                                  username=self.request.user.username)
        except ObjectDoesNotExist:
            # We have no dataset for this user yet
            # login trough globus
            logger.info("Creating new user: {}".format(self.request.user.username))
            owner = SysUser.objects.create(username=self.request.user.username,
                                          email = self.request.user.email)

        # getting the cleaned data
        title = form.cleaned_data['title']
        subtitle = form.cleaned_data['subtitle']
        description = form.cleaned_data['description']
        keywords = form.cleaned_data['keywords']
        dataset_type = form.cleaned_data['type']
        subjects = form.cleaned_data['subject']

        # currently we are generating fake fields other than the title
        properties = generate_fake_dataset_properties(
            title,
            subtitle=subtitle,
            description=description,
            keywords=keywords)

        # TODO: handle the uploaded files
        files = generate_fake_dataset_files()
        structure = json.dumps({'data': files})
        size = sum(f['size'] for f in files)

        data_set = SysDataset(properties=properties,
                              uuid=str(uuid.uuid4()),
                              owner=owner,
                              size=size,
                              structure=structure,
                              category=subjects,
                              type=dataset_type)


        # TODO: Handle all the data in a transaction
        data_set.save()

        # populate dataset files
        for _f in files:
            _r = SysFile(dataset=data_set,
                        name=_f['name'],
                        size=_f['size'])
            _r.save()

        ###
        # try:
        #     dataset_type = post_data['sysdataset-type']
        # except:
        #     dataset_type = 0

        # try:
        #     subjects = post_data['sysdataset-subjects']  # list
        # except:
        #     subjects = None

        # title = post_data['sysdataset-title']
        # subtitle = clean_recieved_val(post_data['sysdataset-subtitle'])
        # description = clean_recieved_val(post_data['sysdataset-description'])

        # try:
        #     keywords = post_data['sysdataset-keywords'].split(",")
        #     keywords = clean_keywords(keywords)
        # except:
        #     keywords = None

        # # currently we are generating fake fields other than the title
        # properties = generate_fake_dataset_properties(
        #     title,
        #     subtitle=subtitle,
        #     description=description,
        #     keywords=keywords)
        # files = generate_fake_dataset_files()
        # structure = json.dumps({'data': files})
        # size = sum(f['size'] for f in files)

        # data_set = SysDataset(properties=properties,
        #                     uuid=str(uuid.uuid4()),
        #                     owner=SysUser.objects.get(
        #                         username=request.user.username),
        #                     size=size,
        #                     structure=structure,
        #                     category=subjects,
        #                     type=dataset_type)

        # data_set.save()

        # # populate dataset files
        # for _f in files:
        #     _r = SysFile(dataset=data_set,
        #                 name=_f['name'],
        #                 size=_f['size'])
        #     _r.save()

        # dataset = unpack_dataset_json(
        #     get_object_or_404(SysDataset.objects.select_related(), id=data_set.id))

        #return super().form_valid(form)
        return redirect('mainpage:dataset-detail', data_set.id)


class DatasetUpdate(UpdateView):
    model = SysDataset
    form_class = DatasetForm
    template_name = 'mainpage/dataset/edit.html'
    success_url = reverse_lazy('mainpage:dataset-detail')


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

        #if not obj.owner == user:
        #    raise PermissionDenied
        return obj

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
