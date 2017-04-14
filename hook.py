#!/usr/bin/env python
#coding: utf-8
from evdev import InputDevice
from select import select

def detectInputKey():
    dev = InputDevice('/dev/input/event0')

    while True:
        select([dev], [], [])
        for event in dev.read():
			if event.code != 0:            
				print "code:%s value:%s" % (event.code, event.value)


if __name__ == '__main__':
    detectInputKey()

