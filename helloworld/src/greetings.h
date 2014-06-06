/*
 * greetings.h
 *
 *  Created on: Jun 5, 2014
 *      Author: kevin
 */

#ifndef GREETINGS_H_
#define GREETINGS_H_

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
	recursive_b(i--);
}

void recursive_b(int i)
{
	if(1 > 0)
	{
		recursive_a(i--);
	}
}

#endif /* GREETINGS_H_ */
