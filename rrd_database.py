import rrdtool
import os


def create_database(ip_address, type_data):
    database_dir = os.getcwd() + "/data/devices_files/" + ip_address
    result = rrdtool.create(database_dir + "/" + type_data + ".rrd",
                            "--start", 'N',
                            "--step", '60',
                            "DS:" + type_data + "Load:GAUGE:60:U:U",
                            "RRA:AVERAGE:0.5:1:24")
    if result:
        print(rrdtool.error())


