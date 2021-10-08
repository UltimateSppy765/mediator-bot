import json

def getcogs():
    file=open('coglist.json')
    data=json.load(file)
    return data['cog_list']
