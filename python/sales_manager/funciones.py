from os import system

# Variables de almacenamiento de datos
# movimientos/facturas
# estructura => {cliente, cedula, cant_arti, [[articulos][precios]], monto}
registro_movs = [] 
productos_en_inventario = [[],[]]
productos_para_venta = [[],[]]

def arcProductos():
    system("clear") 
    while True:
        print("[1]-Productos\n[2]-Agregar productos\n[3]-Eliminar productos\n[4]-Atrás")
        opcion = input(">>> ")

        if opcion == "1":
            print("PRODUCTOS EN VENTA\n")

            for i in

        elif opcion == "2":
            art_cant = input("¿Cuántos proudctos desea agregar? => ")
            while not art_cant.isdigit():
                art_cant = input("Valor inválido. Reingrese => ")

            for i in range(int(art_cant)):
                nombre = input("Nombre del producto => ")

                cant = input("Cantidad => ")
                while not cant.isdigit():
                    cant = input("Valor inválido. Reingrese => ")

                lugar = ""        
                while lugar != "1" or lugar != "2": 
                    lugar = input("[1]-En venta\n[2]-Inventario => ")

                    if lugar == "1":
                        productos_para_venta[0] = nombre 
                        productos_para_venta[1] = int(cant) 

                    elif lugar == "2":
                        productos_en_inventario[0] = nombre
                        productos_en_inventario[1] = int(cant)




        elif opcion == "3":
            pass

        elif opcion == "4":
            break

        else:
            input("Calor inválido.\nEnter...")



def archivo():
    system("clear")
    while True:
        print("[1]-Usuarios\n[2]-Clientes\n[3]-Productos\n[4]-Cambios de usuarios\n[5]-Cambio de claves\n[6]-Salir")
        opcion = input(">>> ")

        if opcion == "1": #USUARIOS
            pass

        elif opcion == "2": # CLIENTES
            pass

        elif opcion == "3": # PRODUCTOS
            arcProductos()

        elif opcion == "4": # CAMBIO-USER
            pass

        elif opcion == "5": # CAMBIO-CLAV
            pass

        elif opcion == "6": # SALIR
            break

        else:
            input("Opción inválida.\nEnter...")
# ------------------------------------------------------------------- #

def movimientos():
    global registro_movs

    while True:
        system("cls")
        print("[1]-Nueva factura\n[2]-Reporte de facturas\n[3]-Atrás")
        opcion = input(">>> ")
        if opcion == "3":
            break
        
        elif opcion == "2": # facturas
            system("cls")
            
            if len(registro_movs) != 0:
                print("#"*50)
                
                for i in range(len(registro_movs)):
                
                    print(f"Cédula: {registro_movs[i]['cedula']}")
                    print(f"Cliente: {registro_movs[i]['nombre']}")
                    print(f"Cantidad de articulos: {registro_movs[i]['cant_arti']}\n")
                    
                    print("Articulos:")

                    for j in range(registro_movs[i]['cant_arti']):
                        print(f"*{registro_movs[i]['articulos'][0][j]} - Bs.{registro_movs[i]['articulos'][1][j]}")
                      
                    print(f"\nMonto: Bs.{registro_movs[i]['monto']}")
                    print("#"*50, "\n")
                    
                input("\nEnter...")
                
            else:
                print("Vacío")
                input("\nEnter...")
            
        elif opcion == "1": # factura nueva
            system("cls")
            nombre = input("Inserte nombre del cliente => ")

            cedula = input("\nInserte un número de cédula válido => ")
            while not cedula.isdigit(): # letras
                cedula = input("Valor inválido. Reingrese => ")

            cant_arti = input("\n¿Cuántos articulos compró el cliente? => ")
            while not cant_arti.isdigit(): # letras
                cant_arti = input("Valor inválido. Reingrese => ")


            
            articulos_precio = [[],[]]
            monto = 0
            
            for i in range(int(cant_arti)):
                print(f"\nInserte artículo Nº{i+1}")
                art = input("=> ")

                while True:
                    try: 
                        pre = float(input("Precio => "))
                        break
                    except ValueError: 
                        print("Valor inválido")
                        continue

                articulos_precio[0].append(art)
                articulos_precio[1].append(pre)
                monto += pre
                
            # Guardamos los datos en el registro_movs

            registro_movs.append({
                "nombre": nombre,
                "cedula": cedula,
                "cant_arti": int(cant_arti),
                "articulos": articulos_precio,
                "monto": monto
            })
            input("\nEnter...")
            
        else:
            print("\nLa opción que elegiste no existe")
            input("Enter...")
    
def ayuda():
    system("cls")

    print("#"*29); print("Sistema de ventas \"Trinidad\""); print("#"*29)
    print("\n")
    
    print("#"*29); print("#Estudiante: | Diego Ascanio#"); print("#"*29)
    print("#"*29); print("#Cédula: | 31.354.306       #"); print("#"*29)
    print("#"*29); print("#Semestre I | Sección 05    #"); print("#"*29)
    
    input("Enter...")
