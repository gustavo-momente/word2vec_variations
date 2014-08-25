word2vec_variations
===================

** Work in progress ** 
===================
- ~~Move files from old repository~~
- ~~Improve in file usage description~~
- Finish this README


## **Dependencies**
-----------------------
This project uses `Python 2.7.x`. Except for the files in _word2vec_ folder that are in `C` as they're the Mikolov et al. implementation from <https://code.google.com/p/word2vec/>, from exception to `compute-accuracy-w.c` and `word2vec-g.c` that are modfied versions of their _word2vec_ counterparts. Also, the compilation of these files was added to the existing `Makefile`.

So for the `Python` code the folloing dependencies are required:

- Numpy
- matplotlib
- Sklearn
- NLTK

One important point is that we need the WordNet corpus provided by NLTK, but as it seems, there is a ciclicity in the tree model in their version of WordNet, and this can make `word_net_tree.py` enter an infinite loop. Fortunately, this seems to be corrected in the newest WordNet release. So we recomend the following aproach: 
1. Install NLTK
2. Install the WordNet corpora using NLTK ([reference](http://www.nltk.org/data.html))
3. Find where the corpora was installed and replace the files with the newest version from [WordNet site](http://wordnet.princeton.edu/wordnet/download/current-version/), version 3.1 has been show to be stable in our tests.

Moreover, the files in the SE2012 are from the [SemEval-2012 Task 2 challenge](https://sites.google.com/site/semeval2012task2/download) and we call most of their `Perl` scripts from within `SE_Test1.py` so a `Perl` interpreter is needed and the `Statistics::RankCorrelation` too.

Forthermore, a corpus is needed for learning, the algorithm proposed by _Mikolov et al._ works better with large corpora. There is a small corpus called `text8` that can be dowloaded [here](ttp://mattmahoney.net/dc/text8.zip). But as you can find, if you check the `Tests` folder we didn't use this one. Our choice was for a larger corpus, that we called `text9`, as the other one text data is extracted from Wikipedia. Truth be told, `text8` is a croped version of `text9`. So, instruction to download and clean Wikipedia articles is described [here](http://mattmahoney.net/dc/textdata.html) where `text9` is called `fil9` and the raw Wikipedia data `enwik9`.

Finaly, in the `Scripts` folder there are some scripts with the words _fb_ or _freebase_  these are related to the freebase triplets kwnow as **FB15k**, more information can be found [in their site](https://www.hds.utc.fr/everest/doku.php?id=en:transe).
