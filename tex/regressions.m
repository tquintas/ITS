clear, clc
p = sort(rand(5,1));
v = std(p)*length(p);
x = 1:5;
xx = linspace(0,6,1000);


D = [ones(5,1), x'-1];
A = D'*D;
y = D'*log(p);
b = A\y;
f = @(x) exp(b(1) + b(2)*(x-1));
r = p - f(x');
r = r'*r;
r2 = 1 - r/v;
k = (-1/4) * b(1);
b_n = b(2) / k;


Dl = [ones(5,1), log(x)'];
Al = Dl'*Dl;
yl = Dl'*p;
bl = Al\yl;
fl = @(x) bl(1) + bl(2)*log(x);
rl = p - fl(x');
rl = rl'*rl;
rl2 = 1 - rl/v;
kl = (1-bl(1))/log(5);
bl_n = bl(2) / kl;




tiledlayout(1,2);
nexttile;
plot(xx, f(xx), "b--", x, p, "ro");
title(sprintf("y = %fe^{%f(x - 1)}", exp(b(1)), b(2)));
ylim([0 1]);
xlim([0 6]);
nexttile;
plot(xx, fl(xx), "b--", x, p, "ro");
title(sprintf("y = %f + %f·ln(x)", bl(1), bl(2)));
ylim([0 1]);
xlim([0 6]);
