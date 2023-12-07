import math
import numpy as np


class pump:
    def __init__(self,rate,freq):
        self.q=rate #m3/s
        self.w=freq #RPM
    def head(self):
        a0=1.823*10**3
        a1=-5.641*10
        a2=6.409*10
        a3=2.061*10**2
        a4=1.712*10**2
        a5=-1.868*10**2
        q_bar=1.593*10**-1
        omega_q=7.068*10**2
        omega_2=1.942*10**7
        omega_3=8.672*10**10
        q_3=7.922*10**-3
        sigma_q=8.964*10**-2
        sigma_omega_q=4.196*10**2
        sigma_omega_2=3.681*10**6
        sigma_omega_3=2.407*10**10
        sigma_q_3=9.304*10**-3
        head=a0+(a1*((self.q-q_bar)/sigma_q))+(a2*((self.w*self.q-omega_q)/sigma_omega_q))+(a3*((self.w**2-omega_2)/sigma_omega_2))+(a4*((self.w**3-omega_3)/sigma_omega_3))+(a5*((self.q**3-q_3)/sigma_q_3))
        head=np.where(head<0,0,head)
        return head
    def efficiency(self):
        b0=1*10**-10
        b1=9.641
        b2=-3.812*10
        b3=5.741*10**-3
        b4=-1.629*10**-7
        efficiency=b0+b1*self.q+b2*self.q**2+b3*self.w*self.q**2+b4*self.q*self.w**2
        efficiency=np.where(efficiency<0.1, 0.1, efficiency)
        efficiency=np.where(efficiency>1, 1, efficiency)
        return efficiency
    def pump_power(self):
        h=self.head()
        e=self.efficiency()
        power= self.q*1000*9.81*h/(0.85*e)/1000000 #megawatt
        #power= np.where(power<0,np.nan,power)
        return power
