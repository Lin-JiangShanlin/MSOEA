import numpy as np
import convergence as cvg

'''get knee'''
def update_nor(p, s):
    return np.array([t.nor[s] for t in p])

def get_Knee(p, s, NK):
    nor_array = update_nor(p, s)

    tem = []
    for x in p: tem.append(x)
    while len(tem) > NK:
        rep_nor_array_1 = nor_array[np.newaxis, :, :].repeat(len(tem), axis = 0)
        rep_nor_array_2 = nor_array[:, np.newaxis, :].repeat(len(tem), axis = 1)
        ang = np.sum(rep_nor_array_1 * rep_nor_array_2, axis = 2) / (np.sqrt(np.sum(rep_nor_array_1 * rep_nor_array_1, axis = 2)) * np.sqrt(np.sum(rep_nor_array_2 * rep_nor_array_2, axis = 2)))
        mone, one = np.eye(len(tem)) * -1, 1 - np.eye(len(tem))
        ang = one * ang + mone

        max_i = np.argmax(ang)
        x1, x2 = max_i // len(tem), max_i % len(tem)

        x = delete_x(tem, x1, x2, s)
        del tem[x]
        nor_array = np.delete(nor_array, x, axis = 0)
    return tem

def delete_x(temp, x1, x2, s):
    if temp[x1].con[s] < temp[x2].con[s]: return x2
    return x1

'''get threshold,transfer,ar'''
def get_param(ks, k1, s1):
    k1_arr = np.array([y.len[s1] for y in k1])
    l_min = k1_arr.min()
    l_max = k1_arr.max()

    new = []
    for x in ks:
        if x not in k1 or x.s != s1:
            new.append(x)
    new_arr = np.array([y.len[s1] for y in new])
    o_min = new_arr.min()
    o_max = new_arr.max()
    return l_min, l_max, o_min, o_max


def get_slope(s, d, idx, z):
    # idx = min_idx[s]
    # z = ideal[s]
    x, y = [], []
    for i in range(len(idx)):
        x.append(idx[i].nor[s][0])
        y.append(idx[i].nor[s][1])

    if x[0] != x[1]:
        slope = (y[0] - y[1]) / (x[0] - x[1])
    else: slope = 1
    c1 = z[1] - slope * z[0]
    c2 = c1 + d * np.sqrt(1 + slope ** 2)
    return slope, c2

def get_trans(ks, Ar, s1, l_min, l_max, o_min, o_max, idx, z, tf, test_number):
    d = l_max
    a, b = get_slope(s1, d, idx, z)
    t = []
    for x in ks:
        if x.nor[s1][1] < (b + a * x.nor[s1][0]):
            if x.check_vio(func = tf, scene = s1):
                t.append(x)
                x.nr += 1
    return t

def update_pcos_ar(Ar, s1, l_min, l_max, o_min, idx, z, test_number):

    d = l_max
    a, b = get_slope(s1, d, idx, z)

    # 板块单独拿出来
    for pcos in Ar:
        if pcos.nor[s1][1] >= (b + a * pcos.nor[s1][0]):
            Ar.remove(pcos)
    return Ar

'''get extreme point'''
def get_ex(k1, s1):
    max_idx = []
    min_idx = []
    max_ex = []
    min_ex = []
    fn = len(k1[0].val[s1])
    for i in range(fn):
        value = np.array([k.val[s1][i] for k in k1])
        max_i = value.argmax()
        max_idx.append(k1[max_i])
        max_ex.append(k1[max_i].val[s1][i])

        min_i = value.argmin()
        min_idx.append(k1[min_i])
        min_ex.append(k1[min_i].val[s1][i])
    return max_idx