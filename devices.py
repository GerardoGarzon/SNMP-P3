from termcolor import colored, cprint
from snmp_requests import *
from database import DataBase
from agent import *
import os
import threading


def print_colored(description, text, color, args):
    print('\t', description, ': ', end='')
    cprint(text, color, attrs=args)


class Devices:

    def __init__(self):
        self.devices_database = DataBase()

    def list_devices(self):
        devices_status = {}
        devices = self.devices_database.read()
        if devices == {}:
            cprint('No hay dispositivos agregados', 'yellow', attrs=['bold'])
        else:
            for device in devices:
                response = snmp_get(devices[device]['community'], devices[device]['ip_address'], '1.3.6.1.2.1.1.1.0')
                devices_status[device] = response

            counter = 0

            for device in devices:
                print("_______________________________________________________________")
                print(str(counter) + ".-")
                counter += 1
                print_colored('Dispositivo', devices[device]['host_name'], 'green', ['bold'])
                print_colored('Dirección IP', devices[device]['ip_address'], 'green', ['bold'])
                if devices_status[device] is not None:
                    print_colored('Estado', 'UP', 'green', ['bold'])
                    num_procesadores = snmp_walk(devices[device]['community'], devices[device]['ip_address'],
                                                 '1.3.6.1.2.1.25.3.3.1.1')
                    print_colored('No. procesadores', len(num_procesadores), 'green', ['bold'])
                else:
                    print_colored('Estado', 'DOWN', 'red', ['bold'])
                    print_colored('No. interfaces', 'Desconocido', 'red', ['bold'])

    def add_devices(self):
        print()
        host_name = input('Ingresa el nombre del dispositivo: ')
        ip_address = input('Ingresa la dirección ip del dispositivo: ')
        snmp_version = input('Ingresa la version de SNMP configurada en el dispositivo: ')
        community = input('Ingresa la comunidad configurada en el dispositivo: ')
        port = input('Ingresa el puerto configurado en el dispositivo (161 default): ' or '161')

        os.system('mkdir data/devices_files/' + ip_address)

        self.devices_database.insert(host_name, ip_address, snmp_version, community, port)

        new_agent = threading.Thread(target=start_agent, args=(host_name, ip_address, community, port))
        new_agent.start()

        print(colored('\nDispositivo agregado exitosamente.', 'green'))

    def delete_devices(self):
        ip_address = input('Ingresa la dirección ip del dispositivo que deseas eliminar: ')
        self.devices_database.delete(ip_address)
        os.system('rm -r data/devices_files/' + ip_address)
        print(colored('\nDispositivo eliminado exitosamente.', 'green'))

# CPU usage:
# RAM usage:
# HDD usage:
