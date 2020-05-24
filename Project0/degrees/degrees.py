#5-23-20 
#Harvard CS50-AI 2020
#Project 0: Degrees of Separation for IMBd Actors

import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set() #movies are loaded later
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set() #Stars are loaded later
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try: #Add to sets we defined ealier ("movies" set in people list, and "stars" set in the movies list)
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


#source and target are person_ids
def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    #movie_id and person_id are ints
    #if there are multiple min. length paths, can return any of them.
    #use neighbors_for_person function - 
    #person id as input, ret. set of (movie_id, person_id) pairs 
    #for all people starring in a movie w given person

    #can check for goal node before we add a node to frontier - faster!
    
    #Initialization
    explored = set() #set of visited nodes to prevent cycle loops
    qFront = QueueFrontier() #initialize frontier
    nodes_explored = 0

    #Initial state: Get all (movie, person) pairs for people 
    #who starred in any movie with the "source" person
    #neighbors = neighbors_for_person(source)
    #print(neighbors)

    #Initialize frontier to starting person (source person_id)
    startNode = Node(state=source, parent=None, action=None)
    qFront.add(startNode)

    while True: #loop until soln found
        #print("LOOP")

        #If frontier empty, then no soln. Return none
        if qFront.empty():
            return None

        #Else: remove node from the frontier
        node = qFront.remove()
        nodes_explored += 1 #Diagnostic

        #If node contains goal state, return soln
        #goal = target #person_id
        if node.state == target: #NEED TO DEFINE WHAT THE GOAL IS. TARGET?
            actions = [] #movie_ids used to get to this node - for backtracing
            states = [] #person_ids
            solution = [] #list of pairs (movie_id, person_id)

            #Backtracing
            #Follow parent nodes to find soln
            while node.parent is not None: #when we get back to orig node, has no parent
                actions.append(node.action)
                states.append(node.state)
                node = node.parent

            actions.reverse() #reverse (bc was goal -> initial)
            states.reverse()

            for i in range(0, len(actions)):
                solution.append((actions[i], states[i]))

            #print(solution)
            return solution #need to change this to return list of pairs

        #Else:
        # Add node to explored set (mark visited)
        # Expand the node, 
        # and add resulting nodes to frontier (look at neighboring nodes/actions)
        # ONLY IF they aren't already in the frontier OR the explored set
        
        explored.add(node.state)

        #Add neighbors (co-stars) to the frontier
        for action, state in neighbors_for_person(node.state): #Neighbors of the current node!
            if not qFront.contains_state(state) and state not in explored:
                child = Node(state=state, parent=node, action=action)
                qFront.add(child) 

        #print("Nodes Explored: ", nodes_explored)

    #end while


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"] #movies that person_id was in
    neighbors = set() 
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
