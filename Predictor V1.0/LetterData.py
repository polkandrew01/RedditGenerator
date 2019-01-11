import json, re, copy, glob

def saveOutput(data, name):
    print("Saving output")
    file = open('data'+name+'.tsv', 'w')
    file.write('Key\ta\tb\tc\td\te\tf\tg\th\ti\tj\tk\tl\tm\tn\to\tp\tq\tr\ts\tt\tu\tv\tw\tx\ty\tz\tspace\t.\t!\t?\n')
    for key, value in data.items():
        string = key
        for key1, value1 in value.items():
            string+='\t'+str(value1)   
        string += '\n'
        file.write(string)
    file.close()
    
    file = open('data'+name+'.txt','w')
    file.write(json.dumps(data, indent=2))
    file.close

def averageData(dictionary):
    print("Averaging Data")
    for key, value in dictionary.items():
        for keyA, valueA in value.items():
            if valueA == 0:
                valueA = letterDict()
            if valueA != 0:
                total=0
                for key1, value1 in valueA.items():
                       total+=value1
                if total > 0:
                    for key1, value1 in valueA.items():
                        dictionary[key][keyA][key1] = (float(value1)/float(total))

def letterDict():
    temp=dict()
    temp2 = 'abcdefghijklmnopqrstuvwxyz .!?'
    for char in temp2:
        temp[char] = 0
    return temp

def sumLetters(bodies, authrs, datas):
    #print("Data Comments")
    pattern = re.compile('[^a-zA-Z .!?]')
    string = pattern.sub('', datas['body'].lower())
    temp = '  '
    for i in range(len(string)-1):
        if temp[0] not in bodies:
            bodies[temp[0]] = letterDict()
        if bodies[temp[0]][temp[1]] == 0:
            bodies[temp[0]][temp[1]] = letterDict()
        bodies[temp[0]][temp[1]][string[i]] += 1
        temp = temp[1]+string[i]

    name = pattern.sub('', datas['author'].lower())+' '
    temp = '  '
    for i in range(len(name)-1):
        if temp[0] not in authrs:
            authrs[temp[0]] = letterDict()
        if authrs[temp[0]][temp[1]] == 0:
            authrs[temp[0]][temp[1]] = letterDict()
        authrs[temp[0]][temp[1]][name[i]] += 1
        temp = temp[1]+name[i]

    if 'replies' in datas:
        for reply in datas['replies']:
            sumLetters(bodies, authrs, reply)

bodies=dict()
titles=dict()
authrs=dict()
filesSearched=0

subreddit = input('Get data for subreddit: ')

files = glob.glob('data/'+subreddit+'*.txt')

for item in files:
    print(item)
    filesSearched+=1
    file = open(item, "r")
    string = file.read()
    file.close()
    data = json.loads(string)

    ###Letters in bodies
    if 'body' in data:
        sumLetters(bodies, authrs, data)
    for comments in data['comments']:
        sumLetters(bodies, authrs, comments)

    ###Letters in titles
    pattern = re.compile('[^a-zA-Z .!?]')
    title = pattern.sub('', data['post'].lower())
    temp = '  '
    for i in range(len(title)-1):
        if temp[0] not in titles:
            titles[temp[0]] = letterDict()
        if titles[temp[0]][temp[1]] == 0:
            titles[temp[0]][temp[1]] = letterDict()
        titles[temp[0]][temp[1]][title[i]] += 1
        temp = temp[1]+title[i]
        '''if title[i] not in titles:
            titles[title[i]]=letterDict()
        if title[i+1] not in titles[title[i]]:
            titles[title[i]][title[i+1]] = 0
        titles[title[i]][title[i+1]]+=1'''

print("Searched "+str(filesSearched)+" files.")
if len(files) > 0:
    #Make percentages ----
    averageData(bodies)
    averageData(titles)
    averageData(authrs)        

    #Save the output to tsv file ---- 
    saveOutput(bodies, 'Bodies')
    saveOutput(titles, 'Titles')
    saveOutput(authrs, 'Authors')
    #print(json.dumps(bodies, indent=2))
