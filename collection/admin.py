from django.contrib import admin 
# import your model 
from collection.models import Category 

# set up automated slug creation
class CategoryAdmin(admin.ModelAdmin): 
    model = Category 
    list_display = ('name', 'description',) 
    prepopulated_fields = {'slug': ('name',)}

# and register it 
admin.site.register(Category, CategoryAdmin)
