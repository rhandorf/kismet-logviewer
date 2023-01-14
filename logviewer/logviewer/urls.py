"""logviewer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import include, path
from django.http import HttpResponse

urlpatterns = [
    path('', include('browse.urls')),
    path('admin/', admin.site.urls),
    path('dbview/', include('dbview.urls')),
    path('devices/views/all_views.json', include('dbview.urls')),
    path('system/user_status.json', include('dbview.urls')),
    path('session/check_setup_ok', include('dbview.urls')),
    path('session/check_login', include('dbview.urls')),
    path('js/<str:loadfile>', include('kiscontent.urls')),
    path('css/<str:loadfile>', include('kiscontent.urls')),
    path('images/<str:loadfile>', include('kiscontent.urls')),
    path('fonts/<str:loadfile>', include('kiscontent.urls')),
    path('favicon.ico', include('kiscontent.urls')),
    path('dynamic.js', include('dbview.urls')),
    path('gps/location.json', include('dbview.urls')),
    path('alerts/alerts_view.json', include('dbview.urls')),
    path('phy/phy80211/ssids/views/ssids.json', include('dbview.urls')),
    path('css/images/<str:loadfile>', include('kiscontent.urls')),
    path('adsb_map_panel.html', include('adsbmap.urls')),
    path('system/status.json', include('dbview.urls')),
    path('alerts/wrapped/last-time/0/alerts.json', include('dbview.urls')),
    path('messagebus/last-time/0/messages.json', include('dbview.urls')),
    path('channels/channels.json', include('dbview.urls')),
    path('devices/views/all/devices.json', include('dbview.urls')),
    path('devices/views/phydot11_accesspoints/devices.json', include('dbview.urls')),
    path('devices/views/phy-RADIATION/devices.json', include('dbview.urls')),
    path('devices/views/phy-802.15.4/devices.json', include('dbview.urls')),
    path('devices/views/phy-RTLADSB/devices.json', include('dbview.urls')),
    path('devices/views/phy-RTLAMR/devices.json', include('dbview.urls')),
    path('devices/views/phy-BTLE/devices.json', include('dbview.urls')),
    path('devices/views/phy-NrfMousejack/devices.json', include('dbview.urls')),
    path('devices/views/phy-UAV/devices.json', include('dbview.urls')),
    path('devices/views/phy-Bluetooth/devices.json', include('dbview.urls')),
    path('devices/views/phy-Z-Wave/devices.json', include('dbview.urls')),
    path('devices/views/phy-RTL433/devices.json', include('dbview.urls')),
    path('devices/views/phy-IEEE802.11/devices.json', include('dbview.urls')),
    path('phy/ADSB/map_data.json', include('dbview.urls')),
    path('devices/by-key/<str:devicename>/device.json', include('devices.urls')),
    path('devices/multikey/as-object/devices.json', include('dbview.urls')),
    path('datasource/by-uuid/<str:devicename>/source.json', include('devices.urls')),
    path('phy/phy80211/ssids/by-hash/<str:devicename>/ssid.json', include('devices.urls')),
    path('eventbus/', include('eventbus.urls')),
]
