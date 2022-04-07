import json

with open("users.log", "r", encoding='utf-8') as f:
    lines = f.readlines()
    unique_users = set()
    for l in lines:
        l = l.replace("\'", "\"")
        user = json.loads(l)
        unique_users.add(user['id'])
    print(f"The service was called by {len(unique_users)} unique users")
