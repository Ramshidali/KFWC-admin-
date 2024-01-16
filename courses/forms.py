from django.forms.widgets import TextInput,Textarea,Select,DateInput,CheckboxInput,FileInput,PasswordInput,EmailInput
from django import forms

from django_summernote.widgets import SummernoteWidget

from . models import *


class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = ['title','subtitle','description','status','mrp','price','image']

        widgets = {
            'title': TextInput(attrs={'class': 'required form-control','placeholder' : 'Title'}), 
            'subtitle': TextInput(attrs={'class': 'required form-control','placeholder' : 'Subtitle'}), 
            'description': SummernoteWidget(), 
            'status': Select(attrs={'class': 'select2 form-control mb-3 custom-select'}),
            'mrp': TextInput(attrs={'class': 'required form-control','placeholder' : 'Subtitle'}), 
            'price': TextInput(attrs={'class': 'required form-control','placeholder' : 'Subtitle'}), 
            'image': FileInput(attrs={'class': 'form-control dropify'}),
        }
        
    def clean_image(self):
        
        image_file = self.cleaned_data.get('image')
        if image_file:
            if not (image_file.name.endswith(".jpg") or image_file.name.endswith(".png") or image_file.name.endswith(".jpeg")):
                raise forms.ValidationError("Only .jpg or .png files are accepted")
        return image_file
        
class DetailsForm(forms.ModelForm):

    class Meta:
        model = Details
        fields = ['title','description']

        widgets = {
            'title': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Agrement End Date'}), 
            'description': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Rent Date'}), 
        }