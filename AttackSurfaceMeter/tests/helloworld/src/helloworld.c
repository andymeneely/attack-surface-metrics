/*
 ============================================================================
 Name        : helloworld.c
 Author      : 
 Version     :
 Copyright   : Your copyright notice
 Description : Hello World in C, Ansi-style
 ============================================================================
 */

#include <stdio.h>
#include <stdlib.h>
#include "greetings.h"

void greet_a(int);
void greet_b(int);

int addInt(int n, int m)
{
    return n+m;
}

int (*functionPtr)(int,int);


typedef struct Greeter_Struct* Greeter;

struct Greeter_Struct
{
	void (*SayHi)();
	void (*SayHiTo)(int value);
};

void GreeterSayHi();
void GreeterSayHiTo(int value);

Greeter new_Greeter();

Greeter new_Greeter()
{
	Greeter self = (Greeter)malloc(sizeof(struct Greeter_Struct));

    self->SayHi = &GreeterSayHi;
    self->SayHiTo = &GreeterSayHiTo;

    return self;
}

void GreeterSayHi()
{
    printf("Hello from greeter!!");
}

void GreeterSayHiTo(int value)
{
    printf("Hello %d from greeter!!", value);
}

int main(void)
{
	greet_a(5);
	greet_b(10);

	puts("lol");

	functionPtr = addInt;
	int sum = (*functionPtr)(2, 3); // sum == 5

	Greeter g = new_Greeter();
	g->SayHi();
	g->SayHiTo(100);

	printf("---> %d", sum);

	return EXIT_SUCCESS;
}

void greet_a(int i)
{
	greet(0);
	recursive_a(i);
}

void greet_b(int i)
{
	char c;
	gets(c);

	greet(0);
	recursive_b(i);
}
