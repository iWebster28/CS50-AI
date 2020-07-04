import os
import random
import re
import sys

import copy
import numpy as np

DAMPING = 0.85
SAMPLES = 10000
THRESHOLD = 0.001

# PageRank = probability that a random surfer is on a 
# page at a given time


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    model = dict()
    N = len(corpus) # total num pages in corpus
    num_links = numLinks(corpus, page) # links on `page`
    # print(num_links) #Diag

    #If no outgoing links, then return EVEN prob. dist. (choose rand among all pages equally)
    if num_links == 0:
        for pg in corpus:
            model[pg] = 1/N

    else:
        # Build dictionary
        for pg in corpus: # For any page in the corpus
            model[pg] = (1 - damping_factor)/N # Base probability that we visit any page

        for pg in corpus[page]: # For outbound links on `page`
            model[pg] += damping_factor/num_links
        
    # Return dict w prob. dist. over which page a rand. surfer would visit next
    return model


def numLinks(corpus, page):
    """
    Get the number of links on a given page
    """

    return len(corpus[page])


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # Assume n is >= 1

    # want to track how many times each page has shown up in
    #a sample.
    samples = dict()

    # Initialize all sample values to 0 (intial probability)
    for pg in corpus:
        samples[pg] = 0
        
    N = len(corpus) # num pages in corpus

    # Generate 1st sample by randomly choosing a page
    prev_pg = random.choice(list(corpus))
    samples[prev_pg] += 1

    # For each other sample: generate next samp. based on prev. 
    #using transition model
    for sample in range(0, n):

        # Get transition model from previous page
        next_proba = transition_model(corpus, prev_pg, damping_factor)

        # Choose random page (key) from probabilities - 
        # RANDOM based on the probabilities (values) given
        next_pg = random.choices(list(next_proba), next_proba.values())[0]
        #print(next_pg)
        samples[next_pg] += 1 # This page has been sampled again; increment count
        prev_pg = next_pg

    # Divide all samples by n (total num samples) to get probabilities
    for pg in corpus:
        samples[pg] /= n

    check_sum(samples)

    return samples    


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    pages = dict()
    N = len(corpus)

    # Start: assign each page rank 1/N (N = num pages in corpus)
    for pg in corpus:
        pages[pg] = 1/N

    # Continue until PageRanks accurate within 0.001 = THRESHOLD
    cont = True
    iterations = 0
    while cont:
        iterations += 1
        prev_pages = copy.deepcopy(pages)

        # Based on curr. rank vals, calc. new rank vals. using PageRank formula
        for pg in corpus:
            pages[pg] = PR(corpus, damping_factor, pg, prev_pages) #pass in pages of prev_pages??? calc. based on constantly updated values or no?

        # Track differences in curr/prev rankings
        diff = np.subtract(list(pages.values()), list(prev_pages.values()))
        diff = np.absolute(diff)

        # Once no items are greater than the threshold, stop.
        if len(diff[diff > THRESHOLD]) == 0:
            cont = False

    check_sum(pages)
    # print('iterations:', iterations)

    return pages


def PR(corpus, damping_factor, page, prev_pages): # where prev_pages are previous page ranks.
    """
    Calculate page rank based on iterative algorithm
    """

    cumulative_rank = 0
    N = len(corpus)

    # Find sum from other pageranks of pages that link to `page`
    # how to find pages that link to `page`?
    linked = set(
            pg for pg in corpus # Check every page in corpus if it links to `page`
            if page in corpus[pg] # if pg contains any links to `page`!
        )

    # print("Page to rank:", page)
    # print('linked pages:', linked)

    for pg in linked: #pg = i
        if pg != page:
            num_links = numLinks(corpus, pg)
            # If 0, treat as having a link to every page in corpus, including itself.
            if num_links == 0:
                num_links = len(corpus)

            cumulative_rank += prev_pages[pg]/num_links #prev_pages[pg] = PR(i)

    pagerank = (1 - damping_factor)/N + (damping_factor * cumulative_rank)
    # print("==========")
    return pagerank


def check_sum(pages):
    """
    Check probabilities sum to 1
    """
    _sum = 0
    for pg in pages:
        _sum += pages[pg]
    print("Sum of Probabilities:", _sum)


if __name__ == "__main__":
    main()
