from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'address/$', AddressListAPIView.as_view()),
    url(r'address/(?P<pk>\d+)$', AddrDestroyAPIView.as_view()),
    url(r'defaultAddress/$', AddrDefaultAPIView.as_view()),
    url(r'mobile/$', CheckMobileAPIView.as_view()),
    url(r'sms/$', SendSMSAPIView.as_view()),
    url(r'login/mobile/$', MobileLoginAPIView.as_view()),
    url(r'login/$', LoginAPIView.as_view()),
    url(r'register/$', RegisterAPIView.as_view()),
]
