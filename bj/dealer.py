"""
/**********************************************************

    Author          :Charlie Cosse

    Email           :ccosse_at_gmail_dot_com

    License         :GPLv3

***********************************************************/
"""
from bj.player import *

class Dealer(Player):

	def hit(self):
		#print 'DEALER HITTING'
		table=self.parent
		card=table.deck.pop(0)
		if card=='yellow':
			#print 'YELLOW CARD'
			table.last_hand=1
			#table.discardPile.append(card)
			card=table.deck.pop(0)
		table.update()
		#print 'dealer dealing:',card
		return(card)

	def tell(self):
		rval=self.hands[0]['cards'][0]
		return(rval)

	def checkDownForAce(self):
		#call after deal:if return(1), then nobody plays,just evaluate hand
		if self.getStrVal([self.hands[0]['cards'][1],],1,0)=='A':return(1)
		else:return(None)

	def checkForBlackjack(self,*args):
		handIdx=args[0]
		rule,col=self.getStrVal(self.hands[handIdx]['cards'],1,0)#override b/c dealer takes soft Aces
		if rule=='A10':return(1)
		else:return(None)

	def giveTakeMoney(self):
		table=self.parent
		players=table.player_list
		#print 'dealer giveTakeMoney'
		dealerHand=self.hands[0]['value']
		numPlayers=len(table.player_list)
		for i in range(0,numPlayers):
			player=table.player_list[i]
			for handIdx in range(0,len(player.hands)):

				total=player.hands[handIdx]['value']
				if (total>dealerHand)&(total<=21):win=1
				elif (dealerHand>21)&(total<=21):win=1
				elif (total==dealerHand)&(total<=21):win=0
				else:win=-1

				if player.hands[handIdx]['blackjack']:#blackjack only possible w/2 cards (i.e. on deal)
					earnings=1.5*player.hands[handIdx]['bet']
					win=1
				elif win==1:earnings=player.hands[handIdx]['bet']
				elif win==-1:earnings=win*player.hands[handIdx]['bet']
				else:earnings=0
				player.earnings=earnings
				player.balance=player.balance+earnings
				player.hands[handIdx]['win']=win
				#print win,earnings
				#if win==1:player.hands[handIdx]['win']=1
			#print "player[%d]: bal=%d"%(i,player.balance)


	def cleanup(self):
		table=self.parent
		deck=table.deck
		players=table.player_list
		for i in range(0,len(players)):
			for handIdx in range(0,len(players[i].hands)):
				for nc in range(0,len(players[i].hands[handIdx]['cards'])):
					table.discard_pile.append(players[i].hands[handIdx]['cards'].pop())
			del players[i].hands
			players[i].hands=[self.newHand(),]
		for nc in range(0,len(self.hands[0]['cards'])):
			table.discard_pile.append(self.hands[0]['cards'].pop())#dealCards->discardPile
		del self.hands
		self.hands=[self.newHand(),]
		try:pass#print "len(deck)=%d\tlen(discardPile)=%d \tsum=%d\tidx(yellow)=%d"%(len(table.deck),len(table.discardPile),len(table.deck)+len(table.discardPile),table.deck.index('yellow'))
		except:pass#print e,"(yellow no longer in deck)"

	def deal(self):
		table=self.parent
		deck=table.deck
		players=table.player_list
		#deal first 2 cards:
		for nc in range(0,2):
			for i in range(0,len(players)):
				card=self.hit()
				#print 'card=',card
				players[i].hands[0]['cards'].append(card)
				table.update()

			#dealer takes a card:
			card=self.hit()
			if nc==0:pass
			else:card.turnDown()
			self.hands[0]['cards'].append(card)
			table.update()

		for i in range(0,len(players)):
			players[i].hands[0]['blackjack']=players[i].checkForBlackjack(0)
		uprule,upvalue=self.getStrVal([self.hands[0]['cards'][0],],1,0)
		#print 'upvalue=',upvalue
		#Ace=self.checkDownForAce()
		if upvalue==10 or uprule=='A':
			#print '***INSURANCE?***'
			for i in range(0,len(players)):
				players[i].insurance=0#not implemented yet
		Blackjack=self.checkForBlackjack(0)#dealer's method wouldn't need args (since 1 hand only) but in case want to experiment...
		if Blackjack:
			table.finish_hand=0
			rule,value=self.getStrVal(self.hands[0]['cards'],1,0)#could just assign=21, but using function anyway...
			self.hands[0]['value']=value
		else:table.finish_hand=1
