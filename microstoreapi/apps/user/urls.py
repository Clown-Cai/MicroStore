from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'address/$', AddressListAPIView.as_view()),
    url(r'address/add', AddressAPIView.as_view()),
]
