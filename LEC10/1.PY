import pygame 
import random

pygame.init()

screen = pygame.display.set_mode((600 , 500))

dice_rolled = []

level = 1

precedence= {
    '+': 1 ,
    '-': 1 , 
    '*': 2  ,
    '/':2
    
    
    }


imput_symbols = "123456*/-+()"

possible_dice = "123456"

def init_dice():
    global dice_rolled , level

    for el in range(1, level*2+2):
        dice_rolled.append(random.randrange(1,7))




running = True 

while running :
    pygame.display.update()

    for x in pygame.event.get():
        if  x.type == pygame.QUIT:
            running = False
    
    font_dice = pygame.font.SysFont("times new roman" , 20)
    dice_text_render = font_dice.render("Level 1. Dice area: "+str(dice_rolled),True)
    screen.fill((255,255,255))

    