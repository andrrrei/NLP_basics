import math
import nltk
from collections import defaultdict
import pymorphy2
morph = pymorphy2.MorphAnalyzer()

def clear_text(name):
    # создаем список токенов, очищая текст от знаков препинания с помощью replace
    # и проводя лемматизацию слов с помощью pymorphy
    f = open(name, 'r')
    tokens = [] 
    for s in f:
        s = s.replace(',', '').replace('\n', ' ').replace('-', ' ').replace('.', '')
        s = s.split()
        for i in s:
            tokens.append(morph.parse(i)[0].normal_form)
    f.close()
    return tokens


def perplexy(lst, dict):
    summ = 0
    N = len(lst)
    for w in lst:
        summ += math.log2(dict[w])
    summ *= (- 1 / N)
    return 2 ** summ


# создаем список токенов, очищенных от знаков препинания
tokens = clear_text('poem.txt')
N = len(tokens)
V = len(set(tokens))

# используем словарь с функцией int по умолчанию для хранения частоты вхождения в текст каждой униграммы
c_unigrams = defaultdict(int)
for unigram in tokens:
    c_unigrams[unigram] += 1

# аналогично храним частоту вхождения в текст каждой биграммы,
# предварительно создав список биграмм с помощью nltk.bigrams
bigr = list(nltk.bigrams(tokens))
c_bigrams = defaultdict(int)
for bigram in bigr:
    c_bigrams[bigram] += 1

# повторяем процедуру для тестирующего текста
tokens = clear_text('test.txt')

# считаем вероятность каждой униграммы со сглаживанием Лапласа
unigrams_probability_LP = defaultdict(int)
for unigram in tokens:
    unigrams_probability_LP[unigram] = (c_unigrams.get(unigram, 0) + 1) / (N + V)

# считаем вероятность каждой биграммы со сглаживанием Лапласа
bigr = list(nltk.bigrams(tokens))
bigrams_probability_LP = defaultdict(int)
for bigram in bigr:
    bigrams_probability_LP[bigram] = (c_bigrams.get(bigram, 0) + 1) / (c_unigrams[bigram[0]] + len(c_bigrams) ** 2)


# считаем вероятность тестируемого множества для каждой униграммы и биграммы
P_unigrams = 1
for w, cnt in unigrams_probability_LP.items():
    P_unigrams *= cnt
P_bigrams = 1
for w, cnt in bigrams_probability_LP.items():
    P_bigrams *= cnt

# находим перплексию со сглаживанием Лагранжа
# print(round(perplexy(tokens, unigrams_probability_LP), 6), round(perplexy(bigr, bigrams_probability_LP), 6))


# считаем вероятности и перплексию со сглаживанием Линдстоуна
unigrams_probability_Lid = defaultdict(int)
bigrams_probability_Lid = defaultdict(int)
for i in range(1, 21):
    k = 0.05 * i
    for unigram in tokens:
        unigrams_probability_Lid[unigram] = (c_unigrams.get(unigram, 0) + k) / (N + V * k)
    for bigram in bigr:
        bigrams_probability_Lid[bigram] = (c_bigrams.get(bigram, 0) + k) / (c_unigrams[bigram[0]] + len(c_bigrams) * k)
    PP_u = perplexy(tokens, unigrams_probability_Lid)
    PP_b = perplexy(bigr, bigrams_probability_Lid)
    print(round(k, 2), round(PP_u, 6), round(PP_b, 6))