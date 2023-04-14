import pandas as pd

from Individual import Ind
from Parameter import Parameter


def write_xlsx(Ar, scenario, test, path, name = ""):
    solution = []
    for i in range(len(Ar)):
        solution.append(Ar[i].x)
    data = {'x': solution}
    df = pd.DataFrame(data)
    if name: 
        df.to_csv(path + test + name + ".csv")
    else: df.to_csv(path + test + ".csv")
