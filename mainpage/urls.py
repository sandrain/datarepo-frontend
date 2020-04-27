from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<dataset_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^update/(?P<dataset_id>[0-9]+)/$', views.update, name='update'),
    url(r'^delete/(?P<dataset_id>[0-9]+)/$', views.delete, name='delete'),
    url(r'^create/', views.create, name='create'),
]
