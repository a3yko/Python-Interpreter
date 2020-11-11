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
    
    while chr < len(src) and src[chr] in [' ', '\t', '\n']:
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
        while src[chr] != '\'':
            varcontent += src[chr]
            chr+=1  
                        
        chr+=1
        variables[varname] = varcontent
        
    if src[chr] in ['0','1','2','3','4','5','6','7','8','9']:   
        while src[chr] != '\n':
            varcontent += src[chr]
            chr+=1 

        #added eval so that it can add when assigned 
        variables[varname] = eval(varcontent)    
    
   
   #lets you set a variable to another variable's value
   #it doesn't let you do any operations on the values yet 
    if src[chr] in '[a-zA-Z]':   
        value = 0
        while src[chr] != '\n':
            varcontent += src[chr]
            chr+=1

            for x in variables:
                if(varcontent == x):
                    value += variables[varcontent]
                    varcontent = ''

        #added eval so that it can add when assigned 
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




#started the if condition 
def ifcondition():
    global chr
    
    chr += 2
    squeeze()
    chr += 1
    condition = ''
    
    
    while src[chr] != ')':
        condition += src[chr]
        chr += 1

    
    
    chr += 1
    squeeze()
    if eval(condition):
        print("true")
        #needs a way to be able to read the lines following the if statement and ignore the else lines
        
    else:
        print("untrue")
        #same as if 


#Reader for input file
while chr < len(src):
    if src[chr:].startswith('#'):
        comment()
        continue
    
    if re.match(r'^([a-zA-z0-9]+)\s+?=', src[chr:]):
        assign()
        continue
    
    if re.match(r'^print\s*\(', src[chr:]):
        printer()
        continue

    # if re.match(r'^if\s*\(', src[chr:]):
    #     ifcondition()
    #     continue

