"""
/**********************************************************
	
	Organization	:Dona Ana Cycle Salvage
					 915 Dona Ana Rd., Las Cruces, NM 88007
					 (575) 526-8278
	
	Website			:http://www.dacyclesalvage.com
					
    License         :GPLv3

***********************************************************/
"""
import pygame
from pygame.locals import *
from spot import Spot

class Board(pygame.sprite.Group):
	def __init__(self,M,N,XC,YC,background_image,default_spot_image):
		pygame.sprite.Group.__init__(self)
		self.M=M
		self.N=N
		self.XC=XC#this is 974/2
		self.YC=YC
		self.default_spot_image=default_spot_image

		if background_image and not default_spot_image:self.make_background_spots(background_image)
		elif default_spot_image and not background_image:self.make_default_spots(default_spot_image)
		else:self.make_invisible_spots(None)

	def check4guest(self,m,n):
		#print 'check4guest:',m,n
		if m<0 or m>self.M-1 or n<0 or n>self.N-1:return(0)
		spot=self.get_spotMN(m,n)
		if spot.guest==None:return(0)
		else:return(1)
		
	def get_listofheads(self):
		heads=[]
		for spot in self.sprites():
			if spot.guest:
				if spot.AMHEAD:heads.append(spot)
		return(heads)			
	
	def clear_spots(self):
		for spot in self.sprites():
			spot.remove(self)
	
	def get_spotMN(self,m,n):
		for spot in self.sprites():
			MN=spot.getMN()
			if MN[0]==m and MN[1]==n:
				return(spot)
	
	def take_guestMN(self,tile,m,n):
		#print 'take_guestMN:',tile,m,n
		for spot in self.sprites():
			MN=spot.getMN()
			if MN[0]==m and MN[1]==n:
				spot.take_guest(tile,1)
				return(spot)
	
	def get_guest_by_str(self,str_val):
		#this function TuxTray->Submission ('getting' from Tux Tray)
		for spot in self.sprites():
			if spot.guest and spot.guest.str_val==str_val:
				return spot.pop_guest()
		return(None)
			
	def get_spots(self):
		#this function is boardspots
		return(self.sprites())
	
	#SPOT MAKERS:
	def make_background_spots(self,background_image):
		#print 'make_background_spots'
		for midx in range(self.M):
			for nidx in range(self.N):
				#print 'need to break-up background image!'
				self.add(Spot(default_spot_image,midx,nidx))#change to background_tile
	
	def make_default_spots(self,default_spot_image):
		#print 'make_default_spots'
		XC=self.XC
		YC=self.YC
		M=self.M
		N=self.N
		
		for midx in range(0,M):
			for nidx in range(0,N):
				spot=Spot(default_spot_image,midx,nidx)
				w=spot.image.get_width()
				h=spot.image.get_height()
				spot.rect.center=(	XC,YC	)
				#print spot.rect.center
				self.add(spot)
	
	def make_invisible_spots(self,invisible):#instantiate with invisible="None"
		#print 'make_invisible_spots'
		for midx in range(self.M):
			for nidx in range(self.N):
				self.add(Spot(invisible,midx,nidx))
	
	
	#def localize(self,submission):
	#	print 'board.localize:',submission
	#	return(1)
		
		
