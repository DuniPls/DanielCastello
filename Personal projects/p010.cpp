/*
The sum of the primes below 10 is 2 + 3 + 5 + 7 = 17.

Find the sum of all the primes below two million.
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
    if (myPrimes[i] * myPrimes[i] > n) {
      break;
    }
  }
  return true;
}

long long unsigned returnVectorSum(std::vector<int>& v){
  long long unsigned sum=0;
  for (size_t i = 0; i < v.size(); i++) {
    sum+=v[i];
  }
  return sum;
}

int main()
{
  std::vector<int> primes;
  primes.push_back(2);
  primes.push_back(3);

  for (int i = 1; (6*i)+1<2000000; i++) {
    if (isPrime(primes, (6*i)-1)) {
      primes.push_back((6*i)-1);
    }
    if (isPrime(primes, (6*i)+1)) {
      primes.push_back((6*i)+1);
    }
  }
  printIntArray(primes);
  std::cout <<'\n' << returnVectorSum(primes) << '\n';
  return 0;
}
