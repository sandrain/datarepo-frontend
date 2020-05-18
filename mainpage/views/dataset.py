from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.template import loader
from mainpage.models import SysDataset
from django.http import HttpResponseNotFound
from django.http import HttpResponse
from mainpage.models import *
import random

from .utils import *

def dataset_create(request):

    if request.method == 'POST':
        post_data = request.POST
        print(post_data)

        ###
        try:
            dataset_type = post_data['sysdataset-type']
        except:
            dataset_type = ''

        try:
            subjects = post_data['sysdataset-subjects'] # list
        except:
            subjects = None
            
        title = post_data['sysdataset-title']
        subtitle = clean_recieved_val(post_data['sysdataset-subtitle'])
        description = clean_recieved_val(post_data['sysdataset-description'])

        try:
            keywords = post_data['sysdataset-keywords'].split(",")
            keywords = clean_keywords(keywords)
        except:
            keywords = None

        ## currently we are generating fake fields other than the title
        properties = generate_fake_dataset_properties(post_data['sysdataset-title'], subtitle = subtitle, description = description, keywords = keywords)
        files = generate_fake_dataset_files()
        structure = json.dumps({'data': files})
        size = sum(f['size'] for f in files)

        d = SysDataset(properties=properties,
                    uuid=str(uuid.uuid4()),
                    owner=SysUser.objects.all()[random.randint(1,100)],
                    size=size,
                    structure=structure)
        d.save()

        # populate dataset files
        for f in files:
            r = SysFile(dataset=d,
                        name=f['name'],
                        size=f['size'])
            r.save()

        dataset = unpack_dataset_json(
                    get_object_or_404(SysDataset.objects.select_related(), id=d.id))

        return render(request, 'mainpage/dataset/detail.html', {'dataset': dataset})

    else:
        qs = SysDataset.objects.select_related().order_by('-created')[:10]
        for obj in qs:
            obj = unpack_dataset_json(obj)
        template = loader.get_template('mainpage/index.html')
        context = {
            'latest_dataset_list': qs,
        }

        return HttpResponse(template.render(context, request))

def dataset_manage(request, dataset_id):

    if request.method == 'POST':

        post_data = request.POST

        if post_data['request-type']=='update':
            description_tosave = post_data['input-description-tosave']
            url_tosave = post_data['input-url-tosave']
            email_tosave = post_data['input-email-tosave']
            keywords_tosave = post_data['input-keywords-tosave']
            institution_tosave = post_data['input-institution-tosave']

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
            
            return render(request, 'mainpage/dataset/detail.html', {'dataset': dataset})

        elif post_data['request-type']=='delete':
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

    elif request.method == 'GET':

        try:
            update = request.GET['update']
        except:
            update = 0

        if update=='1':
            dataset = unpack_dataset_json(
                get_object_or_404(SysDataset.objects.select_related(),
                                  id=dataset_id))

            return render(request, 'mainpage/dataset/update.html', {'dataset': dataset})

        else:

            dataset = unpack_dataset_json(
                    get_object_or_404(SysDataset.objects.select_related(),
                                    id=dataset_id))

            return render(request, 'mainpage/dataset/detail.html', {'dataset': dataset})


