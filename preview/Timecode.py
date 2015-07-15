'''
Created on 11 Jul 2015

@author: matthew
'''

import re

MAX_MINS = 100

# TODO: these should really be immutable

class InvalidTimecodeError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
    
class NotComparableError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Timecode(object):
    '''
    TODO classdocs
    '''


    def __init__(self, string=None, segment=None, mins=None, secs=None, fraction=None):
        '''
        Constructor TODO docs
        '''
        
        if ((string is None) and
            (segment is not None) and
            (mins is not None) and
            (secs is not None)):
            
            self.segment = segment
            self.mins = mins
            self.secs = secs
            self.fraction = fraction
            
        elif ((string is not None) and
            (segment is None) and
            (mins is None) and
            (secs is None) and
            (fraction is None)):
            
            if (re.match('(\d+)-(\d+):(\d+)\.(\d+)', string)):
                m = re.match('(\d+)-(\d+):(\d+)\.(\d+)', string)  # TODO tidy
                self.segment = int(m.group(1))
                self.mins = int(m.group(2))
                self.secs = int(m.group(3))
                self.fraction = int(m.group(4))
            elif (re.match('(\d+)-(\d+):(\d+)', string)):
                m = re.match('(\d+)-(\d+):(\d+)', string)  # TODO tidy
                self.segment = int(m.group(1))
                self.mins = int(m.group(2))
                self.secs = int(m.group(3))
                self.fraction = None
            else:
                raise InvalidTimecodeError(string)
            
        else:
            raise InvalidTimecodeError("Specify either string or timecode")
        
        if (self.mins<0 | self.mins>MAX_MINS):
            raise InvalidTimecodeError("Mins value {m:02d} out of range".format(m=self.mins))
        if (self.secs<0 | self.secs>59):
            raise InvalidTimecodeError("Secs value {s:02d} out of range".format(s=self.secs))
        if (self.fraction is not None):
            if (self.fraction<0 | self.fraction>99):
                raise InvalidTimecodeError("Fraction secs value {f:02d} out of range".format(f=self.fraction))
    
        
        
#    def __eq__(self, other):
#        if isinstance(other,Timecode):
#            if (((self.fraction is None) and (other.fraction is not None)) or
#                ((self.fraction is not None) and (other.fraction is None))):
#                return ((self.segment == other.segment) and
#                    (self.mins == other.mins) and
#                    (self.secs == other.secs))
#            else:
#                return ((self.segment == other.segment) and
#                    (self.mins == other.mins) and
#                    (self.secs == other.secs) and
#                    (self.fraction == other.fraction))
#        else:
#            raise NotComparableError(other)
        
    def __eq__(self, other):
        if isinstance(other,Timecode):
            if ((self.fraction is None) and (other.fraction is not None)):
                return False
            elif ((self.fraction is not None) and (other.fraction is None)):
                return False
            elif ((self.fraction is None) and (other.fraction is None)):
                return ((self.segment == other.segment) and
                    (self.mins == other.mins) and
                    (self.secs == other.secs))
            else:
                return ((self.segment == other.segment) and
                    (self.mins == other.mins) and
                    (self.secs == other.secs) and
                    (self.fraction == other.fraction))
        else:
            raise NotComparableError(other)
        
    def __ne__(self, other):
        if isinstance(other,Timecode):
            return not self.__eq__(other)
        else:
            raise NotComparableError()
    
    def __lt__(self,other):
        if isinstance(other,Timecode):
            if (self.fraction is None) or (other.fraction is None):
                if (self.segment < other.segment):
                    lt = True
                elif (self.segment > other.segment):
                    lt = False
                elif self.mins < other.mins:
                    lt = True
                elif self.mins > other.mins:
                    lt = False
                elif self.secs < other.secs:
                    lt = True
                else:
                    lt = False
            else:
                if self.segment < other.segment:
                    lt = True
                elif self.segment > other.segment:
                    lt = False
                elif self.mins < other.mins:
                    lt = True
                elif self.mins > other.mins:
                    lt = False
                elif self.secs < other.secs:
                    lt = True
                elif self.secs > other.secs:
                    lt = False
                elif self.fraction < other.fraction:
                    lt = True
                else:
                    lt = False
            return lt
        else:
            raise NotComparableError(other)
        
    def __gt__(self,other):
        if isinstance(other,Timecode):
            return ((not self.__lt__(other))
                    and (not self.__eq__(other)))
        else:
            raise NotComparableError(other)
            
    def __le__(self,other):
        if isinstance(other,Timecode):
            return ((self.__lt__(other))
                    or self.__eq__(other))
        else:
            raise NotComparableError(other)
        
    def __ge__(self,other):
        if isinstance(other,Timecode):
            return ((self.__gt__(other))
                    or self.__eq__(other))
        else:
            raise NotComparableError(other)
        
    def __hash__(self):
        if (self.fraction is None): 
            return hash((self.segment,self.mins,self.secs))
        else:
            return hash((self.segment,self.mins,self.secs,self.fraction))
        
        
    def __str__(self):
        if self.fraction == None:
            fraction = 0
        else:
            fraction = self.fraction
        #return (str(self.segment) + "-" + str(self.mins) + "-" + str(self.secs) + "." + str(fraction))
        return "{segment:02d}-{minute:02d}:{secs:02d}.{fraction:03d}".format(segment  = self.segment,
                                                                             minute   = self.mins,
                                                                             secs     = self.secs,
                                                                             fraction = fraction)
                    
    def __repr__(self):
        return self.__str__()