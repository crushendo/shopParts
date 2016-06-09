from __future__ import unicode_literals

from django.db import models
class Part(models.Model): 
    AUTONUM = models.TextField() 
    CATEGORY = models.TextField(default = ' ') 
    NUMBER = models.TextField(default = ' ')
    PART_NUM = models.TextField(default = ' ')
    PART_DESC = models.TextField(default = ' ')
    Slug = models.SlugField(unique = True)
