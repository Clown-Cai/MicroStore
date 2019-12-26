from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^collection/', ProductCollectionAPIView.as_view()),
    url(r'^shoppingcart/', ShoppingAPIView.as_view()),
    url(r'^order/', OrderAPIView.as_view()),
    url(r'^order/success/', SuccessAPIView.as_view()),
    url(r'^history/', BrowserHistoryAPIView.as_view()),
    url(r'^unpayorder/', NoPayOrderAPIView.as_view()),
    url(r'^undeliver/', UndeliverOrderAPIView.as_view()),
    url(r'^unreceive/', UnreceivedAPIView.as_view()),

]
