"""RESUME URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from distutils.command.upload import upload
from django.conf.urls import url
from django.contrib import admin
from RESUME_APP.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    ######## LOGIN & REGISTER START ###########
     #url(r'^$', register), 
    url(r'^register', register, name="register"),
    url(r'^check_register', check_register, name="check_register"),
    ########################
    url(r'^$', display_login_first),
    url(r'^display_login', display_login, name="display_login"),
    url(r'^check_login', check_login, name="check_login"),
    ########### LOGIN & REGISTER END ############

    # ADMIN START
    url(r'^a_home_hr', a_home_hr, name="a_home_hr"),
    url(r'^b_upload_resume_hr', b_upload_resume_hr, name="b_upload_resume_hr"),
    url(r'^upload_resume', upload_resume, name="upload_resume"),
    url(r'^c_view_resume_hr', c_view_resume_hr, name="c_view_resume_hr"),
    url(r'^resumes', resumes, name="resumes"),
    url(r'^delete', delete, name="delete"),
    url(r'^d_resume_screen_hr', d_resume_screen_hr, name="d_resume_screen_hr"),
    url(r'^perform',perform,name="perform"),
    url(r'^store',store,name="store"),
    url(r'^retrieve',retrieve,name="retrieve"),
    url(r'^table_delete',table_delete,name="table_delete"),

    # ADMIN END
]


