from django.shortcuts import render

# Create your views here.

from django.views.generic import TemplateView
from django.shortcuts import render

class NewsView(TemplateView):
   template_name = 'news.html'
