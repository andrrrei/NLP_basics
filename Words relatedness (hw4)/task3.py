import io
from collections import defaultdict
from scipy.stats import spearmanr
import pandas as pd

def load_vectors(fname, dict_word_vec):
    fin = io.open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore')
    n, d = map(int, fin.readline().split())
    for line in fin:
        tokens = line.rstrip().split(' ')
        if dict_word_vec.get(tokens[0], 0) != 0:
            dict_word_vec[tokens[0]] = list(map(float, tokens[1:]))


def readfile(name, main_dict, dict_word_vec):
    f = open(name, 'r', encoding='utf-8', newline='\n', errors='ignore')
    main_dict['pairs'] = []
    main_dict['val'] = []
    main_dict['cos'] = []
    for s in f:
        word1, word2, val = s.split()
        main_dict['pairs'].append([word1, word2])
        main_dict['val'].append(val)
        dict_word_vec[word1] = []
        dict_word_vec[word2] = []
    f.close()


def cosine(u, v):
    numerator = 0
    sum1 = 0
    sum2 = 0
    for i in range(len(u)):
        numerator += u[i] * v[i]
        sum1 += u[i] ** 2
        sum2 += v[i] ** 2
    return numerator / ((sum1 ** 0.5) * (sum2 ** 0.5))


def cosines_calculating(main_dict, word_vec):
    for i in main_dict['pairs']:
        word1 = i[0]
        word2 = i[1]
        cos = cosine(word_vec[word1], word_vec[word2])
        main_dict['cos'].append(cos)



word_vec = defaultdict(list)
d_rel = defaultdict(list)
readfile('wordsim_relatedness_goldstandard.txt', d_rel, word_vec)
d_sim = defaultdict(list)
readfile('wordsim_similarity_goldstandard.txt', d_sim, word_vec)

load_vectors('crawl-300d-2M.vec', word_vec)

cosines_calculating(d_rel, word_vec)
cosines_calculating(d_sim, word_vec)

coef, p = spearmanr(d_rel['val'], d_rel['cos'])
print(coef, p)
coef, p = spearmanr(d_sim['val'], d_sim['cos'])
print(coef, p)