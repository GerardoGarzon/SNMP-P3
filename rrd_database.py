from datetime import datetime
from gmail_notifications import send_alert_attached
import rrdtool
import csv
import os

cpu_limit = [50, 75, 90]
ram_limit = [60, 80, 90]
hdd_limit = [70, 80, 90]


def create_database(ip_address, type_data):
    database_dir = os.getcwd() + "/data/devices_files/" + ip_address
    params = [database_dir + "/" + type_data + ".rrd"]
    params += ["--start", 'N']
    params += ["--step", '5']
    params += ["DS:" + type_data + "Load:GAUGE:5:U:U"]
    params += ["DS:" + type_data + "Max:GAUGE:5:U:U"]
    params += ["RRA:AVERAGE:0.5:1:100"]
    params += ["RRA:AVERAGE:0.5:1:100"]

    result = rrdtool.create(params)

    if result:
        print(rrdtool.error())


def update_database(ip_address, type_data, value, max_value, last_notification):
    database_dir = os.getcwd() + "/data/devices_files/" + ip_address + "/" + type_data + ".rrd"
    database_csv = os.getcwd() + "/data/devices_files/" + ip_address + "/" + type_data + ".csv"

    rrdtool.update(database_dir, value)
    with open(database_csv, 'a', newline='') as f:
        writer = csv.writer(f)
        split_value = value.split(":")
        writer.writerow([split_value[1], max_value])
    graph_detection(ip_address, type_data, max_value)

    last_notification = verify_limits(type_data, max_value, split_value[1], last_notification, ip_address)

    return last_notification


def graph_detection(ip_address, type_data, max_value):
    database_dir = os.getcwd() + "/data/devices_files/" + ip_address + "/" + type_data + ".rrd"
    image_output = os.getcwd() + "/data/devices_files/" + ip_address + "/"

    last_update = int(rrdtool.last(database_dir))
    start_time = last_update - 3000

    ret = rrdtool.graphv(str(image_output) + "detection" + type_data + ".png",
                         "--start", str(start_time),
                         "--end", str(last_update),
                         "--vertical-label=" + str(type_data) + " load",
                         '--lower-limit', '0',
                         '--upper-limit', max_value,
                         "--title=Carga del " + str(type_data) + " de la computadora \n Detección de umbrales",

                         "DEF:cargaCPU=" + str(database_dir) + ":" + str(type_data) + "Load:AVERAGE",
                         "DEF:maxCPU=" + str(database_dir) + ":" + str(type_data) + "Max:AVERAGE",
                         "AREA:cargaCPU#00FF00:Carga del CPU")


def verify_limits(type_data, max_value, actual_value, last_notification, ip_address):
    array = []
    actual_time = datetime.now()
    percentage = (float(actual_value) * float(actual_value)) / float(max_value)
    image_path = "data/devices_files/" + ip_address + "/detection" + type_data + ".png"

    if type_data == "CPU":
        array = cpu_limit
    elif type_data == "RAM":
        array = ram_limit
    elif type_data == "HDD":
        array = hdd_limit

    if array[0] <= percentage < array[1]:
        if int((actual_time - last_notification[0]).total_seconds() / 60) >= 5:
            send_alert_attached("Warning " + type_data, image_path, ip_address, type_data)
            last_notification[0] = actual_time
    elif array[1] <= percentage < array[2]:
        if int((actual_time - last_notification[1]).total_seconds() / 60) >= 5:
            send_alert_attached("Emergency " + type_data, image_path, ip_address, type_data)
            last_notification[1] = actual_time
    elif percentage >= array[2]:
        if int((actual_time - last_notification[2]).total_seconds() / 60) >= 5:
            send_alert_attached("Critical " + type_data, image_path, ip_address, type_data)
            last_notification[2] = actual_time

    return last_notification
