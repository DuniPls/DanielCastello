/******************************************************************************

                              Online C++ Compiler.
               Code, Compile, Run and Debug C++ program online.
Write your code in this editor and press "Run" button to compile and execute it.

*******************************************************************************/
/*
The prime factors of 13195 are 5, 7, 13 and 29.

What is the largest prime factor of the number 600851475143 ?
*/

#include <iostream>
#include <math.h>

int main()
{
    long currentSquareSum=0;
    long currentSumSquare=0;
    int max=100;

    for(int i = 1; i<=max; i++){
        currentSquareSum += pow(i, 2);
    }
    for(int i = 1; i<=max; i++){
        currentSumSquare += i;
    }
    currentSumSquare = pow(currentSumSquare, 2);
    std::cout<<currentSquareSum<<'\t'<<currentSumSquare<<'\n';
    std::cout<<currentSumSquare-currentSquareSum;
    return 0;
}
