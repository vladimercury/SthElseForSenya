def parse_first(filename='/home/vladimercury/CppProjects/linkedLDA/model/model-new-20.twords'):
    input_data = open(filename, 'r').read().splitlines()
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
            split = line.split()
            topic = ' '.join(split[:-1])
            has_class = split[-1]
    result.append((topic, topics))
    return result


def parse_second():
    input_data = open('/home/vladimercury/CppProjects/linkedLDA/model/model-new-20.theta', 'r').read().splitlines()
    result = {}
    for line in input_data:
        split = line.split()
        result[int(split[0])] = list(map(float, split[1:]))
    return result


def parse_third():
    input_data = open('/home/vladimercury/IdeaProjects/website-definition/storage/output/1489078719624/indexed.mapping.data', 'r').read().splitlines()
    result = {}
    for line in input_data:
        split = line.split()
        result[int(split[0])] = split[1]
    return result


# themes = parse_first()
# sites_themes = parse_second()
# sites = parse_third()
#
# out = open('out.txt', 'w')
#
# for key in sites_themes:
#     theme = max(range(len(sites_themes[key])), key=lambda x: sites_themes[key][x])
#     out.write(sites[key]+ ' ' + themes[theme][1] + '\n')
# out.close()