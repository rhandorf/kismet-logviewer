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
def index(request,devicename):
    #print("-------------")
    #print(request.path)
    #print(devicename)
    #print("-------------")
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

