import random

def shuffle(a):
    for i in range(len(a))[::-1]:
        idx = random.randint(0, i)
        a[idx], a[i] = a[i], a[idx]
