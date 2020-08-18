from django import template
from donation_main.models import Donate
from apply_main.models import Request
register = template.Library()

@register.filter
def request_check(value,arg):
    applicants = Request.objects.filter(donor_id=value,applicant__aadhaar_number=arg)
    if len(applicants)==1:
        return "False"
    return "True"

@register.filter
def availability_check(value):
    device = Donate.objects.get(id=value).donated
    return str(device)

@register.filter
def available_donation(value):
    for x in value:
        if x.donated == False:
            return "True"
    return "False"