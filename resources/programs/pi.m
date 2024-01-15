pi = 0.0;
n = 1.0;
for(i = 1:100000) {
    pi += 4.0 / n;
    div = n + 2.0;
    pi -= 4.0 / div;
    n += 4.0;
}
print(pi);