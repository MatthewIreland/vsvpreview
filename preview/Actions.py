'''
Created on 11 Jul 2015

@author: matthew
'''

class UnknownActionError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Action(object):
    '''
    TODO classdocs
    '''
    actionName = "Action"
    
    def __init__(self, startTime=None, endTime=None):
        '''
        TODO docs
        '''
        
        self.startTime = startTime
        self.endTime = endTime
        
        
    def __repr__(self):
        return self.__str__()
        
    def __str__(self):
        return self.actionName + ". Start " + str(self.startTime) + "; End: " + str(self.endTime)
        
class GreyAction(Action):
    actionName = "Grey Action"
    pass
    
class AppearAction(Action):
    actionName = "Appear Action"
    pass
    
class HighlightAction(Action):
    pass
    
class CorrectAction(Action):
    pass

class EmptyAction(Action):
    def __init__(self):
        self.startTime = None
        self.endTime = None
    
    def __repr__(self):
        return self.__str__()
        
    def __str__(self):
        return "Empty action."
    