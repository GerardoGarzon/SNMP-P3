import rrdtool
import os


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


def update_database(ip_address, type_data, value, max_value):
    database_dir = os.getcwd() + "/data/devices_files/" + ip_address + "/" + type_data + ".rrd"
    rrdtool.update(database_dir, value)
    graph_detection(ip_address, type_data, max_value)


def graph_detection(ip_address, type_data, max_value):
    database_dir = os.getcwd() + "/data/devices_files/" + ip_address + "/" + type_data + ".rrd"
    image_output = os.getcwd() + "/data/devices_files/" + ip_address + "/"

    last_update = int(rrdtool.last(database_dir))
    start_time = last_update - 200

    ret = rrdtool.graphv(str(image_output) + "detection" + type_data + ".png",
                         "--start", str(start_time),
                         "--end", str(last_update),
                         "--vertical-label=" + str(type_data) + " load",
                         '--lower-limit', '0',
                         '--upper-limit', max_value,
                         "--title=Carga del " + str(type_data) + " de la computadora \n Detección de umbrales",

                         "DEF:cargaCPU=" + str(database_dir) + ":" + str(type_data) + "Load:AVERAGE",
                         "DEF:maxCPU=" + str(database_dir) + ":" + str(type_data) + "Max:AVERAGE",
                         "AREA:cargaCPU#00FF00:Carga del CPU",)
