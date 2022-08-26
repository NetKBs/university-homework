import os
import string
import random

def serial():
    # 32 carácteres
    return  ''.join([random.choice(string.ascii_letters
            + string.digits) for n in range(32)])

def nuevoUsuario():
    os.system("cls")
    print("CREAR NUEVO USUARIO\n")

    print("Nombre: ", end="")
    nombre = input()
    print("Contraseña: ", end="")
    clave = input()
    id = serial()

    with open("usuarios.log", "a") as f:
        f.write(f"{nombre.strip()}|{clave.strip()}|{id}")

    input("\nEnter...")

def mostrarUsuarios():
    os.system("cls")
    with open("usuarios.log", "r") as f: 
        for linea in f:
            print("*", linea[:linea.find("|")])

    input("\nEnter...")