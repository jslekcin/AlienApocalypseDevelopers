import sys, pygame, math, random

from pygame.constants import K_2

def WinScreenLoop():
    pygame.init()
    pygame.font.init()

    size = width, height = 750, 750 

    screen = pygame.display.set_mode(size)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit
                break

        win_image = pygame.image.load('Images/win_screen.png')
        win_image = pygame.transform.scale(win_image,[750,750])
        screen.blit(win_image,(0,0))

            
        #pygame.draw.rect(screen, (0,0,0),(0,0,75,50))

        

        pygame.display.flip()

if __name__ == "__main__":
    WinScreenLoop()