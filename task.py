import numpy as np
from numpy import linalg as LA
from diff import*
from sweep import*
from puasson import*
import sys
N=10
M=10

def A(u):
	new_u = u.copy()
	hx = 1.0/(u.shape[0] ** 2)
	hy = 1.0/float(u.shape[1] ** 2)
	for i in range(1, u.shape[0] - 1):
		for j in range(1, u.shape[1] - 1):
			new_u[i,j] = ((u[i + 1,j] - 2*u[i,j] + u[i - 1,j])/hx + (u[i,j+1] - 2*u[i,j] + u[i,j-1])/hy)
	return new_u

def toFile(u,v,psi,omega,f):
	#u[N-1] = 1
	#omega[0],omega[N - 1],omega[:,N-1],omega[:,0] = (0,0,0,0)
	#~ f=open("data.dat","a")
	f.write("TITLE = Test\n")
	f.write("VARIABLES = X,Y,U,V,Psi\n")
	x = np.linspace(0,10,10)
	y = np.linspace(0,10,10)
	f.write("ZONE T=Test1,I=" + str(u.shape[0]) + ", J="+ str(u.shape[1]) + ", F=POINT"+"\n")
	for i in range(0, u.shape[0]):
		for j in range(0, u.shape[1]):
			f.write(str(x[i])+" "+str(y[j])+" "+str(u[i][j])+" "+str(v[i][j])+" "+str(psi[i][j])+"\n")
			
def main():
	EPS = 0.0001
	RE = 100#reinolds
	T = 10#maybe second
	f = open("data.dat","w")
	GAPS = 1000#gaps on time
	tau = 0.001#T/GAPS#float(T / GAPS);
	u = np.zeros((N,M))
	hx = 1.0/(u.shape[0])
	hy = 1.0/(u.shape[1])
	v = u.copy()
	psi = u.copy()
	omega = u.copy()
	u[N-1] = (np.arange(0,N,1)**4)
	omega[0],omega[N - 1],omega[:,N-1],omega[:,0] = (2*(-psi[1])/(hx*hx),				#down
									2*(+psi[N-2] + hx*u[N-1])/(hx*hx),	#up
									2*(-psi[:,N-2])/(hy*hy),		#left
									2*(-psi[:,1])/(hy*hy))	#right
	c = np.zeros(u.size)
	c.fill(2.0/tau - 1.0/(RE*hx*hx))
	try:	
		for gap in range(0, GAPS):
			print("Start Sweep onx")
			for j in range(1, N - 1):
				sweep = Sweep((-u[j,1:-1]/(2*hx) - 1.0/(RE*hx*hx)),u[j,1:-1]/(2*hx) - 1.0/(RE*hx*hx),-c,-((2.0/tau)*omega[j,1:-1] - v[j,1:-1]*d(omega[j,1:-1])  + (1.0/RE)*d2(omega[j,1:-1])))
				omega[j,:] = -((sweep.solve(omega[j][0],omega[j][-1])))
				#if gap == 1:
				#	print(omega[1,:])
				#	sys.exit()
			print("Start Sweep ony")
			for i in range(1, N - 1):
				sweep = Sweep((-v[1:-1,i]/(2*hy) - 1.0/(RE*hy*hy)),v[1:-1,i]/(2*hy) - 1.0/(RE*hy*hy),-c,-((2.0/tau)*omega[1:-1,i] - u[1:-1,i]*d(omega[1:-1,i])  +(1.0/RE)*d2(omega[1:-1,i])))
				omega[:,i] = -((sweep.solve(omega[0][i],omega[-1][i])))
			print("Start puasson")
			tp = TaskPuasson(A,psi,-omega)
			psi = tp.solve(EPS)
			v = -1*dx(psi,v)
			u = dy(psi,u)
			omega[0],omega[N - 1],omega[:,N-1],omega[:,0] = (2*(-psi[1])/(hx*hx),				#down
									2*(+psi[N-2] + hx*u[N-1])/(hx*hx),	#up
									2*(-psi[:,N-2])/(hy*hy),		#left
									2*(-psi[:,1])/(hy*hy))	#right
			toFile(u,v,psi,omega,f)
	except RuntimeError:
		print("BAAAD")
		sys.exit()
	f.close()
	
	
main()

def test():
	a = np.zeros(3)
	b = a.copy()
	c = a.copy()
	f = a.copy()
	a[:] = (1,1,1)
	b[:] = (3,3,3)
	c[:] = (2,2,2)
	f[:] = (1,1,1)
	sweep = Sweep(a,b,-c,-f)
	print(-(sweep.solve(0,0))[::-1])
	#TDMA(a,b,c,f)
	
def test2():
	u_cor = np.zeros((50,50))
	u_cor[1:-1,1:-1] = 5
	f = A(u_cor)
	print(f)
	u = np.zeros((50,50))
	t = TaskPuasson(A,u,f)
	s = t.solve(0.000001)
	#s = puasson(A,u,u_cor,0.0000001)
	print(s)
#test()
