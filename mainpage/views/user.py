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

            return render(request, 'mainpage/user/profile.html', {'user': user})


