# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse


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


class SysDataset(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(unique=True, max_length=36)
    owner = models.ForeignKey('SysUser', on_delete=models.SET_NULL, blank=True, null=True)
    public = models.IntegerField(blank=True, null=True)
    size = models.BigIntegerField(blank=True, null=True)
    icon = models.CharField(max_length=256, blank=True, null=True)
    category = models.IntegerField(default=0)
    type = models.IntegerField(default=0)
    properties = models.TextField(blank=True, null=True)
    structure = models.TextField(blank=True, null=True)
    created = models.DateTimeField(null=False, auto_now=True)
    updated = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        #managed = False
        db_table = 'sys_dataset'

    def get_absolute_url(self):
        return reverse('mainpage:dataset-detail', kwargs={'pk': self.pk})


class SysFile(models.Model):
    id = models.BigAutoField(primary_key=True)
    dataset = models.ForeignKey(SysDataset, on_delete=models.CASCADE)
    name = models.CharField(max_length=512)
    size = models.BigIntegerField(blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'sys_file'


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
