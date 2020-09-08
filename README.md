# CS50-AI
For Harvard's CS50 Intro to Artificial Intelligence Course.

## Week0/Project0 - Search
### [Degrees](./Project0/degrees)
Breadth-first search to find the shortest path between two Hollywood actors and the movies they star in.
### [TicTacToe](./Project0/tictactoe)
An AI TicTacToe-player with pygame, using minimax. Experimental depth-limiting and alpha-beta pruning.

## Week1/Project1 - Knowledge
### [Knights](./Project1/knights)
Propositional logic puzzle solver for "Knights and Knaves" puzzles.
### [Minesweeper](./Project1/minesweeper)
AI Minesweeper-player with pygame using propositional logic.

## Week2/Project2 - Uncertainty
### [PageRank](./Project2/pagerank)
Based on Larry Page's PageRank system developed for prioritizing Google search results. Uses a sampling method based on Markov Chains, as well as an iterative method that recursively updates estimated pagerank values until convergence. 

### [Heredity](./Project2/heredity)
Uses unconditional probabilities of passing a trait from parent to child to guess the probabilities of a child having a certain trait, and how many genes they have.  Works with multiple family members, also calculating probabilities of having a specific number of genes related to a trait.

## Week3/Project3 - Optimization
### [Crossword](./Project3/crossword)
A crossword puzzle generator, taking as input a puzzle template and word list, then outputting a finished puzzle.
This is a constraint satisfaction problem that uses the AC-3 arc consistency algorithm to decide where words will go.  

**Further Explanation**  
The empty word-placeholders in the puzzle template are the **variables**, and each variable has a **domain** of words that may be assigned. Variables that overlap one another are called **neighbours**. The variables can be treated as *nodes*, and the constraint linking 2 variables can be treated as an *arc*.  
The **unary constraint** in this case is the length of a word: a variable's domain must only include words that have the same number of letters as the variable itself. The **binary constraint** in this problem is the **arc consistency** between nodes: for every word in domain of variable x, there must be at least one word in the domain of variable y that shares the same overlapping letter, given that the variables overlap in the puzzle template (they're neighbours).   By enforcing arc consistency, domains are reduced, and words may be placed in the puzzle. A **backtracking** search is used choose a word from a domain to assign to a variable. In the backtracking search, a **minimum remaining values** (MRV) heuristic is used to select variables with the smallest domain first. As well, a **least-constraining values heuristic** is used to prioritize variables that rule out the least options from its neighbouring domains.

## Week4/Project4 - Learning
### [Shopping](./Project4/shopping)
A supervised learning problem to predict whether or not a shopper will complete an online purchase. The scikit-learn library is used with K-Nearest-Neighbour model for classification (k = 1). For training, a 12000-line dataset of shopping purchases with visitor type, date, and browser information is used. The dataset is labelled by purchase completion (True/False). The program measures the **sensitivity** and **specificity** of the predictions made (where **sensitivity** is the proportion of positive labels correctly identified (e.g. user makes a purchase) and the **specificity** is the proportion of negative labels correctly identified.)

### [Nim](./Project4/nim)
A game based on piles of items. Players take turns removing any positive number of items from ONE non-empty pile. The player who takes the last item looses. 

This program uses reinforcement learning (Markov Decision Process) to train an AI to play Nim. The AI tracks the results of executing certain **actions** in certain **states**, and assigns a **reward** based on success (reward on AI loss: -1, AI win: 1, Tie: 0). **Actions** are represented as (i, j) where i is a pile, and j is the # of items to take. **States** are the sizes of each pile, respectively.

In particular, Q-learning is used to train the AI in 10000 games of Nim. Q-learning estimates the value of executing a certain action in a certain state. We continuously update q-values (for each state and action) based on the old q-value and a new estimated q-value (see below). To find the best action, we search for the highest q-value and its associated action.
```
Formula: Q(s, a) <- old_q + alpha * (new_q_est - old_q)
```
```
Where:
s: state - size of each pile
a: action - (i, j) - i is pile; j is # items to take
alpha: the learning rate, or the degree to which we value NEW info versus OLD info.
old_q: the previous q-value
new_q_est: sum of the current reward and the future estimated reward
```

The **Epsilon-Greedy** algorithm is used to promote further solution space *exploration* instead of *exploitation*. For example, with a probability of **epsilon**, the AI will make a random move instead of the best move. This potentially allows more creative or faster solutions.

## Week5/Project5 - Neural Networks
### [Traffic](./Project5/traffic)

A convolutional neural network to identify 43 different types of street signs. Uses tensorflow and the gtsrb dataset. Please see the [README.md](./Project5/traffic/README.md) within the 'traffic' folder. After running many tests, I found that the most accurate and consistent results were given by the following network layers and parameters: Relu activation on four layers of 2D Convolutions, two instances of Max Pooling + Batch Normalization, Flattening, 1 Dense Hidden Layer with 128 units, a Dropout rate of 0.5, and a Softmax Output layer. The mean test results (Test 15 Avg) for 5 tests showed a loss of 0.0674 and accuracy of 0.98308.

## Week6/Project6 - Language
### [Parser](./Project6/parser)
Parser uses the ntlk Python library to parse english sentences (grammatically) while extracting 'noun chunk phrases.'
For this project, I came up with a list of **context-free grammar** rules (**non-terminal symbols**) to ensure that the program would be able to 'understand' how to parse the sentences from the provided corpus. I chose rules such that the parser would not suffer from **over- or under- generation** - over- or under- generalizing for what is considered grammatically correct/parsable.
The program first ingests the non-terminal symbols into the nltk parser. We then take an input sentence from the user, and preprocess it by removing any strings that don't contain at least one letter, and converting all characters to lowercase. We then attempt to parse a tree based on the user input and non-terminal symbols. Noun phrase chunks are generated by searching for subtrees containing the 'NP' (Noun-Phrase) non-terminal label. The noun phrase chunks are the **leaves** of each 'NP' subtree.

### [Questions](./Project6/questions)
Questions uses the nltk library to understand queries asked by a user. Provided with a corpus of .txt files, the program can tokenize these files, rank them based on **TF-IDF** (an information retrieval method based on **term frequency (TF)** and **inverse document frequency (IDF)**) and respond to a user query with the most relevant result. It is important to note that when tokenizing, the program removes any stop words and punctuation. We then compute the **IDF** with the following formula:
```
IDF-for-word1 = log((Total Number of Documents)/(Number of Documents Containing word1))
```
The user is then prompted to enter a query, which is tokenized by the previous method. After a user enters a query, we look for the top `n` files containing the query (where n == FILE_MATCHES == 1). Files are ranked on their **TF-IDF** values, where:
```
tf_idfs for `word1` in `doc1` = TF-for-word1-in-doc1 * IDF-of-word1
```
The sentences from the top files are extracted, and we compute their **IDFs**. We find the top sentences based on **matching word measure (mwm)**, which is the sum of idfs for words in both `sentences[sentence]` and `query` (for all sentences). If there is a tie between two or more sentences for **mwm**, then we sort the sentences again by **query term density (qtd)**, which is the proportion of words in sentence that are also in the query.
