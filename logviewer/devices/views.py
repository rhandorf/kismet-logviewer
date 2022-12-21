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
    cursor = connection.cursor()
    rows = cursor.execute(query).fetchall()
    return(rows)

@csrf_exempt
def index(request,devicename):
    if request.path[0:8] == "/devices":
        dev=list(load_db("select cast(device as text) from devices where devkey = \""+devicename+"\""))
        (dev_info,) = dev[0]
        #dev_string = "{ \"recordsTotal\": "+str(dev_count)+", \"data\": ["
        #dev_list = list(load_db("select cast(device as text) from devices limit 50"))
        #for device in dev_list:
        #    (dev,) = device
        #    dev_string = dev_string + dev + ","
        #dev_string = dev_string[:-1]
        #dev_string = dev_string + "],\"draw\": 5,\"recordsFiltered\": "+str(dev_count)+"}"
        return HttpResponse(dev_info, content_type='text/json')
    elif request.path[0:11] == "/datasource":
        datasource=list(load_db("select cast(json as text) from datasources where uuid = \""+str(devicename)+"\""))
        (json_result,) = datasource[0]
        return HttpResponse(json_result, content_type='text/json')
    elif request.path[0:4] == "/phy":
        #INCOMPLETE - Need to work out device mappings still
        devices=list(load_db("select cast(device as text) from devices where type='Wi-Fi AP'"))
        for device in devices:
            (json_result,) = device
            device_json = json.loads(json_result)
            try:
                if str(devicename) == str(device_json['dot11.device']['dot11.device.last_beaconed_ssid_record']['dot11.advertisedssid.ssid_hash']):
                    print("MATCH")
                    print(device_json)
            except:
                print("skipping")
        return HttpResponse("{}", content_type='text/json')
