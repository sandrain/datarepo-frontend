from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^dataset/(?P<dataset_id>[0-9]+)/$', views.manage),
    url(r'^dataset/$', views.create),
]
