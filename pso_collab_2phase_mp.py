import numpy as np
import time
import os
import sch_twophase
import writer_data_nogascap
import calc_economic
import pyDOE
from copy import deepcopy
import json
import multiprocessing


def re100(x,j):
    input = x.vars
    problem = x.cid
    particle = j
    iteration = x.itr
    os.chdir("/private/hsut/private/opt/egg_2phase_collab/include/schedule")
    sch_twophase.write_file(input, problem, particle, iteration)
    os.chdir("/private/hsut/private/opt/egg_2phase_collab/model")
    writer_data_nogascap.write_file(input, problem, particle, iteration)
    init=f"{problem}_{iteration}_{particle}"
    deck=f"/private/hsut/private/opt/egg_2phase_collab/model/EGG_{problem}_{iteration}_{particle}.DATA"
    runner= (f"runeclipse -p eclipse -q mr -v 2022.4 {deck}")
    os.system(runner)
    time.sleep(15)
    prt=f"/private/hsut/private/opt/egg_2phase_collab/model/EGG_{problem}_{iteration}_{particle}.PRT"
    while not os.path.exists(prt):
        print(f"rerun eclipse problem {problem} iteration {iteration}  particle {particle} ")
        os.system(runner)
        time.sleep(60)
    while True:
        with open(prt, "r") as file:
            lines = file.readlines()
            if len(lines)>0:
                #print(f"found PRT problem {problem} iteration {iteration}  particle {particle} ")
                complete_line = lines[-1]
                errors_line = lines[-4].strip()
                bugs_line = lines[-3].strip()
                if "Total number of time steps" in complete_line:
                    errors = int(errors_line.split()[1])
                    bugs = int(bugs_line.split()[1])
                    if errors > 0 or bugs > 0:
                        print(f"rerun error eclipse problem {problem} iteration {iteration}  particle {particle} ")
                        os.system(runner)
                        time.sleep(10)
                    else:
                        #print(f"calculate co2 problem {problem} iteration {iteration}  particle {particle} ")
                        simulation_result = calc_economic.NPV(deck, 10, 40, 0, init)
                        return simulation_result
                #break

def calculatorco2(simulation_result,co2,gasprice):
    npv=simulation_result.npv(0.15,60,gasprice,co2)            
    z=-npv
    return z

out = "/private/hsut/private/opt/egg_2phase_collab/trialpso"
if not os.path.isdir(out):
    #shutil.rmtree(out)
    os.mkdir(out)

coop =  "True"   # This argument will decide to run either the collaborative or the non-collaborative PSO.
run = 10 #change from sys arg
out = out + "/C-PSO"
if not os.path.isdir(out):
    os.mkdir(out)
out = out + "/Run" + str(run)
if not os.path.isdir(out):
    os.mkdir(out)

nv = 15 #number of dimension / variable
nprob = 16 #number of problem

list_OF = [calculatorco2,calculatorco2,calculatorco2,calculatorco2,calculatorco2,calculatorco2,calculatorco2,calculatorco2,calculatorco2,calculatorco2,calculatorco2,calculatorco2,calculatorco2,calculatorco2,calculatorco2,calculatorco2]
#modifier in objective function
co2sens = [0,75,200,750,0,75,200,750,0,75,200,750,0,75,200,750] #USD / tonne
gassens = [1.5,1.5,1.5,1.5,2.5,2.5,2.5,2.5,4.0,4.0,4.0,4.0,7.5,7.5,7.5,7.5] #USD / MMBTU

list_args = []
#[10000,10000,10000,10000,10000,0.1,0.1,0.1,0.1,0.1,0,0,0,0,0]

lb = [1000,1000,1000,1000,1000,0,0,0,0,0,0,0,0,0,0]
ub = [20000,20000,20000,20000,20000,30000,30000,30000,30000,30000,600000,600000,600000,600000,600000]
fb = 0.5  
N = 30  # number of particle depend on dimension
w = 0.5
cp = 2.0
cg = 2.0
vs = 0.5 #vmax definition
max_itr = 60


np.random.seed(run)
#initialize first position
init_vars = []
for i in range(nv):
    lhs = pyDOE.lhs(1, samples=(nprob * N))
    lhs = lhs.flatten()
    lhs = lhs.tolist()
    init = []
    for j in range(nprob):
        cntry = []
        for k in range(N):
            for l in range(len(lhs)):
                rand = lhs[l]
                if k / N <= rand < (k + 1) / N:
                    cntry.append(0 if rand * (ub[i] - lb[i]) + lb[i] < 0.001 else rand * (ub[i] - lb[i]) + lb[i]) #prevent eclipse from breaking down for < 0.001
                    lhs.remove(rand)
                    break
        np.random.shuffle(cntry)
        init.append(cntry)
    init_vars.append(init)

#initialize velocity
vmax = vs * (np.array(ub) - np.array(lb))
vmax = vmax.tolist()
init_vels = []
for i in range(nv):
    init = []
    for j in range(nprob):
        cntry = [] #country, 1 population
        for k in range(N):
            rand = np.random.rand()
            cntry.append(- vmax[i] + rand * 2 * vmax[i])
        init.append(cntry)
    init_vels.append(init)

class Indv(object):
    def __init__(self, itr, cid, vels, vars, ofvs, stat, src):
        self.itr = itr
        self.cid = cid
        self.vels = vels
        self.vars = vars
        self.ofvs = ofvs
        self.stat = stat
        self.src = src

# Initialization
wrld = []
for i in range(nprob):
    cntry = [] #initialize the one country
    for j in range(N): #loop for all particle
        itr = 0
        cid = i
        vels = []
        vars = []
        for k in range(nv): #loop for all dimensions
            vels.append(init_vels[k][i][j])
            vars.append(init_vars[k][i][j])
        stat = "init"
        src = -1
        ofv = None
        cntry.append(Indv(itr, cid, vels, vars, ofv, stat, src))
    wrld.append(cntry)

#run heavy function
def runeclipse_wrapper(wrld, i, j):
    #wrld, i, j = args
    return re100(wrld[i][j],j) #world, problem, particle
#eclipse_result =[] 
#for i in range(nprob):
#    for j in range(N):
#        result = runeclipse_wrapper(wrld, i, j)
#        eclipse_result.append(result)
#print(0)
def runeclipse_parallel(wrld):
    # Define the number of processes
    num_processes = 30

    # Create a Pool of processes
    pool = multiprocessing.Pool(processes=num_processes)

    # Create a list of tuples with the arguments for each process
    args_list = [(wrld, i, j) for i in range(nprob) for j in range(N)]
    #print(args_list)
    # Apply the function to each argument tuple in parallel
    heavy_function = [] 
    for i, args in enumerate(args_list):
        # Apply the function to the argument tuple in parallel
        result = pool.apply_async(runeclipse_wrapper, args_list[i] )
        heavy_function.append(result)
        time.sleep(0.2)
    #heavy_function = pool.map(runeclipse_wrapper, args_list)
    #time.sleep(3)
    heavy_function = [result.get() for result in heavy_function]
    #heavy_function = list(heavy_function)
    pool.close()
    pool.join()
    return heavy_function

eclipse_result = runeclipse_parallel(wrld)
os.system("rm -rf /private/hsut/private/opt/egg_2phase_collab/model/EGG_*_0_*")
print("finished heavy function")

mapped_lists = [eclipse_result[i:i+N] for i in range(0, len(eclipse_result), N)]
for i in range(nprob):
    for j in range(N):
        obv_fun = []  
        for k in range(nprob):
            cal = mapped_lists[i][j].npv(0.15,60,gassens[k] ,co2sens[k] )
            obv_fun.append(cal)
            #print(f"calculating npv problem {i} particle {j} objective {k}")
        wrld[i][j].ofvs = obv_fun

pbest = deepcopy(wrld)
gbest = []
for i in range(nprob):
    cntry = wrld[i]
    best = deepcopy(cntry[0])
    for j in range(N):
        indv = deepcopy(cntry[j])
        if indv.ofvs[i] > best.ofvs[i]:
            best = indv
    gbest.append(best)
wrld_hst = deepcopy(wrld)
best_hst = []
for i in range(nprob):
    best = deepcopy(gbest[i])
    best_hst.append([best])
shrng_hst = []
for i in range(nprob):
    shrng_hst.append([])


def update_pbest():
    for i in range(nprob):
        for j in range(N):
            if wrld[i][j].ofvs[i] > pbest[i][j].ofvs[i]:
                pbest[i][j] = deepcopy(wrld[i][j])


def list_cndts(p):
    cndts = [] #list candidates
    for i in range(nprob):
        if i != p:
            cntry = wrld[i]
            for j in range(N):
                indv = cntry[j]
                cndts.append(deepcopy(indv))
    return cndts


def sort(pop, p):
    tuples = []
    for i in range(len(pop)):
        indv = pop[i]
        ofv = indv.ofvs[p]
        tuples.append((indv, ofv))
    sorted_tuples = sorted(tuples, key=lambda item: item[1], reverse=True)
    sorted_pop = []
    for i in range(len(pop)):
        indv = sorted_tuples[i][0]
        sorted_pop.append(deepcopy(indv))
    return sorted_pop


def improve_gbest():
    for i in range(nprob):
        cndts = list_cndts(i)
        sorted_cndts = sort(cndts, i)
        best = sorted_cndts[0]
        if best.ofvs[i] > gbest[i].ofvs[i]:
            gbest[i] = deepcopy(best)


def update_src():
    for i in range(nprob):
        indv = gbest[i]
        if indv.cid != i:
            indv.src = indv.cid


def update_cid():
    for i in range(nprob):
        indv = gbest[i]
        if indv.cid != i:
            indv.cid = i


def record_shrng():
    for i in range(nprob):
        indv = deepcopy(gbest[i])
        if indv.src != -1:
            shrng_hst[i].append([indv])
        else:
            shrng_hst[i].append([])


def reset_src():
    for i in range(nprob):
        indv = gbest[i]
        indv.src = -1


def update_gbest():
    for i in range(nprob):
        cntry = wrld[i]
        best = deepcopy(cntry[0])
        for j in range(N):
            indv = deepcopy(cntry[j])
            if indv.ofvs[i] > best.ofvs[i]:
                best = indv
        if best.ofvs[i] > gbest[i].ofvs[i]:
            gbest[i] = deepcopy(best)
    if coop:
        improve_gbest()
    update_src()
    update_cid()
    record_shrng()
    reset_src()


def update_itr(itr):
    for i in range(nprob):
        cntry = wrld[i]
        for j in range(N):
            indv = cntry[j]
            indv.itr = itr
        print(f"update iteration problem {i} ")


def update_vels():
    for i in range(nprob):
        cntry = wrld[i]
        for j in range(N):
            indv = cntry[j]
            indv.vels = w * np.array(indv.vels)
            r = []
            for k in range(nv):
                r.append(np.random.rand())
            indv.vels = indv.vels + cp * np.array(r) * (np.array(pbest[i][j].vars) - np.array(indv.vars))
            r = []
            for k in range(nv):
                r.append(np.random.rand())
            indv.vels = indv.vels + cg * np.array(r) * (np.array(gbest[i].vars) - np.array(indv.vars))
            indv.vels = indv.vels.tolist()



def ensure_vels_feasibility():
    for i in range(nprob):
        cntry = wrld[i]
        for j in range(N):
            indv = cntry[j]
            for k in range(nv):
                if indv.vels[k] < - vmax[k]:
                    indv.vels[k] = - vmax[k]
                elif indv.vels[k] > vmax[k]:
                    indv.vels[k] = vmax[k]


def update_vars():
    for i in range(nprob):
        cntry = wrld[i]
        for j in range(N):
            indv = cntry[j]
            indv.vars = np.array(indv.vars) + np.array(indv.vels)
            indv.vars = np.where(indv.vars<0.001,0,indv.vars) #avoid eclipse error
            indv.vars = indv.vars.tolist()


def ensure_vars_feasibility():
    for i in range(nprob):
        cntry = wrld[i]
        for j in range(N):
            indv = cntry[j]
            for k in range(nv):
                if indv.vars[k] < lb[k]:
                    indv.vars[k] = lb[k] + fb * abs(indv.vars[k] - lb[k])
                elif indv.vars[k] > ub[k]:
                    indv.vars[k] = ub[k] - fb * abs(indv.vars[k] - ub[k])


def update_stat(stat):
    for i in range(nprob):
        cntry = wrld[i]
        for j in range(N):
            indv = cntry[j]
            indv.stat = stat


def update_ofvs():
    eclipse_result = runeclipse_parallel(wrld)
    os.system(f"rm -rf /private/hsut/private/opt/egg_2phase_collab/model/EGG_*_{wrld[0][0].itr}_*")
    print("finished update heavy function")
    mapped_lists = [eclipse_result[i:i+N] for i in range(0, len(eclipse_result), N)]
    for i in range(nprob):
        for j in range(N):
            obv_fun = []  
            for k in range(nprob):
                cal = mapped_lists[i][j].npv(0.15,60,gassens[k] ,co2sens[k] )
                obv_fun.append(cal)
            wrld[i][j].ofvs = obv_fun


def record_wrld():
    for i in range(nprob):
        cntry = deepcopy(wrld[i])
        wrld_hst[i].extend(cntry)


def record_best():
    for i in range(nprob):
        cntry = wrld[i]
        best = deepcopy(cntry[0])
        for j in range(N):
            indv = deepcopy(cntry[j])
            if indv.ofvs[i] > best.ofvs[i]:
                best = indv
        if gbest[i].ofvs[i] > best.ofvs[i]:
            best = deepcopy(gbest[i])
        best_hst[i].append(best)


def move():
    update_vels()
    ensure_vels_feasibility()
    update_vars()
    ensure_vars_feasibility()
    update_stat("move")
    update_ofvs()
    record_wrld()
    record_best()

def write_log():
    log_input = {}
    log_input["out"] = out
    log_input["coop"] = coop
    log_input["run"] = run
    log_input["nv"] = nv
    log_input["npar"] = nprob
    log_input["list_OF"] = [i.__name__ for i in list_OF]
    log_input["list_args"] = list_args
    log_input["lb"] = lb
    log_input["ub"] = ub
    log_input["fb"] = fb
    log_input["N"] = N
    log_input["w"] = w
    log_input["cp"] = cp
    log_input["cg"] = cg
    log_input["vs"] = vs
    log_input["max_itr"] = max_itr
    file = open(out + "/log_input.json", "w")
    json.dump(log_input, file, indent=4, separators=(",", ": "))
    file.close()

    log_cases = []
    for i in range(len(wrld_hst)):
        line = []
        for j in range(nprob):
            cntry_hst = wrld_hst[j]
            indv = cntry_hst[i] 
            itr = indv.itr
            cid = indv.cid
            vels = indv.vels
            vars = indv.vars
            ofv = indv.ofvs[j]
            stat = indv.stat
            src = indv.src
            line.extend([itr, cid])
            line.extend(vels)
            line.extend(vars)
            line.extend([ofv, stat, src])
        log_cases.append(line)
    pre = "itr,cid"
    for i in range(nv):
        pre = pre + ",vels[" + str(i) + "]"
    for i in range(nv):
        pre = pre + ",vars[" + str(i) + "]"
    post = "stat,src"
    for i in range(nprob):
        if i == 0:
            hdr = pre + ",ofvs[" + str(i) + "]," + post
        else:
            hdr = hdr + "," + pre + ",ofvs[" + str(i) + "]," + post
    file = open(out + "/log_cases.txt", "w")
    file.write(hdr + "\n")
    for line in log_cases:
        for i in range(len(line)):
            if i == 0:
                file.write(str(line[i]))
            else:
                file.write("," + str(line[i]))
        file.write("\n")
    file.close()

    log_optimization = []
    for i in range(len(best_hst[0])):
        line = []
        for j in range(nprob):
            cntry_hst = best_hst[j]
            best = cntry_hst[i]
            itr = i
            cid = best.cid
            vels = best.vels
            vars = best.vars
            ofv = best.ofvs[j]
            stat = best.stat
            src = best.src
            line.extend([itr, cid])
            line.extend(vels)
            line.extend(vars)
            line.extend([ofv, stat, src])
        log_optimization.append(line)
    file = open(out + "/log_optimization.txt", "w")
    file.write(hdr + "\n")
    for line in log_optimization:
        for i in range(len(line)):
            if i == 0:
                file.write(str(line[i]))
            else:
                file.write("," + str(line[i]))
        file.write("\n")
    file.close()


    def generate_sharing_data(shared_pop):
        sharing_data = [0] * nprob
        for i in range(len(shared_pop)):
            indv = shared_pop[i]
            src = indv.src
            sharing_data[src] = sharing_data[src] + 1
        return sharing_data


    log_sharing = []
    for i in range(len(shrng_hst[0])):
        line = []
        for j in range(nprob):
            cntry_hst = shrng_hst[j]
            shared_pop = cntry_hst[i]
            itr = i + 1
            cid = j
            sharing_data = generate_sharing_data(shared_pop)
            totl = len(shared_pop)
            line.extend([itr, cid])
            line.extend(sharing_data)
            line.append(totl)
        log_sharing.append(line)
    pre = "itr,cid"
    for i in range(nprob):
        if i == 0:
            mid = "src=" + str(i)
        else:
            mid = mid + "," + "src=" + str(i)
    post = "totl"
    for i in range(nprob):
        if i == 0:
            hdr = pre + "," + mid + "," + post
        else:
            hdr = hdr + "," + pre + "," + mid + "," + post
    file = open(out + "/log_sharing.txt", "w")
    file.write(hdr + "\n")
    for line in log_sharing:
        for i in range(len(line)):
            if i == 0:
                file.write(str(line[i]))
            else:
                file.write("," + str(line[i]))
        file.write("\n")
    file.close()


# Iterative process
for i in range(max_itr):
    update_pbest()

    update_gbest()

    update_itr(i + 1)
    write_log()
    move()

os.system("rm -rf /private/hsut/private/opt/egg_2phase_collab/model/*")
write_log()
