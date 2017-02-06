# pair.py
#
# given a string, return a mirror pair of words
# i.e.   "a1ab0ab0a2" returns ab0
#        "123321" returns 3
#        "a23a23" returns a23
#        "12233" returns 2 and 3
#        "1222a2a" returns 2 and 2a
#        "1222" returns 2
#        "12221" returns 2

input_string = "a1ab0ab0a2c"
input_string = "a122323"


Total = len(input_string) #total characters of the string
Div = 2 # to be divded by
First = 0 # first character position.

N = Total / Div # character word pair length
Rem = Total % Div # if = 1 then we may have to compare with string shifted by whatever it is

while N >= 2:

    while S < (D + R - 1):
        first_word = input_string[S:N+S]
        second_word = input_string[N+S:N+N+S]
        if  first_word == second_word:
            print first_word
        S = S + 1

    D = D + 1
    N = M / D
    R = M % D
    S = 0



