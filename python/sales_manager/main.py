import os
import gestion_de_datos, movimientos, archivo

def main():
    # crear carpeta de datos de usuario si no existe
    if not os.path.exists("./datos"):
        os.mkdir("datos")
        
    # creaar registro de usuarios si no existe
    if not os.path.exists("usuarios.log"):
        with open("usuarios.log", "w"): pass

    # si el registro de usuarios está vacío forzamos un registro
    if os.stat("usuarios.log").st_size == 0: 
        gestion_de_datos.nuevoUsuario()

        # iniciamos manualmente la sesion con el  ID
        with open("usuarios.log", "r") as f:
            txt = f.read()
            pos = txt.find("|", txt.find("|")+1) # posición del id
            id = txt[pos+1:] # serial id

        # establacemos id
        with open("actual_id", "w") as f: 
            f.write(id)

    while True: 
        os.system("cls") # limpiar consola
        print("-"*50); print("\tSistema de ventas \"Trinidad\""); print("-"*50)

        print(f" Usuario actual: {gestion_de_datos.obtenerNombre()}\n")
        print(50*"-")

        print("\n[1]- Archivo\n[2]- Movimientos\n[3]- Ayuda\n[4]- Salir")
        opcion = input("\n >>> ")
        
        if opcion == "4": # SALIR
            break 
        
        elif opcion == "3": # AYUDA
            os.system("cls")
            print("-"*50); print("\tSistema de ventas \"Trinidad\""); print("-"*50)
            print("\n")
            print(" Estudiante: | Diego Ascanio"); print("-"*50)
            print("\n Cédula: | 31.354.306       "); print("-"*50)
            print("\n Semestre I | Sección 05    "); print("-"*50)
            
            input("\n Enter...")
            
        elif opcion == "2": # MOVIMIENTOS
            movimientos.inicio()
            
        elif opcion == "1": # ARCHIVO
            archivo.inicio()
        
        else:
            print(50*"-")
            print(" !!!Opción inválida!!!")
            input(" Enter...")




if __name__ == "__main__":
    main()