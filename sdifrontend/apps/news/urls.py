from django.urls import path

from sdifrontend.apps.news import views

urlpatterns = [
    path('news', views.NewsView.as_view()),
]