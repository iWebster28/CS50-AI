#testing.py

#For testing minesweeper functions

from minesweeper import Minesweeper, MinesweeperAI, Sentence

HEIGHT = 8
WIDTH = 8
MINES = 8

# Create game and AI agent
game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
ai = MinesweeperAI(height=HEIGHT, width=WIDTH)

game.print()

test_sent = Sentence([(0, 0), (1, 1)], 2)
test_sent2 = Sentence([(0, 0), (1, 1)], 2)
#{(0, 0), (1, 1)} = 2
print(test_sent)
print(test_sent == test_sent2)

test_sent.mark_mine((1,1))
print(test_sent)

print("known mines:", test_sent.known_mines())
print("known safes:", test_sent.known_safes())


# MinesweeperAI

# apple = set()
# if apple: #set not empty
# 	print(apple.pop())

ai.mark_mine((0,0))
print(ai.make_random_move()) #Works. Take next avail. move, (0,1)

print("hi")

# Testing list iteration that adds items to the list
# listest = [1, 2, 3]
# i = 3
# for item in listest:
# 	if i != 10:
# 		i += 1
# 		listest.append(i)

print(listest)
