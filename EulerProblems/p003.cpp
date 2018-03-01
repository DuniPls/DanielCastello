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

bool multipleOfA(int number, int a){
    int multiple = a;
    int n=0;
    float m=0;
    float difference=0;
    n=number/float(multiple);
    m=number/float(multiple);
    difference=m-float(n);
    if(difference==0){return true;}
    return false;
}

int largestDisvisiblePrime(int n){
  for (int i = 2; i < n; i++) {
    if (multipleOfA(n, i)) {
      largestDisvisiblePrime(n/i);
    }
  }
  return n;
}

int main()
{
    int number = 600851475143;
    std::cout<<largestDisvisiblePrime(number);
    return 0;
}
