from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
import uuid, json, random

from mainpage.models import SysDataset
from mainpage.models import SysUser
from mainpage.models import SysFile

from .utils import *

def update(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        post_data = request.POST

        ## currently we are generating fake fields other than the title
        properties = generate_fake_dataset_properties(post_data['sysdataset_title'])
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

        return render(request, 'mainpage/update.html', {'dataset': dataset})

    dataset = unpack_dataset_json(
                get_object_or_404(SysDataset.objects.select_related(), id=690))
    return render(request, 'mainpage/update.html', {'dataset': dataset})

