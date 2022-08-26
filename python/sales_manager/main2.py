from os import system
from funciones2 import *



# bucle infinito del menu principal
while True: 
    system("cls") # limpiar consola
    #opciones
    print("[1]-Archivo\n[2]-Movimientos\n[3]-Ayuda\n[4]-Salir")
    opcion = input(">>> ")
    
    if opcion == "4": # SALIR
        break 
    
    elif opcion == "3": # AYUDA
        ayuda()
        
    elif opcion == "2": # MOVIMIENTOS
        movimientos()
        
    elif opcion == "1": # ARCHIVO
        archivo()
    
    else:
        print("La opción que elegiste no existe")
        input("Enter...")