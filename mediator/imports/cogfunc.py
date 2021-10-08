import json

def getcogs():
    file=open('mediator/coglist.json')
    data=json.load(file)
    return data['cog_list']
