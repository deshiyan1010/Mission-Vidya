from django import forms
from django.contrib.auth.models import User
from reg_sign_in_out.models import Registration

class UserChangeForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name','last_name','email')

class RegistrationChangeForm(forms.ModelForm):

    class Meta:
        model = Registration
        fields = ('profile_pic','phone_number')