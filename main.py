from devices import Devices
import os


def main():
    devices = Devices()

    while True:
        os.system('clear')
        selection = 0

        while selection < 1 or selection > 4:
            print("Monitoreo de rendimiento utilizando SNMP \n"
                  "\t1.- Listar dispositivos.\n"
                  "\t2.- Agregar dispositivo.\n"
                  "\t3.- Eliminar dispositivo.\n"
                  "\t4.- Salir.\n")
            selection = int(input("Ingrese la opción seleccionada: "))

        if selection == 1:
            devices.list_devices()
        elif selection == 2:
            devices.add_devices()
        elif selection == 3:
            devices.list_devices()
            devices.delete_devices()
        elif selection == 5:
            break

        input()


if __name__ == '__main__':
    main()
