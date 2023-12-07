import numpy as np
import math


# z factor calculator from New explicit correlation for the compressibility factor of natural gas: linearized z-factor isotherms
# DOI 10.1007/s13202-015-0209-3

# Gas heat capacity from as function of specific gravity, pressure, and temperature
# http://dx.doi.org/10.1016/j.jngse.2014.04.011
# SG from 0.55-1, temperature 100-1500 K

# input in bar and celcius
class gas_properties:
    # input in bar and celcius
    def __init__(self, pressure, temperature, sg):
        self.p = pressure * 14.5038  # psig
        self.t = (temperature * 9 / 5) + 459.67  # Rankine
        self.sg = sg

        self.Tpc = 169.2 + 349.5 * self.sg - 74 * self.sg ** 2
        self.Ppc = 756.8 - 131.07 * self.sg - 3.6 * self.sg ** 2
        self.Tpr = self.t / self.Tpc
        self.Ppr = self.p / self.Ppc

    def z(self):
        Tpr = self.Tpr
        Ppr = self.Ppr
        a1 = 0.317842
        a2 = 0.382216
        a3 = -7.768354
        a4 = 14.290531
        a5 = 0.000002
        a6 = -0.004693
        a7 = 0.096254
        a8 = 0.166720
        a9 = 0.966910
        a10 = 0.063069
        a11 = -1.966847
        a12 = 21.0581
        a13 = -27.0246
        a14 = 16.23
        a15 = 207.783
        a16 = -488.161
        a17 = 176.29
        a18 = 1.88453
        a19 = 3.05921
        # correlation uses equation nr. 14
        t = 1 / Tpr
        A = a1 * t * Ppr * (math.exp(a2 * (1 - t) ** 2))
        B = a3 * t + a4 * (t ** 2) + a5 * (Ppr ** 6) * (t ** 6)
        C = a9 + a8 * t * Ppr + a7 * (t ** 2) * (Ppr ** 2) + a6 * (t ** 3) * (Ppr ** 3)
        D = a10 * t * (math.exp(a11 * (1 - t) ** 2))
        E = a12 * t + a13 * (t ** 2) + a14 * (t ** 3)
        F = a15 * t + a16 * (t ** 2) + a17 * (t ** 3)
        G = a18 + a19 * t
        y = (D * Ppr) / (((1 + A ** 2) / C) - ((B * A ** 2) / C ** 3))
        z = (D * Ppr * (1 + y + (y ** 2) - (y ** 3))) / (D * Ppr + E * (y ** 2) - (F * (y ** G)) * (1 - y) ** 3)
        return z

    def gas_dens(self):
        z = self.z()
        dens = 28.97 * 0.001 * 100000 * self.sg * (self.p / 14.5038) / (
                    z * 8.314 * (((self.t - 491.67) * (5 / 9)) + 273.15))  # kg/m3
        return dens  # kg/m3

    def cp_ideal(self):
        # SG from 0.55-1, temperature 100-1500 K
        a1 = -10.9602
        a2 = 25.9033
        b1 = 2.1517 * 10 ** -1
        b2 = -6.8687 * 10 ** -2
        c1 = -1.3337 * 10 ** -4
        c2 = 8.6387 * 10 ** -5
        d1 = 3.1474 * 10 ** -8
        d2 = -2.8396 * 10 ** -8
        Tpr = self.Tpr
        Ppr = self.Ppr
        t = 1 / Tpr
        T_Kelvin = self.t * 5 / 9
        cp_ideal = (a1 * self.sg + a2) + ((b1 * self.sg + b2) * T_Kelvin) + ((c1 * self.sg + c2) * T_Kelvin ** 2) + (
                    (d1 * self.sg + d2) * T_Kelvin ** 3)
        return cp_ideal

    def cp_residual(self):
        # Tpr 1.2-3, Ppr 0.01-15
        a1 = 4.80828
        a2 = -4.01563
        a3 = -0.0700681
        a4 = 0.0567
        a5 = 2.36642
        a6 = -3.82421
        a7 = 7.71784
        Tpr = self.Tpr
        Ppr = self.Ppr
        t = 1 / Tpr
        cp_residual = 8.314 * ( ((1 + (a1 * math.exp(a2*(1-t)**2) * Ppr * t )**2 ) / (a7 + a6*(Ppr*t) + (a5*(Ppr*t)**2) + (a4*(Ppr*t)**3))) - ((((a1*(math.exp(a2*(1-t)**2)))**2) * (a3*((Ppr*t)**6)))/((a7 + a6*(Ppr*t) + (a5*(Ppr*t)**2) + (a4*(Ppr*t)**3))**3) ) )
        return cp_residual

    def cp(self):
        cpi = self.cp_ideal()
        cpr = self.cp_residual()
        cp_real = cpi + cpr
        return cp_real  # kJ/kmol K or joule/mol K

    def k(self):
        cp = self.cp()
        k = cp*1000 / (cp*1000-8134)
        return k