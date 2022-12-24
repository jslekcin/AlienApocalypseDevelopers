import sys, pygame

class WallSave:
    blockImages = [pygame.image.load('Images\Grass.png'), pygame.Surface((25,25)), pygame.Surface((25,25)), pygame.Surface((25,25)), pygame.Surface((25,25)), pygame.Surface((25,25)), pygame.image.load('Images\stone.PNG'), pygame.image.load('Images/pg.png'), pygame.image.load('Images/poison.png'), pygame.image.load('Images/ps.png'), pygame.image.load('Images/Dirt3.png')]
    blockImages[1].fill((255,255,255))
    blockImages[2].fill((255,0,0))
    blockImages[3].fill((0,255,0))
    blockImages[4].fill((0,0,255))  
    blockImages[5].fill((0,0,0))