import pygame #Importing Pygame module
from pygame.locals import *
from pygame import mixer
import random

pygame.init()

#Game Speed

clock = pygame.time.Clock()
fps = 60

#Game Dimensions

scwidth, scheight = (750, 750)
dimension_dict = {scwidth:750,scheight:750}


sc = pygame.display.set_mode((scwidth, scheight))
pygame.display.set_caption("Flappy Bird")
borderfont = pygame.font.Font('C:/Users/mitst/Desktop/Py_Project/ataurus3d.ttf', 60)
font = pygame.font.Font('C:/Users/mitst/Desktop/Py_Project/ataurus.ttf', 60)
white = (255,255,255)
black = (0,0,0)

#Game Icon

new_icon = pygame.image.load("C:/Users/mitst/Desktop/Py_Project/birdflap1.png")
pygame.display.set_icon(new_icon)

#Game Vars

grscroll = 0 #Ground Scroll
scroll_speed = 4 #Scroll Speed
flying = False
end = False
pinterval = 1750 #in miliseconds
lpipe = pygame.time.get_ticks() - pinterval
score = 0
pipepass = False
hit = 1 
finalscore = {"Final Score": score}

#Sprites

bg = pygame.image.load('C:/Users/mitst/Desktop/Py_Project/bg.png')
grim = pygame.image.load("C:/Users/mitst/Desktop/Py_Project/ground.png")
restartbutton = pygame.image.load("C:/Users/mitst/Desktop/Py_Project/restart.png")

def reset_game():
    pipe_group.empty()
    birb.rect.x = 300
    birb.rect.y = 375
    score = 0
    return score


def draw_text(text, font, colour, x, y):
    image = font.render(text, True, colour)
    sc.blit(image, (x,y))

def draw_bordtext(text, font, colour, x, y):
    image = font.render(text, True, colour)
    sc.blit(image, (x,y))

class Bird(pygame.sprite.Sprite): #Defining Bird Class
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for i in range(1,4):
            img = pygame.image.load(f'C:/Users/mitst/Desktop/Py_Project/birdflap{i}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.vel = 0
        self.clicked = False
        self.space = False

    def update(bird):
        
        #For Gravity

        if flying == True:
            bird.vel += 0.5
        if bird.vel > 100:
            bird.vel = 0
        if bird.rect.bottom < 620:
            bird.rect.y += int(bird.vel)

        if end == False:

            #For Counter-Gravity (Jumping)

            keys_pressed = pygame.key.get_pressed()

            if keys_pressed[pygame.K_SPACE] == 1 and bird.space == False and flying == True:
                bird.space = True
                flap = mixer.Sound("C:/Users/mitst/Desktop/Py_Project/flap.wav")
                flap.play()
                bird.vel = -10
            if keys_pressed[pygame.K_SPACE] == 0:
                bird.space = False

                
            if pygame.mouse.get_pressed()[0] == 1 and bird.clicked == False:
                bird.clicked = True
                flap = mixer.Sound("C:/Users/mitst/Desktop/Py_Project/flap.wav")
                flap.play()
                bird.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                bird.clicked = False


            #For Animation of Sprite

            bird.counter += 1
            flap_cd = 8

            if bird.counter > flap_cd:
                bird.counter = 0
                bird.index += 1
                if bird.index >= len(bird.images):
                    bird.index = 0
            bird.image = bird.images[bird.index]

            #Bird Velocity Rotation

            bird.image  = pygame.transform.rotate(bird.images[bird.index], bird.vel * -1.5)

        else:
            bird.image  = pygame.transform.rotate(bird.images[bird.index], -90)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x,y, post):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("C:/Users/mitst/Desktop/Py_Project/pipe.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = [x,y]
        #post 1 up -> 1, post 2 down -> -1
        if post == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x,y-75]
        if post == -1:
            self.rect.topleft = [x,y+75]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill() #To prevent lag

class Button():
    def __init__(self,x , y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

    def draw(self):
        click = False
        post = pygame.mouse.get_pos()
        if self.rect.collidepoint(post):
            if pygame.mouse.get_pressed()[0] == 1:
                click = True
        sc.blit(self.image, (self.rect.x, self.rect.y))
        return click

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

birb = Bird(300, 375)
bird_group.add(birb)

#Restart Button

button = Button(325, 275, restartbutton)

#Main Window

run = True

while run:

#For proper speed
    
    clock.tick(fps)

#For importing background

    sc.blit(bg, (0,-15))
    bird_group.draw(sc)
    bird_group.update()
    pipe_group.draw(sc)

    sc.blit(grim, (grscroll, 620))

#Point System
    
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left and bird_group.sprites()[0].rect.right< pipe_group.sprites()[0].rect.right and pipepass == False:
            pipepass = True
        if pipepass == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pointsound = mixer.Sound("C:/Users/mitst/Desktop/Py_Project/point.wav")
                pointsound.play()
                pipepass = False

    draw_text(str(score), font, white, 375, 25)
    draw_bordtext(str(score), borderfont, black, 375, 25)


#For ending the game
    
    #When touching the pipe

    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or birb.rect.top < 0: #False are used for preventing deletion of pipes upon collision
        end = True
        hit -= 1  
    #When touching the ground

    if birb.rect.bottom >= 620:
        end = True
        flying = False
        hit -= 1

    if hit == 0:
        hitsound = mixer.Sound("C:/Users/mitst/Desktop/Py_Project/ouch.wav")
        hitsound.play()
        print(finalscore)

#For scrolling effect
    if end == False and flying == True:

        #Pipe Script

        runtime = pygame.time.get_ticks()
        if runtime - lpipe > pinterval:
            pheight = random.randint(-125, 125)
            botpipe = Pipe(scwidth, 375 + pheight, -1)
            toppipe = Pipe(scwidth, 375 + pheight, 1)
            pipe_group.add(botpipe)
            pipe_group.add(toppipe)
            lpipe = runtime 


        #Ground Script

        grscroll = grscroll-scroll_speed 
        if abs(grscroll) > 35:
            grscroll = 0
            
        pipe_group.update()


    #Restarting game
    if end == True:
        if button.draw() == True:
            end = False
            flying = True
            score = reset_game()
            swoosh = mixer.Sound("C:/Users/mitst/Desktop/Py_Project/swoosh.wav")
            swoosh.play()
            hit = 1
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_SPACE] == 1:
            flying = True
            end = False
            score = reset_game()
            swoosh = mixer.Sound("C:/Users/mitst/Desktop/Py_Project/swoosh.wav")
            swoosh.play()
            hit = 1
            
    for event in pygame.event.get():

    #For closing the game when you click on the X button
        if event.type == pygame.QUIT:
            run = False

    #For starting game
        keys_pressed = pygame.key.get_pressed()    
        swoosh = mixer.Sound("C:/Users/mitst/Desktop/Py_Project/swoosh.wav")
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and end == False:
            flying = True
            swoosh.play()
        if keys_pressed[pygame.K_SPACE] == 1:
            flying = True

    pygame.display.update()
pygame.quit()
