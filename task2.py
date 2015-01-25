import numpy as np
from params import *
from puasson import *
from diff2 import *
from numpy import linalg as LA
import sweep

def toFile(u,v,p,f):
	f.write("TITLE = Test\n")
	f.write("VARIABLES = X,Y,U,V,P\n")#здесь поставить давление
	x = np.arange(0,HIGHT,hx)
	y = np.arange(0,HIGHT,hy)
	f.write("ZONE T=Test1,I=" + str(N) + ", J="+ str(M) + ", F=POINT"+"\n")
	for i in range(0, N):
		for j in range(0, M):
			f.write(str(x[i])+" "+str(y[j])+" "+str(u[j,i])+" "+str(v[j,i])+" " +str(p[j,i]) + " "+ "\n")#тут добавить давление


def A(u):
	new_u = u.copy()
	for i in range(1, N - 1):
		for j in range(1, M - 1):
			new_u[i,j] = ((u[i + 1,j] - 2*u[i,j] + u[i - 1,j])/(hx*hx) + (u[i,j+1] - 2*u[i,j] + u[i,j-1])/(hy*hy))
	return new_u


'''def A(u):
	u[1:-1,1:-1] = d2x(u) + d2y(u)
	return u
'''
def A2(u):
	u[1:-1,1:-1] = np.dot(d2x(u),d2x(u)) + 2*d2x(u)*d2y(u) + np.dot(d2y(u),d2y(u))
	return u

def calcSpeed(U,V,P):
	U_new = U.copy()
	V_new = V.copy()
	
	#avarUV = np.dot(avarageX(U),avarageY(V))
	avarU = avarageX(U)
	avarV = avarageY(V)
	avarUV = np.dot(avarageY(U),avarageX(V))
	for i in range(1,N -1):
		for j in range(1,M -1):
			
			def calcNewU():
				one = U[i,j]
				two = (   (avarU[i,j+1])**2 - (avarU[j,i])**2   )/hx
				three = (  avarUV[i + 0.5,j + 0.5] - avarUV[i - 0.5,j + 0.5])/hy
				four  = (P[i,j+1] -P[i,j])/hx
				five  = (U[i,j+1.5] - 2*U[i,j+0.5] + U[i,j-0.5])/(hx**2)
				six   = (U[i+1,j+0.5] - 2*U[i,j+0.5] + U[i-1,j+0.5])/(hy**2)
				return one + t*(-two -three - four + (five + six)/RE)

			def calcNewV():				
				one   = V[i,j]
				two   = (   (avarV[i+1,j])**2 - (avarV[i,j])**2   )/hy
				three = (  avarUV[i+0.5,j+0.5] - avarUV[i+0.5,j-0.5])/hx
				four  = (P[i+1,j] -P[i,j])/hy
				five  = (V[i+0.5,j+1] - 2*V[i,j+0.5] + V[i+0.5,j-1])/(hx**2)
				six   = (V[i+1.5,j+0.5] - 2*V[i+0.5,j] + V[i-0.5,j])/(hy**2)
				return one + t*(-two -three - four + (five + six)/RE)


			U_new[i,j] = calcNewU()
			V_new[i,j] = calcNewV()

	return (U_new,V_new)

def calcPressue(U,V,P):
	#avarUV = np.dot(avarageX(U),avarageY(V))
	avarU = avarageX(U)
	avarV = avarageY(V)
	avarUV = np.dot(avarageY(U),avarageX(V))
	P_new = P.copy()
	D     = P.copy()
	Sp    = P.copy()
	for i in range(1,N - 1):
		for j in range(1, M - 1):
			D[i,j] = (U[i,j+0.5] - U[i,j-0.5])/hx + (V[i+0.5,j] - V[i-0.5,j])/hy

	for i in range(1,N - 1):
		for j in range(1, M - 1):
			one = (avarU[i,j+1]**2 - 2*(avarU[i,j]**2) + avarU[i,j-1]**2)/(hx**2)
			two = avarUV[i+0.5,j+0.5]-avarUV[i-0.5,j+0.5] - avarUV[i+0.5,j-0.5] + avarUV[i-0.5,j-0.5]
			three = (avarV[i+1,j]**2 - 2*(avarV[i,j]**2) + avarV[i-1,j]**2)/(hy**2)
			four  = D[i,j]/t
			five  = (D[i,j+1] - 2*D[i,j] + D[i,j - 1])/(hx**2)
			six   = (D[i+1,j] - 2*D[i,j] + D[i -1,j])/(hy**2)

			Sp[i,j] = one + 2*(two)/(hx*hy) + three - four - (five + six)/RE
	puasson = TaskPuasson(A,P,-Sp)
	P_new = puasson.solve(EPS)
	print(LA.norm(D))	
	return P_new


def bounds(U,V,P):
	U[:,-1]=U[:,-2]
	U[:,0] = U[:,1]
	P[-1] = 0
	P[0]  = 0
	'''U[:,0] = USTART_INPUT
	U[:,-1] = USTART_OUTPUT'''


def main():
	index = 'ij'
	#сетка и индексы для U#
	xU,yU   = np.meshgrid(np.linspace(0,HIGHT,nxU),np.linspace(0,HIGHT,nyU),indexing=index)
	ixU,jyU = np.indices((nyU,nxU))
	#сетка и индексы для V#
	xV,yV   = np.meshgrid(np.linspace(0,HIGHT,nxV),np.linspace(0,HIGHT,nyV),indexing=index)
	ixV,jyV = np.indices((nyV,nxV))
	#для P#
	xP,yP   = np.meshgrid(np.linspace(0,HIGHT,nxP),np.linspace(0,HIGHT,nyP),indexing=index)
	ixP,jyP = np.indices((nyP,nxP))
	#для актуальной сетки#
	xG,yG   = np.meshgrid(np.linspace(0,HIGHT,N),np.linspace(0,HIGHT,M),indexing=index)
	ixG,jyG = np.indices((M,N))
	
	G       = np.zeros(xG.shape)
	U       = np.zeros(xU.shape)
	V       = np.zeros(xV.shape)
	P       = np.zeros(xP.shape)
	
	U[:,0] = USTART_INPUT
	U[:,-1] = USTART_OUTPUT
	P[:,0] = PRESSURE_INPUT
	P[:,-1] = PRESSURE_OUTPUT

	f = open("task2.dat","w")
	print(U.shape,V.shape,P.shape,G.shape)
	bounds(U=U,V=V,P=P)
	#print(calcSpeed(U,V,P)[1].shape)
	#print(calcPressue(U,V,P))
	#print(A2(U).shape)
	#print(avarageY(avarageX(P)).shape)
	
	for step in range(T):
		#print(step)
		U,V = calcSpeed(U,V,P)
		P   = calcPressue(U,V,P)
		#print(P.shape)
		bounds(U=U,V=V,P=P)
		toFile(u=avarageX(U),v=avarageY(V),p=avarageY(P),f=f)
		#if step == 1:
		#	print(U)
		#	break
	
	#print(np.dot((avarageY(P)*2),(avarageX(P)*2)).shape)
	
	f.close()	

main()