import os
import gestion_de_datos, movimientos, archivo

def main():
    # creaar registro de usuarios si no existe
    if not os.path.exists("usuarios.log"):
        with open("usuarios.log", "w"): pass

    # si el registro de usuarios está vacío
    # fuerza un registro
    if os.stat("usuarios.log").st_size == 0: 
        gestion_de_datos.nuevoUsuario()
        # iniciamos manualmente la sesion con el  ID
        with open("usuarios.log", "r") as f:
            txt = f.read()
            pos = txt.find("|", txt.find("|")+1)
            id = txt[pos+1:] # serial id

        # establacemos id
        with open("actual_id", "w") as f: 
            f.write(id)

    while True: 
        os.system("cls") # limpiar consola
        print(f"Sesión de {gestion_de_datos.obtenerNombre()}\n")

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