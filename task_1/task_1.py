# import nltk
# nltk.download('wordnet')
# nltk.download('wordnet_ic')

from nltk.corpus import wordnet
from nltk.corpus import wordnet_ic
from nltk.metrics import spearman_correlation


WORD_PAIRS = [
    ('tiger', 'cat'),
    ('plane', 'car'),
    ('train', 'car'),
    ('television', 'radio'),
    ('media', 'radio'),
    ('bread', 'butter'),
    ('cucumber', 'potato'),
    ('doctor', 'nurse'),
    ('professor', 'doctor'),
    ('student', 'professor'),
    ('smart', 'stupid'),
    ('wood', 'forest'),
    ('money', 'cash'),
    ('computer', 'keyboard'),
    ('Jerusalem', 'Israel'),
    ('planet', 'galaxy'),
    ('canyon', 'landscape'),
    ('OPEC', 'country'),
    ('day', 'summer'),
    ('day', 'dawn'),
    ('country', 'citizen'),
    ('planet', 'people'),
    ('environment', 'ecology'),
    ('Maradona', 'football'),
    ('OPEC', 'oil'),
    ('money', 'bank'),
]

lch_similarities = []
jcn_similarities = []
wup_similarities = []

brown_ic = wordnet_ic.ic('ic-brown.dat')
for word_pair in WORD_PAIRS:
    word1, word2 = word_pair
    synset1 = wordnet.synsets(word1)
    synset2 = wordnet.synsets(word2)

    if synset1 and synset2:
        lch_similarity = synset1[0].lch_similarity(synset2[0])
        jcn_similarity = synset1[0].jcn_similarity(synset2[0], brown_ic)
        wup_similarity = synset1[0].wup_similarity(synset2[0])
    else:
        lch_similarity = 0
        jcn_similarity = 0
        wup_similarity = 0

    lch_similarities.append((word1, word2, lch_similarity))
    jcn_similarities.append((word1, word2, jcn_similarity))
    wup_similarities.append((word1, word2, wup_similarity))

lch_similarities.sort(key=lambda x: x[2], reverse=True)
jcn_similarities.sort(key=lambda x: x[2], reverse=True)
wup_similarities.sort(key=lambda x: x[2], reverse=True)

for i in lch_similarities:
    print(f'LCH similarity between {i[0]} and {i[1]}: {i[2]}')

print('#'*50)

for i in jcn_similarities:
    print(f'JCN similarity between {i[0]} and {i[1]}: {i[2]}')

print('#'*50)

for i in wup_similarities:
    print(f'WUP similarity between {i[0]} and {i[1]}: {i[2]}')

print('#'*50)

lch_ranks = {i[0] + i[1]: i[2] for i in lch_similarities}
jcn_ranks = {i[0] + i[1]: i[2] for i in jcn_similarities}
wup_ranks = {i[0] + i[1]: i[2] for i in wup_similarities}

lch_jcn_correlation = spearman_correlation(ranks1=lch_ranks, ranks2=jcn_ranks)

lch_wup_correlation = spearman_correlation(ranks1=lch_ranks, ranks2=wup_ranks)

jcn_wup_correlation = spearman_correlation(ranks1=jcn_ranks, ranks2=wup_ranks)

print(f'Spearman correlation between LCH and JCN similarities: {lch_jcn_correlation}')
print(f'Spearman correlation between LCH and WUP similarities: {lch_wup_correlation}')
print(f'Spearman correlation between JCN and WUP similarities: {jcn_wup_correlation}')
