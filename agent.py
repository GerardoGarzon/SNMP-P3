import time
from os.path import exists
from rrd_database import *

oid_processorLoad = "1.3.6.1.2.1.25.3.3.1.2."
oid_ramUsage = "hrStorageRam"
oid_hddUsage = ""

# 1.3.6.1.2.1.25.2.3.1.2 -> hrStorageRam / 1.3.6.1.2.1.25.2.1.2
# 1.3.6.1.2.1.25.2.3.1.3 -> /
# 1.3.6.1.2.1.25.2.3.1.4 -> Unit
# 1.3.6.1.2.1.25.2.3.1.5 -> StorageSize
# 1.3.6.1.2.1.25.2.3.1.5 -> StorageUsed


def start_agent(host_name, ip_address, community, port):
    create_database(ip_address, "CPU")
    create_database(ip_address, "RAM")
    create_database(ip_address, "HDD")

    while exists(os.getcwd() + "/data/devices_files/" + ip_address):
        print(ip_address)
        time.sleep(3)

def get_processorId():
    pass

def get_hddId():
    pass
