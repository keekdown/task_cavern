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
		if bound0 == 0 and bound1 == 0:
			return -1*((self._u.copy())[::-1])
		else:
			return (self._u.copy())

def TDMA(a,b,c,f):
    #a, b, c, f = map(lambda k_list: map(float, k_list), (a, b, c, f))
 
    alpha = [0]
    beta = [0]
    n = len(f)
    x = [0] * n
 
    for i in range(n-1):
        alpha.append(-b[i]/(a[i]*alpha[i] + c[i]))
        beta.append((f[i] - a[i]*beta[i])/(a[i]*alpha[i] + c[i]))
 
    x[n-1] = (f[n-1] - a[n-2]*beta[n-1])/(c[n-1] + a[n-2]*alpha[n-1])
 
    for i in reversed(range(n-1)):
        x[i] = alpha[i+1]*x[i+1] + beta[i+1]
 
    return x
