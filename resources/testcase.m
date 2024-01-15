A = zeros(4);
B = eye(4);
u = [1.0, 2.0, 3.0, 4.0, 5.0];
v = A * u;


# A + B;
# A - B;
# A * B;
# D4 = A / B; # Should fail since the division operation on two 4x4 matrices makes no sense
# A .+ B;
# A .- B;
# A .* B;
# A ./ B;
# A == B;
# A != B;