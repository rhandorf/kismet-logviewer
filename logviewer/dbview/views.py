from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
import os
import sqlite3
import time
import json
import pprint

from django.views.decorators.csrf import csrf_exempt

def load_db(query):
    dir_list = os.listdir("logs/")
    connection = sqlite3.connect("logs/"+dir_list[0])
    #connection.row_factory = lambda cursor, row: row[0]
    cursor = connection.cursor()
    rows = cursor.execute(query).fetchall()
    return(rows)

@csrf_exempt
def index(request):
    #if request.method == 'POST':
    #    print("GOT A POST")
    if request.path == "/devices/views/all_views.json":
        uuid_members="["
        dev_count=list(load_db("select count(device) from devices where type='Wi-Fi AP'"))
        (devcount,) = dev_count[0]
        uuid_members = uuid_members + "{ \"kismet.devices.view.description\": \"IEEE802.11 Access Points\", \"kismet.devices.view.id\": \"phydot11_accesspoints\", \"kismet.devices.view.size\": "+str(devcount)+" },"
        dev_count=list(load_db("select count(device) from devices where phyname='IEEE802.11'"))
        (devcount,) = dev_count[0]
        uuid_members = uuid_members + "{ \"kismet.devices.view.description\": \"IEEE802.11 devices\", \"kismet.devices.view.id\": \"phy-IEEE802.11\", \"kismet.devices.view.size\": "+str(devcount)+" },"
        dev_count=list(load_db("select count(device) from devices where type='RTL433'"))
        (devcount,) = dev_count[0]
        uuid_members = uuid_members + "{ \"kismet.devices.view.description\": \"RTL433 devices\", \"kismet.devices.view.id\": \"phy-RTL433\", \"kismet.devices.view.size\": "+str(devcount)+" },"
        dev_count=list(load_db("select count(device) from devices where type='Z-wave'"))
        (devcount,) = dev_count[0]
        uuid_members = uuid_members + "{ \"kismet.devices.view.description\": \"Z-Wave devices\", \"kismet.devices.view.id\": \"phy-Z-Wave\", \"kismet.devices.view.size\": "+str(devcount)+" },"
        dev_count=list(load_db("select count(device) from devices where type='BR/EDR'"))
        (devcount,) = dev_count[0]
        uuid_members = uuid_members + "{ \"kismet.devices.view.description\": \"Bluetooth devices\", \"kismet.devices.view.id\": \"phy-Bluetooth\", \"kismet.devices.view.size\": "+str(devcount)+" },"
        dev_count=list(load_db("select count(device) from devices where type='UAV'"))
        (devcount,) = dev_count[0]
        uuid_members = uuid_members + "{ \"kismet.devices.view.description\": \"UAV devices\", \"kismet.devices.view.id\": \"phy-UAV\", \"kismet.devices.view.size\": "+str(devcount)+" },"
        dev_count=list(load_db("select count(device) from devices where type='NrfMousejack'"))
        (devcount,) = dev_count[0]
        uuid_members = uuid_members + "{ \"kismet.devices.view.description\": \"NrfMousejack devices\", \"kismet.devices.view.id\": \"phy-NrfMousejack\", \"kismet.devices.view.size\": "+str(devcount)+"},"
        dev_count=list(load_db("select count(device) from devices where type='BTLE'"))
        (devcount,) = dev_count[0]
        uuid_members = uuid_members + "{ \"kismet.devices.view.description\": \"BTLE devices\", \"kismet.devices.view.id\": \"phy-BTLE\", \"kismet.devices.view.size\": "+str(devcount)+" },"
        dev_count=list(load_db("select count(device) from devices where phyname='AMR'"))
        (devcount,) = dev_count[0]
        uuid_members = uuid_members + "{ \"kismet.devices.view.description\": \"RTLAMR devices\", \"kismet.devices.view.id\": \"phy-RTLAMR\", \"kismet.devices.view.size\": "+str(devcount)+" },"
        dev_count=list(load_db("select count(device) from devices where phyname='ADSB'"))
        (devcount,) = dev_count[0]
        uuid_members = uuid_members + "{ \"kismet.devices.view.description\": \"RTLADSB devices\", \"kismet.devices.view.id\": \"phy-RTLADSB\", \"kismet.devices.view.size\": "+str(devcount)+" },"
        dev_count=list(load_db("select count(device) from devices where phyname='802.15.4'"))
        (devcount,) = dev_count[0]
        uuid_members = uuid_members + "{ \"kismet.devices.view.description\": \"802.15.4 devices\", \"kismet.devices.view.id\": \"phy-802.15.4\", \"kismet.devices.view.size\": "+str(devcount)+" },"
        dev_count=list(load_db("select count(device) from devices where phyname='RADIATION'"))
        (devcount,) = dev_count[0]
        uuid_members = uuid_members + "{ \"kismet.devices.view.description\": \"RADIATION devices\", \"kismet.devices.view.id\": \"phy-RADIATION\", \"kismet.devices.view.size\": "+str(devcount)+" },"
        total_dev=list(load_db("select count(device) from devices"))
        (devcount,) = total_dev[0]
        uuid_members=uuid_members+"{ \"kismet.devices.view.description\": \"All devices\", \"kismet.devices.view.id\": \"all\", \"kismet.devices.view.size\": "+str(devcount)+" },"
        uuid_list = list(load_db("select uuid from datasources"))
        for uuid in uuid_list:
            (single_uuid,) = uuid
            uuid_count = list(load_db("select count(*) from data where datasource='"+str(single_uuid)+"'"))
            (single_uuid_count,) = uuid_count[0]
            uuid_members = uuid_members + "{\"kismet.devices.view.description\": \"Devices seen by datasource "+single_uuid+"\","
            uuid_members = uuid_members + "\"kismet.devices.view.id\": \"seenby-"+single_uuid+"\","
            uuid_members = uuid_members + "\"kismet.devices.view.size\": "+str(single_uuid_count)+"},"
        uuid_members=uuid_members[:-1]
        uuid_members=uuid_members+"]"
        return HttpResponse(uuid_members, content_type='text/json')
    elif request.path == "/system/user_status.json":
        user_status = open('dbview/user_status.json')
        return HttpResponse(user_status, content_type='text/json')
    elif request.path == "/session/check_setup_ok":
        return HttpResponse('Login configured in user config')
    elif request.path == "/session/check_login":
        return HttpResponse('Login valid')
    elif request.path == "/dynamic.js":
        devices = load_db("select distinct(typestring) from datasources")
        load_file = open('static/dynamic.js')
        return HttpResponse(load_file, content_type='application/javascript')
    elif request.path == "/gps/location.json":
        user_status = open('dbview/gps_status.json')
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
        user_status = open('dbview/ssids.json')
        return HttpResponse(user_status, content_type='text/json')
    elif request.path == "/system/status.json":
        user_status = open('dbview/status.json')
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
        user_status = open('dbview/channels.json')
        return HttpResponse(user_status, content_type='text/json')
    elif request.path == "/devices/views/all/devices.json":
        #for key, value in request.POST.items():
        #    #print("-----")
        #    print(key+" = "+value)
        #    #print(value)
        #    if key == "draw":
        #        print("-----")
        #        print("DRAW")
        #        print(value)
        #        print("-----")
        #gotta figure out paging

        total_dev=list(load_db("select count(device) from devices"))
        (dev_count,) = total_dev[0]
        dev_string = "{ \"recordsTotal\": "+str(dev_count)+", \"data\": ["
        dev_list = list(load_db("select cast(device as text) from devices limit 54"))
        for device in dev_list:
            (dev,) = device
            dev_string = dev_string + dev + ","
        dev_string = dev_string[:-1]
        dev_string = dev_string + "],\"draw\": 5,\"recordsFiltered\": "+str(dev_count)+"}"
        #dev_string = open('dbview/devices.json')
        return HttpResponse(dev_string, content_type='text/json')
    elif request.path == "/eventbus/events.ws":
        return HttpResponse("[]", content_type='text/json')
    elif request.path == "/devices/multikey/as-object/devices.json":
        print("here")
        for key, value in request.POST.items():
            print("-----")
            print(key)
            print(value)
            print("-----")
        return HttpResponse("[]", content_type='text/json')
