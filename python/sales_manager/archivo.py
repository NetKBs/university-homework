import os 

def inicio():
    os.system("cls")

    while True:
        print("[1]-Usuarios\n[2]-Clientes\n[3]-Productos\n[4]-Cambios de usuarios\n[5]-Cambio de claves\n[6]-Salir")
        opcion = input(">>> ")

        if opcion == "1": #USUARIOS
            pass

        elif opcion == "2": # CLIENTES
            pass

        elif opcion == "3": # PRODUCTOS
            pass

        elif opcion == "4": # CAMBIO-USER
            pass

        elif opcion == "5": # CAMBIO-CLAV
            pass

        elif opcion == "6": # SALIR
            break

        else:
            input("Opción inválida.\nEnter...")