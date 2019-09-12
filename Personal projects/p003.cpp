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

long long largestDisvisiblePrime(long long n, long long currentI){
  std::cout<<n<<'\n';
  for (long long i = currentI; i <= n; i++) {
    std::cout<<i;
    if (n%i==0) {
      std::cout<<'\t'<<i;
      std::cin.get();
      largestDisvisiblePrime(n/i, i);
      break;
    }
    std::cout<<'\n';
  }
  return n;
}

int main()
{
    long long number = 600851475143;
    long long startI = 2;
    std::cin.get();
    std::cout<<largestDisvisiblePrime(number, startI)<<'\n';
    std::cout<<"Result is two numbers ago +1. 6857 for 600851475143";
    return 0;
}
