
#variables locales
hora_de_apertura = 0 
hora_de_cierre = 0 
duracion_en_minutos= 0
citas = []

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
                print(configuracion())
            case 2:
                print(registrar_medicos())
            case 3:
                print(registrar_pacientes())
            case 4:
                print(crear_lista_de_citas_dia())
            case 5:
                print(pedir_citas())
            case 6:
                print(informes())
            case 7:
                print(ayuda())
            case 8:
                print(acerca_de())
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



