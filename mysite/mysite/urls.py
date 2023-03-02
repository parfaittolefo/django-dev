"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from mysite.views import *
from django.urls import include, re_path, path
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap

urlpatterns = [
    re_path(r'^time/$',currente_time),
    re_path(r'^time_offset/plus/(\d{1,2})/*', currente_time_with_offset,name='offset_timer'),
    re_path('admin/', admin.site.urls),
    path("",include('books.urls')) ,
    re_path(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
    name='django.contrib.sitemaps.views.sitemap')
    ]
