import os
import string
import random
import fileinput

def serial():
    """ Devuelve un serial id aleatorios de 32 carácteres  ASCII y números """

    return  ''.join([random.choice(string.ascii_letters
            + string.digits) for n in range(32)])

def obtenerNombre():
    """  Devuelve el nombre de usuario de la cuenta actual usando el serial de referencia """

    with open("actual_id", "r") as f:
        id = f.read() # serial

    with open("usuarios.log", "r") as f:
        for linea in f:
            if id in linea:
                return linea[:linea.find("|")]

def duplicado(objetivo, dato):
    """"
        Devuelve si existe un duplicado de cierto dato en un archivo
        Recibe el parámetro objetivo que especifica que queremos comprar, este acepta 'usuario, producto o cliente'
        el segundo parámetro dato, será el que se verificará si tiene un duplicado 
    """

    if objetivo == "usuario":
        ruta = "usuarios.log" 
    elif objetivo == "producto":
        ruta = f"./datos/{obtenerNombre()}.pro" 
    elif objetivo == "cliente":
        ruta = f"./datos/{obtenerNombre()}.cli"

    with open(ruta, "r") as f:
        for linea in f:
            if dato.lower() in linea.lower(): # ignoramos mayus/minus
                return True
    return False

# ---------------------------------------------------------------------#
# ----------------------- MANEJO DE USUARIOS --------------------------#
# ---------------------------------------------------------------------#

def mostrarUsuarios():
    """ Muestra una lista de los nombres de los usuaios registrados """

    os.system("cls")
    print(50*"-")
    print("\tLISTA DE USUARIOS REGISTRADOS")
    print(50*"-")

    with open("usuarios.log", "r") as f: 
        for num, linea in enumerate(f):
            print(f" {num+1}- ", linea[:linea.find("|")])


def nuevoUsuario():
    """ Crear nuevo usuario (nombre, clave, id aleatorio) """

    os.system("cls")
    print(40*"-")
    print("\tCREAR NUEVO USUARIO\n")
    print(40*"-")

    nombre = input("\n Nombre: ").strip()

    # evitamos duplicados
    while duplicado("usuario", nombre): 
        print("\n !!!Ese usuario ya existe!!!")    
        nombre = input(" Nombre: ").strip()

    clave = input("\n Clave: ").strip()
    id = serial()

    # lo registramos
    with open("usuarios.log", "a") as f: 
        f.write(f"{nombre}|{clave}|{id}")
        f.write("\n")

    # establecemos el id/serial
    with open("actual_id", "w") as f: 
            f.write(id)

    print("\n"); print(40*"-")
    print(" !!!Usuario creado con éxito!!!")
    input(" Enter...")

def eliminarUsuario():
    """ Elimina un usuario usando el nombre del mismo """

    mostrarUsuarios()
    print(40*"-")
    print("\tELIMINAR USUARIO")
    print(40*"-")

    nombre = input("\n Nombre: ")
    user_actual = obtenerNombre()

    if nombre.lower() == user_actual.lower():
        print("\n"); print(40*"-")
        print(" !!!No puedes eliminar la sesión actual!!!")
        input(" Enter...")

    else:
        for linea in fileinput.input("usuarios.log", inplace=True):
            nombre_en_archivo = linea[:linea.find("|")]
            if nombre_en_archivo.lower() == nombre.lower(): # eliminamos
                continue

            print(linea, end="") # mantenemos lineas

        # Removemos archivos de datos del usuario eliminado
        if os.path.exists(f"./datos/{nombre}.cli"):
            os.remove(f"./datos/{nombre}.cli")

        if os.path.exists(f"./datos/{nombre}.pro"):
            os.remove(f"./datos/{nombre}.pro")
            
        if os.path.exists(f"./datos/{nombre}.mov"):
            os.remove(f"./datos/{nombre}.mov")


def cambioUsuario():
    """ Cambiar de cuenta usando usuario y contraseña para obtener el id/serial """
    while True:
        os.system("cls")
        mostrarUsuarios()

        print(40*"-")
        print("\tCAMBIAR DE USUARIO")
        print(40*"-")

        nombre = input("\n Nombre: ")
        clave = input("\n Clave: ")
        id = ""

        with open("usuarios.log", "r") as f:
            for linea in f:
                # [nombre,clave,id/serial]
                datos = linea.split("|") 
                if nombre.lower() == datos[0].lower() and clave == datos[1]:
                    id = datos[2]
                    break
        
        if id == "":
            print("\n"); print(60*"-")
            print(" !!!Las credenciales ingresadas no se encuentran registradas!!!")
            input("Enter...")
            break

        # Establecemos serial
        with open("actual_id", "w") as f:
            f.write(id)

        print("\n"); print(50*"-")
        print(f" !!!Sesión iniciada como {nombre}!!!")
        input(" Enter...")
        break

def cambioClave():
    """ Cambia la contraseña del usuario actual basandose en su id/serial """

    os.system("cls")
    print(40*"-")
    print("\tCAMBIAR CONTRASEÑA")
    print(40*"-")
    print(f"\tUsuario actual: {obtenerNombre()}")

    nueva_clave = input("\n Nueva clave: ")

    # Id sesión actual
    with open("actual_id", "r") as f:
        actual_id = f.read() 

    # Remplazamos
    for linea in fileinput.input("usuarios.log", inplace=True):
        # [nombre,clave,id/serial]
        datos = linea.split("|")

        if actual_id in linea:
            print(f"{datos[0]}|{nueva_clave}|{datos[2]}")
            continue

        print(linea, end='') 

    print("\n"); print(50*"-")
    print(" !!!Contraseña cambiada con éxito!!!")
    input("Enter...")

# -------------------------------------------------------------------- #
# ----------------------- MANEJO DE CLIENTES ------------------------- #
# -------------------------------------------------------------------- #

def mostrarClientes():
    """ Muestra la liste de clientes registrados luego de haber realizado una factura """
    # existe o no el archivo de clientes para este usuario
    if not os.path.exists(f"./datos/{obtenerNombre()}.cli"):
        with open(f"./datos/{obtenerNombre()}.cli", "w"): pass

    os.system("cls")
    print(50*"-")
    print("\t\t CLIENTES")
    print(50*"-"); print("\n")

    with open(f"./datos/{obtenerNombre()}.cli", "r") as f:
        # genera conteo desde la primera linea desde 0
        for num, linea in enumerate(f): 
            datos = linea.split("|")
            print(f"{num+1}- {datos[0]} C.I {datos[1]} Tot.Comprado: {datos[2]} Tot.Gastado: Bs{datos[3]}")

def agregarClientes(nombre, ci, compras, gastos):
    """
        Agrega un cliente nuevo desde los datos de una factura. Si el cliente existe se
        actualizarán sus datos. Recibe nombre, cédula, cantidad de compras y total de gastos
     """
    
    # cliente no registrado
    if not duplicado("cliente", nombre):
        with open(f"./datos/{obtenerNombre()}.cli", "a") as f:
            f.write(f"{nombre}|{ci}|{compras}|{gastos}")
            f.write("\n")

    else:
        for linea in fileinput.input(f"./datos/{obtenerNombre()}.cli", inplace=True):
            datos = linea.split("|")
            if ci == datos[1]: # nos guiamos por su cédula
                print(f"{datos[0]}|{datos[1]}|{compras + int(datos[2])}|{gastos + float(datos[3])}")

        
def eliminarCliente():
    """ Eliminar un cliente registrado mediante su cédula """

    if os.stat(f"./datos/{obtenerNombre()}.cli").st_size == 0:
        input("No hay clientes para eliminar\nEnter...")
        return 1

    mostrarClientes()
    print(50*"-")
    print("\tELIMINAR CLIENTE")
    print(50*"-")

    cedula = input("\n Cedula: ").strip()
    while not cedula.isdigit(): # no es un número entero
        cedula = input("Cedula: ").strip()

    for linea in fileinput.input(f"./datos/{obtenerNombre()}.cli", inplace=True):
        if cedula in linea: 
            continue # eliminamos cliente

        print(linea, end='') 

    print("\n"); print(50*"-")
    print(" !!!Cliente eliminado con éxito!!!")
    input("Enter...")

# ----------------------- MANEJO DE PRODUCTOS --------------------------#
def mostrarProductos():
    os.system("cls")
    print("INVENTARIO DE PRODUCTOS REGISTRADOS")

    if not os.path.exists(f"./datos/{obtenerNombre()}.pro"):
        with open(f"./datos/{obtenerNombre()}.pro", "w"): pass

    with open(f"./datos/{obtenerNombre()}.pro", "r") as f: 
        for linea in f:
            datos = linea.split("|")
            print(f" *{datos[0]}\t{datos[1]}")


def agregarProductos():
    os.system("cls")
    print("AGREGAR UN PRODUCTO")

    producto = input("Nombre: ").strip()

    cantidad = input("Cantidad: ").strip()
    while not cantidad.isdigit() or cantidad == "0": # no es un entero
        cantidad = input("Valor inválido\nCantidad: ").strip()

    if not duplicado("producto", producto):
        with open(f"./datos/{obtenerNombre()}.pro", "a") as f:
            f.write(f"{producto}|{cantidad}")
            f.write("\n")

    else:
        for linea in fileinput.input(f"./datos/{obtenerNombre()}.pro", inplace=True):
            datos = linea.split()

            if datos[0].lower() in linea.lower():
                print(f"{datos[0]}|{int(datos[1]) + int(cantidad)}")
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
                print(f"{datos[0]}|{cantidad_restante}")
                continue

        print(linea, end='') 


# ----------------------- MANEJO DE FACTURAS --------------------------#
def mostrarFacturas():
    os.system("cls")
    print("")

    if not os.path.exists(f"./datos/{obtenerNombre()}.mov"):
        with open(f"./datos/{obtenerNombre()}.mov", "w"): pass

    with open(f"./datos/{obtenerNombre()}.mov", "r") as f:
        for linea in f:
            print(linea)
   

def nuevaFactura():
    os.system("cls")


    if not os.path.exists(f"./datos/{obtenerNombre()}.pro"):
        with open(f"./datos/{obtenerNombre()}.pro", "w"): pass

    if os.stat(f"./datos/{obtenerNombre()}.pro").st_size == 0:
        print("No se puede realizar una factura sin productos en el inventario")
        input("\nEnter..")
        return 1

    if not os.path.exists(f"./datos/{obtenerNombre()}.mov"):
        with open(f"./datos/{obtenerNombre()}.mov", "w"): pass

    # donde se guardarán los previos
    registro = {
        "cliente":"",
        "cedula":"" ,
        "productos": [],
        "precios": [],
        "cantidades": [],
        "monto": 0
    }

    print("NUEVA FACTURA")

    cliente = input("Nombre del Cliente: ").strip()

    cedula = input("Cédula: ").strip() 
    while not cedula.isdigit(): # no es un entero
        cedula = input("Valor inválido\nCédula: ")

    registro["cliente"] = cliente
    registro["cedula"] = cedula
    mostrarProductos()

    while True:
        producto = input("\nElegir Producto: ").strip()

        if not duplicado("producto", producto):
            input("Ese producto no existe\nEnter...")
            os.system("cls")
            mostrarProductos()
            continue

        cantidad = input("Cantidad: ").strip()
        while not cantidad.isdigit():
            cantidad = input("Valor inválido\nCantidad: ")


        for linea in fileinput.input(f"./datos/{obtenerNombre()}.pro", inplace=True):
            datos = linea.split("|")
            if producto.lower() == datos[0].lower(): 
                cantidad_restante = int(datos[1]) - int(cantidad)
                # si es negativo, entonces la cantidad a eliminar será
                # la cantidad de ese producto disponible
                if cantidad_restante <= 0:
                    cantidad = datos[1]
                    continue
                else:
                    print(f"{datos[0]}|{cantidad_restante}")
                    continue
                
            print(linea, end='') 

        while True:
            try: 
                precio = float(input("Precio: "))
                break
            except ValueError: 
                print("Valor inválido")
                continue
        
        registro["productos"].append(producto) 
        registro["precios"].append(precio)
        registro["cantidades"].append(cantidad)
        
        while True:
            print("\n1.Agregar otro arituclo\t2.Terminar factura")
            seguir = input(">>> ")

            if seguir == "1":
                os.system("cls")
                if os.stat(f"./datos/{obtenerNombre()}.mov").st_size == 0:
                    input("No hay más productos en el inventario\nEnter...")
                    continue
                else:
                    mostrarProductos()
                    break

            elif seguir == "2":
                # cuantos productos en total se compraron
                cantidad_total = 0

                # Guardamos la factura
                with open(f"./datos/{obtenerNombre()}.mov", "a") as f:
                    f.write(40*"-")
                    f.write(f"\n  {cliente}\t|\tC.I {cedula}\n")
                    f.write(40*"-")
                    f.write("\n")

                    for i in range(len(registro["productos"])):
                        # imprimimos los productos, cantidades y sus precios
                        f.write(f"{i+1}- {registro['productos'][i]}\t{registro['cantidades'][i]}u ")
                        f.write(f"\tBs{registro['precios'][i]}\n")

                        # calculamos el monto total de los productos y precios
                        registro["monto"] += registro["precios"][i] * int(registro["cantidades"][i])
                        # calculamos cantidad de productos totales comprados
                        cantidad_total += int(registro["cantidades"][i])

                    f.write(40*"-")
                    f.write(f"\n  Monto: Bs{registro['monto']}\n")
                    f.write(40*"-")
                    f.write("\n")
                    f.write(40*"#")
                    f.write("\n")

                # Registramos cliente
                agregarClientes(cliente, cedula, cantidad_total, registro["monto"])

                return 0 
            else:
                input("\nOpción inválida")

    

