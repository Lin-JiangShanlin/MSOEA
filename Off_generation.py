import numpy as np
import random
from Off_operator import SBX, poly_mut

def close_t(x1, ar, s1):
    x1_arr = np.array([x1.nor[s1] for _ in range(len(ar))])
    ar_arr = np.array([a.nor[s1] for a in ar])
    ang = np.sum(x1_arr * ar_arr, axis = 1) / (np.sqrt(np.sum(x1_arr * x1_arr, axis = 1)) * np.sqrt(np.sum(ar_arr * ar_arr, axis = 1)))
    b = np.argmin(ang)
    return b

def crossover_mutation(p1, p2, s1, cm_param, param):
    off1, off2 = p1, p2
    if random.random() < cm_param["pc"]:
        off1, off2 = SBX(off1, off2, s1, cm_param["x_num"], cm_param["eta_c"], param)
    if random.random() < cm_param["pm"]:
        off1, off2 = poly_mut(off1, off2, s1, cm_param["x_num"], cm_param["eta_m"], param)
    return off1, off2

def get_off(p1, ar, s1, Arp, N, tf, cm_param, param):
	# tf = test_function
    off = []
    nat = len(ar)
    if s1 in Arp:
        arp = Arp[s1]
    else: arp = 0

    cnt = 0
    while len(off) < N:
        flag = False
        a = random.randint(0, N - 1)
        x1 = p1[a]
        if random.random() < arp and nat != 0:
            b = random.randint(0, nat - 1)
            # b = close_t(x1, ar, s1)
            x2 = ar[b]
            flag = True
        else:
            b = random.randint(0, N - 1)
            while b == a: b = random.randint(0, N - 1)
            x2 = p1[b]
        o1, o2 = crossover_mutation(x1, x2, s1, cm_param, param)

        if o1.check_vio(func = tf, scene = s1):
            if flag:
                cnt += 1
                o1.s = "at"
            off.append(o1)
        if o2.check_vio(func = tf, scene = s1):
            if flag: 
                o2.s = "at"
            off.append(o2)
    return off, cnt


def get_off_no_trans(p1, s1, N, tf, cm_param, param):
	# tf = test_function
    off = []
    while len(off) < N:
        a = random.randint(0, N - 1)
        x1 = p1[a]

        b = random.randint(0, N - 1)
        while b == a: b = random.randint(0, N - 1)
        x2 = p1[b]
        o1, o2 = crossover_mutation(x1, x2, s1, cm_param, param)


        if o1.check_vio(func = tf, scene = s1):
            off.append(o1)
        if o2.check_vio(func = tf, scene = s1):
            off.append(o2)
    return off, 0