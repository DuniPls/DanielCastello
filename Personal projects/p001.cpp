/******************************************************************************

                              Online C++ Compiler.
               Code, Compile, Run and Debug C++ program online.
Write your code in this editor and press "Run" button to compile and execute it.

*******************************************************************************/

/*
If we list all the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6 and 9. The sum of these multiples is 23.

Find the sum of all the multiples of 3 or 5 below 1000.
*/

#include <iostream>


bool multipleOfThree(int number){
    int multiple = 3;
    int n=0;
    float m=0;
    float difference=0;
    n=number/float(multiple);
    m=number/float(multiple);
    difference=m-float(n);
    if(difference==0){return true;}
    return false;
}

bool multipleOfFive(int number){
    int multiple = 5;
    int n=0;
    float m=0;
    float difference=0;
    n=number/float(multiple);
    m=number/float(multiple);
    difference=m-float(n);
    if(difference==0){return true;}
    return false;
}

int ifMultipleReturn(int number){
    if(multipleOfThree(number) || multipleOfFive(number)){return number;}
    return 0;
}

int main()
{
    int max=1000;
    int sum=0;
    for (int i = 1; i < max; i++) {
        sum+=ifMultipleReturn(i);
        //std::cout<<i<<'\t'<<sum<<'\n';
    }
    std::cout<<sum;
    return 0;
}
