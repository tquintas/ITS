p = [0.1, 0.7, 0.6, 0.2, 0.5, 0.9]
a = [False, False, True, True, True, True]
s = 0
r = 0

for i in range(len(a)):
    r += p[i]
    if a[i]:
        s += p[i]

per = s / r

print(per)