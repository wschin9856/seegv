"""SEEGV URL Configuration

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
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.index),
    path('detailview/',views.detailview),#
    path('arthouse/',views.arthouse),#
    path('persons/',views.person),#
    path('theater/',views.theater),
    path('get_theaters/',views.get_theaters),
    path('pre-movies/',views.premovie),#
    path('',views.index),#
    path('theater/special/',views.special),
    path('theater/special/detailview/',views.specialcate),
    path('get_schedule/',views.get_schedule),
    path('get_bookmark/',views.get_bookmark),
    path('preview_save/', views.previewSave),
    path('recommand_save/', views.recommandcount),
    path('write_review/', views.write_review),
    path('write_review/checkwrite/', views.checkwrite),
    path('create/', views.movieCreate),
    path('create/check/', views.checkCreate),
    path('update/', views.movieUpdate),
    path('update/check/', views.checkUpdate)
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

