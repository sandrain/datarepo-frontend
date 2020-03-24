from django.conf.urls import url
from . import views

urlpatterns = [
    
    #url(r'', views.IndexView.as_view(), name='index'),
    #url(r'<int:pk>/', views.DetailView.as_view(), name='detail'),
    #path(r'<int:dataset_id>/', views.detail, name='detail'),

    #url(r'^$', views.index, name='index'),
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<dataset_id>[0-9]+)/$', views.detail, name='detail'),

    ]
