# Testing pagerank

import sys
import pagerank as pr


# Test transition model
samples = {"1.html": 0.5, "2.html": 0.1, "3.html": 0.4}

corpus = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {}}
# corpus = pr.crawl(sys.argv[1])
page = "3.html"

output = pr.transition_model(corpus, page, pr.DAMPING)
print(output)


# if len(sys.argv) != 2:
#         sys.exit("Usage: python pagerank.py corpus")
#     corpus = crawl(sys.argv[1])

corpus = {"1.html": {"2.html"}, "2.html": {"1.html", "3.html"}, "3.html": {"2.html", "4.html"}, "4.html": {"2.html"}}

page = "1.html"

linked = set(
            pg for pg in corpus # Check every page in corpus if it links to `page`
            if page in corpus[pg] # if pg contains any links to `page`!
        )