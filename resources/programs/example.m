a = 1;
for(i = 1:15) {
    a *= 2;
    if (a > 1000) {
        b = 10;
        print(a);
    } else {
        print(42);
    }
}