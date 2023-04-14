import random
from Individual import Ind

def SBX(p1, p2, s1, x_num, eta_c, param):
    off1x, off2x = [], []
    for j in range(x_num):
        u1 = random.random()
        if (u1 <= 0.5):
            gama = float((2 * u1) ** (1 / (eta_c + 1)))
        else:
            gama = float((1 / (2 * (1 - u1))) ** (1 / (eta_c + 1)))
        
        off11 = float(0.5 * ((1 + gama) * p1.x[j] + (1 - gama) * p2.x[j]))
        off22 = float(0.5 * ((1 - gama) * p1.x[j] + (1 + gama) * p2.x[j]))
        off1x.append(off11)
        off2x.append(off22)
    off1 = Ind(off1x, s1, param)
    off2 = Ind(off2x, s1, param)
    return off1, off2

def poly_mut(p1, p2, s1, x_num, eta_m, param):
    off1x, off2x = [], []
    for j in range(x_num):
        u2 = random.random() # do gaussian-distribution mean = 0 std = sigma in <ea with gd>
        if (u2 <= 0.5):
            delta = float((2 * u2) ** (1 / (eta_m + 1)) - 1)
        else:
            delta = float(1 - (2 * (1 - u2)) ** (1 / (eta_m + 1)))
        off11 = float(p1.x[j] + delta)

        u2 = random.random()
        if (u2 <= 0.5):
            delta = float((2 * u2) ** (1 / (eta_m + 1)) - 1)
        else:
            delta = float(1 - (2 * (1 - u2)) ** (1 / (eta_m + 1)))
        off22 = float(p2.x[j] + delta)
        off1x.append(off11)
        off2x.append(off22)
    off1 = Ind(off1x, s1, param)
    off2 = Ind(off2x, s1, param)
    return off1, off2
