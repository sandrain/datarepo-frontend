from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.http import HttpResponseNotFound
from django.http import HttpResponse
import random

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, Group


from django.views.generic import TemplateView
from django.shortcuts import render

from sdifrontend.apps.mainpage.models import SysDataset, SysUser
from .utils import unpack_dataset_json
import logging

class UserView(TemplateView):
    user = None

    def get(self, request, *args, **kwargs):
        logger = logging.getLogger("django")
        #user = request.user.social_auth.get(provider='globus').username

        try:
            user = SysUser.objects.get(username=request.user.username)
        except ObjectDoesNotExist:
            # We have no dataset for this user yet
            # login trough globus
            logger.info("Creating new user: {}".format(request.user.username))
            user = SysUser.objects.create(username=request.user.username,
                                          email = request.user.email)

        u = User.objects.get(username=request.user.username)
        #u.groups.add("superuser")
        objs = Group.objects.all()
        for o in objs:
            print(o)

        #user_id = SysUser.objects.filter(username=user_id)[0].id
        #user_dataset_list = SysDataset.objects.filter(owner=user_id).order_by('-created')[:10]

        #for obj in user_dataset_list:
        #    obj = unpack_dataset_json(obj)

        #return render(request, 'mainpage/user/profile.html', { 'bio': user_data.bio } )
        return render(request, 'mainpage/user/profile.html')


