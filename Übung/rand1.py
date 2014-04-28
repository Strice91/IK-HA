import random

userNumber = int(input("Alda gibst du hier Zahl ein: "))
progNumber = random.randint(1,100)

if userNumber > progNumber:
	print("GEWONNEN!")
else:
	print("Du Opfer!")

