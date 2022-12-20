from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
import os
import sqlite3
import time
import json
import pprint

from django.views.decorators.csrf import csrf_exempt

def load_db(query):
    connection = sqlite3.connect("logs/Kismet-20221208-22-56-36-1.kismet")
    #connection.row_factory = lambda cursor, row: row[0]
    cursor = connection.cursor()
    rows = cursor.execute(query).fetchall()
    return(rows)

@csrf_exempt
def index(request,devicename):
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

