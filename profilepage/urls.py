from django.urls import path
from . import views

app_name = "profilepage"

urlpatterns = [
    path('profilepage/',views.profilepage,name='profilepage'),
    path('update_info/',views.changeprofileinfo,name='changeprofileinfo'),
    path('requests-<int:device_id>/',views.request_details,name='request_details'),
    path('delete-device-<int:device_id>/',views.delete_device,name='delete_device'),
    path('deny-<int:aadhaar_number>-<int:device_id>/',views.deny_request,name='deny_request'),
    path('confirm-<int:aadhaar_number>-<int:device_id>/',views.send_confirmation,name='send_confirmation'),
]
