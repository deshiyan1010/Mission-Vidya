from django.http import HttpResponseRedirect
from apply_main.models import Apply
from django.core.exceptions import ValidationError

def received_false():
    def decorator(func):
        def wrap(request,*args,**kwargs):
            status = Apply.objects.get(aadhaar_number=request.session["aadhaar_number"]).completed
            if status==False:
                return func(request,*args,**kwargs)
            else:
                raise ValidationError("You have already claimed one device with the current aadhaar number")

        return wrap
    return decorator