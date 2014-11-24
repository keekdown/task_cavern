import numpy

def dx(u,out):
	h = 1.0/u.shape[0]
	new_u = out.copy()
	for i in range(1, u.shape[0] - 1):
		for j in range(0, u.shape[1]):
			new_u[i,j] = (u[i+1,j] - u[i-1,j]) / (2*h);
	new_u[0,:] = (u[1,:] - u[0,:])/(2*h)
	new_u[-1,:] = (u[-1,:] - u[-2,:])/(2*h)
	return new_u

def dy(u,out):
	h = 1.0/u.shape[1]
	new_u = out.copy()#numpy.zeros(u.shape)
	for i in range(0, u.shape[0]):
		for j in range(1, u.shape[1] - 1):
			new_u[i,j] = (u[i,j+1] - u[i,j-1]) / (2*h)
	new_u[:,0] = (u[:,1] - u[:,0])/(2*h)
	new_u[:,-1] = (u[:,-1] - u[:,-2])/(2*h)
	return new_u
	
def d(u):
	h = 1.0/u.size
	new_u = u.copy()#numpy.zeros(u.shape)
	for i in range(1, u.size - 1):
		new_u[i] = (u[i+1] - u[i - 1]) / (2*h)
	new_u[0] = (u[1] - u[0])/(2*h)
	new_u[-1] = (u[-1] - u[-2])/(2*h)
	return new_u
	
def d2(u):
	h = 1.0/u.size
	new_u = u.copy()#numpy.zeros(u.shape)
	for i in range(1, u.size - 1):
		new_u[i] = (u[i+1] - 2* u[i] + u[i-1]) / (h*h)
	new_u[0] = (u[1] - u[0])/(2*h)
	new_u[-1] = (u[-1] - u[-2])/(2*h)
	return new_u

