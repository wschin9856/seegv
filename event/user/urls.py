"""Kiosk URL Configuration

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
from django.urls import path,include
from user import views


# 파일 전송을 위한 세팅
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index),
    path('mycgv/',views.mycgv),
    path('mycgv/pwcheck',views.mycgv_pwcheck),
    path('mycgv/popup/ajax',views.mycgv_popup_ajax),
    path('mycgv/popup/ajax2',views.mycgv_popup_ajax2),
    path('mycgv/popup/ajax3',views.mycgv_popup_ajax3),


    path('login/',views.login),
    path('login/result',views.login_result),
    path('login/findID',views.login_findID),
    path('login/findID/result',views.login_findID_result),
    path('login/findPW',views.login_findPW),
    path('login/findPW/result',views.login_findPW_result),
    path('logout/',views.logout),

    path('join/',views.join),
    path('join/result',views.join_result),
    path('join/check',views.join_check),
    path('join/ajax_id',views.ajax_post_id),

    path('mycgv/leave',views.mycgv_leave),
    path('mycgv/leave/result',views.mycgv_leave_result),

    path('mycgv/myInfo',views.mycgv_myInfo),
    # path('mycgv/myInfo/check',views.mycgv_myInfo_check),
    path('mycgv/myInfo/result',views.mycgv_myInfo_result),

    path('mycgv/terms',views.mycgv_terms),
    path('mycgv/terms/result',views.mycgv_terms_result),

    path('mycgv/terms',views.mycgv_terms),
    path('mycgv/profile',views.mycgv_profile),
    path('mycgv/profile/result',views.mycgv_profile_result),
    
    path('mycgv/giftcon',views.mycgv_giftcon),
    path('mycgv/giftcon/register',views.mycgv_giftcorn_register),
    path('mycgv/giftcon/register/result',views.mycgv_giftcorn_register_result),
    path('mycgv/giftcard',views.mycgv_giftcard),
    path('mycgv/giftcard/register',views.mycgv_giftcard_register),
    path('mycgv/giftcard/register/result',views.mycgv_giftcard_register_result),
    
    
    path('mycgv/payment',views.mycgv_payment),
    path('mycgv/payment/detail',views.mycgv_payment_detail),
    path('mycgv/refund',views.mycgv_refund),

    path('mycgv/point',views.mycgv_point),
    
    #---------------------현교코드------
    path('mycgv/myevent/',views.myevent),
    path('mycgv/myevent/result/',views.myeventresult),
    path('mycgv/myevent/detail/',views.myeventdetail),
    path('get_win/',views.get_win),

    #--민국--
    path('check_login/',views.check_login),
    path('mycgv/movielog/', views.movielog),
    path('mycgv/movielogdelete/', views.movielogdelete),


]
    


# 파일 전송을 위한 세팅
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

