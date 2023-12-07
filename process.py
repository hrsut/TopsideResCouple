import numpy as np
from Pump import pump
from Compressor import compressor
from Gas_Properties import gas_properties
from optimizer_compressor import opt_comp
from optimizer_pump import opt_pump
import input
import time

class CalcTopside:
    def __init__(self,data,inletpressure, inlettemp, waterdepth,case):
        self.m_tot, self.m_corr_tot, self.pr_d, self.q, self.h, self.mscale, self.prscale, self.TSTEP=input.ReadInput(data,inletpressure,inlettemp,waterdepth,case).conf_input(200)
        self.inletpressure=inletpressure #bar
        self.inlettemp= inlettemp # degC
        self.case=case #case name
            
    def conf_comp(self,single):
        start_time = time.time()
        if single==1:
            a=1
        else:
            a=single
        s,t,f,m_cir=np.zeros(len(self.m_tot)),np.zeros(len(self.m_tot)),np.zeros(len(self.m_tot)),np.zeros(len(self.m_tot))
        m=self.m_corr_tot/self.mscale
        pr=self.pr_d/self.prscale
        for i in range (len(m)):
            if m[i]==0:
                s[i],t[i],f[i]=0,0,0
            else:
                s[i],t[i],f[i],m_cir[i]=opt_comp(m[i],pr[i],a).optimizer()
            #print(s[i],t[i],f[i])
        print("Optimizer finished in %s seconds" % (time.time() - start_time))
        circulated = m_cir - m
        return t,s,f,circulated
    
    def conf_pump(self,single):
        start_time = time.time()
        if single==1:
            a=1
        else:
            a=single
        s,t,f=np.zeros(len(self.q)),np.zeros(len(self.q)),np.zeros(len(self.q))
        for i in range (len(self.q)):
            if self.q[i]==0:
                s[i],t[i],f[i]=0,0,0
            else:
                s[i],t[i],f[i]=opt_pump(self.q[i],self.h[i],a).optimizer()
            #print(s[i],t[i],f[i])
        #print("Optimizer finished in %s seconds" % (time.time() - start_time))
        return t,s,f

    def p_pump(self):
        head = pump(self.q / self.t_pump, self.w_pump).head()
        eff = pump(self.q / self.t_pump, self.w_pump).efficiency()
        pump_power=self.t_pump*self.s_pump*(self.q*1000*9.81*head/(0.85*eff))/1000000 #megawatt
        return pump_power
    
    def p_comp(self):
        pr_compressor=np.zeros((self.s_comp.astype(int).max(),len(self.t_comp)))
        eff=np.zeros((self.s_comp.astype(int).max(),len(self.t_comp)))
        p=np.zeros((self.s_comp.astype(int).max()+1,len(self.t_comp)))
        comp_power=np.zeros((self.s_comp.astype(int).max(),len(self.t_comp)))
        m_c_real=self.m_cir/((101.325/(self.inletpressure*100))*np.sqrt((self.inlettemp+273.15)/293))
        p[0][:]=self.inletpressure
        for i in range(len(self.t_comp)):
            for j in range(self.s_comp.astype(int)[i]):
                if self.t_comp[i] != 0 or self.t_comp[i] == np.nan() :
                    k=gas_properties(p[j][i],self.inlettemp,0.5).k()
                    z=gas_properties(p[j][i],self.inlettemp,0.5).z()
                    pr_compressor[j][i]=compressor(((self.m_corr_tot[i]/self.mscale)+self.m_cir[i])/self.t_comp[i],self.w_comp[i]).pr()
                    eff[j][i]=compressor(((self.m_corr_tot[i]/self.mscale)+self.m_cir[i])/self.t_comp[i],self.w_comp[i]).efficiency()
                    comp_power[j][i]=75*4*(self.t_comp[i]*(k/(k-1))*(self.m_tot[i]+(m_c_real[i]/self.t_comp[i]))*8.314*(self.inlettemp+273.15)*z*(((pr_compressor[j][i])**((k-1)/k))-1)/eff[j][i])/1e6
                    p[j+1][i]=p[j][i]*pr_compressor[j][i]
                else:
                    comp_power[j][i]=0
        mask = np.isnan(eff)
        eff[mask] = np.interp(np.flatnonzero(mask), np.flatnonzero(~mask), eff[~mask])
        comp_power[mask] = np.interp(np.flatnonzero(mask), np.flatnonzero(~mask), comp_power[~mask])
        return np.sum(comp_power,axis=0)
    
    def timestep(self, tstep, *timeseries):
        bin=np.arange(0,self.TSTEP.max(),tstep)
        index_time=np.digitize(self.TSTEP,bin)-1
        
        x=np.zeros((len(timeseries),len(self.TSTEP)))
        count=0
        for array in timeseries:
            y=np.zeros(len(self.TSTEP))
            for i in np.unique(index_time):
                z=np.where(index_time==i)
                if len(z[0])==1:
                    y[z[0][0]]=array[z[0][0]]
                else:
                    y[z[0][0]:z[0][-1]+1]=np.max(array[z[0][0]:z[0][-1]])
            y[0]=array[0]
            x[count]=y
            #print(count)
            count=count+1
        return x
    
   
    def calculation(self):
        self.t_pump, self.s_pump, self.w_pump = CalcTopside.conf_pump(self,0.83)
        self.t_pump, self.s_pump, self.w_pump = CalcTopside.timestep(self, 30, self.t_pump, self.s_pump, self.w_pump)
        self.t_comp, self.s_comp, self.w_comp, self.m_cir = CalcTopside.conf_comp(self,0.5)
        self.t_comp, self.s_comp, self.w_comp = CalcTopside.timestep(self, 30, self.t_comp, self.s_comp, self.w_comp)
        self.Pp = CalcTopside.p_pump(self)
        #self.m_cir = CalcTopside.mc(self)
        self.Pc = CalcTopside.p_comp(self)
        result = np.vstack((self.t_pump, self.s_pump, self.w_pump, self.t_comp, self.s_comp, self.w_comp, self.Pp, self.m_cir, self.Pc))
        np.savetxt(f"process_{self.case}.txt",result,delimiter=",")
        P_total = self.Pp + self.Pc
        return np.nan_to_num(P_total)