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
    # path('',views.index),
    path('',views.store),
    # path('manage',views.store_manage) ,
    # path('manage/result',views.store_manage_result),
    path('category',views.category),
    path('product',views.product),
    path('product_add',views.product_add),

    path('addList',views.addList),
    path('addList/ajax',views.addList_ajax),
    path('addList/purchase',views.addList_purchase),
    path('addList/purchase/result',views.addList_purchase_result),
    path('addList/userGift',views.addList_userGift),
    path('addList/userGift/result',views.addList_userGift_result),

    path('purchase',views.purchase),
    path('purchase/result',views.purchase_result),

    path('userGift',views.userGift),
    path('userGift/result',views.userGift_result),

]





