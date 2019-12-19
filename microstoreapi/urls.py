from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.views.static import serve


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # 放开media文件的访问
    url('^media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^adminer/', include('adminer.urls')),
    url(r'^order/', include('order.urls')),
    url(r'^product/', include('product.urls')),
    url(r'^user/', include('user.urls')),
]
