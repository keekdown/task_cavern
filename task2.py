import numpy as np
from params import *
from puasson import *
from diff2 import *
import sweep

def A(u):
	new_u = u.copy()
	for i in range(1, N - 1):
		for j in range(1, M - 1):
			new_u[i,j] = ((u[i + 1,j] - 2*u[i,j] + u[i - 1,j])/(hx*hx) + (u[i,j+1] - 2*u[i,j] + u[i,j-1])/(hy*hy))
	return new_u

def A2(u):
	u[1:-1,1:-1] = np.dot(d2x(u),d2x(u)) + 2*d2x(u)*d2y(u) + np.dot(d2y(u),d2y(u))
	return u

def calcSpeed(U,V,P):
	U_new = U.copy()
	V_new = V.copy()
	#avarUV = avarageX(U)*avarageY(V)
	avarUV = np.dot(avarageX(U),avarageY(V))
	avarU = avarageX(U)
	avarV = avarageY(V)

	for i in range(1,N -1):
		for j in range(1,M -1):
			
			def calcNewU():
				one = U[i,j]
				two = (   (avarU[i+1,j])**2 - (avarU[i,j])**2   )/hx
				three = (  avarUV[i,j + 1] - avarUV[i,j - 1])/hy
				four  = (P[i+1,j] -P[i,j])/hx
				five  = (U[i+1,j] - 2*U[i,j] + U[i-1,j])/(hx**2)
				six   = (U[i,j+1] - 2*U[i,j] + U[i,j-1])/(hy**2)
				return one + t*(-two -three - four + (five + six)/RE)

			def calcNewV():				
				one   = V[i,j]
				two   = (   (avarV[i,j+1])**2 - (avarV[i,j])**2   )/hy
				three = (  avarUV[i+1,j] - avarUV[i-1,j])/hx
				four  = (P[i,j+1] -P[i,j])/hy
				five  = (V[i+1,j] - 2*V[i,j] + V[i-1,j])/(hx**2)
				six   = (V[i,j+1] - 2*V[i,j] + V[i,j-1])/(hy**2)
				return one + t*(-two -three - four + (five + six)/RE)


			U_new[i,j] = calcNewU()
			V_new[i,j] = calcNewV()

	return (U_new,V_new)

def calcPressue(U,V,P):
	#avarUV = avarageX(U)*avarageY(V)
	avarUV = np.dot(avarageX(U),avarageY(V))
	avarU = avarageX(U)
	avarV = avarageY(V)
	P_new = P.copy()
	D     = P.copy()
	Sp    = P.copy()
	for i in range(1,N - 1):
		for j in range(1, M - 1):
			D[i,j] = (U[i+1,j] - U[i-1,j])/hx + (V[i,j+1] - V[i,j-1])/hy

	for i in range(1,N - 1):
		for j in range(1, M - 1):
			one = (avarU[i+1,j]**2 - 2*avarU[i,j]**2 + avarU[i-1,j]**2)/(hx**2)
			two = avarUV[i,j+1]-avarUV[i,j-1] - avarUV[i-1,j+1] + avarUV[i-1,j-1]
			three = (avarV[i,j+1]**2 - 2*avarV[i,j]**2 + avarV[i,j-1]**2)/(hy**2)
			four  = D[i,j]/t
			five  = (D[i+1,j] - 2*D[i,j] + D[i - 1,j])/(hx**2)
			six   = (D[i,j+1] - 2*D[i,j] + D[i,j -1])/(hy**2)

			Sp[i,j] = one + 2*(two)/(hx*hy) + three - four - (five + six)/RE
	puasson = TaskPuasson(A2,P,Sp)
	return puasson.solve(EPS)


def bounds(U,V,P):
	U[:,0] = USTART_INPUT
	U[:,-1]=U[:,-2]
	P[:,0] = PRESSURE_INPUT
	P[:,-1] = PRESSURE_OUTPUT


def main():
	#сетка и индексы для U#
	xU,yU   = np.meshgrid(np.linspace(0,HIGHT,nxU),np.linspace(0,HIGHT,nyU),indexing='xy')
	ixU,jyU = np.indices((nyU,nxU))
	#сетка и индексы для V#
	xV,yV   = np.meshgrid(np.linspace(0,HIGHT,nxV),np.linspace(0,HIGHT,nyV),indexing='xy')
	ixV,jyV = np.indices((nyV,nxV))
	#для P#
	xP,yP   = np.meshgrid(np.linspace(0,HIGHT,nxP),np.linspace(0,HIGHT,nyP),indexing='xy')
	ixP,jyP = np.indices((nyP,nxP))
	#для актуальной сетки#
	xG,yG   = np.meshgrid(np.linspace(0,HIGHT,N),np.linspace(0,HIGHT,M),indexing='xy')
	ixG,jyG = np.indices((M,N))

	G       = np.zeros(xG.shape)
	U       = np.zeros(xU.shape)
	V       = np.zeros(xV.shape)
	P       = np.zeros(xP.shape)
	
	'''G       = np.zeros((N,M))
	U       = np.zeros((nxU,nyU))
	V       = np.zeros((nxV,nyV))
	P       = np.zeros((nxP,nyP))
	'''
	#print(U.shape,V.shape,P.shape,G.shape)
	bounds(U=U,V=V,P=P)
	#print(calcSpeed(U,V,P)[1].shape)
	#print(calcPressue(U,V,P))
	#print(A2(U).shape)
	for step in range(T):
		print(step)
		U,V = calcSpeed(U,V,P)
		P   = calcPressue(U,V,P)
		if step == 20:
			print(U)
		

main()