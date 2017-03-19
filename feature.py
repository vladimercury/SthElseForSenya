def parse(filename):
    file = open(filename, 'r')
    input_data = file.read().splitlines()
    file.close()
    result = []
    topics = dict()
    topic = None
    for line in input_data:
        if line.startswith('\t'):
            poss = line.split()
            topics[poss[0]] = float(poss[1])
        else:
            if topic is not None:
                result.append((topic, topics))
                topics = dict()
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
                x = len(set(topics[i][1]) & set(topics[j][1]))
                mat[i][j] = x
                mat[j][i] = x
    return mat


def get_arr(train, test):
    import numpy as np
    mat = np.zeros((len(train)))
    for i in range(len(train)):
        x = len(set(train[i][1]) & set(test[i][1]))
        mat[i] = x / len(train[i][1])
    return mat


def get_matrix_poss(topics):
    import numpy as np
    mat = np.zeros((len(topics), len(topics)))
    for i in range(len(topics)):
        for j in range(i, len(topics)):
            if i == j:
                mat[i][j] = 0
            else:
                left, right = topics[i][1], topics[j][1]
                common = set(left) & set(right)
                uncommon_left = set(left) - common
                uncommon_right = set(right) - common
                common_poss = sum([left[x] + right[x] for x in common])
                uncommon_poss = sum([left[x] for x in uncommon_left])
                uncommon_poss += sum([right[x] for x in uncommon_right])
                x = common_poss - uncommon_poss
                mat[i][j] = x
                mat[j][i] = x
    return mat


def get_arr_poss(train, test):
    import numpy as np
    mat = np.zeros((len(train)))
    for i in range(len(train)):
        left, right = train[i][1], test[i][1]
        common = set(left) & set(right)
        uncommon_left = set(left) - common
        common_poss = sum([left[x] for x in common])
        uncommon_poss = sum([left[x] for x in uncommon_left])
        x = common_poss - uncommon_poss
        mat[i] = x
        print({key: left[key] for key in common})
        print({key: right[key] for key in common})
    return mat


def get_arr_jaccard(train, test):
    import numpy as np
    mat = np.zeros((len(train)))
    for i in range(len(train)):
        c = len(set(train[i][1]) & set(test[i][1]))
        a = len(train[i][1]) + len(test[i][1])
        mat[i] = c / (a - c)
    return mat


def get_arr_jaccard_weight(train, test):
    import numpy as np
    mat = np.zeros((len(train)))
    for i in range(len(train)):
        left, right = train[i][1], test[i][1]
        common = set(left) & set(right)
        c = sum([right[x] for x in common])
        a = sum(left.values()) + sum(right.values())
        mat[i] = c / (a - c)
    return mat


def show_3dd(mtrx):
    import numpy as np
    import pylab as pt
    from mpl_toolkits.mplot3d import Axes3D
    nx, ny = mtrx.shape
    xr, yr = range(nx), range(ny)
    X, Y = np.meshgrid(xr, yr)
    fig = pt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(X, Y, mtrx, rstride=1, cstride=1, cmap='hot', linewidth=0, antialiased=False)
    fig.colorbar(surf, shrink=0.5, aspect=5)
    pt.show()


def show_3d(mtrx):
    import numpy as np
    import pylab as pt
    from mpl_toolkits.mplot3d import Axes3D
    nx, ny = mtrx.shape
    xr, yr = range(nx), range(ny)

    hf = pt.figure()
    ha = hf.add_subplot(111, projection='3d')

    X, Y = np.meshgrid(xr, yr)
    ha.plot_surface(X, Y, mtrx)
    pt.show()

def show_arr(mtrx):
    import pylab as pt
    fig = pt.figure()
    pt.plot(range(len(mtrx)), mtrx)
    pt.show()

def show_mat(mtrx):
    import pylab as pt
    fig = pt.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(mtrx, interpolation='nearest')
    fig.colorbar(cax)
    pt.show()


def normalize_weights(dat):
    for i in dat:
        coef = 1 / max(i[1].values())
        for j in i[1]:
            i[1][j] *= coef
#
# train_data = parse('/home/vladimercury/CppProjects/linkedLDA/model/training3/model-test-2.inf.twords')
# test_data = parse('/home/vladimercury/CppProjects/linkedLDA/model/test2/model-test-2.inf.twords')
train_data = parse ('test/model-test-2-30.twords')
test_data = parse('test/model-test-2-40.twords')

# normalize_weights(train_data)
# normalize_weights(test_data)

print(train_data)
print(test_data)

commons = get_arr(train_data, test_data)
print(commons)
show_arr(commons)

# for i in range(1, 5):
#     data.append(parse('test/model-test-2-' + str(i) + '0.twords'))
#     res.append(get_matrix(data[-1]))
# avg_matrix = res[0]
# for i in range(1, len(res)):
#     avg_matrix = avg_matrix + res[i]
# avg_matrix /= len(res)
#
# show_3d(avg_matrix)
# print(sorted(data[1][2][1].keys()))
# print(sorted(data[1][41][1].keys()))