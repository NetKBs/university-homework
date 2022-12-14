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
            # [nombre, cédula,productos totales, gastos totales]
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
            # [nombre, cédula,productos totales, gastos totales]
            datos = linea.split("|")

            if ci == datos[1]: # nos guiamos por su cédula
                print(f"{datos[0]}|{datos[1]}|{compras + int(datos[2])}|{gastos + float(datos[3])}")
                continue
            print(linea, end="")

        
def eliminarCliente():
    """ Eliminar un cliente registrado mediante su cédula """

    if os.stat(f"./datos/{obtenerNombre()}.cli").st_size == 0:
        print("\n"); print(50*"-")
        print(" !!!No hay clientes para eliminar!!!")
        input("Enter...")
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

# --------------------------------------------------------------------- #
# ----------------------- MANEJO DE PRODUCTOS ------------------------- #
# --------------------------------------------------------------------- #

def mostrarProductos():
    """ Muestra todos los productos registrados en el inventario """

    if not os.path.exists(f"./datos/{obtenerNombre()}.pro"):
        with open(f"./datos/{obtenerNombre()}.pro", "w"): pass

    os.system("cls")
    print(60*"-")
    print("\t INVENTARIO DE PRODUCTOS REGISTRADOS")
    print(60*"-"); print("\n")

    with open(f"./datos/{obtenerNombre()}.pro", "r") as f: 
        for linea in f:
            # [nombre, cantidad]
            datos = linea.split("|")
            print(f" - {datos[0]}\tUnidades: {datos[1]}")


def agregarProductos():
    """ 
    Agrega un nuevo producto y la cantidad de este. Si el producto ya existe solo 
    se sumará la cantidad
    """
    os.system("cls")
    print(50*"-")
    print("\tAGREGAR UN PRODUCTO")
    print(50*"-")

    producto = input("\n Nombre: ").strip()

    cantidad = input(" Cantidad: ").strip()
    while not cantidad.isdigit() or cantidad == "0": # no es un entero
        cantidad = input("\n Cantidad: ").strip()

    if not duplicado("producto", producto): # Producto nuevo
        with open(f"./datos/{obtenerNombre()}.pro", "a") as f:
            f.write(f"{producto}|{cantidad}")
            f.write("\n")

    else: # Ya existe el producto
        for linea in fileinput.input(f"./datos/{obtenerNombre()}.pro", inplace=True):
            # [nombre, cantidad]
            datos = linea.split("|")

            if producto.lower() == datos[0].lower():
                print(f"{datos[0]}|{int(datos[1]) + int(cantidad)}")
                continue

            print(linea, end='') 

    print("\n"); print(50*"-")
    print(" !!!Producto agregado con éxito!!!")
    input(" Enter...")
    print(50*"-")


def eliminarProductos():
    """
        Elimina cierta cantidad de un producto. Si se elimina más de lo que hay de cierto producto
        se considera fuera de stock, por lo tanto se elimina completamente.
     """
    mostrarProductos()

    print(50*"-")
    print("\t ELIMINAR PRODUCTO")
    print(50*"-")

    producto = input("\n Nombre: ").strip()
    cantidad = input(" Cantidad: ").strip()

    for linea in fileinput.input(f"./datos/{obtenerNombre()}.pro", inplace=True):
        # [nombre, cantidad]
        datos = linea.split("|")

        if producto.lower() == datos[0].lower(): # existe el producto
            cantidad_restante = int(datos[1]) - int(cantidad)

            if cantidad_restante <= 0: # se elimina del stock
                continue
            else:
                print(f"{datos[0]}|{cantidad_restante}")
                continue

        print(linea, end='') 

    print("\n"); print(50*"-")
    print(" !!!Operación exitosa!!!")
    input(" Enter..")
    print(50*"-")


# -------------------------------------------------------------------- #
# ----------------------- MANEJO DE FACTURAS ------------------------- #
# -------------------------------------------------------------------- #

def mostrarFacturas():
    """ Muestra un historial de todas las facturas efectuadas por el usuario """

    if not os.path.exists(f"./datos/{obtenerNombre()}.mov"):
        with open(f"./datos/{obtenerNombre()}.mov", "w"): pass

    os.system("cls")

    with open(f"./datos/{obtenerNombre()}.mov", "r") as f:
        for linea in f:
            print(linea)
   

def nuevaFactura():
    """ 
        Crea una nueva factura utilizando exclusivamente productos disponibles en el inventario
        y registrando los datos del cliente que efectuó la compra. Si el cliente ha hecho compras
        previas se actualizarán datos
    """
    
    if not os.path.exists(f"./datos/{obtenerNombre()}.pro"):
        with open(f"./datos/{obtenerNombre()}.pro", "w"): pass

    if os.stat(f"./datos/{obtenerNombre()}.pro").st_size == 0:
        print(50*"-")
        print(" !!!No se puede realizar una factura sin productos en el inventario!!!")
        input("\n Enter..")
        return 1

    if not os.path.exists(f"./datos/{obtenerNombre()}.mov"):
        with open(f"./datos/{obtenerNombre()}.mov", "w"): pass


    # diccionario para almacenar temporalmente los datos de la factura
    registro = {
        "cliente":"",
        "cedula":"" ,
        "productos": [],
        "precios": [],
        "cantidades": [],
        "monto": 0
    }

    os.system("cls")
    print(50*"-")
    print("\t NUEVA FACTURA")
    print(50*"-")

    cliente = input("\n Nombre del Cliente: ").strip()

    cedula = input(" Cédula: ").strip() 
    while not cedula.isdigit(): # no es un entero
        cedula = input("\n Cédula: ")

    # almacenamos temporales
    registro["cliente"] = cliente
    registro["cedula"] = cedula

    while True: # loop para el agrego de productos
        mostrarProductos()

        print(50*"-")
        print("\tElige un producto")
        print(50*"-")

        producto = input("\n Producto: ").strip()

        if not duplicado("producto", producto):
            print("\n"); print(50*"-")
            print(" !!!Ese producto no existe!!!")
            input(" Enter...")
            os.system("cls")
            continue

        cantidad = input(" Cantidad: ").strip()
        while not cantidad.isdigit():
            cantidad = input("\n Cantidad: ")


        for linea in fileinput.input(f"./datos/{obtenerNombre()}.pro", inplace=True):
            # [nombre, cantidad]
            datos = linea.split("|")

            # restamos lo vendido del producto en nuestro inventario
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
                precio = float(input(" Precio: "))
                break
            except ValueError: 
                continue
        
        # Registramos temporales
        registro["productos"].append(producto) 
        registro["precios"].append(precio)
        registro["cantidades"].append(cantidad)
        
        while True:
            print(60*"-")
            print("\n 1.Agregar otro arituclo\t\t2.Terminar factura")
            seguir = input(">>> ")

            if seguir == "1":
                os.system("cls")

                # Se desea agregar más artículos, pero en el invetario no hay más
                if os.stat(f"./datos/{obtenerNombre()}.mov").st_size == 0:
                    print(50*"-")
                    print(" !!!No más productos en el inventario!!!")
                    input("\n Enter")
                    continue
                else:
                    break

            elif seguir == "2":
                # cuantos productos en total se compraron
                cantidad_total = 0

                # Registramos la factura
                with open(f"./datos/{obtenerNombre()}.mov", "a") as f:
                    f.write(40*"-")
                    f.write(f"\n  {cliente}\t|\tC.I {cedula}\n")
                    f.write(40*"-"); f.write("\n")

                    for i in range(len(registro["productos"])):
                        # productos, cantidades y sus precios
                        f.write(f"{i+1}- {registro['productos'][i]}\t{registro['cantidades'][i]}u ")
                        f.write(f"\tBs{registro['precios'][i]}\n")

                        # calculamos el monto total de los productos y precios
                        registro["monto"] += registro["precios"][i] * int(registro["cantidades"][i])
                        # calculamos cantidad de productos totales comprados
                        cantidad_total += int(registro["cantidades"][i])

                    f.write(40*"-")
                    f.write(f"\n  Monto: Bs{registro['monto']}\n")
                    f.write(40*"-"); f.write("\n")
                    f.write(40*"#"); f.write("\n")


                # Registramos cliente
                agregarClientes(cliente, cedula, cantidad_total, registro["monto"])
                return 0 

            else:
                print(50*"-")
                print(" !!!Opción inválida!!!")
                input(" Enter...")

    

