clear, clc

belief = [0.46 0.15 0.27 0.33 0.45 0.39]';
questions = [
    1 0
    1 0 
    0 1
    1 0
    1 0
    0 1
];

N = length(belief);
diffs = size(questions, 2);

n = (ones(1, N) * questions);

u = (belief' * questions) ./ n;

xi = (belief * ones(1, diffs) - (ones(N,1) * u)) .* questions;

vars = diag((xi'*xi) ./ (n - ones(1, diffs)))';

term = u .* (ones(1, diffs) - u) ./ vars - ones(1, diffs);

a = u .* term;
b = (ones(1, diffs) - u) .* term;


