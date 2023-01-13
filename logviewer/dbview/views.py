from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
import os
import sqlite3
import time
import json
import websockets

import pprint

from django.views.decorators.csrf import csrf_exempt

def load_db(query):
    dir_list = os.listdir("logs/")
    connection = sqlite3.connect("logs/"+dir_list[0])
    cursor = connection.cursor()
    rows = cursor.execute(query).fetchall()
    return(rows)

@csrf_exempt

def index(request):
    #if request.method == 'POST':
    #    for key, value in request.POST.items():
    #        print(key,value)
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
        #Hardcoded for now
        user_status = open('dbview/user_status.json')
        return HttpResponse(user_status, content_type='text/json')
    elif request.path == "/session/check_setup_ok":
        return HttpResponse('Login configured in user config')
    elif request.path == "/session/check_login":
        return HttpResponse('Login valid')
    elif request.path == "/dynamic.js":
        #INCOMPLETE - read the devices and create a dynamic.js output
        devices = load_db("select distinct(typestring) from datasources")
        load_file = open('static/dynamic.js')
        return HttpResponse(load_file, content_type='application/javascript')
    elif request.path == "/gps/location.json":
        #hardcoded cus it doesnt matter
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
        ssid_count = list(load_db("select count(device) from devices where type='Wi-Fi AP'"))
        ssid_list = "{ \"recordsTotal\": "+str(ssid_count[0][0])+", \"data\": ["
        ssids = list(load_db("select cast(device as text) from devices where type='Wi-Fi AP'"))
        for ssid in ssids:
            (single_ssid,) = ssid
            ssid_json = json.loads(single_ssid)
            try:
                ssid_list = ssid_list + "{"
                ssid_list = ssid_list + "\"dot11.ssidgroup.first_time\": \"" + str(ssid_json['dot11.device']['dot11.device.last_beaconed_ssid_record']['dot11.advertisedssid.first_time']) +"\","
                ssid_list = ssid_list + "\"dot11.ssidgroup.ssid_len\": \"" + str(ssid_json['dot11.device']['dot11.device.last_beaconed_ssid_record']['dot11.advertisedssid.ssidlen'])+"\","
                ssid_list = ssid_list + "\"dot11.ssidgroup.crypt_set\": \"" + str(ssid_json['dot11.device']['dot11.device.last_beaconed_ssid_record']['dot11.advertisedssid.crypt_set'])+"\","
                ssid_list = ssid_list + "\"dot11.ssidgroup.hash\": \"" + str(ssid_json['dot11.device']['dot11.device.last_beaconed_ssid_record']['dot11.advertisedssid.ssid_hash'])+"\","
                ssid_list = ssid_list + "\"dot11.ssidgroup.advertising_devices_len\": \"" + str(ssid_json['dot11.device']['dot11.device.num_advertised_ssids'])+"\","
                ssid_list = ssid_list + "\"dot11.ssidgroup.probing_devices_len\": \"" + str(ssid_json['dot11.device']['dot11.device.num_probed_ssids'])+"\","
                ssid_list = ssid_list + "\"dot11.ssidgroup.ssid\": \"" + str(ssid_json['dot11.device']['dot11.device.last_beaconed_ssid_record']['dot11.advertisedssid.ssid'])+"\","
                ssid_list = ssid_list + "\"dot11.ssidgroup.responding_devices_len\": \"" + str(ssid_json['dot11.device']['dot11.device.last_beaconed_ssid_record']['dot11.advertisedssid.probe_response'])+"\","
                ssid_list = ssid_list + "\"dot11.ssidgroup.last_time\": \"" + str(ssid_json['dot11.device']['dot11.device.last_beaconed_ssid_record']['dot11.advertisedssid.last_time'])+"\""
                ssid_list = ssid_list + "},"
            except:
                ssid_list = ssid_list[:-1]
                #print("Skipping")
        ssid_list = ssid_list[:-2]+ "}], \"draw\": 3, \"recordsFiltered\": "+str(ssid_count[0][0])+" }"
        return HttpResponse(ssid_list, content_type='text/json')
    elif request.path == "/system/status.json":
        #Hardcoded - Setup for other users
        user_status = open('dbview/status.json')
        return HttpResponse(user_status, content_type='text/json')
    elif request.path == "/alerts/alerts_view.json":
        #INCOMPLETE - Check device Mappings
        total_alerts=list(load_db("select count(json) from alerts"))
        (alert_count,) = total_alerts[0]
        alerts = list(load_db("select cast(json as text) from alerts"))
        alert_string="{\"recordsTotal\": "+str(alert_count)+",\"data\": ["
        for alert in alerts:
            (single_alert,) = alert
            alert_string = alert_string + single_alert + ","
        alert_string = alert_string[:-1]
        alert_string = alert_string + "], \"draw\": 6,\"recordsFiltered\": "+str(alert_count)+"}"
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
            message_string = message_string + "\"kismet.messagebus.message_flags\": \"" + str(flag) + "\","
            message_string = message_string + "\"kismet.messagebus.message_time\": \"" + str(message[0]) + "\""
            message_string = message_string + "},"
        message_string = message_string[:-1]
        message_string = message_string + "], \"kismet.messagebus.timestamp\": "+str(time.time())+" }"
        return HttpResponse(message_string, content_type='text/json')
    elif request.path == "/channels/channels.json":
        user_status = open('dbview/channels.json')
        return HttpResponse(user_status, content_type='text/json')
    #elif request.path == "/devices/views/all/devices.json":
    elif request.path.startswith("/devices/views") and request.path.endswith("devices.json"):
        device_request=request.path[15:-13]
        #print("POST INFO")
        #print(request.POST.getlist('search[value]'))
        search = str(request.POST.getlist('search[value]'))[2:-2]
        draw = str(request.POST.getlist('draw'))[2:-2]
        start = str(request.POST.getlist('start'))[2:-2]
        limit = str(request.POST.getlist('length'))[2:-2]
        total_dev=list(load_db("select count(device) from devices"))
        (dev_count,) = total_dev[0]
        dev_string = ""
        dev_string = "{ \"recordsTotal\": "+str(dev_count)+", \"data\": [ "
        if device_request == "all":
            if search == "":
                dev_list = list(load_db("select cast(device as text) from devices LIMIT "+limit+" OFFSET "+start))
            else:
                dev_list = list(load_db("select cast(device as text) from devices where cast(device as text) like '%"+search+"%' LIMIT "+limit+" OFFSET "+start))
        elif device_request == "phy_RTLADSB":
            if search == "":
                dev_list = list(load_db("select cast(device as text) from devices where phyname = 'ADSB' LIMIT "+limit+" OFFSET "+start))
            else:
                dev_list = list(load_db("select cast(device as text) from devices where cast(device as text) like '%"+search+"%' and phyname = 'ADSB' LIMIT "+limit+" OFFSET "+start))
        elif device_request == "phydot11_accesspoints":
            if search == "":
                dev_list = list(load_db("select cast(device as text) from devices where type = 'Wi-Fi AP' LIMIT "+limit+" OFFSET "+start))
            else:
                dev_list = list(load_db("select cast(device as text) from devices where cast(device as text) like '%"+search+"%' and type = 'Wi-Fi AP' LIMIT "+limit+" OFFSET "+start))
        elif device_request == "phy-BTLE":
            if search == "":
                dev_list = list(load_db("select cast(device as text) from devices where phyname = 'BTLE' LIMIT "+limit+" OFFSET "+start))
            else:
                dev_list = list(load_db("select cast(device as text) from devices where cast(device as text) like '%"+search+"%' and type = 'BTLE' LIMIT "+limit+" OFFSET "+start))
        elif device_request == "phy-Bluetooth":
            if search == "":
                dev_list = list(load_db("select cast(device as text) from devices where phyname = 'Bluetooth' LIMIT "+limit+" OFFSET "+start))
            else:
                dev_list = list(load_db("select cast(device as text) from devices where cast(device as text) like '%"+search+"%' and phyname = 'Bluetooth' LIMIT "+limit+" OFFSET "+start))
        elif device_request == "phy-RTL433":
            if search == "":
                dev_list = list(load_db("select cast(device as text) from devices where phyname = 'RTL433' LIMIT "+limit+" OFFSET "+start))
            else:
                dev_list = list(load_db("select cast(device as text) from devices where cast(device as text) like '%"+search+"%' and phyname = 'RTL433' LIMIT "+limit+" OFFSET "+start))
        elif device_request == "phy-IEEE802.11":
            if search == "":
                dev_list = list(load_db("select cast(device as text) from devices where phyname = 'IEEE802.11' LIMIT "+limit+" OFFSET "+start))
            else:
                dev_list = list(load_db("select cast(device as text) from devices where cast(device as text) like '%"+search+"%' and phyname = 'IEEE802.11' LIMIT "+limit+" OFFSET "+start))
        elif device_request == "phy-RADIATION":
            if search == "":
                dev_list = list(load_db("select cast(device as text) from devices where phyname = 'RADIATION' LIMIT "+limit+" OFFSET "+start))
            else:
                dev_list = list(load_db("select cast(device as text) from devices where cast(device as text) like '%"+search+"%' and phyname = 'RADIATION' LIMIT "+limit+" OFFSET "+start))
        elif device_request == "phy-802.15.4":
            if search == "":
                dev_list = list(load_db("select cast(device as text) from devices where phyname = '802.15.4' LIMIT "+limit+" OFFSET "+start))
            else:
                dev_list = list(load_db("select cast(device as text) from devices where cast(device as text) like '%"+search+"%' and phyname = '802.15.4' LIMIT "+limit+" OFFSET "+start))
        elif device_request == "phy-RTLAMR":
            if search == "":
                dev_list = list(load_db("select cast(device as text) from devices where phyname = 'METER' LIMIT "+limit+" OFFSET "+start))
            else:
                dev_list = list(load_db("select cast(device as text) from devices where cast(device as text) like '%"+search+"%' and phyname = 'METER' LIMIT "+limit+" OFFSET "+start))
        elif device_request == "phy-NrfMousejack":
            if search == "":
                dev_list = list(load_db("select cast(device as text) from devices where phyname = 'NrfMousejack' LIMIT "+limit+" OFFSET "+start))
            else:
                dev_list = list(load_db("select cast(device as text) from devices where cast(device as text) like '%"+search+"%' and phyname = 'NrfMousejack' LIMIT "+limit+" OFFSET "+start))
        elif device_request == "phy-UAV":
            if search == "":
                dev_list = list(load_db("select cast(device as text) from devices where phyname = 'UAV' LIMIT "+limit+" OFFSET "+start))
            else:
                dev_list = list(load_db("select cast(device as text) from devices where cast(device as text) like '%"+search+"%' and phyname = 'UAV' LIMIT "+limit+" OFFSET "+start))
        elif device_request == "phy-Zwave":
            if search == "":
                dev_list = list(load_db("select cast(device as text) from devices where phyname = 'Z-Wave' LIMIT "+limit+" OFFSET "+start))
            else:
                dev_list = list(load_db("select cast(device as text) from devices where cast(device as text) like '%"+search+"%' and phyname = 'Z-Wave' LIMIT "+limit+" OFFSET "+start))
        for device in dev_list:
            (dev,) = device
            dev_json = json.loads(dev)
            newdev = {}
            newdev['kismet.device.base.commonname'] = dev_json['kismet.device.base.commonname']
            newdev['kismet.device.base.type'] = dev_json['kismet.device.base.type']
            newdev['kismet.device.base.phyname'] = dev_json['kismet.device.base.phyname']
            newdev['kismet.device.base.crypt'] = dev_json['kismet.device.base.crypt']
            newdev['kismet.device.base.channel'] = dev_json['kismet.device.base.channel']
            newdev['kismet.device.base.datasize'] = dev_json['kismet.device.base.datasize']
            newdev['kismet.device.base.last_time'] = dev_json['kismet.device.base.last_time']
            newdev['kismet.device.base.first_time'] = dev_json['kismet.device.base.first_time']
            newdev['kismet.device.base.key'] = dev_json['kismet.device.base.key']
            newdev['kismet.device.base.macaddr'] = dev_json['kismet.device.base.macaddr']
            newdev['kismet.device.base.frequency'] = dev_json['kismet.device.base.frequency']
            newdev['kismet.device.base.manuf'] = dev_json['kismet.device.base.manuf']
            if newdev['kismet.device.base.phyname'] == "IEEE802.11":
                newdev['adsb.device'] = 0
                newdev['bluetooth.device'] = 0
                newdev['uav.device'] = 0
            if newdev['kismet.device.base.phyname'] == "Bluetooth":
                newdev['adsb.device'] = 0
                newdev['uav.device'] = 0
                newdev['buetooth.device'] = dev_json['bluetooth.device']
            if newdev['kismet.device.base.phyname'] == "ADSB":
                newdev['bluetooth.device'] = 0
                newdev['uav.device'] = 0
                newdev['adsb.device'] = dev_json['adsb.device']
            if "kismet.common.rrd.last_time" in dev_json:
                newdev['kismet.common.rrd.last_time'] = dev_json['kismet.common.rrd.last_time']
            if "dot11.device.num_associated_clients" in dev_json:
                newdev['dot11.device.num_associated_clients'] = dev_json['dot11.device.num_associated_clients']
            if "dot11.device.last_bssid" in dev_json:
                newdev['dot11.device.last_bssid'] = dev_json['dot11.device.last_bssid']
            if "dot11.advertisedssid.dot11e_channel_utilization_perc" in dev_json:
                newdev['dot11.advertisedssid.dot11e_channel_utilization_perc'] = dev_json['dot11.advertisedssid.dot11e_channel_utilization_perc']
            if "dot11.advertisedssid.dot11e_qbss_stations" in dev_json:
                newdev['dot11.advertisedssid.dot11e_qbss_stations'] = dev_json['dot11.advertisedssid.dot11e_qbss_stations']
            if "kismet.common.signal.last_signal" in dev_json:
                newdev['kismet.common.signal.last_signal'] = dev_json['kismet.common.signal.last_signal']
            if "dot11.device.bss_timestamp" in dev_json:
                newdev['dot11.device.bss_timestamp'] = dev_json['dot11.device.bss_timestamp']
            if "dot11.advertisedssid.dot11e_qbss" in dev_json:
                newdev['dot11.advertisedssid.dot11e_qbss'] = dev_json['dot11.advertisedssid.dot11e_qbss']
            if "dot11.device.wpa_handshake_list" in dev_json:
                newdev['dot11.device.wpa_handshake_list'] = dev_json['dot11.device.wpa_handshake_list']
            if "dot11.device.pmkid_packet" in dev_json:
                newdev['dot11.device.pmkid_packet'] = dev_json['dot11.device.pmkid_packet']
            if "kismet.common.rrd.serial_time" in dev_json:
                newdev['kismet.common.rrd.serial_time'] = dev_json['kismet.common.rrd.serial_time']
            
            #print("====")
            #print(json.dumps(newdev))
            #print(dev_json['kismet.device.base.commonname'])
            #print("====")
            #dev_string = dev_string + dev + ","
            dev_string = dev_string + json.dumps(newdev) + ","
        dev_string = dev_string[:-1]
        dev_string = dev_string + "],\"draw\": "+draw+",\"recordsFiltered\": "+str(dev_count)+"}"
        return HttpResponse(dev_string, content_type='text/json')
    elif request.path == "/eventbus/events.ws":
        return HttpResponse("[]", content_type='text/json')
    elif request.path == "/devices/multikey/as-object/devices.json":
        #ClientMap incomplete.... figure out where the rest of the JSON comes from
        search_json = ""
        multikey = "{"
        for key, value in request.POST.items():
            search_json=json.loads(value)
            for device in search_json['devices']:
                device_json = list(load_db("select cast(device as text) from devices where devkey='"+str(device)+"'"))
                (tmp,) = device_json
                device_json_x = json.loads(str(tmp[0]))
                multikey = multikey + "\""+str(device)+"\": {"
                for field in search_json['fields']:
                    if (field[0:6] == "kismet"):
                        multikey = multikey + "\""+field+"\": \""+device_json_x[field]+"\","
                multikey = multikey + "\"dot11.device.client_map\": {},"
                multikey = multikey[:-1]
                multikey = multikey + "},"
        multikey = multikey[:-1]
        multikey = multikey + "}"
        return HttpResponse(multikey, content_type='text/json')
