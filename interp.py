import os
import sys
import re


#This checks if there is an appropriate input file present in the system arguments
if len(sys.argv) < 2:
    print('you must supply an input file')
    quit()

variables = {}
chr = 0
src = ''


#Gets input file and gives source variable the whole file
with open(sys.argv[1]) as file:
    src = file.read()
      
#eats up whitespaces up to the new line
def squeeze():
    global chr
    
    while chr < len(src) and src[chr] in [' ', '\t']:
        chr += 1
           
    
 ## function that ignores comments when it finds them in the code   
def comment():
    global chr 
    while chr < len(src) and src[chr] != '\n':
        chr += 1
    
    chr+= 1

# Assigns contents to variable
def assign():
    global chr

    varname = re.findall(r'^([a-zA-z0-9]+)\s+?=', src[chr:])[0]  
    chr += len(varname)

    squeeze()
    chr+= 1
    squeeze()
    
    varcontent = ''

    if src[chr] == '\'':
        chr+= 1 
        squeeze()
        while src[chr] != '\'':
            varcontent += src[chr]
            chr+=1            
        chr+=1
        variables[varname] = varcontent

    #allows for double quotes
    if src[chr] == '\"':
        chr+= 1 
        squeeze()
        while src[chr] != '\"':
            varcontent += src[chr]
            chr+=1            
        chr+=1
        variables[varname] = varcontent

    
    #allows you to assign to numbers but also have it so you can assign a variable
    #lets you set a variable to another variable's value
    if src[chr] in ['0','1','2','3','4','5','6','7','8','9','a','b', 'c', 'd','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']:   
        value = ''
        
        while src[chr] != '\n':
            squeeze()
            varcontent += src[chr]
            chr+= 1 

            for x in variables:
                if(varcontent == x):
                    value += str(variables[varcontent])
                    chr+=1
                    varcontent = ''
                    varcontent += src[chr]
                    if(varcontent in ['a','b', 'c', 'd','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']):
                        chr-=1
                        value+= '\n'
                    varcontent = ''

            if(varcontent == '+'):
                value+= '+'
                varcontent = ''
                chr+=1
            elif(varcontent == '-'):
                value+= '-'
                varcontent = ''
                chr+=1
            elif(varcontent == '*'):
                value+= '*'
                varcontent = ''
                chr+=1
            elif(varcontent == '/'):
                value+= '/'
                varcontent = ''
                chr+=1
            elif(varcontent == '%'):
                value+= '%'
                varcontent = ''
                chr+=1
            elif(varcontent == '^'):
                value+= '^'
                varcontent = ''
                chr+=1
            elif(varcontent in ['0','1','2','3','4','5','6','7','8','9']):
                value+= str(varcontent)
                varcontent = '' 
                chr+=1
                varcontent += src[chr]
                if(varcontent in ['a','b', 'c', 'd','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']):
                    chr-=1
                    value+= '\n'
                varcontent = '' 
  
        #added eval so that it can add when assigned 
        variables[varname] = eval(value) 

    squeeze()
 
 #this is the print function   
def printer():
    global chr
    
    chr += 5
    squeeze()
    chr += 1
    varname = ''
    
    while src[chr] != ')':
        varname += src[chr]
        chr += 1
        
    chr += 1
    squeeze()
 
    try:
        print(variables[varname])
    except:
        print('unknown variable: %s' % varname)
        quit()


def conditions():
    global chr

    # get varaibles and condiition
    var1 = re.findall(r'^([a-zA-Z0-9]+)\s+?[==|!=|<|<=|>|>=]', src[chr:])[0]
    condition = re.findall(r'(==|!=|>=|<=|>|<)', src[chr:])[0]
    var2 = re.findall(r'[==|!=|<|<=|>|>=]\s+([a-zA-Z0-9]+)', src[chr:])[0]

    # skip var1
    chr += len(var1)
    squeeze()

    # skip condition
    chr += len(condition)
    squeeze()

    # skip var2
    chr += len(var2)
    squeeze()

    
    # if it is a variable (not digit), then retreive the variable from variables dic
    if var1 in variables:
        var1 = variables[var1]
    if var2 in variables:
        var2 = variables[var2]

    # use eval to execute the statement
    return eval(str(var1) + condition + str(var2))


def if_else_block():
    global chr

    # skip if
    chr += 2
    squeeze()

    condition = conditions()

    # skip colon
    chr += 1

    #### if statement

    # skip \n
    chr+=1

    if_statement = ""

    line = ""
    while src[chr] != '\n':
        line+=src[chr]
        chr+=1

    indent = len(line) - len(line.lstrip())


    while (len(line) - len(line.lstrip())) == indent:
        if_statement += line.lstrip() + "\n"
        chr+=1
        line = ""
        while src[chr] != '\n':
            line+=src[chr]
            chr+=1


    #### else statement

    else_statement = ""

    chr+=1

    line = ""
    while src[chr] != '\n':
        line+=src[chr]
        chr+=1

    indent = len(line) - len(line.lstrip())

    while (len(line) - len(line.lstrip())) == indent:
        else_statement += line.lstrip() + "\n"
        chr+=1
        line = ""
        while src[chr] != '\n':
            line+=src[chr]
            chr+=1

            

    if condition:
        exec(if_statement)
    else:
        exec(else_statement)



#used for assignment operators. does not handle regular assignment
def assignment_operators():
    global chr
 
    varname = re.findall(r'^([a-zA-z0-9]+)\s+?["+="|"-="|"*="|"/="|"^="|"%="]', src[chr:])[0]
    operator = re.findall(r'["+="|"-="|"*="|"/="|"^="|"%="]', src[chr:])[0]
    
    chr += len(varname)

    squeeze()

    #skip the assignment operator for the value 
    chr+=2

    squeeze()
    value = ""

    #get the amount that is already stored in the variable
    if varname in variables:
        value = variables[varname]
    
    if value != "":   
        while src[chr] != '\n':
            if operator in ["+","-", "/", "*", "^", "%"]:
                value = eval(str(value) + operator + str(src[chr]))
                chr+=1

    variables[varname] = value
    squeeze()

#Reader for input file
while chr < len(src):
    if src[chr:].startswith('#'):
        comment()
        continue

    if re.match(r'^[a-zA-Z0-9]+\s+?(>=|<=|>|<|!=|==)', src[chr:]):
        print(conditions())
        continue

    if re.match(r'^if\s+?', src[chr:]):
        if_else_block()
        continue
    
    if re.match(r'^([a-zA-z0-9]+)\s+?=', src[chr:]):
        assign()
        continue
    
    if re.match(r'^print\s*\(', src[chr:]):
        printer()
        continue

    if re.match(r'^[a-zA-z0-9]+\s+?["+="|"-="|"*="|"/="|"^="|"%="]', src[chr:]):
        assignment_operators()
        continue

    chr += 1