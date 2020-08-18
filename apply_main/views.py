from django.shortcuts import render
from . import forms 
import json
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.forms import modelformset_factory
import requests
import urllib.parse
from apply_main.models import *
from donation_main.models import *
from django.contrib.gis.geos import Point
from reg_sign_in_out.models import *
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
import string
import random
from donate.settings import STATIC_DIR,BASE_DIR
import os
from datetime import datetime,timezone
from donate.decorator import received_false
import numpy as np
#import cv2
from PIL import Image
import pytesseract
from time import sleep
import re
from io import BytesIO



def getLonLat(subdistrict,district,state):
    subdistrict = re.sub(r'[^\w\s]','',subdistrict)
    district = re.sub(r'[^\w\s]','',district)
    state = re.sub(r'[^\w\s]','',state)

    try:
        try:
            address = str(subdistrict)+", "+str(district)+", "+str(state)
            url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'
            response = requests.get(url).json()
            1/len(response)
            return [response[0]["lat"],response[0]["lon"]]

        except:
            try:
                address = str(subdistrict)
                url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'
                response = requests.get(url).json()
                1/len(response)
                return [response[0]["lat"],response[0]["lon"]]

            except:
                address = str(district)
                url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'
                response = requests.get(url).json()
                1/len(response)
                return [response[0]["lat"],response[0]["lon"]]                    

    except:
        address = str(state)
        url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'
        response = requests.get(url).json()
        return [response[0]["lat"],response[0]["lon"]]




@csrf_protect
def apply(request):

    def generate_key():
        letters_and_digits = string.ascii_lowercase + string.digits
        result_str = ''.join((random.choice(letters_and_digits) for i in range(6)))
        return result_str 

    form = forms.ApplyForm()
    if request.method == 'POST':
        form = forms.ApplyForm(request.POST,request.FILES)

        if form.is_valid():
            application = form.save(commit=False)

            subdistrict_id = int(request.POST.get("subdistrict"))
            district_id = int(request.POST.get("district"))
            state_id = int(request.POST.get("state"))
            
            f = json.loads(open(os.path.join(STATIC_DIR,"data.json")).read())

            subdistrict = f[subdistrict_id-1].get('name')
            district = f[district_id-1].get('name')
            state = f[state_id-1].get('name')

            (lat,lon) = getLonLat(subdistrict,district,state)
            application.lat,application.lon = lat,lon
            application.location = Point([float(lat),float(lon)],srid=4326)
            application.special_key = generate_key()

            application.subdistrict = subdistrict
            application.district = district
            application.state = state
            
            request.session["aadhaar_number"]=str(application.aadhaar_number)
            request.session["path"] = str(application.aadhaar_image.url)
            request.session["dob"] = str(application.date_of_birth)
            request.session["fn"] = str(application.first_name)

            boolx = application.save(request)
            print(boolx)
            if boolx != False:
                return HttpResponseRedirect(reverse('apply_main:applied_login'))
            else:
                context = {
                'form':form,
                'message':'Information attached with Aadhaar card and provided details dont match.'
                }
                return render(request, 'apply_main/apply_form.html', context)
    
    context = {
        'form':form,
        'message':'If you get redirected back to this page after submitting then please fill the form again and upload a much clear image.'
    }
    return render(request, 'apply_main/apply_form.html', context)


def verify(request):

        # response = requests.get(request.session["path"])
        # img = Image.open(BytesIO(response.content))

        # aadhaar_number_processed = [x for x in str(request.session["aadhaar_number"])]
        # aadhaar_number_processed.insert(4,' ')
        # aadhaar_number_processed.insert(9,' ')
        # aadhaar_number_processed = ''.join(aadhaar_number_processed)

        # x = pytesseract.image_to_osd(img)
        # ang = int(re.search('(?<=Rotate: )\d+', x).group(0))
        # img = img.rotate(360-ang)
        # txt = pytesseract.image_to_string(img)
        # print(txt)
        # sleep(10)
        # if aadhaar_number_processed in txt:      
        #     if str(request.session["dob"])[:4] in txt:   
        #         return HttpResponseRedirect(reverse('apply_main:applied_login'))

        # Apply.objects.get(aadhaar_number=request.session["aadhaar_number"]).delete()
        return HttpResponseRedirect(reverse('apply_main:apply'))


# def load_districts(request):
#     state_id = request.GET.get('state')
#     districts = District.objects.filter(state_id=state_id).order_by('name')
#     return render(request, 'apply_main/dist_dropdown_list_options.html', {'districts': districts})

# def load_subdistricts(request):
#     district_id = request.GET.get('district')
#     subdistricts = Subdistrict.objects.filter(district_id=district_id).order_by('name')
#     return render(request, 'apply_main/subdist_dropdown_list_options.html', {'subdistricts': subdistricts})


def applied_login(request):

    if request.method == "POST":

        aadhaar_number = request.POST['aadhaar_number']
        date_of_birth = request.POST['date_of_birth']

        applicant = Apply.objects.filter(aadhaar_number=aadhaar_number)

        request.session["aadhaar_number"] = aadhaar_number
        request.session["date_of_birth"] = date_of_birth 
        

        if len(applicant)==0:
            return render(request, 'apply_main/apply_login.html',{'message':"Please apply first or correct your aadhaar number."})
            
        else:
            if str(applicant[0].date_of_birth) != str(date_of_birth):

                return render(request, 'apply_main/apply_login.html',{'message':"Date of birth is not matching."})

        if len(applicant)==1 and str(applicant[0].date_of_birth) == str(date_of_birth) and applicant[0].completed==False: 
            request.session['special_key'] = applicant[0].special_key 
            return HttpResponseRedirect(reverse('apply_main:applied_list'))
        else:
            return render(request, 'apply_main/apply_login.html',{'message':"You have already been sent/received the device and is confirmed by you by giving the Special Key."})
    
    return render(request, 'apply_main/apply_login.html')

@received_false()
def applied_list(request):

    aadhaar_number = request.session["aadhaar_number"]
    date_of_birth = request.session["date_of_birth"]
    filter_distance=100

    def m_deg(km):
        return km * 0.1/11.1

    if request.method == "POST":
        filter_distance = float(request.POST['filter_distance'])


    applicant = Apply.objects.get(aadhaar_number=aadhaar_number,date_of_birth=date_of_birth)
    app_lon = applicant.lon
    app_lat = applicant.lat
    ref_location = applicant.location

    res = (Registration.objects
    .filter(location__dwithin=(ref_location, m_deg(km=filter_distance)))
    # .filter(location__distance_lte=(ref_location, D(m=0.1)))
    .annotate(distance=Distance('location', ref_location))
    .order_by('distance')
    )
    print(filter_distance)
    return render(request, 'apply_main/donor_list.html',context={'donors': res,
                                                                 'distance':filter_distance})

@received_false()
def donor_details(request,donor_username):

    device_list = Donate.objects.filter(user__username=donor_username)

    return render(request, 'apply_main/donor_details.html',context={'device_list': device_list})

@received_false()
def send_request(request,device_id):
    Request.manager.send_req(request.session["aadhaar_number"],device_id)
    return HttpResponseRedirect(reverse('apply_main:applied_list'))

@received_false()
def remove_request(request,device_id):
    Request.manager.remove_req(request.session["aadhaar_number"],device_id)
    return HttpResponseRedirect(reverse('apply_main:applied_list'))

@received_false()
def request_list(request):

    req_lst = Request.objects.filter(applicant__aadhaar_number=request.session['aadhaar_number'])

    for requestx in req_lst:
        delta = (datetime.now(timezone.utc)-requestx.request_time)

        if delta.total_seconds()>21600-19800:
            requestx.delete()

    req_lst = Request.objects.filter(applicant__aadhaar_number=request.session['aadhaar_number'])

    return render(request, 'apply_main/request_list.html',context={'req_lst': req_lst})
   