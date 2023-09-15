clear, clc
p = linspace(1,5,5);
x = linspace(0.5,5.5,1000);
b = 0.1:0.06:0.34;
a = 0.08:0.04:0.24;
m = 0.05:0.05:0.25;
figure; hold on;
for i=1:5
    y = @(x) b(i) + m(i).*log(x);
    plot(x, y(x),"b--")
    plot(p, y(p), "ro", 'MarkerSize', 8, 'MarkerFaceColor','r');
end
ax = gca;
ax.XGrid = 'off';
ax.YGrid = 'on';
xticks(p);
yticks(0:0.1:1);
ylim([0 1]);
xlabel("Difficulty");
ylabel("Probability");
title("Logarithmic curve");
figure; hold on;
for i=1:5
    y = @(x) a(i)*exp(m(i)*x);
    plot(x, y(x),"b--")
    plot(p, y(p), "ro", 'MarkerSize', 8, 'MarkerFaceColor','r');
end
ax = gca;
ax.XGrid = 'off';
ax.YGrid = 'on';
xticks(p);
yticks(0:0.1:1);
ylim([0 1]);
xlabel("Difficulty");
ylabel("Probability");
title("Exponential curve");