#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os,sys,string,time
from bj.blackjack import *

def usage():
	msg="""
Usage: blackjack [OPTION]
	Available options are:
	-help			Show this help
	-wx				Enable the wx admin interface
	"""
	print(msg)
	

if __name__ == "__main__":
	appdir='bj'
	if len(sys.argv)==1:
		x=BlackJackApp()
	elif sys.argv[1]=='-help':
		usage()
	elif sys.argv.count('-wx')>0:
		from bj.blackjack_wx import *
		x=BlackJackAppWX()
	else:
		x=BlackJackApp()
	
