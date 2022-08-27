import os
import string
import random
import fileinput

def serial():
    """ Devuelve un serial id aleatorios de 32 carácteres  ASCII y números """
    return  ''.join([random.choice(string.ascii_letters
            + string.digits) for n in range(32)])

def usuarioDuplicado(nombre):
    with open("usuarios.log", "r") as f: 
        for linea in f: 
            if nombre in linea:
                return True

    return False

def obtenerNombre():
    with open("actual_id", "r") as f:
        id = f.read()

    with open("usuarios.log", "r") as f:
        for line in f:
            if id in line:
                return line[:line.find("|")]

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
            for line in f:
                datos = line.replace("\n", "").split("|") # nombre,clave,id/serial
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
    for line in fileinput.input("usuarios.log", inplace=True):
        datos = line.replace("\n", "").split("|") # nombre,clave,id/serial

        if actual_id in line:
            print(f"{datos[0]}|{nueva_clave}|{datos[2]}")
            continue

        print(line, end='') 

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

    for line in fileinput.input(f"./datos/{obtenerNombre()}.cli", inplace=True):
        if cliente in line: # eliminamos cliente
            continue
        print(line, end='') 