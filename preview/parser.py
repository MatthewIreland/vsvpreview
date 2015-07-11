'''
Created on 11 Jul 2015

@author: matthew
'''

import ply.yacc as yacc
import globaldecs as globals
import re
from preview import Actions
from Timecode import Timecode
from lexer import tokens

class SyntaxError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

#isInTime = lambda x : (x.startTime < globals.currentTime and x.endTime > globals.currentTime)
#currentTime = globals.currentTime   # TODO delete this line

start = 'latexBlock'  # start symbol

def p_latexString_base_str(p):
    'latexString : STRING'
    p[0] = p[1]
    
def p_latexString_base_ws(p):
    'latexString : WHITESPACE'
    p[0] = p[1]
    
def p_latexString_base_nl(p):
    'latexString : NEWLINE'
    p[0] = p[1]
    
def p_latexString_str(p):
    'latexString : STRING latexString'
    p[0] = p[1] + p[2]
    
def p_latexString_ws(p):
    'latexString : WHITESPACE latexString'
    p[0] = p[1] + p[2]
    
def p_latexString_nl(p):
    'latexString : NEWLINE latexString'
    p[0] = p[1] + p[2]
    
def p_latexBlock_latex(p):
    'latexBlock : latexString latexBlock'
    p[0] = p[1] + p[2]
    
def p_latexBlock_empty(p):
    'latexBlock :'
    p[0] = ''
    
def p_latexBlock_greyenv(p):
    'latexBlock : greyEnv latexBlock'
    p[0] = p[1] + p[2]
    
def p_latexBlock_appearenv(p):
    'latexBlock : appearEnv latexBlock'
    p[0] = p[1] + p[2]
    
def p_latexBlock_hl(p):
    'latexBlock : hl latexBlock'
    p[0] = p[1] + p[2]
    
def p_latexBlock_correct(p):
    'latexBlock : correct latexBlock'
    p[0] = p[1] + p[2]
    
def p_latexBlock_list(p):
    'latexBlock : list latexBlock'
    p[0] = p[1] + p[2]
    
def p_greyEnv(p):
    'greyEnv : vsvBeginEnvGrey latexBlock vsvEndEnvGrey'
    assert isinstance(p[1], Actions.GreyAction)
    if (not hasattr(p.parser, 'colourVariableCounter')):
        p.parser.colourVariableCounter = int(0)
    
    
    print "Current time is " + str(p.parser.currentTime)
    print "Start time is " + str(p[1].startTime)
    print "End time is " + str(p[1].endTime)
    print str((p[1].startTime < p.parser.currentTime) and (p[1].endTime > p.parser.currentTime))
    
    if ((p[1].startTime <= p.parser.currentTime) and (p[1].endTime > p.parser.currentTime)):
        print "Is in time"
        p[0] = '\colorlet{oldcolour'+str(p.parser.colourVariableCounter)+'}{.}\\color{gray}'+p[2]+'\color{oldcolour'+str(p.parser.colourVariableCounter)+'}'
        p.parser.colourVariableCounter += 1
    else:
        print "Is not in time"
        p[0] = p[2]
        
def p_appearEnv(p):
    'appearEnv : vsvBeginEnvAppear latexBlock vsvEndEnvAppear'
    assert isinstance(p[1], Actions.AppearAction)
    if ((p[1].startTime <= p.parser.currentTime) and (p[1].endTime > p.parser.currentTime)):
        p[0] = p[2]
    else:
        p[0] = ''
        
def p_hl(p):
    'hl : vsvHighlight'
    if ((p[1].startTime <= p.parser.currentTime) and (p[1].endTime > p.parser.currentTime)):
        print "******** in time!!!"
        p[0] = '\\hl'
    else:
        p[0] = ''
        
def p_correct(p):
    'correct : vsvCorrect'
    if ((p[1].startTime <= p.parser.currentTime) and (p[1].endTime > p.parser.currentTime)):
        p[0] = '\\xxxcorrect'
    else:
        p[0] = ''
        
def p_list_itemize(p):
    'list : vsvListBeginItemize latexString listBody vsvListEndItemize'
    # TODO condition checking on begin/end
    p[0] = p[1] + p[2] + p[3] + p[4]
    
def p_list_enumerate(p):
    # TODO condition checking on begin/end    
    'list : vsvListBeginEnumerate latexString listBody vsvListEndEnumerate'
    p[0] = p[1] + p[2] + p[3] + p[4]
    
def p_list_description(p):
    # TODO condition checking on begin/end    
    'list : vsvListBeginDescription latexString listBody vsvListEndDescription'
    p[0] = p[1] + p[2] + p[3] + p[3] + p[4]
    
def p_listBody_final(p):
    'listBody : '
    p[0] = ''  
    
def p_listBody(p):
    'listBody : vsvItem latexBlock listBody'
    
    if (not hasattr(p.parser, 'colourVariableCounter')):
        p.parser.colourVariableCounter = int(0)
        
    if (isinstance(p[1], Actions.GreyAction)):
        if (p.parser.isInTime(p[1])):
            p[0] = '\\item\n\colorlet{oldcolour'+str(p.parser.colourVariableCounter)+'}{.}\\color{gray}'+p[2]+'\color{oldcolour'+str(p.parser.colourVariableCounter)+'}\n'+p[3]
            p.parser.colourVariableCounter += 1
        else:
            p[0] = '\\item' + p[2] + p[3]
    elif (isinstance(p[1], Actions.AppearAction)):
        if (p.parser.isInTime(p[1])):
            p[0] = '\\item' + p[2] + p[3]
        else:
            p[0] = ''
    elif (isinstance(p[1], Actions.EmptyAction)):
        p[0] = '\\item' + p[2] + p[3]
    else:
        raise Actions.UnknownActionError(p[1])

    
#def p_error(p):
#    raise SyntaxError(p)



if __name__ == '__main__':
    parser = yacc.yacc()
    parser.colourVariableCounter = int(0)
 
    with open('testLatexSources/test6.tex', 'r') as texFile:
        tex = texFile.read()
    
    result = parser.parse(tex)
    
    print(result)
