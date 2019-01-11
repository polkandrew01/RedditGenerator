import requests, json
import re, os, time

#Recursivly get comments
def getReplies(data):
    temp = {'body':data['body'],
            'author':data['author'],
            'replies':[]}

    if 'replies' in data and data['replies'] != '':
        for reply in data['replies']['data']['children']:
            reply = reply['data']
            if 'body' in reply:
                temp['replies'].append(getReplies(reply))

    return temp

#Get all posts and comments in subreddit
def getPost(url):
    name = url.split('/')
    name = name[4]+'.'+name[7]

    if os.path.isfile('data/'+name+'.txt'):
        return
    
    result = {'post':'',
              'author':'',
              'comments':[]}
    response = requests.get(r''+url+'.json', headers = {'User-agent':'TestDownloadBot 0.1'})
    data = response.json()

    #print(json.dumps(data, indent=2))

    result['post'] = data[0]['data']['children'][0]['data']['title']
    result['author'] = data[0]['data']['children'][0]['data']['author']

    if 'selftext' in data[0]['data']['children'][0]['data']:
        result['body'] = data[0]['data']['children'][0]['data']['selftext']
    
    for thing in data[1]['data']['children']:
        thing = thing['data']
        if 'body' in thing:
            result['comments'].append(getReplies(thing))
    
    file = open('data/'+name+'.txt', 'w')
    file.write(json.dumps(result, indent=2))
    file.close()
    print(result['post'])
    #print(json.dumps(result, indent=2))
    time.sleep(1)

def getData(subreddit, num, total, after):
    #Get posts
    postUrls = []

    if after == '':
        response = requests.get(r'http://www.reddit.com/r/'+subreddit+'/.json', headers = {'User-agent':'TestDownloadBot 0.1'})
    elif after != None:
        response = requests.get(r'http://www.reddit.com/r/'+subreddit+'/.json?after='+after, headers = {'User-agent':'TestDownloadBot 0.1'})
    else:
        return
    data = response.json()

    #print(json.dumps(data, indent=2))

    for url in data['data']['children']:
        if len(postUrls)+total < num:
            postUrls.append('https://www.reddit.com'+url['data']['permalink'])
        
    for url in postUrls:
        getPost(url)

    time.sleep(1)    
    if len(postUrls)+total < num:
        getData(subreddit, num, len(postUrls)+total, data['data']['after'])

subreddit = input('Enter a subreddit: ')
num = int(input('Enter # of posts. [1-1000]: '))
if num > 999:
    num = 999
getData(subreddit, num, 0, '')

