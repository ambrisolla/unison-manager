#!/usr/bin/env python

'''
  dependencies: 
    - pyyaml
    - paramiko
    - requests
    
  pip3 install pyyaml paramiko requests
'''

import os
from lib.arguments import arg_parser

''' set abspath of directory app '''
fullpath = os.path.dirname(os.path.realpath(__file__))

if __name__ == '__main__':
  arg_parser(fullpath=fullpath)