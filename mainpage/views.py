from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import DataSet

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'mainpage/index.html'
    context_object_name = 'latest_dataset_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return DataSet.objects.order_by('-creation_date')[:5]

def detail(request, dataset_id):
    dataset = get_object_or_404(DataSet, pk=dataset_id)
    return render(request, 'mainpage/detail.html', {'dataset': dataset})

#class DetailView(generic.DetailView):
#    model = DataSet
#    template_name = 'mainpage/detail.html'

#def detail_template(request):
#    return HttpResponse("Hello")
