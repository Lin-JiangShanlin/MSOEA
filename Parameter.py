import numpy as np
class Parameter():
    def __init__(self, test):
        # 3-scenarios
        if test == "3SBP1":
            NDim = 2
            self.x_num = NDim
            self.MIN_BOUND = np.zeros(NDim)
            self.MAX_BOUND = [4, 1.75]
            self.f_num = {'3SBP1f1': 2, '3SBP1f2': 2, '3SBP1f3': 2}
            self.scenarios = ['3SBP1f1', '3SBP1f2', '3SBP1f3']
            self.tran_cnt = {"3SBP1f1": [], "3SBP1f2": [], "3SBP1f3": []}
            self.keep_cnt = {"3SBP1f1": [], "3SBP1f2": [], "3SBP1f3": []}
            self.off_cnt = {"3SBP1f1": [], "3SBP1f2": [], "3SBP1f3": []}