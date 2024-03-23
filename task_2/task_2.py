import io
import time

import fasttext


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

def load_vectors(fname):
    fin = io.open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore')
    n, d = map(int, fin.readline().split())
    data = {}
    for line in fin:
        tokens = line.rstrip().split(' ')
        data[tokens[0]] = map(float, tokens[1:])
    return data

print("Loading vectors...")

time_start = time.time()
vectors = load_vectors("wiki-news-300d-1M.vec")
time_end = time.time()

print(f"Time taken to load vectors: {time_end - time_start}")

cnt = 0
for vector in vectors:
    print(vector)
    print(vectors[vector])
    if cnt == 10:
        break
    cnt += 1

# for cnt, word_pairs in enumerate([word_pairs_similarity, word_pairs_relatedness]):
