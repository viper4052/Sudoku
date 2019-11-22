
from tkinter import *
from tkinter import font
from tkinter import messagebox
from tkinter import ttk
import random
from time import *
import os

TITULO = 'Sudoku'
ANCHO, ALTO = 900, 750
POS_VENTANA_X, POS_VENTANA_Y = 310, 15

ventana = Tk()
ventana.title(TITULO)
ventana.geometry('{}x{}+{}+{}'.format(ANCHO, ALTO,
                                      POS_VENTANA_X,
                                      POS_VENTANA_Y))
ventana.resizable(width=False, height=False)
ventana.config(bg='#b2bec3')
for i in range(0, 21):
    ventana.columnconfigure(i, weight=1)
    ventana.rowconfigure(i, weight=1)

# ----------------- ICONO -----------------------------
ventana.iconbitmap('sudoku.ico')


# ----------------- FUENTE GLOBAL -----------------------------
CalibriL = font.Font(family='Calibri Light', size=8, weight='bold')

# ------------------- BOOLEANOS GLOBALES ----------------------
var_timer = False
dific_facil = False
dific_inter = False
dific_dificil = False

# ------------------------ TITULO --------------------------
l_sudoku = Label(ventana, text='SUDOKU', bg="#b2bec3",
                 fg='#d63031', font=(CalibriL, 30))
l_sudoku.grid(column=10, row=0, columnspan=1)

# --------------------- DICCIONARIOS DE PARTIDAS -------------------
# OJO GRABAR EN ARCHIVO Y LEER DESDE AHI
dicc_partida_facil = {1: [
    ['5', '3', '', '', '7', '', '', '', ''],
    ['6', '', '', '1', '9', '5', '', '', ''],
    ['', '9', '8', '', '', '', '', '6', ''],
    ['8', '', '', '', '6', '', '', '', '3'],
    ['4', '', '', '8', '', '3', '', '', '1'],
    ['7', '', '', '', '2', '', '', '', '6'],
    ['', '6', '', '', '', '', '2', '8', ''],
    ['', '', '', '4', '1', '9', '', '', '5'],
    ['', '', '', '', '8', '', '', '7', '9']]}
# OJO GRABAR EN ARCHIVO Y LEER DESDE AHI
dicc_partida_intermedio = {1: [
    ['', '', '', '', '8', '', '', '', '6'],
    ['', '9', '4', '', '5', '', '', '', ''],
    ['8', '', '2', '', '', '3', '', '', ''],
    ['', '', '', '8', '3', '', '7', '5', ''],
    ['', '', '', '7', '4', '', '6', '9', ''],
    ['', '3', '', '1', '', '6', '', '', '2'],
    ['', '6', '', '', '', '', '2', '8', ''],
    ['', '', '', '4', '1', '9', '', '', '5'],
    ['3', '4', '', '', '6', '', '8', '2', '']]}
# OJO GRABAR EN ARCHIVO Y LEER DESDE AHI
dicc_partida_dificil = {}


# --------------------- MARCO DE BOTONES --------------------

def zona_de_juego():
    global dific_facil, dific_inter
    probabilidad = random.randint(0, 100)
    # prueba de muestra de tablero
    tablero = 1
    if dific_facil == True:
        if probabilidad < 50:
            tablero = 1
        else:
            tablero = 2
        # agregar condicional para el tercer sudoku
    elif dific_inter == True:
        if probabilidad < 50:
            tablero = 4
        else:
            tablero = 5
    marco_juego = Frame(ventana, width=250, height=250)
    marco_juego.configure(bg='white')
    for i in range(9):
        marco_juego.columnconfigure(i, weight=1)
        marco_juego.rowconfigure(i, weight=1)
    marco_juego.grid(column=3, row=1, sticky=NSEW, columnspan=9, rowspan=9)
    dict = eval(open('sudoku2019partidas.dat').read())
    for x in range(9):
        for y in range(9):
            btn_celda = Button(marco_juego, text=dict[tablero][y][x])
            if dict[tablero][y][x] != '':
                btn_celda.config(state=DISABLED)
            btn_celda.grid(column=x, row=y, sticky=N+S+E+W)


def botones_ventana():
    boton_1 = Button(ventana, text='1', font=(CalibriL, 12), width=6, command=None)
    boton_1.place(x=650, y=122)

    boton_2 = Button(ventana, text='2', font=(CalibriL, 12), width=6, command=None)
    boton_2.place(x=670, y=155)

    boton_3 = Button(ventana, text='3', font=(CalibriL, 12), width=6, command=None)
    boton_3.place(x=690, y=188)

    boton_4 = Button(ventana, text='4', font=(CalibriL, 12), width=6, command=None)
    boton_4.place(x=710, y=221)

    boton_5 = Button(ventana, text='5', font=(CalibriL, 12), width=6, command=None)
    boton_5.place(x=740, y=254)

    boton_6 = Button(ventana, text='6', font=(CalibriL, 12), width=6, command=None)
    boton_6.place(x=710, y=287)

    boton_7 = Button(ventana, text='7', font=(CalibriL, 12), width=6, command=None)
    boton_7.place(x=690, y=320)

    boton_8 = Button(ventana, text='8', font=(CalibriL, 12), width=6, command=None)
    boton_8.place(x=670, y=353)

    boton_9 = Button(ventana, text='9', font=(CalibriL, 12), width=6, command=None)
    boton_9.place(x=650, y=386)

    boton_iniciar_juego = Button(ventana, text='INICIAR JUEGO', bg='#eb2f06', height=2,
                                 command=b_iniciar_juego)
    boton_iniciar_juego.place(x=35, y=520)

    boton_borrar_jugada = Button(ventana, text='BORRAR JUGADA', bg='#81ecec', height=2,
                                 command=None)
    boton_borrar_jugada.place(x=140, y=520)

    boton_terminar_juego = Button(ventana, text='TERMINAR JUEGO', bg='#44bd32', height=2,
                                  command=None)
    boton_terminar_juego.place(x=260, y=520)

    boton_borrar_juego = Button(ventana, text='BORRAR JUEGO', bg='#74b9ff', height=2,
                                command=None)
    boton_borrar_juego.place(x=380, y=520)

    boton_top_10 = Button(ventana, text='TOP 10', bg='#fff200', height=2, width=8,
                          command=None)
    boton_top_10.place(x=490, y=520)

    boton_guardar_partida = Button(ventana, text='GUARDAR PARTIDA', bg='white', command=None)
    boton_guardar_partida.place(x=370, y=590)

    boton_cargar_partida = Button(ventana, text='CARGAR PARTIDA', bg='white', command=None)
    boton_cargar_partida.place(x=500, y=590)
    

# -------------------------- ENTRY JUGADOR -----------------------
jugador_actual = StringVar()


def entry_jugador():
    global jugador_actual
    jugador = Entry(ventana, width=25, font=(CalibriL, 10), bg='azure',
                    textvar=jugador_actual, justify='left')
    jugador.place(x=155, y=590)
    l_jugador = Label(ventana, text='Nombre del jugador: ', bg='#b2bec3',
                      font=(CalibriL, 10))
    l_jugador.place(x=25, y=590)


# ---------------------------- VALIDACIONES BOTONES SIN NUMERO -----------------
def b_iniciar_juego():
    global jugador_actual
    nombre = jugador_actual.get()
    if 0 < len(nombre) < 30:
        pass
        # realizar el guardado de partida con el nombre del jugador
    else:
        messagebox.showerror(title='Error', message='Espacio de jugador debe'
                                                    ' tener entre 1 y 30 caracteres')


# -------------------------- FUNCIONES MENU -----------------------

def menu_jugar():
    zona_de_juego()
    botones_ventana()
    entry_jugador()

def menu_configurar():
    global dific_facil, dific_inter, dific_dificil
    ANCHO2, ALTO2 = 300, 320
    POS_VENTANA_X2, POS_VENTANA_Y2 = 650, 400
    ventanaConfiguracion = Toplevel()
    ventanaConfiguracion.title('Configuración')
    ventanaConfiguracion.geometry('{}x{}+{}+{}'.format(ANCHO2, ALTO2,
                                                       POS_VENTANA_X2, POS_VENTANA_Y2))
    ventanaConfiguracion.resizable(width=False, height=False)
    for i in range(50):
        ventanaConfiguracion.columnconfigure(i, weight=1)
        ventanaConfiguracion.rowconfigure(i, weight=1)

    nb = ttk.Notebook(ventanaConfiguracion)
    nb.grid(row=1, column=0, columnspan=51, rowspan=49, sticky='NESW')

    # Pagina 1 de config
    pagina1 = ttk.Frame(nb)
    nb.add(pagina1, text='Nivel')
    facil_rb = Radiobutton(pagina1, text='Fácil', value='1', variable=1)
    facil_rb.place(x=50, y=80)
    intermedio_rb = Radiobutton(pagina1, text='Intermedio', value='2', variable=2)
    intermedio_rb.place(x=50, y=110)
    dificil_rb = Radiobutton(pagina1, text='Difícil', value='3', variable=3)
    dificil_rb.place(x=50, y=140)

    # Pagina 2 de config
    pagina2 = ttk.Frame(nb)
    nb.add(pagina2, text='Reloj')
    btn_si = StringVar()
    btn_no = StringVar()
    btn_timer = StringVar()
    si_rb = Radiobutton(pagina2, text='Sí', value=4)#, variable=btn_si)
    si_rb.place(x=50, y=80)
    no_rb = Radiobutton(pagina2, text='No', value=5)#, variable=btn_no)
    no_rb.place(x=50, y=110)
    timer_rb = Radiobutton(pagina2, text='Timer', value=6)#, variable=btn_timer)
    timer_rb.place(x=50, y=140)

    #def guarda_cambios():
     #   x = btn_si.get()
     #   y = btn_no.get()
     #   z = btn_timer.get()
     #   print(x, y, z)

    l_tiempo_pref = Label(pagina2, text='HH:MM:SS', font=(CalibriL, 8))
    l_tiempo_pref.place(x=185, y=75)

    horas_str = StringVar()
    horas = Entry(pagina2, width=3, font=(CalibriL, 10), bg='azure',
                  textvar=horas_str, justify='left')
    horas.place(x=170, y=100)

    minut_str = StringVar()
    minut = Entry(pagina2, width=3, font=(CalibriL, 10), bg='azure',
                  textvar=minut_str, justify='left')
    minut.place(x=200, y=100)

    seg_str = StringVar()
    segundos = Entry(pagina2, width=3, font=(CalibriL, 10), bg='azure',
                  textvar=seg_str, justify='left')
    segundos.place(x=230, y=100)

    # Pagina 3 de config
    pagina3 = ttk.Frame(nb)
    nb.add(pagina3, text='Elementos')

    def cambia_dificultad():
        global dific_facil, dific_inter, dific_dificil
        if facil_rb:
            pass

    # --------------------- BOTON APLICAR CONFIGURACION EN CADA PESTANA
    boton_aplicar_dif = Button(pagina1, text='Aplicar', command=None)
    boton_aplicar_dif.place(x=240, y=250)

    boton_aplicar_reloj = Button(pagina2, text='Aplicar', command=None)
    boton_aplicar_reloj.place(x=240, y=250)

    boton_aplicar_elem = Button(pagina3, text='Aplicar', command=None)
    boton_aplicar_elem.place(x=240, y=250)

    ventanaConfiguracion.transient()
    ventanaConfiguracion.grab_set()
    ventana.wait_window(ventanaConfiguracion)


def acerca_de():
    messagebox.showinfo(message="SUDOKU /// "
                                "Version 1.00 /// "
                                "Fecha de creacion: Lunes 18 de Nov, 2019 /// "
                                "Desarrollador: Carlos Barrantes",
                                title="Acerca de")


def salir():
    pregunta = messagebox.askyesno('Salir', '¿Desea salir del programa?')
    if pregunta:
        ventana.destroy()
    else:
        pass


# ---------------------------- MENU ----------------------------------
menubar = Menu(ventana)
ventana.config(menu=menubar)

menubar.add_cascade(label='Jugar', command=menu_jugar)

menubar.add_cascade(label='Configuracion', command=menu_configurar)

menubar.add_cascade(label='Acerca de', command=acerca_de)

menubar.add_cascade(label='Ayuda', command=None)

menubar.add_cascade(label='Salir', command=salir)

ventana.mainloop()


