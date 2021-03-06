import numpy
from params import *
def dx(u,out,hx,N,M):
	new_u = out.copy()
	for i in range(1, N - 1):
		for j in range(1, M - 1):
			new_u[i,j] = (u[i,j+1] - u[i,j-1]) / (2*hx);
	if approxUVbound is True:
		new_u[:,0] = (u[:,1] - u[:,0])/(hx)
		new_u[:,-1] = (-u[:,-2] + u[:,-1])/(hx)
	return new_u

def dy(u,out,hy,N,M):
	new_u = out.copy()
	for i in range(1, N - 1):
		for j in range(1, M - 1):
			new_u[i,j] = (u[i+1,j] - u[i-1,j]) / (2*hy)
	if approxUVbound is True:
		new_u[0,:] = (u[1,:] - u[0,:])/(hy)
		new_u[-1,:] = (-u[-2,:] + u[-1,:])/(hy)
	return new_u
	
def dC(u,hx,N):
	new_u = u.copy()#numpy.zeros(u.shape)
	for i in range(1, N - 1):
		new_u[i] = (u[i+1] - u[i - 1]) / (2*hx)
	if approxUVbound is True:
		new_u[0] = (u[1] - u[0])/(hx)
		new_u[-1] = (-u[-1] + u[-2])/(hx)
	return new_u

def dR(u,hx,N):
	new_u = u.copy()#numpy.zeros(u.shape)
	for i in range(0, N - 1):
		new_u[i] = (u[i+1] - u[i]) / (hx)
	return new_u
	
def dL(u,hx,N):
	new_u = u.copy()#numpy.zeros(u.shape)
	for i in range(1, N):
		new_u[i] = (u[i] - u[i - 1]) / (hx)
	return new_u	
	
def d2(u,hx,N):
	new_u = u.copy()#numpy.zeros(u.shape)
	for i in range(1, N - 1):
		new_u[i] = (u[i+1] - 2* u[i] + u[i-1]) / (hx*hx)
	if approxUVbound is True:
		new_u[0] = (u[1] - u[0])/(2*hx)
		new_u[-1] = (u[-1] - u[-2])/(2*hx)
	return new_u

def d2x(u,hx,N,M):
	new_u = u.copy()#numpy.zeros(u.shape)
	for i in range(1, N - 1):
		for j in range(1, M - 1):
			new_u[i,j] = (u[i,j+1] - 2* u[i,j] + u[i,j-1]) / (hx*hx)
	if approxUVbound is True:
		new_u[:,0] = (u[:,1] - u[:,0])/(hx)
		new_u[:,-1] = (-u[:,-2] + u[:,-1])/(hx)
	return new_u
	
def d2y(u,hy,N,M):
	new_u = u.copy()#numpy.zeros(u.shape)
	for i in range(1, N - 1):
		for j in range(1, M - 1):
			new_u[i,j] = (u[i+1,j] - 2* u[i,j] + u[i-1,j]) / (hy*hy)
	if approxUVbound is True:
		new_u[0,:] = (u[1,:] - u[0,:])/(hy)
		new_u[-1,:] = (-u[-2,:] + u[-1,:])/(hy)
	return new_u
