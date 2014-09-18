import re

a_file = '667.txt'

sha = re.compile('([0-9]|[a-f]){40}.*')

with open(a_file, 'r') as a_txt:
    print a_txt
    for line in a_txt.readlines():
        text = sha.match(line)
        if text:
            print text.group(0)
    
    
