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
            print("*", linea)

def agregarClientes():
    os.system("cls")
    print("AGREGAR NUEVO CLIENTE")

    cliente = input("Nombre: ").strip()
    with open(f"./datos/{obtenerNombre()}.cli", "a") as f:
        f.write(cliente+"\n")
        
def eliminarCliente():
    mostrarClientes()
    print("ELIMINAR CLIENTE")
    cliente = input("Nombre: ").strip()

    for linea in fileinput.input(f"./datos/{obtenerNombre()}.cli", inplace=True):
        if cliente in linea: # eliminamos cliente
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
            datos = linea.split()
            print(f"{datos[0]}\t{datos[1]}")


def agregarProductos():
    os.system("cls")
    print("AGREGAR UN PRODUCTO")

    producto = input("Nombre: ").strip()

    cantidad = input("Cantidad: "). strip()
    while not cantidad.isdigit() or cantidad == "0": # no es un entero
        print("Valor inválido.")
        cantidad = input("Cantidad: "). strip()

    if not productoDuplicado(producto):
        with open(f"./datos/{obtenerNombre()}.pro", "a") as f:
            f.write(f"{producto} {cantidad}")
            f.write("\n")

    else:
        for linea in fileinput.input(f"./datos/{obtenerNombre()}.pro", inplace=True):
            datos = linea.split()

            if datos[0].lower() in linea.lower():
                print(f"{datos[0]} {int(datos[1]) + int(cantidad)}")
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
                print(f"{datos[0]} {cantidad_restante}")
                continue

        print(linea, end='') 


# ----------------------- MANEJO DE FACTURAS --------------------------#
def mostrarFacturas():
    os.system("cls")
    print("FACTURAS")

    if not os.path.exists(f"./datos/{obtenerNombre()}.mov"):
        with open(f"./datos/{obtenerNombre()}.mov", "w"): pass
   

def nuevaFactura():
    os.system("cls")
    print("NUEVA FACTURA")
    
    if not os.path.exists(f"./datos/{obtenerNombre()}.mov"):
        with open(f"./datos/{obtenerNombre()}.mov", "w"): pass

