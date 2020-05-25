"""
Tic Tac Toe Player
"""

import math

#Moves
X = "X"
O = "O"
EMPTY = None

#Empty board
def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


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

    #Support for larger boards
    x_cnt = 0
    o_cnt = 0
    row_len = len(board[0]) 
    col_len = len(board[:][0])

    #Count Xs and Os; next player's turn is who has LEAST count.
    for i in range(0, row_len):
        for j in range(0, col_len):
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

    #(i, j) tuple - where i is row; j is col
    #0, 1, 2

    #Ret any val if terminal board is input
    # if board == terminal(board):
    #     return None

    actions = set()

    #Support for larger boards
    row_len = len(board[0]) 
    col_len = len(board[:][0])

    for i in range(0, row_len):
        for j in range(0, col_len):
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

    #List of winning boards?
    #win_boards = [[EMPTY, EMPTY, EMPTY],
    #        [EMPTY, EMPTY, EMPTY],
     #       [EMPTY, EMPTY, EMPTY]]




    raise NotImplementedError


#Gameover?
def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    #ret true if someone won, or if the board is full
    #to check if board full, need actions(board) right?? but can't call it bc actions calls this fn. Endless loop
    
    #What defines endgame?
    #1. Winner
    #2. There was no winner, and full board 

    #full board: actions = 0, or ... how else? 
    #Can either keep actions here, or terminal there.

    if winner(board) is not None or (winner(board) is None and actions(board) is None)
        return True

    #ret false if game in progress
    else: 
        return False


#Who won?
def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    #X won: utility is 1
    #O won: " is 0
    #Assume utility called on board only if terminal(board) is True
    #(assume game over)


    raise NotImplementedError


#AI
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """




    raise NotImplementedError
