from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'address/$', AddressListAPIView.as_view()),
    url(r'address/(?P<pk>\d+)$', AddrDestroyAPIView.as_view()),
    url(r'defaultAddress/$', AddrDefaultAPIView.as_view()),
]
