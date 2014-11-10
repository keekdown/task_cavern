import numpy as np
from numpy import linalg as LA
from diff import*
from sweep import*
from puasson import*

def A(u):
	new_u = u.copy()
	hx = 1.0/(u[0].size ** 2)
	hy = 1.0/float(u[0:u[0].size,0:1].size ** 2)
	for j in range(1, u.shape[0] - 1):
		for i in range(1, u.shape[1] - 1):
			new_u[j,i] = ((u[j,i + 1] - 2*u[j,i] + u[j,i - 1])/hx + (u[j + 1,i] - 2*u[j,i] + u[j - 1,i])/hy)
	return new_u

def toFile(u,v,psi,omega,f):
	#~ f=open("data.dat","a")
	f.write("TITLE = Test\n")
	f.write("VARIABLES = X,Y,U,V,Psi,W\n")
	x = np.linspace(0,u.shape[0],u.shape[0])
	y = np.linspace(0,u.shape[1],u.shape[1])
	f.write("ZONE T=Test1,I=" + str(u.shape[0]) + ", J="+ str(u.shape[1]) + ", F=POINT"+"\n")
	for i in range(0, u.shape[0]):
		for j in (range(0, u.shape[1])):
			f.write(str(x[j])+" "+str(y[i])+" "+str(u[i][j])+" "+str(v[i][j])+" "+str(psi[i][j])+" "+str(omega[i][j])+"\n")
			
	
def main():
	N=10
	M=10
	EPS = 0.001
	RE = 400#reinolds
	T = 10#maybe second
	f = open("data.dat","w")
	GAPS = 100#gaps on time
	tau = T / GAPS;
	u = np.zeros((N,M))
	hx = 1.0/(u.shape[0])
	hy = 1.0/(u.shape[1])
	v = u.copy()
	psi = u.copy()
	omega = u.copy()
	u[N-1] = 1
	omega[0],omega[N - 1],omega[:,N-1],omega[:,0] = (2*(psi[0] - psi[1] + hx*u[0])/(hx*hx),				#down
															 2*(psi[N-2] - psi[N-1] + hx*u[N-1])/(hx*hx),	#up
															 2*(psi[:,N-2] - psi[:,N-1] + hy*v[:,N-1])/(hy*hy),		#left
															 2*(psi[:,0] - psi[:,1] + hy*v[:,0])/(hy*hy))	#right
	c = np.zeros(u.size)
	c.fill(-2.0/tau + 1.0/(RE*hx*hx))
	#~ print(omega)
	for gap in range(0, GAPS):
		print("Start Sweep onx")
		for i in range(1, N - 1):
			sweep = Sweep(-u[1:-1,i]/(2*hx) - 1.0/(RE*hx*hx),u[1:-1,i]/(2*hx) - 1.0/(RE*hx*hx),c,((2.0/tau)*omega[1:-1,i] - v[1:-1,i]*d(omega[1:-1,i])  + (1.0/RE)*d2(omega[1:-1,i])))
			omega[i] = sweep.solve(omega[0][i],omega[-1][i])
		print("Start Sweep ony")
		for i in range(1, N - 1):
			sweep = Sweep(-v[i,1:-1]/(2*hy) - 1.0/(RE*hy*hy),v[i,1:-1]/(2*hy) - 1.0/(RE*hy*hy),c,((2.0/tau)*omega[i,1:-1] - u[i,1:-1]*d(omega[i,1:-1])  +(1.0/RE)*d2(omega[i,1:-1])))
			omega[:,i] = sweep.solve(omega[i][0],omega[i][-1])
		print("Start puasson")
		
		tp = TaskPuasson(A,psi,-1*omega)
		#~ print(omega,u)
		psi = tp.solve(EPS)
		v = -1*dx(psi,v)
		u = dy(psi,u)
		omega[0],omega[N - 1],omega[:,N-1],omega[:,0] = (2*(psi[0] - psi[1] + hx*u[0])/(hx*hx),				#down
															 2*(psi[N-2] - psi[N-1] + hx*u[N-1])/(hx*hx),	#up
															 2*(psi[:,N-2] - psi[:,N-1] + hy*v[:,N-1])/(hy*hy),		#left
															 2*(psi[:,0] - psi[:,1] + hy*v[:,0])/(hy*hy))	#right
		toFile(u,v,psi,omega,f)
	f.close()
	#print(omega)
	
	
main()

def test():
	a = np.zeros(2)
	b = a.copy()
	c = a.copy()
	f = a.copy()
	a[:] = (1,2)
	b[:] = (1,0)
	c[:] = (1,1)
	f[:] = (3,2)
	sweep = Sweep(a,b,c,f)
	print(sweep.solve(2,1))
#test()
