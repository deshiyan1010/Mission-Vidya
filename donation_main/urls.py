 
from django.urls import path
from . import views
from donate import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = "donation_main"

urlpatterns = [
    path('donate/',views.donate_form,name='donate_form'),
    path('thankyou/',views.thankyou,name='thankyou'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()