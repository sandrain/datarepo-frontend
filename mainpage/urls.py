#from django.urls import path
#
#from . import views
#
#app_name = 'mainpage'
#urlpatterns = [
#    path('', views.IndexView.as_view(), name='index'),
#    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
#]

from django.conf.urls import url

from . import views

urlpatterns = [
    url('', views.IndexView.as_view(), name='index'),
    url(r'<int:pk>/', views.DetailView.as_view(), name='detail'),
    ]
