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

int main(void)
{
	greet_a(5);
	greet_b(10);

	puts("lol");

	return EXIT_SUCCESS;
}

void greet_a(int i)
{
	greet(CASUAL);
	recursive_a(i);
}

void greet_b(int i)
{
	greet(CASUAL);
	recursive_b(i);
}
