import pygame
import random


pygame.init()
screen = pygame.display.set_mode((600,300))
pygame.display.set_caption('Dinosaur')
WHITE = (255,255,255)
RED = (255,0,0)
background_x = 0
background_y = 0
dinosaur_x = 0
dinosaur_y = 230
tree_x = 550
tree_y = 230
x_velocity = 5
y_velocity = 7
g = 0.1
jump = False
pausing = False
score = 0
font = pygame.font.SysFont('san',20)
font1 = pygame.font.SysFont('san',40)
backgound = pygame.image.load('background.jpg')
dinosaur = pygame.image.load('dinosaur.png')
tree = pygame.image.load('tree.png')

clock = pygame.time.Clock()
running = True
while running:
    clock.tick(60)
    screen.fill(WHITE)
    
    backgound1_rect = screen.blit(backgound,(background_x,background_y))
    backgound2_rect = screen.blit(backgound,(background_x+600,background_y))
    score_txt = font.render('Score:' + str(score),True,RED)
    screen.blit(score_txt,(5,5))
    if background_x+600<=0:
        background_x = 0
    dinosaur_rect = screen.blit(dinosaur,(dinosaur_x,dinosaur_y))
    tree_rect = screen.blit(tree,(tree_x,tree_y))
    #collision
    if dinosaur_rect.colliderect(tree_rect):
        pausing=True
        gameover_txt = font1.render('GAME OVER',True,RED)
        screen.blit(gameover_txt,(200,150))
        x_velocity = 0
        y_velocity = 0
    else:
        score+=1
    #moving
    background_x-=x_velocity
    tree_x-=x_velocity
    if tree_x <=-20:
        tree_x=550 + random.randint(-200,200)
    if 230 >=dinosaur_y>=80:
        if jump==True:
            dinosaur_y-=y_velocity
            # y_velocity-=g   
    else:
        jump=False
    if dinosaur_y<230:
        if jump==False:
            dinosaur_y+=y_velocity
            # y_velocity+=g
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                if dinosaur_y == 230:
                    jump= True
                if pausing:
                    background_x = 0
                    background_y = 0
                    dinosaur_x = 0
                    dinosaur_y = 230
                    tree_x = 550
                    tree_y = 230
                    x_velocity = 5
                    y_velocity = 7
                    score = 0
                    pausing = False               

    
    pygame.display.flip()
pygame.quit()
