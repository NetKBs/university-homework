import os
import string
import random
import fileinput

def serial():
    """ Devuelve un serial id aleatorios de 32 carácteres  ASCII y números """
    return  ''.join([random.choice(string.ascii_letters
            + string.digits) for n in range(32)])

def obtenerNombre():
    with open("actual_id", "r") as f:
        id = f.read()

    with open("usuarios.log", "r") as f:
        for linea in f:
            if id in linea:
                return linea[:linea.find("|")]

def usuarioDuplicado(nombre):
    with open("usuarios.log", "r") as f: 
        for linea in f: 
            if nombre in linea:
                return True

    return False

def productoDuplicado(producto):
    with open(f"./datos/{obtenerNombre()}.pro", "r") as f: 
        for linea in f: 
            if producto.lower() in linea.lower():
                return True

    return False

def clienteDuplicado(cliente):
    with open(f"./datos/{obtenerNombre()}.cli", "r") as f: 
        for linea in f:
            if cliente.lower() in linea.lower():
                return True
    
    return False


# ----------------------- MANEJO DE USUARIOS --------------------------#
def mostrarUsuarios():
    """ Muestra una lista de los nombres de los usuaios registrados """

    os.system("cls")
    with open("usuarios.log", "r") as f: 
        for linea in f:
            print("*", linea[:linea.find("|")])


def nuevoUsuario():
    """ Crear nuevo usuario (nombre, clave, id aleatorio) """

    os.system("cls")
    print("CREAR NUEVO USUARIO\n")

    nombre = input("Nombre: ").strip()
    while usuarioDuplicado(nombre):
        print("Ese usuario ya existe")    
        nombre = input("Nombre: ").strip()

    clave = input("Clave: ").strip()
    id = serial()

    with open("usuarios.log", "a") as f: # lo registramos
        f.write(f"{nombre}|{clave}|{id}")
        f.write("\n")

    with open("actual_id", "w") as f: # sesion id
            f.write(id)

    input("\nEnter...")

def eliminarUsuario():
    mostrarUsuarios()

    print("ELIMINAR USUARIO")
    nombre = input("Nombre: ")
    user_actual = obtenerNombre()

    if nombre == user_actual:
        print("No puedes eliminar la sesión actual")
        input("\nEnter...")

    else:
        for linea in fileinput.input("usuarios.log", inplace=True):
            previo = linea[:linea.find("|")]
            if previo == nombre:
                continue

            print(linea, end="")

        if os.path.exists(f"./datos/{nombre}.cli"):
            os.remove(f"./datos/{nombre}.cli")

        if os.path.exists(f"./datos/{nombre}.pro"):
            os.remove(f"./datos/{nombre}.pro")


def cambioUsuario():
    while True:
        os.system("cls")
        print("CAMBIAR DE USUARIO")

        nombre = input("Nombre: ")
        clave = input("Clave: ")
        id = ""

        with open("usuarios.log", "r") as f:
            for linea in f:
                datos = linea.replace("\n", "").split("|") # nombre,clave,id/serial
                if nombre == datos[0] and clave in datos[1]:
                    id = datos[2]
                    break
        
        if id == "":
            print("Las credenciales ingresadas no se encuentran registradas")
            input("\nEnter...")
            break

        with open("actual_id", "w") as f:
            f.write(id)

        print(f"\nSesión iniciada como {nombre}")
        input("\nEnter...")
        break

def cambioClave():
    """ Cambia la contraseña del usuario actual basandose en su id/serial"""

    os.system("cls")
    print("CAMBIAR CONTRASEÑA")
    nueva_clave = input("\nNueva clave: ")

    with open("actual_id", "r") as f:
        actual_id = f.read() # sesion

    # Remplazamos
    for linea in fileinput.input("usuarios.log", inplace=True):
        datos = linea.replace("\n", "").split("|") # nombre,clave,id/serial

        if actual_id in linea:
            print(f"{datos[0]}|{nueva_clave}|{datos[2]}")
            continue

        print(linea, end='') 

    input("\nEnter...")


# ----------------------- MANEJO DE CLIENTES --------------------------#
def mostrarClientes():
    os.system("cls")
    print("CLIENTES")

    if not os.path.exists(f"./datos/{obtenerNombre()}.cli"):
        with open(f"./datos/{obtenerNombre()}.cli", "w"): pass

    with open(f"./datos/{obtenerNombre()}.cli", "r") as f:
        for linea in f:
            datos = linea.split("|")
            print(f"* {datos[0]} {datos[1]} {datos[2]} {datos[3]}")

def agregarClientes(nombre, ci, compras, gastos):
    if not clienteDuplicado(nombre):
        with open(f"./datos/{obtenerNombre()}.cli", "a") as f:
            f.write(f"{nombre}|{ci}|{compras}|{gastos}")
            f.write("\n")

    else:
        for linea in fileinput.input(f"./datos/{obtenerNombre()}.cli", inplace=True):
            datos = linea.split("|")
            if ci == datos[1]: 
                print(f"* {datos[0]} {datos[1]} {compras + int(datos[2])} {gastos + float(datos[3])}")

        
def eliminarCliente():
    if os.stat(f"./datos/{obtenerNombre()}.cli").st_size == 0:
        input("No hay clientes para eliminar\nEnter...")
        return 1

    mostrarClientes()
    print("ELIMINAR CLIENTE")
    cedula = input("Cedula: ").strip()
    while not cedula.isdigit():
        cedula = input("Cedula: ").strip()

    for linea in fileinput.input(f"./datos/{obtenerNombre()}.cli", inplace=True):
        if cedula in linea: # eliminamos cliente
            continue
        print(linea, end='') 


# ----------------------- MANEJO DE PRODUCTOS --------------------------#
def mostrarProductos():
    os.system("cls")
    print("INVENTARIO DE PRODUCTOS REGISTRADOS")

    if not os.path.exists(f"./datos/{obtenerNombre()}.pro"):
        with open(f"./datos/{obtenerNombre()}.pro", "w"): pass

    with open(f"./datos/{obtenerNombre()}.pro", "r") as f: 
        for linea in f:
            datos = linea.split("|")
            print(f" *{datos[0]}\t{datos[1]}")


def agregarProductos():
    os.system("cls")
    print("AGREGAR UN PRODUCTO")

    producto = input("Nombre: ").strip()

    cantidad = input("Cantidad: ").strip()
    while not cantidad.isdigit() or cantidad == "0": # no es un entero
        cantidad = input("Valor inválido\nCantidad: ").strip()

    if not productoDuplicado(producto):
        with open(f"./datos/{obtenerNombre()}.pro", "a") as f:
            f.write(f"{producto}|{cantidad}")
            f.write("\n")

    else:
        for linea in fileinput.input(f"./datos/{obtenerNombre()}.pro", inplace=True):
            datos = linea.split()

            if datos[0].lower() in linea.lower():
                print(f"{datos[0]}|{int(datos[1]) + int(cantidad)}")
                continue

            print(linea, end='') 


def eliminarProductos():
    mostrarProductos()
    print("ELIMINAR PRODUCTO")
    producto = input("Nombre: ").strip()
    cantidad = input("Cantidad: ").strip()

    for linea in fileinput.input(f"./datos/{obtenerNombre()}.pro", inplace=True):
        datos = linea.split()
        if producto in linea: 
            cantidad_restante = int(datos[1]) - int(cantidad)

            if cantidad_restante <= 0:
                continue
            else:
                print(f"{datos[0]}|{cantidad_restante}")
                continue

        print(linea, end='') 


# ----------------------- MANEJO DE FACTURAS --------------------------#
def mostrarFacturas():
    os.system("cls")
    print("")

    if not os.path.exists(f"./datos/{obtenerNombre()}.mov"):
        with open(f"./datos/{obtenerNombre()}.mov", "w"): pass

    with open(f"./datos/{obtenerNombre()}.mov", "r") as f:
        for linea in f:
            print(linea)
   

def nuevaFactura():
    os.system("cls")


    if not os.path.exists(f"./datos/{obtenerNombre()}.pro"):
        with open(f"./datos/{obtenerNombre()}.pro", "w"): pass

    if os.stat(f"./datos/{obtenerNombre()}.pro").st_size == 0:
        print("No se puede realizar una factura sin productos en el inventario")
        input("\nEnter..")
        return 1

    if not os.path.exists(f"./datos/{obtenerNombre()}.mov"):
        with open(f"./datos/{obtenerNombre()}.mov", "w"): pass

    # donde se guardarán los previos
    registro = {
        "cliente":"",
        "cedula":"" ,
        "productos": [],
        "precios": [],
        "cantidades": [],
        "monto": 0
    }

    print("NUEVA FACTURA")

    cliente = input("Nombre del Cliente: ").strip()

    cedula = input("Cédula: ").strip() 
    while not cedula.isdigit(): # no es un entero
        cedula = input("Valor inválido\nCédula: ")

    registro["cliente"] = cliente
    registro["cedula"] = cedula
    mostrarProductos()

    while True:
        producto = input("\nElegir Producto: ").strip()

        if not productoDuplicado(producto):
            input("Ese producto no existe\nEnter...")
            os.system("cls")
            mostrarProductos()
            continue

        cantidad = input("Cantidad: ").strip()
        while not cantidad.isdigit():
            cantidad = input("Valor inválido\nCantidad: ")


        for linea in fileinput.input(f"./datos/{obtenerNombre()}.pro", inplace=True):
            datos = linea.split("|")
            if producto.lower() == datos[0].lower(): 
                cantidad_restante = int(datos[1]) - int(cantidad)
                # si es negativo, entonces la cantidad a eliminar será
                # la cantidad de ese producto disponible
                if cantidad_restante <= 0:
                    cantidad = datos[1]
                    continue
                else:
                    print(f"{datos[0]}|{cantidad_restante}")
                    continue
                
            print(linea, end='') 

        while True:
            try: 
                precio = float(input("Precio: "))
                break
            except ValueError: 
                print("Valor inválido")
                continue
        
        registro["productos"].append(producto) 
        registro["precios"].append(precio)
        registro["cantidades"].append(cantidad)
        
        while True:
            print("\n1.Agregar otro arituclo\t2.Terminar factura")
            seguir = input(">>> ")

            if seguir == "1":
                os.system("cls")
                if os.stat(f"./datos/{obtenerNombre()}.mov").st_size == 0:
                    input("No hay más productos en el inventario\nEnter...")
                    continue
                else:
                    mostrarProductos()
                    break

            elif seguir == "2":
                # cuantos productos en total se compraron
                cantidad_total = 0

                # Guardamos la factura
                with open(f"./datos/{obtenerNombre()}.mov", "a") as f:
                    f.write(40*"-")
                    f.write(f"\n  {cliente}\t|\tC.I {cedula}\n")
                    f.write(40*"-")
                    f.write("\n")

                    for i in range(len(registro["productos"])):
                        # imprimimos los productos, cantidades y sus precios
                        f.write(f"{i+1}- {registro['productos'][i]}\t{registro['cantidades'][i]}u ")
                        f.write(f"\tBs{registro['precios'][i]}\n")

                        # calculamos el monto total de los productos y precios
                        registro["monto"] += registro["precios"][i] * int(registro["cantidades"][i])
                        # calculamos cantidad de productos totales comprados
                        cantidad_total += int(registro["cantidades"][i])

                    f.write(40*"-")
                    f.write(f"\n  Monto: Bs{registro['monto']}\n")
                    f.write(40*"-")
                    f.write("\n")
                    f.write(40*"#")
                    f.write("\n")

                # Registramos cliente
                agregarClientes(cliente, cedula, cantidad_total, registro["monto"])

                return 0 
            else:
                input("\nOpción inválida")

    

