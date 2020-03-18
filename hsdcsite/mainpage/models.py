from django.db import models

# Create your models here.

class DataSet(models.Model):
    
    # general information
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    keywords = models.CharField(max_length=100)
    product_nos = models.CharField(max_length=100)
    contract_nos = models.CharField(max_length=100)
    originating_research_org = models.CharField(max_length=100)
    sponsor_org = models.CharField(max_length=100)
    contributor_organizations = models.CharField(max_length=100)
    publication_date = models.DateTimeField('date created')
    lanaguage = models.CharField(max_length=100)   
    country = models.CharField(max_length=100)   
    site_url = models.CharField(max_length=100)
    contact_name = models.CharField(max_length=100) 
    contact_org = models.CharField(max_length=100)   
    contact_email = models.CharField(max_length=100)
    other_identifying_nos = models.CharField(max_length=100)   
    doi_infix = models.CharField(max_length=100)   
    software_needed = models.CharField(max_length=100)   
    subject_categories_code = models.CharField(max_length=100)   
    creatorsblock = models.CharField(max_length=100)   
    downloads_int = models.IntegerField(default = 0)
    citations_int = models.IntegerField(default = 0)
    value_int = models.IntegerField(default = 0)
    uniqueness_int = models.IntegerField(default = 0)

    def __str__(self):
        return self.title
