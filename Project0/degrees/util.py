class Node():
    def __init__(self, state, parent, action):
        self.state = state #person_id
        self.parent = parent #used to get to this node
        self.action = action #movie_id

#Stack Frontier - LIFO
#For depth-first search - expand deepest node in froniter
class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state): # ex: are we in the goal state?
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1] #LIFO
            self.frontier = self.frontier[:-1] #Remove last node
            return node

#Queue Frontier - FIFO
#Use for breadth-first search - expand shallowest node in the frontier
class QueueFrontier(StackFrontier): #inherits from StackFrontier

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0] #FIFO
            self.frontier = self.frontier[1:] #remove first node
            return node
