#!/usr/bin/env python
import os
from lib.args import arg_parser

''' set abspath of directory app '''
fullpath = os.path.dirname(os.path.realpath(__file__))

if __name__ == '__main__':
  arg_parser(fullpath=fullpath)