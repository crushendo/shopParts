from django.shortcuts import render
from collection.models import Category

# Create your views here.
def index(request):
    number = 6
    categories = Category.objects.all()
    
    return render( request, 'index.html', { 
        'number': number,
        'categories': categories,
    })
