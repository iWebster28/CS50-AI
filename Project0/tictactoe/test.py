#test.py 
#Used to test functions in tictactoe.py

import tictactoe as ttt

#board = ttt.initial_state()

board = [[ttt.X, ttt.EMPTY, ttt.O],
        [ttt.EMPTY, ttt.EMPTY, ttt.O],
        [ttt.EMPTY, ttt.EMPTY, ttt.EMPTY]]

#player
print(ttt.player(ttt.initial_state()), "plays next")

print(ttt.actions(board))