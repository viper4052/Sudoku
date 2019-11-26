
from tkinter import *
from tkinter import font
from tkinter import messagebox
from tkinter import ttk
import pickle
import random
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

# ------------------- SUDOKU USADO EN EL MOMENTO ----------------------
sudoku = []

# ------------------- lista con datos para top 10 ----------------------
dicc_top_10 = {}

# ------------------- VARIABLES GLOBALES ------------------------------
n_row = 0
n_column = 0
numero_actual = ''
dict_tablero = eval(open('sudoku2019partidas.dat').read())

# ------------------- BOOLEANOS GLOBALES ----------------------
var_timer_arriba = True
var_timer_abajo = False
dific_facil = True
dific_inter = False
dific_dificil = False
cont = 0
var_juego_en_curso = False
var_coloca = True
var_carga = False
tablero = 1
sudoku_inicial = dict_tablero[tablero]
sudoku = dict_tablero[tablero]
pila_coord_jugadas = []

# ------------------------ TITULO --------------------------
l_sudoku = Label(ventana, text='SUDOKU', bg="#b2bec3",
                 fg='#d63031', font=(CalibriL, 30))
l_sudoku.grid(column=10, row=0, columnspan=1)


# --------------------- MARCO DE BOTONES --------------------
def elige_dificultad():
    '''
    E: Nada
    S: Numero de tablero
    R: Nada
    D: Con esta funcion se eligen
       los tableros a utilizar dependiendo
       de la dificultad definida
    '''
    global tablero, dific_dificil, dific_inter, dific_facil
    probabilidad = random.randint(0, 100)
    if dific_facil:
        if probabilidad < 50:
            tablero = 1
        else:
            tablero = 2
    elif dific_inter:
        if probabilidad < 50:
            tablero = 4
        else:
            tablero = 5
    elif dific_dificil:
        if probabilidad < 50:
            tablero = 6
        else:
            tablero = 7
    return tablero

def zona_de_juego(sudoku):
    '''
    E: Sudoku a utilizar
    S: Marco de botones
    R: N/A
    D: Esta funcion permite construir
       el marco de juego en base al tablero
       anteriormente definido
    '''
    global dific_facil, dific_inter, dific_dificil, dict_tablero, var_juego_en_curso, var_carga, tablero


    marco_juego = Frame(ventana, width=250, height=250)
    for i in range(9):
        marco_juego.columnconfigure(i, weight=1)
        marco_juego.rowconfigure(i, weight=1)
    marco_juego.grid(column=3, row=1, sticky=NSEW, columnspan=9, rowspan=9)

    def construye_sudoku():
        '''
        E: N/A
        S: Marco de botones
        R: N/A
        D: Utilizando el sudoku anteriormente
           llamado, se construye un marco de botones
           donde las posiciones originales del marco
           son inmutables
        '''
        global sudoku
        for x in range(9):
            for y in range(9):
                btn_celda = Button(marco_juego, text=sudoku[y][x], command=lambda row=y, column=x: coloca_num(row, column))
                if sudoku[y][x] != '':
                    btn_celda.config(state=DISABLED)
                btn_celda.grid(column=x, row=y, sticky=NSEW)

    if var_juego_en_curso:
        construye_sudoku()
    else:
        elige_dificultad()


# coloca numero si la logica del sudoku lo permite
def coloca_num(y, x):
    '''
    E: Coordenadas del botón dentro del marco de botones
    S: El nuevo marco de botones modificado por el jugador
    R: El numero seleccionado por el usuario no puede encontrarse
       en la misma fila, columna o cuadrante
    D: Esta es la funcion que anida otras que ayudam a definir si
       es posible colocar el numero seleccionado por el usuario
       en la matriz de botones
    '''
    global numero_actual, var_juego_en_curso, sudoku, var_coloca, n_row, n_column, pila_coord_jugadas
    n_row = y
    n_column = x

    def valida_cuadrante(y, x):
        '''
        E: Coordenadas de botones
        S: Lista con coordenadas del cuadrante del botón
        R: N/A
        D: Esta funcion realiza un análisis acerca de la posicion del
           botón de acuerdo con las coordenadas provistas y deja una lista
           con las otras coordenadas del cuadrante del botón para validar
           si se puede poner el numero en dicha posición.
        '''
        global sudoku, numero_actual
        lista = []
        if y in [0, 1, 2] and x in [0, 1, 2]:
            i = range(0, 3)
            j = range(0, 3)
        elif y in [3, 4, 5] and x in [0, 1, 2]:
            i = range(3, 6)
            j = range(0, 3)
        elif y in [6, 7, 8] and x in [0, 1, 2]:
            i = range(6, 9)
            j = range(0, 3)
        elif y in [0, 1, 2] and x in [3, 4, 5]:
            i = range(0, 3)
            j = range(3, 6)
        elif y in [3, 4, 5] and x in [3, 4, 5]:
            i = range(3, 6)
            j = range(3, 6)
        elif y in [6, 7, 8] and x in [3, 4, 5]:
            i = range(6, 9)
            j = range(3, 6)
        elif y in [0, 1, 2] and x in [6, 7, 8]:
            i = range(0, 3)
            j = range(6, 9)
        elif y in [3, 4, 5] and x in [6, 7, 8]:
            i = range(3, 6)
            j = range(6, 9)
        elif y in [6, 7, 8] and x in [6, 7, 8]:
            i = range(6, 9)
            j = range(6, 9)

        for indice in i:
            for indice2 in j:
                lista.append(sudoku[indice][indice2])
        return lista

    if var_juego_en_curso and var_coloca:
        for i in range(9):
            if numero_actual in valida_cuadrante(n_row, n_column):
                messagebox.showwarning('Error', 'Número ya está en el cuadrante')
                break
            if numero_actual not in sudoku[y]:
                if numero_actual not in sudoku[0][x]:
                    if numero_actual not in sudoku[1][x]:
                        if numero_actual not in sudoku[2][x]:
                            if numero_actual not in sudoku[3][x]:
                                if numero_actual not in sudoku[4][x]:
                                    if numero_actual not in sudoku[5][x]:
                                        if numero_actual not in sudoku[6][x]:
                                            if numero_actual not in sudoku[7][x]:
                                                if numero_actual not in sudoku[8][x]:
                                                    sudoku[y][x] = numero_actual
                                                    pila_coord_jugadas.append([y, x])
                                                    var_juego_en_curso = True
                                                    if valida_estado(sudoku):
                                                        messagebox.showinfo('¡Felicidades!', '¡Ganaste el juego!')
                                                    else:
                                                        zona_de_juego(sudoku)
                                                    break
                                                else:
                                                    messagebox.showwarning('Error', 'No se puede colocar en la columna!')
                                                    break
                                            else:
                                                messagebox.showwarning('Error', 'No se puede colocar en la columna!')
                                                break
                                        else:
                                            messagebox.showwarning('Error', 'No se puede colocar en la columna!')
                                            break
                                    else:
                                        messagebox.showwarning('Error', 'No se puede colocar en la columna!')
                                        break
                                else:
                                    messagebox.showwarning('Error', 'No se puede colocar en la columna!')
                                    break
                            else:
                                messagebox.showwarning('Error', 'No se puede colocar en la columna!')
                                break
                        else:
                            messagebox.showwarning('Error', 'No se puede colocar en la columna!')
                            break
                    else:
                        messagebox.showwarning('Error', 'No se puede colocar en la columna!')
                        break
                else:
                    messagebox.showwarning('Error', 'No se puede colocar en la columna!')
                    break
            else:
                messagebox.showwarning('Error', 'No se puede colocar en la fila!')
                break
    else:
        messagebox.showwarning('Error', 'El juego no ha comenzado')


def cambia_numero_actual(numero):
    '''
    E: variable numero
    S: Numero nuevo
    R: N/A
    D: Aquí se cambia el valor del numero a colocar
       en el marco de juego por el usuario.
    '''
    global numero_actual
    numero_actual = numero


def elimina_jugada():
    '''
    E: N/A
    S: Tablero de juego con la jugada reciente, eliminada
    R: La longitud de la pila de coordenadas no debe ser 0
    D: Esta funcion agarra los ultimos valores del último
       botón agregado y si el usuario la utiliza, puede ir
       eliminando cada movimiento que realizó.
    '''
    global var_coloca, sudoku, pila_coord_jugadas
    if len(pila_coord_jugadas) != 0:
        nueva_columna = pila_coord_jugadas[-1][-1]
        nueva_fila = pila_coord_jugadas[-1][-2]
        sudoku[nueva_fila][nueva_columna] = ''
        zona_de_juego(sudoku)
        pila_coord_jugadas.pop(-1)
        print(pila_coord_jugadas)

    else:
        messagebox.showerror('Error', 'No hay más jugadas para borrar')


def borrar_juego():
    '''
    E: N/A
    S: Tablero original vacío
    R: el juego debe estar en curso
    D: Esta funcion realiza un limpiado
       del tablero de juego como si fuera
       a comenzar de nuevo a jugar.
    '''
    global sudoku
    global tablero
    global dict_tablero
    global var_juego_en_curso
    global var_juego_en_curso
    if var_juego_en_curso:
        dict_tablero = eval(open('sudoku2019partidas.dat').read())
        sudoku = dict_tablero[tablero]
        var_juego_en_curso = True
        zona_de_juego(sudoku)
    else:
        messagebox.showerror('Error', 'No se ha iniciado el juego')


def terminar_juego():
    '''
    E: N/A
    S: Nuevo juego de la misma dificultad
    R: El usuario debe haber elegido "sí"
    D: Se comienza una nueva partida de cero y de la
       misma dificultad que el usuario anteriormente
       realizaba
    '''
    global tablero, sudoku, dific_facil, dific_inter, dific_dificil, var_juego_en_curso
    pregunta = messagebox.askyesno('Terminar', '¿Desea terminar el juego?')

    if pregunta:
        if dific_facil:
            tablero = random.randint(1, 2)
        elif dific_inter:
            tablero = random.randint(3, 5)
        elif dific_dificil:
            tablero = random.randint(6, 8)
        sudoku = dict_tablero[tablero]
        var_juego_en_curso = False
        zona_de_juego(sudoku)


def botones_ventana():
    '''
    E: N/A
    S: Botones en ventana
    R: N/A
    D: Aquí se construyen los botones y se llaman
       sus funciones respectivas.
    '''
    boton_1 = Button(ventana, text='1', font=(CalibriL, 12), width=6, command=lambda: cambia_numero_actual('1'))
    boton_1.place(x=650, y=122)

    boton_2 = Button(ventana, text='2', font=(CalibriL, 12), width=6, command=lambda: cambia_numero_actual('2'))
    boton_2.place(x=670, y=155)

    boton_3 = Button(ventana, text='3', font=(CalibriL, 12), width=6, command=lambda: cambia_numero_actual('3'))
    boton_3.place(x=690, y=188)

    boton_4 = Button(ventana, text='4', font=(CalibriL, 12), width=6, command=lambda: cambia_numero_actual('4'))
    boton_4.place(x=710, y=221)

    boton_5 = Button(ventana, text='5', font=(CalibriL, 12), width=6, command=lambda: cambia_numero_actual('5'))
    boton_5.place(x=740, y=254)

    boton_6 = Button(ventana, text='6', font=(CalibriL, 12), width=6, command=lambda: cambia_numero_actual('6'))
    boton_6.place(x=710, y=287)

    boton_7 = Button(ventana, text='7', font=(CalibriL, 12), width=6, command=lambda: cambia_numero_actual('7'))
    boton_7.place(x=690, y=320)

    boton_8 = Button(ventana, text='8', font=(CalibriL, 12), width=6, command=lambda: cambia_numero_actual('8'))
    boton_8.place(x=670, y=353)

    boton_9 = Button(ventana, text='9', font=(CalibriL, 12), width=6, command=lambda: cambia_numero_actual('9'))
    boton_9.place(x=650, y=386)

    boton_iniciar_juego = Button(ventana, text='INICIAR JUEGO', bg='#eb2f06', height=2,
                                 command=b_iniciar_juego)
    boton_iniciar_juego.place(x=35, y=520)

    boton_borrar_jugada = Button(ventana, text='BORRAR JUGADA', bg='#81ecec', height=2,
                                 command=lambda: elimina_jugada())
    boton_borrar_jugada.place(x=140, y=520)

    boton_terminar_juego = Button(ventana, text='TERMINAR JUEGO', bg='#44bd32', height=2,
                                  command=lambda: terminar_juego())
    boton_terminar_juego.place(x=260, y=520)

    boton_borrar_juego = Button(ventana, text='BORRAR JUEGO', bg='#74b9ff', height=2,
                                command=lambda: borrar_juego())
    boton_borrar_juego.place(x=380, y=520)

    boton_top_10 = Button(ventana, text='TOP 10', bg='#fff200', height=2, width=8,
                          command=None)
    boton_top_10.place(x=490, y=520)

    boton_guardar_partida = Button(ventana, text='GUARDAR PARTIDA', bg='white', command=lambda: guarda_partida())
    boton_guardar_partida.place(x=370, y=590)

    boton_cargar_partida = Button(ventana, text='CARGAR PARTIDA', bg='white', command=lambda: carga_partida())
    boton_cargar_partida.place(x=500, y=590)


# -------------------------- ENTRY JUGADOR --------------------------------------
jugador_actual = StringVar()


def entry_jugador():
    '''
    E: N/A
    S: Entry en ventana
    R: N/A
    D: Construye un espacio para que el jugador
       escriba su nombre
    '''
    global jugador_actual
    jugador = Entry(ventana, width=25, font=(CalibriL, 10), bg='azure',
                    textvar=jugador_actual, justify='left')
    jugador.place(x=155, y=590)
    l_jugador = Label(ventana, text='Nombre del jugador: ', bg='#b2bec3',
                      font=(CalibriL, 10))
    l_jugador.place(x=25, y=590)


# ---------------------------- VALIDACIONES BOTONES SIN NUMERO -----------------
def b_iniciar_juego():
    '''
    E: N/A
    S: Juego iniciado
    R: El jugador debe haber escrito su nombre
    D: Esta funcion permite comenzar el juego de Sudoku
       si el campo del nombre de jugador está lleno. Comienza
       el temporizador en el caso que lo decidiera activar.
    '''
    global jugador_actual, var_juego_en_curso, var_timer_abajo, var_timer_arriba
    nombre = jugador_actual.get()
    if 0 < len(nombre) < 30:
        var_juego_en_curso = True
        zona_de_juego(sudoku)
        print(jugador_actual, var_juego_en_curso, var_timer_abajo, var_timer_arriba)
        if var_timer_arriba:
            temporizador_arriba()
        elif var_timer_abajo:
            temporizador_abajo()
        # realizar el guardado de partida con el nombre del jugador
    else:
        messagebox.showerror(title='Error', message='Espacio de jugador debe'
                                                    ' tener entre 1 y 30 caracteres')


# -------------------------- FUNCIONES MENU -----------------------------------

def menu_jugar():
    '''
    E: None
    S: Aparece el marco de juego
    R: N/A
    D: Ejecuta las funciones de aparición de
       widgets en ventana
    '''
    zona_de_juego(sudoku)
    botones_ventana()
    entry_jugador()


def menu_configurar():
    '''
    E: N/A
    S: Widget notebook
    R: N/A
    D: Despliega una pequeña ventana
       donde el usuario puede configurar
       el juego a su gusto.
    '''
    global dific_facil, dific_inter, dific_dificil, cont, var_timer_arriba, var_timer_abajo
    var_timer_arriba = False
    var_timer_abajo = False
    ANCHO2, ALTO2 = 300, 320
    POS_VENTANA_X2, POS_VENTANA_Y2 = 650, 400
    ventanaConfiguracion = Toplevel()
    ventanaConfiguracion.title('Configuración')
    ventanaConfiguracion.geometry('{}x{}+{}+{}'.format(ANCHO2, ALTO2,
                                                       POS_VENTANA_X2, POS_VENTANA_Y2))
    ventanaConfiguracion.resizable(width=False, height=False)
    ventanaConfiguracion.iconbitmap('configuracion.ico')

    for i in range(50):
        ventanaConfiguracion.columnconfigure(i, weight=1)
        ventanaConfiguracion.rowconfigure(i, weight=1)

    nb = ttk.Notebook(ventanaConfiguracion)
    nb.grid(row=1, column=0, columnspan=51, rowspan=49, sticky='NESW')

    # Pagina 1 de config
    pagina1 = ttk.Frame(nb)
    nb.add(pagina1, text='Nivel')
    facil_rb = Radiobutton(pagina1, text='Fácil', value=1, command=lambda: dificultad_facil())
    facil_rb.select()
    facil_rb.place(x=50, y=80)
    intermedio_rb = Radiobutton(pagina1, text='Intermedio', value=2, command=lambda: dificultad_intermedia())
    intermedio_rb.selection_clear()
    intermedio_rb.place(x=50, y=110)
    dificil_rb = Radiobutton(pagina1, text='Difícil', value=3, command=lambda: dificultad_dificil())
    dificil_rb.selection_clear()
    dificil_rb.place(x=50, y=140)



    # Pagina 2 de config
    pagina2 = ttk.Frame(nb)
    nb.add(pagina2, text='Reloj')

    si_rb = Radiobutton(pagina2, text='Sí', value=4, command=lambda: muestra_temporizador_arriba())
    si_rb.select()
    si_rb.place(x=50, y=80)
    no_rb = Radiobutton(pagina2, text='No', value=5, command=lambda: oculta_temporizador())
    no_rb.deselect()
    no_rb.place(x=50, y=110)
    timer_rb = Radiobutton(pagina2, text='Timer', value=6, command=lambda: muestra_temporizador_abajo())
    timer_rb.deselect()
    timer_rb.place(x=50, y=140)

    l_tiempo_pref = Label(pagina2, text='HH:MM:SS', font=(CalibriL, 8))
    l_tiempo_pref.place(x=185, y=75)

    horas_str = StringVar()
    horas_str.set('01')
    entry_horas = Entry(pagina2, width=3, font=(CalibriL, 10), bg='azure',
                        textvar=horas_str, justify='left')
    entry_horas.place(x=170, y=100)

    minut_str = StringVar()
    minut_str.set('30')
    entry_minut = Entry(pagina2, width=3, font=(CalibriL, 10), bg='azure',
                        textvar=minut_str, justify='left')
    entry_minut.place(x=200, y=100)

    seg_str = StringVar()
    seg_str.set('00')
    entry_segundos = Entry(pagina2, width=3, font=(CalibriL, 10), bg='azure',
                           textvar=seg_str, justify='left')
    entry_segundos.place(x=230, y=100)

    def nuevo_reloj():
        global timer, horas, minutos, segundos
        horas = entry_horas.get()
        minutos = entry_minut.get()
        segundos = entry_segundos.get()
        timer.set(str(horas)+':'+str(minutos)+':'+str(segundos))

    # Pagina 3 de config
    pagina3 = ttk.Frame(nb)
    nb.add(pagina3, text='Elementos')

    # --------------------- BOTON APLICAR CONFIGURACION --------------------------------------

    boton_aplicar_reloj = Button(pagina2, text='Aplicar a temporizador', command=lambda: nuevo_reloj())
    boton_aplicar_reloj.place(x=150, y=130)

    ventanaConfiguracion.transient()
    ventanaConfiguracion.grab_set()
    ventana.wait_window(ventanaConfiguracion)
# ------------------------------------------------------------------------


def dificultad_facil():
    '''
    E: N/A
    S: Nueva zona de juego con dificultad facil
    R: N/A
    D: Cambia la dificultad a "Facil"
    '''
    global dific_facil, dific_inter, dific_dificil
    dific_facil = True
    dific_inter = False
    dific_dificil = False
    zona_de_juego(sudoku)


def dificultad_intermedia():
    '''
    E: N/A
    S: Nueva zona de juego con dificultad intermedia
    R: N/A
    D: Cambia la dificultad a "Intermedio"
    '''
    global dific_facil, dific_inter, dific_dificil
    dific_facil = False
    dific_inter = True
    dific_dificil = False
    zona_de_juego(sudoku)


def dificultad_dificil():
    '''
    E: N/A
    S: Nueva zona de juego con dificultad dificil
    R: N/A
    D: Cambia la dificultad a "Dificil"
    '''
    global dific_facil, dific_inter, dific_dificil
    dific_facil = False
    dific_inter = False
    dific_dificil = True
    zona_de_juego(sudoku)

def guarda_dificultad():
    pass

timer = StringVar()
timer.set('00:00:00')
l_timer = Label(ventana, textvariable=timer, font=(CalibriL, 18))
l_timer.config(bg='#b2bec3')


def temporizador_arriba():
    '''
    E: N/A
    S: label timer aumenta en valor
    R: El juego debe estar en marcha
    D: Esta funcion activa el reloj ascendente
       en valor
    '''
    global var_timer_arriba, var_timer_abajo, cont, var_juego_en_curso
    var_timer_arriba = True
    var_timer_abajo = False
    var_juego_en_curso = True

    def resetear():
        '''
        E: N/A
        S: timer queda inicializado en ceros
        R: N/A
        D: El reloj queda en ceros
        '''
        global cont
        cont = 1
        timer.set('00:00:00')

    def iniciar():
        '''
        E: N/A
        S: Ejecuta la funcion de iniciar el timer
        R: N/A
        D: Comienza el timer
        '''
        global cont
        cont = 0
        iniciar_timer()

    def temporizador():
        '''
        E: N/A
        S: label timer aumenta en valor
        R: Contador debe ser 0
        D: Esta es la logica de un reloj
           iniciado en ceros que aumenta
           en valor.
        '''
        global cont
        if cont == 0:
            tiempo = str(timer.get())
            h, m, s = map(int, tiempo.split(':'))
            h = int(h)
            m = int(m)
            s = int(s)
            if s < 59:
                s += 1
            elif s == 59:
                s = 0
                if m < 59:
                    m += 1
                elif m == 59:
                    h += 1
            if h < 10:
                h = str(0)+str(h)
            else:
                h = str(h)
            if m < 10:
                m = str(0)+str(m)
            else:
                m = str(m)
            if s < 10:
                s = str(0)+str(s)
            else:
                s = str(s)
            tiempo = h + ':' + m + ':' + s
            timer.set(tiempo)

            if cont == 0:
                ventana.after(930, iniciar_timer)

    def iniciar_timer():
        '''
        E: N/A
        S: Funcion timer
        R: N/A
        D: Solo ejecuta el timer
        '''
        temporizador()

    def stop():
        '''
        E: N/A
        S: Contador cambia a 1
        R: N/A
        D: Cambia la variable global contador a 1
        '''
        global cont
        cont = 1

    if var_juego_en_curso:
        iniciar_timer()
    else:
        stop()


horas = 0
minutos = 0
segundos = 0


def temporizador_abajo():
    '''
    E: N/A
    S: Temporizador comenzado
    R: Juego debe estar en curso
    D: Contiene las funciones para
       realizar un temporizador cuenta atras
    '''
    global var_timer_arriba, var_timer_abajo, cont, var_juego_en_curso, timer
    var_timer_arriba = False
    var_timer_abajo = True
    var_juego_en_curso = True

    def resetear():
        global cont
        cont = 1
        timer.set('00:00:00')

    def temporizador(h=int(horas), m=int(minutos), s=int(segundos)):
        '''
        E: horas, minutos y segundos
        S: Label timer actualizado
        R: N/A
        D: Logica de un temporizador cuenta atras
        '''
        global proceso
        global horas
        global minutos
        global segundos
        global timer

        if s <= 0:
            s = 59
            m = m - 1
            if m <= 0:
                m = 0
                h = h - 1
                if h <= 0:
                    h = 0
        tiempo = str(h) + ":" + str(m) + ":" + str(s)
        timer.set(tiempo)
        proceso = l_timer.after(1000, temporizador, (h), (m), (s - 1))
        horas = h
        minutos = m
        segundos = s

    def stop():
        '''
        E: N/A
        S: Contador con valor 1
        R: N/A
        D: Solo cambia la variable global contador a 1
        '''
        global cont
        cont = 1

    if var_juego_en_curso:
        global cont
        cont = 0
        temporizador()
    else:
        stop()


def muestra_temporizador_arriba():
    '''
    E: N/A
    S: Cambia booleanos, temporizador arriba a True
    R: N/A
    D: Muestra el label del temporizador hacia arriba
    '''
    global var_timer_arriba, var_timer_abajo
    var_timer_arriba = True
    var_timer_abajo = False
    l_timer.place(x=85, y=650)
    print(var_timer_arriba)


def muestra_temporizador_abajo():
    '''
    E: N/A
    S: Cambia booleanos, temporizador abajo a True
    R: N/A
    D: Muestra el label del temporizador hacia abajo
    '''
    global var_timer_abajo, var_timer_arriba
    var_timer_arriba = False
    var_timer_abajo = True
    l_timer.place(x=85, y=650)


def oculta_temporizador():
    '''
    E: N/A
    S: Cambia ambos booleanos de temporizador a False
    R: N/A
    D: Esconde el label de cualquier temporizador
    '''
    global var_timer_arriba, var_timer_abajo
    var_timer_arriba = False
    var_timer_abajo = False
    l_timer.place_forget()


def guarda_partida():
    '''
    E: N/A
    S: Archivo de guardado de datos
    R: N/A
    D: Guarda cada dato necesario para la partida en un
       archivo binario
    '''
    global sudoku
    global jugador_actual
    global horas
    global minutos
    global segundos
    global dict_tablero
    archivo = open('sudoku2019juegoactual.dat', 'wb')
    pickle.dump(sudoku, archivo)
    pickle.dump(jugador_actual.get(), archivo)
    pickle.dump(horas, archivo)
    pickle.dump(minutos, archivo)
    pickle.dump(segundos, archivo)
    pickle.dump(dict_tablero, archivo)
    archivo.close()


def carga_partida():
    '''
    E: N/A
    S: Carga tablero a zona de juego
    R: N/A
    D: Lee de un archivo binario un tablero
       en el que luego se basa para construir
       un tablero de juego
    '''
    global sudoku
    global jugador_actual
    global horas
    global minutos
    global segundos
    global dict_tablero
    if FileNotFoundError:
        messagebox.showerror('Error', 'No hay partida guardada')
    else:
        archivo = open('sudoku2019juegoactual.dat', 'rb')
        sudoku = pickle.load(archivo)
        jugador_actual = pickle.load(archivo)
        horas = pickle.load(archivo)
        minutos = pickle.load(archivo)
        segundos = pickle.load(archivo)
        dict_tablero = pickle.load(archivo)
        archivo.close()
        zona_de_juego(sudoku)


def valida_estado(sudoku):
    '''
    E: N/A
    S: True o False
    R: Que '' no esté en ninguna parte del sudoku
    D: Verifica si el juego sigue en pie o si
       el jugador logró completar el sudoku
    '''
    if '' not in sudoku[0]:
        if '' not in sudoku[1]:
            if '' not in sudoku[2]:
                if '' not in sudoku[3]:
                    if '' not in sudoku[4]:
                        if '' not in sudoku[5]:
                            if '' not in sudoku[6]:
                                if '' not in sudoku[7]:
                                    if '' not in sudoku[8]:
                                        return True
        else:
            return False


# ----------------------------------------------------


def acerca_de():
    '''
    E: N/A
    S: Messagebox de informacion
    R: N/A
    D: Muestra al usuario informacion
       vital del programa
    '''
    messagebox.showinfo(message="SUDOKU /// "
                                "Version 1.00 /// "
                                "Fecha de creacion: Lunes 18 de Nov, 2019 /// "
                                "Desarrollador: Carlos Barrantes",
                                title="Acerca de")


def abrir_manual():
    '''
    E: N/A
    S: Archivo PDF
    R: N/A
    D: Abre el archivo pdf del manual
       de usuario
    '''
    os.system('manual_de_usuario_Sudoku.pdf')


def salir():
    '''
    E: N/A
    S: Cierra programa o continua
    R: N/A
    D: Permite al usuario salir del programa
       si lo desea. Si no, puede continuar.
    '''
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

menubar.add_cascade(label='Ayuda', command=abrir_manual)

menubar.add_cascade(label='Salir', command=salir)

ventana.mainloop()
