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
        self.color = choice(["white", "yellow", "red", "frozen", "explosive"])
        if self.color == "frozen":
            self.img = pygame.image.load('img/balle_frozen.png').convert_alpha()
            self.points = 0
            self.speed = 3
        elif self.color == "white":
            self.img = pygame.image.load('img/balle.png').convert_alpha()
            self.points = 1
            self.speed = 5
        elif self.color == "yellow":
            self.img = pygame.image.load('img/balle_yellow.png').convert_alpha()
            self.points = 3
            self.speed = 7
        elif self.color == "red":
            self.img = pygame.image.load('img/balle_red.png').convert_alpha()
            self.points = 5
            self.speed = 9
        elif self.color == "explosive":
            self.img = pygame.image.load('img/balle_explosive.png').convert_alpha()
            self.points = 2
            self.speed = 4
        self.x = random()*largeur-55
        self.y = random()*hauteur-55
        self.angle = 2*math.pi*random()
        self.deltax = self.speed*math.cos(self.angle)
        self.deltay = self.speed*math.sin(self.angle)
        self.pos= (self.x, self.y)
    def click_on_ball(pos_ball : tuple[str, str], pos_click: tuple[str, str]):
        return
    def collide(self, other):
        distance = math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
        return distance < 50

score = 0

fond = pygame.image.load('img/fond.jpg').convert()
font = pygame.font.Font('font/elite.ttf', 16) 

WHITE = pygame.Color(255, 255, 255)
def manage_high_scores(mode, score):
    filename = "high_scores.txt"
    scores = {}

    # Read existing scores
    try:
        with open(filename, "r") as file:
            for line in file:
                game_mode, high_score = line.strip().split(":")
                scores[game_mode] = int(high_score)
    except FileNotFoundError:
        pass

    if mode not in scores or score > scores[mode]:
        scores[mode] = score

        with open(filename, "w") as file:
            for game_mode, high_score in scores.items():
                file.write(f"{game_mode}:{high_score}\n")

    return scores.get(mode, 0)

def show_menu():
    menu_font = pygame.font.Font('font/elite.ttf', 32)
    classic_text = menu_font.render("Mode Classique", True, WHITE)
    speed_text = menu_font.render("Mode Rapide (50 balles)", True, WHITE)
    
    classic_button = pygame.Rect(100, 100, 400, 50)
    speed_button = pygame.Rect(100, 200, 400, 50)
    
    while True:
        screen.blit(fond, (0,0))
        pygame.draw.rect(screen, (100, 100, 100), classic_button)
        pygame.draw.rect(screen, (100, 100, 100), speed_button)
        screen.blit(classic_text, (110, 110))
        screen.blit(speed_text, (110, 210))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if classic_button.collidepoint(mouse_pos):
                    return "classic"
                elif speed_button.collidepoint(mouse_pos):
                    return "speed"
def classic_mode():
    global score
    score = 0
    frozen_timer = 0
    liste_balle = [Ball() for _ in range(10)]

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
                        if i.color == "frozen":
                            frozen_timer = 100
                            score += 3
                        if i.color == "explosive":
                            exploded_balls = [b for b in liste_balle if math.sqrt((b.x-i.x)**2 + (b.y-i.y)**2) < 100]
                            for exploded_ball in exploded_balls:
                                score += exploded_ball.points
                                liste_balle.remove(exploded_ball)
                            score += len(exploded_balls) * 2 
                            for _ in range(len(exploded_balls)):
                                liste_balle.append(Ball())
                        else:
                            score += i.points
                            liste_balle.remove(i)
                            liste_balle.append(Ball())
                        touch = True
                        break
                    else:
                        touch = False
                if touch == False:
                    score -= 1
                    touch = True
        if frozen_timer > 0:
            frozen_timer -= 1

        for i in range(len(liste_balle)):            
            for j in range(i + 1, len(liste_balle)):
                if liste_balle[i].collide(liste_balle[j]):
                    liste_balle[i].deltax, liste_balle[j].deltax = liste_balle[j].deltax, liste_balle[i].deltax
                    liste_balle[i].deltay, liste_balle[j].deltay = liste_balle[j].deltay, liste_balle[i].deltay
      
        for elem in liste_balle:
            if frozen_timer > 0 :
                elem.x += elem.deltax * 0.4
                elem.y += elem.deltay * 0.4
            else:
                elem.x += elem.deltax
                elem.y += elem.deltay
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

    high_score = manage_high_scores("classic", score)
    screen.blit(font.render(f'High Score: {high_score}', True, WHITE), (200, 300))
    pygame.display.update()
    pygame.time.wait(3000)

def speed_mode():
    global score
    score = 0
    balls_hit = 0
    start_time = pygame.time.get_ticks()
    
    liste_balle = [Ball() for _ in range(50)]
    
    continuer = True
    while continuer and balls_hit < 50:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuer = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                (click_x, click_y) = event.pos
                for i in liste_balle:
                    if math.sqrt((i.x-click_x)**2 + (i.y-click_y)**2)<55:
                        liste_balle.remove(i)
                        balls_hit += 1
                        break

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
        screen.blit(font.render(f'Balles touchées: {balls_hit}/50', True, WHITE), (400,300))
        for elem in liste_balle: 
            screen.blit(elem.img, (elem.x, elem.y))

        pygame.display.update()
        clock.tick(50)

    if balls_hit == 50:
        end_time = pygame.time.get_ticks()
        total_time = (end_time - start_time) / 1000
        
        high_score = manage_high_scores("speed", int(total_time * 100))  # Store time as integer (in centiseconds)
        
        screen.blit(fond, (0,0))
        time_text = font.render(f"Temps: {total_time:.2f} secondes", True, WHITE)
        high_score_text = font.render(f"Meilleur temps: {high_score/100:.2f} secondes", True, WHITE)
        screen.blit(time_text, (200, 150))
        screen.blit(high_score_text, (200, 200))
        pygame.display.update()
        pygame.time.wait(3000)

# Main game loop
while True:
    mode = show_menu()
    if mode is None:
        break
    elif mode == "classic":
        classic_mode()
    elif mode == "speed":
        speed_mode()

pygame.quit()
