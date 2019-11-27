##@file python_problem.py
#@author Infernos:CS699
#@brief Implementing doxygen-style comments for documenting a python
#program and the functions inside.
#@details This program is implementing some python functions on the given data file of integers. 
#@date Thursday, October 28, 2019
#

##Include section
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

##
#@brief This function is taking a filename as argument and returning a list of integers inside the file.
#@details The given file contains integers each line. This function is picking out text line by line, typecasting it to integers
#and appending it to a list. Finally it is returning that list.
#@return l list 
#@param filename the name of the file 
#
def pre_process(s):
    s = s.translate(str.maketrans('', '', string.punctuation))
    # s = s.replace(" ", "")
    return s.lower()


def dotproduct(v1, v2):
    return sum((a * b) for a, b in zip(v1, v2))


def length(v):
    return math.sqrt(dotproduct(v, v))


def cosangle(v1, v2):
    if (length(v1) * length(v2)) != 0:
        return dotproduct(v1, v2) / (length(v1) * length(v2))
    return 0


def met_cosine_word(s1, s2, n):
    token = word_tokenize(s1)
    ngram = list(ngrams(token, n))
    ngram = ['~'.join(i) for i in ngram]
    freq1 = {}
    for item in ngram:
        if item in freq1:
            freq1[item] += 1
        else:
            freq1[item] = 1
    token = word_tokenize(s2)
    ngram = list(ngrams(token, n))
    ngram = ['~'.join(i) for i in ngram]
    freq2 = {}
    for item in ngram:
        if item in freq2:
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


def met_jaccard(s1, s2, n):
    jac = Jaccard(n)
    return jac.similarity(s1, s2)


def met_cosine(s1, s2, n):
    cosine = Cosine(n)
    p1 = cosine.get_profile(s1)
    p2 = cosine.get_profile(s2)
    val = cosine.similarity_profiles(p1, p2)
    return val


def met_lcs(s1, s2):
    lcs = LongestCommonSubsequence()
    metric_lcs = MetricLCS()
    dist = lcs.distance(s1, s2)
    # our metric
    # print((len(s1)+len(s2)-dist)/(2*len(s1)))
    return 1 - metric_lcs.distance(s1, s2)


def plag_index_strings(str1, str2, weight):
    ind = []
    # ind.append(met_lcs(str1, str2))
    val1 = 0
    val2 = 0
    val3 = 0
    val4 = 0
    p = 1.2
    nw1 = len(str1.split())
    nw2 = len(str2.split())
    for i in range(1, 5):
        if nw1 >= i and nw2 >= i:
            k = i ** p
            val4 += k
            val1 += met_cosine(str1, str2, i) * k
            val2 += met_jaccard(str1, str2, i) * k
            val3 += met_cosine_word(str1, str2, i) * k
    if val4 != 0:
        val1 = val1 / val4
        val2 = val2 / val4
        val3 = val3 / val4
    ind.append(met_lcs(str1, str2))
    ind.append(val1)
    ind.append(val2)
    ind.append(val3)
    ans = 0
    for i in range(0, len(ind)):
        ans += ind[i] * weight[i]
    return ans
