from django import forms
from django.forms import BaseFormSet
from donation_main.models import *
from crispy_forms.helper import FormHelper

class DonateForm(forms.ModelForm):
    
    model_name = forms.CharField(max_length=64,label='',
                widget=forms.TextInput(
                    attrs={'class':'form-control',
                            'style':'width:30%',
                            'placeholder':'Model Name'}
                ))
    class Meta:
        model = Donate
        fields = [
            'model_name',
        ]



class ImagesForm(forms.ModelForm):
    

    class Meta:
        model = Images
        fields = [
            'mobile_images',
        ]

        labels = {
            'mobile_images': 'Mobile Images'
        }

    def has_changed(self): #used for saving data from initial
        changed_data = super(ImagesForm, self).has_changed()
        return bool(self.initial or changed_data)
    
    
    
class BaseImagesFormSet(BaseFormSet): 
    # def clean(self): 
    #     print("in")
    #     # data from the form is fetched using super function 
    #     super(BaseImagesFormSet, self).clean() 
    #     #mobile_images = self.cleaned_data.get('mobile_images', False)        
    #     for form in self.forms:
    #         mobile_images = form.cleaned_data.get('mobile_images', False)
    #         if mobile_images:
    #             if mobile_images.size > 1*1024*1024:
    #                 raise ValidationError("Image file too large ( > 1mb )")

    #             return mobile_images
    #         else:
    #             raise ValidationError("Couldn't read uploaded image") 
    pass