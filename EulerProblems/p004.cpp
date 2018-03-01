/******************************************************************************

                              Online C++ Compiler.
               Code, Compile, Run and Debug C++ program online.
Write your code in this editor and press "Run" button to compile and execute it.

*******************************************************************************/
/*
A palindromic number reads the same both ways. The largest palindrome made from the product of two 2-digit numbers is 9009 = 91 × 99.

Find the largest palindrome made from the product of two 3-digit numbers.
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
        return false;
      }
    }
    return true;
}

int main()
{
  int i=999;
  int j=999;
  for (i=999; i > 900; i--) {
    for (j=999; j > 900; j--) {
      if (checkPalindrome(i*j)) {
        std::cout<<i*j<<'\t'<<i<<'\t'<<j<<'\n';
      }
    }
  }
    return 0;
}
