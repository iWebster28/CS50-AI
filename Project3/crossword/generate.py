import sys
import copy

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        # self.print(self.crossword.variables)
        # print('hi')
        # for var in self.crossword.variables:
        #     print(var)
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """

        # print(self.domains)

        for var in self.crossword.variables: # For each VAR
            for val in self.domains[var].copy(): # For each value (word) in VAR's domain
                # Check consistency with VAR's unary constraints
                if (len(val) != var.length):
                    self.domains[var].remove(val) # Remove if inconsistent
        

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """

        # Leave y dom unchanged

        revised = False

        # Check all possible values in y's dom to see if ANY overlap with curr x_val in x's dom
        # If at the end, no y_val in y's dom overlaps with x's x_val, then delete x's x_val.
        for x_val in self.domains[x].copy():
            # Vals in y's dom that satisfy the binary constraint for the current x val
            # If this set is empty, then we don't satisfy x val's dom.
            valid_y_vals = set()

            for y_val in self.domains[y]:
                #y_var = Variable(y.i, y.j, y.direction, len(y_val)) # Check overlaps
                overlaps = self.crossword.overlaps[x, y] # was y_var, but ignore bc enforce_node_consistency already ensures length, right?
                if overlaps != None: #We have overlap
                    if x_val[overlaps[0]] == y_val[overlaps[1]]: # i.e. no character conflict @ overlapping cell
                        valid_y_vals.add(y_val)

            # If the y_val in y's dom doesn't satisfy the curr x_val 
            # in x's dom, remove x_val
            if valid_y_vals == None:
                self.domains[x].remove(x_val)
                revised = True 

        return revised # Return true if revision was made to x dom; false if no rev. made
        

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        # arcs = intial list of arcs to process
        # If none, start with queue all arcs in list `arcs` 
        # Each arc is tuple (x, y) of var x and diff var y
        queue = []

        if arcs == None: # Append all arcs - are these arcs generated correctly?
            self.get_initial_arcs(queue)   
        else: 
            queue.extend(arcs)

        # Revise each arc in queue one at a time
        # If make change to dom, need to add more arcs to queue to ensure other 
        #arcs remain consistent

        # If all rem. values removed from dom, return False (can't solve problem)
        # Else, return True

        count = 0
        while len(queue) != 0:
            # print('------', queue)
            # count += 1
            # print(count)
            (x, y) = queue.pop()
            if self.revise(x, y): 
                if len(self.domains[x]) == 0:
                    return False
                for z in (self.neighbors(x) - y):
                    queue.append((z, x)) # Add arcs back to queue
        return True


    def get_initial_arcs(self, queue):
        """
        Get list of all initial arcs in the problem.
        """

        # Append all arcs - are these arcs generated correctly?
        # for x_var in self.crossword.variables:
        #     for y_var in self.crossword.variables:
        #         if x_var != y_var:
        #             queue.append((x_var, y_var)) 

        # Or....?
        for x_var in self.crossword.variables:
            neighbors = self.crossword.neighbors(x_var)
            for neighbor in neighbors:
                queue.append((x_var, neighbor))
        return


    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """

        # assignment = dict
        # values = strings of words that vars take on
        # Check if every crossword var is assigned a value (ignoring actual val)
        for val in assignment.values():
            if val == None:
                return False
        return True

        
    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        # If consistent: 
        # 1. all values distinct, 
        values = assignment.values()
        if (len(set(values)) != len(values)):
            return False

        # 2. every value is correct length,
        for var in assignment:
            for var2 in self.crossword.variables:
                if var == var2:
                    if len(var) != len(var2):
                        return False

        # 3. no conflicts btwn neighbouring vars
        for var in assignment:
            neighbors = self.neighbors(var)
            for neighbor in neighbors:
                overlaps = self.crossword.overlaps[var, neighbor]
                if overlaps != None:
                    # Make sure chars line up
                    if assignment[var][overlaps[0]] == neighbor[overlaps[1]]:
                        continue
                    else:
                        return False # i.e. no overlap with neighbours, meaning conflict
                    # ???? makes no sense because already checked overlaps in neighbours fn

        return True


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        # First val: rules out least values in var's neighbours
        # least-constraining values heuristic: computed as # vals 
        # ruled out for unassigned neighbor vars
        # ex: assigning var to val results in elim. `n` poss. choices 
        # for neighbor vars, then order list in ascending order of `n`

        # Any var in `assignment` already has a value - ignore when 
        # computing ruled out vals

        # self.crossword.overlaps 

        # implement first by ret list of vals in arb order 
        # Once working, ensure vals in correct order

        # Use "sort" to sort list by KEY



        raise NotImplementedError

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        # sort list by key
        # If tie btwn vars, choose var with largest degree (most neighbours)
        # If ties in both cases, choose arbitrarily among tied vars

        #Implement by ret arb unassigned var. Then ensure ret var according to heurs.




        raise NotImplementedError

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        # Partial assignment: not all vars will have values

        # If can generate puzzle, ret complete assignment (dict with all keys assigned a val)
        # Else, retu None

        #To make algo more efficient:
        # Interleave search with inference 
        # Maintain arc consistency each time new assignment made
        # (this is why ac3 has arcs arg - in case start w diff queue of arcs)






        raise NotImplementedError


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
