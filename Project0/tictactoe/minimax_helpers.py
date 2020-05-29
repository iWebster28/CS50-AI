#minimax helpers
import math
import tictactoe as ttt

__all__ = ["max_val", "min_val"]

DEPTH_LIM = 7 #Depth-Limited Minimax: Found that 7 works best for speed + effectiveness

def max_val(board, highest_min, lowest_max, depth, maxBool):
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

		min_value = min_val(ttt.result(board, action), 
					highest_min, lowest_max, depth, maxBool) #was false
		
		#If maximizing, track the highest_min in the top tier (this applies more to the min_val FN)
		#maxBool == True means we're maximizing.
		# if (maxBool == True) and (min_value > highest_min): #Alpha/Beta
		# 	highest_min = min_value


		# #return immediately if 
		# if min_value > lowest_max:
		# 	return max(v, min_value) #alpha/beta

		v = max(v, min_value)

	return v
	

def min_val(board, highest_min, lowest_max, depth, maxBool):
	global DEPTH_LIM
	depth += 1

	if ttt.terminal(board):
		return ttt.utility(board)

	v = float("inf")

	max_value = 0
	for action in ttt.actions(board):
		if depth == DEPTH_LIM:
			return v

		max_value = max_val(ttt.result(board, action), 
					highest_min, lowest_max, depth, maxBool) #was true

		#If minimizing, Track the lowest_max in the top tier (this applies more to the max_val FN
		# if (maxBool == False) and (max_value < lowest_max): #Alpha/Beta
		# 	lowest_max = max_value


		# #Return immediately if we get a max value in lower tier greater than the highest_min in the tier above
		# if max_value < highest_min: #max_value is in tier below. #highest min is tier above.
		# 	return min(v, max_value) #alpha/beta - should be return max_value
		
		v = min(v, max_value)

	return v