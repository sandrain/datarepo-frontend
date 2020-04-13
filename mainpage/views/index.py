from django.views import generic
import random, json, uuid

from mainpage.models import SysDataset
from mainpage.models import SysUser

from .utils import *

class IndexView(generic.ListView):
    template_name = 'mainpage/index.html'
    context_object_name = 'latest_dataset_list'

    def get_queryset(self):
        # Get ten recent datasets.
        qs = SysDataset.objects.select_related().order_by('-created')[:10]
        for obj in qs:
            obj = unpack_dataset_json(obj)
        return qs

