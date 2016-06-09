from django.shortcuts import render
from collection.models import Part

# Create your views here.
def index(request):
    parts = Part.objects.all()
    
    
    return render( request, 'index.html', { 
        'PAR_NUM': parts,
    })
