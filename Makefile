CFLAGS=-g -Wall -Werror
ASFLAGS=-g

all: fizzbuzz

fizzbuzz: mal.o kernel.o fizzbuzz.o

kernel.o: kernel.s

fizzbuzz.s: tests/fizzbuzz.mal mal.py
	python mal.py tests/fizzbuzz.mal > fizzbuzz.s
