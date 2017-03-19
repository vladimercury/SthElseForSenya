from merging import parse_first
from fractions import Fraction
from pprint import pprint
from TextSimilarity import TextSimilarity
import numpy as np


N_TOPICS = 2
PATH_PREFIX = '/home/vladimercury/CppProjects/linkedLDA/model/model-new-'
PATH_RANGE_START = 20
PATH_RANGE_END = 60
PATH_RANGE_STEP = 20


def nok(a, b):
    z = a * b
    while a:
        a, b = b % a, a
    return z // b


def get_topics(n):
    topics_list = [[] for i in range(n)]
    for i in range(PATH_RANGE_START, PATH_RANGE_END + 1, PATH_RANGE_STEP):
        topics = parse_first(PATH_PREFIX + str(i) + '.twords')
        for j in range(len(topics)):
            topics_list[j].append(topics[j])
    return topics_list


def generate_fractions(data):
    fractions = list()
    for topic in data:
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
topic_set = get_topics(N_TOPICS)
for topic_num in range(len(topic_set)):
    print('Topic ' + str(topic_num + 1), file=file)
    print(np.asarray(TextSimilarity().get_cosine_similarity(generate_text(normalize_fractions(generate_fractions(topic_set[topic_num]))))), file=file)
file.close()

