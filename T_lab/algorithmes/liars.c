#include <stdio.h>

int graph[9][4] = {{1, 3, -1, -1}, {0, 2, 4, -1}, {1, 5, -1, -1}, {0, 4, 6, -1}, {1, 3, 5, 7}, {2, 4, 8, -1}, {3, 7, -1, -1}, {4, 6, 8, -1}, {5, 7, -1, -1}};

int count_bits(int n) {
    int count = 0;
    while (n) {
        count++;
        n &= (n - 1);
    }
    return count;
}

void print_solution(int bits) {
    int arrangement[9], knights[9], liars[9];
    for (int i = 0; i < 9; i++) {
        arrangement[i] = (bits >> i) & 1;
    }
    int num_knights = 0, num_liars = 0;
    for (int i = 0; i < 9; i++) {
        if (arrangement[i]) {
            knights[num_knights++] = i + 1;
        } else {
            liars[num_liars++] = i + 1;
        }
    }
    int consistent = 1;
    for (int i = 0; i < 9; i++) {
        int neighbors[4], num_neighbors = 0;
        for (int j = 0; j < 4 && graph[i][j] >= 0; j++) {
            neighbors[num_neighbors++] = graph[i][j];
        }
        int liars_count = 0, knights_count = 0;
        for (int j = 0; j < num_neighbors; j++) {
            int neighbor = neighbors[j] - 1;
            if (!arrangement[neighbor]) {
                liars_count++;
            } else {
                knights_count++;
            }
        }
        if (arrangement[i] && liars_count >= knights_count) {
            consistent = 0;
            break;
        } else if (!arrangement[i] && liars_count < knights_count) {
            consistent = 0;
            break;
        }
    }
    if (consistent) {
        printf("Knights: ");
        for (int i = 0; i < num_knights; i++) {
            printf("%d ", knights[i]);
        }
        printf("\nLiars: ");
        for (int i = 0; i < num_liars; i++) {
            printf("%d ", liars[i]);
        }
        printf("\nProduct: %d\n", num_knights * num_liars);
    }
}

int main() {
    for (int i = 0; i < (1 << 9); i++) {
        if (count_bits(i) == 4) {
            print_solution(i);
        }
    }
    return 0;
}
