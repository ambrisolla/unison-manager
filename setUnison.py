#!/usr/bin/env python
import os
from lib.args import arg_parser


#def setFullPath():
fullpath = os.path.abspath(os.path.realpath(__file__))
print(fullpath)
#if __name__ == '__main__':
#  arg_parser()