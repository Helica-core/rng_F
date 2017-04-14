#!/usr/bin/env python
#coding:utf8

#Accumulator.py
#
#   class:Accumulator
#       Public Method:
#       
#       Private Method:    
#


import sys,os
import threading
import time
import hashlib

from evdev import InputDevice
from select import select


class  Accumulator:

    poolnum = 32
    minpoolsize = 256
    running = 1
    lastreseed = 0
    reseedcnt = 0

    MixPool = [""] * poolnum
    R_STATE = {'g':{'K':0,'C':0},'reseedcnt':0,'p':MixPool}


    def __init__(self,g_state):
   
        self.InitEventListener()
        
        self.InitializeAccumulator(g_state)

    
    def InitEventListener(self):
       
        Thread_key = threading.Thread(target=self.KeyboardEvent)
        Thread_key.start()

        Thread_Mouse = threading.Thread(target=self.MouseEvent)
        Thread_Mouse.start()



    def InitializeAccumulator(self,g_state):
        
        e = '0'
        for x in self.R_STATE['p']:
            x = e

        self.R_STATE['g'] = g_state
        self.R_STATE['reseedcnt'] = 0


        return self.R_STATE


    def PseudoRandomData(self, R_state, n):

        print "Pseudo Random Data"


    def CheckNUpdate(self, g_state, reseed):
        """ check if need reseed and recode
        """

        if (time.time() - self.lastreseed > 0.1) and  (len(self.R_STATE['p'][0]) > self.minpoolsize):
            
            #print "[+] pre to reseed"
            
            self.reseedcnt += 1

            s = ''
            
            sha256 = hashlib.sha256()


            for x in range(self.poolnum):
                
                if self.reseedcnt % (2**x) == 0:
                  
                  sha256.update(self.R_STATE['p'][x])

                  s += sha256.hexdigest()
                  
                  self.R_STATE['p'][x] = ''  
                  
            reseed(s)
            
            self.lastreseed = time.time() 
        

    def AddRandomEvent(self,R_state, eo_id, time, i):

        time = str(time)

        assert len(time) <= 32 
        assert len(time) >= 1
        assert eo_id >= 0 
        assert eo_id <= 255
        assert i >= 0
        assert i <= 31

        R_state['p'][i] += (str(eo_id)+str(len(time))+str(time))
		
        #print "[+] Add random event id:%d time:%s" % (eo_id, time)


    def KeyboardEvent(self):
        """event origin id = 1
           Keyboard input Event
        """

        eo_id = 1

        dev = InputDevice('/dev/input/event0')

        while 1:
            
            select([dev],[],[])
            
            for event in dev.read():
            
                if event.code != 0:
            
                    self.AddRandomEvent(self.R_STATE, eo_id, time.time(), eo_id%self.poolnum)
            
                    if event.code == 16:
            
                        self.running = 0
            
                        sys.exit(0)


    def MouseEvent(self):
        """Event origin id  = 0
           Mouse movement Event
        """

        eo_id = 0

        dev = InputDevice('/dev/input/event1')

        while 1:

            if self.running == 0:

                sys.exit(0)
                
            select([dev],[],[])

            for event in dev.read():

                if event.code != 0:

                    self.AddRandomEvent(self.R_STATE, eo_id, time.time(), eo_id%self.poolnum)

    def InterruptEvent(self):

        pass


    def DisplayR(self):
        """
        """
        print '\033[1;34m'
        print '[+] Accumulator State'
        for x in range(self.poolnum):
            if len(self.R_STATE['p'][x]) != 0:
                print '--pool[%d] %s...  size:%d' % (x, self.R_STATE['p'][x][0:10], len(self.R_STATE['p'][x]))
            else:
                print '--pool[%d] empty' % x

        print '--reseedcnt:%d lastreseed:%d' % (self.reseedcnt, self.lastreseed)
        print '\033[0m'

def test():

    prng = Accumulator([0,0])
 
    while prng.running:
        pass

    print str(prng.R_STATE['p'])

    print 'waitting to Exit...'

if __name__ == "__main__":
    
    test()

