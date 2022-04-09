import sys, pygame, math, random


from pygame.constants import K_2
from sympy import false

pygame.init()
pygame.font.init()
pygame.mixer.init()


uiFont = pygame.font.Font(None, 32)

size = width, height = 500, 500 # TODO: Decide on final window size
screen = pygame.display.set_mode(size) 
fps = 60

black = (0,0,0)
background = pygame.image.load('Images\sky.png')
background = pygame.transform.scale(background, size)
gameState = 1

clock = pygame.time.Clock()

while 1:
    clock.tick(fps) 
    
    for event in pygame.event.get(pygame.QUIT):
        pygame.quit()
        sys.exit
        break