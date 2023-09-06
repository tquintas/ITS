clear, clc

Td = 0.5;
Te = 0.32;
b = 0.08;
bv = 0.42;
n = 32;
ns = 24;
tp = 82;
t = 80;
t_u = 60;
t_s = 20;
t_z = (t - t_u) / t_s;
tp_u = 60;
tp_s = 20;
tp_z = (tp - tp_u) / tp_s;
s = 0.35;

P = exp(-b / (0.01 * n));
L = exp(1-n^b);
R = Te^bv;
S = (1 - exp(-tp_z^2))^s;
D = Td^abs(s-0.5);
B = 1 - exp(-(t_z * (ns/50 + 1))^2);

De = [P L R S D B];
De = De(De > 0.25);
u = mean(De);
sigma = std(De);
t = tinv(0.95, length(De)-1);
Up = u + t*sigma/sqrt(length(De));
Lw = u - t*sigma/sqrt(length(De));
Decision = (De > Up);

x = linspace(30,90,1000);
plot(x,gevcdf(x,s,tp_s,tp_u));
