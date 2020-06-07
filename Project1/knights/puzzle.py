from logic import *

#Each character is either a knight or knave
#Knight always tells truth
#Knave always lies

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

characters = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]

sentence0 = And(AKnight, AKnave) #What A says in Puzzle 0


# Puzzle 0
# A says "I am both a knight and a knave." 
knowledge0 = And(

    #Knight tells truth; Knave lies 
    Implication(AKnight, sentence0),
    Implication(AKnave, Not(sentence0)),

    #Either a knight or a knave
    Or(AKnight, AKnave),
    #Or(BKnight, BKnave),
    #Or(CKnight, CKnave),

    #If A is a knight, then A is not a knave, and vice versa
    #Biconditional(AKnight, Not(AKnave)),
    #Biconditional(AKnave, Not(AKnight)),

    #A liar
    #Implication(And(AKnave, AKnight), AKnave),
    #Implication(And(AKnave, AKnight), Not(AKnight)),


    #A cannot be both a knight and a knave
    #Not(And(AKnight, AKnave)),

    #If A is a knight and a knave, then A is a knave
    #Implication(And(AKnight, AKnave), AKnave),
    #AKnave, AKnight,

    #Not(Or(BKnight, BKnave, CKnight, CKnave))


)

print(knowledge0.formula())



# Or(
#     And(AKnight, BKnave), #1 type each
#     And(BKnight, AKnave)
#     ), 

#     Not(Or( #cannot both be same
#     And(AKnight, AKnave), 
#     And(BKnight, BKnave)
#     )),

#We have 1 player in Puzzle 0
num_chars = 1

#Each character is either a knight or knave
#A -> !B
# for i in range(num_chars * 2):
#     if (i % 2 == 0):
#         # print(characters[i],characters[i + 1])
#         knowledge0.add(Implication(
#             characters[i], Not(characters[i + 1])
#         ))
# #B -> !A
# for i in range(num_chars * 2):
#     if (i % 2 == 1):
#         # print(characters[i],characters[i - 1])
#         knowledge0.add(Implication(
#             characters[i], Not(characters[i - 1])
#         ))


# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # TODO
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # TODO
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # TODO
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
