from merging import parse_first
from fractions import Fraction
from pprint import pprint
from TextSimilarity import TextSimilarity
import numpy as np


N_TOPICS = 1
#PATH_PREFIX = '/home/vladimercury/CppProjects/linkedLDA/model/model-new-'
PATH_PREFIX = 'test/model-test-2-'
SINGLE_PATH = '/home/vladimercury/PycharmProjects/SthElseForSenya/test/model-min.twords'
FILES_LIST = [
    '/home/vladimercury/CppProjects/linkedLDA/model/training3/model-test-2.inf.twords',
    '/home/vladimercury/CppProjects/linkedLDA/model/test2/model-test-2.inf.twords',
]
# FILES_LIST = [
#     'test/model-test-2-10.twords',
#     'test/model-test-2-20.twords',
# ]
PATH_RANGE_START = 10
PATH_RANGE_END = 40
PATH_RANGE_STEP = 10


def nok(a, b):
    z = a * b
    while a:
        a, b = b % a, a
    return z // b


# def get_topics(n):
#     topics_list = [[] for i in range(n)]
#     for i in range(PATH_RANGE_START, PATH_RANGE_END + 1, PATH_RANGE_STEP):
#         topics = parse_first(PATH_PREFIX + str(i) + '.twords')
#         for j in range(len(topics)):
#             topics_list[j].append(topics[j])
#     return topics_list


def get_topics(n):
    topics_list = [[] for i in range(n)]
    for i in FILES_LIST:
        topics = parse_first(i)
        for j in range(len(topics)):
            topics_list[j].append(topics[j])
    return topics_list


def get_topics_single_file():
    topics_list = [[]]
    topics = parse_first(SINGLE_PATH)
    for topic in topics:
        topics_list[0].append(topic)
    return topics_list

#
#
#
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

#
#
#
def normalize_weights(data):
    normalized_data = []
    for topic in data:
        line = list()
        normalizer = 0
        for word in topic[1]:
            normalizer += word[1]
        normalizer = 1 / normalizer
        for word in topic[1]:
            line.append((word[0], word[1] * normalizer))
        normalized_data.append(line)
    return normalized_data


def generate_tfidf(data):
    from math import log10
    terms = dict()
    index = 0
    terms_freq = dict()
    normalized = normalize_weights(data)
    n_docs = len(normalized)
    for topic in normalized:
        for term in topic:
            if (term[0] in terms):
                terms_freq[term[0]] += 1
            else:
                terms[term[0]] = index
                index += 1
                terms_freq[term[0]] = 1
    import numpy as np
    tfidf = np.zeros((n_docs, len(terms)))
    for i in range(len(normalized)):
        topic = normalized[i]
        for term in topic:
            tfidf[i][terms[term[0]]] = term[1] * log10(1 + n_docs / terms_freq[term[0]])
    return tfidf


def sparse_to_tuples(sparse_matrix):
    nonzero = sparse_matrix.nonzero()
    tuples = []
    for i in range(len(nonzero[0])):
        x, y = nonzero[0][i], nonzero[1][i]
        tuples.append([x, y, sparse_matrix[(x,y)]])
    return tuples


def print_cosine(cosine_matrix, stream):
    from scipy import sparse
    sparse_cosine = sparse_to_tuples(sparse.csr_matrix(np.triu(np.asarray(cosine_matrix), k=1)))
    print(np.asarray(sorted(sparse_cosine, key=lambda x: x[2], reverse=True)), file=stream)

file = open('cosine.txt', 'w')
file2 = open('cosine2.txt', 'w')
np.set_printoptions(linewidth=100000)
np.set_printoptions(threshold=np.nan)
np.set_printoptions(suppress=True)
topic_set = get_topics(N_TOPICS)
#topic_set = get_topics_single_file()

for topic_num in range(len(topic_set)):
    print('File ' + str(topic_num + 1), file=file)
    print('File ' + str(topic_num + 1), file=file2)
    print_cosine(TextSimilarity().get_cosine_similarity(generate_text(normalize_fractions(generate_fractions(topic_set[topic_num])))), file)
    print_cosine(TextSimilarity().get_cosine_similarity_tfidf(generate_tfidf(topic_set[topic_num])), file2)
file.close()
file2.close()