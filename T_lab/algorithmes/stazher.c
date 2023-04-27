#include <stdio.h>

int main() {
    int s = 0; // the number of trainees on the 26th floor
    int k; // the number of trainees on the 26th floor after Masha's first day of hiring
    
    printf("Enter the number of trainees on the 26th floor: ");
    scanf("%d", &s);
    
    for (k = 1; k <= 10; k++) {
        // simulate the first two days of hiring
        int total_trainees = 7 + k + s;
        int remaining_trainees = 28 - total_trainees;
        int anya_trainees = remaining_trainees / 2;
        int masha_trainees = remaining_trainees - anya_trainees;
        total_trainees += anya_trainees;
        
        // simulate the third day of hiring by Masha
        total_trainees += k + 1;
        
        if (total_trainees >= 28) {
            printf("Masha can win with k = %d\n", k);
            return 0;
        }
    }
    
    printf("Masha cannot win\n");
    return 0;
}
