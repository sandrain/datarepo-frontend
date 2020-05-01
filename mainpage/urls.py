from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^dataset/(?P<dataset_id>[0-9]+)/$', views.dataset_manage),
    url(r'^dataset/$', views.dataset_create),
    url(r'^user/(?P<user_id>[A-Za-z0-9]+)/$', views.user_manage),
]
