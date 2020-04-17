from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseNotFound
import uuid, json, random

from mainpage.models import SysDataset
from mainpage.models import SysUser
from mainpage.models import SysFile

from .utils import *

def create(request):
    if request.method == 'POST':
        post_data = request.POST

        title = post_data['sysdataset-title']
        subtitle = clean_recieved_val(post_data['sysdataset-subtitle'])
        description = clean_recieved_val(post_data['sysdataset-description'])
        try:
            keywords = post_data['sysdataset-keywords'].split(",")
            keywords = clean_keywords(keywords)
        except:
            keywords = None

        print(title,subtitle,description,keywords)  
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

        return render(request, 'mainpage/create.html', {'dataset': dataset})
    else:
        return HttpResponseNotFound("Page not found")
