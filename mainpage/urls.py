from django.conf.urls import url

from . import views

urlpatterns = [
    url('', views.IndexView.as_view(), name='index'),
    url(r'<int:pk>/', views.DetailView.as_view(), name='detail'),
    ]
