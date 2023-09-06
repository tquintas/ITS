from create_questions import *
import matplotlib.pyplot as plt

def getLikelyhood(qt, vt):
    p = 1
    for i in range(len(vt)):
        if vt[i]:
            p *= qt[i]
        else:
            p *= 1 - qt[i]
    return p

def EM(k, a, b, iters=50, students=100):
    v = []
    T = 10
    for _ in range(students):
        vs = []
        for __ in range(T):
            vs.append(round(rd.random()))
        v.append(vs)
    L_sj = [0] * len(v)
    z_sj = [0] * len(v)
    q_tj = []
    for j in range(k):
        qj = []
        for t in range(T):
            qj.append((rd.random()+j)/k)
        q_tj.append(qj)
    p_j = [1/k] * k
    for _ in range(iters):
        for stu in range(len(v)):
            Ls = []
            for j in range(k):
                Ls.append(p_j[j] * getLikelyhood(q_tj[j], v[stu]))
            L_sj[stu] = Ls
        for stu in range(len(v)):
            zs = []
            sumL = sum(L_sj[stu])
            for j in range(k):
                zs.append(L_sj[stu][j] / sumL)
            z_sj[stu] = zs
        for j in range(k):
            qj = []
            den = a + b - 2 + sum(map(lambda stu: z_sj[stu][j], range(len(v))))
            for t in range(T):
                num = a - 1 + sum(map(lambda stu: z_sj[stu][j]*v[stu][t], range(len(v))))
                qj.append(num/den)
            q_tj[j] = qj
        for j in range(k):
            num = sum(map(lambda stu: z_sj[stu][j], range(len(v))))
            den = sum(map(lambda v: sum(v), z_sj))
            p_j[j] = num/den
    return p_j, q_tj

def t_its(n=1000):
    t = []
    for _ in range(n):
        t.append(round(rd.random()-0.2))
    r = sum(t)
    y = []
    dec = 10
    x = list(map(lambda i: i/dec, range(1*dec,100*dec)))
    for p in x:
        ss = 0
        for i in range(n):
            ss += t[i] * (1-(1/p))**(n-i-1) * (1/p)
        y.append(ss)
    print(r)
    print(t)
    return x,y

for _ in range(1):
    x,y = t_its(10)
    plt.plot(x,y)
plt.show()