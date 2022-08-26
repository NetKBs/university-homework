import os 
import gestion_de_datos

def inicio():

    while True:
        os.system("cls")
        print("[1]-Usuarios\n[2]-Clientes\n[3]-Productos\n[4]-Cambio de usuario\n[5]-Cambio de claves\n[6]-Atrás")
        opcion = input(">>> ")

        if opcion == "1": #USUARIOS
            while True:
                gestion_de_datos.mostrarUsuarios()
                print("\n1.Atrás\t2.Nuevo")
                opcion = input(">>> ")

                if opcion == "1":
                    break
                elif opcion == "2":
                    gestion_de_datos.nuevoUsuario()
                else:
                    input("Opción inválida\nEnter...")
                    
            

        elif opcion == "2": # CLIENTES
            while True:
                gestion_de_datos.mostrarClientes()
                print("\n1.Atrás\t2.Nuevo\t3.Eliminar")
                opcion = input(">>> ")

                if opcion == "1":
                    break
                elif opcion == "2":
                    gestion_de_datos.agregarClientes()
                elif opcion == "3":
                    gestion_de_datos.eliminarCliente()
                else: 
                    input("Opción inválida\nEnter...")

        elif opcion == "3": # PRODUCTOS
            pass

        elif opcion == "4": # CAMBIO-USER
            gestion_de_datos.cambioUsuario()

        elif opcion == "5": # CAMBIO-CLAV
            gestion_de_datos.cambioClave()

        elif opcion == "6": # SALIR
            break

        else:
            input("Opción inválida.\nEnter...")