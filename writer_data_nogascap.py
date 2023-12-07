def write_file(x,prob,particle,iter):#input, problem, particle, iteration
    filename = f"EGG_{prob}_{iter}_{particle}.DATA"
    with open(filename, 'w') as f:
        DATA=f"""--NOECHO

RUNSPEC
TITLE
--VEM
UNIFOUT

DIMENS
    60 60 7  /

METRIC
OIL
WATER
GAS
DISGAS
VAPOIL
CPR
/
NUMRES
    1 /
UDQDIMS
10  10  10  10  /
TABDIMS
-- NTSFUN NTPVT NSSFUN  NPPVT   NFIP    NRRSV
    2   2       36       50    5    50  /
EQLDIMS
    2* 100 2* /
REGDIMS
    6* /
WELLDIMS
       12   100     4    12     0     0     0     0     0     0     0     0 /
VFPPDIMS
    6* /
VFPIDIMS
    3* /
AQUDIMS
    2*     1 3* /
NSTACK
 -75 /
START
1 JAN 2025 /

GRID 


SPECGRID
    60 60 7 1 F /

INCLUDE
   '../include/ACTIVE.INC' /


DX
    25200*8 /


DY
    25200*8 /


DZ
    25200*4 /

TOPS
    3600*4000 3600*4004 3600*4008 3600*4012 3600*4016 3600*4020 3600*4024/

INCLUDE
'../include/mDARCY.INC'
/

NTG
  25200*1 /

PORO
  25200*0.2 /

--ECHO
--
--INIT
--/

EDIT
MULTIPLY
'PORV'  150  1   60  1   60  1   7   /
/

PROPS

INCLUDE
'../include/PVT-WET-GAS.INC'
/

INCLUDE
'../include/SCAL_NORNE.INC'
/

REGIONS

EQUALS
'SATNUM'  1    1  60  1   60    1  7  / 
'PVTNUM'  1    1  60  1   60    1  7  /
'FIPNUM'  1    1  60  1   60    1  7  /
/

SOLUTION
EQUIL
-- Datum    P     woc     Pc   goc    Pc  Rsvd  Rvvd
    4030  250  4030     0.0  3800   0.0   1   1   0 / 

RSVD
4008  250
4020  250 /

RVVD
4008  0
4020  0 /

--RPTRST
--BASIC=2 KRO KRW KRG /
--
--RPTSOL
--FIP=3  SWAT / 
--
--RPTSOL
-- RESTART=2 /
--/

SUMMARY
FOPR
FOPT
FWPR
FWPT
FWIR
FWIT
FGPR
FGPT
FGIR
FGIT
FGOR
FPR
FOIP
FGIP
--FUGOUT
--FUWOUT
WBHP
/
WBP9
/
WPI
/
WBP
/
WGPR
/
WOPR
/
WWPR
/
WWIR
/
WGIR
/   
WLPR
/
--EXCEL
--RPTONLY

SCHEDULE

INCLUDE
'../include/schedule/SCHEDULE_{prob}_{iter}_{particle}.INC' /
        """
        f.write(DATA)