import nltk
import sys
import glob
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    while (1): # While loop for debugging!
        # Prompt user for query
        query = set(tokenize(input("Query: ")))

        # Determine top file matches according to TF-IDF
        filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

        # Extract sentences from top files
        sentences = dict()
        for filename in filenames:
            for passage in files[filename].split("\n"):
                for sentence in nltk.sent_tokenize(passage):
                    tokens = tokenize(sentence)
                    if tokens:
                        sentences[sentence] = tokens

        # Compute IDF values across sentences
        idfs = compute_idfs(sentences)

        # Determine top sentence matches
        matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
        for match in matches:
            print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """

    files = {}
    base = os.path.join(os.curdir, directory, '') # Add '' so that os.sep is appended to end of path.
    
    for filepath in glob.glob(base + '*.txt'): # Grab all text files
        with open(filepath, 'r') as f:
            filename = filepath[len(base):] # Keep only the filename from the filepath.
            files[filename] = f.read() # Read in contents to dictionary

    # print(string.punctuation)
    # print('-', nltk.corpus.stopwords.words('english'))

    # print(files.keys())
    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """

    words = []
    source = nltk.word_tokenize(document.lower())
    words = [word for word in source
        if (word not in string.punctuation) and 
        (word not in nltk.corpus.stopwords.words('english'))
    ] # Strip out any punctuation or stopwords

    # print(words)
    # print("Finished tokenizing.")
    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    words = set() 
    idfs = {}

    # 1. Create a set of all words from all documents
    for doc in documents:
        words.update(documents[doc]) # Note: all words are read in as a list already. #word for word in documents[doc]) 

    # print(words)

    # 2. For each word, check how many docs it appears in
    for word in words:
        freq_all = sum(word in documents[doc] for doc in documents)
        # 3. Calculate idfs per word
        idfs[word] = math.log(len(documents)/freq_all)

    # print('Finished computing idfs.')
    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    
    # Assume n is not greater than the total num of files
    tf_idfs = {}

    # Where tf_idfs for `word1` in `doc1` = TF-for-doc1 * IDF-of-word1

    # 1. Rank files according to sum of tf-idf values for words that appear in query AND file
    for file in files:
        for word in query:
            tf = sum([word == w for w in files[file]]) # Get term frequency for current file
            
            if not(file in tf_idfs): # Initialize to 0 if empty
                tf_idfs[file] = 0
            
            tf_idfs[file] += tf * idfs[word] # Calculate tf_idf
            
            # print(file)
            # print('tf:', tf)
            # print('idf:', idfs[word])
            # print('tf_idf:', tf_idfs[file])

    # 2. Return top `n` filenames that match query; best match first
    # Sort the tf_ids in descending order. Want highest values first. Return list of keys from dict.
    sort = sorted(tf_idfs.items(), key = lambda tfidf: tfidf[1], reverse = True) # sort based on values (tf_idfs)
    sort_names = list(zip(*sort))[0] # Get keys (filenames)
    sort_names = sort_names[:n] # Get top `n` filenames
    # Alternate: sort_names = {key: for key, value in sorted(tf_idfs.items(), key = lambda tfidf: tfidf[1], reverse = True)}
    # print('Finished top_files.')
    return sort_names


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    
    best_sents = []

    for sentence in sentences:
        # 'matching word measure' - sum of idfs for words in both `sentences[sentence]` and `query` for all sentences
        mwm = sum(idfs[word] for word in query
            if word in sentences[sentence])
        #'query term density' - proportion of words in sentence that are also in the query
        qtd = sum(w in query for w in sentences[sentence]) / len(sentences[sentence])
        best_sents.append((sentence, mwm, qtd))

    # Return best match first; top `n` results
    # Sort by mwm, then qtd
    sorted_sents = sorted(best_sents, key = lambda item: (item[1], item[2]), reverse = True)
    
    # print(sorted_sents[:n]) #diagnostic
    # Return top `n` results
    return(sorted_sents[0][:n])

if __name__ == "__main__":
    main()
