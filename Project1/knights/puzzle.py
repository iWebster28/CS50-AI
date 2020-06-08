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

# Puzzle 0
# A says "I am both a knight and a knave." 
sentence0 = And(AKnight, AKnave) #What A says in Puzzle 0

knowledge0 = And(
    #Knight tells truth; Knave lies 
    Implication(AKnight, sentence0),
    Implication(AKnave, Not(sentence0)),

    #Either a knight or a knave
    Or(AKnight, AKnave)
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.

sentence1 = And(AKnave, BKnave)

knowledge1 = And(
    #Knight tells truth; Knave lies 
    Implication(AKnight, sentence1),
    Implication(AKnave, Not(sentence1)),

    #A and B are either knight or a knave
    Or(AKnight, AKnave),
    Or(BKnight, BKnave)
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."

sentence2_A = Or(
    And(AKnight, BKnight),
    And(AKnave, BKnave)
)

sentence2_B = Or(
    And(AKnight, BKnave),
    And(AKnave, BKnight)
)

knowledge2 = And(
    #Knight tells truth; Knave lies 
    Implication(AKnight, sentence2_A),
    Implication(AKnave, Not(sentence2_A)),
    Implication(BKnight, sentence2_B),
    Implication(BKnave, Not(sentence2_B)),

    #A and B are either knight or a knave
    Or(AKnight, AKnave),
    Or(BKnight, BKnave)
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."

sentence3_A = Or(AKnight, AKnave)
sentence3_B = And(
    #Implication(AKnight, BKnave),
    Implication()
    CKnave
)
sentence3_C = AKnight

knowledge3 = And(
    #Knight tells truth; Knave lies 
    
    Implication(AKnight, sentence3_A),
    Implication(AKnave, Not(sentence3_A)),
    Implication(BKnight, sentence3_B),
    Implication(BKnave, Not(sentence3_B)),
    Implication(CKnight, sentence3_C),
    Implication(CKnave, Not(sentence3_C)),

    #A, B and C are either knight or a knave
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnight, CKnave)
)

# Beter solution for multiple sentences!
# sentences3 = [sentence3_A, sentence3_B, sentence3_C]
# for i in range(0, len(characters)):
#     if (i % 2 == 0):
#         knowledge3.add(Implication(characters[i], sentences3[i // 2]))
#     else:
#         knowledge3.add(Implication(characters[i], Not(sentences3[i // 2])))



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
