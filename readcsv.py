import csv
import numpy as np
f = open("converge.csv", "rb")
reader = csv.DictReader(f, skipinitialspace=True)

for row in reader:
    data = [row["pt" + str(i) + ".Data[0][199]"] for i in xrange(6)]
    sumdata = sum([float(i) for i in data if i])
    c1 = [row["Constraint ( pt" + str(i) + ".ConCh<=0 )"] for i in xrange(6)]
    c2 = [row["Constraint ( pt" + str(i) + ".ConDs<=0 )"] for i in xrange(6)]
    c3 = [row["Constraint ( pt" + str(i) + ".ConS0<=0 )"] for i in xrange(6)]
    c4 = [row["Constraint ( pt" + str(i) + ".ConS1<=0 )"] for i in xrange(6)]
    c5 = [row["Constraint ( pt" + str(i) + ".SOC[0][0]=pt" + str(i) + ".SOC[0][-1] )"]
          for i in xrange(6)]
    c1_f = np.all([float(i) < 0 for i in c1 if i])
    c2_f = np.all([float(i) < 0 for i in c2 if i])
    c3_f = np.all([float(i) < 0 for i in c3 if i])
    c4_f = np.all([float(i) < 0 for i in c4 if i])
    c5_f = np.all([float(i) < 0 for i in c4 if i])

    feasible = [c1_f, c2_f, c3_f, c4_f, c5_f]
    print sumdata, feasible
