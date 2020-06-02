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
from django.urls import path, include
from django.contrib import admin

import sdifrontend.apps.mainpage.views as mp

urlpatterns = [
    path('', include('sdifrontend.apps.landingpage.url')),
    path('', include('sdifrontend.apps.news.urls')),
    path('', include('sdifrontend.apps.mainpage.urls')),
    path('', include('django.contrib.auth.urls')),
    path('', include('social_django.urls', namespace='social')),
    path(r'admin/', admin.site.urls),
    path(r'user/<username>/', mp.UserView.as_view()),
    path(r'search/', mp.IndexView.as_view()),
]
