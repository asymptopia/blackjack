# -*- coding: UTF-8 -*-

import wx
from bj.wxadmin import *
from bj.blackjack import *

class BlackJackAppWX(wx.App):

	def __init__(self):
		#print 'BlackJackAppWX'
		wx.App.__init__(self, 0)
		prog=BlackJack(True)
		while True:
			mode=prog.run()
			#print 'mode=',mode
			if mode==0:break
			if mode==2:
				if prog.FULLSCREEN>0:
					pygame.display.toggle_fullscreen()
					prog.FULLSCREEN*=-1
				rval=prog.admin.ShowModal()
