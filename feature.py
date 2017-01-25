def parse(filename):
    file = open(filename, 'r')
    input_data = file.read().splitlines()
    file.close()
    result = []
    topics = set()
    topic = None
    for line in input_data:
        if line.startswith('\t'):
            poss = line.split()
            topics.add(poss[0])
        else:
            if topic is not None:
                result.append((topic, topics))
                topics = set()
            topic = line
    result.append((topic, topics))
    return result


def get_matrix(topics):
    import numpy as np
    mat = np.zeros((len(topics), len(topics)))
    for i in range(len(topics)):
        for j in range(i, len(topics)):
            if i == j:
                mat[i][j] = 0
            else:
                x = len(topics[i][1] & topics[j][1])
                mat[i][j] = x
                mat[j][i] = x
    return mat

import pylab as pt
res = []
for i in range(1, 5):
    res.append(get_matrix(parse('test/model-test-2-' + str(i) + '0.twords')))
avg_matrix = res[0]
for i in range(1, len(res)):
    avg_matrix = avg_matrix + res[i]
avg_matrix /= len(res)

pt.matshow(res[0])
pt.matshow(avg_matrix)

pt.show()