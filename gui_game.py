import tkinter as tk
import random
import math

# =========================================================
# WINDOW
# =========================================================

window = tk.Tk()
window.title("🐍 Snake & Ladder")
window.geometry("650x750")
window.configure(bg="white")

BOARD_SIZE = 500
CELL_SIZE = BOARD_SIZE // 10


# =========================================================
# SNAKES
# =========================================================

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


# =========================================================
# LADDERS
# =========================================================

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


# =========================================================
# PLAYERS
# =========================================================

player1 = 1
player2 = 1
current_player = 1


# =========================================================
# TITLE
# =========================================================

title = tk.Label(
    window,
    text="🐍 SNAKE & LADDER 🪜",
    font=("Arial", 20, "bold"),
    bg="white"
)

title.pack(pady=2)


# =========================================================
# CANVAS
# =========================================================

canvas = tk.Canvas(
    window,
    width=BOARD_SIZE,
    height=BOARD_SIZE,
    bg="white",
    highlightthickness=2,
    highlightbackground="black"
)

canvas.pack()


# =========================================================
# GET POSITION
# =========================================================

def get_center(position):

    row = (position - 1) // 10
    column = (position - 1) % 10

    if row % 2 == 1:
        column = 9 - column

    x = column * CELL_SIZE + CELL_SIZE // 2
    y = (9 - row) * CELL_SIZE + CELL_SIZE // 2

    return x, y


# =========================================================
# DRAW BOARD
# =========================================================

def draw_board():

    canvas.delete("all")

    for position in range(1, 101):

        x, y = get_center(position)

        left = x - CELL_SIZE // 2
        top = y - CELL_SIZE // 2
        right = x + CELL_SIZE // 2
        bottom = y + CELL_SIZE // 2

        if position in ladders:
            color = "#B8F2B8"

        elif position in snakes:
            color = "#FFB6B6"

        elif position % 2 == 0:
            color = "#BFE3FF"

        else:
            color = "#FFF3B0"

        canvas.create_rectangle(
            left,
            top,
            right,
            bottom,
            fill=color,
            outline="black"
        )

        canvas.create_text(
            left + 4,
            top + 4,
            text=str(position),
            anchor="nw",
            font=("Arial", 8, "bold")
        )

    draw_ladders()
    draw_snakes()


# =========================================================
# DRAW LADDERS
# =========================================================

def draw_ladders():

    for start, end in ladders.items():

        x1, y1 = get_center(start)
        x2, y2 = get_center(end)

        dx = x2 - x1
        dy = y2 - y1

        length = math.sqrt(dx * dx + dy * dy)

        if length == 0:
            continue

        px = -dy / length
        py = dx / length

        rail_distance = 7

        # Left rail
        canvas.create_line(
            x1 + px * rail_distance,
            y1 + py * rail_distance,
            x2 + px * rail_distance,
            y2 + py * rail_distance,
            fill="#704214",
            width=4
        )

        # Right rail
        canvas.create_line(
            x1 - px * rail_distance,
            y1 - py * rail_distance,
            x2 - px * rail_distance,
            y2 - py * rail_distance,
            fill="#704214",
            width=4
        )

        # Rungs
        rung_count = max(3, int(length / 25))

        for i in range(1, rung_count):

            ratio = i / rung_count

            cx = x1 + dx * ratio
            cy = y1 + dy * ratio

            canvas.create_line(
                cx + px * rail_distance,
                cy + py * rail_distance,
                cx - px * rail_distance,
                cy - py * rail_distance,
                fill="#9A632F",
                width=3
            )


# =========================================================
# DRAW SNAKES
# =========================================================

def draw_snakes():

    for start, end in snakes.items():

        x1, y1 = get_center(start)
        x2, y2 = get_center(end)

        points = []

        segments = 15

        dx = x2 - x1
        dy = y2 - y1

        length = math.sqrt(dx * dx + dy * dy)

        if length == 0:
            continue

        px = -dy / length
        py = dx / length

        for i in range(segments + 1):

            t = i / segments

            x = x1 + dx * t
            y = y1 + dy * t

            wave = math.sin(t * math.pi * 4) * 8

            x += px * wave
            y += py * wave

            points.extend([x, y])

        canvas.create_line(
            points,
            fill="#228B22",
            width=9,
            smooth=True
        )

        # Snake head
        canvas.create_oval(
            x1 - 9,
            y1 - 9,
            x1 + 9,
            y1 + 9,
            fill="#32A852",
            outline="black"
        )


# =========================================================
# DRAW PLAYERS
# =========================================================

def draw_players():

    canvas.delete("players")

    # Player 1
    x1, y1 = get_center(player1)

    canvas.create_oval(
        x1 - 10,
        y1 - 10,
        x1 + 10,
        y1 + 10,
        fill="red",
        outline="darkred",
        width=2,
        tags="players"
    )

    canvas.create_text(
        x1,
        y1,
        text="1",
        fill="white",
        font=("Arial", 8, "bold"),
        tags="players"
    )

    # Player 2
    x2, y2 = get_center(player2)

    if player1 == player2:
        x2 += 14
        y2 += 14

    canvas.create_oval(
        x2 - 10,
        y2 - 10,
        x2 + 10,
        y2 + 10,
        fill="blue",
        outline="darkblue",
        width=2,
        tags="players"
    )

    canvas.create_text(
        x2,
        y2,
        text="2",
        fill="white",
        font=("Arial", 8, "bold"),
        tags="players"
    )


# =========================================================
# MESSAGE
# =========================================================

message = tk.Label(
    window,
    text="🔴 Player 1's turn",
    font=("Arial", 12, "bold"),
    bg="white"
)

message.pack(pady=1)


# =========================================================
# DICE
# =========================================================

dice_display = tk.Label(
    window,
    text="🎲",
    font=("Arial", 20, "bold"),
    bg="white"
)

dice_display.pack()


# =========================================================
# SCORE
# =========================================================

score_frame = tk.Frame(
    window,
    bg="white"
)

score_frame.pack(pady=1)


player1_score = tk.Label(
    score_frame,
    text="🔴 Player 1: 1",
    font=("Arial", 10, "bold"),
    bg="white"
)

player1_score.pack(side="left", padx=15)


player2_score = tk.Label(
    score_frame,
    text="🔵 Player 2: 1",
    font=("Arial", 10, "bold"),
    bg="white"
)

player2_score.pack(side="left", padx=15)


# =========================================================
# UPDATE SCREEN
# =========================================================

def update_screen():

    draw_board()
    draw_players()

    player1_score.config(
        text=f"🔴 Player 1: {player1}"
    )

    player2_score.config(
        text=f"🔵 Player 2: {player2}"
    )


# =========================================================
# FINISH DICE ROLL
# =========================================================

def finish_roll(dice):

    global player1, player2, current_player

    # PLAYER 1
    if current_player == 1:

        new_position = player1 + dice

        if new_position <= 100:
            player1 = new_position

        if player1 in ladders:

            old_position = player1
            player1 = ladders[player1]

            message.config(
                text=f"🪜 Player 1: {old_position} → {player1}"
            )

        elif player1 in snakes:

            old_position = player1
            player1 = snakes[player1]

            message.config(
                text=f"🐍 Player 1: {old_position} → {player1}"
            )

        else:

            message.config(
                text=f"🎲 Player 1 rolled {dice}"
            )

        update_screen()

        if player1 == 100:

            message.config(
                text="🏆 PLAYER 1 WINS! 🏆"
            )

            roll_button.config(
                state="disabled"
            )

            return

        current_player = 2

        message.config(
            text="🔵 Player 2's turn"
        )


    # PLAYER 2
    else:

        new_position = player2 + dice

        if new_position <= 100:
            player2 = new_position

        if player2 in ladders:

            old_position = player2
            player2 = ladders[player2]

            message.config(
                text=f"🪜 Player 2: {old_position} → {player2}"
            )

        elif player2 in snakes:

            old_position = player2
            player2 = snakes[player2]

            message.config(
                text=f"🐍 Player 2: {old_position} → {player2}"
            )

        else:

            message.config(
                text=f"🎲 Player 2 rolled {dice}"
            )

        update_screen()

        if player2 == 100:

            message.config(
                text="🏆 PLAYER 2 WINS! 🏆"
            )

            roll_button.config(
                state="disabled"
            )

            return

        current_player = 1

        message.config(
            text="🔴 Player 1's turn"
        )

    # Enable button again
    roll_button.config(
        state="normal"
    )


# =========================================================
# DICE ANIMATION
# =========================================================

def animate_dice(count=0):

    # Stop animation
    if count >= 10:

        final_dice = random.randint(1, 6)

        dice_display.config(
            text=f"🎲 {final_dice}"
        )

        window.after(
            300,
            lambda: finish_roll(final_dice)
        )

        return

    # Show random dice number
    number = random.randint(1, 6)

    dice_display.config(
        text=f"🎲 {number}"
    )

    # Continue animation
    window.after(
        80,
        lambda: animate_dice(count + 1)
    )


# =========================================================
# ROLL DICE
# =========================================================

def roll_dice():

    # Prevent clicking while dice is rolling
    roll_button.config(
        state="disabled"
    )

    message.config(
        text="🎲 Rolling..."
    )

    animate_dice()


# =========================================================
# RESTART
# =========================================================

def restart_game():

    global player1, player2, current_player

    player1 = 1
    player2 = 1
    current_player = 1

    dice_display.config(
        text="🎲"
    )

    message.config(
        text="🔴 Player 1's turn"
    )

    roll_button.config(
        state="normal"
    )

    update_screen()


# =========================================================
# BUTTONS
# =========================================================

button_frame = tk.Frame(
    window,
    bg="white"
)

button_frame.pack(pady=2)


roll_button = tk.Button(
    button_frame,
    text="🎲 ROLL DICE",
    font=("Arial", 11, "bold"),
    padx=12,
    pady=4,
    command=roll_dice
)

roll_button.pack(
    side="left",
    padx=4
)


restart_button = tk.Button(
    button_frame,
    text="🔄 RESTART",
    font=("Arial", 11, "bold"),
    padx=12,
    pady=4,
    command=restart_game
)

restart_button.pack(
    side="left",
    padx=4
)


# =========================================================
# START
# =========================================================

update_screen()

window.mainloop()