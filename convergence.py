import numpy as np
def cal_con(p, s, ide, nad, fn):
    # ide = ideal[s]
    # fn = f_num[s]
    for i in range(len(p)):
        cal_pbi(p[i], s, ide, fn)

def cal_pbi(x, s, ide, fn):
    if s not in x.val: x.fitness(s)
    nor_x = normalize(x, s, ide, fn)
    x.nor[s] = nor_x

    nor_arr = np.array([nor_x])
    len_nor = np.linalg.norm(nor_arr, ord = 2, axis = 1, keepdims = True)[0][0] #write in euc
    x.len[s] = len_nor #用于计算阈值选择Ar

    vec_x = weight(nor_x, s, fn)
    len_vec = np.sqrt(np.dot(vec_x, vec_x))
    fit = np.dot(nor_x, vec_x) / len_vec
    x.con[s] = fit #用于计算个体的收敛性进行更新

def normalize(x, s, ide, fn):
    nor = []
    for i in range(fn):
        cur = (x.val[s][i] - ide[i])
        if cur == 0: cur = 1e-4
        nor.append(cur)
    return nor


def weight(nor, s, fn):
    sumf = np.sum(nor)
    v = []
    for i in range(fn):
        v.append(nor[i] / sumf)
    # return v
    w = []
    sumv = 0
    for vi in v: sumv += (1 / vi)
    for j in range(fn):
        w.append((1 / v[j]) / sumv)
    return w