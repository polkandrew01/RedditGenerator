import json, random

data = dict()

alpha = 'abcdefghijklmnopqrstuvwxyz .!?'

file = open('dataBodies.txt', 'r')
string = file.read()
file.close()
data = json.loads(string)

for key, value in data.items():
    for key1, value1 in value.items():
        prev = 0
        if value1 != 0:
            for key2, value2 in value1.items():
                data[key][key1][key2] += prev
                prev = data[key][key1][key2]

#Main Script
stop = ''
while stop == '':
    temp = '  '
    string = ''

    while temp[1] not in '.?!':
        val = random.randint(0,100)/100
        i = 0
        for key, value in data[temp[0]][temp[1]].items():
            if val > value:
                i+=1
        if i == 30:
            i = 29
        string+=alpha[i]
        temp = temp[1]+alpha[i]

    print(string)
    stop = input('\n\n')
