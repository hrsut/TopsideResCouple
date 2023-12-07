from Pump import pump
import numpy as np
from scipy.optimize import minimize

class opt_pump:
    def __init__(self,m,pr,speed):
        self.m=m #corrected mass flow rate
        self.pr=pr #corrected pressure ratio
        self.f=speed #rot speed

        def cartesian(*arrays):
            mesh = np.meshgrid(*arrays)  # standard numpy meshgrid
            dim = len(mesh)  # number of dimensions
            elements = mesh[0].size  # number of elements, any index will do
            flat = np.concatenate(mesh).ravel()  # flatten the whole meshgrid
            reshape = np.reshape(flat, (dim, elements)).T  # reshape and transpose
            return reshape

        configuration=cartesian([1,2,3],[1,2,3]) #stages,trains
        self.s=configuration[:,0]
        self.t=configuration[:,1]

    def optimizer(self):
        if self.f==1:
            omega=np.array([1*4674])
            p=np.zeros((len(omega),9))
            for j in range(len(omega)):
                mass=self.m/self.t
                head_calc=np.where((pump(mass,omega[j]).head())*self.s<self.pr,100000,(pump(mass,omega[j]).head()))
                eff_calc=pump(mass,omega[j]).efficiency()
                p[j]=self.s*self.t*mass*head_calc/eff_calc
        
            #find index
            result = np.where(p == np.nanmin(p))
            listOfCordinates = list(zip(result[0], result[1]))
            index=listOfCordinates[0]
            omega_opt=omega[index[0]]
            s_opt=self.s[index[1]]
            t_opt=self.t[index[1]]
        else:
            result=np.zeros((9,4))
            count=0
            #run for each combination train and stage
            for stage in [1,2,3]:
                for train in [1,2,3]:
                    #power function
                    def power(omega):
                        mass=self.m/train
                        w=omega*4674
                        head_calc=np.where((pump(mass,w).head())*stage<self.pr,100000,(pump(mass,w).head()))
                        if w>1*4674:
                            eff_calc=1e-6
                        elif w<self.f*4674:
                            eff_calc=1e-6
                        else:
                            eff_calc=pump(mass,w).efficiency()
                        #print(eff_calc,pr_calc)
                        return stage*train*mass*head_calc/eff_calc
                    res = minimize(power, 1, method='Nelder-Mead', tol=1)
                    result[count,0]=stage
                    result[count,1]=train
                    result[count,2]=res.x
                    result[count,3]=res.fun
                    count=count+1
            conf=result[np.where(result==result[:,3].min())[0]][0]
            #print(conf[0],conf[1],conf[2])
            omega_opt=conf[2]*4674
            s_opt=conf[0]
            t_opt=conf[1]
        return s_opt,t_opt,omega_opt