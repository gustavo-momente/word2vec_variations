CC = gcc
#The -Ofast might not work with older versions of gcc; in that case, use -O2
CFLAGS = -lm -pthread -Ofast -march=native -Wall -funroll-loops -Wno-unused-result

all: word2vec word2vec-g word2phrase distance word-analogy compute-accuracy-w compute-accuracy

word2vec : word2vec.c
	$(CC) word2vec.c -o word2vec $(CFLAGS)
word2vec-g : word2vec-g.c
	$(CC) word2vec-g.c -o word2vec-g $(CFLAGS)
word2phrase : word2phrase.c
	$(CC) word2phrase.c -o word2phrase $(CFLAGS)
distance : distance.c
	$(CC) distance.c -o distance $(CFLAGS)
word-analogy : word-analogy.c
	$(CC) word-analogy.c -o word-analogy $(CFLAGS)
compute-accuracy-w : compute-accuracy-w.c
	$(CC) compute-accuracy-w.c -o compute-accuracy-w $(CFLAGS)
compute-accuracy : compute-accuracy.c
	$(CC) compute-accuracy.c -o compute-accuracy $(CFLAGS)
	chmod +x *.sh

clean:
	rm -rf word2vec word2vec-g word2phrase distance word-analogy compute-accuracy compute-accuracy-w
