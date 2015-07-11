'''
Created on 11 Jul 2015

@author: matthew
'''

import ply.lex as lex
import globaldecs as globals
import re
from preview import Actions
from Timecode import Timecode

startTimecode = 0

class InvalidEnvironmentError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

tokens = ("vsvBeginEnvGrey",
          "vsvEndEnvGrey",
          "vsvBeginEnvAppear",
          "vsvEndEnvAppear",
          "vsvHighlight",
          "vsvHighlightNoWrap",
          "vsvCorrect",
          "vsvListBeginItemize",
          "vsvListBeginEnumerate",
          "vsvListBeginDescription",
          "vsvListEndItemize",
          "vsvListEndEnumerate",
          "vsvListEndDescription",
          "vsvItem",
          "WHITESPACE",
          "NEWLINE",
          "STRING"
          )

# regexes for simple tokens
t_vsvEndEnvGrey = r'\\end\{vsvgrey\}'
t_vsvEndEnvAppear = r'\\end\{vsvappear\}'
#t_NEWLINE = r'\n'
t_vsvListBeginItemize = r'\\begin\{itemize\}'
t_vsvListBeginEnumerate = r'\\begin\{enumerate\}'
t_vsvListBeginDescription = r'\\begin\{description\}'
t_vsvListEndItemize = r'\\end\{itemize\}'
t_vsvListEndEnumerate = r'\\end\{enumerate\}'
t_vsvListEndDescription = r'\\end\{description\}'
t_WHITESPACE = r'\s'
t_STRING = r'\S+'

# methods for other tokens
def t_vsvBeginEnvGrey(t):
    #r'\\begin\{vsvgrey\}\{[\d-:]+\}{[\d-:]+\}'
    r'\\begin\{vsvgrey\}\{[\d\-:\.]+\}\{[\d\-:\.]+\}'
    times = re.findall('[\d\-:\.]+', t.value)
    startTime = Timecode(times[0])
    endTime = Timecode(times[1])
    t.lexer.timecodeSet.add(startTime)
    t.lexer.timecodeSet.add(endTime)
    t.value = Actions.GreyAction(startTime,endTime)
    return t

def t_vsvBeginEnvAppear(t):
    r'\\begin\{vsvappear\}\{[\d\-:\.]+\}\{[\d\-:\.]+\}'
    times = re.findall('[\d\-:\.]+', t.value)
    startTime = Timecode(times[0])
    endTime = Timecode(times[1])
    t.lexer.timecodeSet.add(startTime)
    t.lexer.timecodeSet.add(endTime)
    t.value = Actions.AppearAction(startTime,endTime)
    return t

def t_vsvHighlight(t):
    r'\\vsvhl\{[\d\-:\.]+\}\{[\d\-:\.]+\}'
    times = re.findall('[\d\-:\.]+', t.value)
    startTime = Timecode(times[0])
    endTime = Timecode(times[1])
    t.lexer.timecodeSet.add(startTime)
    t.lexer.timecodeSet.add(endTime)
    t.value = Actions.HighlightAction(startTime,endTime)
    return t

def t_vsvCorrect(t):
    r'\\vsvcorrect\{[\d\-:\.]+\}\{[\d\-:\.]+\}'
    times = re.findall('[\d\-:\.]+', t.value)
    startTime = Timecode(times[0])
    endTime = Timecode(times[1])
    t.lexer.timecodeSet.add(startTime)
    t.lexer.timecodeSet.add(endTime)
    t.value = Actions.CorrectAction(startTime,endTime)
    return t

def t_vsvItem(t):
    r'\\vsvitem\{[\d\-:\.]*\}\{[\d\-:\.]*\}\{(grey|appear|)\}'
#    r'\\vsvitem'
    times = re.findall('[\d\-:\.]+', t.value)
    if (len(times) > 0):
        startTime = Timecode(times[0])
        endTime = Timecode(times[1])
        t.lexer.timecodeSet.add(startTime)
        t.lexer.timecodeSet.add(endTime)
    else:
        tmpValue = Actions.EmptyAction()
    if re.match('.*appear.*',t.value):
        tmpValue = Actions.AppearAction(startTime,endTime)
    elif re.match('.*grey.*',t.value):
        tmpValue = Actions.GreyAction(startTime,endTime)
    else:
        tmpValue = Actions.EmptyAction()
    
    t.value = tmpValue
    return t


#def t_NEWLINE(t):
#    r'\n+'
#    print "newline!"
#    t.lexer.lineno += len(t.value)
#    t.value = '\n'


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
    
lexer = lex.lex(optimize=globals.MODE_DEBUG)

if __name__ == '__main__':
    
    with open('testLatexSources_old/test5.tex', 'r') as texFile:
        tex = texFile.read()
    
    lexer.timecodeSet = set([])
    lexer.input(tex)
    
    for tok in lexer:
        print(tok)
        
    timecodeList = list(lexer.timecodeSet)
    timecodeList.sort()
    print(timecodeList)
        
        