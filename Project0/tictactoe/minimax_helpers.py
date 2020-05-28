#minimax helpers
import math
import tictactoe as ttt

__all__ = ["max_val", "min_val"]

DEPTH_LIM = 7 #Depth-Limited Minimax: Found that 7 works best for speed + effectiveness

def max_val(board, highest_min, lowest_max, depth, max):
	global DEPTH_LIM
	depth += 1

	if ttt.terminal(board):
		return ttt.utility(board)

	v = float("-inf") #where v is the current best value

	#Find best move for current playable actions
	min_value = 0
	for action in ttt.actions(board):
		if (depth == DEPTH_LIM): #Depth limiting
			return v

		min_value = min_val(ttt.result(board, action), highest_min, lowest_max, depth, False)
		
		# if (max == False) and min_value > highest_min: #Alpha/Beta
  #           #highest_min = min_value
  #       	highest_min = min_value

		# if min_value > lowest_max:
		# 	return v #alpha/beta
		v = max(v, min_value)

	return v


def min_val(board, highest_min, lowest_max, depth, max):
	global DEPTH_LIM
	depth += 1

	if ttt.terminal(board):
		return ttt.utility(board)

	v = float("inf")

	max_value = 0
	for action in ttt.actions(board):
		if depth == DEPTH_LIM:
			return v

		max_value = max_val(ttt.result(board, action), highest_min, lowest_max, depth, True)
		
		# if (max == True) and max_value < lowest_max: #Alpha/Beta
  #       	lowest_max = max_value

		# if max_value < highest_min:
		# 	return v #alpha/beta
		v = min(v, max_value)

	return v