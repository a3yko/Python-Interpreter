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

    var1 = re.findall(r'^([a-zA-Z0-9]+)\s+?[==|!=|<|<=|>|>=]', src[chr:])[0]
    condition = re.findall(r'(==|!=|>=|<=|>|<)', src[chr:])[0]
    var2 = re.findall(r'[==|!=|<|<=|>|>=]\s+([a-zA-Z0-9]+)', src[chr:])[0]

    chr += len(var1)
    squeeze()
    chr += len(condition)
    squeeze()
    chr += len(var2)
    squeeze()
    

    # make sure the varaible is in the list 
    if (var1 in variables) and ((var2 in variables) or (var2.isdigit())):
        if condition == "==":
            return variables[var1] == variables[var2] if (var2 in variables) else int(var2)
        if condition == "!=":
            return variables[var1] != variables[var2] if (var2 in variables) else int(var2)
        if condition == ">=":
            return variables[var1] >= variables[var2] if (var2 in variables) else int(var2)
        if condition == "<=":
            return variables[var1] <= variables[var2] if (var2 in variables) else int(var2)
        if condition == ">":
            return variables[var1] > variables[var2] if (var2 in variables) else int(var2)
        if condition == "<":
            return variables[var1] < variables[var2] if (var2 in variables) else int(var2)

    else:
        print("this is not a condition")
        quit()


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

    if re.match(r'^([a-zA-Z0-9]+)\s+?==|!=|<|<=|>|>=', src[chr:]):
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