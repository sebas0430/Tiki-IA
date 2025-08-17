from tkinter import *

# Crear la ventana principal de la aplicación
root = Tk()
root.title("Tic Tac Toe Game")
root.geometry("430x600")  # Ajusta el tamaño de la ventana
root.resizable(False, False)  # Evita que la ventana sea redimensionable

# Crear el contenedor principal del tablero
board = Frame(root, bg="lightblue")
board.pack(expand=True, fill="both") 

# Configurar el borde y el cursor del frame del tablero
board.config(bd=10, relief=RIDGE, cursor="man")

# Crear el título del juego
label = Label(board,
              text="Tic Tac Toe Game",
              bg="lightblue",
              fg="black",
              font=("Arial", 24),
              border=20,
              relief=GROOVE)
label.grid(row=0, column=0, columnspan=3, pady=20)

# Label para mostrar el ganador del juego
winner_label = Label(board,
                     text="",
                     bg="lightblue",
                     fg="black",
                     font=("Arial", 18))
winner_label.grid(row=4, column=0, columnspan=3, pady=10)

# Inicializar el turno del primer jugador
player = "X"

# Label para mostrar de quién es el turno actual
turn_label = Label(board,
                   text=f"Turno: {player}",
                   bg="lightblue",
                   fg="black",
                   font=("Arial", 14))
turn_label.grid(row=5, column=0, columnspan=3, pady=5)

# Crear una matriz para almacenar los botones del tablero
buttons = [[None, None, None],
           [None, None, None],
           [None, None, None]]

# Crear los botones del tablero y asignarles la función de marcar
for i in range(3):
    for j in range(3):
        buttons[i][j] = Button(board,
                               text="",
                               font=("Arial", 24),
                               width=5,
                               height=2,
                               bg="white",
                               fg="black",
                               # Al hacer clic, llama a mark_button con la posición y el jugador actual
                               command=lambda row=i, col=j: mark_button(row, col, player)
                               )
        buttons[i][j].grid(row=i+1, column=j, padx=10, pady=10)

# Función para cambiar el turno del jugador
def change_turn():
    """
    Cambia el turno entre los jugadores 'X' y 'O' y actualiza el label de turno.
    """
    global player
    if player == "X":
        player = "O"
    else:
        player = "X"
    turn_label.config(text=f"Turno: {player}")
    print(f"Current player: {player}")
    return player

# Función para verificar si hay un ganador en el tablero (GUI actual)
def check_winner():
    """
    Verifica si algún jugador ha ganado el juego en la GUI.
    Retorna True si hay un ganador, False en caso contrario.
    """
    # Comprobar filas
    for i in range(3):
        if buttons[i][0]['text'] == buttons[i][1]['text'] == buttons[i][2]['text'] != "":
            print(f"Player {buttons[i][0]['text']} wins!")
            return True

    # Comprobar columnas
    for j in range(3):
        if buttons[0][j]['text'] == buttons[1][j]['text'] == buttons[2][j]['text'] != "":
            print(f"Player {buttons[0][j]['text']} wins!")
            return True

    # Comprobar diagonales
    if buttons[0][0]['text'] == buttons[1][1]['text'] == buttons[2][2]['text'] != "":
        print(f"Player {buttons[0][0]['text']} wins!")
        return True
    if buttons[0][2]['text'] == buttons[1][1]['text'] == buttons[2][0]['text'] != "":
        print(f"Player {buttons[0][2]['text']} wins!")
        return True

    return False

# --- NUEVO: resalta en color la línea ganadora ---
def highlight_winning_line(color="lightgreen"):
    # Filas
    for i in range(3):
        if buttons[i][0]['text'] == buttons[i][1]['text'] == buttons[i][2]['text'] != "":
            for j in range(3):
                buttons[i][j].config(bg=color)
            return
    # Columnas
    for j in range(3):
        if buttons[0][j]['text'] == buttons[1][j]['text'] == buttons[2][j]['text'] != "":
            for i in range(3):
                buttons[i][j].config(bg=color)
            return
    # Diagonal principal
    if buttons[0][0]['text'] == buttons[1][1]['text'] == buttons[2][2]['text'] != "":
        for k in range(3):
            buttons[k][k].config(bg=color)
        return
    # Diagonal secundaria
    if buttons[0][2]['text'] == buttons[1][1]['text'] == buttons[2][0]['text'] != "":
        buttons[0][2].config(bg=color)
        buttons[1][1].config(bg=color)
        buttons[2][0].config(bg=color)
        return

# Función que se ejecuta al hacer clic en un botón del tablero
def mark_button(row, col, current):
    """
    Marca la casilla seleccionada con el símbolo del jugador actual,
    verifica si hay un ganador o empate, y cambia el turno.
    Además, si tras el cambio de turno le toca a la IA (O), realiza su jugada.
    """
    # Si ya hay un ganador o empate, no hacer nada
    if winner_label['text'] != "":
        return

    # Si la casilla está vacía, marcarla
    if buttons[row][col]['text'] == "":
        buttons[row][col].config(text=current)

        # Verificar si hay un ganador
        if check_winner():
            winner_label.config(text=f"¡Ganó {current}!")
            highlight_winning_line()  # <<< NUEVO: resaltar línea
            print(f"Player {current} wins!")
            return

        # Verificar si hay empate (todas las casillas llenas y sin ganador)
        if all(buttons[i][j]['text'] != "" for i in range(3) for j in range(3)):
            winner_label.config(text="¡Empate!")
            print("Draw!")
            return

        # Cambiar turno si no hay ganador ni empate
        change_turn()

        # Si ahora le toca a la IA (O), que juegue
        if winner_label['text'] == "" and player == "O":
            best_move()

# Función para reiniciar el juego y limpiar el tablero
def reset_game():
    """
    Reinicia el juego, limpia el tablero y restablece los labels.
    """
    global player
    player = "X"
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text="", bg="white")  # <<< restaura color también
    winner_label.config(text="")
    turn_label.config(text=f"Turno: {player}")
    print("Game reset. Player X starts again.")

# Botón para reiniciar el juego
reset_button = Button(board,
                      text="Reiniciar Juego",
                      font=("Arial", 14),
                      command=reset_game,
                      bg="red",
                      fg="black")
reset_button.grid(row=6, column=0, columnspan=3, pady=20)

#----------------------------------------------------------------
# parte de IA

def read_state():
    """
    Lee el estado del tablero desde los botones y devuelve una lista 3x3 con 'X', 'O' o ''.
    """
    return [[buttons[i][j]['text'] for j in range(3)] for i in range(3)]

def winner_in_state(state):
    """
    Evalúa un estado (lista 3x3) y devuelve:
    'X' si gana X, 'O' si gana O, 'Draw' si está lleno sin ganador, o None si sigue en juego.
    """
    # Filas
    for i in range(3):
        if state[i][0] == state[i][1] == state[i][2] != "":
            return state[i][0]
    # Columnas
    for j in range(3):
        if state[0][j] == state[1][j] == state[2][j] != "":
            return state[0][j]
    # Diagonales
    if state[0][0] == state[1][1] == state[2][2] != "":
        return state[0][0]
    if state[0][2] == state[1][1] == state[2][0] != "":
        return state[0][2]
    # Empate si no hay vacíos
    if all(state[i][j] != "" for i in range(3) for j in range(3)):
        return "Draw"
    return None

def minimax(state, is_maximizing):
    """
    Minimax puro sobre el estado dado (no usa la GUI).
    Devuelve 1 si favorece a 'O', -1 si favorece a 'X', 0 en empate.
    """
    result = winner_in_state(state)
    if result == 'O':
        return 1
    if result == 'X':
        return -1
    if result == 'Draw':
        return 0

    if is_maximizing:
        best = float('-inf')
        for i in range(3):
            for j in range(3):
                if state[i][j] == "":
                    state[i][j] = 'O'
                    score = minimax(state, False)
                    state[i][j] = ""
                    best = max(best, score)
        return best
    else:
        best = float('inf')
        for i in range(3):
            for j in range(3):
                if state[i][j] == "":
                    state[i][j] = 'X'
                    score = minimax(state, True)
                    state[i][j] = ""
                    best = min(best, score)
        return best

def best_move():
    """
    Calcula y ejecuta la mejor jugada para 'O' en la GUI,
    llamando a mark_button para que respete tu flujo (ganador/empate/turno).
    """
    state = read_state()
    best_score = float('-inf')
    move = None

    for i in range(3):
        for j in range(3):
            if state[i][j] == "":
                state[i][j] = 'O'
                score = minimax(state, False)
                state[i][j] = ""
                if score > best_score:
                    best_score = score
                    move = (i, j)

    if move is not None:
        # Hace la jugada en el tablero real
        mark_button(move[0], move[1], 'O')

# Iniciar el bucle principal de la aplicación
root.mainloop()
