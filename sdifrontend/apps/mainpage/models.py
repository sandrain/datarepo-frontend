# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals
import json
from django.db import models
from django.urls import reverse
from django.contrib.postgres.fields import JSONField

class DoiAuthor(models.Model):
    id = models.BigAutoField(primary_key=True)
    doi_record = models.ForeignKey('DoiRecord', models.DO_NOTHING)
    user = models.ForeignKey('SysUser', models.DO_NOTHING)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    organization = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'doi_author'


class DoiRecord(models.Model):
    id = models.BigAutoField(primary_key=True)
    dataset = models.ForeignKey('SysDataset', models.DO_NOTHING)
    doi = models.CharField(max_length=64, blank=True, null=True)
    suid = models.BigIntegerField()
    title = models.TextField(blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    site_url = models.TextField(blank=True, null=True)
    olcf_project_id = models.CharField(max_length=8, blank=True, null=True)
    dataset_type = models.CharField(max_length=1024, blank=True, null=True)
    subjects = models.TextField(blank=True, null=True)
    product_nos = models.CharField(max_length=255, blank=True, null=True)
    doe_contract_nos = models.CharField(max_length=255, blank=True, null=True)
    other_contract_nos = models.CharField(max_length=255, blank=True, null=True)
    origin_orgs = models.CharField(max_length=1024, blank=True, null=True)
    sponsor_orgs = models.CharField(max_length=1024, blank=True, null=True)
    contrib_orgs = models.CharField(max_length=1024, blank=True, null=True)
    software_needed = models.CharField(max_length=1024, blank=True, null=True)
    other_id_nos = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.DateTimeField()
    publish_time = models.DateTimeField(blank=True, null=True)
    language = models.CharField(max_length=8, blank=True, null=True)
    country = models.CharField(max_length=2, blank=True, null=True)
    doi_infix = models.CharField(max_length=8, blank=True, null=True)
    contact_name = models.CharField(max_length=64, blank=True, null=True)
    contact_org = models.CharField(max_length=64, blank=True, null=True)
    contact_email = models.CharField(max_length=255, blank=True, null=True)
    contact_phone = models.CharField(max_length=32, blank=True, null=True)
    request_status = models.CharField(max_length=12, blank=True, null=True)
    data_status = models.CharField(max_length=15, blank=True, null=True)
    admin_suid = models.BigIntegerField(blank=True, null=True)
    admin_comments = models.TextField(blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'doi_record'


class SidebarMenu:
    def __init__(self):
        self.nav_elements = [
            {
                'name': "Data Subject",
                'id':'category',
                'items': [
                    {'name': "Coal, Lignite, and Peat"},
                    {'name': "Petroleum"},
                    {'name': "Natural Gas"},
                    {'name': "Oil Shales And Tar Sands"},
                    {'name': "Isotope And Radiation Sources"},
                    {'name': "Hydrogen"},
                    {'name': "Biomass Fuels"},
                    {'name': "Synthetic Fuels"},
                    {'name': "Nuclear Fuel Cycle And Fuel Materials"},
                    {'name': "Management Of Radioactive And Non-Radioactive Wastes From Nuclear Facilities"},
                    {'name': "Hydro Energy"},
                    {'name': "Solar Energy"},
                    {'name': "Geothermal Energy"},
                    {'name': "Tidal And Wave Power"},
                    {'name': "Wind Energy"},
                    {'name': "Fossil-Fueled Power Plants"},
                    {'name': "Specific Nuclear Reactors And Associated Plants"},
                    {'name': "General Studies Of Nuclear Reactors"},
                    {'name': "Power Transmission And Distribution"},
                    {'name': "Energy Storage"},
                    {'name': "Energy Planning, Policy, And Economy"},
                    {'name': "Direct Energy Conversion"},
                    {'name': "Energy Conservation, Consumption, And Utilization"},
                    {'name': "Advanced Propulsion Systems"},
                    {'name': "Materials Science"},
                    {'name': "Inorganic, Organic, Physical, And Analytical Chemistry"},
                    {'name': "Radiation Chemistry, Radiochemistry, And Nuclear Chemistry"},
                    {'name': "Engineering"},
                    {'name': "Particle Accelerators"},
                    {'name': "Military Technology, Weaponry, And National Defense"},
                    {'name': "Instrumentation Related To Nuclear Science And Technology"},
                    {'name': "Other Instrumentation"},
                    {'name': "Environmental Sciences"},
                    {'name': "Geosciences"},
                    {'name': "Basic Biological Sciences"},
                    {'name': "Applied Life Sciences"},
                    {'name': "Radiation Protection And Dosimetry"},
                    {'name': "Radiology And Nuclear Medicine"},
                    {'name': "Radiation, Thermal, And Other Environ. Pollutant Effects On Living Orgs. And Biol. Mat."},
                    {'name': "Plasma Physics And Fusion Technology"},
                    {'name': "Classical And Quantum Mechanics, General Physics"},
                    {'name': "Physics Of Elementary Particles And Fields"},
                    {'name': "Nuclear Physics And Radiation Physics"},
                    {'name': "Atomic And Molecular Physics"},
                    {'name': "Condensed Matter Physics, Superconductivity And Superfluidity"},
                    {'name': "Nanoscience And Nanotechnology"},
                    {'name': "Astronomy And Astrophysics"},
                    {'name': "Knowledge Management And Preservation"},
                    {'name': "Mathematics And Computing"},
                    {'name': "Nuclear Disarmament, Safeguards, And Physical Protection"},
                    {'name': "General And Miscellaneous"}
                ]
            }, {
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
            }
        ]

class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(blank=True, null=True)

class SysDataset(models.Model):

    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(unique=True, max_length=36)
    owner = models.ForeignKey('SysUser', on_delete=models.SET_NULL, blank=True, null=True)
    public = models.IntegerField(blank=True, null=True)
    size = models.BigIntegerField(blank=True, null=True)
    icon = models.CharField(max_length=256, blank=True, null=True)
    categories = models.ManyToManyField(Category)
    type = models.IntegerField(default=0)
    properties = JSONField(blank=True, null=True)
    structure = models.TextField(blank=True, null=True)
    created = models.DateTimeField(null=False, auto_now=True)
    updated = models.DateTimeField(blank=True, null=True, auto_now=True)

    title = None
    subtitle = None
    description = None
    keywords = None
    subject = 0

    class Meta:
        #managed = False
        db_table = 'sys_dataset'

    # @classmethod
    # def from_db(cls, db, field_names, values):
    #     instance = super().from_db(db, field_names, values)

    #     instance.title = instance.properties['title']
    #     instance.subtitle = instance.properties['subtitle']
    #     instance.description = instance.properties['description']
    #     instance.keywords = instance.properties['keywords']
    #     instance.attributes = instance.properties

    #     return instance

    def get_absolute_url(self):
        return reverse('mainpage:dataset-detail', kwargs={'pk': self.pk})

    def create_index(self):
        props = self.properties

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
                    si = SearchIndex(attribute = key, value = ''.join(e for e in term if e.isalnum()), dataset = self)
                    si.save()

        # indexing subject
        for item in self.categories.all():
            print(item.name)
            terms = item.name.lower().split(" ")
            for term in terms:
                si = SearchIndex(attribute = 'subject', value = ''.join(e for e in term if e.isalnum()), dataset = self)
                si.save()
                
        # indexing type
        for item in self.categories.all():
            terms = item.name.lower().split(" ")
            for term in terms:
                si = SearchIndex(attribute = 'type', value = ''.join(e for e in term if e.isalnum()), dataset = self)
                si.save()
    
            ci = SubjectIndex(dataset = self, category_id = item.id )
            ci.save()

    def remove_index(self):
        SearchIndex.objects.filter(dataset = self).delete()
        SubjectIndex.objects.filter(dataset = self).delete()


class SysFile(models.Model):
    id = models.BigAutoField(primary_key=True)
    dataset = models.ForeignKey(SysDataset, on_delete=models.CASCADE)
    name = models.CharField(max_length=512)
    size = models.BigIntegerField(blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'sys_file'

class SubjectIndex(models.Model):
    id = models.BigAutoField(primary_key=True)
    dataset = models.ForeignKey(SysDataset, on_delete=models.CASCADE)
    category_id = models.IntegerField()

    class Meta:
        #managed = False
        db_table = 'subject_index'

class SearchIndex(models.Model):
    id = models.BigAutoField(primary_key=True)
    attribute = models.CharField(max_length=512)
    value = models.CharField(max_length=512)
    dataset = models.ForeignKey(SysDataset, on_delete=models.CASCADE)
    
    class Meta:
        #managed = False
        db_table = 'search_index'

class SysPermission(models.Model):
    dataset = models.ForeignKey(SysDataset, on_delete=models.CASCADE)
    user = models.ForeignKey('SysUser', models.DO_NOTHING)
    writable = models.IntegerField(blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'sys_permission'
        unique_together = (('dataset', 'user'),)


class SysUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=128)
    email = models.CharField(unique=True, max_length=256)
    displayname = models.CharField(max_length=128, blank=True, null=True)
    bio = models.CharField(max_length=1024, blank=True, null=True)
    profilephoto = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'sys_user'
