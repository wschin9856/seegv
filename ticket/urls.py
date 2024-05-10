from django.urls import path
from . import views
from django.conf.urls.static import static, settings

urlpatterns = [
    path('', views.list),
    path('ajax1/', views.ajax1),
    path('ajax_getCoupon/', views.ajax_getCoupon),
    path('coupon_regi/', views.coupon_regi),
    path('seat_sel/', views.seat_sel),
    path('seat_sel/payment/', views.payment),
    path('seat_sel/payment/input_Coupon/', views.input_Coupon),
    path('lastpayment/', views.lastpayment), 
    path('seat_sel/payment/lastpayment/', views.lastpayment), 
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
