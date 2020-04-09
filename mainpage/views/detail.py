from django.shortcuts import render
from django.shortcuts import get_object_or_404, render

from mainpage.models import SysDataset
from mainpage.models import SysUser
import random

from .utils import *

def detail(request, dataset_id):
    dataset = unpack_dataset_json(
                get_object_or_404(SysDataset.objects.select_related(),
                                  id=dataset_id))

    return render(request, 'mainpage/detail.html', {'dataset': dataset})


