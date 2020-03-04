import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = (15, 5)
brains = []


def analise(data):
    for i in data:
        brains.append((i.brain, i.my_id))
    count_talants(brains[0])


def count_talants(data):
    result = {i: 0 for i in range(20)}
    for i in data[0]:
        result[i] += 1

    Data = {'kkey': list(result.keys()), 'vvalue': list(result.values())}
    print(Data)

    res = pd.DataFrame(Data)
    print(res)

    res.plot(x='kkey', y='vvalue', kind='scatter')
    plt.show()


