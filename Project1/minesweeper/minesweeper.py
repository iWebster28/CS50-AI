import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other): #Like operator ==
        return self.cells == other.cells and self.count == other.count

    def __str__(self): #Me: Format when printed
        return f"{self.cells} = {self.count}"


    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        
        if (self.count == len(self.cells)): #All mines
            return self.cells
        return None


    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """

        #Corner case
        if (self.count == 0): #No mines
            return self.cells
        return None


    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        #First, check if `cell` is in the sentence provided
        cell_set = set([(cell[0], cell[1])])
        if cell_set.issubset(self.cells): 
            self.cells.remove(cell) #set2 - set1 = count2 - count1
            self.count -= 1


    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        cell_set = set([(cell[0], cell[1])])
        if cell_set.issubset(self.cells):
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        # `cell` is known safe and `count` are surrounding mines
        
        #1) Mark move made
        self.moves_made.add(cell)

        #2) Mark cell safe (and all sentences with that cell)
        self.mark_safe(cell)

        #3) add a new sentence to the AI's knowledge base
        #   based on the value of `cell` and `count`

        surround = self.neighbour_cells(cell) #Get surrounding cells

        #Only include cells whose state is still
        #undetermined in the sentence

        surround_copy = set()

        #if (self.safes != None or self.mines != None):
            
        # Remove already-determined cells from current sentence
        for element in surround:
            #Check if element is NOT already in known safes or mines or moves_made:
            if not((element in self.safes) or (element in self.mines) or (element in self.moves_made)):
                surround_copy.add(element) #add undetermined elements to new list to create sentence from.

            if element in self.mines:
                # Also need to decrement count
                count -= 1

        sentence = Sentence(surround_copy, count)
        self.knowledge.append(sentence) #Add sentence to knowledge base
        print("Finished 3: add sentence to knowledge based on `cell` and `count`")
        print(sentence) # Diagnostic


        #4) mark any additional cells as safe or as mines
        #   if it can be concluded based on the AI's knowledge base
        
        # Check all sentences in self.knowledge 
        # To mark as safes or mines
        for sentence in self.knowledge: #sets: no duplicates to worry about.
            mines = sentence.known_mines()
            safes = sentence.known_safes()
            if mines != None: #Intersect the sets: add new mines/safes
                self.mines |= mines
            if safes != None:
                self.safes |= safes

        print("Finished 4: Added safes/mines to knowledge base.")

        #5) add any new sentences to the AI's knowledge base
        #   if they can be inferred from existing knowledge

        # Check for subsets

        # Is this efficient?
        # Do the for loops account for the dynamic size of knowledge?
        # How many iterations? We keep adding new sentences to end of list.
        print("knowledge size before 5:", len(self.knowledge))

        new_knowledge = []

        # for sent1 in self.knowledge:
        #     for sent2 in self.knowledge:
        #         if (sent1 != sent2) and (sent1.cells != None) and (sent2.cells != None):
        #             if sent1.cells.issubset(sent2.cells):
        #                 new_knowledge.append(Sentence(sent2.cells.difference(sent1.cells), sent2.count - sent1.count))
        #             # print("knowledge size:", len(self.knowledge)) #Diagnostic
        #             # print("new_knowledge size:", len(new_knowledge))

        # #self.knowledge = new_knowledge
        # self.knowledge.extend(new_knowledge)
        # # print(new_knowledge)

        #diagnostic
        print("knowledge size after 5:", len(self.knowledge))
        print("Safes:", self.safes)
        print("Mines:", self.mines)

        print("Finished 5: add any new sentences to the AI's knowledge base")
        print("--------------------------------------")

    #CHECK
    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        for safe in self.safes:
            if safe not in self.moves_made:
                return safe

        return None


    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        moves = []
        for i in range(0, self.height - 1):
            for j in range(0, self.width - 1):
                if (i, j) not in self.moves_made and (i, j) not in self.mines:
                    moves.append((i, j)) #first avail. move
        #random
        length = len(moves)
        #print("length:",length)
        if length == 1:
            return moves[0]
        elif length != 0:
            return moves[random.randint(0, length - 1)]
        return None


    def neighbour_cells(self, cell):
        """
        Return a set of cells that are neighbors to `cell`
        """
        # Similar to nearby_mines in Minesweeper class
        neighbours = set()

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                #Check bounds
                elif (0 <= i < self.height) and (0 <= j < self.width):
                    neighbours.add((i, j))

        return neighbours


