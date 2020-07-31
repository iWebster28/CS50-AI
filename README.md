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
(The empty word-placeholders in the puzzle templace are the **variables**, and each variable has a **domain** of words that they could be assigned. By enforcing arc consistency, domains are reduced, and words are placed in the puzzle.) A **backtracking** search is used choose a word from a domain to assign to a variable. In the backtracking search, a **minimum remaining values** (MRV) heuristic is ysed to select variables with the smallest domain first. As well, a **least-constraining values heuristic** is used to prioritize variables that rule out the least options from its neighbouring domains.
