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
    ha.plot_surface(X, Y, avg_matrix)
    pt.show()


def show_mat(mtrx):
    import pylab as pt
    fig = pt.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(mtrx, interpolation='nearest')
    fig.colorbar(cax)
    pt.show()


data = []
res = []
for i in range(1, 5):
    data.append(parse('test/model-test-2-' + str(i) + '0.twords'))
    res.append(get_matrix(data[-1]))
avg_matrix = res[0]
for i in range(1, len(res)):
    avg_matrix = avg_matrix + res[i]
avg_matrix /= len(res)

show_mat(avg_matrix)
print(sorted(data[1][2][1].keys()))
print(sorted(data[1][41][1].keys()))