import numpy as np
import input
import process

class NPV:
    def __init__(self,data,inletpressure,inlettemp,waterdepth,case):
        self.P_tot=process.CalcTopside(data,inletpressure,inlettemp,waterdepth,case).calculation()
        self.OPR=input.ReadInput(data,inletpressure,inlettemp,waterdepth,case).get_input_vector_().FOPR
        self.OPT=input.ReadInput(data,inletpressure,inlettemp,waterdepth,case).get_input_vector_().FOPT
        self.GPR=input.ReadInput(data,inletpressure,inlettemp,waterdepth,case).get_input_vector_().FGPR
        self.GPT=input.ReadInput(data,inletpressure,inlettemp,waterdepth,case).get_input_vector_().FGPT
        self.WPR=input.ReadInput(data,inletpressure,inlettemp,waterdepth,case).get_input_vector_().FWPR
        self.WPT=input.ReadInput(data,inletpressure,inlettemp,waterdepth,case).get_input_vector_().FWPT
        self.GIR=input.ReadInput(data,inletpressure,inlettemp,waterdepth,case).get_input_vector_().FGIR
        self.GIT=input.ReadInput(data,inletpressure,inlettemp,waterdepth,case).get_input_vector_().FGIT
        self.WIR=input.ReadInput(data,inletpressure,inlettemp,waterdepth,case).get_input_vector_().FWIR
        self.WIT=input.ReadInput(data,inletpressure,inlettemp,waterdepth,case).get_input_vector_().FWIT
        self.TSTEP=input.ReadInput(data,inletpressure,inlettemp,waterdepth,case).get_input_vector_().TIME
        self.FPR=input.ReadInput(data,inletpressure,inlettemp,waterdepth,case).get_input_vector_().FPR
        result = np.vstack((self.TSTEP, self.OPR, self.WPR, self.GPR, self.GIR, self.WIR, self.P_tot,self.OPT,self.GPT,self.WPT,self.GIT,self.WIT,self.FPR))
        self.case=case #case name
        np.savetxt(f'result_{self.case}.txt',result,delimiter=',')

    def co2tax(self):
        #CO2 mass
        Se=15.4 #kWh/kg fuel
        SCO2=2.75 #kg co2/kg fuel
        eta_turbin=0.2
        base_load = 10 #MW
        total_power_with_base = self.P_tot+base_load
        m_fuel=(total_power_with_base)*1e3/(eta_turbin*Se)
        mco2=SCO2*m_fuel #kg
        return mco2, total_power_with_base

    def cf(self, oil_price, gas_price,co2_price):
        oil_rev=self.OPR*oil_price*6.289814*1e-6 #MMUSD
        gas_rev=(self.GPR-self.GIR)*0.037913*gas_price*1e-6 #MMUSD
        co2_mass, total_power_used=NPV.co2tax(self)
        co2_tax=-co2_mass*co2_price*1e-3*1e-6 #MMUSD #77 usd per tonne
        liquid_handling = (self.OPR+self.WPR) * -0.01 * 6.289814*1e-6 # 1 usd per bbl liquid handling MMUSD
        cashflow=oil_rev+gas_rev+co2_tax+liquid_handling
        ccf=np.zeros(len(cashflow))
        ccf[1:]=np.cumsum(cashflow[1:]*(self.TSTEP[1:]-self.TSTEP[:-1]))
        return cashflow

    def npv(self,discount,oil_price,gas_price,co2_price):
        #oil_price=60 #usd/bbl
        #gas_price = 2.84 #usd/btu
        #co2_price = 77 #usd/kg
        co2_mass, total_power_used=NPV.co2tax(self)
        cashflow=NPV.cf(self, oil_price, gas_price,co2_price)
        dcf=(1 + discount)**(1/365)-1  #yearly discount % per year
        discounted_cashflow=cashflow/((1+dcf)**self.TSTEP)
        npv = np.zeros(len(cashflow))
        npv[1:]=np.cumsum(discounted_cashflow[1:]*(self.TSTEP[1:]-self.TSTEP[:-1])) 
        co2_cum = np.zeros(len(npv))
        power_cum = np.zeros(len(npv))
        co2_cum[1:]=np.cumsum(co2_mass[1:]*(self.TSTEP[1:]-self.TSTEP[:-1]))
        power_cum[1:]=np.cumsum(total_power_used[1:]*(self.TSTEP[1:]-self.TSTEP[:-1]))
        co2_npv = np.vstack((co2_mass,npv, co2_cum, power_cum))
        np.savetxt(f"npv_co2_{self.case}.txt",co2_npv,delimiter=',')
        return npv[-1]
        #return npv.max()