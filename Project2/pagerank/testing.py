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
