HIGHT = 1
hx = 1.0/5
hy = 1.0/5
N  = int(HIGHT/hx)
M  = int(HIGHT/hy)

nxU,nyU = N,M + 1
nxV,nyV = N + 1,M
nxP,nyP = N + 1,M + 1


RE = 400
t  = 0.01
T  = 100
USTART_UP = 1
USTART_INPUT = 0
USTART_OUTPUT = 0
EPS    = 0.0001
approxUVbound =  True
shift_1div2      =  1
PRESSURE_INPUT   =  2
PRESSURE_OUTPUT  =  1