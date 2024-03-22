# import nltk
# nltk.download('wordnet')
# nltk.download('wordnet_ic')

from nltk.corpus import wordnet
from nltk.corpus import wordnet_ic
from nltk.metrics import spearman_correlation


wordsim_simularity_file = 'wordsim_similarity_goldstandard.txt'
wordsim_relatedness_file = 'wordsim_relatedness_goldstandard.txt'

word_pairs_similarity = {}
word_pairs_relatedness = {}

with open(wordsim_simularity_file, 'r') as f:
    for line in f:
        line = line.replace('  ', ' ')
        word1, word2, similarity = line.strip().split()
        word_pairs_similarity[(word1, word2)] = float(similarity)

with open(wordsim_relatedness_file, 'r') as f:
    for line in f:
        line = line.replace('  ', ' ')
        word1, word2, relatedness = line.strip().split()
        word_pairs_relatedness[(word1, word2)] = float(relatedness)

lch_similarities = []
jcn_similarities = []
wup_similarities = []

brown_ic = wordnet_ic.ic('ic-brown.dat')

for cnt, word_pairs in enumerate([word_pairs_similarity, word_pairs_relatedness]):
    for word_pair in word_pairs:
        word1, word2 = word_pair
        try:
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
        except:
            continue

    lch_similarities.sort(key=lambda x: x[2], reverse=True)
    jcn_similarities.sort(key=lambda x: x[2], reverse=True)
    wup_similarities.sort(key=lambda x: x[2], reverse=True)

    for i in lch_similarities:
        print(f'LCH {"similarity" if cnt == 0 else "relatedness"} between {i[0]} and {i[1]}: {i[2]}')

    print('#'*50)

    for i in jcn_similarities:
        print(f'JCN {"similarity" if cnt == 0 else "relatedness"} between {i[0]} and {i[1]}: {i[2]}')

    print('#'*50)

    for i in wup_similarities:
        print(f'WUP {"similarity" if cnt == 0 else "relatedness"} between {i[0]} and {i[1]}: {i[2]}')

    print('#'*50)

    lch_ranks = {i[0] + i[1]: i[2] for i in lch_similarities}
    jcn_ranks = {i[0] + i[1]: i[2] for i in jcn_similarities}
    wup_ranks = {i[0] + i[1]: i[2] for i in wup_similarities}

    ranks = {i[0] + i[1]: word_pairs[i] for i in word_pairs}

    lch_correlation = spearman_correlation(ranks1=lch_ranks, ranks2=ranks)

    jcn_correlation = spearman_correlation(ranks1=jcn_ranks, ranks2=ranks)

    wup_correlation = spearman_correlation(ranks1=wup_ranks, ranks2=ranks)

    print(f'Spearman correlation for LCH {"similarity" if cnt == 0 else "relatedness"}: {lch_correlation}')
    print(f'Spearman correlation for JCN {"similarity" if cnt == 0 else "relatedness"}: {jcn_correlation}')
    print(f'Spearman correlation for WUP {"similarity" if cnt == 0 else "relatedness"}: {wup_correlation}')
