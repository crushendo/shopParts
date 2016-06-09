from django.contrib import admin 
# import your model 
from collection.models import Part 

# set up automated slug creation
class PartAdmin(admin.ModelAdmin): 
    model = Part 
    list_display = ('id', 'CATEGORY', 'NUMBER', 'PART_NUM',) 
    prepopulated_fields = {'Slug': ('CATEGORY',)}

# and register it 
admin.site.register(Part, PartAdmin)
