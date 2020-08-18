 
from django.urls import path
from . import views
from donate import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = "apply_main"

urlpatterns = [
    path('apply/',views.apply,name='apply'),
    path('applied_login/',views.applied_login,name='applied_login'),
    path('applied_list/',views.applied_list,name='applied_list'),
    path('donor-info/<donor_username>',views.donor_details,name='donor_details'),
    path('send-request/<int:device_id>',views.send_request,name='send_request'),
    path('remove-request/<int:device_id>',views.remove_request,name='remove_request'),
    path('request-list/',views.request_list,name='request_list'),
    path('verify/',views.verify,name='verify'),
    # path('ajax/load-districts/', views.load_districts, name='ajax_load_districts'),
    # path('ajax/load-subdistricts/', views.load_subdistricts, name='ajax_load_subdistricts'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()