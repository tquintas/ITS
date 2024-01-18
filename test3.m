clear, clc
n = 6;
V = ff2n(n);
A = V'*V;
disp(A)

B = eye(n) + ones(n,n);
disp(2^(n-2)*B)