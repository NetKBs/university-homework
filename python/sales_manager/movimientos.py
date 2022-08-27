import os
import gestion_de_datos

def inicio():
    while True:
        os.system("cls")
        print("[1]-Nueva factura\n[2]-Reporte de facturas\n[3]-Atrás")
        opcion = input(">>> ")

        if opcion == "1":
            gestion_de_datos.nuevaFactura()
        elif opcion == "2":
            gestion_de_datos.mostrarFacturas()
        elif opcion == "3":
            break
        else:
            input("Opción inválida\nEnter...")