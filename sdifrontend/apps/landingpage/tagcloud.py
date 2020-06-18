import json
from django import template
from sdifrontend.apps.mainpage.models import SearchIndex
from sdifrontend.apps.mainpage.models import SysDataset
from django.db.models import Q

register = template.Library()

def full_scan_create_index():
    SearchIndex.objects.all().delete() ## remove all search index items
    alldataset = SysDataset.objects.all()
    dataset_idx = 0
    for dataset in alldataset:
        dataset.create_index()

@register.simple_tag(takes_context=True)
def get_tag_cloud_keywords(context, **kwargs):
    if SearchIndex.objects.all().count()==0:
        full_scan_create_index()        

    keywords = list(SearchIndex.objects.filter(Q(attribute='keywords')|Q(attribute='subject')).values_list('value', flat=True))[:100]
    keywords = ' '.join(word for word in keywords)

    return keywords
