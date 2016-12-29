def parse_first():
    input_data = open('1.txt', 'r').read().splitlines()
    result = []
    topics = []
    topic = None
    for line in input_data:
        if line.startswith('\t'):
            poss = line.split()
            topics.append((poss[0], float(poss[1])))
        else:
            if topic is not None:
                result.append((topic, topics))
                topics = list()
            topic = line
    result.append((topic, topics))
    return result


def parse_second():
    input_data = open('2.txt', 'r').read().splitlines()
    result = {}
    for line in input_data:
        split = line.split()
        result[int(split[0])] = list(map(float, split[1:]))
    return result


def parse_third():
    input_data = open('3.txt', 'r').read().splitlines()
    result = {}
    for line in input_data:
        split = line.split()
        result[int(split[0])] = split[1]
    return result


themes = parse_first()
sites_themes = parse_second()
sites = parse_third()

out = open('out.txt', 'w')

for key in sites_themes:
    theme = max(range(len(sites_themes[key])), key=lambda x: sites_themes[key][x])
    out.write(' '.join([sites[key]] + [x[0] for x in themes[theme][1]]) + '\n')
out.close()