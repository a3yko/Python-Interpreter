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
        value = ""
        while src[chr] != '\'':
            varcontent += src[chr]
            chr+=1            
        chr+=1
        variables[varname] = varcontent

    #allows for double quotes
    if src[chr] == '\"':
        chr+= 1 
        squeeze()
        value = ""
        while src[chr] != '\"':
            varcontent += src[chr]
            chr+=1            
        chr+=1
        variables[varname] = varcontent

    #allows you to assign to numbers but also have it so you can assign a variable
    if src[chr] in ['0','1','2','3','4','5','6','7','8','9']:   
        value = ""
        
        while src[chr] != '\n':
            varcontent += src[chr]
            squeeze()
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
                value+='+'
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
                value+= varcontent
                varcontent = '' 
                chr+=1
                varcontent = src[chr]

                if(varcontent in ['a','b', 'c', 'd','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']):
                        chr-=1
                        value+= '\n'
                varcontent = '' 

        #added eval so that it can add when assigned 
        if (isinstance(value, int) == int):
            variables[varname] = eval(value)
        else:
            variables[varname] = value   
  
    squeeze()
     #lets you set a variable to another variable's value
     #also does operations on the variables
    if src[chr] in ['a','b', 'c', 'd','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']:   
        value = ""
        
        while src[chr] != '\n':
            varcontent = src[chr]
            squeeze()

            for x in variables:
                if(varcontent == x):
                    value += str(variables[varcontent])
                    chr+=1   
                    varcontent = str(src[chr])
                    if(varcontent in ['a','b', 'c', 'd','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']):
                        chr-=1
                        value+= '\n'
      
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
                        value+= '\n'
                        chr-=1
                varcontent = '' 
            
        if (isinstance(value, int) == int):
            variables[varname] = eval(value)
        else:
            variables[varname] = value

    
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

    if_statement = re.findall(r'^:\s+?([a-zA-Z0-9()"]+)\s+?else:', src[chr:])[0]

    # skip colon
    chr += 1

    squeeze()
    chr += len(if_statement)
    squeeze()
    # skip else
    chr += 4
    else_statement = re.findall(r'^:\s+([a-zA-Z0-9()\s"~!@`$%^&*_+-=:;]+)\s+?', src[chr:])[0]

    #skip colon
    chr += 1
    squeeze()
    chr += len(else_statement)
    squeeze()

    if condition:
        eval(if_statement)
    else:
        eval(else_statement)


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

    chr += 1