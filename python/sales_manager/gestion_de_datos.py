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

def obtenerNombre(id):
    with open("usuarios.log", "r") as f:
        for line in f:
            if id in line:
                return line[:line.find("|")]

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

    with open("actual_id", "w") as f: # sesion id
            f.write(id)

    input("\nEnter...")

def mostrarUsuarios():
    """ Muestra una lista de los nombres de los usuaios registrados """

    os.system("cls")
    with open("usuarios.log", "r") as f: 
        for linea in f:
            print("*", linea[:linea.find("|")])


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
            continue

        with open("actual_id", "w") as f:
            f.write(id)

        print(f"\nSesión iniciada como {nombre}")
        input("\nEnter...")
        break



        