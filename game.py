import pygame #Importing Pygame module
from pygame.locals import *

pygame.init()

scwidth, scheight = (864, 936) #Defining the screen width and screen height

sc = pygame.display.set_mode((scwidth, scheight))
pygame.display.set_caption("Flappy Bird")

bg = pygame.image.load('C:/Users/mitst/Desktop/Py%20Project/bg.png')

run = True
while run:
    sc.blit(bg, (0,0))

    for event in pygame.event.get(): #For closing the game when you click on the X button
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
pygame.quit()