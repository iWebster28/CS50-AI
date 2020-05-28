"""
Tic Tac Toe Player
"""

import math
import copy
from exceptions import TransitionError
import minimax_helpers as mmh #bad to have cyclical dependence??

#Moves
X = "X"
O = "O"
EMPTY = None
TURN = X

#Square Board Dimensions
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

    global TURN

    #X has first move in intial board state
    if board == initial_state():
        return X
    
    #Return any val if terminal board is the input board.
    if terminal(board):
        return X

    # if TURN == X: #prev/existing turn
    #     TURN = O #new/next turn
    # else:
    #     TURN = X
    # print("Turn:", TURN)
    # return TURN

    x_cnt = 0
    o_cnt = 0

    #Count Xs and Os; next player's turn is who has LEAST count.
    for i in range(0, DIM):
        for j in range(0, DIM):
            if board[i][j] == X:
                x_cnt += 1
            elif board[i][j] == O:
                o_cnt += 1\

    if (x_cnt < o_cnt) or (x_cnt == o_cnt):
        return X
    return O
    

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

    #EDGE CASE: no ACTIONS
    if action == None:
        return board

    new_board = copy.deepcopy(board)

    #Check for playable space  
    if (new_board[action[0]][action[1]] == EMPTY): #Redundant; in runner.py
        new_board[action[0]][action[1]] = player(new_board)
        return new_board
    else:
        raise TransitionError(board, new_board, "Action invalid")


#Who won?
def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    #X wins: ret X; O wins, ret O
    #At most 1 winner
    #no winner: ret none


    #Code designed for custom grid size (ex: > 3x3 grid)

    #Horizontal wins
    for row in range(0, DIM):
        count = 0 #Track how many Xs or Os per line
        for col in range(1, DIM):
            if board[row][col] == board[row][col - 1]:
                count += 1
                winner = board[row][col]
                if count == DIM - 1: #only DIM - 1 comparisons made
                    return winner
            else:
                break 
    

    #Vertical Wins
    for col in range(0, DIM):
        count = 0 #Reset for each col check
        for row in range(1, DIM):
            if board[row][col] == board[row - 1][col]:
                # print(f"board[{row}][{col}]:", board[row][col])
                # print(f"board[{row - 1}][{col}]:", board[row - 1][col])
                count += 1
                winner = board[row][col]
                if count == DIM - 1:
                    return winner
            else:
                break 
                
    #Diagonal wins (top left to bottom right)
    count = 0
    for x in range(1, DIM):
        if board[x][x] == board[x - 1][x - 1]:
            count += 1
            winner = board[x][x]
        else:
            break

    if count == DIM - 1:
        return winner

    #Diagonal wins (top right to bottom left)
    count = 0
    row = list(range(1, DIM))
    col = list(range(0, DIM - 1))
    col.reverse()

    for i in range(0, DIM - 1):
        if board[row[i]][col[i]] == board[row[i] - 1][col[i] + 1]:
            count += 1
            winner = board[row[i]][col[i]]
            # print(f"board[{row[i]}][{col[i]}]:", board[row[i]][col[i]])
            # print(f"board[{row[i] - 1}][{col[i] + 1}]:", board[row[i] - 1][col[i] + 1])
        else:
            break

    if count == DIM - 1:
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

    v = float("inf")
    lowest_max = float("inf")
    highest_min = float("-inf")
    depth = 0


    #Computer is O
    if player(board) == O: #want to minimize score
        for action in actions(board):
            max_val = mmh.max_val(result(board, action), highest_min, lowest_max, depth, False)

            if max_val < lowest_max: #Alpha/Beta
                lowest_max = max_val

            if (max_val < v): #minimize score
                best_move = action
            v = min(v, max_val)
            
        print(best_move)
        return best_move


    v = float("-inf")

    #Computer is X
    if player(board) == X: #want to maximize score
        for action in actions(board):
            min_val = mmh.min_val(result(board, action), highest_min, lowest_max, depth, True)

            if min_val > highest_min: #Alpha/Beta
                highest_min = min_val

            if (min_val > v): #maximize score
                best_move = action
            v = max(v, min_val)

            
            
        print(best_move)
        return best_move

    #return mmh.min_val(board) if (player(board) == O) else mmh.max_val(board)

    #raise NotImplementedError
