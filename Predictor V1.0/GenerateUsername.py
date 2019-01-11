import json, copy, random

data = dict()
temp = []

total=0
average=[0.0,0.0,0.0,0.0,
          0.0,0.0,0.0,0.0,
          0.0,0.0,0.0,0.0,
          0.0,0.0,0.0,0.0,
          0.0,0.0,0.0,0.0,
          0.0,0.0,0.0,0.0,
          0.0,0.0,0.0]

first = True
with open('dataAuthors.tsv', "r") as f:
    for line in f:
        line = line.split('\t')
        if first == True:
            first = False
            temp = copy.deepcopy(line)
            temp.pop(0)
            temp.pop(-1)
            temp.append(' ')
        else:
            total+=1
            data[line[0]] = dict()
            for i in range(1, len(line)):
                data[line[0]][temp[i-1]] = line[i]
                average[i-1]+=float(line[i])

for key, value in data.items():
    for i in range(len(value)):
        if i == 0:
            data[key][temp[i]]=float(value[temp[i]])*100
        else:
            data[key][temp[i]]=(float(data[key][temp[i]])*100)+float(data[key][temp[i-1]])
        if i+1 == len(value):
            data[key][temp[i]]=float(100.0)
#print(json.dumps(data, indent=2))
for i in range(len(average)):
    average[i] = (average[i]/float(total))*100

percents = []
for i in range(len(average)):
    if i == 0:
        percents.append(average[i])
    else:
        percents.append(percents[-1]+average[i])

#Main Script
stop = ''
while stop == '':
    val = random.randint(0,100)
    i = 0
    while val > percents[i]:
        i+=1
    string = temp[i]
    while string[-1] != ' ':
        val = random.randint(0,100)
        i = 0
        while val > data[string[-1]][temp[i]]:
            i+=1
        string+=temp[i]
    print(string)
    input('')
