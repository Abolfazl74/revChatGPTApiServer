#!/usr/bin/python
import json


with open("tokens_status.json", "r+") as g:
    tokens_status = json.load(g)
    for access_token in tokens_status:
        tokens_status[access_token] = 0
        
    g.seek(0)  # rewind
    json.dump(tokens_status, g)
    g.truncate()