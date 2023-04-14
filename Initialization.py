import numpy as np
import random
from Individual import Ind

def initial(s, N, x_min, x_max, param, tf):
    p = []
    while len(p) < N:
        chromo = [random.uniform(a, b) for a, b in zip(x_min, x_max)]
        solution = Ind(chromo, s, param)
        if solution.check_vio(func = tf, scene = s): 
            p.append(solution)
    return p

def ideal_point(p, s, fn):
    # fn = f_num[s]
    ide = []
    nad = []
    min_idx = []
    max_idx = []
    for i in range(fn):
        value = np.array([t.val[s][i] for t in p])
        min_i = value.argmin()
        max_i = value.argmax()

        min_idx.append(p[min_i])
        max_idx.append(p[max_i])
        ide.append(p[min_i].val[s][i])
        nad.append(p[max_i].val[s][i])
    return min_idx, max_idx, ide, nad

def update(k1, s2, ide, idx, fn):
    """
    k1: 种群
    s2: 被更新场景
    """
    # ide = ideal[s2]
    # idx = min_idx[s2]
    # fn = f_num[s2]
    new_ide = []
    new_idx = []
    for i in range(fn):
        fmin = ide[i]
        fidx = idx[i]
        for j in range(len(k1)):
            if s2 not in k1[j].val: k1[j].fitness(s2) #给knee个体赋值
        val_arr = np.array([k.val[s2][i] for k in k1])
        val_min = val_arr.min()
        val_idx = val_arr.argmin()
        if val_min < fmin:
            fmin = val_min
            fidx = k1[val_idx]
        new_ide.append(fmin)
        new_idx.append(fidx)
    return new_ide, new_idx