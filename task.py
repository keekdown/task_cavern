import numpy as np
from params import *
from numpy import linalg as LA
from diff import*
from sweep import*
from puasson import*
import sys

#omega = du/dy - dv/dx = d2psi/dx + d2psi/dy

def A(u):
	new_u = u.copy()
	for i in range(1, N - 1):
		for j in range(1, M - 1):
			new_u[i,j] = ((u[i + 1,j] - 2*u[i,j] + u[i - 1,j])/(hx*hx) + (u[i,j+1] - 2*u[i,j] + u[i,j-1])/(hy*hy))
	return new_u

def toFile(u,v,psi,omega,f):
	f.write("TITLE = Test\n")
	f.write("VARIABLES = X,Y,U,V,Psi\n")
	x = np.arange(0,HIGHT,hx)
	y = np.arange(0,HIGHT,hy)
	f.write("ZONE T=Test1,I=" + str(N) + ", J="+ str(M) + ", F=POINT"+"\n")
	for i in range(0, N):
		for j in range(0, M):
			f.write(str(x[i])+" "+str(y[j])+" "+str(u[j][i])+" "+str(v[j][i])+" "+str(psi[j][i])+"\n")
			
def boundOmega(psi,u,v,omega):
	omega[0]     = (2*psi[1] + hx*u[0])/(hx*hx)
	omega[N - 1] = (2*psi[N - 2] + hx*u[N - 1] )/(hx*hx)
	omega[:,0]   = (2*psi[:,1])/(hy*hy)
	omega[:,M-1] = (2*psi[:,M-2])/(hy*hy)
			
def main():
	files = open("data.dat","w")
	u = np.zeros((N,M))
	v = u.copy()
	psi = u.copy()
	omega = u.copy()
	u[N - 1] = USTART
	u[0]     = USTART
	boundOmega(psi,u,v,omega)
	#print(omega)
	for step in range(0,T):
		print("Start sweep in x")
		for row in range(0,N):
			a = -u[row,1:-1]/(2*hx) - 1.0/(RE*hx*hx)
			c = numpy.zeros(a.size)
			c.fill((2.0/t - 2.0/(RE*hx*hx)))
			b = u[row,1:-1]/(2*hx) - 1.0/(RE*hx*hx)
			coef_f1 = (dy(omega))[row,1:-1]#(dC(omega[row,:]))
			coef_f2 = (d2y(omega))[row,1:-1]#(d2(omega[row,:]))
			f = (-omega[row,1:-1] * 2)/t + v[row,1:-1]*coef_f1 - (1.0/RE)*coef_f2
			sweep = Sweep(a,b,-c,-f)
			omega[row,:] = sweep.solve(omega[row,0],omega[row,M-1])
		print("Start sweep in y")
		for col in range(0,N):
			a = -v[1:-1,col]/(2*hy) - 1.0/(RE*hy*hy)
			c = a.copy()
			c.fill(2.0/t - 2.0/(RE*hy*hy))
			b = v[1:-1,col]/(2*hy) - 1.0/(RE*hy*hy)
			coef_f1 = (dx(omega))[1:-1,col]#(dC(omega[:,col]))
			coef_f2 = (d2x(omega))[1:-1,col]#((d2(omega[:,col])))
			f = (-omega[1:-1,col] * 2)/t + u[1:-1,col]*coef_f1 - (1.0/RE)*coef_f2
			sweep = Sweep(a,b,-c,-f)
			omega[:,col] = sweep.solve(omega[0,col],omega[M-1,col])
		puasson = TaskPuasson(A,psi,-omega)
		print("Start puasson")
		psi = puasson.solve(EPS)
		v   = -1*dx(psi)
		u   =  dy(psi)
		boundOmega(psi,u,v,omega)
		toFile(u,v,psi,omega,files)
	files.close()
	
	
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
	print(sweep.solve(0,0))
	#TDMA(a,b,c,f)
	
def test2():
	u_cor = np.zeros((N,M))
	u_cor[1:-1,1:-1] = 5
	f = A(u_cor)
	print(f)
	u = np.zeros((N,M))
	t = TaskPuasson(A,u,f)
	s = t.solve(0.000001)
	#s = puasson(A,u,u_cor,0.0000001)
	print(s)
#test2()
