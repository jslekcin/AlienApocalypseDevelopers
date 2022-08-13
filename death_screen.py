import sys, pygame, math, random

from pygame.constants import K_2

def deathScreenLoop():
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

        quitRect = pygame.Rect(170, 160, 170, 50)
        retryRect = pygame.Rect(160, 280, 190, 50)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quitRect.collidepoint(event.pos):
                    pygame.quit()
                    return "quit"

                if retryRect.collidepoint(event.pos):
                    return "main_menu"


        death_image = pygame.image.load('Images/death.jpg')
        death_image = pygame.transform.scale(death_image,[500,500])
        screen.blit(death_image,(0,0))


        QuitText = uiFont.render("QUIT", True, (0,0,0))

        
        pygame.draw.rect(screen,(255,255,255),quitRect)
        pygame.draw.rect(screen,(0,0,0),retryRect)

        screen.blit(QuitText, (180, 160))
        
        
        RetryText = uiFont.render("RETRY", True, (255,255,255))

        screen.blit(RetryText, (160, 280))
        
        #pygame.draw.rect(screen, (0,0,0),(0,0,75,50))
        DeathScreenText = uiFont.render("YOU DIED", True, (252,3,3))
        screen.blit(DeathScreenText, (125,45))

        

        pygame.display.flip()

if __name__ == "__main__":
    deathScreenLoop()