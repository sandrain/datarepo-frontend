"""sdifrontend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

import sdifrontend.apps.mainpage.views as mp

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^main/', mp.IndexView.as_view()),
    url(r'', include('sdifrontend.apps.landingpage.url')),
    url(r'^dataset/(?P<dataset_id>[0-9]+)/$', mp.dataset_manage),
    url(r'^dataset/$', mp.dataset_create),
    url('user/', mp.UserView.as_view()),
    url(r'^search/$', mp.IndexView.as_view()),
    url('', include('sdifrontend.apps.news.urls')),
    url('', include('django.contrib.auth.urls')),
    url('', include('social_django.urls', namespace='social'))
]
