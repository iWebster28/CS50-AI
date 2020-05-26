#test.py 
#Used to test functions in tictactoe.py

import tictactoe as ttt

#board = ttt.initial_state()

# board = [[ttt.X, ttt.EMPTY, ttt.O],
#         [ttt.EMPTY, ttt.EMPTY, ttt.O],
#         [ttt.EMPTY, ttt.EMPTY, ttt.EMPTY]]

board = [[ttt.X, ttt.O, ttt.O],
        [ttt.X, ttt.X, ttt.O],
        [ttt.O, ttt.X, ttt.X]]

#player
print(ttt.player(ttt.initial_state()), "plays next")

print("Actions:", ttt.actions(board))

print("Winner:", ttt.winner(board))

print("Terminal State:", ttt.terminal(board))

print("Utility: ", ttt.utility(board))