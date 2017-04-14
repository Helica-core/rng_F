#!/usr/bin/env python
#coding:utf8
#
#	MixPool Listener
#		1.keyboard input
#		2.Mouse movement
#		3.system interrupt change
#		//4.cpu use change
#		//5.memory use change


import sys,os
import threading

from evdev import InputDevice
from select import select

class EventListener:
    
    name = "EventListener"
    running = 1
    Recoder = 0

    def __init__(self,recoder):
        self.Recoder = recoder
        try:
            pid = os.fork()
            if pid > 0:
            #exit first parent
                sys.exit(0)
        except OSError, e:
            print >>sys.stderr, "fork #1 failed:%d (%s)" % (e.errorno, e.strerror)
            sys.exit(1)

        os.chdir("/")
        os.setsid()
        os.umask(0)

        try:
            pid = os.fork()
            if	pid > 0:
                #exit from second parent, print eventual PID before
                print ("Deamon PID %d" % pid)
                sys.exit(0)
        except OSError, e:
            print >>sys.stderr, "fork #2 failed:%d (%s)" % (e.errorno, e.strerror)
            sys.exit(1)

        self.main()

    def KeyboardEvent(self):
        """event origin id = 1
           Keyboard input Event
        """
        print self.name

        eo_id = 1

        dev = InputDevice('/dev/input/event0')

        while 1:
        #os.system("python Accumulator.py -a eo_id=%s time=%d" % (eo_id, time.time())
            select([dev],[],[])
            for event in dev.read():
                if event.code != 0:
                    os.system("echo "+"code:%d value:%d"%(event.code,event.value))
                    if event.value == 113:
                        self.running = 0


    def MouseEvent(self):
        """Event origin id  = 2
        Mouse movement Event
        """

        eo_id = 2

        dev = InputDevice('/dev/input/event1')

        while 1:
            select([dev],[],[])
            for event in dev.read():
                if event.code != 0:
                    os.system("echo " + "code:%d value:%d" % (event.code,event.value))
        pass

    def InterruptEvent(self):

        pass

    def main(self):
        """	A deamon process for rng_F

        """
        import time

        Thread_key = threading.Thread(target=self.KeyboardEvent)
        Thread_key.start()

        Thread_Mouse = threading.Thread(target=self.MouseEvent)
        Thread_Mouse.start()

        while self.running:

            print (str(time.time()))
            time.sleep(10)

def recoder():
    
    print "recode"

PRNG = EventListener(recoder)
print "Test"
