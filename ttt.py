#!/usr/bin/python
__author__ = "Camtr0n (Cameron Moore)"

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

VALID_MOVES = {1, 2, 3, 4, 5, 6, 7, 8, 9}
VALID_GAMETYPES = {0, 1, 2}

# Iterator toggles between players
turn = cycle((0, 1))


def print_intro():
    print("Welcome to Unbeatable Tic-Tac-Toe!")
    print("Proceed without hope...")
    print("")
    print("Player one is: ", SYMBOLS[0])
    print("Player two is: ", SYMBOLS[1])
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


def is_valid(num, valid):
    try:
        if int(num) in valid:
            return True
        else:
            return False
    except:
        return False


def get_game_type():
    print("This game can be played in the following configurations:")
    print("[0] Human vs. Human")
    print("[1] Human vs. Computer")
    print("[2] Computer vs. Computer")
    print("")
    game_type = input("Enter the number corresponding to the game type you would like to play: ")
    if not is_valid(game_type, VALID_GAMETYPES):
        return get_game_type()

    if game_type is 0:
        player_types = (HUMAN, HUMAN)
    elif game_type is 1:
        player_types = (HUMAN, COMPUTER)
    else:
        player_types = (COMPUTER, COMPUTER)

    return player_types


def square_is_taken(row, col, board):
    return board[row][col] is not " "


def get_move(player, board):
    prompt_text = "Player [" + str(player+1) + "], your turn. Press 1-9 on numpad to select move and hit <ENTER>: "
    num = input(prompt_text)

    # check that number is valid input 1-9
    if not is_valid(num, VALID_MOVES):
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
    if player is 0:
        return 1
    else:
        return 0


# Expect each score to contain a point value and a depth value
def score_max(scores):
    best = (-2, 10)
    for score in scores:
        s = score[0]
        d = score[1]
        if s > best[0] or (s == best[0] and d <= best[1]):
            best = score
    return best


def score_min(scores):
    best = (2, 10)
    for score in scores:
        s = score[0]
        d = score[1]
        if s < best[0] or (s == best[0] and d <= best[1]):
            best = score
    return best


def minimax(initiator, board, player, depth):
    winner = get_winner(board)
    if winner is SYMBOLS[get_opponent(initiator)]:
        return -1, depth
    elif winner is SYMBOLS[initiator]:
        return 1, depth
    elif winner is None:
        return 0, depth

    available_moves = get_available_moves(board)

    scores = [minimax(initiator, apply_move(move, board, player), get_opponent(player), depth + 1) for move in available_moves]
    if player is initiator:
        score = score_max(scores)
    else:
        score = score_min(scores)
    return score


def computers_best(starting_board, player):
    available_moves = get_available_moves(starting_board)
    size = len(starting_board)

    # Always take center square if it is available
    if ((size-1)/2, (size-1)/2) in available_moves:
        return apply_move(((size-1)/2, (size-1)/2), starting_board, player)

    # Depth in game decision tree that computer's move is starting from
    depth = size*size - len(available_moves)

    possible_boards = [apply_move(move, starting_board, player) for move in available_moves]

    scores = {board: minimax(player, board, get_opponent(player), depth+1) for board in possible_boards}

    max_score = score_max(scores.values())
    for board, score in scores.items():
        if score == max_score:
            return board
    return


def get_next_board(board, player, player_types):
    if player_types[player] is COMPUTER:
        next_board = computers_best(board, player)
        print("\nCOMPUTER HAS DECIDED...")
    else:
        move = get_move(player, board)
        next_board = apply_move(move, board, player)
        print("\nHUMAN HAS DECIDED...")

    if next_board is None:
        print("FAILURE :'(")
        exit()

    return next_board


def game_turn(board, player, player_types):
    print_board(board)
    updated_board = get_next_board(board, player, player_types)
    winner = get_winner(updated_board)
    if winner:
        print_board(updated_board)
        print("Player [" + str(player+1) + "] is the WINNER!!! #Sorrynotsorry")
        exit()
    elif winner is None:
        print_board(updated_board)
        print("DRAW! You just can't win, can  you?")
        exit()
    game_turn(updated_board, next(turn), player_types)


def game():
    print_intro()
    player_types = get_game_type()
    game_turn(EMPTY_BOARD, next(turn), player_types)


game()
