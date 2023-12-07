import numpy as np
from ecl.summary import EclSum
from Gas_Properties import gas_properties

class ReadInput:
    def __init__(self, data,inletpressure,inlettemp,waterdepth,case):
        self.data=data
        self.inletpressure=inletpressure #bar
        self.inlettemp= inlettemp # degC
        self.waterdepth=waterdepth
        self.case=case #case name
        
    def get_input_vector_(self):
        summary_ECL = EclSum(self.data)
        self.ILIST = summary_ECL.wells()
        self.injector=['I1','I2','I3','I4','I5','I6','I7','I8']
        self.ILIST_WI=['I1','I2','I3','I5','I6','I7','I8']
        list_summary_ECL = []
        list_summary_ECL.append(summary_ECL)

        self.TIME = summary_ECL.numpy_vector("TIME")   # unit: days
        self.FOPR = summary_ECL.numpy_vector("FOPR")   # FOPR_[time], unit: sm3/d
        self.FOPT = summary_ECL.numpy_vector("FOPT")  # FOPT_[time], unit: sm3
        self.FWPR = summary_ECL.numpy_vector("FWPR")   # FWPR_[time], unit: sm3/d
        self.FWPT = summary_ECL.numpy_vector("FWPT")  # FWPT_[time], unit: sm3
        self.FGPR = summary_ECL.numpy_vector("FGPR")  # FGPR_[time], unit: sm3/d
        self.FGPT = summary_ECL.numpy_vector("FGPT")  # FGPT_[time], unit: sm3
        self.FWIR = summary_ECL.numpy_vector("FWIR")  # FWIR_[time], unit: sm3/d
        self.FWIT = summary_ECL.numpy_vector("FWIT")   # FWIT_[time], unit: sm3
        self.FGIR = summary_ECL.numpy_vector("FGIR")  # FWIR_[time], unit: sm3/d
        self.FGIT = summary_ECL.numpy_vector("FGIT")   # FWIT_[time], unit: sm3
        self.FPR  = summary_ECL.numpy_vector("FPR")   # FWIT_[time], unit: sm3
        self.WWIR = []
        self.WGIR = []
        self.IBHP = []

        for iname in self.ILIST:
            temp = summary_ECL.numpy_vector("WBHP:" + iname)
            temp = temp.tolist()
            self.IBHP.append(temp)
        for iname in self.injector:
            temp_1 = summary_ECL.numpy_vector("WWIR:" + iname)
            temp_2 = summary_ECL.numpy_vector("WGIR:" + iname)
            temp_1 = temp_1.tolist()
            temp_2 = temp_2.tolist()
            self.WWIR.append(temp_1)
            self.WGIR.append(temp_2)
        self.IBHP = np.array(self.IBHP)                  # IBHP_[iname,time], unit: barsa
        self.WWIR = np.array(self.WWIR)                  # unit: sm3/d
        self.WGIR = np.array(self.WGIR)                  # unit: sm3/d
        #print("Read ECL results of %s", self.data)
        return self
    
    def calc_inj(self):
        inj_idx = [self.ILIST.index(x) for x in self.injector]
        IBHP_inj=self.IBHP.take(inj_idx,axis=0)
        self.IBHP_inj_WI=np.zeros(IBHP_inj.shape)
        self.IBHP_inj_WI[np.where(self.WWIR>0)[0],np.where(self.WWIR>0)[1]]=IBHP_inj[np.where(self.WWIR>0)[0],np.where(self.WWIR>0)[1]]
        self.IBHP_inj_GI=np.zeros(IBHP_inj.shape)
        self.IBHP_inj_GI[np.where(self.WGIR>0)[0],np.where(self.WGIR>0)[1]]=IBHP_inj[np.where(self.WGIR>0)[0],np.where(self.WGIR>0)[1]]
        return self

    def inputcalc(self,arraypressure,arrayrate,machinetype):
        pressure_max=np.max(arraypressure, axis=0)
        required_head, required_rate , required_pr, massflow, correctedmass = [],[],[],[],[]
        if machinetype==0: #is pump
            required_pressure=pressure_max-(self.waterdepth*9.81*1000*1e-5)
            p_atm=1
            required_head=np.where(((required_pressure-p_atm)*1e5/(1000*9.81))<0,0,((required_pressure-p_atm)*1e5/(1000*9.81)))
            required_rate=arrayrate/(24*3600) #m3/s
            return required_head,required_rate,pressure_max
        else:
            required_pressure=pressure_max-((self.waterdepth)*9.81*gas_properties(pressure_max,self.inlettemp,0.5).gas_dens()*1e-5)
            required_pressure=np.where(required_pressure<0,0,required_pressure)
            required_pr=np.nan_to_num(required_pressure/self.inletpressure)
            massflow=(arrayrate/gas_properties(self.inletpressure,self.inlettemp,0.5).gas_dens())/(24*3600) #kg/s
            correctedmass=massflow*(101.325/(self.inletpressure*100))*np.sqrt((self.inlettemp+273.15)/293)
            return required_pr, massflow, correctedmass,pressure_max
    
    def inputcalc_prod(self,p_line,arrayrate,machinetype):
        required_head, required_rate , required_pr, massflow, correctedmass = [],[],[],[],[]
        if machinetype==0: #is pump
            required_pressure=p_line
            p_atm=1
            required_head=np.where(((required_pressure-p_atm)*1e5/(1000*9.81))<0,0,((required_pressure-p_atm)*1e5/(1000*9.81)))
            required_rate=arrayrate/(24*3600) #m3/s
            return required_head,required_rate
        else:
            required_pressure=p_line
            required_pr=np.nan_to_num(required_pressure/self.inletpressure)
            massflow=(arrayrate/gas_properties(self.inletpressure,self.inlettemp,0.5).gas_dens())/(24*3600) #kg/s
            correctedmass=massflow*(101.325/(self.inletpressure*100))*np.sqrt((self.inlettemp+273.15)/293)
            return required_pr, massflow, correctedmass

    def conf_input(self,output_pressure):
        #injection
        ReadInput.get_input_vector_(self)
        ReadInput.calc_inj(self)
        self.pr,self.m,self.m_corr,self.discharge_GI=ReadInput.inputcalc(self,self.IBHP_inj_GI,self.FGIR,1)
        h,q,self.discharge_WI=ReadInput.inputcalc(self,self.IBHP_inj_WI,self.FWIR,0)
        
        #gasprod
        p_line=np.ones(len(self.TIME))*output_pressure
        self.pr_prod,self.m_prod,self.m_prod_corr,self.discharge_GP=ReadInput.inputcalc(self,p_line,self.FGPR,1)

        #combine injection production line
        m_tot=self.m+self.m_prod
        m_corr_tot=self.m_corr+self.m_prod_corr
        self.pr=np.where(self.m_corr==0,0,self.pr)
        pr_d=np.maximum(self.pr,self.pr_prod)

        #scalingsize
        #scale_mcorr=70 #change mcorr from 75 initially for correct sizing for two phase model
        #scale_pr=4
        scale_mcorr=m_corr_tot.max()/(1.4*0.8)
        scale_pr=pr_d.max()/(50*0.8)
        #print('scaling mass',scale_mcorr)
        #print('scaling pr',scale_pr)
        return m_tot, m_corr_tot, pr_d, q, h, scale_mcorr, scale_pr, self.TIME