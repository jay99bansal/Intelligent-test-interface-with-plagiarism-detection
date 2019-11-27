##@file Match_strings.py
#@brief This file of the project is applying various string matching algorithms for detecting plagiarism between subjective type questions.
#@details In this analysis of various string matching algorithms implemented in strsim library is done and then the algorithms whose
#performance is good enough for the task are used combinely to come up with a fair match index between strings.
#@author Infernos : CS699 Course Project Software Lab
#@date Thursday, November 29, 2019

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
#@brief This function is taking a String as an argument, truncating spaces and converting it to a lowercase substring as a whole.
#@return String 
#@param s String 
#
def pre_process(s):
    s = s.translate(str.maketrans('', '', string.punctuation))
    # s = s.replace(" ", "")
    return s.lower()

##
#@brief This function is taking two vectors as arguments and returning a single dot product value for them.
#@return Dot product of both the agruments
#@param V1 vector 1
#@param V2 vector 2
#
def dotproduct(v1, v2):
    return sum((a * b) for a, b in zip(v1, v2))

##
#@brief This function is taking a vector as argument and returning a single value which is norm of it.
#@return Norm of the vector
#@param V1 vector 1
#
def length(v):
    return math.sqrt(dotproduct(v, v))

##
#@brief This function is taking two vectors as arguments and returning a single cosine value of the angle between these vectors.
#@return Cosine of the angle between the two vectors
#@param V1 vector 1
#@param V2 vector 2
#
def cosangle(v1, v2):
    if (length(v1) * length(v2)) != 0:
        return dotproduct(v1, v2) / (length(v1) * length(v2))
    return 0

##
#@brief This function is taking two vectors as arguments and returning a single cosine value of the angle between these vectors.
#@return Cosine of the angle between two vectors formed by taking frequency of words instead of characters
#@param s1 String 
#@param s2 String 
#
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
