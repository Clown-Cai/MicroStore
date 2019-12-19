from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^collection/', ProductCollectionAPIView.as_view()),
    url(r'^shoppingcart/', ShoppingAPIView.as_view()),
]
