from tkinter import *
from tkinter import font
from PIL import ImageTk, Image
import tempfile


imagenes=[]
dimensiones=[]

#Declaracion de las clases

class Ventanas(Tk):

    def __init__(self,titulo,ancho,alto):
        super().__init__()
        self.titulo=titulo
        self.ancho=ancho
        self.alto=alto
        self.icon_path = None
        self.teclado=False
        self.__iniciar_ventana()

    def __iniciar_ventana(self):
        self.title(self.titulo)
        # Crear un archivo temporal para el icono
        self.iconbitmap('icono.ico')
        self.minsize(self.ancho,self.alto)

        #self.geometry(f"{self.ancho}x{self.alto}")#esto hay que cambiarlo por lo de abajo
        '''
        self.overrideredirect(True)  # Ocultar barra de título y bordes
        # Obtener el tamaño de la pantalla y ajustar la ventana
        wd = self.winfo_screenwidth()
        hg = self.winfo_screenheight()
        print(f"{wd}x{hg}")
        self.geometry(f"{wd}x{hg}")
        #poner a pantalla completa
        self.state('zoomed')
        #ocultar raton
        self.config(cursor="none")
        '''

    @staticmethod
    def buscar_imagen(nombre):
        for imagen in imagenes:
            if imagen.filename==nombre:
                return imagen
        return None

    def mantener_ventana(self):
        #mantiene la aplicacion abierta
        self.mainloop()

    def crear_panel(self,wd,hg,fondo):
        return Paneles(self,wd,hg,fondo)


class Paneles(Frame,Ventanas):

    @staticmethod
    def que_figura(texto):
        match texto:
            case 'del':
                c_txt = 'light salmon'
                c_fig = 'red3'
            case 'ok':
                c_txt = 'pale green'
                c_fig = 'forest green'
            case _:
                c_txt = 'gray68'
                c_fig = 'gray18'
        return c_fig,c_txt

    def preparar_imagen(self,nombre):
        imagen = self.buscar_imagen(nombre)
        imagen_tk = ImageTk.PhotoImage(imagen)
        return imagen_tk

    def __init__(self,parent,ancho,alto,fondo):
        super().__init__(parent)
        self.ancho=ancho
        self.alto=alto
        self.fondo=fondo
        self.texto=None
        self.x=None
        self.y=None
        self.__iniciar_objeto()

    def __iniciar_objeto(self):
        self.config(bg=self.fondo,
                    width=self.ancho,
                    height=self.alto)

    def cambiar_fondo(self,color):
        self.fondo=color
        self.config(bg=self.fondo)

    def colocar_objeto(self,x,y):
        self.x=x
        self.y=y
        self.place(x=self.x, y=self.y)

    def expandir_panel(self):
        self.pack(fill=BOTH,
                  expand=True)  # Ocupa el espacio total disponible
        self.pack_propagate(False)  # Evitar que el Frame ajuste su tamaño a los widgets internos

    def recolocar_panel(self,evento):
        self.x = int((evento.width - self.ancho) / 2)
        self.y = int((evento.height - self.alto) / 2)
        if self.x>0 and self.y>0:
            self.place(x=self.x,y=self.y)

    def redimensionar_panel(self,wd,hg,x,y):
        self.ancho=wd
        self.alto=hg
        self.config(width=self.ancho,
                    height=self.alto)
        self.colocar_objeto(x,y)

    def cambiar_texto(self,texto):
        self.texto=texto
        self.config(text=texto)

    def crear_boton(self,title,nombre,color):
        return Botones(self,title,nombre,color)

    def crear_ticket(self,ancho,alto,texto):
        return Tickets(self,ancho,alto,texto)

    def crear_marco(self,texto,title,tipo,letra,fondo):
        return Marcos(self,texto,title,tipo,letra,fondo)

    def crear_etiqueta(self,texto,letra,color,fondo,ancho):
        return Etiquetas(self,texto,letra,color,fondo,ancho)

    def crear_barra(self,posicion,direccion):
        return Barras(self,posicion,direccion)

    def crear_lista(self,posicion,direccion):
        return Listas(self,posicion,direccion)

class Listas(Listbox,Paneles):
    def __init__(self,parent,posicion,direccion):
        super().__init__(parent)
        self.posicion = posicion
        self.direccion = direccion
        self.__iniciar_objeto()

    def __iniciar_objeto(self):
        self.pack(side=self.posicion,
                  fill=self.direccion,
                  expand=True)
        self.place(relx=0, rely=0, relwidth=1, relheight=1)

    def sincronizar_lista(self,barra):
        self.config(font=("Consolas", 14),
                    exportselection=False,
                    yscrollcommand=barra.set)

class Barras(Scrollbar,Paneles):
    def __init__(self,parent,posicion,direccion):
        super().__init__(parent)
        self.posicion=posicion
        self.direccion=direccion
        self.__iniciar_objeto()

    def __iniciar_objeto(self):
        self.pack(side=self.posicion,
                    fill=self.direccion)

    def sincronizar_barra(self,lista):
        self.config(command=lista.yview)


class Etiquetas(Label,Paneles):
    def __init__(self,parent,texto,letra,color,fondo,ancho):
        super().__init__(parent)
        self.fuente = None
        self.texto = texto
        self.title = None
        self.letra=letra
        self.ancho=ancho
        self.alto=1
        self.color=color
        self.fondo=fondo
        self.__iniciar_objeto()

    def __iniciar_objeto(self):
        # Crear un objeto Font para definir la fuente
        self.fuente = font.Font(family="Consolas", size=self.letra, weight="bold")
        # Aplicar la fuente al widget Text
        self.config(font=self.fuente,
                    text=self.texto,
                    width=self.ancho,
                    height=self.alto,
                    bg=self.fondo,
                    foreground=self.color,
                    justify=LEFT)

    def cambiar_largo(self,ancho):
        self.ancho=ancho
        self.config(width=self.ancho)

class Botones(Label,Paneles):

    def __init__(self,parent,title,nombre,color):
        super().__init__(parent)
        self.image = None
        self.texto = None
        self.color = color
        self.invertir=False
        self.title = title
        self.nombre = nombre
        self.__iniciar_objeto()

    def __iniciar_objeto(self):
        imagen_tk=self.preparar_imagen(self.nombre)
        self.config(image=imagen_tk,bg=self.color)
        self.image=imagen_tk

    def __cambiar_imagen(self,nombre):
        imagen_tk = self.preparar_imagen(nombre)
        self.config(image=imagen_tk)
        self.image = imagen_tk

    def invertir_colores(self):
        self.invertir=not self.invertir
        if self.invertir:
            self.__cambiar_imagen(self.nombre + '_p')
        else:
            self.__cambiar_imagen(self.nombre)


class Tickets(Label,Paneles):

    def __init__(self,parent,ancho,alto,texto):
        super().__init__(parent)
        self.fuente = None
        self.texto = texto
        self.alto = alto
        self.extendido=False
        self.bloqueado=False
        self.ancho = ancho
        self.__iniciar_objeto()

    def __iniciar_objeto(self):
        # Crear un objeto Font para definir la fuente
        self.fuente = font.Font(family="Consolas", size=10, weight="bold")
        # Aplicar la fuente al widget Text
        self.config(font=self.fuente,
                    width=self.ancho,
                    height=self.alto,
                    text=self.texto,
                    justify=CENTER,
                    anchor=N)

class Marcos(Label,Paneles):

    def __init__(self,parent,texto,title,nombre,letra,fondo):
        super().__init__(parent)
        self.fuente = None
        self.image = None
        self.title = title
        self.texto = texto
        self.letra = letra
        self.fondo = fondo
        self.datos = ''
        self.invertir=False
        self.color=None
        self.inverso=None
        self.nombre=nombre
        self.pack_propagate(False)
        self.__iniciar_objeto()

    def __iniciar_objeto(self):
        # Crear un objeto Font para definir la fuente
        self.fuente = font.Font(family="Consolas", size=self.letra, weight="bold")
        # Aplicar la fuente al widget Text
        self.config(font=self.fuente,
                    compound="center",
                    text=self.texto,
                    bg=self.fondo,
                    justify=CENTER)
        self.__pintar_marco()

    def __pintar_marco(self):
        self.__tipo_marco()
        if self.invertir:
            self.config(fg=self.color)
            imagen_tk = self.preparar_imagen(self.nombre + '_p')
            self.config(image=imagen_tk)
            self.image = imagen_tk
        else:
            self.config(fg=self.inverso)
            imagen_tk = self.preparar_imagen(self.nombre)
            self.config(image=imagen_tk)
            self.image = imagen_tk

    def invertir_colores(self):
        self.invertir=not self.invertir
        self.__pintar_marco()

    def __tipo_marco(self):
        if self.nombre == 'pantalla':
            self.color='green2'
            self.inverso='green2'
        elif self.nombre == 'info' or self.nombre=='textbox':
            self.color = 'SlateGray3'
            self.inverso = 'SlateGray4'
        else:
            self.color='SlateGray4'
            self.inverso='SlateGray3'




