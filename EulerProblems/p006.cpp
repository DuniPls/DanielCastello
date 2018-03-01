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

int checkNumberOfDigits(int number){
    for (int i=7;i>0;i--) {
        if(number/(pow(10, i)) >= 1){return (i+1);}
    }
    return 1;
}

bool isPrime(long * myPrimes, long n){

}

bool checkPalindrome(int number){
    int numberOfDigits=checkNumberOfDigits(number);
    int * arr;
    arr = new int [numberOfDigits];
    for (int i = 0; i < numberOfDigits; i++) {
      int currentDigit = number / (pow(10, (numberOfDigits - i - 1)));
      number-=currentDigit * (pow(10, (numberOfDigits - i - 1)));
      arr[i]= currentDigit;
    }
    for (int i = 0; i < numberOfDigits; i++) {
      if (arr[i]!=arr[numberOfDigits - i - 1]) {
        return false;
      }
    }
    return true;
}

int main()
{
    /*int currentMax = 0;
    //std::cout << checkPalindrome(3165613) << std::endl;
    for(int i = 999; i > 800; i--){
        for(int j = 999; j > 800; j--){
            if(checkPalindrome(i*j) && (i*j > currentMax)){
                currentMax = i*j;
                break;
            }
        }
    }
    std::cout<<currentMax;*/

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
