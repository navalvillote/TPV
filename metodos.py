import datetime
import random
import sys
import tkinter.messagebox as messagebox
import os
import io
import json
import locale
import pickle
import copy
import win32print
import win32ui
from cryptography.fernet import Fernet
from PIL import Image

clave = b'5-uvWBhTHRAk7Eq8wlzdnXZlLCZFj8rE44rUN49wztg='  #clave de encriptacion del archivo json

# funciones de las impresoras

def obtener_lista_impresoras():
    # Obtener una lista de impresoras instaladas
    printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)

    # Mostrar el nombre de cada impresora
    lista_impresoras = [impresora[2] for impresora in printers]
    return lista_impresoras

def abrir_caja_registradora(impresoras):
    # Obtener el nombre de la impresora predeterminada
    # impresora = win32print.GetDefaultPrinter()
    impresora = impresoras[0]
    #print(f"Usando la impresora: {impresora}")

    # Comando ESC/POS para abrir la caja registradora
    # Este comando puede variar según el modelo de la impresora
    comando_abrir_caja = b'\x1B\x70\x00\x19\xFA'

    # Enviar el comando directamente a la impresora
    hprinter = win32print.OpenPrinter(impresora)
    try:
        # Crear un trabajo de impresión
        hprinter_job = win32print.StartDocPrinter(hprinter, 1, ("Abrir caja registradora", None, "RAW"))
        win32print.StartPagePrinter(hprinter)
        win32print.WritePrinter(hprinter, comando_abrir_caja)
        win32print.EndPagePrinter(hprinter)
        win32print.EndDocPrinter(hprinter)
    finally:
        win32print.ClosePrinter(hprinter)

def imprimir_lineas_texto(lineas,impresora):
    # Obtener el nombre de la impresora predeterminada
    # impresora = win32print.GetDefaultPrinter()
    #print(f"Impresora predeterminada: {impresora}")

    # Crear un contexto de impresión
    hprinter = win32print.OpenPrinter(impresora)
    try:
        printer_info = win32print.GetPrinter(hprinter, 2)
        pdc = win32ui.CreateDC()
        pdc.CreatePrinterDC(printer_info['pPrinterName'])
        pdc.StartDoc("Impresión de varias líneas desde Python")
        pdc.StartPage()

        # Configurar las dimensiones y fuente
        fuente = win32ui.CreateFont({
            "name": "Consolas",
            "height": 37,
        })
        pdc.SelectObject(fuente)

        # Imprimir cada línea de texto
        x, y = 0, 0  # Coordenadas iniciales
        line_spacing = 40  # Espaciado entre líneas
        for linea in lineas:
            pdc.TextOut(x, y, linea)
            y += line_spacing  # Mover hacia abajo para la siguiente línea
        pdc.EndPage()
        pdc.EndDoc()
        pdc.DeleteDC()
    finally:
        win32print.ClosePrinter(hprinter)

def obtener_listado_lineas(texto):
    lista = texto.split('\n')
    for i,linea in enumerate(lista):
        if len(linea)<30:
            delante=''
            detras=''
            sw=-1
            for j in range(30-len(linea)):
                sw*=-1
                if sw==1:
                    delante +=' '
                else:
                    detras +=' '
            lista[i]=delante + linea + detras
    return lista

def recibos_mes(anual,mes=0):
    if mes == 0:
        mes = dato_fecha_actual('mes')
    return anual[mes-1]

def dato_fecha_actual(cual=''):
    match cual:
        case 'año':
            return datetime.date.today().year
        case 'mes':
            return datetime.date.today().month
        case 'dia':
            return datetime.date.today().day
        case _:
            return datetime.date.today()

def dias_mes(fecha):
    dia = datetime.timedelta(days=1)
    siguiente = fecha + dia
    while fecha.month == siguiente.month:
        fecha = fecha + dia
        siguiente = fecha + dia
    return fecha.day

def obtener_importes(recibos,fecha,tipo,pago):
    lista=[]
    if tipo == 'mes':
        inicio = datetime.date(fecha.year,fecha.month,1)
        fin = datetime.date(fecha.year,fecha.month,dias_mes(fecha))
    else:
        inicio = fecha
        fin =fecha
    for item in recibos:
        if item['estado']==pago:
            cuando,_ = item['fecha'].split(' - ')
            cuando = cuando.split('/')
            cuando = datetime.date(int(cuando[2]),int(cuando[1]),int(cuando[0]))
            if inicio <= cuando <= fin:
                for linea in item['pedido']:
                    cantidad, _, precio, _ = linea
                    importe = cantidad*float(precio)
                    lista.append(importe)
    return sum(lista)

# Funciones necesarias para el funcionamiento de la aplicación

def obtener_nombres_archivos_png(directorio): #Obtiene una lista con los nombres de los archivos PNG en un directorio, sin la extensión.
    nombres_archivos = []
    for archivo in os.listdir(directorio): #busca los archivos en el directorio
        if archivo.endswith(".png"): #le damos las condiciones de busqueda
            nombre, _ = os.path.splitext(archivo) #cogemos el nombre sin extension
            nombres_archivos.append(nombre) #lo añadimos a la lista de nombres
    return nombres_archivos #devolvemos la lista de nombres

def encriptar_desencriptar(encriptar,texto):
    fernet = Fernet(clave)
    if encriptar:
        texto = pickle.dumps(texto)
        texto = fernet.encrypt(texto)
    else:
        texto = fernet.decrypt(texto)
        texto = pickle.loads(texto)
    return texto

def crear_archivo_imagenes():
    fernet = Fernet(clave)
    lista = obtener_nombres_archivos_png('archivos')
    lista_imagenes=[]
    for imagen in lista:
        ruta = f'archivos/{imagen}.png'
        # Leer la imagen en binario
        with open(ruta, "rb") as image_file:
            imagen_binaria = image_file.read()
        # añadimos el nombre y la imagen a la lista
        lista_imagenes.append([imagen,imagen_binaria])
        #convertir la list en un objeto serializable
    lista_serializada=pickle.dumps(lista_imagenes)
    #encriptar la lista
    lista_encriptada=fernet.encrypt(lista_serializada)
    # Guardar los datos en el archivo
    with open('image.tpv', 'wb') as archivo:
        archivo.write(lista_encriptada)

#Carga una lista encriptada de un archivo.
def cargar_archivo_imagenes(imagenes):
    # Leer los datos del archivo
    with open('image.tpv', 'rb') as archivo:
        datos_encriptados = archivo.read()
    # Crear un objeto Fernet con la clave
    fernet = Fernet(clave)
    # Desencriptar los datos
    datos_serializados = fernet.decrypt(datos_encriptados)
    # Deserializar la lista
    lista = pickle.loads(datos_serializados)
    for nombre,valor in lista:
        imagen = Image.open(io.BytesIO(valor))
        imagen.filename=nombre
        imagenes.append(imagen)

def obtener_database(anio=0): #se obtiene el archivo de db de un año en concreto
    # Si anio == 0 obtenemos el año actual
    if anio==0:
        anio = dato_fecha_actual('año')
    archivo=f'anual.{anio}.tpv'
    return archivo

def guardar_anual_encriptado(anual,anio=0):
    fernet = Fernet(clave)
    ruta = obtener_database(anio)
    datos = json.dumps(anual).encode('utf-8')  # Convertir a formato JSON
    datos_encriptados = fernet.encrypt(datos)  # Encriptar datos
    with open(ruta, 'wb') as archivo:
        archivo.write(datos_encriptados)

def cargar_anual_encriptado(anio=0):
    fernet = Fernet(clave)
    ruta = obtener_database(anio)
    anual=[[],[],[],[],[],[],[],[],[],[],[],[]]
    if os.path.exists(ruta): #si existe el archivo
        with open(ruta, 'rb') as archivo:
            datos_encriptados = archivo.read() #lee el archivo
        datos_recibidos = fernet.decrypt(datos_encriptados).decode('utf-8')  # Desencriptar datos
        anual = json.loads(datos_recibidos)  # Convertir de JSON a datos
    return anual

# Guardar datos en un archivo JSON encriptado
def guardar_datos_encriptados(listas):
    fernet = Fernet(clave)
    datos = json.dumps(listas).encode('utf-8')  # Convertir a formato JSON
    datos_encriptados = fernet.encrypt(datos)  # Encriptar datos
    with open('data.tpv', 'wb') as archivo:
        archivo.write(datos_encriptados)

# Leer datos desde un archivo JSON encriptado
def cargar_datos_encriptados():
    fernet = Fernet(clave)
    ruta = 'data.tpv'
    listas=[]
    if os.path.exists(ruta): #si existe el archivo
        with open(ruta, 'rb') as archivo:
            datos_encriptados = archivo.read() #lee el archivo
        datos_recibidos = fernet.decrypt(datos_encriptados).decode('utf-8')  # Desencriptar datos
        listas = json.loads(datos_recibidos)  # Convertir de JSON a datos
    else: #si no existe, lo crea.
        guardar_datos_encriptados(listas)
    return listas

def apagar_equipo(): #funcion que sirve para apagar el equipo en window
    confirmacion = messagebox.askyesno("Confirmación", "¿Estás seguro que deseas apagar el equipo?")
    if confirmacion:
        os.system("shutdown /s /t 0")  # Comando para Windows

def reiniciar_equipo():  #funcion que sirve para reiniciar el equipo en windows
    confirmacion = messagebox.askyesno("Confirmación", "¿Estás seguro que deseas reiniciar el equipo?")
    if confirmacion:
        os.system("shutdown /r /t 0")  # Comando para Windows

def suspender_equipo(): #funcion que sirve para suspender el equipo en windows
    confirmacion = messagebox.askyesno("Confirmación", "¿Estás seguro que deseas suspender el equipo?")
    if confirmacion:
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")  # Comando para Windows

def salir(principal): #funcion que sirve para salir de la aplicacion mostrando o no un mensaje de confirmacion
    if messagebox.askyesno("Salir", "¿Estás seguro que quieres salir?"):
        principal.destroy()


def convertir_texto(texto,limite=14): #coloca el texto en lineas de un maximo de caracteres estipulados por el limite
    lineas=[]
    frase=''
    lista=texto.split() #convierte el texto en una lista
    for i in range(len(lista)): #recorre la lista
        frase+=lista[i] #va creando la frase a listar
        if i+1 > len(lista):
            lineas.append(frase) #mete cada frase en una lista de lineas
        elif i+1 == len(lista):
            lineas.append(frase) #mete cada frase en una lista de lineas
        else:
            if len(frase + ' ' + lista[i+1])>limite: #comprueba si con la siguiente palabra la frase tiene mas del limite de caracteres
                lineas.append(frase) #mete cada frase en una lista de lineas
                frase=''
            else:
                frase += ' '
    texto='\n'.join(lineas)
    return texto

def formatear_numero(tecla,numero):
    if tecla == 'Delete':  # si pulsamos la tecla de borrar
        if numero != '':  # eliminamos un numero
            num = float(numero)
            num = num * 100
            num = int(num / 10)
            num = num / 100
            if num == 0:
                numero = ''
            else:
                numero = f'{num:.2f}'  # formateamos en moneda
    else:
        if len(numero) < 8:  # controlamos que la cifra tenga menos de 10 caracteres
            if numero != '':  # añadimos un numero
                num = float(numero)
                num *= 10
                num = num + float(tecla)/100
                numero = f'{num:.2f}'  # formateamos en moneda'
            else:
                if tecla != '0':  # añadimos un numero
                    num = int(tecla)
                    num /= 100
                    numero = f'{num:.2f}'  # formateamos en moneda'
    return numero

def existe_en_lista(nombre,lista):
    for item in lista:
        if nombre==item:
            return True
    return False

