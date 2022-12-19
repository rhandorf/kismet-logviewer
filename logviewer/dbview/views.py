from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
import os
import sqlite3
import time
import json
import pprint

from django.views.decorators.csrf import csrf_exempt

def load_db(query):
    connection = sqlite3.connect("/home/rhandorf/kismet-logviewer/logviewer/logs/Kismet-20221208-22-56-36-1.kismet")
    #connection.row_factory = lambda cursor, row: row[0]
    cursor = connection.cursor()
    rows = cursor.execute(query).fetchall()
    return(rows)

@csrf_exempt
def index(request):
    #if request.method == 'POST':
    #    print("GOT A POST")
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
        devices = load_db("select distinct(typestring) from datasources")
        load_file = open('/home/rhandorf/kismet-logviewer/logviewer/static/dynamic.js')
        return HttpResponse(load_file, content_type='application/javascript')
    elif request.path == "/gps/location.json":
        user_status = open('/home/rhandorf/kismet-logviewer/logviewer/dbview/gps_status.json')
        return HttpResponse(user_status, content_type='text/json')
    elif request.path == "/alerts/wrapped/last-time/0/alerts.json":
        alerts = list(load_db("select cast(json as text) from alerts"))
        alert_string="{\"kismet.alert.list\": ["
        for alert in alerts:
            (single_alert,) = alert
            alert_string = alert_string + single_alert + ","
        alert_string = alert_string[:-1]
        alert_string = alert_string + "] ,\"kismet.alert.timestamp\": "+str(time.time())+"}"
        return HttpResponse(alert_string, content_type='text/json')
    elif request.path == "/phy/phy80211/ssids/views/ssids.json":
        user_status = open('/home/rhandorf/kismet-logviewer/logviewer/dbview/ssids.json')
        return HttpResponse(user_status, content_type='text/json')
    elif request.path == "/system/status.json":
        user_status = open('/home/rhandorf/kismet-logviewer/logviewer/dbview/status.json')
        return HttpResponse(user_status, content_type='text/json')
    elif request.path == "/alerts/alerts_view.json":
        #MAY NOT BE COMPLETE
        alerts = list(load_db("select cast(json as text) from alerts"))
        alert_string="["
        for alert in alerts:
            (single_alert,) = alert
            alert_string = alert_string + single_alert + ","
        alert_string = alert_string[:-1]
        alert_string = alert_string + "]"
        return HttpResponse(alert_string, content_type='text/json')
    elif request.path == "/messagebus/last-time/0/messages.json":
        messages = list(load_db("select * from messages DESC limit 30"))
        message_string="{\"kismet.messagebus.list\": ["
        for message in messages:
            message_string = message_string + "{"
            message_string = message_string + "\"kismet.messagebus.message_string\": \"" + message[4] + "\","
            flag = "0"
            if message[3] == "INFO":
                flag = "0"
            if message[3] == "LOW":
                flag = "5"
            if message[3] == "MEDIUM":
                flag = "10"
            if message[3] == "HIGH":
                flag = "15"
            if message[3] == "CRITICAL":
                flag = 20
            if message[3] == "ERROR":
                flag = 20
            message_string = message_string + "\"kismet.messagebus.message_flags\": \"" + flag + "\","
            message_string = message_string + "\"kismet.messagebus.message_time\": \"" + str(message[0]) + "\""
            message_string = message_string + "},"
        message_string = message_string[:-1]
        message_string = message_string + "], \"kismet.messagebus.timestamp\": "+str(time.time())+" }"
        return HttpResponse(message_string, content_type='text/json')
    elif request.path == "/channels/channels.json":
        user_status = open('/home/rhandorf/kismet-logviewer/logviewer/dbview/channels.json')
        return HttpResponse(user_status, content_type='text/json')
    elif request.path == "/devices/views/all/devices.json":
        #gotta figure out paging
        total_dev=list(load_db("select count(device) from devices"))
        (dev_count,) = total_dev[0]
        dev_string = "{ \"recordsTotal\": "+str(dev_count)+", \"data\": ["
        dev_list = list(load_db("select cast(device as text) from devices limit 50"))
        for device in dev_list:
            (dev,) = device
            dev_string = dev_string + dev + ","
        dev_string = dev_string[:-1]
        dev_string = dev_string + "],\"draw\": 5,\"recordsFiltered\": "+str(dev_count)+"}"
        return HttpResponse(dev_string, content_type='text/json')
    elif request.path == "/eventbus/events.ws":
        return HttpResponse("[]", content_type='text/json')


