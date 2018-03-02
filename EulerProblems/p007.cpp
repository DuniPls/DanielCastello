/******************************************************************************

                              Online C++ Compiler.
               Code, Compile, Run and Debug C++ program online.
Write your code in this editor and press "Run" button to compile and execute it.

*******************************************************************************/
/*
By listing the first six prime numbers: 2, 3, 5, 7, 11, and 13, we can see that the 6th prime is 13.

What is the 10 001st prime number?
*/

#include <iostream>
#include <vector>
#include <math.h>

void printIntArray(std::vector<int>& v) {
  for (int i = 0; i < v.size(); i++) {
    std::cout << v[i] << " ";
  }
  std::cout << '\n';
}

bool isPrime(std::vector<int>& myPrimes, long n){
  if(n == 0){return false;}
  for (int i = 0; i < myPrimes.size(); i++) {
    if (n%myPrimes[i]==0) {
      return false;
    }
  }
  return true;
}

int main()
{
  std::vector<int> primes;
  primes.push_back(2);

  for (size_t i = 3; primes.size() < 10001; i++) {
    if (isPrime(primes, i)) {
      primes.push_back(i);
    }
  }
  printIntArray(primes);
  return 0;
}
