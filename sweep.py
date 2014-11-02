import numpy as np
class Sweep:
	def __init__(self,a,b,c,f):
		self._a = a
		self._b = b
		self._c = c
		self._f = f
		self._alpha= np.zeros(a.size + 1)
		self._betta = np.zeros(a.size + 1)
		self._u = np.zeros(a.size + 2)
		
	def solve(self,bound0,bound1):
		self._alpha[0] = 0
		self._betta[0] = bound0
		#print(self._u.size)
		for i in range(0, self._alpha.size - 1):
			self._alpha[i+1] = self._b[i] / (self._c[i] - self._a[i] * self._alpha[i])
			self._betta[i+1] = (self._a[i] * self._betta[i] + self._f[i]) / (self._c[i] - self._a[i] * self._alpha[i])
		#print(self._betta)
		#print(self._alpha)
		self._u[-1] = bound1
		#print(len(self._u))
		#print(self._u[self._u.size - 1])
		for i in reversed(range(0,self._u.size - 1)):
			#print(self._u)
			self._u[i] = self._alpha[i] * self._u[i+1] + self._betta[i]
		self._u[0] = bound0
		return self._u.copy()[1:-1]
