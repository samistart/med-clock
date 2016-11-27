import bluetooth
import time
from tornado.httpclient import HTTPClient, HTTPRequest
from urllib import urlencode
from tornado.httputil import url_concat
import json
from datetime import datetime

devices = {}
serverIp = "52.211.183.223"

station = "enter_waiting_room"


def patientInStage(patientId):
    client = HTTPClient()
    try:
        response = client.fetch("http://" + serverIp + ":5000/api/patient/" + patientId.rstrip())
    except Exception as e:
        print("get patient in stage request error")
        print("Error: " + str(e))
        return True

    try:
        decoded = json.loads(response.body)
        if "enter_waiting_room" in decoded and decoded["enter_waiting_room"] is None:
            print("patient: " + patientId + " not in stage")
            return False
        else:
            print("patient: " + patientId + " in stage")
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


def enterStage(addr, timestamp):
    client = HTTPClient()

    patientId = getMac(addr)
    if patientId is None or patientId is 0:
        return  # Unable to retreive patient -> quit

    if patientInStage(patientId) == True:
        return  # Patient already logged -> quit

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


def leaveStage(addr, timestamp):
    client = HTTPClient()
    body = {"experiment_id": 1, "patient_id": 1, "stage_id": 1, "patient": addr, "timestamp": timestamp}

    response = client.fetch("http://" + serverIp + ":5000/api/stage/1", method="POST", body=urlencode(body),
                            headers=urlencode({}))

    print(response.body)
    client.close()
    return


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
            # leaveStage(addr, timeStamp)
    return timeStamp


def remove_before_time(timeStamp):
    from pprint import pprint
    # pprint(devices)
    for device, data in devices.items():
        if data[1] < timeStamp:
            print("removing device: %s - %s, addedTime: %s" % (device, data[0], data[1]))
            del devices[device]


def main():
    while (True):
        scanTime = scan()
        remove_before_time(scanTime - 10)


if __name__ == '__main__':
    main()
