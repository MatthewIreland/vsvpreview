'''
Created on 15 Jul 2015

@author: matthew
'''

class UnknownFrameTypeError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class FrameInput(object):
    '''
    classdocs
    '''
    type="unknown"


    def __init__(self, texSource, startTime, endTime):
        '''
        Constructor
        '''
        self.startTime = startTime
        self.endTime   = endTime
        self.texSource = texSource
        self.timecodeList = []
        
class LeftFrameInput(FrameInput):
    '''
    classdocs
    '''
    type="left"

        
class RightFrameInput(FrameInput):
    '''
    classdocs
    '''
    type="right"

        