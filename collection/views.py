from django.shortcuts import render, redirect
from collection.models import Part
from collection.forms import PartForm
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import FormView 
from collections import defaultdict
import json

# Create your views here.
def index(request):
    parts = Part.objects.all()
    partDistinct = Part.objects.order_by("CATEGORY").values_list("CATEGORY", flat=True).distinct()
    j = 0
    partDict = defaultdict(list, flat=True)
    test = partDistinct[5]
    while j < len(partDistinct):
        currentCat = partDistinct[j]
        numList = list(Part.objects.filter(CATEGORY=currentCat).order_by("NUMBER").values_list("NUMBER", flat=True).distinct())
        lenNumList = len(numList)
        k = 0
        while k < lenNumList:
            currentNum = numList[k]
            partDict[currentCat].append(currentNum)
            k = k + 1
        j = j + 1
    jsonDict = json.dumps(partDict)
    return render(request, 'index.html', { 
        'parts': parts,
        'jsonDict': jsonDict,
        'numList': numList,
        'partDistinct': partDistinct,
        'partDict': partDict,
        'currentCat': currentCat,
        'test': test,
    })
    

def part_detail(request, Slug): 
    # grab the object... 
    part = Part.objects.get(Slug=Slug) 
    # and pass to the template 
    return render(request, 'parts/part_detail.html', { 
        'part': part, 
        'Slug': Slug,
    })

#editing view
def edit_part(request, Slug): 
    # grab the object 
    part = Part.objects.get(Slug = Slug) 
    # set the form we're using 
    form_class = PartForm
    # if we're coming to this view from a submitted form 
    if request.method == 'POST': 
        # grab the data from the submitted form and apply to 
        # the form 
        form = form_class(data = request.POST, instance = part) 
        if form.is_valid(): 
            # save the new data 
            form.save() 
            return redirect('part_detail',Slug=part.Slug) 
    # otherwise just create the form 
    else: 
        form = form_class(instance = part)
    # and render the template 
    return render(request, 'parts/edit_part.html', { 
        'part': part, 
        'form': form, 
    })

