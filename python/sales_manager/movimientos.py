import os
import gestion_de_datos

def inicio():
    while True:
        os.system("cls")
        print(40*"-"); print("\tMenú Movimientos"); print(40*"-")
        print(f" Usuario actual: {gestion_de_datos.obtenerNombre()}\n")
        print(40*"-")

        print("\n[1]- Nueva factura\n[2]- Reporte de facturas\n[3]- Atrás")
        opcion = input(">>> ")

        if opcion == "1":
            gestion_de_datos.nuevaFactura()

        elif opcion == "2":
            while True:
                gestion_de_datos.mostrarFacturas()
                print("1.Atrás")
                opcion = input(">>> ")

                if opcion == "1":
                    break
                else:
                    print(40*"-")
                    print(" !!!Opción inválida!!!")
                    input(" Enter...")
                    
        elif opcion == "3":
            break
        else:
            print(40*"-")
            print(" !!!Opción inválida!!!")
            input(" Enter...")