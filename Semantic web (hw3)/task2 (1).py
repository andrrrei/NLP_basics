from nltk.corpus import wordnet as wn

def are_synonyms(word1, word2):
    lst1 = wn.synonyms(word1)
    lst2 = wn.synonyms(word2)
    flag = False
    for i in lst1:
        if word2 in i:
            flag = True
            return 1
    if flag == True:
        flag = False
        for i in lst2:
            if word1 in i:
                return 1
    return 0

def are_h_nyms(word1, word2):
    lst1 = wn.synsets(word1)
    lst2 = wn.synsets(word2)
    for i in range(len(lst1)):
        for j in range(len(lst2)):
            word1 = lst1[i]
            word2 = lst2[j]
            hypoword1 = set([i for i in word1.closure(lambda s:s.hyponyms())])
            hypoword2 = set([i for i in word2.closure(lambda s:s.hyponyms())])
            hyperword1 = set([i for i in word1.closure(lambda s:s.hypernyms())])
            hyperword2 = set([i for i in word2.closure(lambda s:s.hypernyms())])
            if word1 in hypoword2 or word1 in hyperword2 or word2 in hypoword1 or word2 in hyperword1:
                return 1
    return 0


f = open('wordsim353.txt', 'r')
f_syn = open('synonyms.txt', 'w')
f_h_onyms = open('h_nyms.txt', 'w')
f_other = open('other.txt', 'w')
synonyms_ev = 0
synonyms_cnt = 0
h_nyms_ev = 0
h_nyms_cnt = 0
other_ev = 0
other_cnt = 0

for s in f:
    if s[0] != '#':
        type, word1, word2, evaluation = s.split()
        if are_synonyms(word1, word2):
            print(word1, word2, file = f_syn)
            synonyms_ev += float(evaluation)
            synonyms_cnt += 1
        elif are_h_nyms(word1, word2):
            print(word1, word2, file = f_h_onyms)
            h_nyms_ev += float(evaluation)
            h_nyms_cnt += 1
        else:
            print(word1, word2, file = f_other)
            other_ev += float(evaluation)
            other_cnt += 1
        
print('Pairs of synonyms:', synonyms_cnt, '|', 'Average proximity weight:', synonyms_ev / synonyms_cnt)
print('Pairs of hyponym-hypernym:', h_nyms_cnt, '|',  'Average proximity weight:', h_nyms_ev / h_nyms_cnt)
print('Other link types:', other_cnt, '|', 'Average proximity weight:', other_ev / other_cnt)

f.close()
f_syn.close()
f_h_onyms.close()
f_other.close