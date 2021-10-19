import json

def getcogs():
    with open('mediator/coglist.json','r') as file:
        data=json.load(file)
    return data['cog_list']
