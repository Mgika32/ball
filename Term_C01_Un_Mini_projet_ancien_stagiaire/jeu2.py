import pygame
import math
from random import *

pygame.init()
clock = pygame.time.Clock()

largeur = 638
hauteur = 320
screen = pygame.display.set_mode((largeur, hauteur))

class Ball:
	def __init__(self):
		self.img = pygame.image.load('img/balle.png').convert_alpha()
		self.x = random()*largeur-55
		self.y = random()*hauteur-55
		self.angle = 2*math.pi*random()
		self.deltax = 5*math.cos(self.angle)
		self.deltay = 5*math.sin(self.angle)
		self.pos= (self.x, self.y)
	def click_on_ball(pos_ball : tuple[str, str], pos_click: tuple[str, str]):
		return
	def collide(self, other):
		distance = math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
		return distance < 50

score = 0
		
	


liste_balle = [Ball() for _ in range(10)]

fond = pygame.image.load('img/fond.jpg').convert()
font = pygame.font.Font('font/elite.ttf', 16) 

WHITE = pygame.Color(255, 255, 255)
text = font.render(f'score= {score} ', True, WHITE) 

continuer = True
touch = False
while continuer:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			continuer = False
		if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
			continuer = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			(click_x, click_y) = event.pos
			for i in liste_balle:
				if math.sqrt((i.x-click_x)**2 + (i.y-click_y)**2)<55:
					liste_balle.remove(i)
					score += 1
					liste_balle.append(Ball())
					touch = True
					break
				else :
					touch = False
			if touch  == False:
				score -= 1
				touch = True

			
	for i in range(len(liste_balle)):
		for j in range(i + 1, len(liste_balle)):
			if liste_balle[i].collide(liste_balle[j]):
				liste_balle[i].deltax, liste_balle[j].deltax = liste_balle[j].deltax, liste_balle[i].deltax
				liste_balle[i].deltay, liste_balle[j].deltay = liste_balle[j].deltay, liste_balle[i].deltay
	
	for elem in liste_balle:
		elem.x = elem.x + elem.deltax
		elem.y = elem.y + elem.deltay
		elem.pos = (elem.x, elem.y)
	
	for elem in liste_balle:
		if (elem.x>largeur-50 and elem.deltax>0) or (elem.x<0 and elem.deltax<0):
			elem.deltax = -elem.deltax
		elif (elem.y>hauteur-50 and elem.deltay>0) or (elem.y<0 and elem.deltay<0):
			elem.deltay = -elem.deltay


	screen.blit(fond, (0,0))
	screen.blit(font.render(f'score= {score} ', True, WHITE), (490,300))
	for elem in liste_balle: 
		screen.blit(elem.img, (elem.x, elem.y))
		

	pygame.display.update()
	clock.tick(50)
