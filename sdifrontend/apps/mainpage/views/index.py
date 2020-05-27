from django.views import generic
import random, json, uuid

from sdifrontend.apps.mainpage.models import SysDataset, SysUser

from .utils import unpack_dataset_json

class IndexView(generic.ListView):
    template_name = 'mainpage/index.html'
    context_object_name = 'latest_dataset_list'

    def get_queryset(self, **kwargs):
        # Get ten recent datasets.

        datatype = self.request.GET.get('datatype', None)
        print("Received data parameter:", datatype)

        try:
            search = self.request.GET.get('search', None)
            print("search is:", search)
        except:
            search = None

        if search is not None:
                
                print("--- implement your search logic here --")
                
                ## to test 
                ## http://localhost:8000/?search=oxidation%20data
                ## above url represents 'querying with keywords: oxidation data'
                
                print("Received search keywords:", search)

                ## 

                qs = SysDataset.objects.select_related().order_by('-created')[:10]
                ## get the correct dataset with the given keywords

                ##
        else:
            
            if datatype is None:
                qs = SysDataset.objects.select_related().order_by('-created')[:10]
            
            else:
                qs = SysDataset.objects.filter(id=int(datatype)).order_by('-created')[:10]
        
        for obj in qs:
            obj = unpack_dataset_json(obj)
        
        return qs
