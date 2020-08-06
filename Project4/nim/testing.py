#testing.py

q = dict()
q[tuple([0, 0, 0, 2]), (3, 2)] = -1

print(q.get((tuple([0, 0, 0, 2]), (3, 2))))