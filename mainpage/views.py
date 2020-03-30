from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
import json

from .models import SysDataset
from .models import SysUser


# Create your views here.

def unpack_dataset_json(dataset):
    dataset.attributes = json.loads(dataset.properties)
    dataset.sizemb = int(dataset.size / (2**20))
    dataset.filecount = len((json.loads(dataset.structure))['data'])
    dataset.keywords = ', '.join(dataset.attributes['keywords'])
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

#class DetailView(generic.DetailView):
#    model = DataSet
#    template_name = 'mainpage/detail.html'

#def detail_template(request):
#    return HttpResponse("Hello")
