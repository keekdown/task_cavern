import numpy as np
from numpy import linalg as LA

def puasson(A,u,f,EPS):
	_u = u.copy()
	r = A(u) - f
	norm_r_0 = LA.norm(r)
	norm_r_N = norm_r_0
	count = 0
	while(norm_r_N/norm_r_0 > EPS):
		r = A(u) - f
		tau = innermultiply(A(r),r) / innermultiply(A(r),A(r))
		u = _u - tau * r
		_u = u.copy()
		norm_r_N = LA.norm(r)
		count += 1
		print(count)
	return u
	
def innermultiply(m1,m2):
	sizeM1 = m1.shape[0]
	sizeM2 = m2.shape[0]
	temp = 0
	for i in range(1,sizeM1 - 1):
		for j in range(1,sizeM2 - 1):
			temp += m1[j,i]*m2[j,i]
	return temp

	
