import os 
import gestion_de_datos

def inicio():

    while True:
        os.system("cls")
        print(40*"-"); print("\tMenú Archivo"); print(40*"-")
        print(f" Usuario actual: {gestion_de_datos.obtenerNombre()}\n")
        print(40*"-")

        print("\n[1]- Usuarios\n[2]- Clientes\n[3]- Productos\n[4]- Cambio de usuario\n[5]- Cambio de claves\n[6]- Atrás")
        opcion = input("\n >>> ")

        if opcion == "1": #USUARIOS
            while True:
                gestion_de_datos.mostrarUsuarios()

                print("\n"); print(50*"-")
                print(" 1.Atrás\t2.Nuevo\t\t3.Eliminar")
                opcion = input(" >>> ")

                if opcion == "1":
                    break
                elif opcion == "2":
                    gestion_de_datos.nuevoUsuario()
                elif opcion == "3":
                    gestion_de_datos.eliminarUsuario()
                else:
                    print("\n");print(40*"-")
                    print(" !!!Opción inválida!!!")
                    input(" Enter...")
            

        elif opcion == "2": # CLIENTES
            while True:
                gestion_de_datos.mostrarClientes()

                print("\n"); print(50*"-")
                print("\n 1.Atrás\t\t2.Eliminar")
                opcion = input(" >>> ")

                if opcion == "1":
                    break
                elif opcion == "2":
                    gestion_de_datos.eliminarCliente()
                else: 
                    print("\n");print(50*"-")
                    print(" !!!Opción inválida!!!")
                    input(" Enter...")


        elif opcion == "3": # PRODUCTOS
            while True:
                gestion_de_datos.mostrarProductos()
            
                print("\n1.Atrás\t2.Nuevo\t3.Eliminar")
                opcion = input(">>> ")

                if opcion == "1":
                    break
                elif opcion == "2":
                    gestion_de_datos.agregarProductos()
                elif opcion == "3":
                    gestion_de_datos.eliminarProductos()
                else: 
                    input("Opción inválida\nEnter...")


        elif opcion == "4": # CAMBIO-USER
            gestion_de_datos.cambioUsuario()

        elif opcion == "5": # CAMBIO-CLAV
            gestion_de_datos.cambioClave()

        elif opcion == "6": # SALIR
            break

        else:
            print(40*"-")
            print(" !!!Opción inválida!!!")
            input(" Enter...")