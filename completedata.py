import re
a='/n 1/2/3/n'
db=re.findall('[0-9 or /]+',a)
print(db)
