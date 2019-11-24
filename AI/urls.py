"""AI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url
from django.conf import settings
from django.urls import path, include
from .views import *
from django.conf.urls.static import static
from apps.qrcreate.views import generate_qrcode
from django.views.static import serve
from apps.identification.views import *
from allauth.account.views import *
import AI.views


urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'', home, name='home'),
    path(r'accounts/', include('allauth.urls')),
    path(r'accounts/', include('authentication.urls')),
    url(r'^qr/(.+)$', generate_qrcode, name='qr'),
    url(r'^qr/', home, name='qrcode'),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    path(r'', include('apps.identification.urls'), ),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT,) + static(settings.STATIC_URL,
                                                                            document_root=settings.STATIC_ROOT)

handler404 = AI.views.page_not_found
handler500 = AI.views.page_error
