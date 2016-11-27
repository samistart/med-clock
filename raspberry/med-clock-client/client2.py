import bluetooth
import time
from tornado.httpclient import HTTPClient, HTTPRequest
from urllib import urlencode
from tornado.httputil import url_concat
import json
from datetime import datetime

devices = {}
serverIp = "52.211.183.223"

#Ed's raspberry
enterStation = "nurse_begins_prep"
leaveStation = "begin_dialysis"


def patientInStage(patientId, stage):
    client = HTTPClient()
    try:
        response = client.fetch("http://" + serverIp + ":5000/api/patient/" + patientId.rstrip())
    except Exception as e:
        print("get patient in stage request error")
        print("Error: " + str(e))
        return True

    try:
        decoded = json.loads(response.body)
        if stage in decoded and decoded[stage] is None:
            print("patient: " + patientId + " not in stage " + stage)
            return False
        else:
            print("patient: " + patientId + " in stage " + stage)
            return True
    except Exception as e:
        print("decode patient stage error")
        print("Error: " + str(e))
        return True


def getMac(mac):
    client = HTTPClient()
    try:
        response = client.fetch("http://" + serverIp + ":5000/api/macmap/" + mac)
    except Exception as e:
        print("Error: " + str(e))
        return None

    # json = json.loads(response.body)
    print("got patient ID: " + response.body)
    return response.body


def sendStageRequest(patientId, timestamp, station):
    # Add area entering time
    body = {station: str(datetime.fromtimestamp(timestamp))}

    client = HTTPClient()
    try:
        headers = {'Content-Type': 'application/json; charset=UTF-8'}
        url = "http://" + serverIp + ":5000/api/patient/" + patientId.rstrip()
        print(url)
        from pprint import pprint
        pprint(body)
        request = HTTPRequest(url, method="PUT", body=json.dumps(body), headers=headers)
        response = client.fetch(request)
        print(response.body)
        client.close()
    except Exception as e:
        print("error in add stage request")
        print("Error: " + str(e))

    return


def enterStage(addr, timestamp):
    client = HTTPClient()

    patientId = getMac(addr)
    if patientId is None or patientId is 0:
        return  # Unable to retreive patient -> quit

    if patientInStage(patientId, enterStation) == True:
        return  # Patient already logged -> quit

    return sendStageRequest(patientId, timestamp, enterStation)


def leaveStage(addr, timestamp):
    client = HTTPClient()

    patientId = getMac(addr)
    if patientId is None or patientId is 0:
        return  # Unable to retreive patient -> quit

    if patientInStage(patientId, leaveStation) == True:
        return  # Patient already logged -> quit

    return sendStageRequest(patientId, timestamp, leaveStation)


def scan():
    timeStamp = int(time.time())
    nearby_devices = bluetooth.discover_devices(duration=1, lookup_names=True)
    print("found %d devices" % len(nearby_devices))

    for addr, name in nearby_devices:
        if (addr not in devices):  # add new device
            devices[addr] = (name, timeStamp)
            print("new device:   %s - %s added on: %s" % (addr, name, str(devices[addr][1])))
            enterStage(addr, timeStamp)
        else:
            # update timestime
            devices[addr] = (name, timeStamp)
            print("updated device: %s - %s, new time: %s" % (addr, name, str(devices[addr][1])))
    return timeStamp


def remove_before_time(timeStamp):
    from pprint import pprint
    # pprint(devices)
    for device, data in devices.items():
        if data[1] < timeStamp:
            print("removing device: %s - %s, addedTime: %s" % (device, data[0], data[1]))
            leaveStage(device, data[1])
            del devices[device]


def main():
    while (True):
        scanTime = scan()
        remove_before_time(scanTime - 10)


if __name__ == '__main__':
    main()
