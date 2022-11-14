import csv

f = open(r"./data.csv", 'r', encoding='CP949', newline='')
csv_reader = csv.reader(f)
first_line = True
for line in csv_reader:
    if first_line:
        print('▶ ' + line[0])
        first_line = False
    else:
        print('- ' + line[0] + ' / ' + line[1]  + ' / ' + line[2])
f.close()