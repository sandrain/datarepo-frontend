import json
from django import template
from sdifrontend.apps.mainpage.models import SearchIndex
from sdifrontend.apps.mainpage.models import SysDataset
register = template.Library()

def full_scan_create_index():
    SearchIndex.objects.all().delete() ## remove all search index items
    alldataset = SysDataset.objects.all()
    dataset_idx = 0
    for dataset in alldataset:
        if dataset_idx%50==0:
            print("Indexing dataset ", dataset_idx)
        dataset_idx+=1
        props = json.loads(dataset.properties)
        for key in props.keys():
            if key=="keywords":
                vals = ""
                for item in props[key]:
                    vals+=item+" "
            else:
                vals = props[key]
                
            if key == "keywords" or key == "title" or key == "subtitle":
                terms = vals.lower().split(" ")

                for term in terms:
                    si = SearchIndex(attribute = key, value = ''.join(e for e in term if e.isalnum()), dataset = dataset)
                    si.save()

@register.simple_tag(takes_context=True)
def get_tag_cloud_keywords(context, **kwargs):
    if SearchIndex.objects.all().count()==0:
        full_scan_create_index()        

    keywords = list(SearchIndex.objects.filter(attribute='keywords').values_list('value', flat=True))[:100]
    keywords = ' '.join(word for word in keywords)

    return keywords
