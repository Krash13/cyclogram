import random
import numpy as np

def less(a, b, xa, xb):
    if a is None:
        return False
    if b is None:
        return True
    if a < b:
        return True
    if a == b:
        if sum(xa) < sum(xb):
            return True
    return False

def myround(x, base=5):
    return base * round(x/base)

def sort(x,f):
    k = 1
    while k > 0:
        k = 0
        for i in range(len(f)-1):
            if less(f[i+1], f[i], x[i+1], x[i]):
                temp = f[i]
                f[i] = f[i+1]
                f[i+1] = temp
                temp = x[i]
                x[i] = x[i+1]
                x[i+1] = temp
                k += 1

def my_min(f):
    min = None
    for fi in f:
        if fi is None:
            continue
        if min is None:
            min = fi
            continue
        if fi < min:
            min = fi
    return min

def my_max(f):
    max = None
    for fi in f:
        if fi is None:
            continue
        if max is None:
            max = fi
            continue
        if fi > max:
            max = fi
    return max



# print(IWO(10, 30, 0, 10, 3, 0.000001, [-5,-5,-5], [5,5,5], 3, 150))
