import numpy as np

def del_update(p, N, scenario):
    return min_x_man(p, N, scenario)

'''Manhattan distance'''
def min_x_man(p, N, scenario):
    temp = []
    for x in p: temp.append(x)
    x_nor = np.array([t.x for t in temp])
    t_arr = np.zeros((1, len(p)))
    for t1 in temp:
        tem = np.array([t1.s == t2.s for t2 in temp]) #equal = 1, un = 0, keep the 0
        t_arr = np.row_stack((t_arr, tem))
    t_arr = np.delete(t_arr, 0, axis = 0)
    rev = (np.ones((len(temp), len(temp))) - t_arr) * 10
    t_arr = t_arr + rev
    t_arr = t_arr * 10 #即首先删除不在同一个类别的

    while len(temp) > N:
        rep_x_nor_1 = x_nor[np.newaxis, :, :].repeat(len(temp), axis = 0)
        rep_x_nor_2 = x_nor[:, np.newaxis, :].repeat(len(temp), axis = 1)
        man = np.sum(abs(rep_x_nor_1 - rep_x_nor_2), axis = 2)
        max_man = np.max(man) * 2
        inf = np.eye(len(temp)) * max_man
        man = man + inf
        min_i = np.argmin(man)
        x1, x2 = min_i // len(temp), min_i % len(temp)

        x = delete_x(temp, x1, x2, scenario)

        del temp[x]
        x_nor = np.delete(x_nor, x, axis = 0)
        t_arr = np.delete(t_arr, x, axis = 0)
        t_arr = np.delete(t_arr, x, axis = 1)
    return temp

def delete_x(temp, x1, x2, scenario):
    less = 0
    equal = 0
    greater = 0
    for s in scenario:
        if temp[x1].con[s] < temp[x2].con[s]: less += 1
        elif temp[x1].con[s] == temp[x2].con[s]: equal += 1
        else: greater += 1
    if greater == 0 and equal != 0: return x2
    elif less == 0 and equal != 0: return x1
    else:
        x = find_min_ang(temp, x1, x2, scenario)
        return x

def find_min_ang(temp, x1, x2, scenario):
    x1_all_ang = np.zeros((len(temp)))
    x2_all_ang = np.zeros((len(temp)))
    for s in scenario:
        temp_arr = np.array([t.nor[s] for t in temp])
        x1_arr = np.array([temp[x1].nor[s]]).repeat(len(temp), axis = 0)
        x2_arr = np.array([temp[x2].nor[s]]).repeat(len(temp), axis = 0)
        x1_ang = np.sum(x1_arr * temp_arr, axis = 1) / (np.sqrt(np.sum(x1_arr * x1_arr, axis = 1)) * np.sqrt(np.sum(temp_arr * temp_arr, axis = 1)))
        x2_ang = np.sum(x2_arr * temp_arr, axis = 1) / (np.sqrt(np.sum(x2_arr * x2_arr, axis = 1)) * np.sqrt(np.sum(temp_arr * temp_arr, axis = 1)))
        x1_all_ang += x1_ang 
        x2_all_ang += x2_ang
    x1_all_ang[x1] = -1 # x1与所有其他个体的角度
    x2_all_ang[x2] = -1
    min_x1 = np.max(x1_all_ang) #没有换算成arccos，cos越大角度越小
    min_x2 = np.max(x2_all_ang)
    if min_x1 >= min_x2: return x1
    return x2

def delete_vector(temp, x1, x2, scenario):
    sn = len(scenario)
    con_x1 = np.array([temp[x1].con[s] for s in scenario])
    w_x1 = weight_vector(con_x1, sn)
    len_vec1 = np.sqrt(np.dot(w_x1, w_x1))
    fit1 = np.dot(con_x1, w_x1) / len_vec1

    con_x2 = np.array([temp[x2].con[s] for s in scenario])
    w_x2 = weight_vector(con_x2, sn)
    len_vec2 = np.sqrt(np.dot(w_x2, w_x2))
    fit2 = np.dot(con_x2, w_x2) / len_vec2

    if fit1 <= fit2: return x2
    else: return x1


def weight_vector(con, sn):
    sum_con = np.sum(con)
    v = []
    for i in range(sn):
        v.append(con[i] / sum_con)
    w = []
    sumv = 0
    for vi in v: sumv += (1 / vi)
    for j in range(sn):
        w.append((1 / v[j]) / sumv)
    return w