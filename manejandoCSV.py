import csv
#EXEMPLO 1
res = [x, y, z, ....]
csvfile = "<path to output csv or txt>"

#Assuming res is a flat list
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in res:
        writer.writerow([val])    

#Assuming res is a list of lists
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(res)
    
#EXEMPLO 3
table = [[1,2,3],[4,5,6]]

import csv

# write it
with open('test_file.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    [writer.writerow(r) for r in table]

# read it
with open('test_file.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    table = [[int(e) for e in r] for r in reader]
