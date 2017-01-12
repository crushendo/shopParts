from __future__ import unicode_literals
from django import forms
from django.db import models


class Part(models.Model):
    AUTONUM = models.TextField(blank=True) 
    CATEGORY = models.TextField(default = ' ', blank=True) 
    NUMBER = models.TextField(default = ' ', blank=True)
    PART_NUM = models.TextField(default = ' ', blank=True)
    PART_DESC = models.TextField(default = ' ', blank=True)
    Slug = models.SlugField(unique = True, blank=True, primary_key=True)
    pass  

def dynamic_path(instance, fileName):
    name = fileName
    getname = instance.relSlug
    part=Part()
    file_path = 'media/{Slug}/{name}'.format(Slug=instance.relSlug, name=fileName) 
    return file_path
        
class Document(models.Model):
    part = models.ForeignKey(Part)
    relSlug = models.SlugField(unique = True, blank=True, primary_key=True)
    imageName = models.FileField(upload_to=dynamic_path)  

    
    
    
