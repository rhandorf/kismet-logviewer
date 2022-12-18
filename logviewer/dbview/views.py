from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
import os

def index(request):
    if request.path == "/devices/views/all_views.json":
        all_views = open('/home/rhandorf/kismet-logviewer/logviewer/dbview/all_views.json')
        return HttpResponse(all_views, content_type='text/json')
    elif request.path == "/system/user_status.json":
        user_status = open('/home/rhandorf/kismet-logviewer/logviewer/dbview/user_status.json')
        return HttpResponse(user_status, content_type='text/json')
    elif request.path == "/session/check_setup_ok":
        return HttpResponse('Login configured in user config')
    elif request.path == "/session/check_login":
        return HttpResponse('Login valid')
    elif request.path == "/dynamic.js":
        load_file = open('/home/rhandorf/kismet-logviewer/logviewer/static/dynamic.js')
        return HttpResponse(load_file, content_type='application/javascript')
    elif request.path == "/gps/location.json":
        user_status = open('/home/rhandorf/kismet-logviewer/logviewer/dbview/gps_status.json')
        return HttpResponse(user_status, content_type='text/json')
    elif request.path == "/alerts/alerts_view.json":
        user_status = open('/home/rhandorf/kismet-logviewer/logviewer/dbview/alerts_view.json')
        return HttpResponse(user_status, content_type='text/json')
    elif request.path == "/phy/phy80211/ssids/views/ssids.json":
        user_status = open('/home/rhandorf/kismet-logviewer/logviewer/dbview/ssids.json')
        return HttpResponse(user_status, content_type='text/json')
    elif request.path == "/system/status.json":
        user_status = open('/home/rhandorf/kismet-logviewer/logviewer/dbview/status.json')
        return HttpResponse(user_status, content_type='text/json')
    elif request.path == "/alerts/wrapped/last-time/0/alerts.json":
        user_status = open('/home/rhandorf/kismet-logviewer/logviewer/dbview/alerts.json')
        return HttpResponse(user_status, content_type='text/json')
    elif request.path == "/messagebus/last-time/0/messages.json":
        user_status = open('/home/rhandorf/kismet-logviewer/logviewer/dbview/messages.json')
        return HttpResponse(user_status, content_type='text/json')
    elif request.path == "/channels/channels.json":
        user_status = open('/home/rhandorf/kismet-logviewer/logviewer/dbview/channels.json')
        return HttpResponse(user_status, content_type='text/json')
    elif request.path == "/devices/views/all/devices.json":
        user_status = open('/home/rhandorf/kismet-logviewer/logviewer/dbview/devices.json')
        return HttpResponse(user_status, content_type='text/json')


