import os
import gestion_de_datos, movimientos, archivo

def main():
    # si no existe datos de acceso de usuarios registrados
    if not os.path.exists("usuarios.log"):
        with open("usuarios.log", "w"): pass

    # No hay usuarios
    if os.stat("usuarios.log").st_size == 0: 
        gestion_de_datos.nuevoUsuario()
        # seleccionamos manualmente el  ID
        with open("actual_id", "w") as f:
            with open("usuarios.log", "r") as ff:
                txt = ff.read()
                pos = txt.find("|", txt.find("|")+1)
                f.write(txt[pos-1:]) # serial id

    while True: 
        os.system("cls") # limpiar consola
        #opciones
        print("[1]-Archivo\n[2]-Movimientos\n[3]-Ayuda\n[4]-Salir")
        opcion = input(">>> ")
        
        if opcion == "4": # SALIR
            break 
        
        elif opcion == "3": # AYUDA
            os.system("cls")
            print("#"*28); print("Sistema de ventas \"Trinidad\""); print("#"*29)
            print("\n")
            print("#"*28); print("#Estudiante: | Diego Ascanio#"); print("#"*29)
            print("#"*28); print("#Cédula: | 31.354.306       #"); print("#"*29)
            print("#"*28); print("#Semestre I | Sección 05    #"); print("#"*29)
            
            input("Enter...")
            
        elif opcion == "2": # MOVIMIENTOS
            movimientos.inicio()
            
        elif opcion == "1": # ARCHIVO
            archivo.inicio()
        
        else:
            print("La opción que elegiste no existe")
            input("Enter...")




if __name__ == "__main__":
    main()