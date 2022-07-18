import json
import re

class LazyDecoder(json.JSONDecoder):
    def decode(self, s, **kwargs):
        regex_replacements = [
            (re.compile(r'([^\\])\\([^\\])'), r'\1\\\\\2'),
            (re.compile(r',(\s*])'), r'\1'),
        ]
        for regex, replacement in regex_replacements:
            s = regex.sub(replacement, s)
        return super().decode(s, **kwargs)

with open("users.log", "r", encoding='utf-8') as f:
    lines = f.readlines()
    unique_users = set()
    calls = 0
    for l in lines:
        l = l.replace("\'", "\"")
        user = json.loads(l, cls=LazyDecoder)
        unique_users.add(user['id'])
        calls += 1
    print(f"The service was called by {len(unique_users)} unique users")
    print(f"The total calls number was {calls}")
