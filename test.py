x = {'a': 0.3, 'b': 0.5, 'c': 0.6, 'd': 0.1}
c = 1 / max(x.values())
for i in x:
    x[i] *= c
print(x)