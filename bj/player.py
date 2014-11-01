"""
/**********************************************************
	
	Organization	:Dona Ana Cycle Salvage
					 915 Dona Ana Rd., Las Cruces, NM 88007
					 (575) 526-8278
	
	Website			:http://www.dacyclesalvage.com
					
    License         :GPLv3

***********************************************************/
"""
import math,time,os, pygame,sys
from pygame.locals import *

DEBUG=0
class Player:
	def __init__(self,*args):
		self.rules=args[0].rules
		try:self.parent=args[1]#only dealer has access to table directly
		except:pass
		self.betScheme=None
		self.balance=0.0
		self.earnings=0
		self.icon=None
		self.hands=[]
		self.hands.append(self.newHand())
		self.me=0
		self.amDealer=0
		self.moneyOnTable=None
		self.wonLastHand=0
		self.insurance=0
		self.win=0
	
	def set_win(self,val):
		self.win=val
	
	def get_win(self):
		return(self.win)
			
	def newHand(self):
		hand={}
		hand['isClosed']=0
		hand['blackjack']=0
		hand['total']=0
		hand['value']=0
		hand['cards']=[]
		hand['blackjack']=0
		hand['rule']=None
		hand['soft']=0
		hand['doubled']=0
		hand['busted']=0
		hand['upval']=None
		hand['bet']=0
		hand['win']=0
		return(hand)

	def checkForBlackjack(self,*args):
		handIdx=args[0]
		rule,col=self.getStrVal(self.hands[handIdx]['cards'],0,0)#called by players during deal to set Blackjack field
		if rule=='A10':return(1)
		else:return(None)

	def play(self,table,interactive):
		hands=self.hands
		while 1:
			open_count=0
			table.update()
			for handIdx in range(0,len(hands)):
				if not hands[handIdx]['isClosed']:open_count=open_count+1
			if open_count==0:break
			
			for handIdx in range(0,len(hands)):
				if len(hands[handIdx]['cards'])==1:
					hands[handIdx]['cards'].append(table.dealer.hit())
					hands[handIdx]['blackjack']=self.checkForBlackjack(handIdx)
					if hands[handIdx]['blackjack']==1:hands[handIdx]['isClosed']=1
							
				while hands[handIdx]['isClosed']!=1:
					time.sleep(table.global_config['TSLEEP_BTW_CARDS']['VALUE'])
					table.message_surface=None
					table.update()
					dealerCard=table.dealer.tell()		
					
					row,value=self.getStrVal(hands[handIdx]['cards'],self.amDealer,hands[handIdx]['value'])
					hands[handIdx]['value']=value
					soft=self.soft_total(hands[handIdx]['cards'],self.amDealer,hands[handIdx]['value'])
					if hands[handIdx]['value']>21 and soft<=21:hands[handIdx]['value']=soft
					
					
					col,dealerValue=self.getStrVal([dealerCard,],1,0)#tell getStrVal to evaluate dealerCard w/prevValue=0
					if hands[handIdx]['value']>=21:#	<-used to have "value>=21" here -- was hard to find bug!!
						rule='A'
						hands[handIdx]['rule']=rule
					else:
						if interactive==0:
							rule=self.getRule(row,col)
						else:
							flag=0
							BG=self.parent.global_config['COLOR_BG']['VALUE']
							HBG=self.parent.global_config['COLOR_HEADER_BG']['VALUE']
							
							table.message_surface=table.pyfont.render("Enter: A,S,D,H",1,BG,HBG)
							table.update()
							
							while 1:
								for event1 in pygame.event.get():
									if event1.type==KEYDOWN and event1.key==K_F1:
										self.parent.MODE=2
										self.parent.RUNNING=False
										flag=1
										return 2
									elif event1.type==KEYDOWN and event1.key==K_F12:
										pygame.display.toggle_fullscreen()
										self.parent.FULLSCREEN*=-1
									elif event1.type==KEYDOWN and event1.key==K_ESCAPE:
										self.parent.MODE=0
										self.parent.RUNNING=False
										flag=1
										return 0
									elif event1.type==KEYDOWN and event1.key==K_a:
										rule='A';flag=1
									elif event1.type==KEYDOWN and event1.key==K_h:
										rule='H';flag=1
									elif event1.type==KEYDOWN and event1.key==K_s:
										if hands[handIdx]['cards'][0].name[0]==hands[handIdx]['cards'][1].name[0]:
											rule='S';flag=1
										else:pass
									elif event1.type==KEYDOWN and event1.key==K_d:
										rule='D';flag=1
									elif event1.type==KEYDOWN and event1.key==K_t:
										rule='Ds';flag=1
									
								if flag==1:break
								table.update()
								
							hands[handIdx]['rule']=rule
							#table.message_surface=None
							table.update()
						
					#print "rule=%s"%rule
					#table.set_status_label(rule)
					if rule=='A':
						hands[handIdx]['isClosed']=1
						soft=self.soft_total(hands[handIdx]['cards'],self.amDealer,hands[handIdx]['value'])
						if value>21 and soft>21:
							hands[handIdx]['busted']=1
						elif value>21 and soft<=21:
							hands[handIdx]['value']=soft
						elif soft>value and soft<=21 and value<=21:
							hands[handIdx]['value']=soft
						table.update()
						break
						
					elif rule=='S':
						#print 'splitting'
						#get back hand of original index and "new hand" which need to append to hands:
						#hands[handIdx],newhand=table.split(hands[handIdx],table)
						newhand=self.newHand()
						newhand['bet']=hands[handIdx]['bet']
						newhand['cards'].append(hands[handIdx]['cards'].pop())
						hands.append(newhand)
						table.update()
						
						#update both after changing:
						#hit and update first hand
						card=table.dealer.hit()
						hands[handIdx]['cards'].append(card)
						row,value=self.getStrVal(hands[handIdx]['cards'],self.amDealer,0)
						hands[handIdx]['value']=value
						table.update()
						
					elif rule=='D' or rule=='Ds':
						if len(hands[handIdx]['cards'])==2:
							#print 'doubling-down'
							hands[handIdx]['bet']=2*hands[handIdx]['bet']
							#
							if interactive:
								bet_label="$%6.2f"%hands[handIdx]['bet']
								table.set_bet_label(bet_label)
							#
							hands[handIdx]['isClosed']=1
							hands[handIdx]['doubled']=1
							card=table.dealer.hit()
							card.isRotated=1
							hands[handIdx]['cards'].append(card)
							row,value=self.getStrVal(hands[handIdx]['cards'],self.amDealer,hands[handIdx]['value'])
							hands[handIdx]['value']=value
							table.update()
							
						elif rule=='Ds':
							#print 'can\'t double so standing'
							hands[handIdx]['isClosed']=1
							hands[handIdx]['rule']='A'
							rule='A'
						else:
							#print 'can\'t double so taking hit'
							hands[handIdx]['cards'].append(table.dealer.hit())
							row,value=self.getStrVal(hands[handIdx]['cards'],self.amDealer,hands[handIdx]['value'])
							hands[handIdx]['value']=value
							
					elif rule=='H':
						hands[handIdx]['cards'].append(table.dealer.hit())
						row,value=self.getStrVal(hands[handIdx]['cards'],self.amDealer,hands[handIdx]['value'])
						hands[handIdx]['value']=value
						if value>21:
							hands[handIdx]['busted']=1
							hands[handIdx]['isClosed']=1
						table.update()
							
					else:
						table.update()
						
					if (not self.amDealer) and (hands[handIdx]['isClosed']==1):
						soft=self.soft_total(hands[handIdx]['cards'],self.amDealer,hands[handIdx]['value'])#bug? if already softened
						if soft<hands[handIdx]['value']:
							pass
							#print 'hand closed @ %d'%(soft)
						else:pass#print 'hand closed @ %d'%(hands[handIdx]['value'])
						break
					
					elif (self.amDealer)&(hands[handIdx]['value']>=17):#dealer stands on 17
						hands[handIdx]['isClosed']=1
						#print 'dealer closed @ %s'%(hands[handIdx]['value'])
						break
		
		#table.message_surface=None
		table.update()
		val_string="returning; value=%d"%hands[0]['value']
		#print val_string
		return 1
					
	
	def getStrVal(self,*args):
		
		"""
		NOTE: this section could use re-writing.
		"""
		
		rule=None
		cards=args[0]
		isDealer=args[1]
		prevValue=args[2]
		numcards=len(cards)
		
		for i in range(0,len(cards)):
			equality="%s=%s"%(cards[i].name,cards[i].name[:-1]),
		
		if numcards==1:
			#being called for dealer upcard(gives col={0,1...8,A=9})
			if cards[0].name[:-1]=='A':
				v0=1
				col=9
				return(col,v0)
			elif cards[0].name[:-1]=='J':v0=10
			elif cards[0].name[:-1]=='Q':v0=10
			elif cards[0].name[:-1]=='K':v0=10
			else:v0=int(cards[0].name[:-1])
			col=`v0-2`
			return(col,v0)
		elif numcards==2:
			#vtot=v0+v1
			#get v0 exhaustively:
			if cards[0].name[:-1]=='A':
				if self.amDealer:v0=1
				else:v0=11
			elif cards[0].name[:-1]=='J':v0=10
			elif cards[0].name[:-1]=='Q':v0=10
			elif cards[0].name[:-1]=='K':v0=10
			else:v0=int(cards[0].name[:-1])
			#get V1 exhaustively:
			if cards[1].name[:-1]=='A':
				if self.amDealer:v1=1
				else:v1=11
			elif cards[1].name[:-1]=='J':v1=10
			elif cards[1].name[:-1]=='Q':v1=10
			elif cards[1].name[:-1]=='K':v1=10
			else:v1=int(cards[1].name[:-1])
			#get vtot:
			vtot=v0+v1#only way can be 2 is if dealer w/2 Aces
			if vtot==2:return('AA',vtot)#only dealer w/A
			elif v0==1:return(`vtot`,vtot)#only dealer w/A
			elif v1==1:return(`vtot`,vtot)#only dealer w/A
			elif vtot==22:return('AA',vtot)#only player w/A
			elif v0==11:return('A'+`v1`,vtot)
			elif v1==11:return('A'+`v0`,vtot)
			elif v0==v1 and cards[0].name[:-1]==cards[1].name[:-1]:return(`v0`+`v1`,vtot)#pair identical
			elif v0==v1:return(`vtot`,vtot)#(Q,10)
			else:return(`vtot`,vtot)#same as above condition
			
		else:
			if self.amDealer:
				return(`self.hard_total(cards,self.amDealer)`,self.hard_total(cards,self.amDealer))
			else:
				htot=self.hard_total(cards,self.amDealer)
				num_aces=0
				for card in cards:
					if card.name[:-1]=='A':num_aces=num_aces+1
				
				#current problem: want value=highest possible;
				if num_aces>0:
					total_minus_ace=htot
					for dummy in range(num_aces):
						total_minus_ace=total_minus_ace-10
						if htot<=21:return('A'+`total_minus_ace`,htot)
						if total_minus_ace<=10:
							return('A'+`total_minus_ace`,total_minus_ace)
					return(`total_minus_ace`,total_minus_ace)
				else:return(`htot`,htot)
		
	def hard_total(self,cards,isDealer):
		tot=0
		for card in cards:
			val=card.name[:-1]
			if val=='A':
				if self.amDealer==0:tot=tot+11
				else:tot=tot+1
			elif val=="J" or val=="Q" or val=="K":tot=tot+10
			else:tot=tot+int(val)
		return(tot)
		
		
	def soft_total(self,*args):
		cards=args[0]
		isDealer=args[1]
		value=args[2]
		strippedList=[]
		for i in range(0,len(cards)):
			strippedList.append(cards[i].strippedName)
		numA=strippedList.count('A')
		if numA==0:
			#print 'soft_total(1) returning ',value
			return(value)
		else:
			soft=self.hard_total(cards,isDealer)
			for i in range(0,numA):
				soft=soft-10
				if soft<=21:
					#print 'soft_total(2) returning ',soft
					return(soft)
			#print 'soft_total(3) returning ',soft
			return(soft)

	def getRule(self,r,c):
		#print 'getRule: ',r,c
		if c=='A':c=9
		else:c=int(c)-2
		try:rule=self.rules[r][c]
		except Exception,e:
			"""
			print "getRule.EXCEPTION",e
			print "r=%s\tc=%s"%(r,c)
			print "cards:",
			for i in range(len(self.hands[0]['cards'])):
				print self.hands[0]['cards'][i].name,
			print
			print "self.amDealer=%d"%(self.amDealer)
			print "dealer upcard:%s"%self.parent.dealer.tell().name
			"""
			#nothing=raw_input('hit enter to continue')
			rule='A'
		return(rule)	
		
	def placeBet(self,*args):
		handIdx=args[0]
		bet=args[1]
		self.hands[handIdx]['bet']=float(bet)


