import pygame
import random
from tkinter import Tk,messagebox,sys
import time
import os 
Tk().wm_withdraw()

pygame.init()
WIDTH = 800
HEIGHT = 600


os.environ['SDL_VIDEO_CENTERED'] = '1'
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Corona Dodge (Made by Sourabh Sathe)")

RED = (255,0,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
BLACK=(0,0,0)
background_image = pygame.image.load("assets/background_small.png").convert_alpha()

player_size = 35
player_pos = [WIDTH/2, HEIGHT-2*player_size-18]
enemy=pygame.image.load('assets/virus_35.png').convert_alpha()
enemy_size = 35
enemy_pos = [random.randint(0,WIDTH-enemy_size), 0]
enemy_list = [enemy_pos]

SPEED = 2

player=pygame.image.load("assets/player_small.png").convert_alpha()


game_over = False

score = 0

clock = pygame.time.Clock()

myFont = pygame.font.SysFont("verdana", 35)

def set_level(score, SPEED):
	if score < 20:
		SPEED = 2
		level=1
	elif score < 50:
		SPEED = 3
		level=2
	elif score < 80:
		SPEED = 5
		level=3
	elif score < 120:
		SPEED = 7
		level=4
	elif score < 170:
		SPEED = 8
		level=5
	elif score < 250:
		SPEED = 10
		level=6
	elif score < 320:
		SPEED = 11
		level=7
	else:
		SPEED = 12
		level=8

	prop=[SPEED,level]
	return prop


def drop_enemies(enemy_list):
	delay = random.random()
	if len(enemy_list) < 10 and delay < 0.1:
		x_pos = random.randint(0,WIDTH-enemy_size)
		y_pos = 0
		enemy_list.append([x_pos, y_pos])

def draw_enemies(enemy_list):
	for enemy_pos in enemy_list:
		screen.blit(enemy,(enemy_pos[0],enemy_pos[1]))
		

def update_enemy_positions(enemy_list, score):
	for idx, enemy_pos in enumerate(enemy_list):
		if enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT:
			enemy_pos[1] += SPEED
		else:
			enemy_list.pop(idx)
			score += 1
	return score

def collision_check(enemy_list, player_pos):
	
	for enemy_pos in enemy_list:
		if detect_collision(enemy_pos, player_pos):
			return True
	return False

def detect_collision(player_pos, enemy_pos):
	p_x = player_pos[0]
	p_y = player_pos[1]

	e_x = enemy_pos[0]
	e_y = enemy_pos[1]

	if (e_x > p_x and e_x < (p_x + player_size)) or (p_x > e_x and p_x <= (e_x+enemy_size)):
		if (e_y > p_y and e_y < (p_y + player_size)) or (p_y > e_y and p_y <= (e_y+enemy_size)):
			return True
	return False


pressed_keys = {"left": False, "right": False, "up": False, "down": False}
while not game_over:
	x = player_pos[0]
	y = player_pos[1]
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		
		elif event.type == pygame.KEYDOWN:
			
			if event.key == pygame.K_LEFT:
				pressed_keys["left"] = True
			if event.key == pygame.K_RIGHT:
				pressed_keys["right"] = True
			if event.key == pygame.K_UP:
				pressed_keys["up"] = True
			if event.key == pygame.K_DOWN:
				pressed_keys["down"] = True
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				pressed_keys["left"] = False
			if event.key == pygame.K_RIGHT:
				pressed_keys["right"] = False
			if event.key == pygame.K_UP:
				pressed_keys["up"] = False
			if event.key == pygame.K_DOWN:
				pressed_keys["down"] = False

	if pressed_keys["left"]:
		x -= player_size-25
		if x<0:
			x=WIDTH-player_size
	if pressed_keys["right"]:
		x += player_size-25
		if x>=WIDTH:
			x=0
	if pressed_keys["up"]:
		y -= player_size-30
		if y<0:
			y=HEIGHT-player_size
	if pressed_keys["down"]:
		y += player_size-30
		if y>=HEIGHT:
			y=0			
	player_pos = [x,y]	

	
	
	drop_enemies(enemy_list)
	score = update_enemy_positions(enemy_list, score)
	prop = set_level(score, SPEED)
	SPEED=prop[0]
	level=prop[1]

	screen.blit(background_image,[0,0])
	text_score = "Score:" + str(score)
	label = myFont.render(text_score, True, BLACK)
	screen.blit(label, (WIDTH-200, 5))

	text_level = "Level:" + str(level)
	label = myFont.render(text_level, True, BLACK)
	screen.blit(label, (5, 5))

	
	screen.blit(player,[player_pos[0], player_pos[1]])
	draw_enemies(enemy_list)
	pygame.display.update()

	if collision_check(enemy_list, player_pos):
		messagebox.showinfo("",f'Game Over!\n\nYou are INFECTED!\nGo to the hospital NOW\n\nYou reached Level {level}\nScore: {score}')
		game_over = True
		break

	clock.tick(60)