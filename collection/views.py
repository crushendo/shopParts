from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from collection.models import Part
from collection.forms import PartForm
from collection.forms import addPartForm
from collection.forms import UploadFileForm
from collection.models import Document
from django.shortcuts import render_to_response
from collection.forms import DocumentForm
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import FormView 
from collections import defaultdict
from django.shortcuts import get_object_or_404
import json
import os
from django.db.models.functions import Lower

#Homepage
def index(request):
    parts = Part.objects.all()
    partDistinct = Part.objects.exclude(CATEGORY__isnull=True).exclude(CATEGORY__iexact=' ').exclude(CATEGORY__iexact='  ').exclude(CATEGORY__iexact='').order_by(Lower("CATEGORY")).values_list("CATEGORY", flat=True).distinct()
    j = 0
    partDict = defaultdict(list, flat=True)
    while j < len(partDistinct):
        currentCat = partDistinct[j]
        numList = list(Part.objects.filter(CATEGORY__iexact=currentCat).order_by(Lower("NUMBER")).values_list("NUMBER", flat=True).distinct())
        lenNumList = len(numList)
        k = 0
        while k < lenNumList:
            currentNum = numList[k]
            partDict[currentCat].append(currentNum)
            k = k + 1
        j = j + 1
    form_class = PartForm
    if request.method == 'POST': 
        # grab the data from the submitted form and apply to 
        # the form 
        form = form_class(data = request.POST) 
        if form.is_valid(): 
            # save the new data 
            form.save() 
            return redirect('parts/list') 
    else: 
        form = form_class()
    jsonDict = json.dumps(partDict)
    return render(request, 'index.html', { 
        'parts': parts,
        'form': form,
        'jsonDict': jsonDict,
        'numList': numList,
        'partDistinct': partDistinct,
        'partDict': partDict,
        'currentCat': currentCat,
    })
    
def part_list(request):
    if request.method == "POST":   
   	 CATEGORY = str(request.POST.get("CATEGORY"))
   	 NUMBER = str(request.POST.get("NUMBER"))
   	 if request.POST.get("searchType") == 'Equip_Num':
   	     searchType = "NUMBER__icontains"
   	 else:
        	searchType = str(request.POST.get("searchType")) + '__icontains' #case insensitive search
    	 searchValue = str(request.POST.get("searchValue"))
    parts = Part.objects.all()
    #if using the browse function
    if searchValue == '':
        SelectNumStr = str(NUMBER)
        SelectCatStr = str(CATEGORY)
        selectedList = list(Part.objects.filter(NUMBER=SelectNumStr).filter(CATEGORY=SelectCatStr).order_by(Lower("PART_NUM")).values_list("PART_NUM", flat=True))
        slugList = list(Part.objects.filter(NUMBER=SelectNumStr).filter(CATEGORY=SelectCatStr).order_by(Lower("PART_NUM")).values_list("Slug", flat=True))
        descList = list(Part.objects.filter(NUMBER=SelectNumStr).filter(CATEGORY=SelectCatStr).order_by(Lower("PART_NUM")).values_list("PART_DESC", flat=True))
        selectedListjson = json.dumps(selectedList)
        descListjson = json.dumps(descList)
        slugListjson = json.dumps(slugList)
        listLength = len(selectedList)
    #if using the search function
    else:
        NUMBER = ''
        my_filter = {}
        my_filter[searchType] = searchValue
        selectedList = list(Part.objects.filter(**my_filter).order_by(Lower("PART_NUM")).values_list("PART_NUM", flat=True))
        slugList = list(Part.objects.filter(**my_filter).order_by(Lower("PART_NUM")).values_list("Slug", flat=True))
        descList = list(Part.objects.filter(**my_filter).order_by(Lower("PART_NUM")).values_list("PART_DESC", flat=True))
        selectedListjson = json.dumps(selectedList)
        descListjson = json.dumps(descList)
        slugListjson = json.dumps(slugList)
        listLength = len(selectedList)
    
    return render(request, 'parts/part_list.html', {
        'parts': parts,
        'NUMBER': NUMBER,
        'searchValue': searchValue,
        'selectedListjson': selectedListjson,
        'slugListjson': slugListjson,
        'descListjson': descListjson,
        'listLength': listLength,
        'slugList': slugList,
        'selectedList': selectedList,
    })
    
    
def part_detail(request, Slug): 
    searchValue = request.POST.get("searchValue")
    passDesc = list(Part.objects.filter(Slug=Slug).order_by("PART_DESC").values_list("PART_DESC", flat=True));
    if Document.objects.filter(relSlug=Slug).exists():
        filePath = list(Document.objects.filter(relSlug=Slug).order_by("relSlug").values_list("imageName", flat=True)) #needs to run for image only
        filePathEle = filePath[0]
    else:
        filePathEle = ""
    part = Part.objects.get(Slug=Slug)
    form_class = PartForm
    currentDir = os.getcwd()
    # if we're coming to this view from a submitted form 
    if request.method == "POST": 
        # grab the data from the submitted form and apply to 
        # the form 
	CATEGORY = str(request.POST.get("CATEGORY"))
        NUMBER = str(request.POST.get("NUMBER"))
	searchValue = str(request.POST.get("searchValue"))
	if request.POST.get("searchType") == 'Equip_Num':
             searchType = "NUMBER__icontains"
        else:
                searchType = str(request.POST.get("searchType")) + '__icontains' #case insensitive search
        form = form_class(request.POST, instance=part) 
        if form.is_valid():
	    whatDo = request.POST.get("whatDo")
	    if whatDo == "delete": 
            	#Delete row from Parts db
            	deletingPart=Part.objects.get(Slug=Slug)
            	deletingPart.delete()
            	#Delete row from Document db
            	#Check to see if is image
            	descCheck = str(passDesc[0][:7])
            	#Deleting image file from media folder
	
            	if descCheck == 'C:\\fake':
                	deletingDoc = Document.objects.get(relSlug=Slug)
                	deletingDoc.delete()
                	currentDir = os.getcwd()
                	smartPath = currentDir + '/media/' + str(filePathEle)
                	os.remove(smartPath)
	    form = form_class(data = request.POST)
            form.save()
	    parts = Part.objects.all()
            #if using the browse function
    	    if searchValue == '':
       		 SelectNumStr = str(NUMBER)
       		 SelectCatStr = str(CATEGORY)
       		 selectedList = list(Part.objects.filter(NUMBER=SelectNumStr).filter(CATEGORY=SelectCatStr).order_by(Lower("PART_NUM")).values_list("PART_NUM", flat=True))
       		 slugList = list(Part.objects.filter(NUMBER=SelectNumStr).filter(CATEGORY=SelectCatStr).order_by(Lower("PART_NUM")).values_list("Slug", flat=True))
       		 descList = list(Part.objects.filter(NUMBER=SelectNumStr).filter(CATEGORY=SelectCatStr).order_by(Lower("PART_NUM")).values_list("PART_DESC", flat=True))
         	 selectedListjson = json.dumps(selectedList)
        	 descListjson = json.dumps(descList)
       		 slugListjson = json.dumps(slugList)
       		 listLength = len(selectedList)
   	    #if using the search function
    	    else:
      		  NUMBER = ''
      		  my_filter = {}
       	          my_filter[searchType] = searchValue
  		  selectedList = list(Part.objects.filter(**my_filter).order_by(Lower("PART_NUM")).values_list("PART_NUM", flat=True))
  		  slugList = list(Part.objects.filter(**my_filter).order_by(Lower("PART_NUM")).values_list("Slug", flat=True))
  		  descList = list(Part.objects.filter(**my_filter).order_by(Lower("PART_NUM")).values_list("PART_DESC", flat=True))
  		  selectedListjson = json.dumps(selectedList)
  		  descListjson = json.dumps(descList)
      		  slugListjson = json.dumps(slugList)
      		  listLength = len(selectedList)    
            return render(request, 'parts/part_list.html', {
        	'parts': parts,
        	'NUMBER': NUMBER,
        	'searchValue': searchValue,
        	'selectedListjson': selectedListjson,
        	'slugListjson': slugListjson,
        	'descListjson': descListjson,
        	'listLength': listLength,
        	'slugList': slugList,
        	'selectedList': selectedList,
   	     })
        else:
            print form.errors
    # otherwise just create the form 
    else: 
        form = form_class(instance=part)
    # and pass to the template 
    return render(request, 'parts/part_detail.html', { 
        'part': part, 
        'form': form,
        'searchValue': searchValue,
        'currentDir': currentDir,
        'passDesc': passDesc,
        'filePathEle': filePathEle,
        'Slug': Slug,
    })

#editing view
def edit_part(request, Slug): 
    # grab the object 
    part = Part.objects.get(Slug = Slug)
    parts = Part.objects.all()
    allSlugs = Part.objects.order_by("Slug").values_list("Slug", flat=True).distinct()
    allAUTONUMs = Part.objects.order_by("AUTONUM").values_list("AUTONUM", flat=True).distinct()
    lastSlug = allSlugs.reverse()[0]
    lastSlugNum = int(lastSlug)
    partDistinct = Part.objects.exclude(CATEGORY__isnull=True).exclude(CATEGORY__exact=' ').exclude(CATEGORY__exact='  ').exclude(CATEGORY__exact='').order_by(Lower("CATEGORY")).values_list("CATEGORY", flat=True).distinct()
    j = 0
    partDict = defaultdict(list, flat=True)
    while j < len(partDistinct):
        currentCat = partDistinct[j]
        numList = list(Part.objects.filter(CATEGORY=currentCat).order_by(Lower("NUMBER")).values_list("NUMBER", flat=True).distinct())
        lenNumList = len(numList)
        k = 0
        while k < lenNumList:
            currentNum = numList[k]
            partDict[currentCat].append(currentNum)
            k = k + 1
        j = j + 1
    jsonDict = json.dumps(partDict)
    # set the form we're using 
    form_class = PartForm
    # if we're coming to this view from a submitted form 
    if request.method == 'POST': 
        # grab the data from the submitted form and apply to 
        # the form 
        form = form_class(request.POST, instance = part) 
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
        'Slug': Slug,
	'lastSlugNum': lastSlugNum,
        'parts': parts,
        'jsonDict': jsonDict,
        'numList': numList,
        'partDistinct': partDistinct,
        'partDict': partDict,
        'currentCat': currentCat, 
        'form': form, 
    })


def addpart(request):
    parts = Part.objects.all()
    allSlugs = Part.objects.order_by("Slug").values_list("Slug", flat=True).distinct()
    allAUTONUMs = Part.objects.order_by("AUTONUM").values_list("AUTONUM", flat=True).distinct()
    lastSlug = allSlugs.reverse()[0]
    lastSlugNum = int(lastSlug)
    partDistinct = Part.objects.exclude(CATEGORY__isnull=True).exclude(CATEGORY__exact=' ').exclude(CATEGORY__exact='  ').exclude(CATEGORY__exact='').order_by(Lower("CATEGORY")).values_list("CATEGORY", flat=True).distinct()
    j = 0
    partDict = defaultdict(list, flat=True)
    while j < len(partDistinct):
        currentCat = partDistinct[j]
        numList = list(Part.objects.filter(CATEGORY=currentCat).order_by(Lower("NUMBER")).values_list("NUMBER", flat=True).distinct())
        lenNumList = len(numList)
        k = 0
        while k < lenNumList:
            currentNum = numList[k]
            partDict[currentCat].append(currentNum)
            k = k + 1
        j = j + 1
    jsonDict = json.dumps(partDict)
    
    #Hidden form from 'Edit Part'
    # set the form we're using 
    form_class = addPartForm
    duplicateFlag=0
    if request.method == 'POST': 
        # grab the data from the submitted form and apply to 
        # the form 
        form = form_class(data = request.POST)
        CATEGORY = str(request.POST.get("CATEGORY"))
        NUMBER = str(request.POST.get("NUMBER"))
        PART_DESC = str(request.POST.get("PART_DESC"))
	searchValue = request.POST.get("searchValue")
        partNum = str(request.POST.get("partNum")).upper()
        partNum = partNum.strip()
        aaaa = Part.objects.filter(CATEGORY=CATEGORY).filter(NUMBER=NUMBER).filter(PART_NUM=partNum).order_by("PART_NUM").values_list("PART_NUM", flat=True)
        if Part.objects.filter(CATEGORY=CATEGORY).filter(NUMBER=NUMBER).filter(PART_NUM=partNum).exists() > 0:
            duplicateFlag=1
            return render(request, 'parts/addpart.html', {
                    'duplicateFlag': duplicateFlag,
                    'lastSlugNum': lastSlugNum,
                    'parts': parts,
                    'jsonDict': jsonDict,
                    'numList': numList,
                    'partDistinct': partDistinct,
                    'partDict': partDict,
                    'currentCat': currentCat, 
                    'form': form, 
                    'CATEGORY': CATEGORY,
                    'NUMBER': NUMBER,
                    'PART_DESC': PART_DESC,
                })
        if form.is_valid(): 
            form.save()
	parts = Part.objects.all()
	SelectNumStr = str(NUMBER)
        SelectCatStr = str(CATEGORY)
        selectedList = list(Part.objects.filter(NUMBER=SelectNumStr).filter(CATEGORY=SelectCatStr).order_by(Lower("PART_NUM")).values_list("PART_NUM", flat=True))
        slugList = list(Part.objects.filter(NUMBER=SelectNumStr).filter(CATEGORY=SelectCatStr).order_by(Lower("PART_NUM")).values_list("Slug", flat=True))
        descList = list(Part.objects.filter(NUMBER=SelectNumStr).filter(CATEGORY=SelectCatStr).order_by(Lower("PART_NUM")).values_list("PART_DESC", flat=True))
        selectedListjson = json.dumps(selectedList)
        descListjson = json.dumps(descList)
        slugListjson = json.dumps(slugList)
        listLength = len(selectedList)
        return render(request, 'parts/part_list.html', {
   	     'parts': parts,
   	     'NUMBER': NUMBER,
   	     'searchValue': searchValue,
   	     'selectedListjson': selectedListjson,
   	     'slugListjson': slugListjson,
   	     'descListjson': descListjson,
   	     'listLength': listLength,
   	     'slugList': slugList,
   	     'selectedList': selectedList,
   	 })

    # otherwise just create the form 
    else: 
        form = form_class()
    return render(request, 'parts/addpart.html', { 
        'lastSlugNum': lastSlugNum,
        'parts': parts,
        'jsonDict': jsonDict,
        'numList': numList,
        'partDistinct': partDistinct,
        'partDict': partDict,
        'currentCat': currentCat, 
        'form': form, 
    })

def addimage(request):
    parts = Part.objects.all()
    allSlugs = Part.objects.order_by("Slug").values_list("Slug", flat=True).distinct()
    lastSlug = allSlugs.reverse()[0]
    lastSlugNum = int(lastSlug)
    currentSlug = lastSlugNum + 1
    partDistinct = Part.objects.exclude(CATEGORY__isnull=True).exclude(CATEGORY__exact='').exclude(CATEGORY__exact=' ').order_by(Lower("CATEGORY")).values_list("CATEGORY", flat=True).distinct()
    j = 0
    partDict = defaultdict(list, flat=True)
    while j < len(partDistinct):
        currentCat = partDistinct[j]
        numList = list(Part.objects.filter(CATEGORY=currentCat).order_by(Lower("NUMBER")).values_list("NUMBER", flat=True).distinct())
        lenNumList = len(numList)
        k = 0
        while k < lenNumList:
            currentNum = numList[k]
            partDict[currentCat].append(currentNum)
            k = k + 1
        j = j + 1
    jsonDict = json.dumps(partDict)
    form_class = addPartForm
  
    # **Image Handling**
    if request.method == 'POST':
        infoForm = form_class(data = request.POST)
        imageForm = DocumentForm(request.POST, request.FILES)
        if infoForm.is_valid() and imageForm.is_valid():
            infoForm.save()
            newdoc = Document(relSlug=currentSlug, imageName=request.FILES['imageName'])
            newdoc.save()
            return redirect('/') 
    else:
        imageForm = DocumentForm() # A empty, unbound form
        infoForm = form_class()

    return render(request, 'parts/addimage.html', {
        'lastSlugNum': lastSlugNum,
        'parts': parts,
        'jsonDict': jsonDict,
        'numList': numList,
        'partDistinct': partDistinct,
        'partDict': partDict,
        'currentCat': currentCat,
        'imageForm': imageForm,
        'infoForm': infoForm
    })



