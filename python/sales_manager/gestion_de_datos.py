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
        f.write(f"{nombre}|{clave}|{id}")

    input("\nEnter.")
