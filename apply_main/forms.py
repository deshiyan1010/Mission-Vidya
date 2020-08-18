from django import forms
from apply_main.models import *
import phonenumbers
import datetime
def Validate(aadharNum):

    mult = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 0, 6, 7, 8, 9, 5], [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
            [3, 4, 0, 1, 2, 8, 9, 5, 6, 7], [4, 0, 1, 2, 3, 9, 5, 6, 7, 8], [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
            [6, 5, 9, 8, 7, 1, 0, 4, 3, 2], [7, 6, 5, 9, 8, 2, 1, 0, 4, 3], [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
            [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]]
    perm = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 5, 7, 6, 2, 8, 3, 0, 9, 4], [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
            [8, 9, 1, 6, 0, 4, 3, 5, 2, 7], [9, 4, 5, 3, 1, 2, 6, 8, 7, 0], [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
            [2, 7, 9, 3, 8, 0, 6, 4, 1, 5], [7, 0, 4, 6, 9, 1, 3, 2, 5, 8]]

    if len(aadharNum) == 12 and aadharNum.isdigit():
        try:
            i = len(aadharNum)
            j = 0
            x = 0

            while i > 0:
                i -= 1
                x = mult[x][perm[(j % 8)][int(aadharNum[i])]]
                j += 1
            if x == 0:
                return True
            else:
                return False

        except ValueError:
            return False
        except IndexError:
            return False

    else:
        return False

def date_val(field):
    birth_year = int(str(field)[:4])
    cyear = int(datetime.datetime.now().year)
    age = cyear - birth_year
    if age<=18 or age>=5:
        return True
    return False

class ApplyForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(
        attrs={
            'placeholder': 'MM/DD/YYYY'
        }
    ))

    aadhaar_number = forms.CharField(widget=forms.TextInput())
    

    class Meta:
        model = Apply
        fields = [
            'first_name',
            'last_name',
            'aadhaar_number',
            'phone_number',
            'date_of_birth',
            'aadhaar_image',
            # 'state',
            # 'district',
            # 'subdistrict',            
        ]
        labels = {
            'first_name':'First Name',
            'last_name':'Last Name',
            'aadhaar_number':'Aadhaar Card Number',
            'phone_number':'Phone Number',
            'date_of_birth':'Date of birth (as in aadhaar card)',
            'state':"State",
            'district':'District',
            'subdistrict':'Thasil/Sub-district',   
        }

    def clean(self): 
  
        # data from the form is fetched using super function 
        super(ApplyForm, self).clean() 
          
        # extract the username and text field from the data 
        aadhaar_number = self.cleaned_data.get('aadhaar_number') 
        phone_number = self.cleaned_data.get('phone_number') 
        date_of_birth = self.cleaned_data.get('date_of_birth') 

        # conditions to be met for the username length 
        if Validate(aadhaar_number)==False: 
            self._errors['aadhaar_number'] = self.error_class([ 
                'Invalid Aadhaar Number']) 


        if len(str(phone_number)) !=10 or phonenumbers.is_valid_number(phonenumbers.parse("+91"+str(phone_number))) == False: 
            self._errors['phone_number'] = self.error_class([ 
                'Invalid phone number']) 


        if date_val(date_of_birth) == False: 
            self._errors['date_of_birth'] = self.error_class([ 
                'The age of the candidate must be between 5 and 18'])  

        # return any errors if found 
        return self.cleaned_data

  

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
