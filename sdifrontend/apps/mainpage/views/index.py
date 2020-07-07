from django.views import generic
from django.shortcuts import render
import random, json, uuid

from sdifrontend.apps.mainpage.models import SysDataset, SysUser, SearchIndex, SidebarMenu
from django.contrib.postgres.search import SearchQuery
from django.db.models import Q

from .dataset import DatasetForm

from .utils import unpack_dataset_json

class IndexView(generic.ListView):
    template_name = 'mainpage/index.html'
    context_object_name = 'datasets'

    form = None

    def post(self, request, *args, **kwargs):
        print(request.POST)
        return render(request, self.template_name)

    #def get(self, request, *args, **kwargs):
    #    return render(request, self.template_name)

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        if not self.form:
            self.form = DatasetForm
        context.update({
            'form': self.form
        })
        return context

    def get_queryset(self, **kwargs):
        # Get ten recent datasets.

        print(self.request)

        try:
            search = self.request.GET.get('search', None)
            print("search is:", search)
        except:
            search = None

        try:
            category = self.request.GET.get('category', None)
            print("category is:", category)
        except:
            category = None

        try:
            type = self.request.GET.get('type', None)
            print("type is:", type)
        except:
            type = None

        try:
            page = self.request.GET.get('page', None)
            print("page is:", page)
        except:
            page = 1

        try:
            page = int(page)
        except:
            page = 1
        
        print("############# search = ", search, "page =", page)

        if search is not None:
                
                print("--- implement your search logic here --")
                
                ## to test 
                ## http://localhost:8000/?search=oxidation%20data
                ## above url represents 'querying with keywords: oxidation data'
                
                keywords=search.split()
                
                print("Received {} search keywords: {}".format(len(keywords), keywords))

                ## 

                qs = SysDataset.objects
                for key_id in range(0,len(keywords)):
                    print('chaning search keywords: {}'.format(keywords[key_id]))
                    qs = qs.filter(searchindex__value=keywords[key_id])
                
                qs=qs.order_by('-created')
                print('result set size: {}'.format(len(qs)))
                ## get the correct dataset with the given keywords

                ##

        else: ## search is None  
            qs = SysDataset.objects.order_by('-created')
        
        if category is not None:
            qs = qs.filter(category=int(category))
        
        if type is not None:
            qs = qs.filter(type=int(type))
            
        qs = qs[10*(page-1):10*page]

        for obj in qs:
            try:
                o = unpack_dataset_json(obj)
            except:
                o = obj
            obj = o

            
        
        return qs

