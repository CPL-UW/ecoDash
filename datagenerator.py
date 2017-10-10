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
		uwriter.writerow(["user", "exp", "tink", "ref"])

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
				uwriter.writerow([str(fileno), exp/1000.0, tink/1000.0, ref/1000.0])





'''
import csv
import random

datas = {
	"ohmmgg1": {"exp": 0, "tink": 0, "ref": 0, "alpha": 0}, 
	"ohmmgg2": {"exp": 0, "tink": 0, "ref": 0, "alpha": 0}, 
	"ohmmgg3": {"exp": 0, "tink": 0, "ref": 0, "alpha": 0}, 
	"ohmmgg4": {"exp": 0, "tink": 0, "ref": 0, "alpha": 0}, 
	"ohmmgg5": {"exp": 0, "tink": 0, "ref": 0, "alpha": 0}, 
	"ohmmgg6": {"exp": 0, "tink": 0, "ref": 0, "alpha": 0}, 
	"ohmmgg7": {"exp": 0, "tink": 0, "ref": 0, "alpha": 0}, 
	"ohmmgg8": {"exp": 0, "tink": 0, "ref": 0, "alpha": 0}, 
	"ohmmgg9": {"exp": 0, "tink": 0, "ref": 0, "alpha": 0}, 
	"ohmmgg10": {"exp": 0, "tink": 0, "ref": 0, "alpha": 0}, 
	"ohmmgg11": {"exp": 0, "tink": 0, "ref": 0, "alpha": 0}, 
	"ohmmgg12": {"exp": 0, "tink": 0, "ref": 0, "alpha": 0}, 
	"ohmmgg13": {"exp": 0, "tink": 0, "ref": 0, "alpha": 0}, 
	"ohmmgg14": {"exp": 0, "tink": 0, "ref": 0, "alpha": 0}, 
	"ohmmgg15": {"exp": 0, "tink": 0, "ref": 0, "alpha": 0}, 
	"ohmmgg16": {"exp": 0, "tink": 0, "ref": 0, "alpha": 0}, 
	"ohmmgg17": {"exp": 0, "tink": 0, "ref": 0, "alpha": 0}, 
	"ohmmgg18": {"exp": 0, "tink": 0, "ref": 0, "alpha": 0}, 
	"ohmmgg19": {"exp": 0, "tink": 0, "ref": 0, "alpha": 0},
	"ohmmgg20": {"exp": 0, "tink": 0, "ref": 0, "alpha": 0},
	"ohmmgg21": {"exp": 0, "tink": 0, "ref": 0, "alpha": 0},
	"ohmmgg22": {"exp": 0, "tink": 0, "ref": 0, "alpha": 0},
	"ohmmgg23": {"exp": 0, "tink": 0, "ref": 0, "alpha": 0},
	"ohmmgg24": {"exp": 0, "tink": 0, "ref": 0, "alpha": 0},
	"ohmmgg25": {"exp": 0, "tink": 0, "ref": 0, "alpha": 0},
}

fileno = 0

for u in datas.keys():
	with open("fakedata/testusr" + str(u) + ".csv", "wb") as csvf:
		uwriter = csv.writer(csvf)
		uwriter.writerow(["user", "exp", "tink", "ref", "alpha"])


# exp = 0
# tink = 0
# ref = 0
while fileno < 30:
	fileno = fileno + 1
	with open("fakedata/testcr" + str(fileno) + ".csv", 'wb') as csvfile:
		wrr = csv.writer(csvfile)
		wrr.writerow(["user", "exp", "tink", "ref", "alpha"])
		for u in datas.keys():
			if (random.randint(0,100) > 10):
				exp = random.randint(0, 1000)
				tink = random.randint(0, (1000 - exp))
				ref = 1000 - exp - tink
				datas[u]["exp"] = exp
				datas[u]["tink"] = tink
				datas[u]["ref"] = ref
				datas[u]["alpha"] = 0
			else:
				if (datas[u]["alpha"] < 1):
					datas[u]["alpha"] += 0.1

			wrr.writerow([u, exp/1000.0, tink/1000.0, ref/1000.0])
			with open("fakedata/testusr" + str(u) + ".csv", "ab") as csvf:
				uwriter = csv.writer(csvf)
				uwriter.writerow([str(fileno), exp/1000.0, tink/1000.0, ref/1000.0])

'''