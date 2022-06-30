""" Ingresar el nombre del archivo csv (o hardcodearlo)
Ingresar el DNI del cliente
Elegir la salida del "reporte" (pantalla o csv)
Filtros:
	Elegir el tipo de cheque (emitido o depositado)
	Elegir el estado del cheque (Pendiente, Aprobado, Rechazado) (Opcional)
	Elegir un rango de fecha (Opcional)
Si en un reporte, se repite un número de cheque, informar el error en pantalla
Si la salida es pantalla se imprime todo en pantalla
Si la salida es csv se exporta un archivo que:
	Nombre = <DNI><TIMESTAMPS ACTUAL>.csv
	Se exporta fechaorigen, fechapago, valor y cuenta(contraria al DNI).
Si no se recibe el estado del cheque imprimir sin filtro de estado """

import csv
import datetime

#Inicialización de variables
#Objeto con las entradas del usuario
datos = {
    "archivo_lectura": "cheques.csv",
    "dni": 00000000,
    "salida": 0,
    "tipo": 0,
    "estado": 0,
    "fecha_inicio": 0000000000,
    "fecha_fin": 0000000000
}
cheques = []                    #Array de diccionarios con los cheques leídos del archivo csv
cheques_salida = []             #Array con los cheques filtrados

#Lee el archivo csv especificado en datos["archivo_lectura"] y guarda sus datos como un diccionario en el array cheques
def leerCSV():
    with open(datos["archivo_lectura"], "r", newline="") as archivo:   #Abre el archivo (se cierra automáticamente)
        archivo_csv = csv.DictReader(archivo)               #Al omitir fieldnames utiliza como campos la primera fila del csv
        for diccionario in archivo_csv:                     #Copia fila por fila al array
            if diccionario != []:                           #Verifica que la fila no esté vacía
                cheques.append(diccionario)                  #Agrega el diccionario de la fila al array

#Busca en el array cheques el documento ingresado, si lo encuentra lo guarda en cheques_salida
def buscarChequesPorDNI():
    aux = 0
    for cheque in cheques:
        if cheque["DNI"] == datos["dni"]:                   #Si encuentra el cheque buscado
            cheques_salida.append(cheque)                   #Lo agrega al array
            aux = 1
    if aux == 0:                                            #Si no encontró ningún cheque
        print("No se encontraron cheques con ese documento.")
    return aux

#Cuenta la cantidad de veces que aparece un número de cheque para un DNI, si se repite informa el error
def validarRepetidos():
    aux = 0
    numeros_cheque = []             #Array para guardar los números de cheque
    for cheque in cheques_salida:
        numeros_cheque.append(cheque["NroCheque"])
    for numero in numeros_cheque:
        if numeros_cheque.count(numero) != 1:       #Si se repite algún cheque informa el error (para todos los repetidos)
            print(f"Error. El nº de cheque {numero} se encuentra repetido")
            aux = 1
    return aux

#Filtra los cheques guardados en cheques_salida por el tipo
def filtrarChequesPorTipo():
    for cheque in reversed(cheques_salida):    #Recorre en orden inverso porque sino se generan conflictos de índice (Borra uno -> saltea el siguiente (porque se desplaza))
        if datos["tipo"] == "1" and cheque["Tipo"] != "EMITIDO":   #Si el filtro es EMITIDO y el cheque no lo es              
            cheques_salida.remove(cheque)                         #Elimina el cheque del array
        elif datos["tipo"] == "2" and cheque["Tipo"] != "DEPOSITADO": #Si el filtro es DEPOSITADO y el cheque no lo es
            cheques_salida.remove(cheque)                             #Elimina el cheque del array

#Filtra los cheques guardados en cheques_salida por el estado
def filtrarChequesPorEstado():
    if 1 <= datos["estado"] <= 3:                           #Si se eligió una opción de filtro (sino no hace nada)
        for cheque in reversed(cheques_salida):
            if datos["estado"] == 1 and cheque["Estado"] != "PENDIENTE":   #Si el filtro es PENDIENTE y el cheque no lo es              
                cheques_salida.remove(cheque)
            elif datos["estado"] == 2 and cheque["Estado"] != "APROBADO":  #Si el filtro es APROBADO y el cheque no lo es
                cheques_salida.remove(cheque)  
            elif datos["estado"] == 3 and cheque["Estado"] != "RECHAZADO": #Si el filtro es RECHAZADO y el cheque no lo es
                cheques_salida.remove(cheque) 

def filtrarChequesPorFechas():
    if datos["fecha_inicio"] != "":
        try:
            fecha_inicio = datetime.datetime.strptime(datos["fecha_inicio"], "%d/%m/%Y")    #Conversión del string ingresado
        except ValueError:
            print("No ha ingresado una fecha de inicio correcta.")
        else:
            for cheque in reversed(cheques_salida):
                fecha_origen = datetime.datetime.fromtimestamp(int(cheque["FechaOrigen"]))  #Conversión del string leido
                if fecha_origen < fecha_inicio:     #Si la fecha de origen es menor al inicio del filtro
                    cheques_salida.remove(cheque)   #Se elimina el cheque
    if datos["fecha_fin"] != "":
        try:
            fecha_fin = datetime.datetime.strptime(datos["fecha_fin"], "%d/%m/%Y")    #Conversión del string ingresado
        except ValueError:
            print("No ha ingresado una fecha de fin correcta.")
        else:
            for cheque in reversed(cheques_salida):
                fecha_origen = datetime.datetime.fromtimestamp(int(cheque["FechaOrigen"]))  #Conversión del string leido
                if fecha_origen > fecha_fin:        #Si la fecha de origen es mayor al fin del filtro
                    cheques_salida.remove(cheque)   #Se elimina el cheque

#Secuencia de validación y filtración de los cheques (ante cualquier error retorna un 1)
def filtrarCheques():
    leerCSV()
    if buscarChequesPorDNI() == 1:                          #Validación que encontró al menos un cheque
        if validarRepetidos() == 0:                         #Validación que no se repitan cheques
            filtrarChequesPorTipo()
            filtrarChequesPorEstado()
            filtrarChequesPorFechas()
        else:
            return 1
    else:
        return 1

#Impresión en pantalla de todos los datos de los cheques filtrados
def salidaPantalla():
    print("Documento del cliente: ", datos["dni"])
    if len(cheques_salida) > 0:
        for cheque in cheques_salida:
            fecha_origen = datetime.datetime.fromtimestamp(int(cheque["FechaOrigen"]))  #Formato de fechas para mejor legibilidad/compresión
            fecha_pago = datetime.datetime.fromtimestamp(int(cheque["FechaPago"]))
            print(f"""Número de cheque: {cheque["NroCheque"]}
                    \tCódigo del Banco: {cheque["CodigoBanco"]}
                    \tCódigo de la Sucursal: {cheque["CodigoSucurusal"]}
                    \tNúmero de la cuenta origen: {cheque["NumeroCuentaOrigen"]}
                    \tNúmero de la cuenta destino: {cheque["NumeroCuentaDestino"]}
                    \tImporte del cheque: ${cheque["Valor"]}
                    \tFecha de origen: {fecha_origen}
                    \tFecha de pago: {fecha_pago}
                    \tTipo de cheque: {cheque["Tipo"]}
                    \tEstado del cheque: {cheque["Estado"]}""")
    else:
        print("No se pudieron obtener cheques. Por favor revise los filtros.")

#Generación de un archivo csv con los datos solicitados
def salidaCSV():
    if len(cheques_salida) > 0:
        dni = datos["dni"]
        timestamp = int(datetime.datetime.now().timestamp())
        #Nombre = <DNI><TIMESTAMPS ACTUAL>.csv
        documento_csv = f"{dni}_{timestamp}.csv"
        #Elimina los datos que no se solicitan
        for cheque in cheques_salida:
            cheque.pop("NroCheque")
            cheque.pop("CodigoBanco")
            cheque.pop("CodigoSucurusal")
            cheque.pop("DNI")
            cheque.pop("Tipo")
            cheque.pop("Estado")
        campos = cheques_salida[0].keys()              #Lee las claves del primer diccionario del array
        with open(documento_csv, "w", newline="") as archivo:          
            archivo_csv = csv.DictWriter(archivo, fieldnames=campos)
            archivo_csv.writeheader()                                 #Escribe el encabezado  
            archivo_csv.writerows(cheques_salida)                     #Escribe las filas
    else:
        print("No se pudieron obtener cheques. Por favor revise los filtros.")

#Secuencia de salida según lo especificado
def salida():
    if datos["salida"] == "1":              #Impresión en pantalla
        salidaPantalla()
    elif datos["salida"] == "2":
        salidaCSV()

#Ingreso de datos (validación de los obligatorios)
def ingresarDatos():
    # datos["archivo_lectura"] = input("Ingrese el archivo de cheques a leer: ")
    datos["dni"] = input("Ingrese el DNI del cliente: ")
    while datos["dni"] < "0" and datos["dni"] > "99999999":
        datos["dni"] = input("Error. Reingrese el número de documento: ")
    datos["salida"] = input("Seleccione método de salida:\n\t1-Pantalla\n\t2-Archivo CSV\n")
    while datos["salida"] != "1" and datos["salida"] != "2":
        datos["salida"] = input("Error. Reingrese el método de salida: ")
    datos["tipo"] = input("Selecciones el filtro del tipo de cheque:\n\t1-Emitido\n\t2-Depositado\n")
    while datos["tipo"] != "1" and datos["tipo"] != "2":
        datos["tipo"] = input("Error. Reingrese el filtro de tipo: ")
    datos["estado"] = int(input("Seleccione el filtro de estado del cheque:\n\t1-Pendiente\n\t2-Aprobado\n\t3-Rechazado\n\t4-No filtrar\n"))
    datos["fecha_inicio"] = input("Ingrese la fecha de inicio del filtro en formato dd/mm/aaaa (opcional): ")
    datos["fecha_fin"] = input("Ingrese la fecha de fin del filtro en formato dd/mm/aaaa (opcional): ")

if __name__ == "__main__":
    print("Generar reporte de cheques:")
    ingresarDatos()                         #Ingreso de datos y filtros
    if filtrarCheques() != 1:               #Selección de los cheques filtrados
        salida()                            #Devolución de los datos en pantalla o por archivo