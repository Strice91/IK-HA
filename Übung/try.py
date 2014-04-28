flag = True

while flag:
	try:
		user = int(input("Schreibst du hier: "))
		flag = False
	except ValueError:
		print("Ey Alta, des war keine Zahl!")	

print("Rüschdüsch: %i" % user)