from nltk.corpus import wordnet as wn

a = wn.synsets('dog')[0]
b = wn.synsets('cat')[0]
print(a.wup_similarity(b))
