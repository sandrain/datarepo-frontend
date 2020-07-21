from django.urls import path

from sdifrontend.apps.news import views

app_name = 'news'

urlpatterns = [
    path('news', views.NewsView.as_view(), name='index'),
]