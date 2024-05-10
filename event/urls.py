"""MyHome URL Configuration

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
from django.urls import path,include
from django.conf.urls.static import static
from . import views    
urlpatterns = [
    path('',views.event),
    path('content/',views.eventContent),
    path('end/',views.endevent),
    path('apply_events/',views.apply_events),
    path('benefit/',views.benefit),
    path('get_theaters/',views.get_theaters),
    path('ajaxtest/',views.ajaxtest),
    path('check_apply/',views.check_apply),
    path('vip',views.vip),
    path('get_grade/',views.get_grade),
    path('vip/faq/',views.vip_faq),
    path('vip/special/',views.vip_special),
    path('vip/coupons',views.vip_coupons),
    path('vip/coupon/set/',views.vip_couponset),
    path('vip/mycoupon/',views.vip_mycoupon),
    path('vip/benefitset/',views.vip_benefitset),
    ]