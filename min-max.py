class jugador:
    def __init__(self, nombre, simbolo,turno):
        self.nombre = nombre
        self.simbolo = simbolo
        self.turno = turno

class NodoJugada:
    def __init__(self, tablero, jugador):
        self.tablero = tablero
        self.jugador = jugador  # 'X' o 'O'
        self.hijos = []  # Lista de nodos hijos
        self.valor = None


def cambio_turno(jugador1, jugador2):
    if jugador1.turno:
        jugador1.turno = False
        jugador2.turno = True
    else:
        jugador1.turno = True
        jugador2.turno = False 
    
def condiciones_ganadoras(tablero):
    # Comprobar filas
    for fila in tablero:
        if fila[0] != "" and fila[0] == fila[1] == fila[2]:
            return True
    
    # Comprobar columnas
    for col in range(3):
        if tablero [0][col] != "" and tablero[0][col] == tablero[1][col] == tablero[2][col]:
            return True
        
    # Comprobar diagonales
    if tablero[1][1] != "" and tablero[0][0] == tablero[1][1] == tablero[2][2] or tablero[0][2] == tablero[1][1] == tablero[2][0]:
        return True
    
    # Si no hay ganador
    return False


def mapa ():
    return [["","",""], ["","",""],["","",""]]
    
def marcar_jugada(mapa, fila, columna, simbolo):
    try:
        if mapa[fila][columna] == "":
            mapa[fila][columna] = simbolo
            return True
        else:
            print("La casilla ya está ocupada. Intente de nuevo.")
            return False
    except IndexError:
        print("Posición fuera del rango. Intente de nuevo.")
        return False
    
INF = float('inf')

def lineas_de(tablero):
    return [
        tablero[0], tablero[1], tablero[2],                      # filas
        [tablero[0][0], tablero[1][0], tablero[2][0]],          # columnas
        [tablero[0][1], tablero[1][1], tablero[2][1]],
        [tablero[0][2], tablero[1][2], tablero[2][2]],
        [tablero[0][0], tablero[1][1], tablero[2][2]],          # diagonales
        [tablero[0][2], tablero[1][1], tablero[2][0]],
    ]

def ganador_simbolo(tablero, s):
    return any(all(c == s for c in L) for L in lineas_de(tablero))

def tablero_lleno(tablero):
    return all(tablero[i][j] != "" for i in range(3) for j in range(3))

def terminal_y_utilidad(tablero, max_s, min_s):
    # +1 si gana MAX, -1 si gana MIN, 0 si empate, None si no terminal
    if ganador_simbolo(tablero, max_s): return True, 1
    if ganador_simbolo(tablero, min_s): return True, -1
    if tablero_lleno(tablero):          return True, 0
    return False, None

def sucesores(tablero, s):
    # Genera (movimiento, nuevo_tablero) para cada casilla vacía
    for i in range(3):
        for j in range(3):
            if tablero[i][j] == "":
                hijo = [fila[:] for fila in tablero]
                hijo[i][j] = s
                yield (i, j), hijo

def minimax(tablero, es_max, max_s, min_s):
    terminal, util = terminal_y_utilidad(tablero, max_s, min_s)
    if terminal:
        return util, None

    if es_max:
        mejor_val, mejor_mov = -INF, None
        for mov, hijo in sucesores(tablero, max_s):
            val, _ = minimax(hijo, False, max_s, min_s)
            if val > mejor_val:
                mejor_val, mejor_mov = val, mov
        return mejor_val, mejor_mov
    else:
        mejor_val, mejor_mov = INF, None
        for mov, hijo in sucesores(tablero, min_s):
            val, _ = minimax(hijo, True, max_s, min_s)
            if val < mejor_val:
                mejor_val, mejor_mov = val, mov
        return mejor_val, mejor_mov
             
if __name__ == "__main__":
    print("¡Bienvenido al juego de Triki!\n")

    nombre_jugador1 = input("Ingrese el nombre del Jugador 1: ")
    jugador1 = jugador(nombre_jugador1, 'X', True)
    
    nombre_jugador2 = input("Ingrese el nombre del Jugador 2: ")
    jugador2 = jugador(nombre_jugador2, 'O', False)

    jugadas = 0
    sigue = False
    tablero = mapa()

    while jugadas < 9:
        for fila in tablero:
            print(" | ".join(fila))
        print("\n")

        
        turno = jugador1 if jugador1.turno else jugador2

        if turno is jugador2:  # IA = MAX
            max_s, min_s = jugador2.simbolo, jugador1.simbolo, mov = minimax(map, True, max_s, min_s)
            fila, columna = mov
            print(f"IA juega: fila {fila+1}, columna {columna+1}")
            marcar = marcar_jugada(map, fila, columna, max_s)
        
        #print(f"Turno de {turno.nombre} ({turno.simbolo})")
        else:  # Jugador humano
            columna = int(input("ingrese la columna: "))
            fila = int(input("ingrese la fila: "))
            if jugador1.turno:
                simbolo = jugador1.simbolo
            else:
                simbolo = jugador2.simbolo

        marcar = marcar_jugada(tablero, fila, columna, simbolo)
        print(sigue)

        sigue = condiciones_ganadoras(tablero)

        if jugadas >= 4:
            if sigue:
                break
               
        if marcar == True:
            cambio_turno(jugador1, jugador2)
            jugadas += 1

        print(jugadas)
    if (jugadas == 9 ):
        print("El juego ha terminado en empate.")
    if sigue == True:
        print(f"¡{turno.nombre} ha ganado!")
        for fila in tablero:
            print(" | ".join(fila))
        print("\n")
        print(f"Simbolo ganador: {turno.simbolo}")
        print(f"Jugadas totales: {jugadas + 1}")


    
 
    
   