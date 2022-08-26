import os
import string
import random
import fileinput

def serial():
    """ Devuelve un serial id aleatorios de 32 carácteres  ASCII y números """
    return  ''.join([random.choice(string.ascii_letters
            + string.digits) for n in range(32)])

def nuevoUsuario():
    """ Crear nuevo usuario (nombre, clave, id aleatorio) """

    os.system("cls")
    print("CREAR NUEVO USUARIO\n")

    nombre = input("Nombre: ").strip()
    clave = input("Clave: ").strip()
    id = serial()

    with open("usuarios.log", "a") as f: # lo registramos
        f.write(f"{nombre}|{clave}|{id}")

    input("\nEnter...")

def mostrarUsuarios():
    """ Muestra una lista de los nombres de los usuaios registrados """

    os.system("cls")
    with open("usuarios.log", "r") as f: 
        for linea in f:
            print("*", linea[:linea.find("|")])

    input("\nEnter...")


def cambioClave():
    """ Cambia la contraseña del usuario actal basandose en su id/serial"""

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
        