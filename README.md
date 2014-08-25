word2vec_variations
===================

** Work in progress ** 
===================
Moving and documentation files from the previous BitBucket repertoire


## **Dependencies**
-----------------------
This project uses `Python 2.7.x`. Except for the files in _word2vec_ folder that are in `C` as they're the Mikolov et al. implementation from <https://code.google.com/p/word2vec/>, from exception to `compute-accuracy-w.c` and `word2vec-g.c` that are modfied versions of their _word2vec_ counterparts.

So for the `Python` code the folloing dependencies are required:

- Numpy
- matplotlib
- Sklearn
- NLTK

One important point is that we need the WordNet corpus provided by NLTK, but as it seems, there is a ciclicity in the tree model in their version of WordNet, and this can make `word_net_tree.py` enter an infinite loop. Fortunately, this seems to be corrected in the newest WordNet release. So we recomend the following aproach: 
1. Install NLTK
2. Install the WordNet corpora using NLTK ([reference](http://www.nltk.org/data.html))
3. Find where the corpora was installed and replace the files with the newest version from [WordNet site](http://wordnet.princeton.edu/wordnet/download/current-version/) version 3.1 has been show to be stable in our tests.

