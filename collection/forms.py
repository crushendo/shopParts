from django.forms import ModelForm, ModelChoiceField, FileField
from django import forms
from collection.models import Part

#Displaying part info or editing existing part
class PartForm(ModelForm):
    class Meta: 
        model = Part 
        fields = ('CATEGORY', 'NUMBER', 'PART_NUM', 'PART_DESC')

#Adding a new part, must generate new Slug/AUTONUM automatically
class addPartForm(ModelForm):
    class Meta: 
        model = Part 
        fields = ('CATEGORY', 'NUMBER', 'PART_NUM', 'PART_DESC', 'Slug', 'AUTONUM')

#Unused?
class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
    label='Select an Image'

#Used for uploading Images
class DocumentForm(forms.Form):
    imageName = forms.FileField(
        label='Select a file',
    )

#Attempt at dropdown menu form
"""class DropDown(forms.Form):
    cats = forms.ModelChoiceField(queryset = [], required=False)
    def __init__(self, *args, **kwargs):
        super(DropDown, self).__init__(*args, **kwargs)
        self.fields['cats'].queryset = Part.objects.all().order_by(part.CATEGORY).values_list(part.Category, flat=True).distinct()
        ##.values_list('CATEGORY', flat=True)
        
    print cats"""
      