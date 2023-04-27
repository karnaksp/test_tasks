#include <stdio.h>

int main() {
    // Probability of getting a problem right
    double p = 0.8;
    
    // Number of initial problems
    int n = 15;
    
    // Expected value of number of problems before first failure
    double q = 1.0 - p;
    double k = 1.0 / q;
    
    // Expected value of number of additional problems per failure
    double m = 2.0;
    
    // Expected value of number of failures
    double f = k * q / p;
    
    // Expected value of total number of problems
    double x = n + f * m;
    
    printf("Expected value of total number of problems: %f\n", x);
    
    return 0;
}
