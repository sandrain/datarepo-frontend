from django import template
from django.db.models import Count
from sdifrontend.apps.mainpage.models import SubjectIndex
from sdifrontend.apps.mainpage.models import SysDataset
from sdifrontend.apps.mainpage.models import SidebarMenu

register = template.Library()

@register.simple_tag(takes_context=True)

def get_sidebar_items(context, **kwargs):
    sb = SidebarMenu()
    count_data_by_subject = list(SubjectIndex.objects.values('category_id').order_by('category_id').annotate(count=Count('category_id')))
    count_data_by_type = list(SysDataset.objects.values('type').order_by('type').annotate(count=Count('type')))
    for item in count_data_by_subject:
        sb.nav_elements[0]['items'][item['category_id']]['count'] = item['count']
    for item in count_data_by_type:
        sb.nav_elements[1]['items'][item['type']]['count'] = item['count']
        
    for i in range(0,len(sb.nav_elements[0]['items'])):
        try:
            sb.nav_elements[0]['items'][i]['count']
        except:
            sb.nav_elements[0]['items'][i]['count'] = 0

    for i in range(0,len(sb.nav_elements[1]['items'])):
        try:
            sb.nav_elements[1]['items'][i]['count']
        except:
            sb.nav_elements[1]['items'][i]['count'] = 0

    sb.nav_elements[0]['items'] = sorted(sb.nav_elements[0]['items'], key=lambda k: k['count'], reverse=True) 
    sb.nav_elements[1]['items'] = sorted(sb.nav_elements[0]['items'], key=lambda k: k['count'], reverse=True) 

    return sb.nav_elements

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
    sb = SidebarMenu()
    items = sb.nav_elements[0]['items']

    options = []
    for item in items:
        o = ("{}".format(items.index(item)), item['name'])
        options.append(o)
    return options
