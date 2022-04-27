import time
import re
from os.path import exists
from rrd_database import *
from snmp_requests import *
from datetime import datetime, date


# 1.3.6.1.2.1.25.2.3.1.2 -> hrStorageRam / 1.3.6.1.2.1.25.2.1.2
# 1.3.6.1.2.1.25.2.3.1.3 -> /
# 1.3.6.1.2.1.25.2.3.1.4 -> Unit
# 1.3.6.1.2.1.25.2.3.1.5 -> StorageSize
# 1.3.6.1.2.1.25.2.3.1.6 -> StorageUsed


def start_agent(host_name, ip_address, community, port):
    create_database(ip_address, "CPU")
    create_database(ip_address, "RAM")
    create_database(ip_address, "HDD")

    ram_id = find_ram_id(ip_address, community)
    ram_units = snmp_get(community, ip_address, '1.3.6.1.2.1.25.2.3.1.4.' + str(ram_id))
    hdd_id = find_hdd_id(ip_address, community)
    hdd_units = snmp_get(community, ip_address, '1.3.6.1.2.1.25.2.3.1.4.' + str(hdd_id))

    update_agent(ip_address, community, ram_id, ram_units, hdd_id, hdd_units)


def update_agent(ip_address, community, ram_id, ram_units, hdd_id, hdd_units):
    last_cpu_notification = [0, 0, 0]
    last_ram_notification = [0, 0, 0]
    last_hdd_notification = [0, 0, 0]

    while exists(os.getcwd() + "/data/devices_files/" + ip_address):
        value_cpu = get_cpu_value(community, ip_address)
        value_ram = get_memory_value(community, ip_address, ram_id, ram_units)
        value_hdd = get_memory_value(community, ip_address, hdd_id, hdd_units)

        update_database(ip_address, 'CPU', value_cpu, "100", last_cpu_notification)
        update_database(ip_address, 'RAM', "N:" + str(value_ram["usage_storage"]) + ":" + str(value_ram["total_storage"]), str(value_ram["total_storage"]), last_ram_notification)
        update_database(ip_address, 'HDD', "N:" + str(value_hdd["usage_storage"]) + ":" + str(value_hdd["total_storage"]), str(value_hdd["total_storage"]), last_hdd_notification)
        time.sleep(1)


def find_ram_id(ip_address, community):
    ram_id = 0
    hrStorageType = snmp_walk(community, ip_address, '1.3.6.1.2.1.25.2.3.1.2')
    for i in range(len(hrStorageType)):
        if hrStorageType[i].split(' = ')[1] == "1.3.6.1.2.1.25.2.1.2":
            oid_id = hrStorageType[i].split(' = ')[0].split('.')
            ram_id = oid_id[len(oid_id) - 1]
            break
    return str(ram_id)


def find_hdd_id(ip_address, community):
    hdd_id = 0
    hrStorageDesc = snmp_walk(community, ip_address, '1.3.6.1.2.1.25.2.3.1.3')
    for i in range(len(hrStorageDesc)):
        if hrStorageDesc[i].split(' = ')[1] == "/" or re.match(r'(C:).*', hrStorageDesc[i].split(' = ')[1]):
            oid_id = hrStorageDesc[i].split(' = ')[0].split('.')
            hdd_id = oid_id[len(oid_id) - 1]
            break
    return hdd_id


def get_cpu_value(community, ip_address):
    hrProcessorLoad = snmp_walk(community, ip_address, '1.3.6.1.2.1.25.3.3.1.2')
    value_processor = "N:" + str(hrProcessorLoad[0].split(' = ')[1]) + ":100"
    return value_processor


def get_memory_value(community, ip_address, mem_id, mem_units):
    hrStorageSize = int(snmp_get(community, ip_address, '1.3.6.1.2.1.25.2.3.1.5.' + str(mem_id)))
    hrStorageUsed = int(snmp_get(community, ip_address, '1.3.6.1.2.1.25.2.3.1.6.' + str(mem_id)))

    memory_value = {
        "total_storage": convert_bytes_gb(hrStorageSize * int(mem_units)),
        "usage_storage": convert_bytes_gb(hrStorageUsed * int(mem_units))
    }

    return memory_value


def convert_bytes_gb(bytes_to_convert):
    converted_bytes = float(bytes_to_convert)
    for i in range(3):
        converted_bytes = converted_bytes / 1024

    return converted_bytes


# a = datetime.now()
#
# time.sleep(60)
#
# b = datetime.now()
#
# print(str((b - a).total_seconds() / 60))
