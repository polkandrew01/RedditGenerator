#Generate txt file
import os
import json
import string

def getBodies(jsn):
    result = ''
    if 'body' in jsn:
        result += 'COMMENT: '+jsn['author']+'\n'
        result += jsn['body']+'\n'
        for reply in jsn['replies']:
            result += getBodies(reply)
    return result

bodies = open('reddit.txt', 'w', encoding='utf-8')
bodies.write('')
bodies.close()

directory = os.fsencode('data')
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    print(filename)
    if 'AskReddit.' in filename:
        txt = ''
        with open('data/'+filename, 'r', encoding='utf-8') as f:
            jsn = json.loads(f.read())
            txt += "POST: "+jsn['author']+'\n'
            txt += jsn['post']+'\n'
            if 'comments' in jsn:
                for comment in jsn['comments']:
                    txt += getBodies(comment) 
            #txt += jsn['post']+'\n'
        txt = txt.replace('&gt;', '').replace('*', '  ').replace('  ', ' ').replace('/thread', '').replace('/Thread', '')
        txt = ''.join(filter(lambda x:x in string.printable, txt))
        txt += '\n\n'
        bodies = open('reddit.txt', 'a', encoding='utf-8')
        bodies.write(txt)
        bodies.close()
