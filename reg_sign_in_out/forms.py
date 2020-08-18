from django import forms
from reg_sign_in_out.models import *
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30,required=True,
                                widget = forms.TextInput(attrs={'class': 'input'}))
    last_name = forms.CharField(max_length=30,required=True,
                                widget = forms.TextInput(attrs={'class': 'input'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input'}),)
    
    username = forms.CharField(max_length=30,required=True,
                                widget = forms.TextInput(attrs={'class': 'input'}))
    email = forms.CharField(max_length=30,required=True,
                                widget = forms.TextInput(attrs={'class': 'input'}))
    class Meta:
        model = User
        fields = ('first_name','last_name','username','email','password',)

    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError('Exists')
        return username


class RegistrationForm(forms.ModelForm):
    
    class Meta:
        model = Registration
        fields = ('profile_pic','phone_number')

        labels = {
            'profile_pic':'Profile Picture'
        }
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['district'].queryset = District.objects.none()
    #     self.fields['subdistrict'].queryset = Subdistrict.objects.none()

    #     if 'state' in self.data:
    #         try:
    #             state_id = int(self.data.get('state'))
    #             self.fields['district'].queryset = District.objects.filter(state_id=state_id).order_by('name')
    #         except (ValueError, TypeError):
    #             pass  # invalid input from the client; ignore and fallback to empty City queryset
    #     elif self.instance.pk:
    #         self.fields['district'].queryset = self.instance.state.district_set.order_by('name')

    #     if 'district' in self.data:
    #         try:
    #             district_id = int(self.data.get('district'))
    #             self.fields['subdistrict'].queryset = Subdistrict.objects.filter(district_id=district_id).order_by('name')
    #         except (ValueError, TypeError):
    #             pass  # invalid input from the client; ignore and fallback to empty City queryset
    #     elif self.instance.pk:
    #         self.fields['subdistrict'].queryset = self.instance.district.subdistrict_set.order_by('name')