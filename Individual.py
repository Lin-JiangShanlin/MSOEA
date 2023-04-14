import numpy as np
from Parameter import Parameter


'''initialization'''
class Ind():
    def __init__(self, x, task, param):
        self.param = param
        self.x = x
        self.s = task
        self.val = {}
        self.con = {}
        self.nor = {}
        self.len = {}
        self.cr = 0 #用于MS-NSGA
        self.nr = 0 
        self.fitness(task)
    
    def fitness(self, task):
        fit = []

        # 3-scenarios
        if task == "3SBP1f1":
            f1 = (self.x[0] - 4) ** 2 + (self.x[1] - 1) ** 2
            f2 = (self.x[0] - 5) ** 2 + (self.x[1] - 4) ** 2
            fit = [f1, f2]
        elif task == "3SBP1f2":
            f1 = self.x[0] ** 2 + (self.x[1] - 4) ** 2
            f2 = (self.x[0] - 6) ** 2 + (self.x[1] - 2) ** 2
            fit = [f1, f2]
        elif task == "3SBP1f3":
            f1 = (self.x[0] - 2) ** 2 + (self.x[1] - 1) ** 2
            f2 = (self.x[0] - 3) ** 2 + (self.x[1] - 4) ** 2
            fit = [f1, f2]

        if fit: self.val[task] = fit



    
    def check_vio(self, func, scene):
        test_list = ["3SBP1"]
        if func in test_list:
            x_arr = np.array(self.x)
            if (x_arr < self.param.MIN_BOUND).any() or (x_arr > self.param.MAX_BOUND).any(): 
                return False
            if (self.x[1] ** 2 - self.x[0] * 0.5) <= 0 and ((self.x[0] - 2) ** 2 + self.x[1] ** 2 - 4) <= 0:
                return True
            else: return False