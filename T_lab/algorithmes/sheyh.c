#include <stdio.h>
#include <math.h>

int main() {
    int num_jewelry = 8;
    int num_choices = 9;  // 0, 1, 2, or 3 pieces for each wife, or not buying any
    int num_subsets = pow(2, num_jewelry);
    int num_satisfying = 0;

    // Iterate over all possible choices of jewelry
    for (int i = 0; i < pow(num_choices, num_jewelry); i++) {
        int choice = i;
        int counts[3][num_jewelry];
        for (int j = 0; j < num_jewelry; j++) {
            // Decode the current choice of jewelry
            int count = choice % num_choices;
            counts[0][j] = count;
            choice /= num_choices;
            // Propagate the counts to the other wives
            counts[1][j] = counts[2][j] = count;
            if (count == 1) {
                counts[1][j] = 0;
                counts[2][j] = 1;
            }
        }
        // Iterate over all possible subsets of jewelry
        for (int j = 0; j < num_subsets; j++) {
            int subset = j;
            int valid = 1;
            int parity = -1;
            for (int k = 0; k < num_jewelry; k++) {
                // Check if the current type of jewelry is in the subset
                if (subset % 2 == 1) {
                    // Check if the counts satisfy the wives' preferences
                    if (counts[0][k] == 1 && (counts[1][k] != 0 || counts[2][k] != 1)) {
                        valid = 0;
                        break;
                    }
                    if (counts[1][k] != counts[2][k]) {
                        if (parity == -1) {
                            parity = counts[1][k] < counts[2][k] ? 0 : 1;
                        } else if (counts[1][k] < counts[2][k] != parity) {
                            valid = 0;
                            break;
                        }
                    }
                }
                subset /= 2;
            }
            if (valid) {
                num_satisfying++;
            }
        }
    }
    printf("Number of ways satisfying wives' preferences: %d\n", num_satisfying);
    return 0;
}
