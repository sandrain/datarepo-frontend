from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
import json
import uuid

from .models import SysDataset
from .models import SysUser
import random

# Create your views here.

def unpack_dataset_json(dataset):
    dataset.id = dataset.id
    dataset.attributes = json.loads(dataset.properties)
    dataset.sizemb = int(dataset.size / (2**20))
    dataset.filecount = len((json.loads(dataset.structure))['data'])
    dataset.keywords = ', '.join(dataset.attributes['keywords'])
    dataset.icon = 'icons/{:d}.png'.format(dataset.id % 500)
    return dataset
   

class IndexView(generic.ListView):
    template_name = 'mainpage/index.html'
    context_object_name = 'latest_dataset_list'

    def get_queryset(self):
        """Return the last five published questions."""
        #return SysDataset.objects.select_related().order_by('-created')[:10]
        qs = SysDataset.objects.select_related().order_by('-created')[:10]
        for obj in qs:
            obj = unpack_dataset_json(obj)
        return qs

def detail(request, dataset_id):
    dataset = unpack_dataset_json(get_object_or_404(SysDataset.objects.select_related(), id=dataset_id))
    
    return render(request, 'mainpage/detail.html', {'dataset': dataset})

def update(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        post_data = request.POST
        sysdataset_title = post_data['sysdataset_title']
        uuid_str = str(uuid.uuid4())

        d = SysDataset(properties='{"title":"'+sysdataset_title+'","keywords":["a","b","c"]}', uuid = uuid_str, owner = SysUser.objects.all()[random.randint(0,10)], size = random.randint(100000,20000000), structure='{"data":[{"name":"1.csv","size": 1024}]}')
        d.save()

        dataset = unpack_dataset_json(get_object_or_404(SysDataset.objects.select_related(), id=d.id))
        return render(request, 'mainpage/update.html', {'dataset': dataset})

    dataset = unpack_dataset_json(get_object_or_404(SysDataset.objects.select_related(), id=690))
    return render(request, 'mainpage/update.html', {'dataset': dataset})

#class DetailView(generic.DetailView):
#    model = DataSet
#    template_name = 'mainpage/detail.html'

#def detail_template(request):
#    return HttpResponse("Hello")
