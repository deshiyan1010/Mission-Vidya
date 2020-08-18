from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect
from django.urls import reverse
from . import forms
from reg_sign_in_out.models import Registration
from django.contrib.auth.models import User
from apply_main.models import Request,Apply
import os
import json
import requests
import urllib.parse
from donate.settings import STATIC_DIR
from django.contrib.gis.geos import Point
from datetime import datetime,timezone
from donation_main.models import DonatedInformation,Donate
import re




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


def send_confirmation(request,aadhaar_number,device_id):

    print("out")
    print(request.method)
    if request.method == "POST":
        special_key = request.POST['special_key']

        real_special_key = Apply.objects.get(aadhaar_number=aadhaar_number).special_key

        if special_key==real_special_key:
            Y = Apply.objects.get(aadhaar_number=aadhaar_number)
            Y.completed = True
            Y.save(request)
            
            completed_entry = DonatedInformation(device_id=device_id,receiver=Y)
            completed_entry.save()
            
            X = Donate.objects.get(id=device_id)
            X.donated = True
            X.save()

            Request.objects.get(applicant=Y,donor_id=device_id).delete()
            return render(request, 'donation_main/thankyou.html')
        
        else:
            return render(request,"profilepage/send_confirmation.html",{'message':'Incorrect Key'})
    return render(request,"profilepage/send_confirmation.html",)



@login_required
def profilepage(request):


    return render(request,"profilepage/profilepage.html",{"user":request.user,})

@login_required
def changeprofileinfo(request):

    if request.method == "POST":
        form = forms.UserChangeForm(request.POST)
        profileform = forms.RegistrationChangeForm(request.POST,request.FILES)

        if form.is_valid() and profileform.is_valid():
            
            subdistrict_id = int(request.POST.get("subdistrict"))
            district_id = int(request.POST.get("district"))
            state_id = int(request.POST.get("state"))

            f = json.loads(open(os.path.join(STATIC_DIR,"data.json")).read())

            subdistrict = f[subdistrict_id-1].get('name')
            district = f[district_id-1].get('name')
            state = f[state_id-1].get('name')

            (lat,lon) = getLonLat(subdistrict,district,state)

            cuser = User.objects.get(username=request.user.username)

            if len(request.POST['first_name'])!=0:
                cuser.first_name = request.POST['first_name']
            if len(request.POST['last_name'])!=0:
                cuser.last_name = request.POST['last_name']
            if len(request.POST['email'])!=0:
                cuser.email = request.POST['email']
            cuser.save()
            try:
                xuser = Registration.objects.get(user=request.user).delete()
            except:
                pass
            profile = profileform.save(commit=False)
            profile.user = request.user
            profile.lat = lat
            profile.lon = lon 
            profile.location = Point([float(lat),float(lon)],srid=4326)

            profile.subdistrict = subdistrict
            profile.district = district
            profile.state = state

            profile.save()
  
            return HttpResponseRedirect(reverse('profilepage:profilepage'))

        else:

            print(form.errors,profileform.errors)
            
            return render(request,"profilepage/change.html",{"tried":"True",
                                                   "profile_form":profileform,
                                                   "user_form":form,
                                                   })
            

    else:
        form = forms.UserChangeForm()
        profileform = forms.RegistrationChangeForm()

    return render(request,"profilepage/change.html",{
                                                   "profile_form":profileform,
                                                   "user_form":form,
                                                   })
@login_required
def request_details(request,device_id):

    requests = Request.objects.filter(donor__user=request.user,donor_id=device_id)

    for requestx in requests:
        delta = (datetime.now(timezone.utc)-requestx.request_time)

        if delta.total_seconds()>21600:
            requestx.delete()
        

    requests = Request.objects.filter(donor__user=request.user,donor_id=device_id)
    return render(request,"profilepage/request_list.html",{
                                                   "requests":requests,
                                                   "device_id":device_id,
                                                   })
@login_required
def deny_request(request,aadhaar_number,device_id):
    Request.objects.get(donor__user=request.user,donor_id=device_id,applicant__aadhaar_number=aadhaar_number).delete()

    return HttpResponseRedirect(reverse('profilepage:request_details',args=(device_id,)))


@login_required
def delete_device(request,device_id):
    Donate.objects.get(id=device_id).delete()
    return HttpResponseRedirect(reverse('profilepage:profilepage'))