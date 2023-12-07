import os
from pyswarm import pso


def banana(x):
    x1 = x[0]
    x2 = x[1]
    return x1**4 - 2*x2*x1**2 + x2**2 + x1**2 - 2*x1 + 5

def con(x):
    x1 = x[0]
    x2 = x[1]
    return [-(x1 + 0.25)**2 + 0.75*x2]

lb = [-3, -1]
ub = [2, 6]

xopt, fopt = pso(banana, lb, ub, f_ieqcons=con)
print(xopt,fopt)
#base_data = "DROGON_HIST_MSW-"
#cur_dir=os.getcwd()
#for i in range(5):
#    runner= (f"runeclipse -p eclipse -q bigmem ./realization-{i}/iter-0/eclipse/model/{base_data}{i}.DATA")
#    print(runner)
#    os.system(runner)
