import pygame
import os
import random
import math
import sys
import numpy as np
# from genetic import Genetic
pygame.init()


# Global Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]

JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))

DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]
SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird3.png"))]

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

FONT = pygame.font.Font('Fonts/PressStart2P.ttf',16)

class Dinosaur:
    X_POS = 80
    Y_POS = 310
    JUMP_VEL = 8.5

    def __init__(self, img=RUNNING[0]):
        self.image = img
        self.dino_run = True
        self.dino_jump = False
        self.dino_duck = False
        self.jump_vel = self.JUMP_VEL
        self.rect = pygame.Rect(self.X_POS, self.Y_POS, img.get_width(), img.get_height())
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.step_index = 0
        self.W = np.random.randn(16,5)
        self.W2 = np.random.randn(3,16)
        self.score = 0
    def update(self):
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()
        if self.dino_duck:
            self.duck()
        if self.step_index >= 10:
            self.step_index = 0
    def jump(self):
        self.image = JUMPING
        if self.dino_jump:
            self.rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel <= -self.JUMP_VEL: #return to background
            self.dino_jump = False
            self.dino_run = True
            self.jump_vel = self.JUMP_VEL

    def run(self):
        self.image = RUNNING[self.step_index // 5]
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS
        self.step_index += 1


    def duck(self):
        self.image = DUCKING[self.step_index // 5]
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS+40
        self.step_index += 1
        # self.dino_run = True
        # self.dino_jump = False
        # self.dino_duck = False

    def draw(self, SCREEN,line=True,border = True):
        global obstacles
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))
        if border==True:
            pygame.draw.rect(SCREEN, self.color, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 2)
        if line==True:
            for obstacle in obstacles:
                pygame.draw.line(SCREEN, self.color, (self.rect.x + 54, self.rect.y + 12), obstacle.rect.center, 2)
class Obstacle:
    def __init__(self, image, number_of_cacti):
        self.image = image
        self.type = number_of_cacti
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH + random.randint(0,200)*(1+game_speed*0.01)

    def update(self):
        self.rect.x -= game_speed*0.9
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image, number_of_cacti):
        super().__init__(image, number_of_cacti)
        self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self, image, number_of_cacti):
        super().__init__(image, number_of_cacti)
        self.rect.y = 300

class Bird(Obstacle):
    def __init__(self, image, number_of_cacti):
        super().__init__(image, number_of_cacti)
        self.rect.y = 250 + random.choice([-50,50,15,-75])
class HighBird(Obstacle):
    def __init__(self, image, number_of_cacti):
        super().__init__(image, number_of_cacti)
        self.rect.y = 250 - 50
def remove(index):
    dinosaurs.pop(index)


def distance(pos_a, pos_b):
    dx = pos_a[0]-pos_b[0]
    dy = pos_a[1]-pos_b[1]
    return math.sqrt(dx**2+dy**2)
dinosaur = Dinosaur()
dino_guide = Dinosaur()
running  = True
obstacles = []
x_pos_bg = 0
y_pos_bg = 380
game_speed = 20
points = 0
pausing = False
dinosaurs = [dinosaur,dino_guide]
dino_guide.W = np.load('Data\w.npy')
dino_guide.W2 = np.load('Data\w2.npy')
# print(f'W1: {dino_guide.W}')
# print(f'W2: {dino_guide.W2}')
dino_guide.X_POS = 120
def background():
    global x_pos_bg, y_pos_bg
    image_width = BG.get_width()
    SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
    SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
    if x_pos_bg <= -image_width:
        x_pos_bg = 0
    x_pos_bg -= game_speed

def score():
    global points, game_speed
    points += 1
    if points % 200 == 0:
        game_speed += 1
        game_speed = min(30,game_speed)
    text = FONT.render(f'Points:{str(points)}', True, (0, 0, 0))
    SCREEN.blit(text, (850, 50))
clock = pygame.time.Clock()
mode = 0
text1 = FONT.render(f'Jump!', True, (0, 0, 0))
text2 = FONT.render(f'Duck!', True, (0, 0, 0))
text3 = FONT.render(f'Run!', True, (0, 0, 0))
guide = True
while running:
    #exiting   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    #color screen
    SCREEN.fill((255, 255, 255))
    dinosaur.update() #dino's action
    dinosaur.draw(SCREEN,line=False,border=False) #
    if guide==True:
        dino_guide.update()
        dino_guide.draw(SCREEN,line=True,border=True)
    score()
    background()
    clock.tick(30)
    
    if len(obstacles) == 0: #What's len(ob)=0 means
        rand_int = random.randint(0, 2)
        #Random obstacle
        if rand_int == 0:
            obstacles.append(SmallCactus(SMALL_CACTUS, random.randint(0, 2)))
        elif rand_int == 1:
            obstacles.append(LargeCactus(LARGE_CACTUS, random.randint(0, 2)))
        elif rand_int == 2:
            if np.random.rand()<0.5:
                obstacles.append(Bird(BIRD, random.randint(0, 1)))
            else:
                obstacles.append(HighBird(BIRD,2))  
    for obstacle in obstacles:
        obstacle.draw(SCREEN)
        obstacle.update()
        #remove dino if collides
        if dinosaur.rect.colliderect(obstacle.rect):
            dinosaur.score = points
            dinosaurs = []
            running = False 
            gameover_txt = FONT.render('GAME OVER',True,(0,0,0))
            SCREEN.blit(gameover_txt,(200,150))
        if dino_guide.rect.colliderect(obstacle.rect):
            guide = False
        else:
            if dino_guide.rect.y == dino_guide.Y_POS or dino_guide.rect.y == dino_guide.Y_POS+40 and len(obstacles)>0:
                # output = dino_guide.W @ np.array([dino_guide.rect.y,distance((dino_guide.rect.x, dino_guide.rect.y),obstacle.rect.midtop)],dtype=float).reshape(-1,1)
                output = dino_guide.W @ np.array([dino_guide.rect.y,obstacle.rect.x,obstacle.rect.y,distance((dino_guide.rect.x, dino_guide.rect.y),obstacle.rect.midtop),game_speed],dtype=float).reshape(-1,1)
                # output = sigmoid(output)
                output   = np.maximum(output,0)
                output = dino_guide.W2 @ output
                output = output.reshape(-1)
                # print(np.argmax(output))
                if np.argmax(output)==0 :
                    dino_guide.dino_jump = True
                    dino_guide.dino_run = False
                    dino_guide.dino_duck = False
                    
                    mode = 1
                elif np.argmax(output)==1 :
                    dino_guide.dino_jump = False
                    dino_guide.dino_run = False
                    dino_guide.dino_duck = True
                    mode = 2
                else:
                    dino_guide.dino_jump = False
                    dino_guide.dino_run = True
                    dino_guide.dino_duck = False
                    mode = 3
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if dinosaur.rect.y == dinosaur.Y_POS or dinosaur.rect.y == dinosaur.Y_POS+40:
                if event.key==pygame.K_UP:
                    dinosaur.dino_jump = True
                    dinosaur.dino_run = False 
                    dinosaur.dino_duck = False
                    mode = 1
                elif event.key==pygame.K_DOWN:
                    dinosaur.dino_jump = False
                    dinosaur.dino_run = False
                    dinosaur.dino_duck = True
                    mode = 2
                elif event.key==pygame.K_RIGHT:
                    dinosaur.dino_jump = False
                    dinosaur.dino_run = True
                    dinosaur.dino_duck = False
                    mode = 3
    if dino_guide.dino_jump == True:
        SCREEN.blit(text1, (400, 50))
    elif dino_guide.dino_duck == True:
        SCREEN.blit(text2, (400, 50))
    else:
        SCREEN.blit(text3, (400, 50))
    if pausing:
        X_POS = 80
        Y_POS = 310
        JUMP_VEL = 8.5
        score = 0
        pausing = False

    pygame.display.update()
    pygame.display.flip()
pygame.quit() 


        