# Testing pagerank

import pagerank as pr


# Test transition model

corpus = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
page = "1.html"

output = pr.transition_model(corpus, page, pr.DAMPING)
print(output)
