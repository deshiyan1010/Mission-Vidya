from django.shortcuts import render
from . import forms 
from donation_main.forms import BaseImagesFormSet
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.forms import modelformset_factory
from donation_main.models import Images,Donate

# Create your views here.
@login_required
def donate_form(request):
    ImageFormSet = modelformset_factory(Images, fields=('mobile_images',),extra=1,min_num=1,validate_min=True, formset=BaseImagesFormSet)
    form = forms.DonateForm()
    formset = ImageFormSet()
    if request.method == 'POST':

        form = forms.DonateForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():

            donation = form.save(commit=False)
            donation.user = request.user
            donation.save()

            for f in formset:
                try:

                    photo = Images(donation=donation,mobile_images=f.cleaned_data['mobile_images'])
                    photo.save()
                except Exception as e:
                    pass
            return HttpResponseRedirect(reverse('donation_main:thankyou'))        
        else:
            print(form.errors,formset.non_form_errors())     
    
    else:

        formset = ImageFormSet()

    if formset.non_form_errors():   

        context = {
            'form':form,
            'formset':formset,
            'message':str(formset.non_form_errors())[26:-16]+" images."
        }
    context = {
        'form':form,
        'formset':formset,
    }

    return render(request, 'donation_main/donate_form.html', context)

@login_required
def thankyou(request):
    return render(request, 'donation_main/thankyou.html')