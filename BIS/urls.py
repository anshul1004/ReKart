"""BIS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from ReKart.views import *
from django.contrib.auth.views import login
from django.conf.urls import url, include
from django.contrib import admin
import ReKart.views
from django.conf import settings
from django.conf.urls import patterns
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', homepage),
    url(r'^base/', base),
    url(r'^contact/', contact_us),
    url(r'^logout/$', logout),
    url(r'^accounts/login/$', login1), # If user is not login it will redirect to login page
    url(r'^register/$', register),
    url(r'^register/success/$', register_success),
    url(r'^confirm/(?P<activation_key>\w+)/', register_confirm),
    url(r'^upload/$', ReKart.views.upload, name='upload'),
    url(r'uploaded/$', ReKart.views.uploaded, name='uploaded'),
    url(r'display/$', ReKart.views.display, name='display'),
    url(r'^kartadd/(?P<itemid1>\w+)/$', add_to_kart),
    url(r'^kartdel/(?P<itemid1>\w+)/$', del_from_kart),
    url(r'^kart/$', disp_kart),
    url(r'^view/(?P<itemid>\w+)/', ReKart.views.view, name='view'),
    url(r'^returnfrompaypal/', ReKart.views.returnfrompaypal, name='returnfrompaypal'),
    url(r'^cancel/', ReKart.views.cancel, name='cancel'),
    url(r'^success/', ReKart.views.success, name='success'),
    url(r'^payment-url/(?P<amt>[0-9]+)/$', ReKart.views.buy_my_item, name="views.buy_my_item"),
    url(r'^paypal/', include('paypal.standard.ipn.urls')),
    url(r'^payment/(?P<amount>[0-9]+)/(?P<itemid>[0-9]+)/$', ReKart.views.view_that_asks_for_money, name='payment'),
    url(r'^paypal/', include('paypal.standard.ipn.urls')),


]
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))