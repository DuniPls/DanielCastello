

/*2520 is the smallest number that can be divided by each of the numbers from 1 to 10 without any remainder.

What is the smallest positive number that is evenly divisible by all of the numbers from 1 to 20?*/

#include <iostream>
#include <vector>
#include <math.h>


void printIntArray(std::vector<int>& v) {
  for (int i = 0; i < v.size(); i++) {
    std::cout << v[i] << " ";
  }
  std::cout << '\n';
}

bool isFactor(int number, int factor){
  if(factor!=0){
    if (number%factor==0) {
      return true;
    }
  }
  return false;
}

std::vector<int> returnFactors(int n){
  std::vector<int> f;
  int currentN = n;
  for (int i = 2; i < n; i++) {
    if (isFactor(currentN,i)) {
      f.push_back(i);
      currentN = currentN/i;
      i--;
    }
  }
  if (f.size()==0) {
    f.push_back(n);
  }
  return f;
}

int main()
{
  int max = 20;
  std::vector<int> currentFactors;
  currentFactors.push_back(2);

  std::vector<int> currentFactorsCopy;
  std::vector<int> arrCopy;

  for (int i = 3; i <= max; i++) {

    std::vector<int> arr = returnFactors(i);
    printIntArray(currentFactors);
    currentFactorsCopy = currentFactors;
    arrCopy = arr;
    for (int j = 0; j < arrCopy.size(); j++) {
      for (int k = 0; k < currentFactorsCopy.size(); k++) {
        if (arrCopy[j]==currentFactorsCopy[k]) {
          std::cout << "Erased " << arrCopy[j] <<'\n';
          currentFactorsCopy.erase(currentFactorsCopy.begin()+k);
          arrCopy.erase(arrCopy.begin()+j);
          j--;
          break;
        }
      }

    }
    for (int k = 0; k < arrCopy.size(); k++) {
      currentFactors.push_back(arrCopy[k]);
      //printIntArray(currentFactors);
    }
  }
  printIntArray(currentFactors);
  int result = 1;
  for (int i = 0; i < currentFactors.size(); i++) {
    result *=currentFactors[i];
  }
  std::cout << "Result: " << result << '\n';
  return 0;
}
