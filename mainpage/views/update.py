from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
import uuid, json, random

from mainpage.models import SysDataset
from mainpage.models import SysUser
from mainpage.models import SysFile
from django.http import HttpResponse
from django.template import loader

from .utils import *

def delete(request, dataset_id):
    
    # for POST request, apply changes to the database
    if request.method == 'POST':
        post_data = request.POST
        d = SysDataset.objects.filter(id=dataset_id)[0]
        d.delete()

        qs = SysDataset.objects.select_related().order_by('-created')[:10]
        for obj in qs:
            obj = unpack_dataset_json(obj)
        
        template = loader.get_template('mainpage/index.html')
        context = {
            'latest_dataset_list': qs,
        }

        return HttpResponse(template.render(context, request))

def update(request, dataset_id):
    # for POST request, apply changes to the database
    if request.method == 'POST':
        post_data = request.POST
        description_tosave = post_data['input-description-tosave']
        url_tosave = post_data['input-url-tosave']
        email_tosave = post_data['input-email-tosave']
        keywords_tosave = post_data['input-keywords-tosave']
        institution_tosave = post_data['input-institution-tosave']
        
        print(description_tosave, url_tosave, email_tosave, keywords_tosave, institution_tosave)

        d = SysDataset.objects.filter(id=dataset_id)[0]
        properties = json.loads(d.properties)
        properties['description'] = description_tosave
        properties['url'] = url_tosave
        properties['institution'] = institution_tosave
        properties['keywords'] = clean_keywords(make_keywords_list(keywords_tosave))

        o = SysDataset.objects.filter(id=dataset_id)[0].owner
        o.email = email_tosave
        o.save()

        d.properties = json.dumps(properties)

        d.save()

        dataset = unpack_dataset_json(get_object_or_404(
                    SysDataset.objects.select_related(), id=dataset_id))
        return render(request, 'mainpage/detail.html', {'dataset': dataset})
    else:
        # otherwise, display the editable page
        dataset = unpack_dataset_json(get_object_or_404(
            SysDataset.objects.select_related(), id=dataset_id))
        return render(request, 'mainpage/update.html', {'dataset': dataset})
