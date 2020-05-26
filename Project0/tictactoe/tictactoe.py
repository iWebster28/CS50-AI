"""
Tic Tac Toe Player
"""

import math

#Moves
X = "X"
O = "O"
EMPTY = None

#Board Dimensions
DIM = 3


#Empty board
def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


#Is the board full?
def full(board):
    for i in range(0, DIM):
        for j in range(0, DIM):
            if board[i][j] == EMPTY:
                return False
    return True


#Who plays next? - Implemented
def player(board):
    """
    Returns player who has the next turn on a board.
    """

    #X has first move in intial board state
    if board == initial_state():
        return X
    
    #Return any val if terminal board is the input board.
    if terminal(board):
        return X

    x_cnt = 0
    o_cnt = 0

    #Count Xs and Os; next player's turn is who has LEAST count.
    for i in range(0, DIM):
        for j in range(0, DIM):
            if board[i][j] == X:
                x_cnt += 1
            elif board[i][j] == O:
                o_cnt += 1
    
    return X if (x_cnt < o_cnt) else O #return smaller, or O as default.


#Where can anyone move?
def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    #(i, j) tuple - where i is row; j is col; range 0, 1, 2

    #Ret any val if terminal board is input
    if board == terminal(board):
        return None

    actions = set()

    for i in range(0, DIM):
        for j in range(0, DIM):
            if board[i][j] == EMPTY:
                actions.add((i, j))

    return actions


#New board state after move?
def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    #Deepcopy the board!!
    #Don't modify original board (bc Minimix requires diff board states!)
    #Raise exception is action not valid


    raise NotImplementedError


#Who won?
def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    #X wins: ret X; O wins, ret O
    #At most 1 winner
    #no winner: ret none

    count = 0 #Track how many Xs or Os per line

    #Code designed for custom grid size (ex: > 3x3 grid)

    #Horizontal wins
    for row in range(1, DIM):
        for col in range(1, DIM):
            if board[row][col] == board[row][col - 1]:
                count += 1
                winner = board[row][col]
            else:
                break #SHOULD BREAK OUT OF 1 LOOP ONLY
    
    if count == DIM:
        return winner

    #Vertical Wins
    count = 0
    for col in range(1, DIM):
        for row in range(1, DIM):
            if board[row][col] == board[row - 1][col]:
                count += 1
                winner = board[row][col]
            else:
                break 
                
    if count == DIM:
        return winner

    #Diagonal wins (top left to bottom right)
    for x in range(1, DIM):
        if board[x][x] == board[x - 1][x - 1]:
            count += 1
            winner = board[x][x]
        else:
            break

    if count == DIM:
        return winner

    #Diagonal wins (top right to bottom left)
    for row in range(1, DIM):
        list_range = list(range(0, DIM - 1))
        list_range.reverse()
        for col in list_range:
            if board[row][col] == board[row - 1][col + 1]:
                count += 1
                winner = board[row][col]
            else:
                break

    if count == DIM:
        return winner

    return None

#Gameover?
def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    #ret true if someone won, or if the board is full
    
    #What defines endgame?
    #1. Winner
    #2. There was no winner, and full board 

    #full board: actions = 0, or just check board is EMPTY

    if winner(board) is not None or full(board):
        return True

    #ret false if game in progress
    else: 
        return False


#Who won?
def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    #Assume utility called on board only if terminal(board) is True
    #(assume game over)

    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1

    return 0


#AI
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """




    raise NotImplementedError
