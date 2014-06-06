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

int main(void) {

	greet(CASUAL);
	recursive_a(5);

	return EXIT_SUCCESS;
}
