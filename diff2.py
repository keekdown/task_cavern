d2x = lambda u:(u[2:,1:-1]-2*u[1:-1,1:-1]+u[:-2,1:-1])
d2y = lambda u:(u[1:-1, 2:] - 2*u[1:-1, 1:-1] + u[1:-1, :-2])
dxC = lambda u:(u[2:,:] - u[:-2,:])
dyC = lambda u:(u[:, 2:] - u[:, :-2])
dxR = lambda u:(u[1:,:] - u[:-1,:])
dyR = lambda u:(u[:,1:] - u[:,:-1])
avarageX = lambda u:(u[1:,:] + u[:-1,:])/2
avarageY = lambda u:(u[:,1:] + u[:,:-1])/2