def write_file(x,prob,particle,iter):#input, problem, particle, iteration
   #print(y1)
   filename = f"SCHEDULE_{prob}_{iter}_{particle}.INC"
   #print(filename)
   with open(filename, 'w') as f:
        schedule=f"""-- <+> SCHEDULE 7/7/2011 (0 days)

--RPTSCHED
--    FIP WELSPECS WELLS /

WELSPECS
-- NAME GROUP I J K PHASE
   'I1'     'WI'   8    54  1* 'WATER' /
	'I2'     'WI'   29   51  1* 'WATER' /
	'I3'     'WI'   5    36  1* 'WATER' /
	'I4'     'GI'   27   29  1* 'GAS' /
	'I5'     'WI'   45   36  1* 'WATER' /
	'I6'     'WI'   8    20   1* 'WATER' /
	'I7'     'WI'   31   7   1* 'WATER' /
	'I8'     'WI'   53   21   1* 'WATER' /
   'P1'     'P'   16   43  1* 'OIL' /
   'P2'     'P'   35   40  1* 'OIL' /
   'P3'     'P'   23   16  1* 'OIL' /
   'P4'     'P'   43   18  1* 'OIL' /
/

COMPDAT
-- NAME    I   J  K1    K2    STAT     SATNUM   TRANS DIAM    KH  SKIN DFAC    
   'I1'        2*        5     7      'OPEN'      2*     0.1546 	1*          0 / 
	'I2'        2*        5     7      'OPEN'      2*     0.1546 	1*          0 /
	'I3'        2*        5     7      'OPEN'      2*     0.1546 	1*          0 /
	'I4'        2*        1     2      'OPEN'      2*     0.1546 	1*          0 /
	'I5'        2*        5     7      'OPEN'      2*     0.1546 	1*          0 /
	'I6'        2*        5     7      'OPEN'      2*     0.1546 	1*          0 /
	'I7'        2*        5     7      'OPEN'      2*     0.1546 	1*          0 /
	'I8'        2*        5     7      'OPEN'      2*     0.1546    1*          0 /
   'P1'        2*        3     5      'OPEN'      2*     0.1546 	1*          0 / 
   'P2'        2*        3     5      'OPEN'      2*     0.1546 	1*          0 / 
   'P3'        2*        3     5      'OPEN'      2*     0.1546 	1*          0 / 
   'P4'        2*        3     5      'OPEN'      2*     0.1546		1*          0 / 
/

GRUPTREE
-- CHILD PARENT
   'WI'  'F'   /
   'GI'  'F'   /
   'P'   'F'   /
/

WCONPROD
--NAME   STATUS   CONTROL  ORAT  WRAT  GRAT LRAT RESV BHP THP VFP
   'P1'     'OPEN'      'BHP' 5*  150/
   'P3'     'OPEN'      'BHP' 5*  150/
   'P2'     'OPEN'      'BHP' 5*  150/
   'P4'     'OPEN'      'BHP' 5*  150/
/

WCONINJE
-- NAME     PHASE       STAT     CONTROL     RATE  RESV  BHP   THP VFP
   'I1'     'WATER'  'OPEN'   BHP   2*   400     /
   'I2'     'WATER'  'OPEN'   BHP   2*   400     /
   'I3'     'WATER'  'OPEN'   BHP   2*   400     /
   'I4'     'GAS'    'OPEN'   BHP   2*   400     /
   'I5'     'WATER'  'OPEN'   BHP   2*   400     /
   'I6'     'WATER'  'OPEN'   BHP   2*   400     /
   'I7'     'WATER'  'OPEN'   BHP   2*   400     /
   'I8'     'WATER'  'OPEN'   BHP   2*   400     /
/

WPIMULT
'I1'     10 /
'I2'     10 /
'I3'     10 /
'I4'     10 /
'I5'     10 /
'I6'     10 /
'I7'     10 /
'I8'     10 /
'P1'     10 /
'P2'     10 /
'P3'     10 /
'P4'     10 /
/

GCONPROD
--NAME CONTROL ORAT  WRAT  GRAT  LRAT
'F'   'LRAT'   3*   {x[0]}   /
/

GCONINJE
'F'  'WATER'  'REIN'   2*   {x[5]}  /
'F'  'GAS'    'REIN'   2*   {x[10]} /
/


NUPCOL
10 /


DATES
1 'FEB' 2025   /
/
DATES
1 'MAR' 2025   /
/
DATES
1 'APR' 2025   /
/
DATES
1 'MAY' 2025   /
/
DATES
1 'JUN' 2025   /
/
DATES
1 'JUL' 2025   /
/
DATES
1 'AUG' 2025   /
/
DATES
1 'SEP' 2025   /
/
DATES
1 'OCT' 2025   /
/
DATES
1 'NOV' 2025   /
/
DATES
1 'DEC' 2025   /
/
DATES
1 'JAN' 2026   /
/
DATES
1 'FEB' 2026   /
/
DATES
1 'MAR' 2026   /
/
DATES
1 'APR' 2026   /
/
DATES
1 'MAY' 2026   /
/
DATES
1 'JUN' 2026   /
/
DATES
1 'JUL' 2026   /
/
DATES
1 'AUG' 2026   /
/
DATES
1 'SEP' 2026   /
/
DATES
1 'OCT' 2026   /
/
DATES
1 'NOV' 2026   /
/
DATES
1 'DEC' 2026   /
/
DATES
1 'JAN' 2027   /
/
GCONPROD
--NAME CONTROL ORAT  WRAT  GRAT  LRAT
'F'   'LRAT'   3*   {x[1]}   /
/

GCONINJE
'F'  'WATER'  'REIN'   2*   {x[6]}  /
'F'  'GAS'    'REIN'   2*   {x[11]} /
/
DATES
1 'FEB' 2027   /
/
DATES
1 'MAR' 2027   /
/
DATES
1 'APR' 2027   /
/
DATES
1 'MAY' 2027   /
/
DATES
1 'JUN' 2027   /
/
DATES
1 'JUL' 2027   /
/
DATES
1 'AUG' 2027   /
/
DATES
1 'SEP' 2027   /
/
DATES
1 'OCT' 2027   /
/
DATES
1 'NOV' 2027   /
/
DATES
1 'DEC' 2027   /
/
DATES
1 'JAN' 2028   /
/
DATES
1 'FEB' 2028   /
/
DATES
1 'MAR' 2028   /
/
DATES
1 'APR' 2028   /
/
DATES
1 'MAY' 2028   /
/
DATES
1 'JUN' 2028   /
/
DATES
1 'JUL' 2028   /
/
DATES
1 'AUG' 2028   /
/
DATES
1 'SEP' 2028   /
/
DATES
1 'OCT' 2028   /
/
DATES
1 'NOV' 2028   /
/
DATES
1 'DEC' 2028   /
/
DATES
1 'JAN' 2029   /
/
GCONPROD
--NAME CONTROL ORAT  WRAT  GRAT  LRAT
'F'   'LRAT'   3*   {x[2]}   /
/

GCONINJE
'F'  'WATER'  'REIN'   2*   {x[7]}  /
'F'  'GAS'    'REIN'   2*   {x[12]} /
/
DATES
1 'FEB' 2029   /
/
DATES
1 'MAR' 2029   /
/
DATES
1 'APR' 2029   /
/
DATES
1 'MAY' 2029   /
/
DATES
1 'JUN' 2029   /
/
DATES
1 'JUL' 2029   /
/
DATES
1 'AUG' 2029   /
/
DATES
1 'SEP' 2029   /
/
DATES
1 'OCT' 2029   /
/
DATES
1 'NOV' 2029   /
/
DATES
1 'DEC' 2029   /
/
DATES
1 'JAN' 2030   /
/
DATES
1 'FEB' 2030   /
/
DATES
1 'MAR' 2030   /
/
DATES
1 'APR' 2030   /
/
DATES
1 'MAY' 2030   /
/
DATES
1 'JUN' 2030   /
/
DATES
1 'JUL' 2030   /
/
DATES
1 'AUG' 2030   /
/
DATES
1 'SEP' 2030   /
/
DATES
1 'OCT' 2030   /
/
DATES
1 'NOV' 2030   /
/
DATES
1 'DEC' 2030   /
/
DATES
1 'JAN' 2031   /
/
GCONPROD
--NAME CONTROL ORAT  WRAT  GRAT  LRAT
'F'   'LRAT'   3*   {x[3]}   /
/

GCONINJE
'F'  'WATER'  'REIN'   2*   {x[8]}  /
'F'  'GAS'    'REIN'   2*   {x[13]} /
/
DATES
1 'FEB' 2031   /
/
DATES
1 'MAR' 2031   /
/
DATES
1 'APR' 2031   /
/
DATES
1 'MAY' 2031   /
/
DATES
1 'JUN' 2031   /
/
DATES
1 'JUL' 2031   /
/
DATES
1 'AUG' 2031   /
/
DATES
1 'SEP' 2031   /
/
DATES
1 'OCT' 2031   /
/
DATES
1 'NOV' 2031   /
/
DATES
1 'DEC' 2031   /
/
DATES
1 'JAN' 2032   /
/
DATES
1 'FEB' 2032   /
/
DATES
1 'MAR' 2032   /
/
DATES
1 'APR' 2032   /
/
DATES
1 'MAY' 2032   /
/
DATES
1 'JUN' 2032   /
/
DATES
1 'JUL' 2032   /
/
DATES
1 'AUG' 2032   /
/
DATES
1 'SEP' 2032   /
/
DATES
1 'OCT' 2032   /
/
DATES
1 'NOV' 2032   /
/
DATES
1 'DEC' 2032   /
/
DATES
1 'JAN' 2033   /
/
GCONPROD
--NAME CONTROL ORAT  WRAT  GRAT  LRAT
'F'   'LRAT'   3*   {x[4]}   /
/

GCONINJE
'F'  'WATER'  'REIN'   2*   {x[9]}  /
'F'  'GAS'    'REIN'   2*   {x[14]} /
/
DATES
1 'FEB' 2033   /
/
DATES
1 'MAR' 2033   /
/
DATES
1 'APR' 2033   /
/
DATES
1 'MAY' 2033   /
/
DATES
1 'JUN' 2033   /
/
DATES
1 'JUL' 2033   /
/
DATES
1 'AUG' 2033   /
/
DATES
1 'SEP' 2033   /
/
DATES
1 'OCT' 2033   /
/
DATES
1 'NOV' 2033   /
/
DATES
1 'DEC' 2033   /
/
DATES
1 'JAN' 2034   /
/
DATES
1 'FEB' 2034   /
/
DATES
1 'MAR' 2034   /
/
DATES
1 'APR' 2034   /
/
DATES
1 'MAY' 2034   /
/
DATES
1 'JUN' 2034   /
/
DATES
1 'JUL' 2034   /
/
DATES
1 'AUG' 2034   /
/
DATES
1 'SEP' 2034   /
/
DATES
1 'OCT' 2034   /
/
DATES
1 'NOV' 2034   /
/
DATES
1 'DEC' 2034   /
/
DATES
1 'JAN' 2035   /
/
DATES
1 'FEB' 2035   /
/
DATES
1 'MAR' 2035   /
/
DATES
1 'APR' 2035   /
/
DATES
1 'MAY' 2035   /
/
DATES
1 'JUN' 2035   /
/
DATES
1 'JUL' 2035   /
/
DATES
1 'AUG' 2035   /
/
DATES
1 'SEP' 2035   /
/
DATES
1 'OCT' 2035   /
/
DATES
1 'NOV' 2035   /
/
DATES
1 'DEC' 2035   /
/
END"""
        f.write(schedule)
