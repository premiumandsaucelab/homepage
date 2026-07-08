import re
with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

c = re.sub(r'https://docs\.google\.com/forms/[^\s\"\'<>]+', 
           'https://docs.google.com/forms/d/e/1FAIpQLSd-yh1RmZEtljz6Pg4IifrBh_mTQYO7jYvX-3GPfFti8hai7Q/viewform?usp=header', c)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('Replaced Google forms.')