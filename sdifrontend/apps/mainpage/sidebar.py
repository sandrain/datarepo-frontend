# -*- coding: utf-8 -*-

from django import template
from django.db.models import Count
from sdifrontend.apps.mainpage.models import SubjectIndex
from sdifrontend.apps.mainpage.models import SysDataset, Category, SidebarMenu

register = template.Library()

@register.simple_tag(takes_context=True)

def get_sidebar_items(context, **kwargs):
    # get the categories
    nav_elements = [{
                'name': "Data Subject",
                'id':'category',
                'items': []
            },{
                'name': "Data Type",
                'id':'type',
                'items': [
                    {'name': "Animations/Simulations"},
                    {'name': "Genome/Genetic Data"},
                    {'name': "Interactive Data Map"},
                    {'name': "Numeric Data"},
                    {'name': "Still Images/Photos"},
                    {'name': "Figures/Plots"},
                    {'name': "Specialized Mix"},
                    {'name': "Multimedia"},
                    {'name': "General (Other)"}
                ]
            }]
    
    for category in Category.objects.all().annotate(count=Count('sysdataset')).order_by('-count'):
        nav_elements[0]['items'].append({'id': category.id, 'name': category.name, 'count': category.count, 'section': "category"})
    
    count_data_by_type = list(SysDataset.objects.values('type').annotate(count=Count('type')).order_by('type'))
    
    for item in count_data_by_type:
        nav_elements[1]['items'][item['type']]['count'] = item['count']

    for i in range(0,len(nav_elements[1]['items'])):
        try:
            nav_elements[1]['items'][i]['count']
        except:
            nav_elements[1]['items'][i]['count'] = 0
        
        nav_elements[1]['items'][i]['section'] = "type"
        nav_elements[1]['items'][i]['id'] = i

    return nav_elements

@register.simple_tag(takes_context=True)
def get_ds_types(context, **kwargs):
    sb = SidebarMenu()
    items = sb.nav_elements[1]['items']
    options = []
    for item in items:
        o = ('0', item['name'])
        options.append(o)
    return options



@register.simple_tag(takes_context=True)
def get_ds_subjects(context, **kwargs):
    options = []
    for category in Category.objects.all():
        o = ("{}".format(category.id), category.name)
        options.append(o)
    return options

def get_ds_subjects_list(context, **kwargs):
    return {}