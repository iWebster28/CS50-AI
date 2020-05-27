#minimax helpers
import math
import tictactoe as ttt

__all__ = ["max_val", "min_val"]

def max_val(board):
	#print("Max")
	if ttt.terminal(board):
		return ttt.utility(board)

	v = -1000000 #float("-inf") #where v is the current best value

	#Find best move for current playable actions
	for action in ttt.actions(board):
		v = max(v, min_val(ttt.result(board, action)))

	return v


def min_val(board):
	#print("Min")
	if ttt.terminal(board):
		return ttt.utility(board)

	v = 1000000 #float("inf")

	for action in ttt.actions(board):
		v = min(v, max_val(ttt.result(board, action)))

	return v