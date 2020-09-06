import nltk
import sys
import re

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

# Where:
# S is full sentence - how would we allow infinite conjunctions?
# B is base phrase - I should reconsider how a sentence should start either start with NP ONLY
# i.e. have 'NP VP' from B as it's own START. Then for every S, have START be the first nonterminal symbol. (to make the most grammatical sense)
# NP is noun phrase
# PP is pronoun phrase
# AdvP is adverb phrase
# VP is verb phrase
# AdjP is an adjective phrase

NONTERMINALS = """
S -> BEGIN | BEGIN Conj B | BEGIN NP PP Conj B | BEGIN NP PP
BEGIN -> NP VP | NP VP PP
B -> NP VP | VP NP | NP VP PP | VP NP PP
NP -> N | Det N | Det AdjP N | Det AdjP N Adv | Det N Adv
PP -> P NP | P NP PP
AdvP -> Adv V | V Adv
VP -> V | V NP | AdvP NP | AdvP
AdjP -> Adj | Adj AdjP
"""

# Revisions to make:
# the single AdvP for VP is not a great idea. for sentence 8.
# added P NP PP for sentence 10
# sentence 7: how to deal with Adv folowing last N?
# sentence 9: B NP PP Conj B PP --- could remove last PP and instead add VP NP PP to B
# sentence 10: B NP PP
# How to reduce the NP PP for both sent 9 and 10?
# Added Det AdjP N Adv | Det N Adv for case 7 (Det AdjP N Adv is extra)
# BEGIN is extra; copied from B. Could just leave all as B

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    words = []
    words = nltk.word_tokenize(sentence.lower())
    for word in words:
        has_alpha = re.search("[a-zA-Z]", word)
        if has_alpha is None: # Remove any strings without at least 1 alpha character
            words.remove(word)

    # print(words) # Should we check for alpha before or after? (ex: is "Hello," with the comma considered a 'word'?)
    return words


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    noun_phrases = []
    # Assume input is an nltk.tree object with label `S`
    # print(tree.label())
    # for elem in tree.subtrees():
    #     if elem.label() == 'NP':
    #         print('NP found:', elem)
    #     else:
    #         print(elem)


    # using the filter feature test
    # print('-------------------')
    for item in tree.subtrees(lambda t: t.label() == 'NP'):
        # print(item)
        noun_phrases.append(item)
        # noun_phrases.extend([i for i in item.leaves()])
    # print(noun_phrases)
    return noun_phrases # For debugging
    


if __name__ == "__main__":
    main()
