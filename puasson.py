import numpy as np
from numpy import linalg as LA
class TaskPuasson:
	def __init__(self,A,u,f):
		self._A = A
		self._u = u
		self._f = f
		self._newU = u.copy()
		self._sizenew = 0
		self._normu0 = LA.norm(self._A(self._u) - self._f)
		self._normu  = self._normu0
		
	def solve(self,eps):
		sizex = self._u[0].size
		sizey = self._u[0:(self._u[0].size),0:1].size
		count = 0
		r = np.zeros((self._u.shape[0],self._u.shape[1]))
		N = self._u.shape[0]
		while(self._normu / self._normu0 > eps):
			r = self._A(self._u) - (self._f)
			r[0],r[N - 1],r[0:N,N-1:N],r[0:N,0:1] = (0,0,0,0)
			tau = float((np.dot(self.cutBounds(self._A(r)).reshape(self._sizenew), self.cutBounds(r).reshape(self._sizenew)))) / \
				  float((np.dot(self.cutBounds(self._A(r)).reshape(self._sizenew),self.cutBounds(self._A(r)).reshape(self._sizenew))))
			count += 1
			#~ r.shape = ((sizex,sizey))
			#~ self._u = self._u - tau * r
			self.calc(tau,r)
			#print(count)
			#~ if count % 100 == 0:
				#~ print(self._u)
			self._normu = LA.norm(self.cutBounds(r))
		return self._u.copy()
		
	def calc(self,tau,r):
		for j in range(1, self._u.shape[0] - 1):
			for i in range(1, self._u.shape[1] - 1):
				self._newU[j,i] = self._u[j,i] - tau*r[j,i]
		self._u = self._newU.copy()
				
	def cutBounds(self,u):
		new_u = u.copy()
		new_u = new_u[1:]#cut up
		new_u = new_u[0:,1:]#cut left
		new_u = new_u[0:-1]#cut down
		new_u = new_u[0:,0:-1]
		self._sizenew = new_u.size
		return new_u

