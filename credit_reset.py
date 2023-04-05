import json



with open("users_status.json", "r+") as g:
    users_status = json.load(g)
    for user_site in users_status:
        users_status[user_site] = 0
        
    g.seek(0)  # rewind
    json.dump(users_status, g)
    g.truncate()