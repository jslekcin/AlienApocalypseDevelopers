import sys, pygame, math, random

from player_save import Save

from pygame.constants import K_2

def deathScreenLoop(prev_level):
    pygame.init()
    pygame.font.init()

    pygame.mixer.music.load('GameMusic/death.mp3')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

    size = width, height = 750, 750 

    uiFont = pygame.font.Font(None, 65)
    screen = pygame.display.set_mode(size)

    QuitButtonPressed = False
    while 1:
        for event in pygame.event.get(pygame.QUIT):
            pygame.quit()
            sys.exit
            break
        mouse = pygame.mouse.get_pos()

        quitRect = pygame.Rect(275, 420, 200, 60)
        retryRect = pygame.Rect(275, 300, 200, 65)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quitRect.collidepoint(event.pos):
                    pygame.quit()
                    return "quit"

                if retryRect.collidepoint(event.pos):
                    if prev_level == "":
                        prev_level = "tutorial"
                    return prev_level


        death_image = Save.DeathScreens[Save.LastDamageSource]
        death_image = pygame.transform.scale(death_image,[750,750])
        screen.blit(death_image,(0,0))


        QuitText = uiFont.render("QUIT", True, (0,0,0))

        
        pygame.draw.rect(screen,(255,255,255),quitRect)
        pygame.draw.rect(screen,(0,0,0),retryRect)

        screen.blit(QuitText, (315, 430))
        
        
        RetryText = uiFont.render("RETRY", True, (255,255,255))

        screen.blit(RetryText, (301, 310))
        
        #pygame.draw.rect(screen, (0,0,0),(0,0,75,50))
        """DeathScreenText = uiFont.render("YOU DIED", True, (252,3,3))
        screen.blit(DeathScreenText, (125,45))"""

        

        pygame.display.flip()

if __name__ == "__main__":
    deathScreenLoop()