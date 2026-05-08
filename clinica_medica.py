import os
import matplotlib.pyplot as plt
from fpdf import FPDF

# ---------- VARIABLES GLOBALES ----------
hora_de_apertura = 0      # hora de apertura de la clinica en formato hhmm
hora_de_cierre   = 0      # hora de cierre de la clinica en formato hhmm
duracion_en_minutos = 0   # duracion de cada cita en minutos (15, 20 o 30)

# (id, nombre, apellido1, apellido2, telefono, residencia, correo, hora_apertura, hora_cierre)
lista_medicos = []         # lista de tuplas con los datos de cada medico registrado

# (id, nombre, apellido1, apellido2, telefono, residencia, correo)
lista_pacientes = []       # lista de tuplas con los datos de cada paciente registrado

# [id_medico, [(hora_hhmm, valor), ...]]  valor: 0=libre, -1=deshabilitado, >0=id_paciente
citas = []                 # lista de citas del dia por medico
# ---------- FIN VARIABLES GLOBALES ----------

# ---------- DATOS DE PRUEBA ----------
# Estos datos estan aqui para facilitar las pruebas del sistema.
# Se pueden eliminar antes de la entrega final si se desea empezar en blanco.
hora_de_apertura = 800
hora_de_cierre   = 1700
duracion_en_minutos = 30

lista_medicos = [
    (101, "Carlos",  "Mora",    "Solano", 88887777, "San Jose", "cmora@clinica.com",  800, 1700),
    (102, "Ana",     "Vega",    "Rojas",  77776666, "Heredia",  "avega@clinica.com",  900, 1600),
    (103, "Roberto", "Campos",  "Nunez",  66669999, "Alajuela", "rcampos@clinica.com",800, 1200),
]

lista_pacientes = [
    (201, "Luis",   "Castro", "Jimenez", 66665555, "Alajuela", "lcastro@gmail.com"),
    (202, "Maria",  "Arias",  "Lopez",   55554444, "Cartago",  "marias@gmail.com"),
    (203, "Pedro",  "Gomez",  "Bravo",   44443333, "Limon",    "pgomez@gmail.com"),
]

citas = [
    [101, [
        (800, 0),    (830, 201),  (900, 201),  (930, 0),
        (1000, 202), (1030, 0),   (1100, 202), (1130, -1),
        (1200, 0),   (1230, 203), (1300, 0),   (1330, -1),
        (1400, 0),   (1430, 0),   (1500, 203), (1530, 0),
        (1600, 0),   (1630, 0),
    ]],
    [102, [
        (900, 201),  (930, 0),    (1000, 202), (1030, -1),
        (1100, 0),   (1130, 203), (1200, 0),   (1230, 0),
        (1300, 202), (1330, 0),   (1400, 0),   (1430, -1),
        (1500, 0),   (1530, 0),
    ]],
    [103, [
        (800, 201),  (830, 0),    (900, 203),  (930, -1),
        (1000, 0),   (1030, 202), (1100, 0),   (1130, 0),
    ]],
]
# ---------- FIN DATOS DE PRUEBA ----------

def menu():
    # Muestra el menu principal con todas las opciones del sistema
    # No necesita nada antes de ejecutarse, es la primera funcion que corre
    # Segun el numero que ingrese el usuario llama a la funcion correspondiente
    # Si el usuario escribe 0 el programa termina
    while True:
        print ("                  CLINICA MEDICA                ")
        print ("1. Configuracion")
        print ("2. Registrar medicos")
        print ("3. Registrar pacientes")
        print ("4. Crear lista de citas del dia")
        print ("5. Pedir citas")
        print ("6. Informes")
        print ("7. Ayuda")
        print ("8. Acerca de")
        print ("0. Salir")
        # try/except atrapa el error si el usuario escribe texto en lugar de un numero
        try:
            opcion = int (input("Ingrese una opcion: "))
        except ValueError:
            print("Debe ingresar unicamente valores numericos")
            opcion = -1


        match opcion:
            case 1:
                configuracion()
            case 2:
                registrar_medicos()
            case 3:
                registrar_pacientes()
            case 4:
                crear_lista_de_citas_dia()
            case 5:
                pedir_citas()
            case 6:
                informes()
            case 7:
                ayuda()
            case 8:
                acerca_de()
            case 0:
                break
            case _:
                print ("Opcion invalida") 




def configuracion():
    # Permite cambiar el horario de apertura, cierre y la duracion de cada cita
    # No requiere datos previos para ejecutarse
    # Si hay medicos registrados verifica que sus horarios queden dentro del nuevo horario de la clinica
    # Si algun medico queda fuera del rango la operacion se cancela y se muestra cuales medicos son el problema
    # Si se acepta borra la lista de citas existente y guarda la nueva configuracion
    global hora_de_apertura,hora_de_cierre,duracion_en_minutos,citas,lista_medicos

    print ("        CLINICA MEDICA      ")
    print ("        CONFIGURACION       ")
    print ("Horario de la clinica")

    # loop independiente para apertura: solo repite apertura si hay error
    while True:
        apertura = input("Hora de apertura(hhmm):").upper()
        if apertura == "C":
            return
        try:
            apertura = int(apertura)
        except ValueError:
            print("Debe ingresar unicamente valores numericos")
            continue
        hh = apertura // 100
        mm = apertura % 100
        if hh < 0 or hh > 23 or mm < 0 or mm > 59:
            print("Hora invalida, formato debe ser hhmm")
            continue
        break  # apertura valida, sale de este loop

    # loop independiente para cierre: solo repite cierre si hay error
    while True:
        try:
            cierre = int(input("Hora de cierre(hhmm):"))
        except ValueError:
            print("Debe ingresar unicamente valores numericos")
            continue
        hh = cierre // 100
        mm = cierre % 100
        if hh < 0 or hh > 23 or mm < 0 or mm > 59:
            print("Hora invalida, formato debe ser hhmm")
            continue
        if cierre <= apertura:
            print("Error: la hora de cierre debe ser mayor a la hora de apertura")
            continue
        break  # cierre valido, sale de este loop

    # loop independiente para duracion: solo repite duracion si hay error
    while True:
        try:
            duracion = int(input("Duracion en minutos de cada cita(15,20,30):"))
        except ValueError:
            print("Debe ingresar unicamente valores numericos")
            continue
        if duracion not in (15, 20, 30):
            print("Error: la duracion debe estar entre (15,20,30)")
            continue
        break  # duracion valida, sale de este loop

    
    # loop que repite hasta que el usuario ingrese A o C correctamente
    while True:
        opcion = str(input("OPCION C-CANCELAR A-ACEPTAR")).upper() # .upper() convierte la entrada a mayuscula para aceptar c o C
        if opcion == "A":
            confirmacion = input("AL ACEPTAR ESTA CONFIGURACION BORRA LA LISTA DE CITAS QUE SE TENGA ACTUALMENTE. CONFIRMA LA ACEPTACION (SI/NO)").upper()
            if confirmacion == "SI":
                medicos_fuera_rango = []
                for medico in lista_medicos:
                    if medico[7] < apertura or medico[8] > cierre:
                        medicos_fuera_rango.append(medico)
                if medicos_fuera_rango:
                    print("NO SE PUEDE ACEPTAR ESTA OPERACION PORQUE LOS SIGUIENTES MEDICOS TIENEN HORARIOS FUERA DEL HORARIO DE LA CLINICA:")
                    for m in medicos_fuera_rango:
                        print(f"{m[0]} {m[1]} {m[2]} {m[3]}")
                else:
                    citas.clear() # borra la lista de citas existente antes de aplicar la nueva configuracion
                    hora_de_apertura = apertura
                    hora_de_cierre = cierre
                    duracion_en_minutos = duracion
            break  # sale del loop tanto si confirmo SI como si confirmo NO
        elif opcion == "C":
            break  # usuario cancelo, sale sin guardar
        else:
            print("Opcion invalida, ingrese A para aceptar o C para cancelar.") 




def registrar_medicos():
    # Muestra el submenu para gestionar medicos: agregar, consultar, modificar o eliminar
    # No requiere nada antes de ejecutarse
    # Dependiendo de la opcion elegida llama a la funcion correspondiente
    print ("         CLINICA MEDICA       ")
    print ("         REGISTRAR MEDICOS   ")

    while True:
        print("1. Agregar medicos")
        print("2. Consultar medicos")
        print("3. Modificar medicos")
        print("4. Eliminar medicos")
        print("0. Salir")
        try:
            opcion = int (input("OPCION"))
        except ValueError:
            print ("El dato a ingresar debe ser un numero.")
            opcion = -1
        match opcion:
            case 1:
                agregar_medico()
            case 2:
                consultar_medico()
            case 3:
                modificar_medico()
            case 4:
                eliminar_medico()
            case 0:
                break
            case _:
                print("Opcion invalida")

            
def agregar_medico():
    # Agrega un nuevo medico a la lista del sistema
    # Antes de usarla debe estar configurado el horario de la clinica (hora de apertura y cierre)
    # Pide todos los datos del medico uno por uno y los valida
    # Verifica que el ID no este siendo usado por otro medico ni por un paciente
    # El horario del medico debe estar dentro del horario de la clinica
    # Al final muestra un resumen y pide confirmacion antes de guardar
    global lista_medicos,lista_pacientes,hora_de_apertura,hora_de_cierre
    while True:
        dato = input("Ingrese el numero de identificacion (C para cancelar): ").upper()
        if dato == "C":
            return 
        try:
            id_medico = int(dato) 
        except ValueError:
            print("El id del medico debe ser un entero")
            continue
        if  id_medico < 1 or id_medico >  999999999:
            print("El numero de id debe estar entre 1 y 999999999")
            continue
        encontrado = False
        for medico in lista_medicos:
            if medico[0] == id_medico:
                encontrado = True
                print("EL MEDICO YA ESTA REGISTRADO, NO SE PUEDE AGREGAR")
                break
        if not encontrado:
            for paciente in lista_pacientes:
                if paciente[0] == id_medico:
                    encontrado = True
                    print("ESE ID YA PERTENECE A UN PACIENTE.")
                    break
        if not encontrado:
            break  

    while True :
        nombre = input("Nombre: ")
        if   2 <= len(nombre) <= 20:
            break 
        else:
            print("El nombre debe tener entre 2 y 20 caracteres.")
            continue 
    
    while True :
        apellido1 = input("Primer apellido: ")
        if   2 <= len(apellido1) <= 20:
            break 
        else:
            print("El apellido debe tener entre 2 y 20 caracteres.")
            continue 

    while True :
        apellido2 = input("Segundo apellido: ")
        if   2 <= len(apellido2) <= 20:
            break 
        else:
            print("El apellido debe tener entre 2 y 20 caracteres.")
            continue  

    while True:
        try:
            numero_telefono = int(input("Ingrese el numero telefonico: "))
        except ValueError:
            print("El numero debe estar unicamente formado por enteros.")
            continue  # evita el doble mensaje al saltar directamente al siguiente intento
        if len(str(numero_telefono)) == 8:
            break
        else:
            print("El numero de telefono debe tener 8 digitos exactos. ")

    while True:
        lugar_residencia = input("Ingrese el lugar de residencia: ")
        if 5 <= len(lugar_residencia) <= 50:
            break
        else:
            print("El lugar de residencia debe estar entre 5 y 50 caracteres. ")
            continue

    while True:
        correo_electronico = input("Ingrese el correo electronico: ")
        if "@" in correo_electronico and "." in correo_electronico:
            break
        else:
            print("Correo invalido. Debe contener '@' y '.'  Ejemplo: nombre@dominio.com")
            continue
    while True:
        try:
            hora_apertura = int(input("Ingrese la hora de apertura (hhmm): "))
        except ValueError: 
            print("La hora deben ser numeros enteros.")
            continue 
        hh = hora_apertura // 100
        mm = hora_apertura % 100
        if hh < 0 or hh > 23 or mm < 0 or mm > 59:
            print("Hora invalida, formato debe ser hhmm")
            continue
        if hora_apertura >= hora_de_apertura:
            break 
        else:
            print("La hora de apertura del medico debe ser mayor o igual a la hora de apertura de la clinica")
            continue
        
    while True:
        try:
            hora_cierre = int(input("Ingrese la hora de cierre: ")) 
        except ValueError:
            print ("La hora deben ser numeros enteros.")
            continue 
        hh = hora_cierre // 100
        mm = hora_cierre % 100
        if hh < 0 or hh > 23 or mm < 0 or mm > 59:
            print("Hora invalida, formato debe ser hhmm")
            continue
        if hora_cierre <= hora_de_cierre and hora_cierre > hora_apertura:
            break
        else:
            print("La hora de cierre del medico debe ser menor o igual a la hora de cierre de la clinica.")
            continue

    medicos = (id_medico,nombre,apellido1,apellido2,numero_telefono,lugar_residencia,correo_electronico,hora_apertura,hora_cierre)
    print ("    REGISTRAR MEDICOS   ")
    print ("    AGREGAR MEDICOS     ")
    print("Identificacion del medico: ",id_medico)
    print("Nombre: ",nombre)
    print("Apellido 1: ",apellido1)
    print("Apellido 2: ",apellido2)
    print("Telefono: ",numero_telefono)
    print("Lugar de residencia: ",lugar_residencia)
    print("Correo electronico: ",correo_electronico)
    print("Hora de apertura: ",hora_apertura)
    print("Hora de cierre: ",hora_cierre)
    while True:  # repite hasta que el usuario ingrese A o C correctamente
        opcion_final = input("OPCION C-CANCELAR A-ACEPTAR").upper()
        if opcion_final == "A":
            lista_medicos.append(medicos)
            break
        elif opcion_final == "C":
            return
        else:
            print("Opcion invalida, ingrese A para aceptar o C para cancelar.")


def consultar_medico():
    # Busca un medico por su ID y muestra todos sus datos en pantalla
    # Necesita que haya al menos un medico registrado en lista_medicos
    # Si el ID no existe avisa y vuelve a preguntar
    global lista_medicos

    print ("    REGISTRAR MEDICOS   ")
    print ("    CONSULTAR MEDICOS    ") 
    while True:
        dato = input("Identificacion del medico (C para cancelar): ").upper()
        if dato == "C":
            return
        try:
            id_medico = int(dato)
        except ValueError:
            print("La identificacion debe ser un dato numerico.")
            continue
        encontrado = False 
        for medico in lista_medicos:
            if medico[0] == id_medico:
               encontrado = True
               print("Identificacion del medico: ",medico[0])
               print("Nombre: ",medico[1])
               print("Apellido 1: ",medico[2])
               print("Apellido 2: ",medico[3])
               print("Telefono: ",medico[4])
               print("Lugar de residencia: ",medico[5])
               print("Correo electronico: ",medico[6])
               print("Hora de apertura: ",medico[7])
               print("Hora de cierre: ",medico[8])
               break 

        if not encontrado:
            print ("EL MEDICO NO ESTA REGISTRADO, NO SE PUEDE CONSULTAR")
            continue
        else:
            input("OPCION A-ACEPTAR ")

def modificar_medico():
    # Permite cambiar los datos de un medico ya registrado
    # Necesita que el medico exista en lista_medicos
    # Si hay citas activas no deja cambiar el horario del medico
    # Cada campo se puede dejar igual presionando Enter sin escribir nada
    # Pide confirmacion antes de guardar los cambios
    global lista_medicos,citas
    print ("    REGISTRAR MEDICOS   ")
    print ("    MODIFICAR MEDICOS    ")
    while True:
        dato = input("Identificacion del medico (C para cancelar): ").upper()
        if dato == "C":
            return
        try:
            id_medico = int(dato)
        except ValueError:
            print("La identificacion debe ser un dato numerico.")
            continue 
        encontrado = False
        for medico in lista_medicos:
            if medico[0] == id_medico:
                encontrado = True  
                print(f"Nombre: {medico[1]}")
                while True:
                    nuevo_nombre = input("    MODIFICAR: ")
                    if nuevo_nombre == "":
                        nuevo_nombre = medico[1]
                        break
                    elif 2 <= len(nuevo_nombre) <= 20:
                        break
                    else:
                        print("El nombre debe tener entre 2 y 20 caracteres.")

                print(f"Apellido 1: {medico[2]}")
                while True:
                    nuevo_apellido1 = input("    MODIFICAR: ")
                    if nuevo_apellido1 == "":
                        nuevo_apellido1 = medico[2]
                        break
                    elif 2 <= len(nuevo_apellido1) <= 20:
                        break
                    else:
                        print("El apellido debe tener entre 2 y 20 caracteres.")

                print(f"Apellido 2: {medico[3]}")
                while True:
                    nuevo_apellido2 = input("    MODIFICAR: ")
                    if nuevo_apellido2 == "":
                        nuevo_apellido2 = medico[3]
                        break
                    elif 2 <= len(nuevo_apellido2) <= 20:
                        break
                    else:
                        print("El apellido debe tener entre 2 y 20 caracteres.")

                print(f"Telefono: {medico[4]}")
                while True:
                    telefono = input("    MODIFICAR: ")
                    if telefono == "":
                        telefono = medico[4]
                        break
                    else:
                        try:
                            telefono = int(telefono)
                            if len(str(telefono)) == 8:
                                break
                            else:
                                print("El telefono debe tener 8 digitos exactos.")
                        except ValueError:
                            print("El telefono debe ser numerico.")

                print(f"Lugar de residencia: {medico[5]}")
                while True:
                    residencia = input("    MODIFICAR: ")
                    if residencia == "":
                        residencia = medico[5]
                        break
                    elif 5 <= len(residencia) <= 50:
                        break
                    else:
                        print("El lugar de residencia debe tener entre 5 y 50 caracteres.")

                print(f"Correo electronico: {medico[6]}")
                while True:
                    correo_electronico = input("    MODIFICAR: ")
                    if correo_electronico == "":
                        correo_electronico = medico[6]
                        break
                    elif "@" in correo_electronico and "." in correo_electronico:
                        break
                    else:
                        print("Correo invalido. Debe contener '@' y '.'  Ejemplo: nombre@dominio.com")
                if citas:
                    print(f"Hora de apertura {medico[7]} (no modificable, hay citas activas)")
                    hora_apertura = medico[7] 
                else:
                    print(f"Hora de apertura {medico[7]}")
                    hora_apertura = input("    MODIFICAR: ")
                    if hora_apertura == "":
                        hora_apertura = medico[7]
                    else:
                        try:
                            hora_apertura = int(hora_apertura)
                            hh = hora_apertura // 100
                            mm = hora_apertura % 100
                            if hh < 0 or hh > 23 or mm < 0 or mm > 59:
                                print("Hora invalida, formato debe ser hhmm")
                                hora_apertura = medico[7]
                        except ValueError:
                            print("La hora debe ser numerica.")
                            hora_apertura = medico[7]
                if citas:
                    print(f"Hora de cierre {medico[8]} (no modificable, hay citas activas)")
                    hora_cierre = medico[8] 
                else:
                    print(f"Hora de cierre {medico[8]}")
                    hora_cierre = input("    MODIFICAR: ")
                    if hora_cierre == "":
                        hora_cierre = medico[8]
                    else:
                        try:
                            hora_cierre = int(hora_cierre)
                            hh = hora_cierre // 100
                            mm = hora_cierre % 100
                            if hh < 0 or hh > 23 or mm < 0 or mm > 59:
                                print("Hora invalida, formato debe ser hhmm")
                                hora_cierre = medico[8]
                        except ValueError:
                            print("La hora debe ser numerica.")
                            hora_cierre = medico[8]
                while True:  # repite hasta que el usuario ingrese A o C correctamente
                    opcion_mod = input("OPCION C-CANCELAR A-ACEPTAR ").upper()
                    if opcion_mod == "A":
                        nueva_tupla = (id_medico,nuevo_nombre,nuevo_apellido1,nuevo_apellido2,telefono,residencia,correo_electronico,hora_apertura,hora_cierre)
                        indice = lista_medicos.index(medico)
                        lista_medicos[indice] = nueva_tupla
                        break
                    elif opcion_mod == "C":
                        break
                    else:
                        print("Opcion invalida, ingrese A para aceptar o C para cancelar.")
        if not encontrado:
            print ("EL MEDICO NO ESTA REGISTRADO, NO SE PUEDE MODIFICAR")
            continue
        

def eliminar_medico():
    # Elimina un medico de la lista del sistema
    # Necesita que el medico exista en lista_medicos
    # Si el medico tiene citas con pacientes asignados no se puede eliminar
    # Pide confirmacion doble antes de borrar
    global lista_medicos, citas
    print("    REGISTRAR MEDICOS   ")
    print("    ELIMINAR MEDICOS    ")
    while True:
        dato = input("Identificacion del medico (C para cancelar): ").upper()
        if dato == "C":
            return
        try:
            id_medico = int(dato)
        except ValueError:
            print("La identificacion debe ser un dato numerico.")
            continue 
        encontrado  = False 
        for medico in lista_medicos:
            if medico[0] == id_medico:
                encontrado = True
                print("Identificacion del medico: ",medico[0])
                print("Nombre: ",medico[1])
                print("Apellido 1: ",medico[2])
                print("Apellido 2: ",medico[3])
                print("Telefono: ",medico[4])
                print("Lugar de residencia: ",medico[5])
                print("Correo electronico: ",medico[6])
                print("Hora de apertura: ",medico[7])
                print("Hora de cierre: ",medico[8])
                
                opcion = input("OPCION C-CANCELAR A-ACEPTAR ").upper()
                if opcion == "A":
                    opcion2 = input("CONFIRMA LA ELIMINACION (SI/NO)").upper()
                    if opcion2 == "SI":
                        tiene_cita = False
                        for cita in citas:  # recorre todas las citas buscando las del medico
                            if cita[0] == id_medico:
                                for horario in cita[1]:
                                    if horario[1] > 0:  # valor > 0 significa paciente asignado
                                        tiene_cita = True
                                        break
                        if tiene_cita:  # la verificacion va FUERA del for, no dentro
                            print("ESTE MEDICO TIENE CITAS ASOCIADAS, NO SE PUEDE ELIMINAR.")
                        else:
                            lista_medicos.remove(medico)  # solo elimina si no tiene citas activas
                    if opcion2 == "NO":
                        pass 
                    
                if opcion == "C":
                    pass
                break                        
        
        if not encontrado:
            print("EL MEDICO NO ESTA REGISTRADO, NO SE PUEDE ELIMINAR" )
            continue
    
def registrar_pacientes():
    # Muestra el submenu para gestionar pacientes: agregar, consultar, modificar o eliminar
    # No requiere nada antes de ejecutarse
    # Dependiendo de la opcion elegida llama a la funcion correspondiente
    print ("         CLINICA MEDICA       ")
    print ("       REGISTRAR PACIENTES   ")

    while True:
        print("1. Agregar pacientes")
        print("2. Consultar pacientes")
        print("3. Modificar pacientes")
        print("4. Eliminar pacientes")
        print("0. Fin")
        try:
            opcion = int (input("OPCION"))
        except ValueError:
            print ("El dato a ingresar debe ser un numero.")
            opcion = -1
        match opcion:
            case 1:
                agregar_paciente()
            case 2:
                consultar_paciente()
            case 3:
                modificar_paciente()
            case 4:
                eliminar_paciente()
            case 0:
                break
            case _:
                print("Opcion invalida")
                continue



def agregar_paciente():
    # Agrega un nuevo paciente a la lista del sistema
    # No requiere configuracion previa para ejecutarse
    # Pide todos los datos del paciente y los valida uno por uno
    # Verifica que el ID no este siendo usado por otro paciente ni por un medico
    # Al final muestra un resumen y pide confirmacion antes de guardar
    global lista_pacientes
    while True:
        dato = input("Ingrese el numero de identificacion (C para cancelar): ").upper()
        if dato == "C":
            return 
        try:
            id_paciente = int(dato) 
        except ValueError:
            print("El id del paciente debe ser un entero")
            continue
        if  id_paciente < 1 or id_paciente >  999999999:
            print("El numero de id debe estar entre 1 y 999999999")
            continue
        encontrado = False
        for paciente in lista_pacientes:   
            if paciente[0] == id_paciente:
                encontrado = True 
                print("EL PACIENTE YA ESTA REGISTRADO, NO SE PUEDE AGREGAR")
                break
        if not encontrado:
            for medico in lista_medicos:   # verifica que el ID no pertenezca a un medico
                if medico[0] == id_paciente:
                    encontrado = True
                    print("ESE ID YA PERTENECE A UN MEDICO.")
                    break
        if not encontrado:
            break 
    

    while True :
        nombre = input("Nombre: ")
        if   2 <= len(nombre) <= 20:
            break 
        else:
            print("El nombre debe tener entre 2 y 20 caracteres.")
            continue 
    
    while True :
        apellido1 = input("Primer apellido: ")
        if   2 <= len(apellido1) <= 20:
            break 
        else:
            print("El apellido debe tener entre 2 y 20 caracteres.")
            continue 

    while True :
        apellido2 = input("Segundo apellido: ")
        if   2 <= len(apellido2) <= 20:
            break 
        else:
            print("El apellido debe tener entre 2 y 20 caracteres.")
            continue  

    while True:
        try:
            numero_telefono = int(input("Ingrese el numero telefonico: "))
        except ValueError:
            print("El numero debe estar unicamente formado por enteros.")
            continue  # evita el doble mensaje al saltar directamente al siguiente intento
        if len(str(numero_telefono)) == 8:
            break
        else:
            print("El numero de telefono debe tener 8 digitos exactos. ")

    while True:
        lugar_residencia = input("Ingrese el lugar de residencia: ")
        if 5 <= len(lugar_residencia) <= 50:
            break
        else:
            print("El lugar de residencia debe estar entre 5 y 50 caracteres. ")
            continue

    while True:
        correo_electronico = input("Ingrese el correo electronico: ")
        if "@" in correo_electronico and "." in correo_electronico:
            break
        else:
            print("Correo invalido. Debe contener '@' y '.'  Ejemplo: nombre@dominio.com")
            continue

    pacientes = (id_paciente,nombre,apellido1,apellido2,numero_telefono,lugar_residencia,correo_electronico)
    print ("    REGISTRAR PACIENTES   ")
    print ("    AGREGAR PACIENTE     ")
    print("Identificacion del paciente: ",id_paciente)
    print("Nombre: ",nombre)
    print("Apellido 1: ",apellido1)
    print("Apellido 2: ",apellido2)
    print("Telefono: ",numero_telefono)
    print("Lugar de residencia: ",lugar_residencia)
    print("Correo electronico: ",correo_electronico)
    while True:  # repite hasta que el usuario ingrese A o C correctamente
        opcion_final = input("OPCION C-CANCELAR A-ACEPTAR").upper()
        if opcion_final == "A":
            lista_pacientes.append(pacientes)
            break
        elif opcion_final == "C":
            return
        else:
            print("Opcion invalida, ingrese A para aceptar o C para cancelar.")

def consultar_paciente():
    # Busca un paciente por su ID y muestra todos sus datos en pantalla
    # Necesita que haya al menos un paciente registrado en lista_pacientes
    # Si el ID no existe avisa y vuelve a preguntar
    global lista_pacientes

    print ("    REGISTRAR PACIENTES   ")
    print ("    CONSULTAR PACIENTE    ") 
    while True:
        dato = input("Identificacion del paciente (C para cancelar): ").upper()
        if dato == "C":
            return
        try:
            id_paciente = int(dato)
        except ValueError:
            print("La identificacion debe ser un dato numerico.")
            continue
        encontrado = False 
        for paciente in lista_pacientes:
            if paciente[0] == id_paciente:
               encontrado = True
               print("Identificacion del paciente: ",paciente[0])
               print("Nombre: ",paciente[1])
               print("Apellido 1: ",paciente[2])
               print("Apellido 2: ",paciente[3])
               print("Telefono: ",paciente[4])
               print("Lugar de residencia: ",paciente[5])
               print("Correo electronico: ",paciente[6])
               break 

        if not encontrado:
            print ("EL PACIENTE NO ESTA REGISTRADO, NO SE PUEDE CONSULTAR")
            continue
        else:
            input("OPCION A-ACEPTAR ")


def modificar_paciente():
    # Permite cambiar los datos de un paciente ya registrado
    # Necesita que el paciente exista en lista_pacientes
    # Cada campo se puede dejar igual presionando Enter sin escribir nada
    # Pide confirmacion antes de guardar los cambios
    global lista_pacientes
    print ("    REGISTRAR PACIENTES   ")
    print ("    MODIFICAR PACIENTES    ")
    while True:
        dato = input("Identificacion del paciente (C para cancelar): ").upper()
        if dato == "C":
            return
        try:
            id_paciente = int(dato)
        except ValueError:
            print("La identificacion debe ser un dato numerico.")
            continue 
        encontrado = False
        for paciente in lista_pacientes:
            if paciente[0] == id_paciente:
                encontrado = True  
                print(f"Nombre: {paciente[1]}")
                while True:
                    nuevo_nombre = input("    MODIFICAR: ")
                    if nuevo_nombre == "":
                        nuevo_nombre = paciente[1]
                        break
                    elif 2 <= len(nuevo_nombre) <= 20:
                        break
                    else:
                        print("El nombre debe tener entre 2 y 20 caracteres.")

                print(f"Apellido 1: {paciente[2]}")
                while True:
                    nuevo_apellido1 = input("    MODIFICAR: ")
                    if nuevo_apellido1 == "":
                        nuevo_apellido1 = paciente[2]
                        break
                    elif 2 <= len(nuevo_apellido1) <= 20:
                        break
                    else:
                        print("El apellido debe tener entre 2 y 20 caracteres.")

                print(f"Apellido 2: {paciente[3]}")
                while True:
                    nuevo_apellido2 = input("    MODIFICAR: ")
                    if nuevo_apellido2 == "":
                        nuevo_apellido2 = paciente[3]
                        break
                    elif 2 <= len(nuevo_apellido2) <= 20:
                        break
                    else:
                        print("El apellido debe tener entre 2 y 20 caracteres.")

                print(f"Telefono: {paciente[4]}")
                while True:
                    telefono = input("    MODIFICAR: ")
                    if telefono == "":
                        telefono = paciente[4]
                        break
                    else:
                        try:
                            telefono = int(telefono)
                            if len(str(telefono)) == 8:
                                break
                            else:
                                print("El telefono debe tener 8 digitos exactos.")
                        except ValueError:
                            print("El telefono debe ser numerico.")

                print(f"Lugar de residencia: {paciente[5]}")
                while True:
                    residencia = input("    MODIFICAR: ")
                    if residencia == "":
                        residencia = paciente[5]
                        break
                    elif 5 <= len(residencia) <= 50:
                        break
                    else:
                        print("El lugar de residencia debe tener entre 5 y 50 caracteres.")

                print(f"Correo electronico: {paciente[6]}")
                while True:
                    correo_electronico = input("    MODIFICAR: ")
                    if correo_electronico == "":
                        correo_electronico = paciente[6]
                        break
                    elif "@" in correo_electronico and "." in correo_electronico:
                        break
                    else:
                        print("Correo invalido. Debe contener '@' y '.'  Ejemplo: nombre@dominio.com")

                while True:  # repite hasta que el usuario ingrese A o C correctamente
                    opcion_mod = input("OPCION C-CANCELAR A-ACEPTAR ").upper()
                    if opcion_mod == "A":
                        nueva_tupla = (id_paciente,nuevo_nombre,nuevo_apellido1,nuevo_apellido2,telefono,residencia,correo_electronico)
                        indice = lista_pacientes.index(paciente)
                        lista_pacientes[indice] = nueva_tupla
                        break
                    elif opcion_mod == "C":
                        break
                    else:
                        print("Opcion invalida, ingrese A para aceptar o C para cancelar.")
                break
        if not encontrado:
            print ("EL PACIENTE NO ESTA REGISTRADO, NO SE PUEDE MODIFICAR")
            continue



def eliminar_paciente():
    # Elimina un paciente de la lista del sistema
    # Necesita que el paciente exista en lista_pacientes
    # Si el paciente tiene citas activas asignadas no se puede eliminar
    # Pide confirmacion doble antes de borrar
    global lista_pacientes, citas
    while True:
        dato = input("Identificacion del paciente (C para cancelar): ").upper()
        if dato == "C":
            return
        try:
            id_paciente = int(dato)
        except ValueError:
            print("La identificacion debe ser un dato numerico.")
            continue 
        encontrado  = False 
        for paciente in lista_pacientes:
            if paciente[0] == id_paciente:
                encontrado = True
                print("Identificacion del paciente: ",paciente[0])
                print("Nombre: ",paciente[1])
                print("Apellido 1: ",paciente[2])
                print("Apellido 2: ",paciente[3])
                print("Telefono: ",paciente[4])
                print("Lugar de residencia: ",paciente[5])
                print("Correo electronico: ",paciente[6])
                
                opcion = input("OPCION C-CANCELAR A-ACEPTAR ").upper()
                if opcion == "A":
                    opcion2 = input("CONFIRMA LA ELIMINACION (SI/NO)").upper()
                    if opcion2 == "SI":
                        tiene_cita = False
                        for cita in citas:
                                for horario in cita[1]:
                                     if horario [1] == id_paciente:
                                         tiene_cita = True 
                                         break
                                if tiene_cita:
                                    break
                        if tiene_cita == True:
                            print ("ESTE PACIENTE TIENE CITAS ASOCIADAS, NO SE PUEDE ELIMINAR." )
                        else:
                            lista_pacientes.remove(paciente)
                    if opcion2 == "NO":
                        pass 
                    
                if opcion == "C":
                    pass
                break                        
        
        if not encontrado:
            print("EL PACIENTE NO ESTA REGISTRADO, NO SE PUEDE ELIMINAR" )
            continue




def crear_lista_de_citas_dia():
    # Genera los horarios disponibles del dia para cada medico registrado
    # Necesita que la configuracion este hecha (duracion distinta de 0)
    # Necesita que haya al menos un medico registrado
    # Si hay citas con pacientes asignados no permite crear la lista hasta cancelarlas
    # Borra las citas anteriores y crea los nuevos slots segun el horario de cada medico
    # Al terminar muestra todos los horarios generados por medico
    global citas,lista_medicos,hora_de_apertura,hora_de_cierre,duracion_en_minutos
    # valida que la configuracion haya sido completada antes de crear la lista
    if duracion_en_minutos == 0:
        print("DEBE HACER LA CONFIGURACION PRIMERO (opcion 1 del menu).")
        return

    # valida que existan medicos registrados antes de crear la lista
    if len(lista_medicos) == 0:
        print("NO HAY MEDICOS REGISTRADOS. REGISTRE AL MENOS UN MEDICO PRIMERO.")
        return
    
    hay_agendadas = False
    for cita in citas:
        for horario in cita[1]:
            if horario[1] > 0:
                hay_agendadas = True
                break
        if hay_agendadas:
            break

    if hay_agendadas:
        print("NO SE PUEDE CREAR LA LISTA DE CITAS DEL DIA DEBIDO A QUE HAY CITAS AGENDADAS. PARA CREAR LA LISTA PRIMERO DEBE CANCELAR ESAS CITAS. PUEDE EMITIR UN INFORME DE CITAS QUE LE SIRVA DE REFERENCIA PARA LUEGO HACER ESA CANCELACION.")
        return
    citas.clear()

    for medico in lista_medicos:
        hora_apertura = medico[7]
        hora_cierre = medico[8]
        lista_horarios = []
        while hora_apertura < hora_cierre:
            lista_horarios.append((hora_apertura,0))
            horas = hora_apertura // 100 
            minutos = hora_apertura % 100 
            minutos += duracion_en_minutos
            if minutos >= 60:
                horas+=1
                minutos -= 60
            hora_apertura = horas * 100 + minutos
        citas.append([medico[0],lista_horarios])
    print("LISTA DE CITAS DEL DIA CREADA EXITOSAMENTE.")
    print("")
    for cita in citas:  # muestra los horarios creados para cada medico
        for medico in lista_medicos:
            if medico[0] == cita[0]:
                print(f"MEDICO {medico[0]} {medico[2]} {medico[3]} {medico[1]}")
        for horario in cita[1]:  # imprime cada slot generado
            hh = horario[0] // 100
            mm = horario[0] % 100
            print(f"  {hh:02d}:{mm:02d} - LIBRE")
        print("")

def pedir_citas():
    # Permite asignar citas a pacientes, cancelarlas o deshabilitar horarios
    # Necesita que la lista de citas del dia este creada (opcion 4 del menu)
    # Necesita que los pacientes esten registrados para poder asignarles una cita
    # Muestra los medicos disponibles y sus horarios libres
    # Si el paciente ya tiene cita da la opcion de cancelarla antes de asignar una nueva
    # Si se ingresa -1 como ID se puede habilitar o deshabilitar un horario especifico
    global lista_medicos, citas
    if len(citas) == 0:
        print("NO HAY LISTA DE CITAS CREADA. PRIMERO EJECUTE LA OPCION 4 DEL MENU.")
        return
    print("    CLINICA MEDICA    ")
    print("    PEDIR CITAS       ")
    print("LISTA DE MEDICOS")
    print(f"{'Identificacion del medico':<30} {'Nombre'}")
    for medico in lista_medicos:
        print(f"{medico[0]:<30} {medico[1]} {medico[2]} {medico[3]}")
    print(F"{'0':<30} Salir")

    while True:
        opcion = input ("Medico seleccionado (0 o C para salir): ")
        if opcion == "0" or opcion.upper() == "C":
            return
        try:
            opcion_medico = int(opcion)
        except ValueError:
            print ("La identificacion del medico debe ser un dato numerico.")
            continue
        medico_encontrado = False  # bandera para saber si el id ingresado existe
        for medico in lista_medicos:
            if medico[0] == opcion_medico:
                medico_encontrado = True  # se encontro el medico en la lista
                print("     CITAS DISPONIBLES    ")
                for cita in citas:
                    if cita[0] == opcion_medico:
                       
                        while True:
                            print(f"Medico: {medico[0]} {medico[1]} {medico[2]} {medico[3]}")
                            print("Horarios disponibles")
                            for horario in cita[1]:
                                if horario [1] == 0:
                                    horas = horario[0] // 100 
                                    minutos = horario[0] % 100
                                    print(f"{horas:02d}:{minutos:02d}" )
                                elif horario[1] == -1:
                                    horas = horario[0] // 100
                                    minutos = horario [0] % 100
                                    print(f"{horas:02d}:{minutos:02d}**")
                            print("C - Cancelar")
                            dato = input("Identificacion del paciente: ").upper()
                            if dato == "C":
                                break
                            try:
                                id_paciente = int(dato)
                            except ValueError:
                                print("La identificacion deben ser datos numericos.")
                                continue
                            if id_paciente == -1:
                                try:
                                    ingrese_horario = int(input("Horario seleccionado (hhmm): "))
                                except ValueError:
                                    print("DEBEN SER DATOS NUMERICOS.")
                                    continue
                                for j in range(len(cita[1])):
                                   
                                    if cita[1][j][0] == ingrese_horario:
                                        if cita[1][j][1] == 0:
                                            cita[1][j] = (cita[1][j][0],-1)#si esta habilitado, se desabilita
                                            break
                                        elif cita[1][j][1] == -1:
                                            cita[1][j] = (cita[1][j][0],0) #estaba deshabilitado y ahora se habilita
                                            break
                                        else:
                                            print("NO SE PUEDE DESHABILITAR, TIENE UN PACIENTE ASIGNADO.")#otro caso: esta ocupado
                                continue #vuelve al inicio del while       
                            encontrado = False
                            for paciente in lista_pacientes:
                                if paciente[0] == id_paciente: 
                                    encontrado = True
                                    print(f"{paciente[1]} {paciente[2]} {paciente[3]}")
                                    break
                            if not encontrado: 
                                print("EL PACIENTE NO ESTA REGISTRADO.")
                                continue
                            tiene_citas = False
                            for second_cita in citas:
                                for paciente in second_cita[1]:
                                    if paciente [1] == id_paciente:
                                        tiene_citas = True  
                                        horas = paciente[0] // 100
                                        minutos = paciente[0] % 100
                                        print("Horario seleccionado: ", f"{horas:02d}:{minutos:02d}")
                                        if second_cita[0] != opcion_medico:
                                            for otro_medico in lista_medicos:
                                                if otro_medico[0] == second_cita [0]:  
                                                     print(f"Medico: {otro_medico[0]} {otro_medico[1]} {otro_medico[2]} {otro_medico[3]}")
                                        opcion = input("Cancelar cita (s/n).").upper()
                                        if opcion == "S":
                                            for j in range(len(second_cita[1])):
                                                if second_cita[1][j][1] == id_paciente:
                                                    second_cita[1][j] = (second_cita[1][j][0],0)
                                                    break
                                        if opcion == "N":
                                            break
                                if  tiene_citas:
                                    break      
                            if not tiene_citas:
                                    try:
                                        horario_seleccionado = int(input("Horario seleccionado (hhmm): "))
                                    except ValueError:
                                        print("LA HORA DEBE ESTAR COMPUESTA POR DATOS NUMERICOS.")
                                        continue
                                    encontro_horario = False
                                    for j in range (len(cita[1])):
                                        if cita[1][j][0] == horario_seleccionado:
                                            encontro_horario = True 
                                            if cita[1][j][1] == 0:
                                                cita [1][j] = (cita[1][j][0],id_paciente)
                                                break
                                            elif cita[1][j][1] == -1:
                                                print("ESE HORARIO NO ESTA DISPONIBLE.")
                                                break 
                                            else:
                                                print("ESE HORARIO YA ESTA OCUPADO.")
                                                break
                                    

                                    if not encontro_horario:
                                        print("ESE HORARIO NO EXISTE.")

        if not medico_encontrado:  # si el id no corresponde a ningun medico, avisa al usuario
            print("EL MEDICO NO ESTA REGISTRADO.")


def generar_pdf(titulo, lineas, nombre_archivo):
    # Recibe un titulo, una lista de lineas de texto y un nombre de archivo
    # Crea el PDF en orientacion horizontal para que las tablas no se corten
    # La llaman internamente las funciones de informes, no el usuario directamente
    # Al terminar guarda el PDF y lo abre automaticamente con el visor de Windows
    # Crea un documento PDF usando la biblioteca fpdf2
    # titulo: encabezado del informe, lineas: lista de texto a escribir, nombre_archivo: nombre del PDF a guardar
    pdf = FPDF(orientation="L")  # orientacion horizontal para que las tablas con muchas columnas no se corten
    pdf.add_page()  # agrega una pagina en blanco al documento
    pdf.set_margins(10, 10, 10)  # margenes: izquierda, superior, derecha en mm

    pdf.set_font("Helvetica", "B", 14)  # fuente en negrita para el titulo principal
    # new_x="LMARGIN", new_y="NEXT" reemplaza ln=True que esta deprecado en fpdf2 v2.5.2+
    pdf.cell(0, 10, "CLINICA MEDICA", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "B", 11)  # fuente ligeramente mas pequena para el subtitulo
    pdf.cell(0, 8, titulo, align="C", new_x="LMARGIN", new_y="NEXT")  # nombre del informe centrado

    pdf.ln(4)  # espacio en blanco entre el encabezado y el contenido

    pdf.set_font("Courier", size=8)  # fuente monoespaciada para que las columnas queden alineadas
    ancho_pagina = pdf.w - pdf.l_margin - pdf.r_margin  # calcula el ancho disponible restando los margenes
    for linea in lineas:
        # si la linea es muy larga se recorta para evitar el error "not enough horizontal space"
        linea_recortada = linea[:200]
        pdf.cell(ancho_pagina, 5, linea_recortada, new_x="LMARGIN", new_y="NEXT")

    pdf_bytes = pdf.output()  # obtiene el contenido del PDF como bytes
    with open(nombre_archivo, "wb") as f:  # escribe los bytes al archivo manualmente (evita problema de pathlib en Python 3.14)
        f.write(pdf_bytes)
    os.startfile(nombre_archivo)  # abre el PDF automaticamente con el visor predeterminado de Windows
    print(f"PDF generado: {nombre_archivo}")


def informes():
    # Muestra el submenu de informes y estadisticas del sistema
    # Para la mayoria de los informes necesita que la lista de citas este creada
    # Dependiendo de la opcion elige entre informe por medico, hora, paciente, estadistica o grafico
    while True:
        print("1. Informe de citas por medico") 
        print("2. Informe de citas por hora") 
        print("3. Informe de citas por paciente") 
        print("4. Estadistica de ocupacion por medico ")     
        print("5. Grafico (circular) de ocupacion por medico")    
        print("0. Salir")
        try:
            opcion = int(input("OPCION "))
        except ValueError:
            print("DEBE INGRESAR UN DATO NUMERICO.")
            continue
        match opcion:
            case 1:
                informe_citas_medico()
            case 2:
                informe_citas_hora()
            case 3:
                informe_citas_paciente()
            case 4:
                estadistica_ocupacion()
            case 5:
                grafico_ocupacion_medico()
            case 0:
                break
            case _:
                print("Opcion invalida.")  # avisa si el numero ingresado no corresponde a ninguna opcion


def informe_citas_medico():
    # Genera un informe de citas ordenado por medico
    # Necesita que la lista de citas este creada y que haya medicos registrados
    # Permite ver un medico especifico o todos los medicos
    # Permite filtrar por citas ocupadas solamente o ver todos los horarios
    # Ordena los medicos por apellido usando burbuja antes de mostrarlos
    # Al final genera un PDF con el informe y lo abre automaticamente
    global citas, lista_medicos, lista_pacientes

    # copia para ordenar sin modificar la lista original
    copia_medicos = lista_medicos[:]
    # ordenamiento burbuja por apellido1, apellido2, nombre
    for i in range(len(copia_medicos)):
        for j in range(i+1, len(copia_medicos)):
            if copia_medicos[i][2] > copia_medicos[j][2]:
                copia_medicos[i], copia_medicos[j] = copia_medicos[j], copia_medicos[i]
            elif copia_medicos[i][2] == copia_medicos[j][2]:
                if copia_medicos[i][3] > copia_medicos[j][3]:
                    copia_medicos[i], copia_medicos[j] = copia_medicos[j], copia_medicos[i]
                elif copia_medicos[i][3] == copia_medicos[j][3]:
                    if copia_medicos[i][1] > copia_medicos[j][1]:
                        copia_medicos[i], copia_medicos[j] = copia_medicos[j], copia_medicos[i]

    while True:
        opcion = input("DESEA VER LA INFORMACION DE UNO O TODOS LOS MEDICOS: T = todos, U = uno, C para cancelar: ").upper()

        if opcion == "U":
            try:
                id_medico = int(input("Ingrese la identificacion del medico: "))
            except ValueError:
                print("DEBE INGRESAR UN DATO NUMERICO")
                continue
            while True:  # repite hasta obtener O o T valido
                filtro = input("Ver horarios: O = solo los ocupados, T = todos ").upper()
                if filtro in ("O", "T"):
                    break
                print("Opcion invalida. Ingrese O o T.")
            encontrado = False
            lineas = []  # lista donde se acumula el contenido del informe para el PDF
            for cita in citas:
                if cita[0] == id_medico:
                    encontrado = True
                    for medico in copia_medicos:
                        if medico[0] == id_medico:
                            lineas.append(f"MEDICO {medico[0]} {medico[2]} {medico[3]} {medico[1]}")
                            lineas.append(f"{'HORARIO':<10} {'ID.PACIENTE':<15} NOMBRE DEL PACIENTE")
                            for horario in cita[1]:
                                if filtro == "T" or horario[1] > 0:
                                    hh = horario[0] // 100
                                    mm = horario[0] % 100
                                    if horario[1] > 0:
                                        for paciente in lista_pacientes:
                                            if paciente[0] == horario[1]:
                                                lineas.append(f"{hh:02d}:{mm:02d}     {paciente[0]:<15} {paciente[1]} {paciente[2]} {paciente[3]}")
                                    elif horario[1] == -1:
                                        lineas.append(f"{hh:02d}:{mm:02d}**")
                                    elif horario[1] == 0:
                                        lineas.append(f"{hh:02d}:{mm:02d}")
            if not encontrado:
                print("EL MEDICO NO POSEE CITAS PARA MOSTRAR")
                continue
            for linea in lineas:  # muestra el informe en consola
                print(linea)
            generar_pdf("INFORME DE CITAS POR MEDICO", lineas, "informe_citas_medico.pdf")

        elif opcion == "T":
            while True:  # repite hasta obtener O o T valido
                filtro = input("Ver horarios: O = solo los ocupados, T = todos ").upper()
                if filtro in ("O", "T"):
                    break
                print("Opcion invalida. Ingrese O o T.")
            lineas = []  # lista donde se acumula el contenido del informe para el PDF
            for cita in citas:
                for medico in copia_medicos:
                    if cita[0] == medico[0]:
                        lineas.append(f"MEDICO {medico[0]} {medico[2]} {medico[3]} {medico[1]}")
                        lineas.append(f"{'HORARIO':<10} {'ID.PACIENTE':<15} NOMBRE DEL PACIENTE")
                        for horario in cita[1]:
                            if filtro == "T" or horario[1] > 0:
                                hh = horario[0] // 100
                                mm = horario[0] % 100
                                if horario[1] > 0:
                                    for paciente in lista_pacientes:
                                        if paciente[0] == horario[1]:
                                            lineas.append(f"{hh:02d}:{mm:02d}     {paciente[0]:<15} {paciente[1]} {paciente[2]} {paciente[3]}")
                                elif horario[1] == -1:
                                    lineas.append(f"{hh:02d}:{mm:02d}**")
                                elif horario[1] == 0:
                                    lineas.append(f"{hh:02d}:{mm:02d}")
                        lineas.append("")  # linea en blanco entre medicos
            for linea in lineas:  # muestra el informe en consola
                print(linea)
            generar_pdf("INFORME DE CITAS POR MEDICO", lineas, "informe_citas_medico.pdf")

        elif opcion == "C":
            break
        else:
            print("OPCION INVALIDA.")


def informe_citas_hora():
    # Genera un informe de citas agrupado por horario
    # Necesita que la lista de citas este creada con horarios registrados
    # Permite consultar una hora especifica o todas las horas del dia
    # Permite filtrar por citas ocupadas o ver todos los horarios
    # Ordena las horas de menor a mayor usando burbuja
    # Al final genera un PDF con el informe y lo abre automaticamente
    global citas, lista_medicos, lista_pacientes

    # recopila todas las horas distintas que existen en las citas de todos los medicos
    horas_unicas = []
    for cita in citas:
        for horario in cita[1]:
            hora = horario[0]
            encontrado = False
            for h in horas_unicas:
                if h == hora:
                    encontrado = True
                    break
            if not encontrado:
                horas_unicas.append(hora)
    # ordena las horas de menor a mayor (orden ascendente)
    for i in range(len(horas_unicas)):
        for j in range(i+1, len(horas_unicas)):
            if horas_unicas[i] > horas_unicas[j]:
                horas_unicas[i], horas_unicas[j] = horas_unicas[j], horas_unicas[i]

    while True:
        opcion = input("DESEA VER LA INFORMACION POR HORARIO: T = todos, U = uno, C para cancelar: ").upper()

        if opcion == "U":
            try:
                hora_buscada = int(input("Ingrese la hora: "))
            except ValueError:
                print("DEBE INGRESAR UN DATO NUMERICO")
                continue
            while True:  # repite hasta obtener O o T valido
                filtro = input("Ver horarios: O = solo los ocupados, T = todos ").upper()
                if filtro in ("O", "T"):
                    break
                print("Opcion invalida. Ingrese O o T.")
            encontrado = False
            hh = hora_buscada // 100
            mm = hora_buscada % 100
            lineas = []  # lista donde se acumula el contenido del informe para el PDF
            lineas.append(f"HORARIO: {hh:02d}:{mm:02d}")
            lineas.append(f"{'ID.MEDICO':<12} {'NOMBRE DEL MEDICO':<30} {'ID.PACIENTE':<12} NOMBRE DEL PACIENTE")
            for cita in citas:
                for horario in cita[1]:
                    if horario[0] == hora_buscada:
                        encontrado = True
                        if filtro == "T" or horario[1] > 0:
                            for medico in lista_medicos:
                                if medico[0] == cita[0]:
                                    if horario[1] > 0:
                                        for paciente in lista_pacientes:
                                            if paciente[0] == horario[1]:
                                                lineas.append(f"{medico[0]:<12} {medico[1]} {medico[2]} {medico[3]:<30} {paciente[0]:<12} {paciente[1]} {paciente[2]} {paciente[3]}")
                                    elif horario[1] == -1:
                                        lineas.append(f"** {medico[0]:<10} {medico[1]} {medico[2]} {medico[3]}")
                                    elif horario[1] == 0:
                                        lineas.append(f"{medico[0]:<12} {medico[1]} {medico[2]} {medico[3]}")
            if not encontrado:
                print("ESA HORA NO EXISTE EN EL SISTEMA.")
                continue
            for linea in lineas:  # muestra el informe en consola
                print(linea)
            generar_pdf("INFORME DE CITAS POR HORA", lineas, "informe_citas_hora.pdf")

        elif opcion == "T":
            while True:  # repite hasta obtener O o T valido
                filtro = input("Ver horarios: O = solo los ocupados, T = todos ").upper()
                if filtro in ("O", "T"):
                    break
                print("Opcion invalida. Ingrese O o T.")
            lineas = []  # lista donde se acumula el contenido del informe para el PDF
            lineas.append(f"{'HORARIO':<10} {'ID.MEDICO':<12} {'NOMBRE DEL MEDICO':<30} {'ID.PACIENTE':<12} NOMBRE DEL PACIENTE")
            for hora_actual in horas_unicas:
                hh = hora_actual // 100
                mm = hora_actual % 100
                lineas.append(f"{hh:02d}:{mm:02d}")
                for cita in citas:
                    for horario in cita[1]:
                        if horario[0] == hora_actual:
                            if filtro == "T" or horario[1] > 0:
                                for medico in lista_medicos:
                                    if medico[0] == cita[0]:
                                        if horario[1] > 0:
                                            for paciente in lista_pacientes:
                                                if paciente[0] == horario[1]:
                                                    lineas.append(f"           {medico[0]:<12} {medico[1]} {medico[2]} {medico[3]:<30} {paciente[0]:<12} {paciente[1]} {paciente[2]} {paciente[3]}")
                                        elif horario[1] == -1:
                                            lineas.append(f"**         {medico[0]:<12} {medico[1]} {medico[2]} {medico[3]}")
                                        elif horario[1] == 0:
                                            lineas.append(f"           {medico[0]:<12} {medico[1]} {medico[2]} {medico[3]}")
                lineas.append("")  # linea en blanco entre horas
            if len(lineas) == 1:  # solo tiene el encabezado, no hay citas registradas
                print("NO HAY CITAS REGISTRADAS.")
                continue
            for linea in lineas:  # muestra el informe en consola
                print(linea)
            generar_pdf("INFORME DE CITAS POR HORA", lineas, "informe_citas_hora.pdf")

        elif opcion == "C":
            break
        else:
            print("OPCION INVALIDA.")



def informe_citas_paciente():
    # Genera un informe de citas agrupado por paciente
    # Necesita que haya citas con pacientes asignados para mostrar datos utiles
    # Permite consultar un paciente especifico o todos los pacientes
    # Permite filtrar por un horario especifico o ver todas las citas
    # Ordena los pacientes por apellido usando burbuja antes de mostrarlos
    # Al final genera un PDF con el informe y lo abre automaticamente
    global citas, lista_medicos, lista_pacientes

    # copia para ordenar sin modificar la lista original
    copia_pacientes = lista_pacientes[:]
    # ordenamiento burbuja por apellido1, apellido2, nombre
    for i in range(len(copia_pacientes)):
        for j in range(i+1, len(copia_pacientes)):
            if copia_pacientes[i][2] > copia_pacientes[j][2]:
                copia_pacientes[i], copia_pacientes[j] = copia_pacientes[j], copia_pacientes[i]
            elif copia_pacientes[i][2] == copia_pacientes[j][2]:
                if copia_pacientes[i][3] > copia_pacientes[j][3]:
                    copia_pacientes[i], copia_pacientes[j] = copia_pacientes[j], copia_pacientes[i]
                elif copia_pacientes[i][3] == copia_pacientes[j][3]:
                    if copia_pacientes[i][1] > copia_pacientes[j][1]:
                        copia_pacientes[i], copia_pacientes[j] = copia_pacientes[j], copia_pacientes[i]

    while True:
        opcion = input("U = un paciente, T = todos, C = cancelar: ").upper()
        if opcion == "C":
            return

        # loop que repite hasta obtener un filtro valido (H o T)
        while True:
            filtro = input("Desea buscar segun: H = horario especifico, T = todos los horarios: ").upper()
            if filtro == "T":
                hora_buscada = 0
                break
            elif filtro == "H":
                try:
                    hora_buscada = int(input("Ingrese la hora que desea consultar (hhmm): "))
                    break
                except ValueError:
                    print("DEBE INGRESAR UN DATO NUMERICO.")
            else:
                print("OPCION INVALIDA. Ingrese H o T.")

        if opcion == "U":
            dato = input("Ingrese el id del paciente (C para cancelar): ").upper()
            if dato == "C":
                continue
            try:
                id_paciente = int(dato)
            except ValueError:
                print("DEBE SER UN DATO NUMERICO.")
                continue
            encontrado = False
            lineas = []  # lista donde se acumula el contenido del informe para el PDF
            lineas.append(f"{'ID.PACIENTE':<12} {'NOMBRE DEL PACIENTE':<30} {'HORARIO':<10} {'ID.MEDICO':<12} NOMBRE DEL MEDICO")
            for cita in citas:
                for horario in cita[1]:
                    if horario[1] == id_paciente:
                        encontrado = True
                        if filtro == "T" or horario[0] == hora_buscada:
                            for medico in lista_medicos:
                                if medico[0] == cita[0]:
                                    hh = horario[0] // 100
                                    mm = horario[0] % 100
                                    for paciente in lista_pacientes:
                                        if paciente[0] == id_paciente:
                                            lineas.append(f"{paciente[0]:<12} {paciente[1]} {paciente[2]} {paciente[3]:<30} {hh:02d}:{mm:02d}     {medico[0]:<12} {medico[1]} {medico[2]} {medico[3]}")
            if not encontrado:
                print("EL PACIENTE NO TIENE CITAS REGISTRADAS.")
                continue
            if len(lineas) == 1:  # solo tiene el encabezado, no hay datos para ese filtro
                print("NO HAY CITAS EN ESE HORARIO.")
                continue
            for linea in lineas:  # muestra el informe en consola
                print(linea)
            generar_pdf("INFORME DE CITAS POR PACIENTE", lineas, "informe_citas_paciente.pdf")

        elif opcion == "T":
            lineas = []  # lista donde se acumula el contenido del informe para el PDF
            lineas.append(f"{'ID.PACIENTE':<12} {'NOMBRE DEL PACIENTE':<30} {'HORARIO':<10} {'ID.MEDICO':<12} NOMBRE DEL MEDICO")
            for paciente in copia_pacientes:
                for cita in citas:
                    for horario in cita[1]:
                        if horario[1] == paciente[0]:
                            if filtro == "T" or horario[0] == hora_buscada:
                                for medico in lista_medicos:
                                    if medico[0] == cita[0]:
                                        hh = horario[0] // 100
                                        mm = horario[0] % 100
                                        lineas.append(f"{paciente[0]:<12} {paciente[1]} {paciente[2]} {paciente[3]:<30} {hh:02d}:{mm:02d}     {medico[0]:<12} {medico[1]} {medico[2]} {medico[3]}")
            if len(lineas) == 1:  # solo tiene el encabezado, ningun paciente tiene citas
                print("NO HAY CITAS REGISTRADAS.")
                continue
            for linea in lineas:  # muestra el informe en consola
                print(linea)
            generar_pdf("INFORME DE CITAS POR PACIENTE", lineas, "informe_citas_paciente.pdf")

        else:
            print("OPCION INVALIDA.")
        
def estadistica_ocupacion():
    # Muestra cuantas citas estan ocupadas, libres y reservadas por medico con porcentajes
    # Necesita que la lista de citas este creada
    # Permite ver un medico especifico o todos los medicos
    # Ordena los medicos por apellido usando burbuja antes de mostrarlos
    # Al final genera un PDF con la estadistica y lo abre automaticamente
    global lista_medicos,lista_pacientes,citas
    copia_medicos = lista_medicos[:]
    for i in range (len(lista_medicos)):
        for j in range(i+1,len(lista_medicos)):
            if copia_medicos[i][2] > copia_medicos[j][2]:
                copia_medicos[i], copia_medicos[j] = copia_medicos[j], copia_medicos[i]
            elif copia_medicos[i][2] == copia_medicos[j][2]:
                if copia_medicos[i][3] > copia_medicos[j][3]:
                    copia_medicos[i] , copia_medicos[j] = copia_medicos[j],copia_medicos[i]
                elif copia_medicos[i][3] == copia_medicos[j][3]:
                    if copia_medicos[i][1] >copia_medicos[j][1]:
                        copia_medicos[i],copia_medicos[j] = copia_medicos[j], copia_medicos[i]
    while True:
        opcion = input("U = un medico, T = todos, C = cancelar: ").upper()
        if opcion == "C":
            return   
        if opcion == "U":
            dato = input("Ingrese el id del medico (C para cancelar): ").upper()  # .upper() para aceptar c minuscula
            if dato == "C":
                continue
            try:
                id_medico = int(dato)
            except ValueError:
                print("DEBEN SER DATOS NUMERICOS.")
                continue
            encontrado = False
            lineas = []  # lista donde se acumula el contenido del informe para el PDF
            lineas.append(f"{'ID.MEDICO':<10} {'NOMBRE DEL MEDICO':<30} {'DISPONIBLES':<13} {'OCUPADAS':<12} {'LIBRES':<12} RESERVADAS")
            for medico in copia_medicos:
                if medico[0] == id_medico:
                    encontrado = True
                    disponibles = 0
                    ocupadas = 0
                    libres = 0
                    reservadas = 0
                    for cita in citas:
                        if cita[0] == id_medico:
                            for horario in cita[1]:
                                disponibles += 1
                                if horario[1] > 0:
                                    ocupadas += 1
                                elif horario[1] == 0:
                                    libres += 1
                                elif horario[1] == -1:
                                    reservadas += 1
                    if disponibles > 0:
                        porcentaje_ocupacion = (ocupadas / disponibles) * 100
                        porcentaje_libres = (libres / disponibles) * 100
                        porcentaje_reservadas = (reservadas / disponibles) * 100
                        ocup_str = f"{ocupadas} {porcentaje_ocupacion:.0f}%"  # texto con ancho fijo para columna
                        libr_str = f"{libres} {porcentaje_libres:.0f}%"  # texto con ancho fijo para columna
                        res_str = f"{reservadas} {porcentaje_reservadas:.0f}%"  # texto con ancho fijo para columna
                        lineas.append(f"{medico[0]:<10} {(medico[2]+' '+medico[3]+' '+medico[1]):<30} {disponibles:<13} {ocup_str:<12} {libr_str:<12} {res_str}")
                    else:
                        print("EL MEDICO NO TIENE HORARIOS REGISTRADOS.")
            if not encontrado:
                print("EL MEDICO NO ESTA REGISTRADO.")
                continue
            for linea in lineas:  # muestra el informe en consola
                print(linea)
            generar_pdf("ESTADISTICA DE OCUPACION POR MEDICO", lineas, "estadistica_ocupacion.pdf")

        elif opcion == "T":
            lineas = []  # lista donde se acumula el contenido del informe para el PDF
            lineas.append(f"{'ID.MEDICO':<10} {'NOMBRE DEL MEDICO':<30} {'DISPONIBLES':<13} {'OCUPADAS':<12} {'LIBRES':<12} RESERVADAS")
            for medico in copia_medicos:
                disponibles = 0
                ocupadas = 0
                libres = 0
                reservadas = 0
                for cita in citas:
                    if cita[0] == medico[0]:
                        for horario in cita[1]:
                            disponibles += 1
                            if horario[1] > 0:
                                ocupadas += 1
                            elif horario[1] == 0:
                                libres += 1
                            elif horario[1] == -1:
                                reservadas += 1
                if disponibles > 0:
                    porcentaje_ocupacion = (ocupadas / disponibles) * 100
                    porcentaje_libres = (libres / disponibles) * 100
                    porcentaje_reservadas = (reservadas / disponibles) * 100
                    ocup_str = f"{ocupadas} {porcentaje_ocupacion:.0f}%"  # texto con ancho fijo para columna
                    libr_str = f"{libres} {porcentaje_libres:.0f}%"  # texto con ancho fijo para columna
                    res_str = f"{reservadas} {porcentaje_reservadas:.0f}%"  # texto con ancho fijo para columna
                    lineas.append(f"{medico[0]:<10} {(medico[2]+' '+medico[3]+' '+medico[1]):<30} {disponibles:<13} {ocup_str:<12} {libr_str:<12} {res_str}")
                else:
                    lineas.append(f"{medico[0]:<10} {(medico[2]+' '+medico[3]+' '+medico[1]):<30} SIN HORARIOS REGISTRADOS.")
            for linea in lineas:  # muestra el informe en consola
                print(linea)
            generar_pdf("ESTADISTICA DE OCUPACION POR MEDICO", lineas, "estadistica_ocupacion.pdf")

        else:
            print("OPCION INVALIDA.")





def grafico_ocupacion_medico():
    # Genera un grafico circular (pie chart) mostrando ocupacion, citas libres y reservadas
    # Necesita que la lista de citas este creada con horarios registrados
    # Permite graficar un medico especifico o todos uno por uno
    # Ordena los medicos por apellido usando burbuja antes de procesarlos
    # Solo incluye en el grafico las categorias que tienen al menos una cita (evita etiquetas encimadas)
    # Guarda cada grafico como PDF con el nombre grafico_medico_{id}.pdf y lo abre automaticamente
    global lista_medicos, lista_pacientes, citas

    # copia para ordenar sin modificar la lista original
    copia_medicos = lista_medicos[:]
    # ordenamiento burbuja por apellido1, apellido2, nombre
    for i in range(len(lista_medicos)):
        for j in range(i+1, len(lista_medicos)):
            if copia_medicos[i][2] > copia_medicos[j][2]:
                copia_medicos[i], copia_medicos[j] = copia_medicos[j], copia_medicos[i]
            elif copia_medicos[i][2] == copia_medicos[j][2]:
                if copia_medicos[i][3] > copia_medicos[j][3]:
                    copia_medicos[i], copia_medicos[j] = copia_medicos[j], copia_medicos[i]
                elif copia_medicos[i][3] == copia_medicos[j][3]:
                    if copia_medicos[i][1] > copia_medicos[j][1]:
                        copia_medicos[i], copia_medicos[j] = copia_medicos[j], copia_medicos[i]

    while True:
        opcion = input("U = un medico, T = todos, C = cancelar: ").upper()
        if opcion == "C":
            return

        if opcion == "U":
            dato = input("Ingrese el id del medico (C para cancelar): ").upper()  # .upper() para aceptar c minuscula
            if dato == "C":
                continue
            try:
                id_medico = int(dato)
            except ValueError:
                print("DEBEN SER DATOS NUMERICOS.")
                continue
            encontrado = False
            for medico in copia_medicos:
                if medico[0] == id_medico:
                    encontrado = True
                    disponibles = 0
                    ocupadas = 0
                    libres = 0
                    reservadas = 0
                    for cita in citas:
                        if cita[0] == id_medico:
                            for horario in cita[1]:
                                disponibles += 1
                                if horario[1] > 0:
                                    ocupadas += 1
                                elif horario[1] == 0: 
                                    libres += 1
                                elif horario[1] == -1:
                                    reservadas += 1
                    if disponibles > 0:
                        # se calculan los porcentajes para mostrar en el titulo del grafico
                        porcentaje_ocupacion = (ocupadas / disponibles) * 100
                        porcentaje_libres = (libres / disponibles) * 100
                        porcentaje_reservadas = (reservadas / disponibles) * 100
                        # filtra categorias con valor 0 para evitar etiquetas encimadas en el grafico
                        datos = [(v, l, c) for v, l, c in zip(
                            [ocupadas, libres, reservadas],
                            ['Citas ocupadas', 'Citas libres', 'Citas reservadas'],
                            ['green', 'red', 'peachpuff']  # ocupadas=verde, libres=rojo, reservadas=durazno
                        ) if v > 0]
                        sizes  = [d[0] for d in datos]
                        labels = [d[1] for d in datos]
                        colors = [d[2] for d in datos]

                        plt.figure()
                        plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors)  # autopct muestra el porcentaje en cada sector
                        plt.title(f"Ocupacion para: {medico[2]} {medico[3]} {medico[1]}\nTotal de citas disponibles: {disponibles}")

                        # nombre del PDF unico por medico usando su identificacion
                        nombre_pdf = f"grafico_medico_{medico[0]}.pdf"
                        # savefig guarda el grafico actual como archivo PDF antes de mostrarlo en pantalla
                        plt.savefig(nombre_pdf, format="pdf", bbox_inches="tight")
                        os.startfile(nombre_pdf)  # abre el PDF automaticamente con el visor de Windows
                        print(f"PDF generado: {nombre_pdf}")
                        plt.show()
                    else:
                        print("EL MEDICO NO TIENE HORARIOS REGISTRADOS.")
            if not encontrado:
                print("EL MEDICO NO ESTA REGISTRADO.")
                continue

        elif opcion == "T":
            for medico in copia_medicos:
                disponibles = 0
                ocupadas = 0
                libres = 0
                reservadas = 0
                for cita in citas:
                    if cita[0] == medico[0]:
                        for horario in cita[1]:
                            disponibles += 1
                            if horario[1] > 0:
                                ocupadas += 1
                            elif horario[1] == 0:
                                libres += 1
                            elif horario[1] == -1:
                                reservadas += 1
                if disponibles > 0:
                    # se calculan los porcentajes para mostrar en el titulo del grafico
                    porcentaje_ocupacion = (ocupadas / disponibles) * 100
                    porcentaje_libres = (libres / disponibles) * 100
                    porcentaje_reservadas = (reservadas / disponibles) * 100
                    # filtra categorias con valor 0 para evitar etiquetas encimadas en el grafico
                    datos = [(v, l, c) for v, l, c in zip(
                        [ocupadas, libres, reservadas],
                        ['Citas ocupadas', 'Citas libres', 'Citas reservadas'],
                        ['red', 'green', 'peachpuff']  # ocupadas=rojo, libres=verde, reservadas=durazno
                    ) if v > 0]
                    sizes  = [d[0] for d in datos]
                    labels = [d[1] for d in datos]
                    colors = [d[2] for d in datos]

                    plt.figure()
                    plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors)  # autopct muestra el porcentaje en cada sector
                    plt.title(f"Ocupacion para: {medico[2]} {medico[3]} {medico[1]}\nTotal de citas disponibles: {disponibles}")

                    # nombre del PDF unico por medico usando su identificacion
                    nombre_pdf = f"grafico_medico_{medico[0]}.pdf"
                    # savefig guarda el grafico actual como archivo PDF antes de mostrarlo en pantalla
                    plt.savefig(nombre_pdf, format="pdf", bbox_inches="tight")
                    os.startfile(nombre_pdf)  # abre el PDF automaticamente con el visor de Windows
                    print(f"PDF generado: {nombre_pdf}")
                    plt.show()
                else:
                    print(f"{medico[1]} {medico[2]} {medico[3]} — SIN HORARIOS REGISTRADOS.")
        else:
            print("OPCION INVALIDA.")



def ayuda():
    # Abre el manual de usuario del sistema en formato PDF
    # Necesita que el archivo manual_de_usuario_clinica_medica.pdf este en la misma carpeta que el programa
    # Si el archivo no existe muestra un mensaje de error en lugar de crashear
    print("    CLINICA MEDICA    ")
    print("    AYUDA             ")
    try:
        os.startfile("manual_de_usuario_clinica_medica.pdf")  # abre el manual con el visor PDF del sistema
        print("El manual de usuario ha sido desplegado.")
    except FileNotFoundError:
        print("NO SE ENCONTRO EL ARCHIVO manual_de_usuario_clinica_medica.pdf")
    input("Presione Enter para volver al menu principal...")

 





def acerca_de():
    # Muestra la informacion general del programa: nombre, version, fecha y autor
    # No necesita nada antes de ejecutarse
    print("CLINICA MEDICA")
    print("Version: 1.0")
    print("Fecha de creacion: 24/4/2026")
    print("Autor: Aldrickson Diaz Tijerino")

if __name__ == "__main__":
    menu()
 