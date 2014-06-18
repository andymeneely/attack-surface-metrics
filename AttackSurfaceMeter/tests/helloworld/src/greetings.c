/*
 * greetings.c
 *
 *  Created on: Jun 16, 2014
 *      Author: kevin
 */

#include <stdio.h>
#include <stdlib.h>
#include "greetings.h"



void greet(int greeting_code)
{
	if(greeting_code == 0)
	{
		puts("Whats up!");
	}
	else
	{
		puts("Not implemented");
	}
}

void recursive_a(int i)
{
	printf("%d\n", i);
	recursive_b(--i);
}

void recursive_b(int i)
{
	printf("%d\n", i);
	if(i > 0)
	{
		recursive_a(--i);
	}
}

