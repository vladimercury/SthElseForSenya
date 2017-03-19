from merging import parse_first
from fractions import Fraction
from pprint import pprint
from TextSimilarity import TextSimilarity
import numpy as np


def nok(a, b):
    z = a * b
    while a:
        a, b = b % a, a
    return z // b


def generate_fractions():
    topics = []
    for i in range(20, 101, 20):
        topics += parse_first('/home/vladimercury/CppProjects/linkedLDA/model/model-new-' + str(i) + '.twords')
    fractions = list()
    for topic in topics:
        line = list()
        normalizer = 1 / topic[1][0][1]
        for word in topic[1]:
            line.append((word[0], Fraction(word[1] * normalizer).limit_denominator(10)))
        fractions.append(line)
    return fractions


def normalize_fractions(topics):
    for i in range(len(topics)):
        multiplier = 1
        for j in range(len(topics[i])):
            multiplier = nok(multiplier, topics[i][j][1].denominator)
        for j in range(len(topics[i])):
            topics[i][j] = (topics[i][j][0], topics[i][j][1] * multiplier)
    return topics


def generate_text(topics):
    text = []
    for topic in topics:
        line = ''
        for word in topic:
            for i in range(word[1].numerator):
                line += word[0] + ' '
        text.append(line)
    return text

file = open('cosine.txt', 'w')
np.set_printoptions(linewidth=1000)
print(np.asarray(TextSimilarity().get_cosine_similarity(generate_text(normalize_fractions(generate_fractions())))), file=file)
file.close()
