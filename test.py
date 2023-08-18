import random2 as rd
import matplotlib.pyplot as plt

def randomAnswers(n):
    a = []
    for _ in range(n):
        a.append(round(rd.random()))
    return a

def getInitialProbs(q, b, s, g, levels):
    probs = []
    for j in range(levels, 0, -1):
        qt = (j / levels)**1
        ft = list(map(lambda i: (6-i)**(5**(-b)), q))
        phi = list(
            map(
                lambda i: qt*((1-g)*(1-b)**i + (b*s)**i),
                ft
                )
            )
        probs.append(phi)
    return probs

def getInitialLikes(q, a, b, s, g, levels):
    likes = []
    probs = getInitialProbs(q, b, s, g, levels)
    for j in range(levels):
        p = 1
        for i in range(len(q)):
            if a[i]:
                p *= probs[j][i]
            else:
                p *= 1 - probs[j][i]
        likes.append(p)
    return likes

def getLikelyhood(q, a, b, s, g, qt):
    ft = list(map(lambda i: (6-i)**(5**(-b)), q))
    phi = list(
        map(
            lambda i: qt[i]*((1-g)*(1-b)**ft[i] + (b*s)**ft[i]),
            range(len(q))
            )
        )
    p = 1
    for i in range(len(q)):
        if a[i]:
            p *= phi[i]
        else:
            p *= 1 - phi[i]
    return p

def getQfromPhi(q, b, s, g, phis):
    ft = list(map(lambda i: (6-i)**(5**(-b)), q))
    qs = list(
        map(
            lambda i: phis[i] / ((b*s)**ft[i] + (1-g)*(1-b)**ft[i]),
            range(len(q))
            )
        )
    return qs

def EM(q, b, s, g, k, ans, alpha=1, beta=1, iters=15):
    mean_q = []
    for i in range(len(q[0])):
        mean_q.append(sum(map(lambda v: v[i]/len(q), q)))
    mean_b = sum(b) / len(b)
    tn = len(ans[0])
    L_sj = [0] * len(ans)
    z_sj = [0] * len(ans)
    q_tj = []
    for j in range(k):
        qj = []
        for t in range(tn):
            qj.append((rd.random()+j)/k)
        q_tj.append(qj)
    p_j = [1/k] * k
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
        
nq = 10
groups = 3
q = []
a = []
b = []
for i in range(1000):
    q.append(list(map(lambda _: 3, range(nq))))
    a.append(randomAnswers(nq))
    b.append(0.8)
s = 0.1
g = 0.25

p, qs = EM(q, b, s, g, groups, a, 1, 1, 15)

def ploting(groups, nq, p, qs):
    plt.figure()
    plt.subplot(3,3,1)
    plt.bar(range(groups), p)
    for i in range(groups):
        plt.subplot(3,3,i+2)
        plt.plot(range(nq), qs[i])
    plt.show()

ploting(groups, nq, p, qs)