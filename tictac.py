import random

def play_game():
    # Initialize board
    board = [" " for _ in range(9)]

    def print_board():
        print()
        print(f" {board[0]} | {board[1]} | {board[2]} ")
        print("---+---+---")
        print(f" {board[3]} | {board[4]} | {board[5]} ")
        print("---+---+---")
        print(f" {board[6]} | {board[7]} | {board[8]} ")
        print()

    def check_winner(player):
        win_conditions = [
            [0,1,2],[3,4,5],[6,7,8],
            [0,3,6],[1,4,7],[2,5,8],
            [0,4,8],[2,4,6]
        ]
        for cond in win_conditions:
            if all(board[i] == player for i in cond):
                return True
        return False

    def check_draw():
        return " " not in board

    # Smart AI move
    def ai_move(ai_player, user_player):
        # 1. Can AI win this move?
        for i in range(9):
            if board[i] == " ":
                board[i] = ai_player
                if check_winner(ai_player):
                    print(f"AI chooses position {i + 1} to WIN!")
                    return
                board[i] = " "

        # 2. Can player win next move? Block it
        for i in range(9):
            if board[i] == " ":
                board[i] = user_player
                if check_winner(user_player):
                    board[i] = ai_player
                    print(f"AI chooses position {i + 1} to BLOCK!")
                    return
                board[i] = " "

        # 3. Pick center if free
        if board[4] == " ":
            board[4] = ai_player
            print("AI chooses center (5)")
            return

        # 4. Pick a corner if free
        for i in [0,2,6,8]:
            if board[i] == " ":
                board[i] = ai_player
                print(f"AI chooses corner position {i + 1}")
                return

        # 5. Pick any remaining cell
        empty_cells = [i for i, cell in enumerate(board) if cell == " "]
        move = random.choice(empty_cells)
        board[move] = ai_player
        print(f"AI chooses position {move + 1}")

    # Choose game mode
    mode = ""
    while mode not in ["1", "2"]:
        print("Choose game mode:")
        print("1. Play with Friend")
        print("2. Play with AI")
        mode = input("Enter 1 or 2: ")

    if mode == "2":
        # AI mode
        user_player = ""
        while user_player not in ["X", "O"]:
            user_player = input("Choose your marker (X/O): ").upper()
        ai_player = "O" if user_player == "X" else "X"
        current_player = random.choice([user_player, ai_player])
        print(f"{current_player} starts first!")
    else:
        # 2-player mode
        player1 = "X"
        player2 = "O"
        current_player = random.choice([player1, player2])
        print(f"{current_player} starts first!")

    # Main game loop
    while True:
        print_board()

        if mode == "2":
            if current_player == user_player:
                move = input(f"Your turn ({user_player}), choose position (1-9): ")
                if not move.isdigit() or int(move) < 1 or int(move) > 9:
                    print("Invalid input! Choose 1-9.")
                    continue
                move = int(move) - 1
                if board[move] != " ":
                    print("Cell already occupied! Try again.")
                    continue
                board[move] = user_player
                if check_winner(user_player):
                    print_board()
                    print("Congratulations! You win! ")
                    break
                current_player = ai_player
            else:
                ai_move(ai_player, user_player)
                if check_winner(ai_player):
                    print_board()
                    print("AI wins! Better luck next time ")
                    break
                current_player = user_player

        else:
            if current_player == player1:
                move = input(f"Player 1 ({player1}), choose position (1-9): ")
                if not move.isdigit() or int(move) < 1 or int(move) > 9:
                    print("Invalid input! Choose 1-9.")
                    continue
                move = int(move) - 1
                if board[move] != " ":
                    print("Cell already occupied! Try again.")
                    continue
                board[move] = player1
                if check_winner(player1):
                    print_board()
                    print("Player 1 wins! ")
                    break
                current_player = player2
            else:
                move = input(f"Player 2 ({player2}), choose position (1-9): ")
                if not move.isdigit() or int(move) < 1 or int(move) > 9:
                    print("Invalid input! Choose 1-9.")
                    continue
                move = int(move) - 1
                if board[move] != " ":
                    print("Cell already occupied! Try again.")
                    continue
                board[move] = player2
                if check_winner(player2):
                    print_board()
                    print("Player 2 wins! ")
                    break
                current_player = player1

        if check_draw():
            print_board()
            print("It's a draw! ")
            break

# Main program loop for replay
while True:
    play_game()
    play_again = input("Do you want to play again? (y/n): ").lower()
    if play_again != "y":
        print("Thanks for playing! Goodbye ")
        break
