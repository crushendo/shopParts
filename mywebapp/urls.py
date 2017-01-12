"""mywebapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import include, url
from django.contrib import admin
from collection import views
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
import os

import django.views.defaults


urlpatterns = [
    url(r'^$',views.index,name='home'),
    url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'), 
    url(r'^contact/$', TemplateView.as_view(template_name ='contact.html'), name='contact'),
    url(r'^parts/addpart/$', views.addpart,name='addpart'),
    url(r'^parts/addimage/$', views.addimage,name='addimage'),
    url(r'^parts/(?P<Slug>[-\w]+)/$', views.part_detail,name='part_detail'), 
    url(r'^parts/(?P<Slug>[-\w]+)/edit/$', views.edit_part, name='edit_part'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^parts/list$', views.part_list, name='part_list'),
    url(r'^parts/(?P<Slug>[-\w]+)/$', views.part_detail,name='part_detail'), 
    
    
]


if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
