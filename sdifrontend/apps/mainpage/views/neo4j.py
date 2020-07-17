from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.http import HttpResponseNotFound
from django.http import HttpResponse
import random
from django.http import JsonResponse

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, Group


from django.views.generic import TemplateView
from django.shortcuts import render

from sdifrontend.apps.mainpage.models import SysDataset, SysUser
from .utils import unpack_dataset_json
import logging
from py2neo import Database
from py2neo import Graph
import json



graph = Graph(host="neo4j", auth=('neo4j','1234'))

def get_similar_datasets(request):
    
    dataset_id = request.GET.get('dataset', None)
    data = {}
    query = '''MATCH (n:Dataset)-[:hasKeyword]->(k)<-[:hasKeyword]-(m:Dataset) 
        where n.id='{0}' and n<>m
        RETURN m.id as id, m.title as title, count(*) as cnt order by cnt desc limit 10 
        '''
    
    query = query.format(dataset_id)
    data['result'] = graph.run(query).data()

    return JsonResponse(data)