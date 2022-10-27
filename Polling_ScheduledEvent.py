import json
from venv import create
import requests
import datetime
import time
import threading
import os

metadata_url ="http://169.254.169.254/metadata/scheduledevents"
header = {'Metadata' : 'true'}
query_params = {'api-version':'2020-07-01'}
basepath = '/mnt/files-east-vm1/'

def get_now():
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    return now.strftime('%Y%m%d-%H%M%S')

def get_scheduled_events():
    resp = requests.get(metadata_url, headers = header, params = query_params)
    data = resp.json()
    return data

def create_result_file():
    data = get_scheduled_events()
    now_time = get_now()
    filename = str(now_time)+".json"

    year = now_time[0:4]
    month = now_time[4:6]
    day = now_time[6:8]
    hour = now_time[9:11]
    minutes = now_time[11:13]
    datepath = year + '/' + month + '/' + day + '/' + hour + '/' + minutes + '/'

    path = basepath + datepath + filename
    os.makedirs(basepath + datepath, exist_ok=True)
    with open(path, 'w') as file:
        json.dump(data, file, indent=4)

def scheduler(interval, func, wait = True):
    base_time = time.time()
    next_time = 0
    while True:
        t = threading.Thread(target = func)
        t.start()
        if wait:
            t.join()
        next_time = ((base_time - time.time()) % interval) or interval
        time.sleep(next_time)

def main():
    scheduler(1, create_result_file, False)

main()