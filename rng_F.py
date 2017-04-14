#
#
#The main file
#
#
#
#
#

import getopt
import sys

from Accumulator import *
from Generator import *
from SeedMan import *

banner = """
\033[1;32m
                                       _______
                                     /\  _____\\
         _ __    ___      __         \ \ \____/
        /\`'__\/' _ `\  /'_ `\        \ \  ___\\
        \ \ \/ /\ \/\ \/\ \L\ \        \ \ \__/
         \ \_\ \ \_\ \_\ \____ \        \ \_\\
          \/_/  \/_/\/_/\/___L\ \ _______\/_/
                          /\____//\______\\
                          \_/__/ \/______/
        
\033[0m
"""

info = \
"""
rng_F is a randow number gengrator use Fortuna algorithm
It is written in Python 2.7

auth:Helica@bupt
"""

usage = \
""" 
        -r=n get n bytes random data, default print hexdump format 
            --raw get the random data string
            --hex get the hex format of the random data

        -u update seed file and reseed

        -s display the state, default display all the state
            --gstate display the state of the gengertor 
            --rstate display the state of the accumulator

        -d display the seed file content

        -h help

        press q to quit
"""

 
def Usage():
    print banner
   
    print info
   
    print usage

if __name__ == "__main__":

    Usage()
 
    #init the generator 
    #G_STATE[0,0]
    print '\033[1;34m[+] Initializing Generator\033[0m'
    gen = Generator()
    
    #init the Accumulator
    #start EventListener Thread
    #
    print '\033[1;34m[+] Initializing Accumulator\033[0m'
    acc = Accumulator(gen.G_STATE)

    #init SeedManger
    #
    print '\033[1;34m[+] Initializing SeedManager\033[0m'
    seman = SeedMan(gen.PseudoRandomData, gen.ReSeed)
    
                 
    #op = input("please input you operator:")

    #User input to get RandomNumber

    while acc.running:
        
        opt = raw_input(">:")
        opt += '  X'
                
        opt = opt.split(' ')
        opt_s = opt_r = False 
        
        for x in opt:
            
            if x[0:2] == '-r':
                opt_r = True  
                size = int(x[3:])
                #Check if need reseed

                acc.CheckNUpdate(gen.G_STATE, gen.ReSeed)
                
                res = gen.PseudoRandomData(size)
                
                continue
                 
            if opt_r and x == '--hex':
                
                print "\033[1;32m[+] get random data:\033[0m"
                
                print ord2hex(res)

                break

            if opt_r and x == '--raw':

                print "\033[1;32m[+] get random data:\033[0m"

                print res

                break

            if opt_r :
                print "\033[1;32m[+] get random data:\033[0m"

                hexdump(res)
                break
            if x == '-u':
                
                seman.UpdateSeedFile()
                print '[+] updated'
                break

            if x == '-s':

                opt_s = True
            
                continue

            if opt_s and x == '--gstate':

                gen.DisplayG()

                break
            
            if opt_s and x == '--rstate':

                acc.DisplayR()
                break
            
            if opt_s == True:
                gen.DisplayG()
                acc.DisplayR()
                break
            if x == '-d':
                
                res = seman.ReadSeedFile()
                hexdump(res)
                break

            if x == '-h':

                print usage
                break
   
    print 'quit...' 
