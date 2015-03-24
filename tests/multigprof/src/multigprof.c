#include<stdio.h>

int factorial(int number)
{
	if(number == 1)
		return number;
	return number * factorial(number - 1);
}

void fibonacci(int number)
{
	int curr = 0;
	int next = 1;
	int i;
	int swap;
	for(i=0;i<number;i++)
	{
		printf("%d\n", curr);
		swap = curr;
		curr = next;
		next = swap + next;
	}
}

void main(int argc, char* argv[])
{
	int number = 10;
	if(argc != 2)
		printf("Usage: %s (fact|fibo)\n", argv[0]);
	else
	{
		if(strcmp("fact",argv[1]) == 0)
		{
			// Factorial
			printf("%d! is %d\n", number, factorial(number));
		}
		else if(strcmp("fibo",argv[1]) == 0)
		{
			// Fibonacci
			printf("First %d fibonacci numbers are:\n", number);
			fibonacci(number);
		}
		else
		{
			printf("Usage: %s (fact|fibo)\n", argv[0]);
		}
	}
}