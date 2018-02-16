import os
import json

def read_json(filename):
    jsonFile = open(os.getcwd()+'/bot_config/'+filename+'.json', 'r')
    data = json.load(jsonFile)
    jsonFile.close()
    return data

def write_json(data, filename):
    jsonFile = open(os.getcwd()+'/bot_config/'+filename+'.json', 'w+') 
    jsonFile.write(json.dumps(data))
    jsonFile.close()
