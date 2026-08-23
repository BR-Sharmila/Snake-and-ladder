import tkinter as tk
import random

# ---------------- WINDOW ----------------

window = tk.Tk()
window.title("🐍 Snake & Ladder")
window.geometry("700x800")
window.configure(bg="white")


# ---------------- TITLE ----------------

title = tk.Label(
    window,
    text="🐍 SNAKE & LADDER 🪜",
    font=("Arial", 24, "bold"),
    bg="white"
)

title.pack(pady=10)


# ---------------- BOARD ----------------

board_frame = tk.Frame(window, bg="black")
board_frame.pack()

cells = {}

for row in range(10):

    for col in range(10):

        if row % 2 == 0:
            number = row * 10 + col + 1
        else:
            number = row * 10 + (9 - col) + 1

        cell = tk.Label(
            board_frame,
            text=str(number),
            width=6,
            height=3,
            font=("Arial", 10, "bold"),
            relief="solid",
            borderwidth=1,
            bg="lightyellow"
        )

        cell.grid(row=9 - row, column=col)

        cells[number] = cell


# ---------------- MESSAGE ----------------

message = tk.Label(
    window,
    text="Player 1's turn",
    font=("Arial", 16, "bold"),
    bg="white"
)

message.pack(pady=10)


# ---------------- PLAYERS ----------------

player1 = 1
player2 = 1

current_player = 1


# ---------------- SNAKES ----------------

snakes = {
    17: 7,
    54: 34,
    62: 19,
    64: 60,
    87: 24,
    93: 73,
    95: 75,
    99: 78
}


# ---------------- LADDERS ----------------

ladders = {
    4: 14,
    9: 31,
    20: 38,
    28: 84,
    40: 59,
    51: 67,
    63: 81,
    71: 91
}


# ---------------- PLAYER PIECES ----------------

player1_piece = tk.Label(
    board_frame,
    text="🔴",
    font=("Arial", 18),
    bg="lightyellow"
)

player2_piece = tk.Label(
    board_frame,
    text="🔵",
    font=("Arial", 18),
    bg="lightyellow"
)


# ---------------- MOVE PLAYER ----------------

def move_player(piece, position):

    row = 9 - ((position - 1) // 10)

    column = (position - 1) % 10

    if ((position - 1) // 10) % 2 == 1:
        column = 9 - column

    piece.grid(
        row=row,
        column=column
    )


# ---------------- ROLL DICE ----------------

def roll_dice():

    global player1, player2, current_player

    dice = random.randint(1, 6)

    # -------- PLAYER 1 --------

    if current_player == 1:

        new_position = player1 + dice

        if new_position <= 100:
            player1 = new_position

        # Ladder
        if player1 in ladders:

            old_position = player1
            player1 = ladders[player1]

            message.config(
                text=f"🪜 LADDER! Player 1: {old_position} → {player1}"
            )

        # Snake
        elif player1 in snakes:

            old_position = player1
            player1 = snakes[player1]

            message.config(
                text=f"🐍 SNAKE! Player 1: {old_position} → {player1}"
            )

        else:

            message.config(
                text=f"🎲 Player 1 rolled {dice} | Position: {player1}"
            )

        move_player(player1_piece, player1)

        # Winner
        if player1 == 100:

            message.config(
                text="🏆 PLAYER 1 WINS! 🏆"
            )

            roll_button.config(state="disabled")

            return

        current_player = 2


    # -------- PLAYER 2 --------

    else:

        new_position = player2 + dice

        if new_position <= 100:
            player2 = new_position

        # Ladder
        if player2 in ladders:

            old_position = player2
            player2 = ladders[player2]

            message.config(
                text=f"🪜 LADDER! Player 2: {old_position} → {player2}"
            )

        # Snake
        elif player2 in snakes:

            old_position = player2
            player2 = snakes[player2]

            message.config(
                text=f"🐍 SNAKE! Player 2: {old_position} → {player2}"
            )

        else:

            message.config(
                text=f"🎲 Player 2 rolled {dice} | Position: {player2}"
            )

        move_player(player2_piece, player2)

        # Winner
        if player2 == 100:

            message.config(
                text="🏆 PLAYER 2 WINS! 🏆"
            )

            roll_button.config(state="disabled")

            return

        current_player = 1


# ---------------- ROLL BUTTON ----------------

roll_button = tk.Button(
    window,
    text="🎲 ROLL DICE",
    font=("Arial", 16, "bold"),
    padx=20,
    pady=10,
    command=roll_dice
)

roll_button.pack(pady=10)


# ---------------- START ----------------

window.mainloop()