from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
import uuid, json, random

from mainpage.models import SysDataset
from mainpage.models import SysUser
from mainpage.models import SysFile

from .utils import *

def update(request, dataset_id):
    # for POST request, apply changes to the database
    if request.method == 'POST':
        post_data = request.POST
        description_tosave = post_data['input-description-tosave']
        d = SysDataset.objects.filter(id=dataset_id)[0]
        properties = json.loads(d.properties)
        properties['description'] = description_tosave
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
