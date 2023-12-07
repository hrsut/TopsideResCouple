import numpy as np
import math

class compressor:
    def __init__(self,mass,freq):
        self.m=mass/2.5 #corrected mass flow rate (correlation range from 0.02 to 0.133 kg/s)
        self.freq=freq*1.2 #rpm #normalized corrected rpm (maximum 14000 rpm, range from 0.42 to 1)


    def pr(self):
        g0=1.0450851654150264
        g1=241.64148855294323
        g2=-1085.5539911660774
        g3=186.78063215738922
        g4=-18.851414930402566
        g5=0.5803839900163186
        ratio=g0+g1*self.freq*self.m+g2*self.m**2+g3*self.freq*self.m**2+g4*self.freq**2+g5*((self.freq**3)/self.m)
        ratio = np.where(ratio < 1, 1, ratio)
        ratio = np.where(ratio > 5, 5, ratio)
        return ratio
    def efficiency(self):
        f0=8.059894398447188
        f1=5.011282026215329
        f2=-0.15484073546802357
        f3=4.270025962501383e-09
        f4=-14.344509471466102
        f5=-0.7023340383687516
        f6=2.9184319006777293
        f7=-51.640302738581724
        f8=-0.02334534516666194
        eta=f0*self.freq+f1*self.freq**2+f2*self.freq**3+f3*((self.freq**f4)/self.m)+f5*((self.freq**f6)/self.m)+f7*(self.freq**f8)*self.m
        eta = np.where(eta < 0.5, np.nan, eta)
        eta = np.where(eta > 1, 1, eta)
        return eta
