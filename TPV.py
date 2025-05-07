from objetos import *
from metodos import *


#Declaracion de variables globales

lista_productos = [] #lista con todos los productos del TPV
lista_recibos_mensuales = []   #lista de los recibos pagados de un mes
lista_recibos_anuales = [] #lista de todos los recivos del año por meses(enero=0...diciembre=11)
lista_clientes = [] #lista de todos los clientes
lista_recibos_impagados = [] #lista de los recibos impagados
lista_camareros = [] #lista de los empleados que atienden el bar
lista_impresoras = [] #lista de las impresoras usadas

lista_camareros_recibos=[] #lista de camareros que hay en los recibos
lista_tickets_dia=[] #lista con los recibos de un dia
diccionario_recibo = {'pedido': []} #diccionario que guarda los datos de un pedido

lista_marcos_productos = []  #lista con todos los marcos de los productos del panel principal
lista_marcos_pie_principal = [] #lista con todos los marcos del pie
lista_marcos_teclado_alfanumerico = []  #lista con todas las teclas del teclado virtual
lista_marcos_recibos_impagados=[] #lista con los marcos de los tickets impagados
lista_marcos_modo_producto=[]   #lista con los marcos del modo Producto
lista_marcos_modo_pendiente=[] #lista con los marcos del modo Pendiente
lista_marcos_modo_camarero=[] #Lista con los marcos del modo Camarero
lista_marcos_impagados_unir=[] #guarda los dos marcos de los recibos impagados a unir
lista_botones_pagos=[] #lista con todos los botones de las formas de pago
lista_marcos_fecha_calendario=[] #lista con los botones de dia mes año del calendario
lista_marcos_dias_calendario=[] #lista con los botones dia del calendario
lista_marcos_meses_calendario=[] #lista con los botones mes del calendario
lista_marcos_anios_calendario=[] #lista con los botones anio del calendario
lista_marcos_camareros=[] #Lista con botones de los los camareros

ventana_aplicacion = None  # Ventana de la aplicación
contenedor = None  # Panel contenedor
cont_prin = None  # Panel contenedor de la pantalla principal
titulo = None  # Panel contenedor del titulo de la pantalla principal
apagar = None #Boton de apagado
logotipo = None #Label logotipo
camarero_actual=None #Label con el nombre del camarero activo
camarero_anterior=None #Marco con el camarero anterior
camarero=None #Boton que sirve para seleccionar camareros
numericos = None  # Panel que contiene el teclado numerico y la pantalla principal
pantalla = None  # Label de la pantalla del teclado numerico de la pantalla principal
bebidas = None  # Panel contenedor de las bebidas de la pantalla principal
comidas = None   # Panel contenedor de las comidas de la pantalla principal
otros = None   # Panel contenedor de los otros productos de la pantalla principal
impago = None #Panel contenedor de los tickets pendientes de la pantalla principal
barman = None #Panel contenedor de los camareros de la pantalla principal
impresion = None  # Panel contenedor del ticket y los botones de impresion de la pantalla principal
ticket = None  #  Label de informacion del ticket en la pantalla principal
pie = None  # Panel contenedor de los botones de opciones de la pantalla principal
entrada = None #el contenedor de texto escrito con el teclado en el teclado virtual
volver = None # la tecla que envia la infomacion de vuelta en el teclado virtual
cont_sec = None #el contenedor del teclado virtual
cont_tec = None #contiene el teclado unicamente
ocul_tec = None #oculta el teclado
cont_sec_modos= None # el contendor de los modos del panel secundario
cont_producto = None #el contendor de los widges del modo Producto en el teclado virtual
cont_pendiente = None #el contenedor de los widges del modo Pendiente en le teclado virtual
cont_mesero = None #el contenedor de los widges del modo Camarero en le teclado virtual
info = None # el marco que contiene la informacion de las acciones
listado = None # listado de seleccion en el teclado virtual
mayusculas = True #nos dice si el teclado esta en mayusculas
modo = None # modo que nos dice que widges tenemos que cargar en el teclado virtual
cont_ter = None  # Panel contenedor de la pantalla principal
cont_calista = None #contenedor del calendario y de la lista
cont_calendario = None  # Panel contenedor del calendario del contenedor terciario
cont_impresion = None # Panel que contiene la zona de impresion
cont_dia = None  # Panel contenedor de los dias del calendario del contenedor terciario
cont_mes = None  # Panel contenedor de los meses del calendario del contenedor terciario
cont_anio = None # Panel contenedor de los años del calendario del contenedor terciario
info_calendario = None # Marco de información del calendario
cont_bot_pie = None #Contenedor botonera del pie del calendario
cont_bot_cabeza = None #Contenedor botonera de la cabeza del calendario
fechado = None # Pantalla que mostrara la fecha del calendario del contenedor terciario
imprimir = None # Boton que se usa para imprimir un ticket del contenedor terciario
info_iva = None # texto informativo del impuesto_iva
ticket_calendario = None # El ticket que se muestra en la pantalla del calendario
listado_ticket = None # Crea el listado de los tickets en la pantalla del calendario
comodin = None # Crea el boton comodin del terciario
boton_totales = None #Crea el botón que muestra el ticket de los totales

cont_sec_password=None # el contenedor del password del panel secundario
password_mensaje = None #guarda los mensages de acierto o error
password_info = None # Etiqueta informativa del password
password_label = None # Etiqueta tipo de password
password_set = None #Entrada para gestionar los password situada arriba
password_send = None #Boton para chequear la contraseña
password_change = None #Boton para cambiar la contraseña

password = '' #Variable que guarda el password de la aplicacion
administrador= '857281478'
cabecera_ticket='Bar Robledo - BR2010'
impuesto_iva=21
incremento_decremento = None  #valor unico 1 o -1 para incrementar o decrementar
escritura = ''  #variable que guarda el modo de escritura en el teclado virtual
espacio = False
totales=(
    ('Caja Total Diaria','día'),
    ('Caja Total Mensual','mes'),
    ('Caja Mensual por Día','día a día'),
    ('Caja Mensual en Efectivo','efectivo'),
    ('Caja Mensual con Tarjeta','tarjeta')
        )



def cargar_listado_impresoras():
    global listado_ticket
    listado_ticket.delete(0, END) #se limpia la lista
    # Llamada a la función
    printers = obtener_lista_impresoras()
    for impresora in printers:
        listado_ticket.insert(END, impresora)  # añade la informacion a la lista

def generador_consumiciones():
    carta = {
        "Bebida":{
            "Caña": 1.3,
            "Jarra de Cerveza": 3.5,
            "Tinto de verano": 1.8,
            "Copa de vino": 1.3,
            "Vermut": 2.5,
            "Copa Nacional": 3.5,
            "Copa Importación": 4.5,
            "Refresco": 1.8,
            "Zumo natural": 2.5,
            "Agua con gas": 1.5,
            "Café solo": 1.2,
            "Café con leche": 1.5,
            "Té": 1.5,
            "Batido": 2,
            "Botellin": 1.3,
            "Tercio":2
            },
        "Comida":{
            "Patatas bravas": 6,
            "Croquetas caseras": 7,
            "Jamón ibérico": 10,
            "Tabla de queso": 9,
            "Tortilla de patatas": 6,
            "Bocadillos": 4,
            "Calamares a la romana": 8,
            "Alitas de pollo": 7,
            "Nachos con queso": 6,
            "Ensalada mixta": 6,
            "Hamburguesas": 7,
            "Pizza": 9
            },
        "Otros":{
            "Mechero":1.5,
            "Navaja":10
            }
    }
    for familia,consumicion in carta.items():
        for nombre,precio in consumicion.items():
            producto = {'nombre': nombre, 'precio': precio, 'familia': familia}
            lista_productos.append(producto)


def generador_automatico_tickets(anio):
    gen_anual=[]
    num_prod=len(lista_productos)
    for c_mes in range(1,13):
        gen_recibos = []
        fecha = datetime.date(anio,c_mes,1)
        num_dias = dias_mes(fecha)
        for c_dia in range(1,num_dias+1): # i guarda los dias del mes
            for c_hora in range(24): # j guarda las horas del dia
                if c_hora <=2 or c_hora>=9:
                    for c_min in range (60):
                        resultado = random.randint(1,9) # 1 se añade minuto,!=1 se desestima
                        if resultado==1:
                            pedido=[]
                            for c_pedidos in range(random.randint(1,3)): #k guarda la cantidad de pedidos
                                pos=-1
                                while pos<0:
                                    pos = random.randint(0,num_prod-1) # un producto al azar que sea Bebida
                                    if lista_productos[pos]['familia']!='Bebida':
                                        pos=-1
                                consumicion=[random.randint(1,2), #una cantidad aleatoria del mismo
                                             lista_productos[pos]['nombre'],
                                             lista_productos[pos]['precio'],
                                             lista_productos[pos]['familia']]
                                pedido.append(copy.deepcopy(consumicion)) #lo añadimos al pedido
                            diccionario_recibo['pedido']=pedido[:]
                            resultado = random.randint(0,1) # 1 tarjeta, 0 efectivo
                            if resultado==0:
                                diccionario_recibo['nombre']='Pagado efectivo'
                                diccionario_recibo['estado']='efectivo'
                            else:
                                diccionario_recibo['nombre']='Pagado tarjeta'
                                diccionario_recibo['estado']='tarjeta'
                            fecha_ticket=datetime.datetime(fecha.year,fecha.month,c_dia,c_hora,c_min,random.randint(0,59))
                            fecha_ticket=fecha_ticket.strftime('%d/%m/%Y - %H:%M:%S')
                            diccionario_recibo['fecha']=fecha_ticket
                            resultado = random.randint(0, 1)  # 1 impreso:True, 0 impreso:False
                            if resultado == 0:
                                diccionario_recibo['impreso'] = False
                            else:
                                diccionario_recibo['impreso'] = True
                            resultado = random.randint(0,len(lista_camareros)-1)
                            diccionario_recibo['camarero'] = lista_camareros [resultado]
                            gen_recibos.append(copy.deepcopy(diccionario_recibo))
        gen_anual.append(copy.deepcopy(gen_recibos))
    guardar_anual_encriptado(gen_anual,anio)

# Creamos el contenedor terciario del Calendario

def crear_cont_ter(): # Creamos el contenedor de todos los widges principales
    global cont_ter
    cont_ter = contenedor.crear_panel(dimensiones[0],dimensiones[1],'gray82')
    cont_ter.colocar_objeto(0, 0)
    crear_cont_impresion()
    crear_cont_calista()
    crear_cont_bot_pie()
    crear_cont_bot_cabeza()

def crear_cont_calendario():  # Creamos el contenedor de todos los widges principales
    global cont_calendario
    global info_calendario
    cont_calendario = cont_calista.crear_panel(500, 603, 'gray22')
    cont_calendario.colocar_objeto(0, 0)
    info_calendario = cont_calendario.crear_etiqueta('', 14, 'gray92', 'gray32',49)  # etiqueta informativa
    info_calendario.colocar_objeto(2, 555)

    crear_dia_mes_anio()
    crear_cont_anio()
    crear_cont_mes()
    crear_cont_dia()

def crear_cont_calista():  # creamos el panel que contiene las el calendario y la lista
    global cont_calista
    cont_calista = cont_ter.crear_panel(dimensiones[0] - 232, dimensiones[1] - 164, 'gray82')
    cont_calista.colocar_objeto(5, 82)
    crear_cont_calendario()
    crear_listado_ticket()

def on_click_tecla_dia(event): #actuaciones al evento al pulsar una tecla del teclado del panel principal
    event.widget.invertir_colores()
    cont_dia.tkraise()

def off_click_tecla_dia(event):  #actuaciones al evento al soltar una tecla del teclado del panel
    event.widget.invertir_colores()

def actualizar_dias(): #elimina los marcos existentes de los dias y los crea ya actualizados
    for dia in lista_marcos_dias_calendario:
        dia.destroy() #destruye los marcos existentes
    lista_marcos_dias_calendario.clear()
    crear_dias(fechado.title) #los vuelve a crear ya actualizados

def cambiar_fechado(fecha):
    global lista_recibos_mensuales
    if comodin.title!='impresoras' and modo=='Pendiente':
        comodin.title = 'impresoras'
        comodin.cambiar_texto('Asignar\nImpresoras')
        info_calendario.cambiar_texto('')
        listado_ticket.delete(0, END)  # se limpia la lista
    fechado.title=fecha
    fechado.cambiar_texto(fechado.title.strftime('%d/%m/%Y'))
    dia = fechado.title.strftime('%A')
    dia = f'{dia[:3].upper()}, {str(fechado.title.day).zfill(2)}'
    lista_marcos_fecha_calendario[0].title=fechado.title.day
    lista_marcos_fecha_calendario[0].cambiar_texto(dia)
    actualizar_dias()
    lista_recibos_mensuales=recibos_mes(lista_recibos_anuales,fecha.month)
    cargar_listado_ticket()
    cont_dia.tkraise()
    ticket_calendario.cambiar_texto('')

def on_click_tecla_dias(event): #actuaciones al evento al pulsar una tecla del teclado del panel principal
    for dia in lista_marcos_dias_calendario:
        if dia.invertir:
            dia.invertir_colores()
    event.widget.invertir_colores()
    fecha = datetime.date(fechado.title.year, fechado.title.month, event.widget.title)
    cambiar_fechado(fecha)

def on_click_tecla_mes(event): #actuaciones al evento al pulsar una tecla del teclado del panel principal
    event.widget.invertir_colores()
    cont_mes.tkraise()

def off_click_tecla_mes(event):  #actuaciones al evento al soltar una tecla del teclado del panel
    event.widget.invertir_colores()

def on_click_tecla_meses(event): #actuaciones al evento al pulsar una tecla del teclado del panel principal
    for mes in lista_marcos_meses_calendario:
        if not mes.invertir:
            mes.invertir_colores()
    event.widget.invertir_colores()
    fecha = datetime.date(fechado.title.year, event.widget.title, 1)
    n_dias=dias_mes(fecha)
    if fechado.title.day > n_dias:
        fecha = datetime.date(fechado.title.year, event.widget.title, n_dias)
    else:
        fecha = datetime.date(fechado.title.year, event.widget.title, fechado.title.day)
    lista_marcos_fecha_calendario[1].title = fecha.month
    lista_marcos_fecha_calendario[1].cambiar_texto(fecha.strftime('%B').upper())

    cambiar_fechado(fecha)

def on_click_tecla_entre_anios(event): #actuaciones al evento al pulsar una tecla del teclado del panel principal
    event.widget.invertir_colores()
    titulo_evento = event.widget.title
    cual = titulo_evento - 9
    for i in range (2,17):
        if lista_marcos_anios_calendario[i].invertir:
            lista_marcos_anios_calendario[i].invertir_colores()
        lista_marcos_anios_calendario[i].title=i+cual
        lista_marcos_anios_calendario[i].cambiar_texto(i+cual)
        if lista_marcos_anios_calendario[i].title==fechado.title.year:
            lista_marcos_anios_calendario[i].invertir_colores()
    lista_marcos_anios_calendario[0].title=titulo_evento-15
    lista_marcos_anios_calendario[0].cambiar_texto(f'{lista_marcos_anios_calendario[0].title - 7} - {lista_marcos_anios_calendario[0].title + 7}')
    lista_marcos_anios_calendario[1].title=titulo_evento+15
    lista_marcos_anios_calendario[1].cambiar_texto(f'{lista_marcos_anios_calendario[1].title - 7} - {lista_marcos_anios_calendario[1].title + 7}')

def off_click_tecla_entre_anios(event):  #actuaciones al evento al soltar una tecla del teclado del panel
    event.widget.invertir_colores()

def on_click_tecla_anios(event): #actuaciones al evento al pulsar una tecla del teclado del panel principal
    global lista_recibos_anuales
    for i in range (2,17):
        if lista_marcos_anios_calendario[i].invertir:
            lista_marcos_anios_calendario[i].invertir_colores()
    event.widget.invertir_colores()
    fecha = datetime.date(event.widget.title, fechado.title.month, fechado.title.day)
    lista_marcos_fecha_calendario[2].title = fecha.year
    lista_marcos_fecha_calendario[2].cambiar_texto(fecha.year)
    lista_recibos_anuales=cargar_anual_encriptado(event.widget.title)
    cambiar_fechado(fecha)

def on_click_tecla_anio(event): #actuaciones al evento al pulsar una tecla del teclado del panel principal
    event.widget.invertir_colores()
    cont_anio.tkraise()

def off_click_tecla_anio(event):  #actuaciones al evento al soltar una tecla del teclado del panel
    event.widget.invertir_colores()

def inicializar_calendario():
    global lista_recibos_anuales
    global lista_recibos_mensuales
    fechado.title=datetime.date.today()
    #inicializamos los años
    anio=fechado.title.year
    lista_recibos_anuales = cargar_anual_encriptado(anio)
    lista_recibos_mensuales=recibos_mes(lista_recibos_anuales,fechado.title.month)
    cual = anio - 9
    for i in range (2,17):
        if lista_marcos_anios_calendario[i].invertir:
            lista_marcos_anios_calendario[i].invertir_colores()
        lista_marcos_anios_calendario[i].title=i+cual
        lista_marcos_anios_calendario[i].cambiar_texto(i+cual)
        if lista_marcos_anios_calendario[i].title==fechado.title.year:
            lista_marcos_anios_calendario[i].invertir_colores()
    lista_marcos_anios_calendario[0].title=anio-15
    lista_marcos_anios_calendario[0].cambiar_texto(f'{lista_marcos_anios_calendario[0].title - 7} - {lista_marcos_anios_calendario[0].title + 7}')
    lista_marcos_anios_calendario[1].title=anio+15
    lista_marcos_anios_calendario[1].cambiar_texto(f'{lista_marcos_anios_calendario[1].title - 7} - {lista_marcos_anios_calendario[1].title + 7}')
    lista_marcos_fecha_calendario[2].title = fechado.title.year
    lista_marcos_fecha_calendario[2].cambiar_texto(fechado.title.year)
    #inicializamos los meses
    for mes in lista_marcos_meses_calendario:
        if not mes.invertir:
            mes.invertir_colores()
        if mes.title == fechado.title.month:
            mes.invertir_colores()
    lista_marcos_fecha_calendario[1].title = fechado.title.month
    lista_marcos_fecha_calendario[1].cambiar_texto(fechado.title.strftime('%B').upper())
    #inicializamos los dias
    for dia in lista_marcos_dias_calendario:
        if dia.invertir:
            dia.invertir_colores()
        if dia.title == fechado.title.day:
            dia.invertir_colores()

def crear_dia_mes_anio():
    x=5
    y=5
    dia=fechado.title.strftime('%A')
    dia=f'{dia[:3].upper()}, {str(fechado.title.day).zfill(2)}'
    tecla = cont_calendario.crear_marco(dia, fechado.title.day, 'tecla_doble', 20, cont_calendario.fondo)
    tecla.title='Calendario'
    tecla.colocar_objeto(x, y)
    tecla.bind("<Button-1>", on_click_tecla_dia) #obtenemos el evento al pulsar en la tecla
    tecla.bind("<ButtonRelease-1>", off_click_tecla_dia) #obtenemos el evento al soltar la tecla
    lista_marcos_fecha_calendario.append(tecla)
    x+=140
    mes = fechado.title.strftime('%B')
    tecla = cont_calendario.crear_marco(mes.upper(), mes, 'tecla_envio', 20, cont_calendario.fondo)
    tecla.colocar_objeto(x, y)
    tecla.bind("<Button-1>", on_click_tecla_mes) #obtenemos el evento al pulsar en la tecla
    tecla.bind("<ButtonRelease-1>", off_click_tecla_mes) #obtenemos el evento al soltar la tecla
    lista_marcos_fecha_calendario.append(tecla)
    x+=210
    tecla = cont_calendario.crear_marco(str(fechado.title.year), str(fechado.title.year), 'tecla_doble', 20, cont_calendario.fondo)
    tecla.colocar_objeto(x, y)
    tecla.bind("<Button-1>", on_click_tecla_anio) #obtenemos el evento al pulsar en la tecla
    tecla.bind("<ButtonRelease-1>", off_click_tecla_anio) #obtenemos el evento al soltar la tecla
    lista_marcos_fecha_calendario.append(tecla)

def crear_cont_dia(): # Creamos el contenedor de todos los widges principales
    global cont_dia
    dias_semana = ("LUN", "MAR", "MIE", "JUE", "VIE", "SAB", "DOM")
    cont_dia = cont_calendario.crear_panel(500,460,'gray22')
    cont_dia.colocar_objeto(0, 75)
    x=10
    y=5
    for dia in dias_semana:
        etiq = cont_dia.crear_etiqueta(dia, 12, 'SlateGray4', cont_dia.fondo, 6)  # etiqueta informativa
        etiq.colocar_objeto(x, y)
        x+=70
    crear_dias(fechado.title)

def crear_cont_mes(): # Creamos el contenedor de todos los widges principales
    global cont_mes
    cont_mes = cont_calendario.crear_panel(500,460,'gray22')
    cont_mes.colocar_objeto(0, 75)
    crear_meses()

def crear_cont_anio(): # Creamos el contenedor de todos los widges principales
    global cont_anio
    cont_anio = cont_calendario.crear_panel(500,460,'gray22')
    cont_anio.colocar_objeto(0, 75)
    crear_anios()

def crear_anios():
    contador=fechado.title.year - 15
    for x in range(2):

        posy = 5
        posx = x * 235 + 27
        tecla = cont_anio.crear_marco(f'{contador-7} - {contador+7}', contador, 'tecla_envio', 20, cont_anio.fondo)
        tecla.invertir_colores()
        tecla.colocar_objeto(posx, posy)
        contador=fechado.title.year + 15
        tecla.bind("<Button-1>", on_click_tecla_entre_anios)  # obtenemos el evento al pulsar en la tecla
        tecla.bind("<ButtonRelease-1>", off_click_tecla_entre_anios)  # obtenemos el evento al soltar la tecla
        lista_marcos_anios_calendario.append(tecla)

    contador = fechado.title.year - 7
    for y in range(5):
        posy = y * 75 + 83
        for x in range(3):
            posx = x * 157 + 22
            tecla = cont_anio.crear_marco(contador,contador, 'tecla_doble', 20, cont_anio.fondo)
            tecla.colocar_objeto(posx, posy)
            if tecla.title == fechado.title.year:
                tecla.invertir_colores()
            contador += 1
            tecla.bind("<Button-1>", on_click_tecla_anios)  # obtenemos el evento al pulsar en la tecla
            lista_marcos_anios_calendario.append(tecla)

def crear_meses():
    contador = 0
    for y in range(6):
        posy=y*75 + 8
        for x in range(2):
            fecha=datetime.date(fechado.title.year,contador+1,1)
            posx = x * 235 + 27
            tecla = cont_mes.crear_marco(fecha.strftime('%B'), contador+1, 'tecla_envio', 20, cont_mes.fondo)
            tecla.colocar_objeto(posx, posy)
            if tecla.title==fechado.title.month:
                tecla.invertir_colores()
            contador+=1
            lista_marcos_meses_calendario.append(tecla)
            tecla.bind("<Button-1>", on_click_tecla_meses)  # obtenemos el evento al pulsar en la tecla

def crear_dias(fecha): #creamos las teclas del teclado numerico
    contador=0
    fecha=datetime.date(fecha.year,fecha.month, 1)
    dia = fecha.weekday()
    mes = dias_mes(fecha)
    for y in range(6):
        posy=y*70+35
        for x in range(7):
            if dia <= contador < mes+dia:
                pintar=True
            else:
                pintar=False
            posx=x*70+5
            if pintar:
                tecla = cont_dia.crear_marco(str(contador-dia+1), contador-dia+1, 'tecla', 20,cont_dia.fondo)
                tecla.colocar_objeto(posx, posy)
                if int(fechado.title.day)==contador-dia+1:
                    tecla.invertir_colores()
                tecla.bind("<Button-1>", on_click_tecla_dias) #obtenemos el evento al pulsar en la tecla
                lista_marcos_dias_calendario.append(tecla)
            contador += 1

def generar_ticket(pedido): #genera la parte central del ticket, donde esta detallado el pedido
    lista=[]
    total=0
    texto=''
    if len(pedido)>0:
        for linea in pedido: #va recorriendo el pedido
            cantidad,nombre,precio,familia = linea
            suma=cantidad*float(precio)  # guarda la cantidad x importe de cada linea
            total+=suma #va sumando el total de cada linea
            suma=f'{suma:.2f}'
            num = 24 - (len(str(cantidad)) + len(nombre) + len(suma))
            lista.append(f'{cantidad} x {nombre}:{'.'*num}{suma}€') #formatea cada linea
        lista.append('-'*30)
        suma = total / (1 + impuesto_iva / 100)
        lista.append(f'Base imponible: {suma:.2f}€')  # añade la base imponible del ticket
        suma = total - suma
        lista.append(f'{impuesto_iva}% de IVA: {suma:.2f}€')  # añade el impuesto_iva del ticket
        lista.append(f'Total a pagar: {total:.2f}€')  # añade el total del ticket
        texto = '\n'.join(lista)  # lo convierte en un texto para mostrar en el ticket
    return texto

def actualizar_ticket(): #formatea el ticket para mostrarlo en pantallla
    texto=''
    texto += f'\n{'-' * 30}'  #30
    texto += f'\n{diccionario_recibo['nombre']}'
    texto += f'\n{diccionario_recibo['fecha']}'
    texto += f'\n{'-' * 30}\n'  #30
    texto += generar_ticket(diccionario_recibo['pedido']) #genera el corazon del ticket
    texto += f'\n{'-' * 30}'  #30
    texto += '\nGracias por su Visita!!!'
    texto += '\n.'
    return texto

def generar_ticket_total(tipo): #genera la parte central del ticket, donde esta detallado el pedido
    lista=[]
    total=0
    if tipo=='día' or tipo=='mes':
        importe = obtener_importes(lista_recibos_mensuales,fechado.title, tipo, 'efectivo')
        total += importe
        importe = f'{importe:.2f}'
        lista.append(f'Pagado en efectivo:{'.' * (10 - len(importe))}{importe}€')
        importe = obtener_importes(lista_recibos_mensuales,fechado.title, tipo, 'tarjeta')
        total += importe
        importe = f'{importe:.2f}'
        lista.append(f'Pagado con tarjeta:{'.' * (10 - len(importe))}{importe}€')
    else:
        for i in range(1, dias_mes(fechado.title) + 1):
            fecha = datetime.date(fechado.title.year, fechado.title.month, i)
            if tipo=='día a día':
                importe = obtener_importes(lista_recibos_mensuales,fecha, 'día', 'efectivo')
                importe += obtener_importes(lista_recibos_mensuales,fecha, 'día', 'tarjeta')
            else:
                importe = obtener_importes(lista_recibos_mensuales,fecha, tipo, tipo)
            total += importe
            importe = f'{importe:.2f}'
            fecha = fecha.strftime("%d/%m/%Y")
            lista.append(f'{fecha}:{'.' * (30 - len(importe) - len(fecha) - 2)}{importe}€')
    lista.append('-' * 30)
    importe=total / (1 + impuesto_iva/100)
    lista.append(f'Base imponible: {importe:.2f}€')  # añade la base imponible del ticket
    importe = total-importe
    lista.append(f'{impuesto_iva}% de IVA: {importe:.2f}€')  # añade el impuesto_iva del ticket
    lista.append(f'Total a pagar: {total:.2f}€')  # añade el total del ticket
    texto = '\n'.join(lista)  # lo convierte en un texto para mostrar en el ticket
    return texto

def actualizar_ticket_total(): #formatea el ticket para mostrarlo en pantalla
    texto=''
    texto += f'\n{'-' * 30}'  #30
    texto += f'\n{boton_totales.cget('text')}'
    if boton_totales.title=='día':
        texto += f'\n{fechado.title.strftime("%d de %B de %Y")}'
    else:
        texto += f'\n{fechado.title.strftime("%B de %Y")}'
    texto += f'\n{'-' * 30}\n'  #30
    texto += generar_ticket_total(boton_totales.title) #genera el corazon del ticket
    texto += f'\n{'-' * 30}'  #30
    texto += '\n.'
    return texto

def cargar_listado_ticket():
    global listado_ticket
    listado_ticket.delete(0, END) #se limpia la lista
    lista_tickets_dia.clear()
    for pagado in lista_recibos_mensuales:
        fecha,_=pagado['fecha'].split(' - ')
        if fecha == fechado.title.strftime('%d/%m/%Y'):
            lista_tickets_dia.append(pagado)
            listado_ticket.insert(END, pagado['fecha']) #añade la informacion a la lista

def obtener_seleccion_ticket(event):
    global diccionario_recibo
    seleccion = event.widget.curselection()  # Obtener la selección actual
    if seleccion:
        # Obtener el valor seleccionado
        #item = event.widget.get(seleccion[0])
        if comodin.title == 'principal':
            if lista_impresoras[0]!= event.widget.get(seleccion[0]):
                lista_impresoras[0] = event.widget.get(seleccion[0])
                guardar_datos()
        elif comodin.title == 'comanda':
            if lista_impresoras[1] != event.widget.get(seleccion[0]):
                lista_impresoras[1] = event.widget.get(seleccion[0])
                guardar_datos()
        else:
            diccionario_recibo=lista_tickets_dia[seleccion[0]]
            ticket_calendario.cambiar_texto(actualizar_ticket())

def crear_listado_ticket(): #creamos la lista en el teclado virtual
    global listado_ticket
    cont_list_tick = cont_calista.crear_panel(287, 604, 'black')
    cont_list_tick.expandir_panel()
    cont_list_tick.colocar_objeto(dimensiones[0]-cont_list_tick.ancho-cont_impresion.ancho-15, 0)
    listado_ticket=cont_list_tick.crear_lista(LEFT,BOTH)
    barra=cont_list_tick.crear_barra(RIGHT,Y)
    listado_ticket.sincronizar_lista(barra)
    barra.sincronizar_barra(listado_ticket)
    listado_ticket.bind("<<ListboxSelect>>", obtener_seleccion_ticket)
    cargar_listado_ticket()

def crear_cont_impresion(): #creamos el panel que contiene la impresion en el panel principal
    global cont_impresion
    cont_impresion = cont_ter.crear_panel(216, dimensiones[1]-10, 'gray94') #94
    cont_impresion.colocar_objeto(dimensiones[0] - cont_impresion.ancho - 5, 5)
    crear_fechado()
    crear_recibo_calendario()
    crear_imprimir()

def crear_recibo_calendario(): #creamos el label recibo del panel principal
    global ticket_calendario
    ticket_calendario = cont_impresion.crear_ticket(30,41,'')
    ticket_calendario.colocar_objeto(0,61)

def crear_fechado(): #creamos el label del la pantalla del teclado numerico
    global fechado
    hoy = datetime.date.today()
    fechado = cont_impresion.crear_marco(hoy.strftime('%d/%m/%Y'), hoy, 'pantalla', 26,cont_impresion.fondo)
    fechado.colocar_objeto(0, 0)

def on_click_imprimir(event): #actuaciones al evento al pulsar una tecla del teclado del panel principal
    event.widget.invertir_colores()
    lineas = obtener_listado_lineas(ticket_calendario.cget('text'))
    imprimir_lineas_texto(lineas,lista_impresoras[0])
    '''
    print(lineas)
    for linea in lineas:
        print(len(linea),linea)
    '''

def off_click_imprimir(event):  #actuaciones al evento al soltar una tecla del teclado del panel
    event.widget.invertir_colores()

def crear_imprimir():
    global imprimir
    imprimir = cont_impresion.crear_marco('Imprimir', 'imprimir', 'tecla_envio', 20, cont_impresion.fondo)
    imprimir.invertir_colores()
    imprimir.colocar_objeto(3, cont_impresion.alto-73)
    imprimir.bind("<Button-1>", on_click_imprimir) #obtenemos el evento al pulsar en la tecla
    imprimir.bind("<ButtonRelease-1>", off_click_imprimir) #obtenemos el evento al soltar la tecla

def crear_cont_bot_pie():  # Creamos el contenedor de todos los widges principales
    global cont_bot_pie
    cont_bot_pie = cont_ter.crear_panel(792, 75, 'gray82')
    cont_bot_pie.colocar_objeto(5, 688)
    crear_totales()

def crear_cont_bot_cabeza():
    global cont_bot_cabeza
    cont_bot_cabeza = cont_ter.crear_panel(792, 75, 'gray82')
    cont_bot_cabeza.colocar_objeto(5, 5)
    crear_iva()

def on_click_totales(event): #actuaciones al evento al pulsar una tecla del teclado del panel principal
    event.widget.invertir_colores()
    if comodin.title!='impresoras' and modo=='Pendiente':
        comodin.title = 'impresoras'
        comodin.cambiar_texto('Asignar\nImpresoras')
        info_calendario.cambiar_texto('')
        listado_ticket.delete(0, END)  # se limpia la lista
    ticket_calendario.cambiar_texto(actualizar_ticket_total())

def off_click_totales(event):  #actuaciones al evento al soltar una tecla del teclado del panel
    event.widget.invertir_colores()

def on_click_cambiar_totales(event): #actuaciones al evento al pulsar una tecla del teclado del panel principal
    event.widget.invertir_colores()
    for pos,boton in enumerate(totales):
        if boton[1]==boton_totales.title:
            break
    pos+=event.widget.title
    if pos<0:
        pos=len(totales)-1
    elif pos==len(totales):
        pos=0
    boton_totales.cambiar_texto(totales[pos][0])
    boton_totales.title=totales[pos][1]

def off_click_cambiar_totales(event):  #actuaciones al evento al soltar una tecla del teclado del panel
    event.widget.invertir_colores()

def crear_totales():
    global boton_totales
    x=110
    y=5
    boton = cont_bot_pie.crear_marco('<<', -1, 'tecla', 20, cont_bot_pie.fondo)
    boton.colocar_objeto(x,y)
    boton.bind("<Button-1>", on_click_cambiar_totales)  # obtenemos el evento al pulsar en la tecla
    boton.bind("<ButtonRelease-1>", off_click_cambiar_totales)  # obtenemos el evento al soltar la tecla
    x+=67
    boton_totales = cont_bot_pie.crear_marco(totales[0][0],totales[0][1], 'tecla_space', 20, cont_bot_pie.fondo)
    boton_totales.invertir_colores()
    boton_totales.colocar_objeto(x,y)
    boton_totales.bind("<Button-1>", on_click_totales)  # obtenemos el evento al pulsar en la tecla
    boton_totales.bind("<ButtonRelease-1>", off_click_totales)  # obtenemos el evento al soltar la tecla
    x+=416
    boton = cont_bot_pie.crear_marco('>>', 1, 'tecla', 20, cont_bot_pie.fondo)
    boton.colocar_objeto(x,y)
    boton.bind("<Button-1>", on_click_cambiar_totales)  # obtenemos el evento al pulsar en la tecla
    boton.bind("<ButtonRelease-1>", off_click_cambiar_totales)  # obtenemos el evento al soltar la tecla

def on_click_iva(event): #actuaciones al evento al pulsar una tecla del teclado del panel principal
    global impuesto_iva
    event.widget.invertir_colores()
    info_iva.title+=event.widget.title
    impuesto_iva=info_iva.title
    guardar_datos()
    info_iva.cambiar_texto(f'{impuesto_iva}% de IVA')

def off_click_iva(event):  #actuaciones al evento al soltar una tecla del teclado del panel
    event.widget.invertir_colores()

def on_click_atras(event): #actuaciones al evento al pulsar una tecla del teclado del panel principal
    global diccionario_recibo
    event.widget.invertir_colores()
    diccionario_recibo=copy.deepcopy(lista_marcos_modo_pendiente[0].title)
    lista_marcos_modo_pendiente[0].title='tickets'
    inicializar_calendario()
    cont_sec.tkraise()

def off_click_atras(event):  #actuaciones al evento al soltar una tecla del teclado del panel
    event.widget.invertir_colores()

def crear_iva():
    global info_iva
    global comodin
    x=0
    y=2
    boton = cont_bot_cabeza.crear_marco('-', -0.5, 'tecla', 20, cont_bot_cabeza.fondo)
    boton.colocar_objeto(x,y)
    boton.bind("<Button-1>", on_click_iva)  # obtenemos el evento al pulsar en la tecla
    boton.bind("<ButtonRelease-1>", off_click_iva)  # obtenemos el evento al soltar la tecla
    x+=67
    info_iva = cont_bot_cabeza.crear_marco(f'{impuesto_iva}% de IVA',impuesto_iva, 'tecla_envio', 20, cont_bot_cabeza.fondo)
    info_iva.invertir_colores()
    info_iva.colocar_objeto(x,y)
    x+=206
    boton = cont_bot_cabeza.crear_marco('+', 0.5, 'tecla', 20, cont_bot_cabeza.fondo)
    boton.colocar_objeto(x,y)
    boton.bind("<Button-1>", on_click_iva) #obtenemos el evento al pulsar en la tecla
    boton.bind("<ButtonRelease-1>", off_click_iva) #obtenemos el evento al soltar la tecla

    x += 160
    comodin = cont_bot_cabeza.crear_marco('', '', 'tecla_envio', 16, cont_bot_cabeza.fondo)
    comodin.colocar_objeto(x, y)
    comodin.bind("<Button-1>", on_click_comodin)  # obtenemos el evento al pulsar en la tecla
    comodin.bind("<ButtonRelease-1>", off_click_comodin)  # obtenemos el evento al soltar la tecla

    x += 210
    boton = cont_bot_cabeza.crear_marco('Volver', '', 'tecla_marco', 20, cont_bot_cabeza.fondo)
    boton.colocar_objeto(x, y)
    boton.invertir_colores()
    boton.bind("<Button-1>", on_click_atras)  # obtenemos el evento al pulsar en la tecla
    boton.bind("<ButtonRelease-1>", off_click_atras)  # obtenemos el evento al soltar la tecla

def buscar_camareros_recibo():
    for item in lista_recibos_mensuales:
        hay=False
        for cam in lista_camareros_recibos:
            if item['camarero']==cam:
                hay=True
                break
        if not hay:
            lista_camareros_recibos.append(item['camarero'])

def buscar_siguiente_camarero():
    idx=-1
    if len(lista_camareros_recibos)>0:
        for i,cam in enumerate(lista_camareros_recibos):
            if cam==comodin.title:
                if i==len(lista_camareros_recibos)-1:
                    idx=0
                else:
                    idx=i+1
                break
    return idx

def on_click_comodin(event): #actuaciones al evento al pulsar una tecla del teclado del panel principal
    event.widget.invertir_colores()
    if modo=='Pendiente':
        if event.widget.title=='principal':
            comodin.title = 'comanda'
            comodin.cambiar_texto('Impresora\nComandas')
            info_calendario.cambiar_texto(f'Comanda: {lista_impresoras[1]}')
        else:
            cargar_listado_impresoras()
            comodin.title = 'principal'
            comodin.cambiar_texto('Impresora\nPrincipal')
            info_calendario.cambiar_texto(f'Principal: {lista_impresoras[0]}')
    elif modo=='Camarero':
        idx = buscar_siguiente_camarero()
        if idx>=0:
            comodin.title = lista_camareros_recibos[idx]
            comodin.cambiar_texto(convertir_texto(lista_camareros_recibos[idx]))
            info_calendario.cambiar_texto(f'Tickets de: {lista_camareros_recibos[idx]}')

def off_click_comodin(event):  #actuaciones al evento al soltar una tecla del teclado del panel
    event.widget.invertir_colores()

# Funciones necesarias para el funcionamiento de la aplicación

# Guardar datos en un archivo JSON encriptado
def guardar_datos():
    guardar_datos_encriptados([lista_productos,lista_recibos_impagados,lista_clientes,lista_camareros,impuesto_iva,password,lista_impresoras])

# Leer datos desde un archivo JSON encriptado
def cargar_datos():
    global lista_productos
    global lista_clientes
    global lista_recibos_impagados
    global impuesto_iva
    global lista_camareros
    global password
    global lista_impresoras
    #carga la informacion el las listas
    listas=cargar_datos_encriptados()
    if listas:
        lista_productos=copy.deepcopy(listas[0])
        lista_recibos_impagados=copy.deepcopy(listas[1])
        lista_clientes=copy.deepcopy(listas[2])
        lista_camareros=copy.deepcopy(listas[3])
        impuesto_iva=copy.deepcopy(listas[4])
        password=copy.deepcopy(listas[5])
        lista_impresoras=copy.deepcopy(listas[6])

def guardar_anual():
    lista_recibos_anuales[dato_fecha_actual('mes')]=copy.deepcopy(lista_recibos_mensuales)
    guardar_anual_encriptado(lista_recibos_anuales)

def cargar_anual():
    global lista_recibos_anuales
    global lista_recibos_mensuales
    lista_recibos_anuales=cargar_anual_encriptado()
    lista_recibos_mensuales=recibos_mes(lista_recibos_anuales)

def crear_importe(tecla): #interpreta la lista de numeros y lo formatea en un string para salida en pantalla
    if diccionario_recibo['nombre']==cabecera_ticket:
        importe=pantalla.cget('text')[:-1] #elimina el simbolo € del final
        match tecla:
            case 'del': #si se pulsa la tecla borrar numero
                tecla='Delete'
                importe = formatear_numero(tecla,importe) #formateamos numero
            case 'ok': # si se pulsa la tecla ok, envia la informacion al ticket en formato numero.
                if importe != '':
                    completar_pedido(importe) # completamos el pedido
                    ticket.cambiar_texto(actualizar_ticket()) #actualizamos el ticket
                    importe='' #se queda vacio para borrar la pantalla
            case _:
                importe = formatear_numero(tecla,importe) #formateamos numero
        if importe != '':
            importe += '€' #agregamos el simbolo € al final
        pantalla.cambiar_texto(importe) #actualizamos la pantalla

def completar_pedido(consumicion): # funcion que va añadiendo o quitando productos al pedido
    lista=[] #lista que guarda la informacion de cada producto
    hay=False #si existe el producto en el pedido
    for i, producto in enumerate(diccionario_recibo['pedido']): #para todos los productos en el pedido
        if producto[1] == consumicion or (producto[1]=="Varios" and producto[2]==consumicion):
            #comprueba si el producto ya ha sido pedido o no
            diccionario_recibo['pedido'][i][0]+=incremento_decremento # se incrmenta o decrementa la cantidad
            if diccionario_recibo['pedido'][i][0]==0:  #si se decrementa al llegar a 0 se elimina
                del diccionario_recibo['pedido'][i]
            hay=True
            break
    if not hay: # si no habia anteriormente el producto en el pedido
        if incremento_decremento>0:
            hay=False #si existe el producto en la lista de productos
            for producto in lista_productos:
                if producto['nombre'] == consumicion:
                    lista=[1,producto['nombre'],producto['precio'],producto['familia']]  #si hay se agrega el producto
                    hay=True
                    break
            if not hay: #si no existe el producto (es porque se ha cogido el valor de la pantalla del teclado numerico)
                lista=[1,'Varios',consumicion,'Varios'] #se agrega como varios ya que consumicion es el precio
            diccionario_recibo['pedido'].append(lista) #se agrega la informcion al los pedidos del recibo.

# Creacion de un teclado virtual

def interpretar_teclado(texto):  #interpreta la tecla que ha sido pulsada
    global mayusculas
    escrito = entrada.cget("text")
    if texto=='Shift': # si se pulsa la tecla mayusculas
        for virtual in lista_marcos_teclado_alfanumerico: #para todas las teclas
            tecla = virtual.cget("text")
            if tecla.isalpha and len(tecla) == 1: #que sean una letra
                if mayusculas: #si estan en mayusculas
                    virtual.cambiar_texto(tecla.lower()) #se las pone en minuscula
                else: #si estan en minuscualas
                    virtual.cambiar_texto(tecla.upper()) #se las pone en mayusculas
        mayusculas = not mayusculas #se cambia la informacion de estado del teclado
    else:
        if texto =='Delete': #si se pulsa la tecla borrar
            escrito = escrito[:-1] #se elimina el ultimo caracter
            if len(escrito) == 0: #si se ha quedado la cadena vacia
                escrito = '' # se añade el espacio de inicio y se actualiza el valor de espacio
        elif texto=='Space': #si se pulsa la tecla de espacio
            if escrito != '':  #si la cadena no esta vacia
                if escrito[-1]!=' ': #si el ultimo caracter del texto no es un espacio
                    escrito += ' ' #se añade al texto un espacio
        else: # si la tecla pulsada es una letra
            escrito += texto # se añade el caracter de la tecla pulsada
        entrada.cambiar_texto(escrito) #se pone el nuevo texto en la entrada
    return escrito #devolvemos el texto por si se necesita

def controlar_saltos(): #controlador de escritura
    saltos=0
    no_espacios=0
    escrito = entrada.cget("text")  # leemos el texto que hay el la entrada
    texto=convertir_texto(escrito)
    for caracter in texto: #actualiza saltos y no espacios
        if caracter=='\n':
            saltos+=1
            no_espacios=0
        else:
            if caracter ==' ':
                no_espacios=0
            else:
                no_espacios+=1

    if saltos > 2 or no_espacios > 14:  # si se intentan escribir mas de 15 caracteres o mas de 2 espacios
        interpretar_teclado('Delete')  # el ultimo caracter añadido se borra
        if entrada.cget("text")[-1]==' ':
            interpretar_teclado('Delete')  # el ultimo caracter es un espacio se borra

def nombres_propios(texto): #esta aplicacion pone en mayusculas la primera letra de cada palabra escrita
    if texto.isalpha() or texto==' ':  #Comprobamos que la tecla pulsada sea una letra o un espacio en blanco
        escrito=interpretar_teclado(texto) #accedemos a la interpretacion de la tecla pulsada y recibimos el texto nuevo
        if texto != 'Shift': #Comprobamos que no haya sido Shift
            if escrito=='': #si es la primera letra a escribir
                if not mayusculas:  # si el teclado esta en minusculas
                    interpretar_teclado('Shift')  # Ponemos el teclado en mayusculas
            else: #si no es la primera letra a escribir
                if escrito[-1] == ' ':  # si la letra anterior es un espacio
                    if not mayusculas:  # si el teclado esta en minusculas
                        interpretar_teclado('Shift')  # Ponemos el teclado en mayusculas
                else:  # si la letra anterior no es un espacio
                    if mayusculas:  # si el teclado esta en mayusculas
                        interpretar_teclado('Shift')  # Ponemos el teclado en minusculas

def primera_mayuscula(texto): #nos pone en mayusculas la primera palabra del texto
    if texto.isalpha() or texto == ' ':  # Comprobamos que la tecla pulsada sea una letra o un espacio en blanco
        escrito = interpretar_teclado(texto)  # accedemos a la interpretacion de la tecla pulsada y recibimos el texto nuevo
        if texto != 'Shift':  # Comprobamos que no haya sido Shift
            if escrito=='': #si es la primera letra a escribir
                if not mayusculas:  # si el teclado esta en minusculas
                    interpretar_teclado('Shift')  # Ponemos el teclado en mayusculas
            else: #si no es la primera letra a escribir
                if mayusculas:  # si el teclado esta en mayusculas
                    interpretar_teclado('Shift')  # Ponemos el teclado en minusculas

def cifra_monetaria(tecla): #nos pone el texto en formato moneda
    if tecla.isnumeric() or tecla=='Delete': #comprobamos que lo que se haya pulsado hay sido un numero o la tecla borrar
        escrito = entrada.cget('text')  # accedemos a la interpretacion de la tecla pulsada y recibimos el texto nuevo
        entrada.cambiar_texto(formatear_numero(tecla,escrito))

def clave_password(texto):
    if texto=='Space':
        pass
    elif texto=='Shift':
        interpretar_teclado(texto)
    else:
        if texto=='Delete':
            password_set.title=password_set.title[:-1]
            password_set.cambiar_texto(password_set.cget('text')[:-1])
            if password_set.cget('text') == '':
                if lista_marcos_teclado_alfanumerico[0].cget('text') == 'Q':
                    interpretar_teclado('Shift')
        else:
            if len(password_set.cget('text')) < 22:
                password_set.cambiar_texto(password_set.cget('text')+'*')
                password_set.title=password_set.title + texto

def funcionalidad_teclado(texto): #le dice al teclado que tipo de escritura usar
    if escritura == 'password':
        clave_password(texto)
    else:
        if escritura == 'nombres':
            nombres_propios(texto)
        elif escritura == 'productos':
            primera_mayuscula(texto)
        elif escritura == 'monedas':
            cifra_monetaria(texto)
        controlar_saltos() #controlamos la escritura.
        actualizar_modo() # tiene en cuenta en el modo que hemos accedido al teclado

def actualizar_modo(): #acciones especiales cuando se usa el teclado dependiendo del modo de acceso
    if modo == 'Producto':
        texto=convertir_texto(entrada.cget("text"))
        if lista_marcos_modo_producto[4].invertir: # añade el texto de la entrada a la etiqueta nombre
            lista_marcos_modo_producto[4].cambiar_texto(texto)
            lista_marcos_modo_producto[4].datos=entrada.cget("text")
        else:
            lista_marcos_modo_producto[5].cambiar_texto(texto) # añade el texto de la entrada a la etiqueta precio
            lista_marcos_modo_producto[5].datos = entrada.cget("text")

def limpiar_productos(): #limpia los widges del modo Producto
    if lista_marcos_modo_producto[5].invertir:
        lista_marcos_modo_producto[4].invertir_colores()
        lista_marcos_modo_producto[5].invertir_colores()
    for i in range(3,6):
        lista_marcos_modo_producto[i].cambiar_texto('')
        lista_marcos_modo_producto[i].datos = ''
    nombre_precio()
    entrada.cambiar_texto('')
    primera_mayuscula('Delete')
    cargar_listado()

def limpiar_pendientes():
    if not lista_marcos_modo_pendiente[3].invertir:
        lista_marcos_modo_pendiente[3].invertir_colores()
        if lista_marcos_modo_pendiente[4].invertir:
            lista_marcos_modo_pendiente[4].invertir_colores()
        if lista_marcos_modo_pendiente[5].invertir:
            lista_marcos_modo_pendiente[5].invertir_colores()
    entrada.cambiar_texto('')
    primera_mayuscula('Delete')
    cargar_listado()

def guardar_producto(): #guarda el producto en la lista productos y en la base de datos
    prdt={}
    esnuevo=True
    for producto in lista_productos:
        if lista_marcos_modo_producto[4].datos == producto['nombre']: #lo actualiza si existe
            producto['familia']=lista_marcos_modo_producto[3].datos
            producto['precio']=lista_marcos_modo_producto[5].datos
            esnuevo=False
            break
    if esnuevo: # lo añade si no existe
        prdt['nombre']=lista_marcos_modo_producto[4].datos
        prdt['familia']=lista_marcos_modo_producto[3].datos
        prdt['precio']=lista_marcos_modo_producto[5].datos
        lista_productos.append(prdt)
    limpiar_productos() #limpia los widget modo Producto
    guardar_datos() #guarda en la base de datos

def eliminar_producto(): # elimina un producto existente en la lista productos y en la base de datos
    encontrado = False
    for producto in lista_productos:
        if lista_marcos_modo_producto[4].datos == producto['nombre']: #comprueba si esta en la lista productos
            lista_productos.remove(producto) #lo elimina de la lista
            encontrado=True
            break
    if encontrado: #en caso de que lo haya eliminado de la lista
        limpiar_productos() #limpia los widget modo Producto
        guardar_datos() #guarda en la base de datos

def crear_cont_sec(): #creamos el contenedor del teclado
    global cont_sec
    cont_sec = contenedor.crear_panel(dimensiones[0],dimensiones[1],'gray82')
    cont_sec.colocar_objeto(0, 0)
    crear_cont_tec()
    crear_ocul_tec()
    crear_entrada()
    crear_volver()
    crear_cont_sec_modos()
    crear_cont_sec_pass()

def crear_cont_tec():  # creamos el contenedor del teclado
    global cont_tec
    cont_tec = cont_sec.crear_panel(dimensiones[0], 290, 'gray82')
    cont_tec.colocar_objeto(0, 445)
    crear_teclados_virtuales()

def crear_ocul_tec(): #creamos el contenedor del teclado
    global ocul_tec
    ocul_tec = cont_sec.crear_panel(750,290,'gray82')
    ocul_tec.colocar_objeto(0, 445)
    ocul_tec.lower()

def crear_teclados_virtuales(): #creamos un teclado virtual completamente funcional
    # Definir las filas de teclas
    filas = (('Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '7', '8', '9'),
             ('A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Ñ', '4', '5', '6'),
             ('-', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', 'Ü', 'Ç', '1', '2', '3'),
             ('Shift', 'Space', 'Delete', '0', '.'))
    y = -65
    # Crear el teclado
    for fila in filas:
        y+=70
        x=-30
        for tecla in fila:
            tipo='tecla'
            match tecla: #posicionamos cada tecla y la damos su anchura.
                case '7':
                    x += 30
                case '4':
                    x += 30
                case '1':
                    x += 30
                case 'Space':
                    tipo='tecla_space'
                    x += 70
                case 'Shift':
                    tipo='tecla_doble'
                case 'Delete':
                    tipo='tecla_doble'
                    x += 350
                case '0':
                    tipo='tecla_doble'
                    x += 100
                case '.':
                    x += 70
            x+=70
            #crear_marco(self,texto,title,tipo,letra,fondo)
            virtual=cont_tec.crear_marco(tecla,tecla,tipo,24,cont_tec.fondo)
            virtual.colocar_objeto(x, y)
            if not virtual.title.isnumeric() and not tipo=='tecla_space':
                virtual.invertir_colores()
            # capta los eventos del teclado virtual
            virtual.bind("<Button-1>", on_click_virtual)
            virtual.bind("<ButtonRelease-1>", off_click_virtual)
            lista_marcos_teclado_alfanumerico.append(virtual)

def crear_entrada(): #creamos un contenedor de texto en el teclado virtual
    global entrada
    entrada = cont_sec.crear_marco('', '', 'textbox', 20, cont_sec.fondo)
    entrada.colocar_objeto(40, 370)

def crear_volver(): #creamos la tecla volver en el teclado virtual
    global volver
    volver = cont_sec.crear_marco('Volver', 'volver', 'tecla_envio', 24, cont_sec.fondo)
    volver.invertir_colores()
    volver.colocar_objeto(771, 370)
    volver.bind("<Button-1>", on_click_volver)  # capta los eventos del boton volver
    volver.bind("<ButtonRelease-1>", off_click_volver)

def ingresar_password():
    global escritura
    cont_sec_password.tkraise()
    limpiar_pendientes()
    escritura = 'password'
    if lista_marcos_teclado_alfanumerico[0].cget('text') == 'Q':
        interpretar_teclado('Shift')
    password_mensaje.cambiar_texto('Introduzca contraseña para acceder')
    password_label.title = None
    password_label.cambiar_texto('Ingresa Password')
    password_label.cambiar_largo(len(password_label.cget('text')))
    password_change.cambiar_texto('Administrar\nContraseña')
    password_change.title = 'admin'
    password_set.cambiar_texto('')
    password_set.title = ''

def acceso_terciario():
    if modo=='Pendiente':
        if password_change.title=='admin':
            cambiar_fechado(fechado.title)
            cont_ter.tkraise()
            cont_sec_password.lower()
            comodin.title='impresoras'
            comodin.cambiar_texto('Asignar\nImpresoras')
    elif modo=='Camarero':
        buscar_camareros_recibo()
        cambiar_fechado(fechado.title)
        cont_ter.tkraise()
        cont_sec_password.lower()
        comodin.title = camarero_actual.title
        comodin.cambiar_texto(convertir_texto(camarero_actual.title))

def ventanas_password(pw):
    password_change.title = pw[0]
    password_change.cambiar_texto(pw[1])
    password_label.title = pw[2]
    password_label.cambiar_texto(pw[3])
    password_mensaje.cambiar_texto(pw[4])
    password_label.cambiar_largo(len(password_label.cget('text')))
    password_set.cambiar_texto('')
    password_set.title = ''

def gestionar_password(objeto):
    global password
    if objeto.title=='envio':
        if password_set.title == administrador:
            pw = ['nueva','Cancelar\nCambios',password,'Ingresa Nuevo Password','Va a proceder a cambiar la contraseña']
            ventanas_password(pw)
        elif password_set.title == password:
            if password_change.title == 'admin':
                lista_marcos_modo_pendiente[0].title = copy.deepcopy(diccionario_recibo)
                acceso_terciario()
                password_mensaje.cambiar_texto('Acceso Normal')
            elif password_change.title == 'cambio':
                password_mensaje.cambiar_texto('Acceso Especial')
            elif password_change.title == 'repite':
                if password_set.title == password:
                    guardar_datos()
                    pw = ['admin', 'Administrar\nContraseña',None,'Ingresa Password','La contraseña se guardo correctamente']
                    ventanas_password(pw)
                else:
                    password_mensaje.cambiar_texto('Las contraseñas no coinciden')
        else:
            if password_change.title == 'nueva':
                pw = ['repite', 'Cancelar\nCambios',password,'Repita Nuevo Password','Vuelva a repetir la nueva contraseña']
                password=password_set.title
                ventanas_password(pw)
            else:
                password_mensaje.cambiar_texto('La contraseña introducida es incorrecta')
    elif objeto.title=='admin':
        if password_set.title == password:
            pw = ['cambio', 'Cambiar\nContraseña',password,'Ingresa Password','Ha accedido a la administración de contraseñas']
            ventanas_password(pw)
        else:
            password_mensaje.cambiar_texto('La contraseña introducida es incorrecta')
    elif objeto.title=='cambio':
        if password_set.title == password:
            pw = ['nueva', 'Cancelar\nCambios',password,'Ingresa Nuevo Password','Va a proceder a cambiar la contraseña']
            ventanas_password(pw)
        else:
            password_mensaje.cambiar_texto('La contraseña introducida es incorrecta')
    elif objeto.title == 'nueva' or objeto.title == 'repite':
        pw = ['cambio', 'Cambiar\nContraseña',None,'Ingresa Password','Se cancelo la operación de cambio de contraseña']
        password=password_label.title
        ventanas_password(pw)

def on_click_password(event): #actuaciones al evento al pulsar una tecla del teclado del panel principal
    event.widget.invertir_colores()
    gestionar_password(event.widget)

def off_click_password(event):  #actuaciones al evento al soltar una tecla del teclado del panel
    event.widget.invertir_colores()

def crear_cont_sec_pass(): #creamos el contenedor del teclado en el teclado virtual
    global cont_sec_password
    global password_set
    global password_send
    global password_change
    global password_label
    global password_mensaje

    x= 45
    y = 75
    etiqueta = 'Ingresa Password'
    nombre_ps = 'Aceptar'
    title_ps = 'envio'
    nombre_pc = 'Administrar\nContraseña'
    title_pc = 'admin'

    cont_sec_password = cont_sec.crear_panel(dimensiones[0],365,'gray82')
    cont_sec_password.colocar_objeto(0, 0)

    password_mensaje=cont_sec_password.crear_etiqueta('',16,'SlateGray4',cont_sec_password.fondo,77) #etiqueta informativa
    password_mensaje.colocar_objeto(x, y)

    y+=75
    password_label=cont_sec_password.crear_etiqueta(etiqueta,16,'SlateGray4',cont_sec_password.fondo,len(etiqueta)) #etiqueta informativa
    password_label.colocar_objeto(x, y)

    y+=30
    password_set = cont_sec_password.crear_marco('', '', 'tecla_space', 24, cont_sec_password.fondo)
    password_set.invertir_colores()
    password_set.colocar_objeto(x, y)

    x+=465
    password_send = cont_sec_password.crear_marco(nombre_ps, title_ps, 'tecla_envio', 24, cont_sec_password.fondo)
    password_send.invertir_colores()
    password_send.colocar_objeto(x, y)
    password_send.bind("<Button-1>", on_click_password)  # capta los eventos del boton password_send
    password_send.bind("<ButtonRelease-1>", off_click_password)

    x += 260
    password_change = cont_sec_password.crear_marco(nombre_pc, title_pc, 'tecla_envio', 18, cont_sec_password.fondo)
    password_change.invertir_colores()
    password_change.colocar_objeto(x, y)
    password_change.bind("<Button-1>", on_click_password)  # capta los eventos del boton password_send
    password_change.bind("<ButtonRelease-1>", off_click_password)

    cont_sec_password.lower()

def crear_cont_sec_modos(): #creamos el contenedor del teclado en el teclado virtual
    global cont_sec_modos
    cont_sec_modos = cont_sec.crear_panel(dimensiones[0],365,'gray82')
    cont_sec_modos.colocar_objeto(0, 0)
    crear_info()
    crear_listado()
    crear_cont_producto()
    crear_cont_pendiente()
    crear_cont_mesero()

def crear_cont_producto(): #creamos el contenedor del teclado en el teclado virtual
    global cont_producto
    cont_producto = cont_sec_modos.crear_panel(dimensiones[0]-430,225,'gray82')
    cont_producto.colocar_objeto(0, 130)
    gestionar_productos()

def crear_cont_pendiente(): #creamos el contenedor del teclado en el teclado virtual
    global cont_pendiente
    cont_pendiente = cont_sec_modos.crear_panel(dimensiones[0]-430,225,'gray82')
    cont_pendiente.colocar_objeto(0, 130)
    gestionar_pendientes()

def crear_cont_mesero(): #creamos el contenedor del teclado en el teclado virtual
    global cont_mesero
    cont_mesero = cont_sec_modos.crear_panel(dimensiones[0]-430,225,'gray82')
    cont_mesero.colocar_objeto(0, 130)
    gestionar_meseros()

def crear_info(): #creamos el contenedor del teclado en el teclado virtual
    global info #hasta 54 caracteres
    info = cont_sec_modos.crear_marco('', 'info', 'info', 12, cont_sec_modos.fondo)
    info.colocar_objeto(40, 45)

def deshabilitar_espacio(event): #deshabilita la autoseleccion con el espacio
    global espacio
    tecla=event.keysym
    if tecla=='space':
        espacio=True

def crear_listado(): #creamos la lista en el teclado virtual
    global listado
    cont_list = cont_sec_modos.crear_panel(380, 310, 'black')
    cont_list.expandir_panel()
    cont_list.colocar_objeto(dimensiones[0]-cont_list.ancho-50, 45)
    listado=cont_list.crear_lista(LEFT,BOTH)
    barra=cont_list.crear_barra(RIGHT,Y)
    listado.sincronizar_lista(barra)
    barra.sincronizar_barra(listado)
    listado.bind("<Key>", deshabilitar_espacio)
    listado.bind("<<ListboxSelect>>", obtener_seleccion)

def crear_listado_clientes():
    lista=[]
    for nombre in lista_clientes:
        cont=0
        for item in lista_recibos_impagados:
            if nombre==item['nombre']:
                cont+=1
        lista.append([nombre,cont])
    return lista

def cargar_listado(busqueda=''): # carga la informacion correspondiente en la listbox
    global listado
    listado.delete(0, END) #se limpia la lista
    match modo:
        case 'Producto':
            for producto in lista_productos: # para todos los productos en producto
                if producto['familia']==busqueda: #si coincide la familia
                    listado.insert(END, f"{producto['nombre']} - {producto['precio']}€") #añade la informacion a la lista
        case 'Pendiente':
            lista=crear_listado_clientes()
            for nombre,cuantos in lista:
                if lista_marcos_modo_pendiente[3].invertir:
                    listado.insert(END, f'{nombre} - ({cuantos})')
                    if cuantos > 0:
                        listado.itemconfig(listado.size() - 1, {'fg': 'red'})  # Cambia el color de la línea recién añadida.
                elif lista_marcos_modo_pendiente[4].invertir:
                    if cuantos > 0:
                        listado.insert(END, f'{nombre} - ({cuantos})')
                        listado.itemconfig(listado.size() - 1, {'fg': 'red'})  # Cambia el color de la línea recién añadida.
                elif lista_marcos_modo_pendiente[5].invertir:
                    if cuantos == 0:
                        listado.insert(END, f'{nombre} - ({cuantos})')
        case 'Camarero':
            for empleado in lista_camareros:
                listado.insert(END, empleado)  # añade la informacion a la lista

def gestionar_pendientes(): #creamos los botones y marcos en modo Pendiente en el teclado virtual
    lista_marcos_modo_pendiente.clear()
    posx=40
    posy=25
    dis=180

    x=posx
    y=posy
    pendiente = cont_pendiente.crear_marco('Guardar','guardar','tecla_marco',20,cont_pendiente.fondo) #0 boton guardar
    pendiente.datos='Pendiente'
    pendiente.colocar_objeto(x, y)
    lista_marcos_modo_pendiente.append(pendiente)
    x+=dis
    pendiente = cont_pendiente.crear_marco('Eliminar','eliminar','tecla_marco',20,cont_pendiente.fondo) #1 boton eliminar
    pendiente.datos = 'Pendiente'
    pendiente.colocar_objeto(x, y)
    lista_marcos_modo_pendiente.append(pendiente)
    x+=dis
    pendiente = cont_pendiente.crear_marco('Agregar','agregar','tecla_marco',20,cont_pendiente.fondo) #2 boton limpiar
    pendiente.datos = 'Pendiente'
    pendiente.colocar_objeto(x, y)
    lista_marcos_modo_pendiente.append(pendiente)
    x=posx
    y=posy+100
    pendiente = cont_pendiente.crear_marco('','todos','tecla_marco',12,cont_pendiente.fondo) #3 marco familia
    pendiente.datos = 'Todos'
    pendiente.colocar_objeto(x, y)
    pendiente.cambiar_texto(convertir_texto('Todos los Clientes'.upper()))
    pendiente.invertir_colores()
    lista_marcos_modo_pendiente.append(pendiente)
    x+=dis
    pendiente = cont_pendiente.crear_marco('','pendientes','tecla_marco',12,cont_pendiente.fondo) #4 marco nombre
    pendiente.datos = 'Pendientes'
    pendiente.colocar_objeto(x, y)
    pendiente.cambiar_texto(convertir_texto('Clientes con Tickets Pendientes'.upper()))
    lista_marcos_modo_pendiente.append(pendiente)
    x+=dis
    pendiente = cont_pendiente.crear_marco('','pagado','tecla_marco',12,cont_pendiente.fondo) #5 marco precio
    pendiente.datos = 'Pagado'
    pendiente.colocar_objeto(x, y)
    pendiente.cambiar_texto(convertir_texto('Clientes sin Deudas Asociadas'.upper()))
    lista_marcos_modo_pendiente.append(pendiente) #los añadimos a la lista pendientess para luego poder controlarlos
    for pendiente in lista_marcos_modo_pendiente: #capta los eventos del modo Producto
        pendiente.bind("<Button-1>", on_click_pendiente)
        pendiente.bind("<ButtonRelease-1>", off_click_pendiente)

def gestionar_productos(): #creamos los botones y marcos en modo Producto en el teclado virtual
    lista_marcos_modo_producto.clear()
    posx=40
    posy=25
    dis=180

    x=posx
    y=posy
    nuevo = cont_producto.crear_marco('Guardar','guardar','tecla_marco',20,cont_producto.fondo) #0 boton guardar
    nuevo.colocar_objeto(x, y)
    lista_marcos_modo_producto.append(nuevo)
    x+=dis
    nuevo = cont_producto.crear_marco('Eliminar','eliminar','tecla_marco',20,cont_producto.fondo) #1 boton eliminar
    nuevo.colocar_objeto(x, y)
    lista_marcos_modo_producto.append(nuevo)
    x+=dis
    nuevo = cont_producto.crear_marco('Limpiar','limpiar','tecla_marco',20,cont_producto.fondo) #2 boton limpiar
    nuevo.colocar_objeto(x, y)
    lista_marcos_modo_producto.append(nuevo)
    x=posx+3
    y=posy+80
    etiq=cont_producto.crear_etiqueta('Familia',12,'SlateGray4',cont_producto.fondo,16) #etiqueta informativa
    etiq.colocar_objeto(x, y)
    x+=dis
    etiq=cont_producto.crear_etiqueta('Nombre',12,'SlateGray4',cont_producto.fondo,16) #etiqueta informativa
    etiq.colocar_objeto(x, y)
    x+=dis
    etiq=cont_producto.crear_etiqueta('Precio',12,'SlateGray4',cont_producto.fondo,16) #etiqueta informativa
    etiq.colocar_objeto(x, y)
    x=posx
    y=posy+100
    nuevo = cont_producto.crear_marco('','familia','tecla_marco',12,cont_producto.fondo) #3 marco familia
    nuevo.colocar_objeto(x, y)
    lista_marcos_modo_producto.append(nuevo)
    x+=dis
    nuevo = cont_producto.crear_marco('','nombre','tecla_marco',12,cont_producto.fondo) #4 marco nombre
    nuevo.colocar_objeto(x, y)
    nuevo.invertir_colores()
    lista_marcos_modo_producto.append(nuevo)
    x+=dis
    nuevo = cont_producto.crear_marco('','precio','tecla_marco',12,cont_producto.fondo) #5 marco precio
    nuevo.colocar_objeto(x, y)
    lista_marcos_modo_producto.append(nuevo) #los añadimos a la lista nuevos para luego poder controlarlos
    for novo in lista_marcos_modo_producto: #capta los eventos del modo Producto
        novo.bind("<Button-1>", on_click_producto)
        novo.bind("<ButtonRelease-1>", off_click_producto)

def gestionar_meseros():  # creamos los botones y marcos en modo Pendiente en el teclado virtual
    lista_marcos_modo_camarero.clear()
    posx = 40
    posy = 25
    dis = 180

    x = posx
    y = posy
    mesero = cont_mesero.crear_marco('Tickets', 'tickets', 'tecla_marco', 20,cont_mesero.fondo)  # 0 boton tickets
    mesero.colocar_objeto(x, y)
    lista_marcos_modo_camarero.append(mesero)
    x += dis
    mesero = cont_mesero.crear_marco('Eliminar', 'eliminar', 'tecla_marco', 20,cont_mesero.fondo)  # 1 boton eliminar
    mesero.colocar_objeto(x, y)
    lista_marcos_modo_camarero.append(mesero)
    x += dis
    mesero = cont_mesero.crear_marco('Agregar', 'agregar', 'tecla_marco', 20,cont_mesero.fondo)  # 2 boton agregar
    mesero.colocar_objeto(x, y)
    lista_marcos_modo_camarero.append(mesero)
    for mesero in lista_marcos_modo_camarero: #capta los eventos del modo Producto
        mesero.bind("<Button-1>", on_click_mesero)
        mesero.bind("<ButtonRelease-1>", off_click_mesero)

def on_click_mesero(event): #actuaciones al evento pulsar una tecla modo Camarero
    event.widget.invertir_colores()
    if event.widget.title == 'tickets':
        if camarero_actual.title != '':
            ingresar_password()
    else:
        empleado=entrada.cget('text')
        if empleado!='':
            if existe_en_lista(empleado,lista_camareros):
                if event.widget.title == 'eliminar':
                    lista_camareros.remove(empleado)
                    guardar_datos()
                    limpiar_camareros()
                    info.cambiar_texto(convertir_texto(f'{empleado} ha sido eliminado', 54))
                else:
                    info.cambiar_texto(convertir_texto(f'{empleado} ya existe en la base de datos', 54))
            else:
                if event.widget.title == 'agregar':
                    lista_camareros.append(empleado)
                    guardar_datos()
                    limpiar_camareros()
                    info.cambiar_texto(convertir_texto(f'{empleado} ha sido agregado', 54))
                else:
                    info.cambiar_texto(convertir_texto(f'{empleado} no existe en la base de datos, no se puede eliminar', 54))
        else:
            info.cambiar_texto(convertir_texto('Debes introducir algún nombre válido de camarero', 54))

def off_click_mesero(event): #actuaciones al evento soltar una tecla del teclado
    event.widget.invertir_colores()

def tecla_pulsada(event): #le doy funcionalidad al teclado por si se conecta alguno al terminal
    tecla=event.keysym
    if ventana_aplicacion.teclado: #si estamos en el panel secundario controlamos el teclado virtual
        texto=''
        if len(tecla)==1: #controlo la tecla pulsada y la comparo con mi sistema
            if tecla.isalpha():
                if mayusculas:
                    texto=tecla.upper()
                else:
                    texto=tecla.lower()
            elif tecla.isnumeric():
                texto=tecla
        elif tecla=='space':
            texto='Space'
        elif tecla=='Shift_L' or tecla=='Shift_R' or tecla=='Caps_Lock':
            texto='Shift'
        elif tecla=='Delete' or tecla=='BackSpace':
            texto='Delete'
        elif tecla.lower()=='ntilde':
            if mayusculas:
                texto='Ñ'
            else:
                texto='ñ'
        elif tecla.lower()=='ccedilla':
            if mayusculas:
                texto='Ç'
            else:
                texto='ç'
        elif tecla=='Multi_key':
            if mayusculas:
                texto='Ü'
            else:
                texto='ü'
        elif tecla=='minus':
            texto='-'
        elif tecla=='period':
            texto='.'
        elif tecla=='Return':
            if modo=='Producto':
                lista_marcos_modo_producto[4].invertir_colores()
                lista_marcos_modo_producto[5].invertir_colores()
                nombre_precio()
        funcionalidad_teclado(texto)
    else: #si estamos en el panel principal controlamos el teclado numerico
        texto = ''
        if len(tecla) == 1:  # controlo la tecla pulsada y la comparo con mi sistema
            if tecla.isnumeric():
                texto = tecla
        elif tecla=='Delete' or tecla=='BackSpace':
            texto='del'
        elif tecla=='Return':
            texto='ok'
        if texto != '':
            crear_importe(texto)
    if tecla=='Escape': # si queremos salir de la aplicacion, independientemente donde estemos
        salir(ventana_aplicacion)

def obtener_seleccion(event): #actuaciones al evento seleccionar un elemento del listbox
    global espacio
    if espacio:
        espacio=False
    else:
        seleccion = event.widget.curselection() # Obtener la selección actual
        if seleccion:
            # Obtener el valor seleccionado
            item = event.widget.get(seleccion[0])
            match modo: #dependiendo del modo en el que estemos
                case 'Producto': #si estamos en el modo Producto
                    producto, precio = item.split(" - ") #lo guardamos en variables
                    # asignamos la informacion al los diferentes marcos en el formato correcto
                    precio=precio[:-1] # quitamos el simbolo € del precio
                    lista_marcos_modo_producto[4].datos=producto
                    lista_marcos_modo_producto[4].cambiar_texto(convertir_texto(producto))
                    lista_marcos_modo_producto[5].datos=precio
                    lista_marcos_modo_producto[5].cambiar_texto(precio)
                    if lista_marcos_modo_producto[4].invertir:
                        entrada.cambiar_texto(producto)
                    else:
                        entrada.cambiar_texto(precio)
                case 'Pendiente': #si estamos en modo Pendiente
                    nombre, _ = item.split(' - ')
                    entrada.cambiar_texto(nombre)
                case 'Camarero': #si estamos en modo camarero
                    entrada.cambiar_texto(item)

def crear_ticket_pendiente():
    global diccionario_recibo
    consumidor = entrada.cget('text')
    if consumidor!='':
        if not existe_en_lista(consumidor,lista_clientes):
            lista_clientes.append(consumidor)
        #actualizamos la variable recibo y la guardamos en la base de datos
        diccionario_recibo['nombre']=consumidor
        diccionario_recibo['fecha']=datetime.datetime.now().strftime('%d/%m/%Y - %H:%M:%S')
        diccionario_recibo['estado']='pendiente'
        diccionario_recibo['impreso']=False
        diccionario_recibo['camarero']= camarero_actual.title
        lista_recibos_impagados.append(copy.deepcopy(diccionario_recibo)) #aqui debemos agregar el pedido a la lista de morosos
        guardar_datos()# Aqui llamar a guardar en la base de datos
        limpiar_pendientes()
        #obtener_recibo(datetime.datetime.now().strftime('%d/%m/%Y - %H:%M:%S'))
        ticket.cambiar_texto(actualizar_ticket()) #actualizamos el ticket
        info.cambiar_texto(convertir_texto('El ticket ha sido guardado', 54))
    else:
        info.cambiar_texto(convertir_texto('Debes introducir algún nombre válido de cliente',54))

def on_click_volver(event): # #actuaciones al evento pulsar la tecla de volver
    event.widget.invertir_colores()
    info.cambiar_texto('')
    if modo=='Producto':
        actualizar_consumiciones()  # actualizamos los marcos de las consumiciones
    elif modo=='Pendiente':
        actualizar_marcos_recibos_impagados()
    elif modo=='Camarero':
        actualizar_camareros()
    ventana_aplicacion.teclado = False  # indicamos que ya no estamos en el teclado virtual
    cont_prin.tkraise()  # traemos el panel principal al frente

def off_click_volver(event): #actuaciones al evento soltar la tecla de volver
    event.widget.invertir_colores()

def on_click_virtual(event): #actuaciones al evento pulsar una tecla del teclado
    funcionalidad_teclado(event.widget.cget("text"))
    event.widget.invertir_colores()

def off_click_virtual(event): #actuaciones al evento soltar una tecla del teclado
    event.widget.invertir_colores()

def on_click_producto(event):  #actuaciones al evento pinchar en un boton del modo Producto
    event.widget.invertir_colores()
    match event.widget.title:
        case 'nombre': # activa o desactiva precio
            lista_marcos_modo_producto[5].invertir_colores()
        case 'precio': #activa o desactiva nombre
            lista_marcos_modo_producto[4].invertir_colores()
        case 'guardar': # guarda los productos en la base de datos
            if lista_marcos_modo_producto[4].datos and lista_marcos_modo_producto[3].datos and lista_marcos_modo_producto[5].datos:
                guardar_producto()
        case 'familia': #va navegando por las diferentes familias
            if event.widget.cget('text')=='Bebida':
                event.widget.datos='Comida'
                event.widget.cambiar_texto('Comida')
            elif event.widget.cget('text')=='Comida':
                event.widget.datos='Otros'
                event.widget.cambiar_texto('Otros')
            else:
                event.widget.datos='Bebida'
                event.widget.cambiar_texto('Bebida')
            cargar_listado(event.widget.datos)
        case 'eliminar': #elimina un producto de la base de datos
            eliminar_producto()
        case 'limpiar': #limpia los campos del modo Producto
            limpiar_productos()

def nombre_precio(): #cambia el tipo de escritura dependiendo del marco activo del modo Producto
    global escritura

    if lista_marcos_modo_producto[4].invertir: # si el marco activo es nombre
        escritura = 'productos' # activa el modo de escritura de productos
        nombre = lista_marcos_modo_producto[4].cget('text').split('\n') # quitamos los saltos de linea
        entrada.cambiar_texto(' '.join(nombre)) # y lo unimos con espacios

    else: #si el marco activo es precio
        escritura = 'monedas' # activa el modo de escritura de numeros
        entrada.cambiar_texto(lista_marcos_modo_producto[5].cget('text'))

def off_click_producto(event):  #actuaciones al evento soltar boton del modo Producto
    if event.widget.title!='nombre' and event.widget.title!='precio':
        event.widget.invertir_colores()
    else:
        nombre_precio()

def reiniciar_pendientes():
    for i in range(3,6):
        if lista_marcos_modo_pendiente[i].invertir:
            lista_marcos_modo_pendiente[i].invertir_colores()

def tiene_ticket_pendiente(nombre):
    for item in lista_recibos_impagados:
        if nombre==item['nombre']:
            return True
    return False

def on_click_pendiente(event):  #actuaciones al evento pinchar en un boton del modo Pendiente
    if event.widget.datos != 'Pendiente':
        reiniciar_pendientes()
    else:
        if event.widget.title == 'guardar':
            crear_ticket_pendiente()  # creamos el ticket de pendiente
            event.widget.title='comanda'
            event.widget.cambiar_texto('Comanda')
            pulsar_boton_pie(lista_marcos_pie_principal[4])
        elif event.widget.title == 'tickets':
            ingresar_password()
        elif event.widget.title == 'comanda':
            pass
        else:
            consumidor=entrada.cget('text')
            if consumidor!='':
                if existe_en_lista(consumidor,lista_clientes):
                    if event.widget.title == 'eliminar':
                        if not tiene_ticket_pendiente(consumidor):
                            lista_clientes.remove(consumidor)
                            guardar_datos()
                            limpiar_pendientes()
                            info.cambiar_texto(convertir_texto(f'{consumidor} ha sido eliminado', 54))
                        else:
                            info.cambiar_texto(convertir_texto(f'{consumidor} tiene ticket pendiente de pago', 54))
                    else:
                        info.cambiar_texto(convertir_texto(f'{consumidor} ya existe en la base de datos', 54))
                else:
                    if event.widget.title == 'agregar':
                        lista_clientes.append(consumidor)
                        guardar_datos()
                        limpiar_pendientes()
                        info.cambiar_texto(convertir_texto(f'{consumidor} ha sido agregado', 54))
                    else:
                        info.cambiar_texto(convertir_texto(f'{consumidor} no existe en la base de datos, no se puede eliminar', 54))
            else:
                info.cambiar_texto(convertir_texto('Debes introducir algún nombre válido de cliente', 54))
    event.widget.invertir_colores()

def off_click_pendiente(event):  #actuaciones al evento soltar boton del modo Pendiente
    if event.widget.datos=='Pendiente':
        event.widget.invertir_colores()
    else:
        cargar_listado()

# Creacion del panel pricipal y sus aplicaciones

def crear_aplicacion(): #creamos la ventana principal de la aplicacion que contendra todos los elementos
    global ventana_aplicacion
    dimensiones.append(1024) #anchura minima de la pantalla principal +5px
    dimensiones.append(768) #altura minima de la pantalla principal +5px
    ventana_aplicacion = Ventanas("TPV",dimensiones[0]+5,dimensiones[1]+5)
    ventana_aplicacion.bind("<Key>", tecla_pulsada)  # capta el evento del pulsar una tecla
    locale.setlocale(locale.LC_TIME, 'es_ES')
    crear_contenendor()

def crear_contenendor(): #creamos el contenedor que estara siempre en el centro de la pantalla principal
    global contenedor
    contenedor = ventana_aplicacion.crear_panel(dimensiones[0],dimensiones[1],'gray34')
    ventana_aplicacion.bind("<Configure>", contenedor.recolocar_panel)  # centra el contenedor en la aplicacion principal
    crear_cont_prin()
    crear_cont_sec()
    crear_cont_ter()

def crear_cont_prin(): # Creamos el contenedor de todos los widges principales
    global cont_prin
    cont_prin = contenedor.crear_panel(dimensiones[0],dimensiones[1],'gray82')
    cont_prin.colocar_objeto(0, 0)
    crear_titulo()
    crear_pie()
    crear_bebidas()
    crear_comidas()
    crear_otros()
    crear_consumiciones()
    crear_impago()
    crear_numericos()
    crear_impresion()
    crear_barman()

def crear_titulo(): # Creamos el contenedor del titulo
    global titulo
    titulo=cont_prin.crear_panel(dimensiones[0]-226,76,'gray82')
    titulo.colocar_objeto(5,5)
    crear_logotipo()

def crear_logotipo():
    global logotipo
    global apagar
    global camarero_actual
    global camarero_anterior
    global camarero
    x=0
    y=2
    logotipo = titulo.crear_boton('logo', 'logo', titulo.fondo)
    logotipo.colocar_objeto(x, 2)
    x+=95
    etiqueta='Está atendiendo el camarero:'
    etiq = titulo.crear_etiqueta(etiqueta, 14, 'SlateGray4', 'gray92',38)  # etiqueta informativa
    etiq.colocar_objeto(x, y+2)
    etiqueta=''
    camarero_actual = titulo.crear_etiqueta(etiqueta, 14, 'Gray10', 'gray92',38)  # etiqueta informativa
    camarero_actual.colocar_objeto(x, y+38)
    camarero_actual.title=''
    x+=395
    camarero_anterior = titulo.crear_marco('', '', 'tecla_marco', 12, titulo.fondo)
    camarero_anterior.colocar_objeto(x, y)
    camarero_anterior.invertir_colores()
    camarero_anterior.bind("<Button-1>", on_click_camarero_anterior)  # obtenemos el evento al pulsar en la marco
    camarero_anterior.bind("<ButtonRelease-1>", off_click_camarero_anterior)  # obtenemos el evento al soltar la marco
    x+=158
    camarero = titulo.crear_boton ('barman', 'barman', titulo.fondo)
    camarero.colocar_objeto(x, y+2)
    camarero.bind("<Button-1>", on_click_camarero)  # obtenemos el evento al pulsar en la marco
    camarero.bind("<ButtonRelease-1>", off_click_camarero)  # obtenemos el evento al soltar la marco
    x+=77
    apagar = titulo.crear_boton ('apagar', 'apagado', titulo.fondo)
    apagar.colocar_objeto(x, y)
    apagar.bind("<Button-1>", on_click_apagado)  # obtenemos el evento al pulsar en la marco
    apagar.bind("<ButtonRelease-1>", off_click_apagado)  # obtenemos el evento al soltar la marco

def on_click_camarero_anterior(event):  #actuaciones al evento pulsar en cualquiera de los marcos de las consumiciones
    event.widget.invertir_colores()
    if event.widget.title != '':
        camarero_nombre=convertir_texto(camarero_actual.cget('text'))
        camarero_titulo=camarero_actual.title
        camarero_actual.cambiar_texto(camarero_anterior.title)
        camarero_actual.title=camarero_anterior.title
        camarero_anterior.cambiar_texto(camarero_nombre)
        camarero_anterior.title=camarero_titulo


def off_click_camarero_anterior(event):  #actuaciones al evento al soltar el boton de las consumiciones
        event.widget.invertir_colores()

def on_click_camarero(event):  #actuaciones al evento pulsar en cualquiera de los marcos de las consumiciones
    event.widget.invertir_colores()
    if lista_marcos_pie_principal[3].invertir:
        barman.tkraise()

def off_click_camarero(event):  #actuaciones al evento al soltar el boton de las consumiciones
        event.widget.invertir_colores()

def on_click_apagado(event):  #actuaciones al evento pulsar en cualquiera de los marcos de las consumiciones
    event.widget.invertir_colores()
    apagar_equipo()

def off_click_apagado(event):  #actuaciones al evento al soltar el boton de las consumiciones
        event.widget.invertir_colores()

def crear_pie(): # Creamos el contenedor de los botones de opciones de la pantalla principal
    global pie
    pie=cont_prin.crear_panel(dimensiones[0]-226,76,'gray82')
    pie.colocar_objeto(5,ventana_aplicacion.alto-86)
    crear_botones_pie()

def crear_botones_pie():  # creamos los botones de las opciones del panel principal
    mp = ['modificar', 'consumiciones', 'productos', 'ordenar', 'impagos']
    y = 6
    x = 3
    # se pueden introducir has 40 registros de cada familia
    texto = ''
    for marco in mp:
        match marco:
            case 'modificar':
                texto = 'AÑADIR\nCONSUMICION'
            case 'consumiciones':
                texto = 'MOSTRAR\nCONSUMICIONES'
            case 'productos':
                texto = 'GESTIONAR\nPRODUCTOS'
            case 'ordenar':
                texto = 'REORDENAR\nPRODUCTOS'
            case 'impagos':
                texto = 'TICKETS\nPENDIENTES\nDE PAGO'

        boton = pie.crear_marco(texto, marco, 'tecla_marco', 12, pie.fondo)
        boton.datos = 'Bebida'
        boton.colocar_objeto(x, y)
        boton.invertir_colores()
        x += 158
        boton.bind("<Button-1>", on_click_pie)  # obtenemos el evento al pulsar en la tecla
        boton.bind("<ButtonRelease-1>", off_click_pie)  # obtenemos el evento al soltar la tecla
        lista_marcos_pie_principal.append(boton)

def pulsar_boton_pie(objeto):
    global modo
    if objeto.title == 'impagos':  # en caso de pulsar el boton de tickets pendientes de pago
        if lista_marcos_pie_principal[3].invertir:
            modificar_consumiciones(False)
            if not ticket.bloqueado:
                cambiar_estado_impresion()
            lista_marcos_pie_principal[1].cambiar_texto('MOSTRAR\nCONSUMICIONES')
            impago.tkraise()  # lo mismo que impago.lift() si quiero enviarlo al fondo impago.lower()
            if objeto.cget('text') == 'TICKETS\nPENDIENTES\nDE PAGO':
                objeto.cambiar_texto('UNIR TICKETS\nDEL MISMO\nCLIENTE')
                impago.cambiar_fondo('red4')
            else:
                objeto.cambiar_texto('TICKETS\nPENDIENTES\nDE PAGO')
                impago.cambiar_fondo('MediumPurple1')
            actualizar_marcos_recibos_impagados()
    elif diccionario_recibo['nombre'] == cabecera_ticket and lista_marcos_pie_principal[4].cget('text') != 'UNIR TICKETS\nDEL MISMO\nCLIENTE':
        if objeto.title != 'productos':
            lista_marcos_pie_principal[4].cambiar_texto('GESTION DE\nTICKETS')
        if objeto.title == 'consumiciones':  # en caso de que el boton pulsado sea el de consumiciones
            match objeto.cget("text"):
                # trae el panel correspondiente al frente
                case 'MOSTRANDO\nBEBIDAS':
                    objeto.cambiar_texto('MOSTRANDO\nCOMIDAS')
                    objeto.datos = 'Comida'
                    comidas.tkraise()
                case 'MOSTRANDO\nCOMIDAS':
                    objeto.cambiar_texto('MOSTRANDO\nOTROS')
                    objeto.datos = 'Otros'
                    otros.tkraise()
                case 'MOSTRANDO\nOTROS':
                    objeto.cambiar_texto('MOSTRANDO\nBEBIDAS')
                    objeto.datos = 'Bebida'
                    bebidas.tkraise()
                case _:
                    mostrar_consumiciones()
        elif objeto.title == 'ordenar':  # en caso de que el boton pulsado sea el de reordenar productos
            modificar_consumiciones(False)
            bebidas.tkraise()
            if not objeto.invertir:
                if not ticket.bloqueado:
                    cambiar_estado_impresion()
                fondo_demandas('red4')
            else:  # activa la opcion añadir productos al ticket
                if ticket.bloqueado:
                    cambiar_estado_impresion()
                fondo_demandas('original')
            objeto.invertir_colores()
        elif lista_marcos_pie_principal[3].invertir:
            if objeto.title == 'modificar':  # en caso de que que el boton pulsado sea el de modificar
                modificar_consumiciones(True)
            elif objeto.title == 'productos':  # en caso de que el boton pulsado sea el de productos
                modo = 'Producto'  # activa el modo Producto
                cont_sec.tkraise()  # trae el panel del teclado virtual al frente
                cont_producto.tkraise()  # trae el panel de producto del teclado virtual al frente
                ventana_aplicacion.teclado = True  # activa la informacion de que se esta usando el teclado principal
                limpiar_productos()  # limpia los widges del modo Producto
                volver.cambiar_texto('Volver')
                cont_sec_modos.tkraise()

def on_click_pie(event):  # actuaciones al evento al pulsar en cualquiera de las opciones del pie del menu pricipal
    event.widget.invertir_colores()
    pulsar_boton_pie(event.widget)

def off_click_pie(event):  # actuaciones al evento al soltar el boton de opciones del pie
    event.widget.invertir_colores()

def crear_impresion(): #creamos el panel que contiene la impresion en el panel principal
    global impresion
    impresion = cont_prin.crear_panel(216, 412, 'gray94')
    impresion.colocar_objeto(dimensiones[0] - impresion.ancho - 5, 351)
    crear_recibo()
    crear_pagos()
    cambiar_estado_impresion()

def extender_panel_impresion():
    if not ticket.bloqueado:
        if ticket.extendido:
            impresion.redimensionar_panel(216,412,dimensiones[0] - impresion.ancho - 5,351)
            ticket.alto=22
        else:
            impresion.redimensionar_panel(216,dimensiones[1]-10,dimensiones[0] - impresion.ancho - 5,5)
            ticket.alto = 45
        ticket.extendido=not ticket.extendido
        ticket.config(height=ticket.alto)
        for x,boton in enumerate(lista_botones_pagos):
            posy = impresion.alto - 70
            posx = x * 70 + 4
            boton.colocar_objeto(posx, posy)

def on_click_impresion(event):
    extender_panel_impresion()

def cambiar_estado_impresion():
    if not ticket.extendido:
        extender_panel_impresion()
    ticket.bloqueado = not ticket.bloqueado
    if ticket.extendido:
        extender_panel_impresion()

def crear_recibo(): #creamos el label recibo del panel principal
    global ticket
    ticket = impresion.crear_ticket(30,22,'')
    ticket.colocar_objeto(0,0)
    ticket.bind("<Button-1>", on_click_impresion)  # obtenemos el evento al pulsar en la tecla

def crear_numericos(): #creamos el panel que contiene el teclado numerico y la pantalla
    global numericos
    numericos=cont_prin.crear_panel(216,346,'grey94')
    numericos.colocar_objeto(dimensiones[0]-numericos.ancho-5,5)
    crear_pantalla()
    crear_teclas()

def crear_pantalla(): #creamos el label del la pantalla del teclado numerico
    global pantalla
    pantalla = numericos.crear_marco(' ', 'Pantalla', 'pantalla', 26,numericos.fondo)
    pantalla.colocar_objeto(0, 0)

def crear_teclas(): #creamos las teclas del teclado numerico
    tnum=['7','8','9','4','5','6','1','2','3','del','0','ok']
    contador=0
    for y in range(4):
        posy=y*70+62
        for x in range(3):
            posx=x*70+3
            tecla = numericos.crear_marco(tnum[contador].upper(), tnum[contador], 'tecla', 20,numericos.fondo)
            tecla.colocar_objeto(posx, posy)
            if not tecla.title.isnumeric():
                tecla.invertir_colores()
            contador += 1
            tecla.bind("<Button-1>", on_click_tecla) #obtenemos el evento al pulsar en la tecla
            tecla.bind("<ButtonRelease-1>", off_click_tecla) #obtenemos el evento al soltar la tecla

def on_click_tecla(event): #actuaciones al evento al pulsar una tecla del teclado del panel principal
    event.widget.invertir_colores()
    crear_importe(event.widget.title) #se interpreta la tecla pulsada

def off_click_tecla(event):  #actuaciones al evento al soltar una tecla del teclado del panel
    event.widget.invertir_colores()

def crear_pagos(): #creamos los botones de forma de pago
    tc=['efectivo','guardar','tarjeta']
    contador=0
    for x in range(len(tc)):
        posy=impresion.alto-70
        posx=x*70+4
        nombre = f'tecla_{tc[contador]}'
        boton = impresion.crear_boton(tc[contador],nombre,'gray94')
        boton.colocar_objeto(posx, posy)
        contador += 1
        lista_botones_pagos.append(boton)
        boton.bind("<Button-1>", on_click_pago) #obtenemos el evento al pulsar en la tecla
        boton.bind("<ButtonRelease-1>", off_click_pago) #obtenemos el evento al soltar la tecla

def on_click_pago(event):  #actuaciones al evento pulsar en un boton de las opciones de pago del ticket
    global diccionario_recibo
    global modo
    global escritura
    event.widget.invertir_colores()
    if event.widget.title == 'guardar': #si pulsamos en guardar
        ventana_aplicacion.teclado = True  # activa la informacion de que se esta usando el teclado principal
        modo = 'Pendiente'  # activa el modo Pendiente
        escritura = 'nombres'
        cont_sec_modos.tkraise()
        limpiar_pendientes()  # limpia los widges del modo Pendiente
        if not diccionario_recibo['pedido']:
            lista_marcos_modo_pendiente[0].title = 'tickets'
            lista_marcos_modo_pendiente[0].cambiar_texto('Tickets')
        elif diccionario_recibo['nombre'] == cabecera_ticket: #para tratar guardar o ticket
            lista_marcos_modo_pendiente[0].title='guardar'
            lista_marcos_modo_pendiente[0].cambiar_texto('Guardar')
        else:
            lista_marcos_modo_pendiente[0].title='comanda'
            lista_marcos_modo_pendiente[0].cambiar_texto('Comanda')
            entrada.cambiar_texto(diccionario_recibo['nombre'])
        cont_sec.tkraise()  # trae el panel del teclado virtual al frente
        cont_pendiente.tkraise() # trae el panel del modo Pendiente del teclado virtual al frente
    else: #si pulsamos en tarjeta o efectivo
        #actualizamos la variable recibo y la guardamos en la base de datos
        if event.widget.title == 'efectivo':
            abrir_caja_registradora(lista_impresoras)
        if diccionario_recibo['pedido']:
            eliminado=False
            if diccionario_recibo['nombre'] != cabecera_ticket:
                eliminado=eliminar_moroso(diccionario_recibo['fecha'])
            diccionario_recibo['nombre']=f'Pagado {event.widget.title}'
            diccionario_recibo['fecha']=datetime.datetime.now().strftime('%d/%m/%Y - %H:%M:%S')
            diccionario_recibo['estado']=event.widget.title
            diccionario_recibo['impreso']=False
            diccionario_recibo['camarero']=camarero_actual.title
            lista_recibos_mensuales.append(copy.deepcopy(diccionario_recibo)) #aqui debemos agregar el pedido a la lista de recibos
            guardar_anual() #Aqui llamar a guardar en la base de datos
            obtener_recibo(datetime.datetime.now().strftime('%d/%m/%Y - %H:%M:%S'))
            ticket.cambiar_texto(actualizar_ticket()) #actualizamos el ticket
            if eliminado:
                actualizar_marcos_recibos_impagados()

def off_click_pago(event):   #actuaciones al evento al soltar un boton de las opciones de pago
    event.widget.invertir_colores()

def crear_bebidas(): #creamos el panel que contiene las bebidas en el planel principal
    global bebidas
    bebidas=cont_prin.crear_panel(dimensiones[0]-232,dimensiones[1]-164,'dark slate gray')
    bebidas.colocar_objeto(5,82)

def crear_comidas(): #creamos el panel que contiene las comidas en el planel principal
    global comidas
    comidas=cont_prin.crear_panel(dimensiones[0]-232,dimensiones[1]-164,'salmon4')
    comidas.colocar_objeto(5,82)

def crear_otros(): #creamos el panel que contiene los otros productos en el planel principal
    global otros
    otros=cont_prin.crear_panel(dimensiones[0]-232,dimensiones[1]-164,'DarkOrange4')
    otros.colocar_objeto(5,82)

def nueva_posicion(x,y):
    x += 157
    if x > 780:
        x = 5
        y += 75
    return x,y

def crear_consumiciones(): #se crean los marcos de cada uno de los prodcutos en su panel correspondiente
    boton=None
    y_b=5
    y_c=y_b
    y_o=y_b
    x_b=5
    x_c=x_b
    x_o=x_b
    # se pueden introducir has 40 registros de cada familia
    """
    for i in range(44):
        if i<len(productos):
            producto=productos[i]
        else:
            producto=productos[0]
    """
    for producto in lista_productos:
        texto=convertir_texto(producto['nombre'])
        match producto['familia']:
            case 'Bebida':
                boton = bebidas.crear_marco(texto.upper(),producto['nombre'],'tecla_marco',12,bebidas.fondo)
                boton.colocar_objeto(x_b, y_b) #dentro del panel bebidas
                x_b,y_b=nueva_posicion(x_b,y_b)
            case 'Comida':
                boton = comidas.crear_marco(texto.upper(),producto['nombre'],'tecla_marco',12,comidas.fondo)
                boton.colocar_objeto(x_c, y_c) #dentro del panel comidas
                x_c, y_c = nueva_posicion(x_c, y_c)
            case 'Otros':
                boton = otros.crear_marco(texto.upper(),producto['nombre'],'tecla_marco',12,otros.fondo)
                boton.colocar_objeto(x_o, y_o) #dentro del panel otros
                x_o,y_o=nueva_posicion(x_o,y_o)
        boton.datos=producto['familia']
        boton.bind("<Button-1>", on_click_demanda) #obtenemos el evento al pulsar en la tecla
        boton.bind("<ButtonRelease-1>", off_click_demanda) #obtenemos el evento al soltar la tecla
        lista_marcos_productos.append(boton)

def mostrar_consumiciones():
    if lista_marcos_pie_principal[1].cget(
            'text') == 'MOSTRAR\nCONSUMICIONES':  # vuelve al panel de consumiciones que se mostraba con anterioridad
        if lista_marcos_pie_principal[1].datos == 'Bebida':
            lista_marcos_pie_principal[1].cambiar_texto('MOSTRANDO\nBEBIDAS')
            bebidas.tkraise()
        elif lista_marcos_pie_principal[1].datos == 'Comida':
            lista_marcos_pie_principal[1].cambiar_texto('MOSTRANDO\nCOMIDAS')
            comidas.tkraise()
        else:
            lista_marcos_pie_principal[1].cambiar_texto('MOSTRANDO\nOTROS')
            otros.tkraise()
        if ticket.bloqueado:
            cambiar_estado_impresion()

def fondo_demandas(color):
    if color=='original':
        for demanda in lista_marcos_productos:
            # actualiza todos los fondos
            match demanda.datos:
                case 'Bebida':
                    demanda.cambiar_fondo('dark slate gray')
                case 'Comida':
                    demanda.cambiar_fondo('salmon4')
                case 'Otros':
                    demanda.cambiar_fondo('DarkOrange4')
        bebidas.cambiar_fondo('dark slate gray')
        comidas.cambiar_fondo('salmon4')
        otros.cambiar_fondo('DarkOrange4')
    else:
        for demanda in lista_marcos_productos:  # actualiza el fondo de las demandas
            demanda.cambiar_fondo(color)
        # actualiza el fondo de los contenedores
        bebidas.cambiar_fondo(color)
        comidas.cambiar_fondo(color)
        otros.cambiar_fondo(color)

def modificar_consumiciones(propio):
    global incremento_decremento
    modificar=True
    if not propio:
        if lista_marcos_pie_principal[0].cget("text") =='AÑADIR\nCONSUMICION':
            modificar=False
    if modificar:
        for demanda in lista_marcos_productos:
            demanda.invertir_colores()
        if lista_marcos_pie_principal[0].cget("text") == 'AÑADIR\nCONSUMICION':
            lista_marcos_pie_principal[0].cambiar_texto('QUITAR\nCONSUMICION')  # activa la opcion quitar productos del ticket
            fondo_demandas('Gray18')
            incremento_decremento = -1  # actualiza la variable para decrementar el producto en el ticket
        else:  # activa la opcion añadir productos al ticket
            fondo_demandas('original')
            lista_marcos_pie_principal[0].cambiar_texto('AÑADIR\nCONSUMICION')
            incremento_decremento = 1  # actualiza la variable para incremetar el producto en el ticket
        mostrar_consumiciones()

def actualizar_consumiciones(): #elimina los marcos existentes de las consumiciones y los crea ya actualizados
    for marco in lista_marcos_productos:
        marco.destroy() #destruye los marcos existentes
    lista_marcos_productos.clear()
    crear_consumiciones() #los vuelve a crear ya actualizados

def intercambiar_posiciones(marco):
    for i,producto in enumerate(lista_productos):
        if producto['nombre']==marco.title:
            if not marco.invertir:
                lista_marcos_impagados_unir.remove(i)
            else:
                lista_marcos_impagados_unir.append(i)
    if len(lista_marcos_impagados_unir)==2:
        lista_productos[lista_marcos_impagados_unir[0]], lista_productos[lista_marcos_impagados_unir[1]] = lista_productos[lista_marcos_impagados_unir[1]], lista_productos[lista_marcos_impagados_unir[0]]
        guardar_datos() #guarda en la base de datos
        lista_marcos_impagados_unir.clear()
        fondo_demandas('red4')
        actualizar_consumiciones()

def crear_impago(): #creamos el panel que contiene el impago de tickets en el planel principal
    global impago
    impago=cont_prin.crear_panel(dimensiones[0]-232,dimensiones[1]-164,'MediumPurple1')
    impago.colocar_objeto(5,82)
    crear_impagos()

def crear_impagos(): #se crean los marcos de cada uno de los prodcutos en su panel correspondiente
    y=5
    x=5
    if lista_marcos_pie_principal[4].cget('text') == 'TICKETS\nPENDIENTES\nDE PAGO':
        boton = impago.crear_marco('CREAR NUEVO\nTICKET', cabecera_ticket, 'tecla_marco', 12, impago.fondo)
        boton.datos = 'Ticket'
        boton.colocar_objeto(x, y)  # dentro del panel impago
        boton.invertir_colores()
        x, y = nueva_posicion(x, y)
        boton.bind("<Button-1>", on_click_moroso)  # obtenemos el evento al pulsar en la tecla
        boton.bind("<ButtonRelease-1>", off_click_moroso)  # obtenemos el evento al soltar la tecla
        lista_marcos_recibos_impagados.append(boton)
    # se pueden introducir has 39 registros de impagados
    for impagado in lista_recibos_impagados:
        texto=convertir_texto(impagado['nombre'])
        boton = impago.crear_marco(texto.upper(),impagado['nombre'],'tecla_marco',12,impago.fondo)
        boton.datos = impagado['fecha']
        boton.colocar_objeto(x, y) #dentro del panel impago
        x,y=nueva_posicion(x,y)
        boton.bind("<Button-1>", on_click_moroso) #obtenemos el evento al pulsar en la tecla
        boton.bind("<ButtonRelease-1>", off_click_moroso) #obtenemos el evento al soltar la tecla
        lista_marcos_recibos_impagados.append(boton)

def on_click_moroso(event):  #actuaciones al evento pulsar en cualquiera de los marcos de las consumiciones
    event.widget.invertir_colores()

def off_click_moroso(event):  #actuaciones al evento al soltar el boton de las consumiciones
    global diccionario_recibo
    event.widget.invertir_colores()
    if lista_marcos_pie_principal[4].cget('text')=='TICKETS\nPENDIENTES\nDE PAGO':
        pantalla.cambiar_texto('')
        diccionario_recibo = obtener_recibo(event.widget.datos)
        if not diccionario_recibo['pedido']:
            cambiar_estado_impresion()
            lista_marcos_pie_principal[4].cambiar_texto('GESTION DE\nTICKETS')
            lista_marcos_pie_principal[1].cambiar_texto('MOSTRANDO\nBEBIDAS')
            bebidas.tkraise()
        ticket.cambiar_texto(actualizar_ticket()) #actualizamos el ticket
    else:
        unir_tickets(event.widget)

def unir_tickets(marco):
    global diccionario_recibo
    lista_marcos_impagados_unir.clear()
    uniones=[]
    for i,impagado in enumerate(lista_recibos_impagados):
        if impagado['nombre']==marco.title:
            lista_marcos_impagados_unir.append(i)
    if len(lista_marcos_impagados_unir)>1:
        for idx in lista_marcos_impagados_unir:
            for pedido in lista_recibos_impagados[idx]['pedido']:
                enc=False
                for union in uniones:
                    if union[1]==pedido[1]:
                        union[0]+=pedido[0]
                        enc=True
                        break
                if not enc:
                    uniones.append(pedido)
        diccionario_recibo = {
            'pedido': uniones,
            'nombre': lista_recibos_impagados[lista_marcos_impagados_unir[0]]['nombre'],
            'fecha': lista_recibos_impagados[lista_marcos_impagados_unir[0]]['fecha'],
            'estado': lista_recibos_impagados[lista_marcos_impagados_unir[0]]['estado'],
            'impreso': False,
            'camarero':camarero_actual.title
        }
        fin = False
        while not fin:
            fin = True
            for impagado in lista_recibos_impagados:
                if impagado['nombre'] == marco.title:
                    lista_recibos_impagados.remove(impagado)
                    fin=False
                    break
        lista_recibos_impagados.append(copy.deepcopy(diccionario_recibo))
        guardar_datos() #guarda en la base de datos
        lista_marcos_impagados_unir.clear()
        actualizar_marcos_recibos_impagados()
        ticket.cambiar_texto(actualizar_ticket())  # actualizamos el ticket

def actualizar_marcos_recibos_impagados(): #elimina los marcos existentes de los impagos y los crea ya actualizados
    for marco in lista_marcos_recibos_impagados:
        marco.destroy() #destruye los marcos existentes
    lista_marcos_recibos_impagados.clear()
    crear_impagos() #los vuelve a crear ya actualizados

def eliminar_moroso(fecha):
    for moroso in lista_recibos_impagados:
        if moroso['fecha']==fecha:
            lista_recibos_impagados.remove(moroso)
            return True
    return False

def obtener_recibo(fecha):
    global diccionario_recibo
    for item in lista_recibos_impagados:
        if item['fecha']==fecha:
            return item
    diccionario_recibo = {
        'pedido': [],
        'nombre': cabecera_ticket,
        'fecha': fecha,
        'estado': 'Nuevo',
        'impreso': False,
        'camarero':camarero_actual.title
    }
    return diccionario_recibo

def on_click_demanda(event):  #actuaciones al evento pulsar en cualquiera de los marcos de las consumiciones
    event.widget.invertir_colores()
    if not lista_marcos_pie_principal[3].invertir:
        intercambiar_posiciones(event.widget)
    else:
        completar_pedido(event.widget.title)
        ticket.cambiar_texto(actualizar_ticket())

def off_click_demanda(event):  #actuaciones al evento al soltar el boton de las consumiciones
    if lista_marcos_pie_principal[3].invertir:
        event.widget.invertir_colores()

def recolocar_barman():
    if camarero_actual.title!='':
        barman.redimensionar_panel(dimensiones[0]-232, dimensiones[1]-164, 5, 82)

def crear_barman(): #creamos el panel que contiene el barman de tickets en el planel principal
    global barman
    barman=cont_prin.crear_panel(dimensiones[0],dimensiones[1],'black')
    barman.colocar_objeto(0,0)
    crear_camareros()

def actualizar_camareros(): #elimina los marcos existentes de los impagos y los crea ya actualizados
    for marco in lista_marcos_camareros:
        marco.destroy() #destruye los marcos existentes
    lista_marcos_camareros.clear()
    crear_camareros() #los vuelve a crear ya actualizados

def crear_camareros(): #se crean los marcos de cada uno de los prodcutos en su panel correspondiente
    y=5
    x=5
    boton = barman.crear_marco('GESTIONAR\nCAMAREROS', 'gestion', 'tecla_marco', 12, barman.fondo)
    boton.colocar_objeto(x, y)  # dentro del panel barman
    boton.invertir_colores()
    x, y = nueva_posicion(x, y)
    boton.bind("<Button-1>", on_click_barman)  # obtenemos el evento al pulsar en la tecla
    boton.bind("<ButtonRelease-1>", off_click_barman)  # obtenemos el evento al soltar la tecla
    lista_marcos_camareros.append(boton)
    # se pueden introducir has 39 registros de impagados
    for empleado in lista_camareros:
        texto=convertir_texto(empleado)
        boton = barman.crear_marco(texto.upper(),empleado,'tecla_marco',12,barman.fondo)
        boton.colocar_objeto(x, y) #dentro del panel barman
        x,y=nueva_posicion(x,y)
        boton.bind("<Button-1>", on_click_barman) #obtenemos el evento al pulsar en la tecla
        boton.bind("<ButtonRelease-1>", off_click_barman) #obtenemos el evento al soltar la tecla
        lista_marcos_camareros.append(boton)

def limpiar_camareros(): #limpia los widges del modo Producto
    entrada.cambiar_texto('')
    primera_mayuscula('Delete')
    cargar_listado()

def on_click_barman(event):  #actuaciones al evento pulsar en cualquiera de los marcos de las consumiciones
    global modo
    global escritura
    global camarero_anterior
    global camarero_actual
    event.widget.invertir_colores()
    if event.widget.title == 'gestion': #si pulsamos en guardar
        ventana_aplicacion.teclado = True  # activa la informacion de que se esta usando el teclado principal
        modo = 'Camarero'  # activa el modo Pendiente
        escritura = 'nombres'
        cont_sec_modos.tkraise()
        limpiar_camareros()  # limpia los widges del modo Camarero
        cont_sec.tkraise()  # trae el panel del teclado virtual al frente
        cont_mesero.tkraise() # trae el panel del modo Pendiente del teclado virtual al frente
    else:
        if event.widget.title!=camarero_actual.title:
            if camarero_actual.title != '':
                camarero_anterior.cambiar_texto(convertir_texto(camarero_actual.title))
                camarero_anterior.title = camarero_actual.title
            camarero_actual.cambiar_texto(event.widget.title)
            camarero_actual.title = event.widget.title
            recolocar_barman()

def off_click_barman(event):  #actuaciones al evento al soltar el boton de las consumiciones
    event.widget.invertir_colores()

def tamanio_recibos():
    # Obtener el tamaño en bytes
    tamano_bytes = sys.getsizeof(lista_recibos_mensuales)
    # Convertir a kilobytes (aproximado)
    tamano_kb = tamano_bytes / 1024
    print("El tamaño de la lista en KB es:", tamano_kb)

def ejecutar_prueba():
    pass
    #crear_archivo_imagenes()
    #recibos.clear()
    #impagados.clear()
    #generador_automatico_tickets(2024)
    #generador_consumiciones()
    #guardar_datos()
    #cont_ter.lower()
    #cont_ter.lift()
    #ingresar_password()
    #cont_sec.lift()
    tamanio_recibos()

def inicializar_variables():
    global lista_impresoras
    lista_impresoras = ['', '']
    global incremento_decremento
    incremento_decremento=1

def cargar_archivos():
    cargar_archivo_imagenes(imagenes)
    cargar_datos() #informacion de la base de datos
    cargar_anual()
def ejecutar(): #funcion que llama a las funciones necesarias para ejecutar el programa
    inicializar_variables()
    cargar_archivos()
    crear_aplicacion() #creamos el total del contenido de la aplicación
    obtener_recibo(datetime.datetime.now().strftime('%d/%m/%Y - %H:%M:%S'))#Muestro ticket nuevo
    ticket.cambiar_texto(actualizar_ticket())  # actualizamos el ticket
    cont_prin.tkraise() # trae el panel principal al frente
    ejecutar_prueba() #este hay que eliminarlo
    ventana_aplicacion.mantener_ventana() # lanza el loop que mantiene la ventana abierta

ejecutar() #ejecutamos la aplicacion