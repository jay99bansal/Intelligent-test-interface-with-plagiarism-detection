from similarity.normalized_levenshtein import NormalizedLevenshtein
from similarity.longest_common_subsequence import LongestCommonSubsequence
from similarity.metric_lcs import MetricLCS
from similarity.cosine import Cosine
from similarity.jaccard import Jaccard
import functools
import math
from nltk import word_tokenize 
from nltk.util import ngrams
import string

def pre_process(s):
    s = s.translate(str.maketrans('', '', string.punctuation))
    #s = s.replace(" ", "")
    return s.lower()

def dotproduct(v1, v2):
    return sum((a*b) for a, b in zip(v1, v2))

def length(v):
    return math.sqrt(dotproduct(v, v))

def cosangle(v1, v2):
    if ((length(v1) * length(v2)) != 0):
        return dotproduct(v1, v2) / (length(v1) * length(v2))
    return 0

def met_cosine_word(s1,s2,n):
    token = word_tokenize(s1)
    ngram = list(ngrams(token, n))
    ngram = ['~'.join(i) for i in ngram]
    freq1 = {} 
    for item in ngram: 
        if (item in freq1): 
            freq1[item] += 1
        else: 
            freq1[item] = 1
    token = word_tokenize(s2)
    ngram = list(ngrams(token, n))
    ngram = ['~'.join(i) for i in ngram]
    freq2 = {} 
    for item in ngram: 
        if (item in freq2): 
            freq2[item] += 1
        else: 
            freq2[item] = 1
    alldict = [freq1, freq2]
    allkey = functools.reduce(set.union, map(set, map(dict.keys, alldict)))
    vec1 = []
    vec2 = []
    for key in allkey:
        if key in freq1:
            vec1.append(freq1[key])
        else:
            vec1.append(0)
        if key in freq2:
            vec2.append(freq2[key])
        else:
            vec2.append(0)
    return cosangle(vec1, vec2)

def met_jaccard(s1,s2,n):
    jac = Jaccard(n)
    return jac.similarity(s1, s2)

def met_cosine(s1,s2,n):
    cosine = Cosine(n)
    p1 = cosine.get_profile(s1)
    p2 = cosine.get_profile(s2)
    return cosine.similarity_profiles(p1, p2)

def met_lcs(s1,s2):
    lcs = LongestCommonSubsequence()
    metric_lcs = MetricLCS()
    dist = lcs.distance(s1,s2)
    # our metric
    #print((len(s1)+len(s2)-dist)/(2*len(s1)))
    return 1-metric_lcs.distance(s1, s2)

def met_weighted(str1, str2):
    ind = []
    #ind.append(met_lcs(str1, str2))
    val1 = 0
    val2 = 0
    val3 = 0
    val4 = 0
    p = 1.2
    for i in range(1,5):
        k = i**p
        val4 += k
        val1 += met_cosine(str1, str2,i)*k
        val2 += met_jaccard(str1, str2,i)*k
        val3 += met_cosine_word(str1, str2,i)*k
    val1 = val1/val4
    val2 = val2/val4
    val3 = val3/val4
    # ind.append(met_lcs(str1, str2))
    ind.append(val1)
    ind.append(val2)
    ind.append(val3)
    met_weights = [0.2, 0.3, 0.5]
    ans = 0
    for i in range(0,len(ind)):
        ans+=ind[i]*met_weights[i]
    return ans


s1 = 'Plagiarism detection is the process of locating instances of plagiarism within a work or document. The widespread use of computers and the advent of the Internet have made it easier to plagiarize the work of others. Detection of plagiarism can be undertaken in a variety of ways. Human detection is the most traditional form of identifying plagiarism from written work. This can be a lengthy and time-consuming task for the reader and can also result in inconsistencies in how plagiarism is identified within an organization. Text-matching software (TMS), which is also referred to as "plagiarism detection software" or "anti-plagiarism" software, has become widely available, in the form of both commercially available products as well as open-source software. TMS does not actually detect plagiarism per se, but instead finds specific passages of text in one document that match text in another document.'

s2 = 'A dictionary has multiple key:value pairs. There can be multiple pairs where value corresponding to a key is a list. To check that the value is a list or not we use the isinstance() method which is inbuilt in Python. Plagiarism detection is the process of locating instances of plagiarism within a work or document. The widespread use of computers and the advent of the Internet have made it easier to plagiarize the work of others. Text-matching software, which is also referred to as "plagiarism detection software" or "anti-plagiarism" software.'

s1 = pre_process(s1)
s2 = pre_process(s2)

print(met_weighted(s1,s2))
