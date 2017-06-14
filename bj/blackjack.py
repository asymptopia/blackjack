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
import time,sys
from pygame.locals import *
from bj.environment import *
from bj.rules import *
from bj.dealer import *
from bj.player import *
from bj.cards import *
from bj.board import *
from bj.spot import *

class BlackJackApp:
	def __init__(self):
		#print 'BlackJackApp'
		prog=BlackJack(False)
		while True:
			mode=prog.run()
			if mode==0:break
			if mode==2:
				msg="admin requires that you run with the -wx flag"
				prog.set_message(msg)
				prog.show_message()
				pygame.display.flip()
				time.sleep(2)
				
class BlackJack:
	def __init__(self,USE_WX):
		
		if USE_WX:
			import wxadmin
			from wxadmin import wxAdmin
	
		self.env=Environment('bj')
		self.env.USE_WX=False
		if USE_WX:self.env.USE_WX=USE_WX

		if self.env.OS=='win':
			os.environ['SDL_VIDEODRIVER'] = 'windib'
		pygame.display.init()
		pygame.init()
		pygame.event.set_blocked(MOUSEMOTION)
		
		self.FULLSCREEN=-1
		self.RUNNING=True
		self.MODE=0
		
		self.COVER_HAND_VALUES=None
		self.COVER_SCORES=None
		
		self.screen=None
		self.bkg=None
		self.header=None
		self.message_surface=None
		self.img_bg=None
		self.num_players=None
		self.player_list=None
		self.num_shuffle=None
		self.my_player_idx=None
		self.idx_who=0
		
		self.BG=None
		self.HBG=None
		self.SF=None
		self.dealer_tray=None
		self.trays=None
		self.trayspots=None
		self.dealer_trayspots=None
		
		self.status_label=None
		self.balance_label=None
		self.bet_label=None
		self.earnings_label=None
		self.pyfont=None
		
		self.t_last=time.time()
		self.clock = pygame.time.Clock()
		
		self.Deck=None
		self.deck=None
				
		self.red_spot=None
		self.face_down=None
		
		
		self.default_dealer_rules=None
		self.default_player_rules=None
		
		self.snd_shuffle=None
		self.snd_win=None
		self.snd_lose=None
		self.snd_push=None
		self.snd_blackjack=None
		
		self.global_config=self.load_config()
		self.update_global_config_dependents()
		
		pygame.display.set_caption(self.global_config['APPNAME']['VALUE'])
		
		self.admin=None
		if self.env.USE_WX:
			self.admin=wxAdmin(self)
			self.admin.setup()
		
		

		#for board in trays:
		#	print "(",board.XC,board.YC,")"
		
	def load_config(self):
		
		fontdir		=self.env.fontdir
		configdir	=self.env.configdir
		homedir=os.getenv('HOME')
		if not homedir:homedir=os.getenv('USERPROFILE')
		infname=os.path.join(homedir,'.blackjack_config')
		
		if not os.path.exists(infname):
			master_fname=os.path.join(fontdir,'dot_blackjack_config')
			if self.env.OS=='win':
				cmd="copy %s \"%s\""%(master_fname,os.path.join(homedir,'.blackjack_config'))
				os.system(cmd)
			else:
				cmd="cp %s %s"%(master_fname,os.path.join(homedir,'.blackjack_config'))
				os.system(cmd)
			
		inf=open(infname)
		content=inf.read()
		
		content=string.strip(content)
		
		config=eval(content)
		
		inf.close()
		return config

	def reload_configs(self):
		self.global_config=self.load_config()
		self.update_global_config_dependents()
		self.update()
	
	def set_status_label(self,msg):
		self.status_label=  "status  :%s"%msg
	def get_status_label(self):
		return self.status_label
	
	def set_balance_label(self,msg):
		self.balance_label="balance :%s"%msg
	def get_balance_label(self):
		return self.balance_label

	def set_bet_label(self,msg):
		self.bet_label="bet     :%s"%msg
	def get_bet_label(self):
		return self.bet_label

	def set_earnings_label(self,msg):
		self.earnings_label="earnings:%s"%msg
	def get_earnings_label(self):
		return self.earnings_label
				
	def run(self):
		self.MODE=0
		self.RUNNING=True
		
		self.set_status_label("Ready!")
		self.set_earnings_label("$  0.00")
		self.set_bet_label("$  0.00")
		self.set_balance_label("$  0.00")
		
		self.last_hand=True
		self.finish_hand=1
		
		player_list=self.player_list
		my_player_idx=self.my_player_idx
		num_players=self.num_players
		
		#clear out K1-up event
		for event in pygame.event.get():pass
		
		while self.RUNNING:
			
			self.COVER_SCORES=True
			
			if self.last_hand:
				
				self.message_surface=self.pyfont.render("Shuffling ...",1,self.BG,self.HBG)
				self.set_status_label("shuffling...")
				self.update()
				
				self.last_hand=0
				self.finish_hand=1
				self.discard_pile=[]
				self.Deck=Deck(self.global_config,self.env) #need ref to class for shuffle,place_yellow
				self.deck=self.Deck.deck
				self.snd_shuffle.play()
				
				
				for i in range(int(self.global_config['NUM_SHUFFLE']['VALUE'])):
					self.deck=self.Deck.shuffle(self.deck)
					
				self.deck=self.Deck.place_yellow(self.deck)
				self.set_status_label("  ready")
				self.update()
			
			self.set_earnings_label("$  0.00")
			self.set_bet_label("$  0.00")
			self.update()
			
			#_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
			#Manual Betting for playerList[myPlayerIdx]; everyone else betting $1/hand
			
			for i in range(len(player_list)):
				
				if not self.RUNNING:break
				
				if i==my_player_idx:
					self.idx_who=i
					
					self.set_status_label('place bet')
					self.update()
					
					self.message_surface=self.pyfont.render("Place Bet: $1 - $0 (0=10)",1,self.BG,self.HBG)
					self.show_message()
					pygame.display.flip()
					
					flag=0
					
					while 1:
						for event in pygame.event.get():
							#print event
							if event.type == (KEYUP or KEYDOWN) and event.key == K_ESCAPE:
								self.MODE=0
								self.RUNNING=False
								#print 'Exiting ... L227'
								flag=1
								return 0
							
							elif event.type==KEYDOWN and event.key==K_F12:
								pygame.display.toggle_fullscreen()
								self.FULLSCREEN*=-1
							
							elif event.type == KEYDOWN and event.key == K_F1:
								self.MODE=2
								self.RUNNING=False
								return 2
								flag=1
								
							elif event.type == KEYDOWN and event.key == K_1:
								player_list[my_player_idx].placeBet(0,1)
								flag=1
							elif event.type == KEYDOWN and event.key == K_2:
								player_list[my_player_idx].placeBet(0,2)
								flag=1
							elif event.type == KEYDOWN and event.key == K_3:
								player_list[my_player_idx].placeBet(0,3)
								flag=1
							elif event.type == KEYDOWN and event.key == K_4:
								player_list[my_player_idx].placeBet(0,4)
								flag=1
							elif event.type == KEYDOWN and event.key == K_5:
								player_list[my_player_idx].placeBet(0,5)
								flag=1
							elif event.type == KEYDOWN and event.key == K_6:
								player_list[my_player_idx].placeBet(0,6)
								flag=1
							elif event.type == KEYDOWN and event.key == K_7:
								player_list[my_player_idx].placeBet(0,7)
								flag=1
							elif event.type == KEYDOWN and event.key == K_8:
								player_list[my_player_idx].placeBet(0,8)
								flag=1
							elif event.type == KEYDOWN and event.key == K_9:
								player_list[my_player_idx].placeBet(0,9)
								flag=1
							elif event.type == KEYDOWN and event.key == K_0:
								player_list[my_player_idx].placeBet(0,10)
								flag=1
							else:pass
						
						self.update()
						time.sleep(.1)
						if flag==1:
							self.set_status_label('')
							break
				else:
					player_list[i].placeBet(0,1)
			
			self.message_surface=None	
			bet="$%6.2f"%player_list[my_player_idx].hands[0]['bet']
			self.set_bet_label(bet)
			self.update()
			self.dealer.deal()
			
			#_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
			
			self.idx_who=0
			for i in range(0,len(player_list)):
				self.idx_who=i
				card_rect=player_list[i].hands[0]['cards'][0].rect
				xc_card=card_rect[0]+card_rect[3]+5
				if i==my_player_idx:
					rval=player_list[i].play(self,1)
					if rval==2:return 2
					elif rval==0:return 0
				else:
					rval=player_list[i].play(self,0)
					if rval==2:return 2
					elif rval==0:return 0
				
			card_rect=self.dealer.hands[0]['cards'][0].rect
			xc_card=card_rect[0]+card_rect[3]-self.SF*25
			self.idx_who+=1
			self.dealer.hands[0]['cards'][1].turnUp()
			self.dealer.play(self,0)
			self.update()
			
			self.dealer.giveTakeMoney()
			
			for handIdx in range(len(player_list[my_player_idx].hands)):
				if player_list[my_player_idx].hands[handIdx]['blackjack']==1:
					self.set_status_label("BlackJack!")
					self.snd_blackjack.play()#should really be played when player takes turn...
				elif player_list[my_player_idx].hands[handIdx]['win']==1:
					self.set_status_label("you win")
					self.snd_win.play()
				elif player_list[my_player_idx].hands[handIdx]['win']==0:
					self.set_status_label("push")
					self.snd_push.play()
				else:
					self.set_status_label("bummer")
					self.snd_lose.play()
			
			balance="$%6.2f"%player_list[my_player_idx].balance
			earnings="$%6.2f"%player_list[my_player_idx].earnings
			self.set_balance_label(balance)
			self.set_earnings_label(earnings)
			
			
			#----------------------------------------------------------------------------
			self.COVER_SCORES=False
			self.show_hand_values()
			self.update()
			self.COVER_SCORES=True
			
			self.dealer.cleanup()#hand values zeroed here
			
			BG=self.BG
			HBG=self.HBG
			
			self.message_surface=self.pyfont.render("Press SpaceBar To Continue",1,BG,HBG)
			self.show_message()
			self.show_status()

			pygame.display.flip()
			
			#----------------------------------------------------------------------------
			
			#require spacebar for next hand:
			while(1):
				flag=0
				for event in pygame.event.get([KEYDOWN,KEYUP]):
					if event.type==KEYDOWN and event.key==K_SPACE:flag=1
					elif event.type==KEYDOWN and event.key==K_F12:
						pygame.display.toggle_fullscreen()
						self.FULLSCREEN*=-1
					elif event.type==KEYDOWN and event.key==K_ESCAPE:
						#print 'Exiting ... L326'
						return 0
					
					elif event.type == KEYDOWN and event.key == K_F10:
						display_surface=pygame.display.get_surface()
						pygame.image.save(display_surface,'blackjack_screenshot.bmp')
						#print 'wrote blackjack_screenshot.bmp'
					
					elif event.type==KEYDOWN and event.key==K_F1:
						#print 'launch admin ...'
						self.MODE=2
						self.RUNNING=False
						flag=1
						#print 'returning 2 L345'
						
				if flag==1:break
				time.sleep(.1)
				
			self.message_surface=None
				
		return self.MODE
	
	def set_message(self,msg):
		self.message_surface=self.pyfont.render(msg,1,self.BG,self.HBG)
			
	def show_message(self):
		if self.message_surface:
			tlcx=self.screen.get_width()/2-self.message_surface.get_width()/2
			tlcy=self.screen.get_height()/2
			self.screen.blit(self.message_surface,(tlcx,tlcy))
	
	def show_status(self):	
		status_label=self.get_status_label()
		status_surface=self.pyfont.render(status_label,1,self.BG,self.HBG)
		dy=status_surface.get_height()
		self.screen.blit(status_surface,(20,0))		
	
	def show_hand_values(self):
		try:
			for idx in range(self.num_players):
				value_str="%02d"%self.player_list[idx].hands[0]['value']
				surf=self.pyfont.render(value_str,1,self.BG,self.HBG)
				xc=int(self.trays[idx].XC-surf.get_width()/2)
				yc=int(self.trays[idx].YC + self.face_down.get_height())
				
				dx=5
				w=int(surf.get_width()+2*dx)
				h=int(surf.get_height()+2*dx)
				surf2=pygame.Surface((w,h))
				surf2.fill(self.global_config['COLOR_HILIGHT']['VALUE'])
				if idx==self.idx_who:
					self.screen.blit(surf2,(xc-dx,yc-dx))
				
				self.screen.blit(surf,(xc,yc))

				if self.COVER_HAND_VALUES:
					if self.COVER_SCORES:
						self.screen.blit(self.red_spot,(xc,yc))
				
				
				
			value_str="%02d"%self.dealer.hands[0]['value']
			surf=self.pyfont.render(value_str,1,self.BG,self.HBG)
			xc=self.dealer_tray.XC-surf.get_width()/2
			yc=self.dealer_tray.YC + self.face_down.get_height()
			self.screen.blit(surf,(xc,yc))
			if self.COVER_HAND_VALUES:
				if self.COVER_SCORES:
					self.screen.blit(self.red_spot,(xc,yc))
			
		except Exception,e:
			print e
			pass
	
	def update(self):
		
		self.clock.tick(80)
		if time.time()-self.t_last>0.05:pass
		else:return
		
		self.t_last=time.time()
		
		self.screen.blit(self.bkg,(0,0))
		self.screen.blit(self.header,(0,0))
		if self.img_bg:
			x=0;y=0
			if self.img_bg.get_width()<self.screen.get_width():
				x=self.screen.get_width()/2-self.img_bg.get_width()/2
			if self.img_bg.get_height()<(self.screen.get_height()-self.global_config['HEADER_H']['VALUE']):
				y=(self.screen.get_height()-self.global_config['HEADER_H']['VALUE'])/2-self.img_bg.get_height()/2
			self.screen.blit(self.img_bg,(x,self.global_config['HEADER_H']['VALUE']+y))
		
		BG=self.BG
		HBG=self.HBG
		
		self.show_message()
		self.show_status()		
		
		#just to get dy
		status_label=self.get_status_label()
		status_surface=self.pyfont.render(status_label,1,self.BG,self.HBG)
		dy=status_surface.get_height()
		
		bet_label=self.get_bet_label()
		bet_surface=self.pyfont.render(bet_label,1,BG,HBG)
		self.screen.blit(bet_surface,(20,dy))
		
		earnings_label=self.get_earnings_label()
		earnings_surface=self.pyfont.render(earnings_label,1,BG,HBG)
		self.screen.blit(earnings_surface,(20,2*dy))
		
		balance_label=self.get_balance_label()
		balance_surface=self.pyfont.render(balance_label,1,BG,HBG)
		self.screen.blit(balance_surface,(20,3*dy))
		
		player_list=self.player_list
		
		centers=[]
		for idx in range(len(self.trayspots)):
			self.trayspots[idx].draw(self.screen)
			#centers.append(self.trayspots[idx].get_center())
		
		for idx in range(self.num_players):
			for handIdx in range(0,len(player_list[idx].hands)):
				for nc in range(0,len(player_list[idx].hands[handIdx]['cards'])):
					card=player_list[idx].hands[handIdx]['cards'][nc]
					xc=self.trayspots[idx].sprites()[0].rect.centerx
					yc=self.trayspots[idx].sprites()[0].rect.centery
					card.rect=self.trayspots[idx].sprites()[0].rect.move(0,(-150*handIdx)-self.SF*25*nc)
					#target.add(playerList[idx].hands[handIdx]['cards'][nc])
					
					if card.isRotated:
						card.rect=card.rect.move(-25,0)
						self.screen.blit(pygame.transform.rotate(card.image,-90),(card.rect[0],card.rect[1]))
					else:
						#print card.rect[0],card.rect[1]
						xc=self.trays[idx].XC-card.image.get_width()/2
						yc=self.trays[idx].YC
						self.screen.blit(card.image,(xc,card.rect[1]))#xc,yc#card.rect[1]-100
		
		dealer=self.dealer
		for didx in range(len(dealer.hands[0]['cards'])):
			card=dealer.hands[0]['cards'][didx]
			card.rect=self.dealer_trayspots.sprites()[0].rect.move(self.SF*(-25)*didx,0)
			
			if card.isUp or dealer.hands[0]['isClosed']:
				self.screen.blit(card.image,(card.rect[0],card.rect[1]))
			else:
				#Face Down Card:
				self.screen.blit(self.face_down,(card.rect[0],card.rect[1]))
		
		self.show_hand_values()
		pygame.display.flip()
	
	def update_global_config_dependents(self):
		
		#ie adminbutton which is pygame.sprite.RenderPlain(Group..)
		self.screen=pygame.display.set_mode((int(self.global_config['WIN_W']['VALUE']),int(self.global_config['WIN_H']['VALUE'])))
		self.bkg=pygame.Surface(self.screen.get_size())
		self.bkg=self.bkg.convert()
		self.bkg.fill(self.global_config['COLOR_BG']['VALUE'])
		
		#SET DISPLAY MODE:
		if pygame.display.get_init():
			self.screen=pygame.display.set_mode((int(self.global_config['WIN_W']['VALUE']),int(self.global_config['WIN_H']['VALUE'])))
			self.bkg=pygame.Surface(self.screen.get_size())
			self.bkg=self.bkg.convert()
			self.bkg.fill(self.global_config['COLOR_BG']['VALUE'])
			pygame.font.init()

		#ATTEMPT TO LOAD IMG_BG:
		if self.global_config['IMG_BG']['VALUE']!='':
			try:
				fname=os.path.join(self.env.sitepkgdir,self.global_config['IMG_BG']['PATH'],self.global_config['IMG_BG']['VALUE'])
				#print fname
				self.img_bg=pygame.image.load(fname)
				self.img_bg.set_alpha(self.global_config['IMG_BG_ALPHA']['VALUE'])
				
				w=self.img_bg.get_width()
				h=self.img_bg.get_height()
				img_aspect=w/float(h)
				screen_aspect=self.screen.get_width()/float(self.screen.get_height()-self.global_config['HEADER_H']['VALUE'])
				
				if img_aspect>screen_aspect:#clamp to width
					new_w=self.screen.get_width()
					new_h=int(new_w/float(w)*h)
				else:#clamp to height
					new_h=self.screen.get_height()-self.global_config['HEADER_H']['VALUE']
					new_w=int(new_h/float(h)*w)
				
				self.img_bg=pygame.transform.smoothscale(self.img_bg,(new_w,new_h))
				
			except Exception,e:
				print e
				self.img_bg=None
		
		self.header=pygame.Surface((self.screen.get_width(),self.global_config['HEADER_H']['VALUE']))
		self.header.fill(self.global_config['COLOR_HEADER_BG']['VALUE'])
		
		self.num_players=self.global_config['NUM_PLAYERS']['VALUE']
		self.my_player_idx=self.global_config['MY_PLAYER_IDX']['VALUE']
		
		self.BG=self.global_config['COLOR_BG']['VALUE']
		self.HBG=self.global_config['COLOR_HEADER_BG']['VALUE']
		
		font_fname=os.path.join(self.env.sitepkgdir,self.global_config['FONT_FNAME']['PATH'],self.global_config['FONT_FNAME']['VALUE'])
		self.pyfont=pygame.font.Font(font_fname,24)
		
		self.face_down=pygame.image.load(os.path.join(self.env.sitepkgdir,self.global_config['IMG_DECK']['PATH'],self.global_config['IMG_DECK']['VALUE']))
		new_width=int(self.face_down.get_width()*self.global_config['CARD_SCALE_FACTOR']['VALUE'])
		new_height=int(self.face_down.get_height()*self.global_config['CARD_SCALE_FACTOR']['VALUE'])
		self.face_down=pygame.transform.smoothscale(self.face_down,(new_width,new_height))
		
		surf=self.pyfont.render("00",1,self.BG,self.HBG)#just to match size of red_spot
		red_spot = pygame.Surface((surf.get_width(),surf.get_height()))
		red_spot = red_spot.convert()
		red_spot.fill(self.HBG)
		self.red_spot=red_spot
		
		self.COVER_HAND_VALUES=self.global_config['COVER_HAND_VALUES']['VALUE']
		
		self.last_hand=None
		self.finish_hand=None
		self.discard_pile=None
		self.Deck=None
		self.deck=None
		self.SF=self.global_config['CARD_SCALE_FACTOR']['VALUE']
		self.my_player_idx=self.global_config['MY_PLAYER_IDX']['VALUE']
		self.num_shuffle_idx=self.global_config['NUM_SHUFFLE']['VALUE']
		
		pygame.mixer.pre_init()
		pygame.mixer.init()
		if not pygame.mixer or not pygame.mixer.get_init():sys.exit()
		
		fname_shuffle=os.path.join(self.env.sitepkgdir,self.global_config['SND_SHUFFLE']['PATH'],self.global_config['SND_SHUFFLE']['VALUE'])
		fname_win=os.path.join(self.env.sitepkgdir,self.global_config['SND_WIN']['PATH'],self.global_config['SND_WIN']['VALUE'])
		fname_lose=os.path.join(self.env.sitepkgdir,self.global_config['SND_LOSE']['PATH'],self.global_config['SND_LOSE']['VALUE'])
		fname_push=os.path.join(self.env.sitepkgdir,self.global_config['SND_PUSH']['PATH'],self.global_config['SND_PUSH']['VALUE'])
		fname_blackjack=os.path.join(self.env.sitepkgdir,self.global_config['SND_BLACKJACK']['PATH'],self.global_config['SND_BLACKJACK']['VALUE'])
		
		self.snd_shuffle=pygame.mixer.Sound(fname_shuffle)
		self.snd_win=pygame.mixer.Sound(fname_win)
		self.snd_lose=pygame.mixer.Sound(fname_lose)
		self.snd_push=pygame.mixer.Sound(fname_push)
		self.snd_blackjack=pygame.mixer.Sound(fname_blackjack)
		
		self.default_dealer_rules=DefaultDealerRules()
		self.dealer=Dealer(self.default_dealer_rules,self)
		
		self.default_player_rules=DefaultPlayerRules()
		self.player_list=[]
		self.num_players=self.global_config['NUM_PLAYERS']['VALUE']
		for i in range(self.num_players):
			self.player_list.append(Player(self.default_player_rules,self))
		
		#print 'self.player_list=',len(self.player_list)

		trays=[]
		trayspots=[]
		
		#First, the `num_players` players:
		W=self.global_config['WIN_W']['VALUE']
		H=self.global_config['WIN_H']['VALUE']+self.global_config['HEADER_H']['VALUE']
		
		fname=os.path.join(self.env.sitepkgdir,self.global_config['IMG_SPOT']['PATH'],self.global_config['IMG_SPOT']['VALUE'])
		dummy=pygame.image.load(fname)
		for idx in range(self.num_players):
			#trays.append(Board(1,1,W-(idx+1)*W/8,H-150,None,fname))
			XC=W-(idx+1)*W/(self.num_players+1)
			YC=self.screen.get_height()-self.SF*140
			trays.append(Board(1,1,XC,YC,None,fname))
			trayspots.append(pygame.sprite.RenderPlain(trays[idx].get_spots()))
		
		#Dealer is eighth player
		YC=self.global_config['HEADER_H']['VALUE']+dummy.get_height()
		dealer_tray=Board(1,1,W/2,YC,None,fname)
		dealer_trayspots=pygame.sprite.RenderPlain(dealer_tray.get_spots())
		trays.append(dealer_tray)
		trayspots.append(dealer_trayspots)
		
		self.dealer_tray=dealer_tray
		self.trays=trays
		self.trayspots=trayspots
		self.dealer_trayspots=dealer_trayspots
