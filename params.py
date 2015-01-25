HIGHT = 1
hx = 0.1#1.0/5
hy = 0.1#1.0/5
N  = int(HIGHT/hx)
M  = int(HIGHT/hy)

nxU,nyU = N,M + 1
nxV,nyV = N + 1,M
nxP,nyP = N +1,M + 1


RE = 400
t  = 0.01
T  = 100
USTART_UP = 0
USTART_INPUT = 1
USTART_OUTPUT = 1
EPS    = 0.0001
approxUVbound =  True
PRESSURE_INPUT   =  1
PRESSURE_OUTPUT  =  0