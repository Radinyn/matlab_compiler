for(x = 1:9) {
    sqrt_x = 1.0;
    for (i = 1:10000) {
        numerator = sqrt_x + x / sqrt_x;
        sqrt_x = numerator / 2;
    }
    print(sqrt_x);
}
