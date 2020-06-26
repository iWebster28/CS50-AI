import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000

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
            model[pg] = (1 - damping_factor)/N

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

    # Generate 1st sample by randomly choosing page
    # For each other sample: generate next samp. based on prev. using transition model
    #transition_model








    #raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # Start: assign each page rank 1/N (N = num pages in corpus)

    # Based on curr. rank vals, calc. new rank vals. using PageRank formula

    # Page with no links = interpret as having 
    #1 link for every page in corpus, including itself

    # Continue until PageRanks accurate within 0.001







    #raise NotImplementedError


if __name__ == "__main__":
    main()
