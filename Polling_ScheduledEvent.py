import json
from venv import create
import requests
import datetime
import time
import threading

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
    filename = str(get_now())+".json"
    path = basepath + filename
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