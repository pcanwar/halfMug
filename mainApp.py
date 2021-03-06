#!/usr/bin/python
'''
@author: anwar
'''
from __future__ import absolute_import
from __future__ import print_function
from CommandsSelfTraining import *
import time


def looping(commander):
    '''Enter user interactive mode, wait for user's input
    '''
    while True:
        commands = raw_input('> ')
        if not commander.processes(commands):
            break
    print ("Goodbye...")

if __name__ == "__main__":
    print ("""
halfMug 1.0.0 {}
by Anwar aalruwai@stevens.edu
User can provide an account, if the account doesn't exist, a new one will be created otherwise
it will be added to the same user's account if the user exist.

..Use 'quit' to quit the program.

..Use 'help' to get more information.

COMMAND arguments - input help for more information
""".format(time.strftime("%c")))

    commander = Commands()
    looping(commander)


