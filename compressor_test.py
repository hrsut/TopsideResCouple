import numpy as np
from Pump import pump
from Compressor import compressor
from Gas_Properties import gas_properties
from optimizer_compressor import opt_comp
from optimizer_pump import opt_pump
import input
import time
from process import CalcTopside


calc_topside = CalcTopside(None,None,None,None,None)
calc_topside.m_corr_tot = np.array([ 0.        ,  2.55134891,  3.42592989,  4.32327167,  5.47154975,
        7.1535258 , 10.02686313, 11.22603876, 11.78138581, 12.82072889,
       13.45341542, 14.01647555, 14.46662565, 14.95514039, 15.39037217,
       16.28980407, 17.33397893, 18.01766456, 18.32179356, 18.66687575,
       19.3781078 , 19.9360454 , 20.36760883, 20.54576914, 20.59259885,
       20.68394812, 20.63409293, 20.71699744, 20.58032803, 20.70846347,
       20.54757822, 20.98524202, 20.64753634, 21.62910245, 20.53042982,
       22.56208394, 19.71355751, 22.90254346, 19.46240796, 24.86675507,
       19.09689378, 22.91075481, 19.56078323, 22.36421496, 19.96314333,
       22.43752842, 20.0308081 , 22.89254295, 19.68612102, 23.45157747,
       19.24935897, 23.46882465, 19.06119895, 23.49487425, 18.96756424,
       23.57012504, 18.88869052, 23.69039725, 18.79913519, 23.82386911,
       18.68924905, 23.88432864, 18.71031513, 23.38297271, 19.04643079,
       22.96118515, 19.46881421, 22.79320459, 19.80364098, 22.90001984,
       19.9245417 , 23.27379395, 19.74665144, 23.87027423, 19.32575368,
       24.22757705, 18.97906873, 24.41215477, 18.94732662, 23.30536718,
       19.51975995, 22.77172826, 20.06279954, 22.73468558, 20.3392929 ,
       23.05646006, 20.22492111, 23.77779219, 19.67885603, 24.12265532,
       19.06250776, 24.42985282, 18.88055006, 24.29560109, 18.92759087,
       23.91716686, 19.2470568 , 23.40066997, 19.72357076, 23.10681233,
       20.14068787, 23.11311502, 20.32685719, 23.39869042, 20.20482051,
       23.97060356, 19.45484026, 24.36920211, 19.37231254, 24.01701505,
       19.59503543, 23.51563842, 20.00474893, 23.23306142, 20.35226633,
       23.22523802, 20.48280033, 23.48177417, 20.32610679, 24.17389022,
       19.84475348, 24.33345072, 19.55811303, 24.35545838, 19.44133073,
       24.041297  , 19.63586753, 23.57764335, 20.04422363, 23.26818828,
       20.4175158 , 23.20562653, 20.60146261, 23.46528695, 20.47857517,
       23.50672367, 20.45732428, 23.72728379, 20.24482813, 24.10060783,
       19.87425316, 24.50135879, 19.18288433, 24.66401727, 19.44248261,
       22.85424164, 20.48363039, 22.33503074, 21.14899423, 22.42453269,
       21.38397758, 22.76223837, 21.12417776, 23.33122321, 20.48532714,
       24.14263085, 19.6181416 , 24.87202936, 18.5715634 , 24.59741119,
       18.12485103, 22.14463944, 20.00671972, 21.46463091, 20.92402732,
       21.65370463, 21.26139763, 21.74443972, 21.21222512, 21.60170101,
       20.97562706, 21.3279838 , 20.68566877, 21.05150477, 20.5522463 ,
       20.6523478 , 20.38401003, 20.66578325, 20.50987994, 20.81691653,
       20.80637991, 21.14380359, 21.10269825, 21.32576686, 21.3813958 ,
       21.62901323, 21.75369462, 22.11087317, 22.4202207 , 22.86025756,
       22.95143158, 23.10423373, 23.420248  , 23.80733808, 24.20793131,
       24.41902703, 24.61269315, 24.92427912, 25.40264996, 25.81137807,
       26.23658385, 26.65660933, 26.95808008, 27.29935134, 27.77960534,
       28.46295241, 29.13710275, 30.02318763, 30.55159289, 30.97622033,
       31.51746678, 31.61743047, 31.70397943, 31.7148578 , 31.80417574,
       31.79670682, 31.93049095, 31.88926851, 31.83730313, 31.67546435,
       31.59286175, 31.41619984, 31.32856273, 31.18482269, 31.09996731,
       30.95351405, 30.86013824, 30.74257287, 30.67893731, 30.57237617,
       30.46049375, 30.48382775, 30.64666387, 30.76335775, 30.89855346,
       31.00920274, 31.14178719, 31.36434917, 31.50934146, 31.5408422 ,
       31.65817654, 31.66233957, 31.68212074, 31.61521115, 31.50116516,
       31.3537289 , 31.29826326, 31.21884706, 31.17346318, 31.10924928,
       31.08384413, 31.04057602, 31.00677311, 30.97926175, 30.9219241 ,
       30.85605964, 30.75991644, 30.66263888, 30.56112818, 30.49593287,
       30.42159579, 30.35300219, 30.25396095, 30.12806953, 30.00683184,
       29.88596856, 29.77465969, 29.67200348, 29.44449303, 29.16077132,
       28.73334622, 28.44315134, 28.26847774, 30.05286256, 31.48764208,
       32.79089027, 34.00440787, 34.974816  , 35.94054332, 36.74548815,
       37.52448613, 38.22161439, 38.85412247, 39.44560887, 40.01300131,
       40.46404081, 40.93608027, 41.23589808, 41.738049  , 42.09214711,
       42.48087021, 42.68121184, 43.08297528, 43.20161127, 43.81697972,
       43.5411077 , 23.44709978, 18.86465073, 19.69743672, 12.43670652,
       14.86101258, 10.62329681, 10.11052243,  8.19911741,  6.85263458,
        5.86438978,  5.09350317,  4.46226367,  3.95423065,  3.551953  ,
        3.21719913,  2.92841562,  2.68772025,  2.48289835,  2.30764483,
        2.16084765,  2.03342198,  1.91812393,  1.81698027,  1.73063266,
        1.65398294,  1.5249094 ,  1.41916637,  1.33874177,  1.2635828 ,
        1.20193893,  1.14666387,  1.10035594,  1.05907844,  1.02324828,
        0.99327164,  0.96607832,  0.94315089,  0.92260419,  0.90544872,
        0.89146043,  0.87776439,  0.84051848,  0.83495543,  0.63568204,
        0.79673632,  0.46762227,  0.78310072,  0.42743292,  0.79006778,
        0.41314078,  0.79098676,  0.39522179,  0.77957423,  0.37688339,
        0.76490738,  0.35738821,  0.74435775,  0.3506795 ,  0.70157044,
        0.35776119,  0.66187249,  0.36138781,  0.62801133,  0.36929556,
        0.5836847 ,  0.39169016])
calc_topside.pr_d = np.array([20.        , 40.        , 40.        , 40.        , 40.        ,
       40.        , 40.        , 40.        , 40.        , 40.        ,
       40.        , 40.        , 40.        , 40.        , 40.        ,
       40.        , 40.        , 40.        , 40.        , 40.        ,
       40.        , 40.        , 39.73846741, 39.50779724, 39.29280701,
       39.15154724, 38.95588989, 38.78076782, 38.5113739 , 38.39947205,
       38.17947083, 38.2815918 , 38.07595825, 38.4173584 , 37.93044434,
       38.712146  , 37.53964539, 38.75882874, 37.42168884, 39.03023376,
       37.48808289, 38.54162598, 37.59266968, 38.39746399, 37.68073425,
       38.44909058, 37.68136597, 38.62834167, 37.55719604, 38.80574341,
       37.42737427, 38.78411865, 37.36469116, 38.76561584, 37.3327179 ,
       38.76506958, 37.31413269, 38.77938843, 37.29913635, 38.79940186,
       37.28538513, 38.74854431, 37.32297363, 38.59736023, 37.41118164,
       38.47200623, 37.5150116 , 38.43768921, 37.60099182, 38.49898682,
       37.63776855, 38.64728699, 37.59842834, 38.85569458, 37.50698547,
       38.95628052, 37.43514709, 38.90515747, 37.48011475, 38.60256042,
       37.60481873, 38.46245117, 37.72568054, 38.48234863, 37.79568176,
       38.62625122, 37.76990662, 38.90147095, 37.63112488, 39.01244507,
       37.54668579, 39.05025024, 37.49921265, 38.97692566, 37.51887207,
       38.84724731, 37.60302734, 38.69526978, 37.71726685, 38.6272644 ,
       37.81908569, 38.66113281, 37.87165833, 38.78828735, 37.85037842,
       39.00200806, 37.7355835 , 39.06470032, 37.72076111, 38.94489441,
       37.77495728, 38.8012207 , 37.86806335, 38.73726196, 37.94858704,
       38.76558533, 37.98517151, 38.88259583, 37.95371094, 39.10024109,
       37.86604919, 39.15959778, 37.8129425 , 39.15474243, 37.80319824,
       39.04707947, 37.86049805, 38.91178589, 37.96164246, 38.83877258,
       38.05596008, 38.85094299, 38.11046753, 38.94764404, 38.1070343 ,
       38.9901001 , 38.1098053 , 39.0894043 , 38.06740112, 39.23391724,
       37.99162292, 39.37011108, 37.87643127, 39.27085571, 37.99426575,
       38.80423889, 38.20928345, 38.68979492, 38.37173462, 38.75968323,
       38.47810974, 38.93254089, 38.52041626, 39.21067505, 38.48342285,
       39.57423401, 38.38967285, 39.98577271, 38.13429565, 39.77612915,
       38.158255  , 39.05860901, 38.53913269, 38.88936768, 38.7481842 ,
       38.97098389, 38.88620911, 39.05262146, 38.96730957, 39.11704712,
       39.00870056, 39.14390259, 39.04116821, 39.16582642, 39.05836182,
       39.00638428, 38.96183167, 39.0433075 , 39.03452148, 39.13247681,
       39.17736511, 39.29537659, 39.30582581, 39.38472595, 39.4291687 ,
       39.52206726, 39.58588867, 39.72179871, 39.8497345 , 40.        ,
       40.        , 40.        , 40.        , 40.        , 40.        ,
       40.        , 40.        , 40.        , 40.        , 40.        ,
       40.        , 40.        , 40.        , 40.        , 40.        ,
       40.        , 40.        , 40.        , 40.        , 40.        ,
       40.        , 40.        , 40.        , 40.        , 40.        ,
       40.        , 40.        , 40.        , 40.        , 40.        ,
       40.        , 40.        , 40.        , 40.        , 40.        ,
       40.        , 40.        , 40.        , 40.        , 40.        ,
       40.        , 40.        , 40.        , 40.        , 40.        ,
       40.        , 40.        , 40.        , 40.        , 40.        ,
       40.        , 40.        , 40.        , 40.        , 40.        ,
       40.        , 40.        , 40.        , 40.        , 40.        ,
       40.        , 40.        , 40.        , 40.        , 40.        ,
       40.        , 40.        , 40.        , 39.99696045, 40.        ,
       40.        , 40.        , 40.        , 40.        , 40.        ,
       40.        , 40.        , 40.        , 40.        , 40.        ,
       39.99048157, 40.        , 40.        , 40.        , 40.        ,
       40.        , 40.        , 40.        , 40.        , 40.        ,
       40.        , 40.        , 40.        , 40.        , 40.        ,
       40.        , 39.97969055, 39.91156311, 39.89125671, 39.84000244,
       39.79256592, 39.69637756, 39.65837402, 39.54380798, 39.56552429,
       39.35097351, 20.        , 20.        , 20.        , 20.        ,
       20.        , 20.        , 20.        , 20.        , 20.        ,
       20.        , 20.        , 20.        , 20.        , 20.        ,
       20.        , 20.        , 20.        , 20.        , 20.        ,
       20.        , 20.        , 20.        , 20.        , 20.        ,
       20.        , 20.        , 20.        , 20.        , 20.        ,
       20.        , 20.        , 20.        , 20.        , 20.        ,
       20.        , 20.        , 20.        , 20.        , 20.        ,
       20.        , 20.        , 20.        , 20.        , 20.        ,
       20.        , 20.        , 20.        , 20.        , 20.        ,
       20.        , 20.        , 20.        , 20.        , 20.        ,
       20.        , 20.        , 20.        , 20.        , 20.        ,
       20.        , 20.        , 20.        , 20.        , 20.        ,
       20.        , 20.        ])

self.t_comp, self.s_comp, self.w_comp = CalcTopside.conf_comp(self,0.5)
print(0)