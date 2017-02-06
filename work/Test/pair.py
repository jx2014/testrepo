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

input_string = "11cab0aab0a2ccg7g7aa"
#input_string = "a123123b"



def Pair2(input_string):
    Total = len(input_string)
    #print('\ninput_string: ', input_string, 'Total: ', Total)
    
    if Total >= 2:    
        a = 0
        b = 1
        c = 2
        remove_position = 1
        result = None
        
        while c <= Total:
            Fword = input_string[a:b]
            Sword = input_string[b:c]
            
            if Fword == Sword:
                result = Fword
                remove_position = c
            
            #print(a, b, c, Fword, Sword)
            
            b = b + 1
            c = c + 2
            
            if result is not None and c > Total:            
                print('Found pair: ', result)
        
        #print('\nremove_position: ', remove_position)
        input_string =  input_string[remove_position:]
        Pair2(input_string)









def Pair1(input_string):
    Total = len(input_string) #total characters of the string
    Div = 2 # to be divded by
    
    N = int(Total / Div) # character word pair length
    Rem = Total % Div # if = 1 then we may have to compare with string shifted by whatever it is
    n = 1 # for looping compare
    
    
    B = N
    
    
    while n <= N:
        i = 2 * n - (1 - Rem)
        
        a = 0 
        b = B
        c = b * 2
        
        while c <= Total:       
                    
            Fword = input_string[a:b]
            Sword = input_string[b:c]
                        
            if Fword == Sword:
                print("pairs: ", Fword, input_string, Total)
                #input_string = input_string[c:]
                #Pair(input_string)
            
            a = a + 1
            b = b + 1
            c = c + 1
            
        n = n + 1
        B = B - 1
    

Pair2(input_string)

