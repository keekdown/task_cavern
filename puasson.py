import numpy as np
from numpy import linalg as LA
from params import *
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
		count = 0
		r = np.zeros((self._u.shape[0],self._u.shape[1]))
		N = self._u.shape[0]
		while(self._normu / self._normu0 > eps):
			r = self._A(self._u) - (self._f)
			r[0],r[N - 1],r[:,-1],r[:,0] = (0,0,0,0)
			_r = r[1:-1,1:-1]
			Ar = self._A(r)[1:-1,1:-1]
			a = float(np.dot(Ar.reshape(Ar.size),_r.reshape(_r.size)))
			b = float(np.dot(Ar.reshape(Ar.size),Ar.reshape(Ar.size)))
			tau =  a / b
			count += 1
			self._u[1:-1,1:-1] = self._u[1:-1,1:-1] - tau * r[1:-1,1:-1]
			self._normu = LA.norm(r)
		return self._u.copy()
