"""donate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from reg_sign_in_out import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('',views.index,name="index"),
    path('admin/', admin.site.urls),
    path('',include('donation_main.urls'),name="donation_main"),
    path('',include('apply_main.urls'),name="apply_main"),
    path('',include('profilepage.urls'),name="profilepage"),
    path('',include('reg_sign_in_out.urls'),name="reg_sign_in_out"),
    path('logout/',views.user_logout,name='logout'),
    # path('donate/progbar', csrf_exempt(TemplateView.as_view(template_name='file_upload_parser.php'))),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='password_reset.html', email_template_name='email_template.html'),name='reset_password'),
    path('password-reset/sent/',auth_views.PasswordResetDoneView.as_view(template_name='password_reset_sent.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html',success_url = reverse_lazy('reg_sign_in_out:user_login')),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html',),name='password_reset_complete'),

]
