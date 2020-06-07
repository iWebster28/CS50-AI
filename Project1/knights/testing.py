#testing.py

#Testing knowledge bases

from logic import *

#IF No rain -> Harry visits Hagrid
#Harry visited Hagrid, OR Dumbledore today, but not both (XOR)
#Harry visited Dumbledore today

#Q: Who did Harry visit?
#Q2: Did it rain?

#A:
#Harry did not visit Hagrid today
#It rained today

rain = Symbol("It rained today")
hagrid = Symbol("Harry visited Hagrid")
dumbledore = Symbol("Harry visited Dumbledore")

knowledge = And(
	Implication(Not(rain), hagrid), #one way only
	Not(And(hagrid, dumbledore)),

	Or(hagrid, dumbledore),

	dumbledore
)

print(knowledge.formula())

print("Did it rain?", model_check(knowledge, rain))
print("Did Harry visit hagrid?", model_check(knowledge, hagrid))
print("Did Harry visit dumbledore?", model_check(knowledge, dumbledore))
