import matplotlib.pyplot as plt
import math as _m

def sigma(b,n):
    return ((b*(1-b))/(n+1))**0.5

def u(b,n,z):
    return b + z*sigma(b,n)

def upper(mu,sig,eps):
    return mu - (sig/eps)

def F(x,mu,sig,eps):
    s = (x-mu)/sig
    if eps == 0:
        return _m.exp(-_m.exp(-s))
    else:
        if s*eps > -1:
            return _m.exp(-(1+s*eps)**(-1/eps))
        else:
            if eps > 0:
                return 0
            else:
                return 1

x = [i / 1000 for i in range(1, 1000)]
learn = []
n = 25
z = 1.2
for i in x:
    mu = u(i,n,z)
    sig = sigma(i,n)
    up = upper(mu,sig,n)
    learn.append(F(1-i,mu,sig,n))
plt.plot(x,learn)
plt.show()