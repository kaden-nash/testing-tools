#include <stdio.h>

int main () {
    char str[50];
    int res = 0;
    int count = 0;

    while (count < 3 && res != EOF) {

        if (count == 0)
            printf("a\nangel\n");
        
        if (count == 1)
            printf("\n");

        if (count == 2)
            printf("a\n");
        

        // res = scanf("%s", str);
        printf("\n", str);
        ++count;
    }
}
