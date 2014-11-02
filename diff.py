import numpy

def dx(u,out):
	h = 1.0/u.shape[0]
	new_u = out.copy()#numpy.zeros(u.shape)
	for row in range(1, u.shape[0] - 1):
		for col in range(1, u.shape[1] - 1):
			new_u[row,col] = (u[row+1,col] - u[row-1,col]) / (2*h);
	#~ new_u[-1] = (u[-2] - u[-1]) / 2*h
	return new_u

def dy(u,out):
	h = 1.0/u.shape[1]
	new_u = out.copy()#numpy.zeros(u.shape)
	for row in range(1, u.shape[0] - 1):
		for col in range(1, u.shape[1] - 1):
			new_u[row,col] = (u[row,col + 1] - u[row,col - 1]) / (2*h)
	#~ new_u[0:u.shape[0],-1] = (u[0:u.shape[0],-2] - u[0:u.shape[0],-1]) / 2*h
	return new_u
	
def d2x(u):
	h = 1.0/u.shape[0]
	new_u = u.copy()#numpy.zeros(u.shape)
	for row in range(1, u.shape[0] - 1):
		for col in range(1, u.shape[1]):
			new_u[row,col] = (u[row+1,col] - 2*u[row,col] + u[row-1,col]) / h*h
	#~ new_u[-1] = (u[-2] - u[-1]) / 2*h
	#~ new_u[0]  = (u[1]  - u[0])  / 2*h
	return new_u
	
def d2y(u):
	h = 1.0/u.shape[1]
	new_u = u.copy()#numpy.zeros(u.shape)
	for row in range(0, u.shape[0]):
		for col in range(1, u.shape[1] - 1):
			new_u[row,col] = (u[row,col + 1] - 2*u[row,col] + u[row,col-1]) / h*h
	#~ new_u[0:u.shape[0],-1] = (u[0:u.shape[0],-2] - u[0:u.shape[0],-1]) / 2*h
	#~ new_u[0:u.shape[0],0] = (u[0:u.shape[0],1] - u[0:u.shape[0],0]) / 2*h
	return new_u

def d(u):
	h = 1.0/u.size
	new_u = u.copy()#numpy.zeros(u.shape)
	for i in range(1, u.size - 1):
		new_u[i] = (u[i+1] - u[i - 1]) / (2*h)
	#~ new_u[-1] = (new_u[-2] - new_u[-1]) / 2*h
	return new_u
	
def d2(u):
	h = 1.0/u.size
	new_u = u.copy()#numpy.zeros(u.shape)
	for i in (range(1, u.size - 1)):
		new_u[i] = (u[i+1] - 2* u[i] + u[i-1]) / h*h
	#~ new_u[-1] = (new_u[-2] - new_u[-1]) / 2*h
	#~ new_u[0]  = (new_u[1] - new_u[0]) / 2*h
	return new_u
	
