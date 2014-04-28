import random

win = 0
turns = 100000
for n in range(0,turns):
	n1 = random.randint(1,100)
	n2 = random.randint(1,100)
	if n1 > n2:
		win += 1

print("Gewinnchace: %2.4f%%" % (win/turns))

