import csv
import random

users = [
	"ohmmgg1", 
	"ohmmgg2", 
	"ohmmgg3", 
	"ohmmgg4", 
	"ohmmgg5", 
	"ohmmgg6", 
	"ohmmgg7", 
	"ohmmgg8", 
	"ohmmgg9", 
	"ohmmgg10", 
	"ohmmgg11", 
	"ohmmgg12", 
	"ohmmgg13", 
	"ohmmgg14", 
	"ohmmgg15", 
	"ohmmgg16", 
	"ohmmgg17", 
	"ohmmgg18", 
	"ohmmgg19",
	"ohmmgg20",
	"ohmmgg21",
	"ohmmgg22",
	"ohmmgg23",
	"ohmmgg24",
	"ohmmgg25",
]

fileno = 0

for u in users:
	with open("fakedata/testusr" + str(u) + ".csv", "wb") as csvf:
		uwriter = csv.writer(csvf)
		uwriter.writerow(["time", "exp", "tink", "ref"])

while fileno < 30:
	fileno = fileno + 1
	with open("fakedata/testcr" + str(fileno) + ".csv", 'wb') as csvfile:
		wrr = csv.writer(csvfile)
		wrr.writerow(["user", "exp", "tink", "ref"])
		for u in users:
			if (random.randint(0,100) > 10):
				exp = random.randint(0, 1000)
				tink = random.randint(0, (1000 - exp))
				ref = 1000 - exp - tink
			else:
				exp = 0
				tink = 0
				ref = 0
			wrr.writerow([u, exp/1000.0, tink/1000.0, ref/1000.0])
			with open("fakedata/testusr" + str(u) + ".csv", "ab") as csvf:
				uwriter = csv.writer(csvf)
				uwriter.writerow(["", exp/1000.0, tink/1000.0, ref/1000.0])

