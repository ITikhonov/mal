#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdint.h>

extern void vm_go(int32_t *);

void print_hex(int x) {
	printf("%x ",x);
}

void print_str(char *x) {
	printf("%s ",x);
}

int main(int argc,char *argv[]) {
	int32_t stack[16];
	vm_go(&stack[16]);
	return 0;
}

