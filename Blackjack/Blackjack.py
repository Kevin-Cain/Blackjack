import pygame
import math
import string
import os
from random import randrange


""" SETUP DISPLAY """
pygame.init()								      
WIDTH, HEIGHT = 1000, 750							# Making size of game					  
win = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('BLACKJACK') 	      # making app title
	

"""SOUNDS"""
jackpot = pygame.mixer.Sound('jackpot.wav')
intro = pygame.mixer.Sound("intro.wav")
chip_sound =  pygame.mixer.Sound("chip.wav")
card_sound =  pygame.mixer.Sound("card.wav")
bust_sound =  pygame.mixer.Sound("bust.wav")
shuffle_sound =  pygame.mixer.Sound("shuffle.wav")
double_sound = pygame.mixer.Sound("double.wav")
thankyou_sound = pygame.mixer.Sound("thankyou.wav")
win_sound = pygame.mixer.Sound("win.wav")


""" COLORS """
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (51, 102, 0)
RED = (255, 0, 0)



""" FONTS """
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)
TIED_FONT = pygame.font.SysFont('comicsans', 100)


""" LOAD IMAGES """
arrow = pygame.image.load("arrow.png")
arrow = pygame.transform.scale(arrow, (100, 75))

Frontlogo = pygame.image.load("Frontlogo.png")
Frontlogo = pygame.transform.scale(Frontlogo, (350, 200))

continue_button = pygame.image.load("continue.png")
continue_button = pygame.transform.scale(continue_button, (150, 150))

busted = pygame.image.load("bust.png")
busted = pygame.transform.scale(busted, (165, 110))

bankrupt = pygame.image.load("bankrupt.png")
bankrupt = pygame.transform.scale(bankrupt, (400, 250))

blackjack_21 = pygame.image.load("21.png")
blackjack_21 = pygame.transform.scale(blackjack_21, (180, 125))

loser = pygame.image.load("lost.png")
loser = pygame.transform.scale(loser, (165, 110))

winner = pygame.image.load("win.png")
winner = pygame.transform.scale(winner, (200, 165))

chip_20 = pygame.image.load("20.png")
chip_20 = pygame.transform.scale(chip_20, (165, 120))

chip_50 = pygame.image.load("50.png")
chip_50 = pygame.transform.scale(chip_50, (160, 115))

chip_100 = pygame.image.load("100.png")
chip_100 = pygame.transform.scale(chip_100, (105, 105))

card_back = pygame.image.load("gray_back.png")
card_back = pygame.transform.scale(card_back, (125, 150))

images = []
value = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
suit = ['C','D','H','S']
for i in value:
	for x in suit:
		image = pygame.image.load(i + x + ".png")
		image = pygame.transform.scale(image, (125, 150))
		images.append(image)


# Clock object  / Keep Track of time	

FPS = 60			
clock = pygame.time.Clock()	

class Blackjack(object):

	bankroll = 1000
	
	def __init__(self):
		self.intro()
		self.main() 

	def start_screen():
		win.fill(BLACK)
		win.blit(continue_button, (800, 550))
		pygame.mixer.Sound.play(intro)
		win.blit(Frontlogo, (100, 525))
		text = TITLE_FONT.render("WELCOME TO MY FIRST PROJECT!!!", 1, WHITE)
		win.blit(text, (80, 80))
		text = WORD_FONT.render("BLACKJACK BY KEVIN CAIN", 1, WHITE)
		win.blit(text, (200, 200))
		text = WORD_FONT.render("WRITTEN IN PYTHON", 1, WHITE)
		win.blit(text, (275, 300))

	def chips():
		win.blit(chip_20, (800, 150))
		win.blit(chip_50, (800, 272))
		win.blit(chip_100, (825, 400))

	def card_value(num):
		values = ['2','2','2','2','3','3','3','3','4','4','4','4','5','5','5','5','6','6','6','6','7','7','7','7','8','8','8','8','9','9','9','9','10','10','10','10','10','10','10','10','10','10','10','10','10','10','10','10','11','11','11','11']
		value = int(values[num])
		return value

	def deal_card():
		num = randrange(52)
		pygame.mixer.Sound.play(card_sound)
		return num	

	def dealNewCard(hand_value, cardWidth, cardHeight, width, height, person, scoreWidth, scoreHeight):
		num1 = Blackjack.deal_card()
		cardValue = Blackjack.card_value(num1)
		hand_value.append(cardValue)																	# Rendering word, '1' doesnt matter, color	
		win.blit(images[num1], (cardWidth, cardHeight))													# MOVING NEXT HIT CARD TO RIGHT
		pygame.draw.rect(win, GREEN, pygame.Rect(width, height, 50, 50))								# GREEN BOX OVER SCORE TO ADD NEXT SCORE OVER OLD ONE CLEANY
		text = LETTER_FONT.render(person + str(sum(hand_value)), 1, WHITE)								# DISPLAY PLAYER SCORE
		win.blit(text, (scoreWidth, scoreHeight))
		pygame.display.update()
		return hand_value

	def hit_button():
		pygame.draw.circle(win, BLACK, (425, 650), 65, 130)
		text = LETTER_FONT.render('HIT', 1, WHITE)
		win.blit(text, (WIDTH/2-100, HEIGHT/2+265))

	def stay_button():
		pygame.draw.circle(win, BLACK, (575, 650), 65, 130)
		text = LETTER_FONT.render('STAY', 1, WHITE)
		win.blit(text, (WIDTH/2+43, HEIGHT/2+265))

	def deal_button():
		pygame.draw.circle(win, BLACK, (275, 650), 65, 130)
		text = LETTER_FONT.render('DEAL', 1, WHITE)
		win.blit(text, (242, 640))

	def double_button():
		pygame.draw.circle(win, BLACK, (125, 650), 65, 130)
		text = LETTER_FONT.render('DOUBLE', 1, WHITE)
		win.blit(text, (68, 640))

	def click_position(xx, yy, zz):
		mouse = pygame.mouse.get_pos()
		x = pygame.mouse.get_pos()[0]
		y = pygame.mouse.get_pos()[1]
		sqx = (x - xx)**2
		sqy = (y - yy)**2
		if math.sqrt(sqx + sqy) < zz:
			pygame.mixer.Sound.play(chip_sound)
			return True
		else:
			return False

	def betScreen(bet, bankroll):
		win.fill(GREEN)
		text = LETTER_FONT.render('BET:  '+ '$ ' + str(bet), 1, WHITE)		
		win.blit(text, (700, 580))
		text = LETTER_FONT.render('BANKROLL:  '+ '$ ' + str(bankroll), 1, WHITE)			
		win.blit(text, (700, 650))
		Blackjack.chips()
		Blackjack.double_button()
		Blackjack.hit_button()
		Blackjack.stay_button()
		Blackjack.deal_button()
		pygame.display.update()

	def swap_11(hand_value, width, height, textWidth, textHeight, person):
		pygame.draw.rect(win, GREEN, pygame.Rect(width, height, 50, 50))
		hand_value.remove(11)
		hand_value.append(1)													
		text = LETTER_FONT.render(person + str(sum(hand_value)), 1, WHITE)
		win.blit(text, (textWidth, textHeight))
		pygame.display.update()

	def betValueRefresh(bet):
		pygame.draw.rect(win, GREEN, pygame.Rect(796, 570, 75, 50))
		text = LETTER_FONT.render('BET:  '+ '$ ' + str(bet), 1, WHITE)		
		win.blit(text, (700, 580))
		pygame.display.update()

	def whoWins(self, dealer_start_score, handValueList, outcomeWidth, outcomeheight, bet_win, bet_tied):
		if sum(dealer_start_score) > 21 and sum(handValueList) <= 21:
			win.blit(winner, (outcomeWidth, outcomeheight)) 
			pygame.mixer.Sound.play(win_sound)					              
			pygame.display.update()
			self.bankroll += bet_win
		if sum(dealer_start_score) <= 21 and sum(handValueList) <= 21:
			if 21 - sum(dealer_start_score) < 21 - sum(handValueList):
				win.blit(loser, (outcomeWidth, outcomeheight))												               
				pygame.display.update()
			if sum(dealer_start_score) == sum(handValueList):
				text = TIED_FONT.render('TIED', 1, BLACK)
				win.blit(text, (outcomeWidth, outcomeheight))					              
				pygame.display.update()
				self.bankroll += int(bet_tied)
			if 21 - sum(dealer_start_score) > 21 - sum(handValueList):
				win.blit(winner, (outcomeWidth, outcomeheight))
				self.bankroll += bet_win
				pygame.mixer.Sound.play(win_sound)
				pygame.display.update()

	def dealerPlayout(start_hand_value, splitHand2, dealer_start_score, dealerCardWidth):
		while sum(dealer_start_score) < 17:
			Blackjack.dealNewCard(dealer_start_score, dealerCardWidth, 75, 180, 85, 'DEALER: ', 50, 100)
			dealerCardWidth += 65
			if sum(dealer_start_score) > 21:
				if 11 in dealer_start_score:
					Blackjack.swap_11(dealer_start_score, 180, 85, 50, 100, 'DEALER: ')
					pygame.time.delay(1000)
				else:
					break
			pygame.time.delay(1000)

	def split_button(circleWidth, text, color, textWidth):
		pygame.draw.circle(win, WHITE, (circleWidth, 305), 35, 75)
		text = TITLE_FONT.render(text, 1, color)
		win.blit(text, (textWidth, 285))
		pygame.display.update()

	def hit(handList, CardWidth_name, CardHeight_name, rectangleWidth, rectangleHeight, person, swapTextWidth, swapTextHeight, bustedWidth, bustedHeight):
		Blackjack.dealNewCard(handList, CardWidth_name, CardHeight_name, rectangleWidth, rectangleHeight, person, swapTextWidth, swapTextHeight)
		if sum(handList) > 21:
			if 11 in handList:
				Blackjack.swap_11(handList, rectangleWidth, rectangleHeight, swapTextWidth, swapTextHeight, person)
				return
			else:
				win.blit(busted, (bustedWidth, bustedHeight)) 					               
				pygame.display.update()
				pygame.time.delay(1000)
				return 'busted'
		elif sum(handList) == 21:
			return 'busted'
		else:
			return

	def intro(self):

		""" INTRO SCREEN / ABOUT """

		clock.tick(FPS)
		while True:
			event = pygame.event.wait()
			Blackjack.start_screen()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if Blackjack.click_position(850, 650, 100) == True:		
					pygame.mixer.Sound.stop(intro)
					break
			pygame.display.update()

	def betRound(self):

		""" Betting Screen """

		bet = 0
		while self.bankroll > 0:
			event = pygame.event.wait()
			Blackjack.betScreen(bet, self.bankroll)		

			if event.type == pygame.QUIT:					
				pygame.quit()

			# IF CLICK == BET 20

			if event.type == pygame.MOUSEBUTTONDOWN:
				if Blackjack.click_position(880, 210, 55) == True:
		 			if bet + 20 <= self.bankroll:
		 				bet += 20
				
		   # IF CLICK == bet 50

			if event.type == pygame.MOUSEBUTTONDOWN:
				if Blackjack.click_position(880, 330, 55) == True:
					if bet + 50 <= self.bankroll:
						bet += 50

			# IF CLICK == bet 100

			if event.type == pygame.MOUSEBUTTONDOWN:
				if Blackjack.click_position(878, 460, 55) == True:
					if bet + 100 <= self.bankroll:
						bet += 100
		
			# IF CLICK == DEAL

			if event.type == pygame.MOUSEBUTTONDOWN:
				if Blackjack.click_position(275, 650, 65) == True:	
					self.bankroll -= bet
					pygame.mixer.Sound.play(shuffle_sound)
					pygame.draw.rect(win, GREEN, pygame.Rect(900, 640, 100, 50))
					text = LETTER_FONT.render('BANKROLL:  '+ '$ ' + str(self.bankroll), 1, WHITE)			
					win.blit(text, (700, 650))
									
					playerCardWidth = 490
					playerCardHeight = 375
					dealerCardWidth = 430

					dealer_start_score = []
					start_hand_value = []
					
					""" TESTING """

					# num1 = (INSERT NUMBERS HERE 1-51 FOR TESTING)
					# num2 = (INSERT NUMBERS HERE 1-51 FOR TESTING)

					""" DEALING FIRST CARDS """

					num1 = Blackjack.deal_card()                # COMMENT OUT LINE FOR TESTING
					cardValue1 = Blackjack.card_value(num1)
					start_hand_value.append(cardValue1)																	
					win.blit(images[num1], (355, 375))

					pygame.display.update()
					pygame.time.delay(500)

					dealer_start_score = Blackjack.dealNewCard(dealer_start_score, 355, 75, 180, 85, 'DEALER: ', 50, 100)
					pygame.time.delay(500)

					num2 = Blackjack.deal_card()               # COMMENT OUT LINE FOR TESTING
					cardValue2 = Blackjack.card_value(num2)
					start_hand_value.append(cardValue2)																	
					win.blit(images[num2], (430, 375))

					pygame.draw.rect(win, GREEN, pygame.Rect(170, 385, 50, 50))								
					text = LETTER_FONT.render('PLAYER: ' + str(sum(start_hand_value)), 1, WHITE)							
					win.blit(text, (50, 400))
					pygame.display.update()
					pygame.time.delay(500)

					win.blit(card_back, (430, 75))
					pygame.display.update()


					if sum(start_hand_value) > 21:														# CHECKING FOR 2 ACES
							Blackjack.swap_11(start_hand_value, 170, 385, 50, 400, 'PLAYER: ')
	
					""" IF PLAYER HAS BLACKJACK """

					if sum(start_hand_value) == 21:
						Blackjack.dealNewCard(dealer_start_score, dealerCardWidth, 75, 180, 85, 'DEALER: ',50, 100)
						if 21 - sum(dealer_start_score) > 21 - sum(start_hand_value):
							win.blit(blackjack_21, (360, 235))
							pygame.mixer.Sound.play(jackpot)
							self.bankroll += int(bet * 2.5)
						pygame.display.update()
						pygame.time.delay(2000)
						bet = 0		
						continue

					""" MAIN LOOP """

					while True:

						""" IF SPLIT BUTTON IS PUSHED """
						if start_hand_value[0] == start_hand_value[1] and (bet*2) < self.bankroll:
							text = TIED_FONT.render('SPLIT ?', 1, BLACK)
							win.blit(text, (200,275))
							Blackjack.split_button(540, 'Y', GREEN, 523)	
							Blackjack.split_button(630, 'N', RED, 613)				          
							while True:
								event = pygame.event.wait()
								if event.type == pygame.MOUSEBUTTONDOWN:						
									if Blackjack.click_position(630, 305, 35) == True:
										pygame.draw.rect(win, GREEN, pygame.Rect(175, 250, 500, 100))
										pygame.display.update()
										break
								if event.type == pygame.MOUSEBUTTONDOWN:						
									if Blackjack.click_position(540, 305, 35) == True:
										pygame.draw.rect(win, GREEN, pygame.Rect(25, 250, 750, 300))
										self.bankroll -= bet
										pygame.draw.rect(win, GREEN, pygame.Rect(900, 640, 100, 50))
										text = LETTER_FONT.render('BANKROLL:  '+ '$ ' + str(self.bankroll), 1, WHITE)			
										win.blit(text, (700, 650))
										bet += bet
										Blackjack.betValueRefresh(bet)


										# SPLITTING CARDS AND MAKING ANOTHER HAND LIST 

										win.blit(images[num1], (130, 260))																							
										text = LETTER_FONT.render('HAND: ' + str(start_hand_value[0]), 1, WHITE)
										win.blit(text, (30, 475))

										splitHand2 = []
										x = start_hand_value.pop(1)
										splitHand2.append(x)

										win.blit(images[num2], (450, 260))																							
										text = LETTER_FONT.render('HAND: ' + str(splitHand2[0]), 1, WHITE)
										win.blit(text, (365, 475))
										pygame.display.update()
										pygame.time.delay(500)
										

										# HITTING EACH HAND ONCE
										Blackjack.dealNewCard(start_hand_value, 150, 280, 120, 470, 'HAND: ', 30, 475)
										pygame.display.update()
										pygame.time.delay(500)
										

										Blackjack.dealNewCard(splitHand2, 470, 280, 455, 470, 'HAND: ', 365, 475)
										win.blit(arrow, (10,300))
										pygame.display.update()

										""" FIRST HAND LOOP """

										hand1CardWidth = 170
										hand1CardHeight = 300
										while True:
											event = pygame.event.wait()
											if event.type == pygame.QUIT:         	# Exiting / Quitting Game if red x clicked
												pygame.quit()

											""" IF HIT BUTTON PUSHED """
											if event.type == pygame.MOUSEBUTTONDOWN:
												if Blackjack.click_position(425, 650, 65) == True:						
													if Blackjack.hit(start_hand_value, hand1CardWidth, hand1CardHeight, 120, 470, 'HAND: ', 30, 475, 120, 300) == 'busted':
														break
													hand1CardWidth += 20
													hand1CardHeight += 20

											""" IF STAY BUTTON PUSHED """
											if event.type == pygame.MOUSEBUTTONDOWN:
												if Blackjack.click_position(575, 650, 65) == True:
													break
										
										""" SECOND HAND LOOP """

										hand2CardWidth = 490
										hand2CardHeight = 300
										while True:
											win.blit(arrow, (340, 300))
											pygame.draw.rect(win, GREEN, pygame.Rect(10, 300, 100, 100))
											pygame.display.update()
											event = pygame.event.wait()
											if event.type == pygame.QUIT:         	
												pygame.quit()

											""" IF HIT BUTTON PUSHED """

											if event.type == pygame.MOUSEBUTTONDOWN:
												if Blackjack.click_position(425, 650, 65) == True:	
													if Blackjack.hit(splitHand2, hand2CardWidth, hand2CardHeight, 455, 470, 'HAND: ', 365, 475, 450, 300) == 'busted':
														break
													hand2CardWidth += 20
													hand2CardHeight += 20									

											""" IF STAY BUTTON PUSHED """	

											if event.type == pygame.MOUSEBUTTONDOWN:
												if Blackjack.click_position(575, 650, 65) == True:
													break
															
											""" DEALER PLAY OUT """	

										if sum(start_hand_value) > 21 and sum(splitHand2) > 21:	
											Blackjack.dealNewCard(dealer_start_score, dealerCardWidth, 75, 180, 85, 'DEALER: ', 50, 100)	
										else:	
											Blackjack.dealerPlayout(start_hand_value, None, dealer_start_score, dealerCardWidth)
								
										""" CHECKING WHO WON HAND 1 """

										Blackjack.whoWins(self, dealer_start_score, start_hand_value, 125, 300, bet, (bet/2))

										""" CHECKING HAND 2 OUTCOME """

										Blackjack.whoWins(self, dealer_start_score, splitHand2, 450, 300, bet, (bet/2))
										pygame.time.delay(2000)
										return
										
												  
						""" MAIN LOOP IF SPLIT != TRUE """

						while True:
							event = pygame.event.wait()
							if event.type == pygame.QUIT:         	# Exiting / Quitting Game if red x clicked
								pygame.quit()

							""" IF HIT BUTTON PUSHED """

							if event.type == pygame.MOUSEBUTTONDOWN:
								if Blackjack.click_position(425, 650, 65) == True:	
									if Blackjack.hit(start_hand_value, playerCardWidth, playerCardHeight, 170, 385, 'PLAYER: ', 50, 400, 350, 250) == 'busted':
										break
									playerCardWidth += 65


							""" IF STAY BUTTON PUSHED """

							if event.type == pygame.MOUSEBUTTONDOWN:
								if Blackjack.click_position(575, 650, 65) == True:
									break

							""" IF DOUBLE BUTTON IS PUSHED """

							if event.type == pygame.MOUSEBUTTONDOWN:						
								if Blackjack.click_position(125, 650, 65) == True:
									if self.bankroll >= bet:
										if len(start_hand_value) == 2:					
											pygame.mixer.Sound.play(double_sound)
											self.bankroll -= bet
											bet += bet 
											Blackjack.betValueRefresh(bet)
											pygame.draw.rect(win, GREEN, pygame.Rect(900, 640, 100, 50))
											text = LETTER_FONT.render('BANKROLL:  '+ '$ ' + str(self.bankroll), 1, WHITE)	
											win.blit(text, (700, 650))
											if sum(Blackjack.dealNewCard(start_hand_value, playerCardWidth, 375, 170, 385, 'PLAYER: ', 50, 400)) > 21:
												Blackjack.swap_11(start_hand_value, 170, 385, 50, 400, 'PLAYER: ')
											break
							
						""" DEALER PLAY OUT """

						if sum(start_hand_value) > 21:	
							Blackjack.dealNewCard(dealer_start_score, dealerCardWidth, 75, 180, 85, 'DEALER: ', 50, 100)
						else:
							Blackjack.dealerPlayout(start_hand_value, None, dealer_start_score, dealerCardWidth)

						""" CHECKING WHO WON """

						Blackjack.whoWins(self, dealer_start_score, start_hand_value, 360, 250, (bet * 2), bet)
						pygame.time.delay(2000)
						bet = 0		
						return
									
						
		Blackjack.bankruptScreen()

	def bankruptScreen():

		""" EXIT SCREEN WHEN BANKROLL == 0 """
		pygame.mixer.Sound.play(thankyou_sound)
		win.fill(GREEN)
		win.blit(bankrupt, (300, 250))
		pygame.display.update()
		pygame.time.delay(2000)
		pygame.quit()

	def main(self):

		while True:
			Blackjack.betRound(self)


if __name__ == "__main__":
	Blackjack()