from Compressor_opt import compressor
import numpy as np
from scipy.optimize import minimize
import math

class opt_comp:
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
        circulation = 0
        if self.f==1:
            omega=np.array([1])
            p=np.zeros((len(omega),9))
            for j in range(len(omega)):
                mass=self.m/self.t
                pr_calc=np.where((compressor(mass,omega[j]).pr())**self.s<self.pr,np.nan,(compressor(mass,omega[j]).pr()))
                eff_calc=compressor(mass,omega[j]).efficiency()
                p[j]=self.s*self.t*mass*pr_calc/eff_calc
        
            #find index
            result = np.where(p == np.nanmin(p))
            #print(result[0].size)
            count=0
            m_cir=self.m
            if result[0].size==0:
                while result[0].size==0:
                    m_upper = m_cir + 0.48
                    while m_upper- m_cir > 0.01:
                        m_mid = (m_cir + m_upper) / 2
                        for j in range(len(omega)):
                            mass=m_mid/self.t
                            pr_calc=np.where((compressor(mass,omega[j]).pr())**self.s<self.pr,np.nan,(compressor(mass,omega[j]).pr()))
                            eff_calc=compressor(mass,omega[j]).efficiency()
                            p[j]=self.s*self.t*mass*pr_calc/eff_calc
                        result = np.where(p == np.nanmin(p))
            listOfCordinates = list(zip(result[0], result[1]))
            if len(listOfCordinates)==0:
                f_opt=np.nan
                s_opt=np.nan
                t_opt=np.nan
            else:
                index=listOfCordinates[0]
                omega_opt=omega[index[0]]
                s_opt=self.s[index[1]]
                t_opt=self.t[index[1]]
        else:
            m_cir=self.m
            result=np.zeros((9,4))
            count=0
            #run for each combination train and stage
            for stage in [1,2,3]:
                for train in [1,2,3]:
                    #power function
                    def power(omega):
                        mass=self.m/train
                        pr_calc=np.where((compressor(mass,omega).pr())**stage<self.pr,np.nan,(compressor(mass,omega).pr()))
                        eff_calc=compressor(mass,omega).efficiency()
                        if eff_calc == 0.5:
                            eff_calc = np.nan
                        #print(eff_calc,pr_calc)
                        return stage*train*mass*pr_calc/eff_calc
                    res = minimize(power, 0.9, method='Nelder-Mead', tol=1, bounds = [(0.5, 1.0)])
                    result[count,0]=stage
                    result[count,1]=train
                    result[count,2]=res.x
                    result[count,3]=res.fun
                    count=count+1
            
            nan_rows = np.isnan(result).any(axis=1)

            # Use boolean indexing to drop rows with NaN values
            result = result[~nan_rows]
            if len(result) == 0:
                circulation = 1
                m_cir=self.m
                #if c>1000 or math.isnan(c):
                result=np.zeros((9,4))
                count = 0
                temp_results = np.empty((0, 5))
                for stage in [1,2,3]:
                    for train in [1,2,3]:
                        m_upper = 1.59
                        m_cir = self.m #reset mass
                        while m_upper - m_cir > 0.08:
                            m_mid = (m_cir + m_upper) / 2
                            def power(omega):
                                mass=m_mid/train
                                pr_calc=np.where((compressor(mass,omega).pr())**stage<self.pr,1e3,(compressor(mass,omega).pr()))
                                eff_calc=compressor(mass,omega).efficiency()
                                #print(eff_calc,pr_calc)
                                return stage*train*mass*pr_calc/eff_calc
                            res = minimize(power, 0.9, method='Nelder-Mead', tol=1)

                            if res.fun>1000 or math.isnan(res.fun):
                                row = np.array([stage, train, res.x[0] , res.fun ,m_mid])
                                temp_results = np.vstack((temp_results, row))
                                m_cir = (m_cir + m_mid) /2 
                            else:
                                row = np.array([stage, train, res.x[0] , res.fun ,m_mid])
                                temp_results = np.vstack((temp_results, row))
                                m_upper = (m_mid+m_upper)/2
                        
                        #result[count,0]=iter_result[0] 
                        #result[count,1]=iter_result[1]
                        #result[count,2]=iter_result[2]
                        #result[count,3]=iter_result[3]
                        count = count +1
                        
                result = temp_results[np.where(temp_results==temp_results[:,3].min())[0]]
                    #check=result[np.where(result==result[:,3].min())[0]]
                    #c_cir+=1
                    #print(m_cir,c_cir)
                    #if c_cir>100:
                    #    break          

            
                
            conf=result[np.where(result==result[:,3].min())[0]][0]
            #print(conf[0],conf[1],conf[2])
            omega_opt=conf[2]
            s_opt=conf[0]
            t_opt=conf[1]
            if circulation == 1:
                m_cir = conf[-1]
            else:
                m_cir = self.m 
        return s_opt,t_opt,omega_opt,m_cir