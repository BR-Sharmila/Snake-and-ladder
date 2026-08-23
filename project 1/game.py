import random

print("==============================")
print("     🐍 SNAKE & LADDER 🎲")
print("==============================")

# Starting positions
player1 = 0
player2 = 0

# Ladders: bottom -> top
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

# Snakes: head -> tail
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

while player1 < 100 and player2 < 100:

    # ---------------- PLAYER 1 ----------------

    input("\nPlayer 1 - Press ENTER to roll the dice...")

    dice = random.randint(1, 6)

    print("🎲 Player 1 rolled:", dice)

    new_position = player1 + dice

    if new_position <= 100:
        player1 = new_position
    else:
        print("Player 1 needs an exact number to reach 100.")

    # Check ladder
    if player1 in ladders:
        print("🪜 LADDER! Player 1 goes from",
              player1, "to", ladders[player1])
        player1 = ladders[player1]

    # Check snake
    elif player1 in snakes:
        print("🐍 SNAKE! Player 1 goes from",
              player1, "to", snakes[player1])
        player1 = snakes[player1]

    print("\n📊 CURRENT SCORE")
    print("----------------")
    print("Player 1:", player1)
    print("Player 2:", player2)

    # Check winner
    if player1 == 100:
        print("\n🏆 PLAYER 1 WINS! 🏆")
        break

    # ---------------- PLAYER 2 ----------------

    input("\nPlayer 2 - Press ENTER to roll the dice...")

    dice = random.randint(1, 6)

    print("🎲 Player 2 rolled:", dice)

    new_position = player2 + dice

    if new_position <= 100:
        player2 = new_position
    else:
        print("Player 2 needs an exact number to reach 100.")

    # Check ladder
    if player2 in ladders:
        print("🪜 LADDER! Player 2 goes from",
              player2, "to", ladders[player2])
        player2 = ladders[player2]

    # Check snake
    elif player2 in snakes:
        print("🐍 SNAKE! Player 2 goes from",
              player2, "to", snakes[player2])
        player2 = snakes[player2]

    print("\n📊 CURRENT SCORE")
    print("----------------")
    print("Player 1:", player1)
    print("Player 2:", player2)

    # Check winner
    if player2 == 100:
        print("\n🏆 PLAYER 2 WINS! 🏆")
        break