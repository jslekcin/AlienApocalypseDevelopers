import sys, pygame, math, random

from pygame.constants import K_2

pygame.init()
pygame.font.init()

size = width, height = 500, 500 

uiFont = pygame.font.Font(None, 36)
screen = pygame.display.set_mode(size)

bg = pygame.image.load("images\Menu Screen.png")

startButtonPressed = False
def mainMenuLoop(gameState):
    while 1:
        for event in pygame.event.get(pygame.QUIT):
            pygame.quit()
            sys.exit
            break
        
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 100 <= mouse[0] <= 400 and 200 <= mouse[1] <= 250:
                    print("Start button was pressed")
                    startButtonPressed = True
                elif 100 <= mouse[0] <= 240 and 265 <= mouse[1] <= 315:
                    print("Quit button was pressed")
                    #pygame.quit()
                    #sys.exit
                    break
                elif 260 <= mouse[0] <= 400 and 265 <= mouse[1] <= 315:
                    print("Instruction button was pressed")

        screen.blit(bg,(0,0))
        
        startButton = pygame.draw.rect(screen, (255,255,255), pygame.Rect(100, 200, 300, 50))
        quitButton = pygame.draw.rect(screen, (255,255,255), pygame.Rect(100, 265, 140, 50))
        instructionButton = pygame.draw.rect(screen, (255,255,255), pygame.Rect(260, 265, 140, 50))

        startText = uiFont.render("Start", True, (0,0,0))
        quitText = uiFont.render("Quit Game", True, (0,0,0))
        instructionText = uiFont.render("How to Play", True, (0,0,0))

        TitleText = uiFont.render("Ailen Apocalypse",True,(255,0,0))

        screen.blit(startText, (225, 215))
        screen.blit(quitText, (105, 280))
        screen.blit(instructionText, (260, 280))

        screen.blit(TitleText, (145, 150))

        if startButtonPressed == True:
            gameState = 1

        pygame.display.flip()



    