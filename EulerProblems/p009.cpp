/******************************************************************************

                              Online C++ Compiler.
               Code, Compile, Run and Debug C++ program online.
Write your code in this editor and press "Run" button to compile and execute it.

*******************************************************************************/
/*
A Pythagorean triplet is a set of three natural numbers, a < b < c, for which,

a2 + b2 = c2
For example, 32 + 42 = 9 + 16 = 25 = 52.

There exists exactly one Pythagorean triplet for which a + b + c = 1000.
Find the product abc.
*/

#include <iostream>
#include <math.h>

void evenTest(){
    int a;
  int b;
  int c;
  int j = 0;
  int k = 0;
  for (int i = 2; i < 50; i=i+2) {
    j += (i - 1);
    k = j + 2;
    if(i + j + k == 1000){std::cout<<(i*j*k)<<'\n';}
  }
}

void oddTest(){
    int a;
  int b;
  int c;
  int j = 0;
  int k = 0;
  for (int i = 1; i < 50; i=i+2) {
    j += (i + 1);
    k = j + 1;
    if(i + j + k == 1000){std::cout<<(i*j*k)<<'\n';}
  }
}

int main()
{
  evenTest();
  oddTest();

  return 0;
}
