from math import ceil
from itertools import cycle

# Placeholder for an empty square in the board
EMPTY = " "

# Game board is a tuple of tuples
EMPTY_BOARD = ((EMPTY, EMPTY, EMPTY),
               (EMPTY, EMPTY, EMPTY),
               (EMPTY, EMPTY, EMPTY))

HUMAN = 0
COMPUTER = 1

SYMBOLS = ('X', 'O')

# Iterator toggles between players
turn = cycle((HUMAN, COMPUTER))


def print_intro():
    print("Welcome to Unbeatable Tic-Tac-Toe!")
    print("Proceed without hope...")
    print("")
    print("Player one is: ", SYMBOLS[HUMAN])
    print("Player two is: ", SYMBOLS[COMPUTER])
    print("")
    print("Use the number pad to select your move like so:\n")
    print("7 | 8 | 9")
    print("----------")
    print("4 | 5 | 6")
    print("----------")
    print("1 | 2 | 3")
    print("")
    print("(Note: you may need to press the Num Lock key to activate your numeric keypad)")
    print("")
    print("")
    print("")


def print_board(board):
    print(" | ".join(board[0]))
    print(10*"-")
    print(" | ".join(board[1]))
    print(10*"-")
    print(" | ".join(board[2]))
    print("")
    print("")


def is_valid(num):
    valid_input = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    try:
        if int(num) in valid_input:
            return True
        else:
            return False
    except:
        return False


def square_is_taken(row, col, board):
    return board[row][col] is not " "


def get_move(player, board):
    prompt_text = "Player [" + str(player+1) + "], your turn. Press 1-9 on numpad to select move and hit <ENTER>: "
    num = input(prompt_text)

    # check that number is valid input 1-9
    if not is_valid(num):
        print("\nInvalid input; Please select a number 1-9.\n ")
        print_board(board)
        return get_move(player, board)

    # math to get row/column 0, 1, or 2 from keypad input 1-9
    row = 3 - ceil(int(num) / 3)
    col = ((int(num) % 3) - 1) % 3

    # check that move is not already taken, ask for input again if fails
    if square_is_taken(row, col, board):
        print("\nInvalid move, square is already taken; Please select an available square.\n")
        print_board(board)
        return get_move(player, board)

    return row, col


def apply_move(move, board, player):
    row, col = move
    size = len(board)

    # new tuple with player symbol in place specified by move using tuple concatenation
    new_row = board[row][:col] + (SYMBOLS[player],)
    if col != size-1:
        new_row += board[row][col+1:]

    new_board = board[:row] + (new_row,)
    if row != size-1:
        new_board += board[row+1:]
    return new_board


# Use property of sets to check if all provided game squares are the same and that they are not blanks
def is_win(squares):
    return len(set(squares)) == 1 and EMPTY not in squares


def is_full(board):
    for row in board:
        if EMPTY in row:
            return False
    return True


def get_winner(board):
    size = len(board)

    for row in board:
        if is_win(row):
            return row[0]

    # zip used to effectively get transpose of the board matrix
    for col in zip(*board):
        if is_win(col):
            return col[0]

    diag1 = [board[i][i] for i in range(size)]
    if is_win(diag1):
        return diag1[0]

    diag2 = [board[i][size-(i+1)] for i in range(size)]
    if is_win(diag2):
        return diag2[0]

    # Return None for a tie game
    if is_full(board):
        return None

    # Return False for no conclusion yet
    return False


def get_available_moves(board):
    size = len(board)
    valid_moves = []
    for i in range(size):
        for j in range(size):
            if board[i][j] is EMPTY:
                valid_moves.append((i, j))
    return valid_moves


def get_opponent(player):
    if player is COMPUTER:
        return HUMAN
    else:
        return COMPUTER


def minimax(board, player):
    winner = get_winner(board)
    if winner is SYMBOLS[HUMAN]:
        return -1
    elif winner is SYMBOLS[COMPUTER]:
        return 1
    elif winner is None:
        return 0

    moves = get_available_moves(board)
    scores = [minimax(apply_move(move, board, player), get_opponent(player)) for move in moves]
    if player is COMPUTER:
        score = max(scores)
    else:
        score = min(scores)
    return score


def computers_best(starting_board):
    available_moves = get_available_moves(starting_board)
    possible_boards = [apply_move(move, starting_board, COMPUTER) for move in available_moves]
    scores = {board: minimax(board, HUMAN) for board in possible_boards}
    max_score = max(scores.values())
    for board, score in scores.items():
        if score == max_score:
            return board
    return


def get_next_board(board, player):
    if player is COMPUTER:
        next_board = computers_best(board)
        print("\nCOMPUTER HAS DECIDED...")
    else:
        move = get_move(player, board)
        next_board = apply_move(move, board, player)
        print("\nHUMAN HAS DECIDED...")

    if next_board is None:
        print("FAILURE :'(")
        exit()

    return next_board


def game_turn(board, player):
    print_board(board)
    updated_board = get_next_board(board, player)
    winner = get_winner(updated_board)
    if winner:
        print_board(updated_board)
        print("Player [" + str(player+1) + "] is the WINNER!!! #Sorrynotsorry")
        exit()
    elif winner is None:
        print("DRAW! You just can't win, can  you?")
        exit()
    game_turn(updated_board, next(turn))


def game():
    print_intro()
    game_turn(EMPTY_BOARD, next(turn))


game()
