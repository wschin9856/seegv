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
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.index),
    path('members',views.members),
    path('members/detail',views.members_detail),
    path('members/detail/change',views.members_detail_change),
    path('members/detail/remove',views.members_detail_remove),

    path('product',views.product),
    path('product/detail',views.product_detail),
    path('product/change',views.product_change),
    path('product/change/result',views.product_change_result),
    path('product/remove',views.product_remove),

    path('product/add',views.product_add),
    path('product/add/result',views.product_add_result),

    path('giftcon',views.giftcon),
    path('giftcon/<num>',views.giftcon_num),
    path('state',views.giftcon_state),





]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)