import numpy as np
import knee_trans_ar as kta

def env_select(temp1, s1, N):
    nor_array = kta.update_nor(temp1, s1)

    while len(temp1) > N:
        '''找到夹角最小的一对而不是找到一个随机个体的最小夹角'''
        rep_nor_array_1 = nor_array[np.newaxis, :, :].repeat(len(temp1), axis = 0)
        rep_nor_array_2 = nor_array[:, np.newaxis, :].repeat(len(temp1), axis = 1)
        ang = np.sum(rep_nor_array_1 * rep_nor_array_2, axis = 2) / (np.sqrt(np.sum(rep_nor_array_1 * rep_nor_array_1, axis = 2)) * np.sqrt(np.sum(rep_nor_array_2 * rep_nor_array_2, axis = 2)))
        mone, one = np.eye(len(temp1)) * -1, 1 - np.eye(len(temp1))
        ang = one * ang + mone

        max_i = np.argmax(ang)
        x1, x2 = max_i // len(temp1), max_i % len(temp1)
        
        x = kta.delete_x(temp1, x1, x2, s1)
        del temp1[x]
        nor_array = np.delete(nor_array, x, axis = 0)
    new = []
    cnt = 0
    for i in range(len(temp1)):
        if temp1[i].s == "at":
            cnt += 1
        temp1[i].s = s1
        new.append(temp1[i])

    return new, cnt