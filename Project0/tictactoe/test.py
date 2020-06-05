#test.py 
#Used to test functions in tictactoe.py

import tictactoe as ttt

#board = ttt.initial_state()

board = [[ttt.EMPTY, ttt.O, ttt.X],
        [ttt.EMPTY, ttt.EMPTY, ttt.X],
        [ttt.EMPTY, ttt.EMPTY, ttt.EMPTY]]

# board = [[ttt.X, ttt.O, ttt.O],
#         [ttt.X, ttt.X, ttt.O],
#         [ttt.O, ttt.X, ttt.EMPTY]]

# board = ttt.result(board, (2, 2))
# print("Result of move (2,2):", board)

who_played = ttt.player(board)
their_actions = ttt.actions(board)

move = ttt.minimax(board)
print("Diag move:", move)
board = ttt.result(board, move)
for i in range(0, 3):
    print(f"AI board[{i}]:", board[i])

#player
print(who_played, "just played")

print("They had these possible Actions:", their_actions)


print("Winner:", ttt.winner(board))

print("Terminal State:", ttt.terminal(board))

print("Utility: ", ttt.utility(board))

#Exception checking
# board = ttt.result(board, (2, 2))
# print("Result of move (2,2)", board)