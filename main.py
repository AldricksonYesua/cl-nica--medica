
#variables globales
hora_de_apertura = 0 
hora_de_cierre = 0 
duracion_en_minutos= 0
citas = []
lista_medicos = [] 
lista_pacientes = []

def menu():
    while True:
        print ("                  CLINICA MEDICA                ")
        print ("1. Configuracion")
        print ("2. Registrar medicos")
        print ("3. Registrar pacientes")
        print ("4. Crear lista de cistas del dia")
        print ("5. Pedir citas")
        print ("6. Informes")
        print ("7. Ayuda")
        print ("8. Acerca de")
        print ("0. Salir")
        #Para aprender a como manejar errores de entrada de usuario
        #Le pregunte a la herramenta de IA (claude) sobre una herramienta que me ayudara a manejar este tipo de errores
        #En este caso que ocurre si el usuario escribe una letra en vez de un numero?
        #Lo entendi y lo implemente en el menu principal 
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


menu()

def configuracion():
    global hora_de_apertura,hora_de_cierre,duracion_en_minutos,citas

    print ("        CLINICA MEDICA      ")
    print ("        CONFIGURACION       ")
    print ("Horario de la clinica")

    while True:
        apertura = input("Hora de apertura(hhmm):").upper()
        if apertura == "C":
            return
        try:
            apertura = int(apertura)
        except ValueError:
            print("Debe ingresar unicamente valores numericos")
            apertura = -1
        try:
            cierre = int(input("Hora de cierre(hhmm):")) 
        except ValueError:
            print("Debe ingresar unicamente valores numericos")
            cierre = -1

        try:
            duracion = int(input("Duracion en minutos de cada cita(15,20,30):"))
        except ValueError:
            print("Debe ingresar unicamente valores numericos")
            duracion = -1
        if apertura >= cierre:
            print("Error: la hora de apertura debe ser menor a la hora de cierre")
            continue
        if duracion not in (15,20,30):
            print("Error: la duracion debe estar entre (15,20,30)")
            continue 
        else:
            break 

    
    opcion = str(input("OPCION C-CANCELAR A-ACEPTAR")).upper() #sirve para detectar c o C lo descrubri investigando por internet 
   
    match opcion:
        case "A":
            opcion = input("AL ACEPTAR ESTA CONFIGURACIÓN BORRA LA LISTA DE CITAS QUE SE TENGA ACTUALMENTE. CONFIRMA LA ACEPTACIÓN (SI/NO)").upper()
            if opcion == "SI":
                #FALTA VALIDAR EL HORARIO DE MEDICOS CON EL NUEVO HORARIO PERO AUN ESTA CREDA LA FUNCION DE MEDICOS
                citas.clear() #Para limppiar la funcion y eliminar los datos anteriores
                hora_de_apertura = apertura
                hora_de_cierre = cierre
                duracion_en_minutos = duracion
            else:
                pass

        case "C":
            pass #instruccion aprendida gracias a la IA claude, ya que dijo que en python debe haber al mennos una instrucion 
        case _:
            print ("Opcion invalida") 




def registrar_medicos():
    print ("         CLINICA MEDICA       ")
    print ("         REGISTRAR MEDICOS   ")

    while True:
        print("1. Agregar medicos")
        print("2. Consultar medicos")
        print("3. Modificar medicos")
        print("4. Eliminar medicos")
        print("5. Salir")
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
            case 5:
                break
            case _:
                print("Opcion invalida")

            
def agregar_medico():
    global lista_medicos,hora_de_apertura,hora_de_cierre
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
            numero_telefono = -1 
        
        if len(str(numero_telefono)) == 8:
                break
        else:
            print("El numero de telefono debe tener 8 digitos exactos. ")
            continue

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
            print("Correo inválido. Debe contener '@' y '.'  Ejemplo: nombre@dominio.com")
            continue 
    while True: 
        try:
            hora_apertura = int(input("Ingrese la hora de apertura (hhmm): "))
        except ValueError: 
            print("La hora deben ser numeros enteros.")
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
        if hora_cierre <= hora_de_cierre and hora_cierre > hora_apertura:
            break
        else:
            print("La hora de cierre del medico debe ser menor o igual a la  hora de apertura de la clinica.")
            continue

    medicos = (id_medico,nombre,apellido1,apellido2,numero_telefono,lugar_residencia,correo_electronico,hora_apertura,hora_cierre)
    print ("    REGISTRAR MEDICOS   ")
    print ("    AGREGAR MEDICOS     ")
    print("Identificación del médico: ",id_medico)
    print("Nombre: ",nombre)
    print("Apellido 1: ",apellido1)
    print("Apellido 2: ",apellido2)
    print("Teléfono: ",numero_telefono)
    print("Lugar de residencia: ",lugar_residencia)
    print("Correo electrónico: ",correo_electronico)
    print("Hora de apertura: ",hora_apertura)
    print("Hora de cierre: ",hora_cierre)
    opcion_final = input("OPCION C-CANCELAR A-ACEPTAR").upper()
    if opcion_final == "A":
        lista_medicos.append(medicos)
    elif opcion_final == "C":
        return
    else:
        print("Opción inválida")


def consultar_medico():
    global lista_medicos

    print ("    REGISTRAR MEDICOS   ")
    print ("    CONSULTAR MEDICOS    ") 
    while True:
        dato = input("Identificación del médico (C para cancelar): ").upper()
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
               print("Identificación del médico: ",medico[0])
               print("Nombre: ",medico[1])
               print("Apellido 1: ",medico[2])
               print("Apellido 2: ",medico[3])
               print("Teléfono: ",medico[4])
               print("Lugar de residencia: ",medico[5])
               print("Correo electrónico: ",medico[6])
               print("Hora de apertura: ",medico[7])
               print("Hora de cierre: ",medico[8])
               break 

        if not encontrado:
            print ("EL MÉDICO NO ESTA REGISTRADO, NO SE PUEDE CONSULTAR")
            continue
        else:
            input("OPCION A-ACEPTAR ")

def modificar_medico():
    global lista_medicos
    print ("    REGISTRAR MEDICOS   ")
    print ("    MODIFICAR MEDICOS    ")
    while True:
        dato = input("Identificación del médico (C para cancelar): ").upper()
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
                nuevo_nombre = input("    MODIFICAR: ")
                if nuevo_nombre == "":
                    nuevo_nombre = medico[1]

                print(f"Apellido 1: {medico[2]}")
                nuevo_apellido1 = input("    MODIFICAR: ")
                if nuevo_apellido1 == "":
                    nuevo_apellido1 = medico[2]

                print(f"Apellido 2: {medico[3]}")
                nuevo_apellido2 = input("    MODIFICAR: ")
                if nuevo_apellido2 == "":
                    nuevo_apellido2 = medico[3]

                print(f"Teléfono: {medico[4]}")
                telefono = input("    MODIFICAR: ")
                if telefono == "":
                    telefono = medico[4]

                print(f"Lugar de residencia: {medico[5]}")
                residencia = input("    MODIFICAR: ")
                if residencia == "":
                    residencia = medico[5]

                print(f"Correo electrónico: {medico[6]}")
                correo_electronico = input("    MODIFICAR: ")
                if correo_electronico == "":
                    correo_electronico = medico[6]

                print(f"Hora de apertura {medico[7]}")
                hora_apertura = input("    MODIFICAR: ")
                if hora_apertura == "":
                    hora_apertura = medico[7]

                print(f"Hora de cierre {medico[8]}")
                hora_cierre = input("    MODIFICAR: ")
                if hora_cierre == "":
                    hora_cierre = medico[8]
                opcion = input ("OPCION C-CANCELAR A-ACEPTAR ")
                if opcion == "A":
                    nueva_tupla = (id_medico,nuevo_nombre,nuevo_apellido1,nuevo_apellido2,telefono,residencia,correo_electronico,hora_apertura,hora_cierre)
                    indice = lista_medicos.index(medico) 
                    lista_medicos[indice] = nueva_tupla
                if opcion == "C":

                    pass
        if not encontrado:
            print ("EL MEDICO NO ESTA REGISTRADO, NO SE PUEDE MODIFICAR")
            continue
        

def eliminar_medico():
    global lista_medicos, citas
    while True:
        dato = input("Identificación del médico (C para cancelar): ").upper()
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
                print("Identificación del médico: ",medico[0])
                print("Nombre: ",medico[1])
                print("Apellido 1: ",medico[2])
                print("Apellido 2: ",medico[3])
                print("Teléfono: ",medico[4])
                print("Lugar de residencia: ",medico[5])
                print("Correo electrónico: ",medico[6])
                print("Hora de apertura: ",medico[7])
                print("Hora de cierre: ",medico[8])
                
                opcion = input("OPCION C-CANCELAR A-ACEPTAR ").upper()
                if opcion == "A":
                    #falta verificar si tiene citas asociadas 
                    opcion2 = input("CONFIRMA LA ELIMINACIÓN (SI/NO)").upper()
                    if opcion2 == "SI":
                        tiene_cita = False
                        for cita in citas:
                            if cita[0] == id_medico:
                                for horario in cita[1]:
                                     if horario [1] != 0:
                                         tiene_cita = True 
                                         break
                                if tiene_cita == True:
                                    print ("ESTE MÉDICO TIENE CITAS ASOCIADAS, NO SE PUEDE ELIMINAR." )
                                else:
                                    lista_medicos.remove(medico)
                    if opcion2 == "NO":
                        pass 
                    
                if opcion == "C":
                    pass
                break                        
        
        if not encontrado:
            print("EL MÉDICO NO ESTA REGISTRADO, NO SE PUEDE ELIMINAR" )
            continue
    
def registrar_pacientes():
    print ("         CLINICA MEDICA       ")
    print ("       REGISTRAR PACIENTES   ")

    while True:
        print("1. Agregar pacientes")
        print("2. Consultar pacientes")
        print("3. Modificar pacientes")
        print("4. Eliminar pacientes")
        print("5. Fin")
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
            case 5:
                break
            case _:
                print("Opcion invalida")
                continue



def agregar_paciente():
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
            numero_telefono = -1 
        
        if len(str(numero_telefono)) == 8:
                break
        else:
            print("El numero de telefono debe tener 8 digitos exactos. ")
            continue

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
            print("Correo inválido. Debe contener '@' y '.'  Ejemplo: nombre@dominio.com")
            continue 
    

    pacientes = (id_paciente,nombre,apellido1,apellido2,numero_telefono,lugar_residencia,correo_electronico)
    print ("    REGISTRAR PACIENTES   ")
    print ("    AGREGAR PACIENTE     ")
    print("Identificación del paciente: ",id_paciente)
    print("Nombre: ",nombre)
    print("Apellido 1: ",apellido1)
    print("Apellido 2: ",apellido2)
    print("Teléfono: ",numero_telefono)
    print("Lugar de residencia: ",lugar_residencia)
    print("Correo electrónico: ",correo_electronico)
    opcion_final = input("OPCION C-CANCELAR A-ACEPTAR").upper()
    if opcion_final == "A":
        lista_pacientes.append(pacientes)
    elif opcion_final == "C":
        return
    else:
        print("Opción inválida")

def consultar_paciente():
    global lista_pacientes 

    print ("    REGISTRAR PACIENTES   ")
    print ("    CONSULTAR PACIENTE    ") 
    while True:
        dato = input("Identificación del paciente (C para cancelar): ").upper()
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
               print("Identificación del paciente: ",paciente[0])
               print("Nombre: ",paciente[1])
               print("Apellido 1: ",paciente[2])
               print("Apellido 2: ",paciente[3])
               print("Teléfono: ",paciente[4])
               print("Lugar de residencia: ",paciente[5])
               print("Correo electrónico: ",paciente[6])
               break 

        if not encontrado:
            print ("EL PACIENTE NO ESTA REGISTRADO, NO SE PUEDE CONSULTAR")
            continue
        else:
            input("OPCION A-ACEPTAR ")


def modificar_paciente():
    global lista_pacientes
    print ("    REGISTRAR PACIENTES   ")
    print ("    MODIFICAR PACIENTES    ")
    while True:
        dato = input("Identificación del paciente (C para cancelar): ").upper()
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
                nuevo_nombre = input("    MODIFICAR: ")
                if nuevo_nombre == "":
                    nuevo_nombre = paciente[1]

                print(f"Apellido 1: {paciente[2]}")
                nuevo_apellido1 = input("    MODIFICAR: ")
                if nuevo_apellido1 == "":
                    nuevo_apellido1 = paciente[2]

                print(f"Apellido 2: {paciente[3]}")
                nuevo_apellido2 = input("    MODIFICAR: ")
                if nuevo_apellido2 == "":
                    nuevo_apellido2 = paciente[3]

                print(f"Teléfono: {paciente[4]}")
                telefono = input("    MODIFICAR: ")
                if telefono == "":
                    telefono = paciente[4]

                print(f"Lugar de residencia: {paciente[5]}")
                residencia = input("    MODIFICAR: ")
                if residencia == "":
                    residencia = paciente[5]

                print(f"Correo electrónico: {paciente[6]}")
                correo_electronico = input("    MODIFICAR: ")
                if correo_electronico == "":
                    correo_electronico = paciente[6]

                opcion = input ("OPCION C-CANCELAR A-ACEPTAR ")
                if opcion == "A":
                    nueva_tupla = (id_paciente,nuevo_nombre,nuevo_apellido1,nuevo_apellido2,telefono,residencia,correo_electronico)
                    indice = lista_pacientes.index(paciente) 
                    lista_pacientes[indice] = nueva_tupla
                if opcion == "C":

                    pass
                break
        if not encontrado:
            print ("EL PACIENTE NO ESTA REGISTRADO, NO SE PUEDE MODIFICAR")
            continue



def eliminar_paciente():
    global lista_pacientes, citas
    while True:
        dato = input("Identificación del paciente (C para cancelar): ").upper()
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
                print("Identificación del paciente: ",paciente[0])
                print("Nombre: ",paciente[1])
                print("Apellido 1: ",paciente[2])
                print("Apellido 2: ",paciente[3])
                print("Teléfono: ",paciente[4])
                print("Lugar de residencia: ",paciente[5])
                print("Correo electrónico: ",paciente[6])
                
                opcion = input("OPCION C-CANCELAR A-ACEPTAR ").upper()
                if opcion == "A":
                    #falta verificar si tiene citas asociadas 
                    opcion2 = input("CONFIRMA LA ELIMINACIÓN (SI/NO)").upper()
                    if opcion2 == "SI":
                        tiene_cita = False
                        for cita in citas:
                                for horario in cita[1]:
                                     if horario [1] == id_paciente:
                                         tiene_cita = True 
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
    global citas,lista_medicos,hora_de_apertura,hora_de_cierre,duracion_en_minutos
    if len(citas) > 0:
        print("NO SE PUEDE CREAR LA LISTA DE CITAS DEL DÍA DEBIDO A QUE HAY CITAS AGENDADAS. PARA CREAR LA LISTA PRIMERO DEBE CANCELAR ESAS CITAS. PUEDE EMITIR UN INFORME DE CITAS QUE LE SIRVA DE REFERENCIA PARA LUEGO HACER ESA CANCELACIÓN.")
        return 

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
