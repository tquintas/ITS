import random2 as rd
import matplotlib.pyplot as plt
from scipy import stats

def randomAnswers(n):
    a = []
    for _ in range(n):
        a.append(round(rd.random()))
    return a

def getLikelyhood(qt, vt):
    p = 1
    for i in range(len(vt)):
        if vt[i]:
            p *= qt[i]
        else:
            p *= 1 - qt[i]
    return p

def getPriorQ(qs, bs, g, s):
    alphas = []
    betas = []
    c = len(qs)
    def getPs(b):
        if b < 0.05:
            return g
        elif b > 0.95:
            return s
        else:
            m = (s - g) / 0.9
            i = s - 0.95*m
            return m*b + i
    ps = list(map(getPs, bs))
    p = 1
    for i in range(c):
        alpha = ps[i] * qs[i]
        alphas.append(alpha)
        beta = (1-ps[i]) * qs[i]
        betas.append(beta)
        p *= stats.beta.pdf(getPs(bs[i]), alpha, beta)
    return p, alphas, betas

def EM(qs, bs, g, s, groups, vs, iters=15):
    T = len(qs[0])
    S = len(qs)
    L_sj = [0] * S
    z_sj = [0] * S
    q_tj = []
    alphas_t = []
    betas_t = []
    
    for s in range(S):
        p, alphas, betas = getPriorQ(qs[s], bs[s], g, s)

    for j in range(groups):
        qj = []
        for t in range(T):
            qj.append((rd.random()+j)/k)
        q_tj.append(qj)
    p_j = [1/groups] * groups
    for _ in range(iters):
        for stu in range(len(ans)):
            Ls = []
            for j in range(k):
                Ls.append(p_j[j] * getLikelyhood(q[stu], ans[stu], b[stu], s, g, q_tj[j]))
            L_sj[stu] = Ls
        for stu in range(len(ans)):
            zs = []
            sumL = sum(L_sj[stu])
            for j in range(k):
                zs.append(L_sj[stu][j] / sumL)
            z_sj[stu] = zs
        for j in range(k):
            qj = []
            den = alpha + beta - 2 + sum(map(lambda stu: z_sj[stu][j], range(len(ans))))
            for t in range(tn):
                num = alpha - 1 + sum(map(lambda stu: z_sj[stu][j]*ans[stu][t], range(len(ans))))
                qj.append(num/den)
            q_tj[j] = getQfromPhi(mean_q, mean_b, s, g, qj)
        for j in range(k):
            num = alpha + beta - 2 + sum(map(lambda stu: z_sj[stu][j], range(len(ans))))
            den = sum(map(lambda v: sum(v), z_sj))
            p_j[j] = num/den
    return p_j, q_tj

def ploting(groups, nq, p, qs):
    plt.figure()
    plt.subplot(3,3,1)
    plt.bar(range(groups), p)
    for i in range(groups):
        plt.subplot(3,3,i+2)
        plt.plot(range(nq), qs[i])
    plt.show()