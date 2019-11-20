
from tkinter import *
from tkinter import font
import tkinter.messagebox
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
ventana.iconbitmap(r'sudoku.ico')



# ----------------- FUENTE GLOBAL -----------------------------
CalibriL = font.Font(family='Calibri Light', size=8, weight='bold')


# ------------------------ TITULO --------------------------
l_sudoku = Label(ventana, text='SUDOKU', bg="#b2bec3",
                 fg='#d63031', font=(CalibriL, 30))
l_sudoku.grid(column=10, row=0, columnspan=1)



# --------------------- MARCO DE BOTONES --------------------

def zona_de_juego():
    marco_juego = Frame(ventana, width=250, height=250)
    marco_juego.configure(bg='white')
    for i in range(81):
        marco_juego.columnconfigure(i, weight=1)
        marco_juego.rowconfigure(i, weight=1)
    marco_juego.grid(column=3, row=1, sticky=NSEW, columnspan=9, rowspan=9)
    botones_ventana()
    entry_jugador()


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
                                 command=None)
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
    jugador = Entry(ventana, width=30, font=(CalibriL, 10), bg='azure',
                        textvar=jugador_actual, justify='left')
    jugador.place(x=140, y=590)
    l_jugador = Label(ventana, text='Nombre del jugador: ', bg='#b2bec3',
                      font=(CalibriL, 10))
    l_jugador.place(x=25, y=590)



# ---------------------------- MENU ----------------------------------
menubar = Menu(ventana)
ventana.config(menu=menubar)

menubar.add_cascade(label='Jugar', command=zona_de_juego)

menubar.add_cascade(label='Configuracion', command=None)

menubar.add_cascade(label='Acerca de', command=None)

menubar.add_cascade(label='Ayuda', command=None)

menubar.add_cascade(label='Salir', command=None)







ventana.mainloop()


