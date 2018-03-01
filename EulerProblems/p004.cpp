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
        return false
      }
    }
    return true
}

int main()
{
    std::cout << checkPalindrome(313) << std::endl;
    return 0;
}
