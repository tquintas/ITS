clear, clc

iter = 10000;
step = 0.01;

gym = [];
for i = 1:20
    gym(i) = round(rand(1));
end
xn = .5:step:length(gym);
start = .5/step;
for i = 1:length(xn)
    yn(i) = gym(floor((xn(i) - .5)) + 1);
end

hold on
plot(xn,yn,'o')

B = [5; 0];

% y = 0.5 * sen((2π/T) * x + B) + 0.5
% dy/dA = sen((2π/T) * x + B))
% dy/dT = A * (2π/T^2) * x * cos((2π/T) * x + B)
% dy/dB = A * (2π/T) * cos((2π/T) * (x - B))
% dy/dC = 1

for i = 1:iter
    J = zeros(length(yn), 2);
    r = zeros(length(yn), 1);
    for row = 1:length(yn)
        xk = xn(row);
        J(row, 1) = -(pi/(B(1)^2)) * xk * cos((2*pi/B(1)) * xk - B(2));   
        J(row, 2) = -cos((2*pi/B(1)) * xk - B(2));   
        r(row) = yn(row) - (0.4 * sin((2*pi/B(1)) * xk - B(2)) + 0.5);
    end
    delta = (J'*J)\(J'*r);   
    B = B + delta;
end

x = 0:.01:length(gym);

y = 0.4 * sin((2*pi/B(1)) * x - B(2)) + 0.5;

plot(x,y)