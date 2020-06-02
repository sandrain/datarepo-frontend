"""
    Dataset View
"""

from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied

from django import forms
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from sdifrontend.apps.mainpage.models import SysDataset, SysUser, SysFile

from .utils import (unpack_dataset_json, clean_recieved_val,
                    clean_keywords, uuid, json, make_keywords_list)

# we only need thos for testing
from .utils import generate_fake_dataset_properties, generate_fake_dataset_files

class DatasetForm(forms.ModelForm):
    """
    Form to create / update a dataset
    """

    title = forms.CharField()
    sub_title = forms.CharField()
    description = title = forms.CharField()

    class Meta:
        model = SysDataset
        exclude = ['id']


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
    # def get(self, request, *args, **kwargs):
    #     print(request)
    #     print(args)

    #     context = super().get_context_data(**kwargs)

    #     print(context)

    #     ds_id = request.dataset_id

    #     dataset = unpack_dataset_json(
    #                 get_object_or_404(SysDataset.objects.select_related(),
    #                                 id=ds_id))

    #     return render(request, 'mainpage/dataset/detail.html', {'dataset': dataset})

    def get_object(self, queryset=None):
        _id = self.kwargs.get(self.pk_url_kwarg)
        #tmp = get_object_or_404(SysDataset.objects.select_related(), id=_id)
        tmp = get_object_or_404(SysDataset.objects.select_related(), id=_id)
        obj = unpack_dataset_json(tmp)

        print("obj: {}".format(obj))

        return obj

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context


class DatasetCreate(CreateView):
    model = SysDataset
    form_class = DatasetForm
    template_name = 'mainpage/dataset/edit.html'


class DatasetUpdate(UpdateView):
    model = SysDataset
    form_class = DatasetForm
    template_name = 'mainpage/dataset/edit.html'


class DatasetDelete(DeleteView):
    """
        Delete a dataset
    """
    template_name = 'mainpage/dataset/delete.html'
    model = SysDataset
    success_url = reverse_lazy('dataset-index')

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super().get_object()
        user = SysUser.objects.get(username=self.request.user.username)
        print("obj: {}".format(obj.owner))
        print("user: {}".format(user))

        if not obj.owner == user:
            raise PermissionDenied
        return obj

def dataset_create(request):

    if request.method == 'POST':
        post_data = request.POST
        print(post_data)

        ###
        try:
            dataset_type = post_data['sysdataset-type']
        except:
            dataset_type = ''

        try:
            subjects = post_data['sysdataset-subjects']  # list
        except:
            subjects = None

        title = post_data['sysdataset-title']
        subtitle = clean_recieved_val(post_data['sysdataset-subtitle'])
        description = clean_recieved_val(post_data['sysdataset-description'])

        try:
            keywords = post_data['sysdataset-keywords'].split(",")
            keywords = clean_keywords(keywords)
        except:
            keywords = None

        # currently we are generating fake fields other than the title
        properties = generate_fake_dataset_properties(
            post_data['sysdataset-title'],
            subtitle=subtitle,
            description=description,
            keywords=keywords)
        files = generate_fake_dataset_files()
        structure = json.dumps({'data': files})
        size = sum(f['size'] for f in files)

        data_set = SysDataset(properties=properties,
                              uuid=str(uuid.uuid4()),
                              owner=SysUser.objects.get(
                                  username=request.user.username),
                              size=size,
                              structure=structure)

        data_set.save()

        # populate dataset files
        for _f in files:
            _r = SysFile(dataset=data_set,
                         name=_f['name'],
                         size=_f['size'])
            _r.save()

        dataset = unpack_dataset_json(
            get_object_or_404(SysDataset.objects.select_related(), id=data_set.id))

        return render(request, 'mainpage/dataset/detail.html', {'dataset': dataset})

    else:
        qs = SysDataset.objects.select_related().order_by('-created')[:10]
        for obj in qs:
            obj = unpack_dataset_json(obj)
        template = loader.get_template('mainpage/index.html')
        context = {
            'latest_dataset_list': qs,
        }

        return HttpResponse(template.render(context, request))


def dataset_manage(request, dataset_id):

    if request.method == 'POST':

        post_data = request.POST

        if post_data['request-type'] == 'update':
            description_tosave = post_data['input-description-tosave']
            url_tosave = post_data['input-url-tosave']
            email_tosave = post_data['input-email-tosave']
            keywords_tosave = post_data['input-keywords-tosave']
            institution_tosave = post_data['input-institution-tosave']

            d = SysDataset.objects.filter(id=dataset_id)[0]
            properties = json.loads(d.properties)
            properties['description'] = description_tosave
            properties['url'] = url_tosave
            properties['institution'] = institution_tosave
            properties['keywords'] = clean_keywords(
                make_keywords_list(keywords_tosave))

            o = SysDataset.objects.filter(id=dataset_id)[0].owner
            o.email = email_tosave
            o.save()

            d.properties = json.dumps(properties)

            d.save()

            dataset = unpack_dataset_json(get_object_or_404(
                SysDataset.objects.select_related(), id=dataset_id))

            return render(request, 'mainpage/dataset/detail.html', {'dataset': dataset})

        elif post_data['request-type'] == 'delete':
            d = SysDataset.objects.filter(id=dataset_id)[0]
            d.delete()

            qs = SysDataset.objects.select_related().order_by('-created')[:10]
            for obj in qs:
                obj = unpack_dataset_json(obj)
            template = loader.get_template('mainpage/index.html')
            context = {
                'latest_dataset_list': qs,
            }

            return HttpResponse(template.render(context, request))

    elif request.method == 'GET':

        try:
            update = request.GET['update']
        except:
            update = 0

        if update == '1':
            dataset = unpack_dataset_json(
                get_object_or_404(SysDataset.objects.select_related(),
                                  id=dataset_id))

            return render(request, 'mainpage/dataset/update.html', {'dataset': dataset})

        else:

            dataset = unpack_dataset_json(
                get_object_or_404(SysDataset.objects.select_related(),
                                  id=dataset_id))

            return render(request, 'mainpage/dataset/detail.html', {'dataset': dataset})
