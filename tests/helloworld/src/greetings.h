/*
 * greetings.h
 *
 *  Created on: Jun 5, 2014
 *      Author: kevin
 */

#ifndef GREETINGS_H_
#define GREETINGS_H_

void greet(int);
void recursive_a(int);
void recursive_b(int);

int CASUAL = 0;
int MORNING = 1;
int EVERYONE = 2;

void greet(int greeting_code)
{
	if(greeting_code == CASUAL)
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

#endif /* GREETINGS_H_ */
