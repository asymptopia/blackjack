"""
/**********************************************************
	
	Organization	:Dona Ana Cycle Salvage
					 915 Dona Ana Rd., Las Cruces, NM 88007
					 (575) 526-8278
	
	Website			:http://www.dacyclesalvage.com
					
    License         :GPLv3

***********************************************************/
"""
import pygame,os
from pygame.locals import *
from random import random
DEBUG=0

class Card(pygame.sprite.Sprite):
	def __init__(self,*args):
		pygame.sprite.Sprite.__init__(self)
		
		self.name=args[0]
		self.cfile=args[1]
		self.global_config=args[2]
		self.env=args[3]
		
		self.strippedName=self.name[:-1]#stip-off suit letter
		self.image=pygame.image.load(args[1])
		
		w_card=self.image.get_width()
		h_card=self.image.get_height()
		dx=14
		dy=11
		sf=self.global_config['CARD_SCALE_FACTOR']['VALUE']
		
		new_width=int(w_card*sf)
		new_height=int(h_card*sf)
		self.image=pygame.transform.smoothscale(self.image,(new_width,new_height))
		w_card=self.image.get_width()
		h_card=self.image.get_height()
		dx*=sf
		dy*=sf
		
		h_over=w_card-dx-dx
		w_over=h_card-dy-dy
		aspect_over=w_over/float(h_over)#1.69
		#print aspect_over
		
		img_fname=os.path.join(self.env.sitepkgdir,self.global_config['IMG_OVERLAY']['PATH'],self.global_config['IMG_OVERLAY']['VALUE'])
		mx_img=pygame.image.load(img_fname)
		mx_aspect=mx_img.get_width()/float(mx_img.get_height())#1.64
		#print mx_aspect
		
		new_width=None
		new_height=None
		if mx_aspect<aspect_over:
			#print 'clamp to height; mx_height->h_over'
			new_height=int(h_over)
			new_width=int(mx_img.get_width()*new_height/float(mx_img.get_height()))
		else:
			#print 'clamp to width: mx_width->w_over'
			new_width=int(w_over)
			new_height=int(mx_img.get_height()*new_width/float(mx_img.get_width()))
		
		mx_img=pygame.transform.smoothscale(mx_img,(new_width,new_height))
		
		bg_surf=pygame.Surface((int(sf*76),int(sf*46)))
		bg_surf=pygame.Surface((w_over,h_over))
		bg_surf.fill((255,255,255))
		
		if mx_aspect<aspect_over:
			bg_surf.blit(mx_img,(w_over/2-new_width/2,0))
		else:
			bg_surf.blit(mx_img,(0,h_over/2-new_height/2))
		
		bg_surf=pygame.transform.rotate(bg_surf,90.)
		
		self.image.blit(bg_surf,(dx,dy))
		
		self.default_image=self.image
		self.isUp=1
		self.isRotated=0
		
	def turnDown(self):
		self.isUp=0	
	def turnUp(self):
		self.isUp=1

		
class Deck:
	def __init__(self,*args):
		self.global_config=args[0]
		self.env=args[1]
		self.ndecks=self.global_config['NUM_DECKS']['VALUE']
		#self.ndecks=args[0]
		deckpath=os.path.join(self.env.sitepkgdir,self.global_config['IMG_CARD']['PATH'])
		suits=['c','s','h','d']
		members=['A','K','Q','J','10','9','8','7','6','5','4','3','2']
		deck=[]
		for i in range(0,self.ndecks):
			idx=0
			for cnum in range(1,14):
				for suit_idx in range(0,4):
					idx=idx+1
					val=members[cnum-1]
					name=val+suits[suit_idx]
					cfile=os.path.join(deckpath,`idx`+'.png')
					#if DEBUG:print val,name,cfile
					card=Card(name,cfile,self.global_config,self.env)
					deck.append(card)
		self.deck=deck
		
		
	def shuffle(self,deck):
		tmp1=[]
		tmp2=[]
		try:
			#cut deck:
			cut=int(random()*len(deck))
			for i in range(0,cut):
				tmp1.append(deck[i])
			for i in range(cut,len(deck)):
				tmp2.append(deck[i])
			deck=[]
			#fold together->deck:
			while 1:
				n=int(random()*3)
				for i in range(0,n):
				   try:
					card=tmp1.pop()
					deck.append(card)
				   except:continue
				n=int(random()*3)
				for i in range(0,n):
				   try:
					card=tmp2.pop()
					deck.append(card)
				   except:continue
				if (len(tmp1)==0)|(len(tmp2)==0):break

			#append the rest:
			try:
				for i in range(0,len(tmp1)):
					card=tmp1.pop()
					deck.append(card)
			except:pass
			try:
				for i in range(0,len(tmp2)):
					card=tmp2.pop()
					deck.append(card)
			except:pass
		except:print 'deck: shuffle error!'
		return(deck)

	def place_yellow(self,deck):
		ndecks=self.ndecks
		loc=52*max(1,(ndecks-1))-30
		try:
			idx=deck.index('yellow')
			yellow=deck.pop(idx)
		except:
			yellow='yellow'
		if(loc<len(deck)):
			deck.insert(loc,yellow)
		else:
			deck.append(yellow)
		#print 'YELLOW CARD PLACED AT: %s loc=%d count(yellow)=%d len(deck)=%d'%(deck.index('yellow'),loc,deck.count('yellow'),len(deck))
		return(deck)

