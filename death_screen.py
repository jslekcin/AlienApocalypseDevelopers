import sys, pygame, math, random

from pygame.constants import K_2

pygame.init()
pygame.font.init()

size = width, height = 500, 500 

uiFont = pygame.font.Font(None, 80)
screen = pygame.display.set_mode(size)

QuitButtonPressed = False
while 1:
    for event in pygame.event.get(pygame.QUIT):
        pygame.quit()
        sys.exit
        break
    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
       if event.type == pygame.MOUSEBUTTONDOWN:
            if 100 <= mouse[0] <= 400 and 200 <= mouse[1] <= 250:
                pygame.quit()


    QuitText = uiFont.render("QUIT", True, (255,255,255))

    screen.blit(QuitText, (180, 160))
    
    
    RetryText = uiFont.render("RETRY", True, (255,255,255))

    screen.blit(RetryText, (160, 280))
    
    #pygame.draw.rect(screen, (0,0,0),(0,0,75,50))
    DeathScreenText = uiFont.render("YOU DIED", True, (252,3,3))
    screen.blit(DeathScreenText, (125,45))

    screen.blit('Images/death.jpg')

    pygame.display.flip()