from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.template import loader
from mainpage.models import SysDataset
from django.http import HttpResponseNotFound
from django.http import HttpResponse
from mainpage.models import *
import random

from .utils import *


def user_manage(request, user_id):

    if request.method == 'GET':

        try:
            update = request.GET['update']
        except:
            update = 0

        user = get_object_or_404(SysUser.objects.select_related(),
                                username=user_id)

        user_id = SysUser.objects.filter(username=user_id)[0].id
        user_dataset_list = SysDataset.objects.filter(owner=user_id).order_by('-created')[:10]

        for obj in user_dataset_list:
            obj = unpack_dataset_json(obj)
        
        return render(request, 'mainpage/user/profile.html', {'user': user, 'user_dataset_list':user_dataset_list})


