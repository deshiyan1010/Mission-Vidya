from django.shortcuts import render
from reg_sign_in_out.models import *
from . import forms 
import requests
import urllib.parse
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from apply_main.models import *
from django.contrib.gis.geos import Point
import json
import os
from donate.settings import STATIC_DIR
import re


def index(request):
    return render(request,"index.html")

@login_required
def special(request):
    return HttpResponse("In!")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))  

@csrf_protect
def registration(request):

    registered = False

    def getLonLat(subdistrict,district,state):
        subdistrict = re.sub(r'[^\w\s]','',subdistrict)
        district = re.sub(r'[^\w\s]','',district)
        state = re.sub(r'[^\w\s]','',state)

        try:
            try:
                print("try",'\n'*3)
                address = str(subdistrict)+", "+str(district)+", "+str(state)
                print(address)
                url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'
                print(url)
                response = requests.get(url).json()
                print(response)
                1/len(response)
                return [response[0]["lat"],response[0]["lon"]]

            except:
                try:
                    print("try",'\n'*3)
                    address = str(subdistrict)
                    print(address)
                    url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'
                    print(url)
                    response = requests.get(url).json()
                    print(response)
                    1/len(response)
                    return [response[0]["lat"],response[0]["lon"]]

                except:
                    print("try",'\n'*3)
                    address = str(district)
                    print(address)
                    url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'
                    print(url)
                    response = requests.get(url).json()
                    print(response)
                    1/len(response)
                    return [response[0]["lat"],response[0]["lon"]]                    

        except:
            print("except",'\n'*3)
            address = str(state)
            print(address)
            url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'
            print(url)
            response = requests.get(url).json()
            print(response)
            return [response[0]["lat"],response[0]["lon"]]


    if request.method == "POST":
        form = forms.UserForm(request.POST)
        profileform = forms.RegistrationForm(request.POST,request.FILES)

        if form.is_valid() and profileform.is_valid():
            
            subdistrict_id = int(request.POST.get("subdistrict"))
            district_id = int(request.POST.get("district"))
            state_id = int(request.POST.get("state"))
            
            f = json.loads(open(os.path.join(STATIC_DIR,"data.json")).read())

            subdistrict = f[subdistrict_id-1].get('name')
            district = f[district_id-1].get('name')
            state = f[state_id-1].get('name')


            user = form.save()
            user.set_password(user.password)
            user.save()

            profile = profileform.save(commit=False)
            profile.user = user
            (lat,lon) = getLonLat(subdistrict,district,state)
            profile.lat,profile.lon = lat,lon
            profile.state = state
            profile.district = district
            profile.subdistrict = subdistrict
            profile.location = Point([float(lat),float(lon)],srid=4326)
            profile.save()

            registered = True
            return HttpResponseRedirect(reverse('reg_sign_in_out:user_login'))
        
        else:

            print(form.errors,profileform.errors)
            
            return render(request,"reg_sign_in_out/registration.html",{"tried":"True",
                                                    "registered":registered,
                                                   "profile_form":profileform,
                                                   "user_form":form,
                                                   "errorone":form.errors,
                                                   "errortow":profileform.errors,
                                                   })
            

    else:
        user = forms.UserForm()
        profileform = forms.RegistrationForm()

    return render(request,"reg_sign_in_out/registration.html",{"registered":registered,
                                                   "profile_form":profileform,
                                                   "user_form":user,
                                                   })


@csrf_protect
def user_login(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('donation_main:donate_form'))

        else:

            return render(request,"reg_sign_in_out/login.html",{'tried':'True'})

    else:
        return render(request,"reg_sign_in_out/login.html")


def load_districts(request):
    state_id = request.GET.get('state')
    districts = District.objects.filter(state_id=state_id).order_by('name')
    return render(request, 'apply_main/dist_dropdown_list_options.html', {'districts': districts})

def load_subdistricts(request):
    district_id = request.GET.get('district')
    subdistricts = Subdistrict.objects.filter(district_id=district_id).order_by('name')
    return render(request, 'apply_main/subdist_dropdown_list_options.html', {'subdistricts': subdistricts})