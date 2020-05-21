from django.contrib import admin

# Register your models here.
from .models import SysDataset
from .models import SysUser

admin.site.register(SysDataset)
admin.site.register(SysUser)
