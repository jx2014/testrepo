import subprocess
import re
from os import path

output = 'output.txt'

a_file_name = raw_input('Type 1st txt File(.txt not required): ')
a_file_input = a_file_name + '.txt'
b_file_name = raw_input('Type 2nd txt File(.txt not required): ')
b_file_input = b_file_name + '.txt'


sha_only = re.compile('([0-9]|[a-f]){40}')
sha = re.compile('([0-9]|[a-f]){40}.*')
hsd = re.compile('(?<=#)H(?=\d{9,14})')


def getSHA(file):
    result = list()
    for line in file:
        sha_string = sha_only.match(line)
        if sha_string:
            result.append(sha_string.group(0))

    return result

try:
    with open(a_file_input, 'r') as a_txt, open(b_file_input, 'r') as b_txt:
        a_txt_sha = set(getSHA(a_txt))
        b_txt_sha = set(getSHA(b_txt))

        in_a_not_in_b = a_txt_sha.difference(b_txt_sha)
        in_b_not_in_a = b_txt_sha.difference(a_txt_sha)
        

    ##    for i in in_a_not_in_b:
    ##        print i
    ##
    ##    print '_'*40
    ##    
    ##    for i in in_b_not_in_a:
    ##        print i

        a_txt.seek(0,0)
        b_txt.seek(0,0)

        with open(output, 'w') as output_file:
            output_file.write('\n******FW Commit(s) in {} since {}'.format(a_file_name,b_file_name) + '*'*12 +'\n\n')  
            for a_line in a_txt:
                #print a_line
                for sha_line in in_a_not_in_b:
                    #print sha_line
                    if re.match(sha_line+'.*', a_line):
                        a_line = re.sub(hsd, ' ', a_line) 
                        output_file.write(a_line.rstrip('\n')+'\n')
                        
        with open(output, 'a') as output_file:
            output_file.write('\n******FW Commit(s) in {} since {}'.format(b_file_name, a_file_name) + '*'*12 + '\n\n')    
            for b_line in b_txt:
                #print b_line
                for sha_line in in_b_not_in_a:
                    #print sha_line
                    if re.match(sha_line+'.*', b_line):
                        b_line = re.sub(hsd, ' ', b_line)
                        output_file.write(b_line.rstrip('\n')+'\n')                        
                        
    subprocess.Popen("notepad output.txt", shell=False)
except IOError, Argument:
    print '\n%s\n' % Argument
    subprocess.call('pause', shell=True)




