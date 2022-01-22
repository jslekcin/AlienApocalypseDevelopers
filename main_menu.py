import sys, pygame, math, random

from pygame.constants import K_2

pygame.init()
pygame.font.init()

size = width, height = 500, 500 

uiFont = pygame.font.Font(None, 36)
screen = pygame.display.set_mode(size)

bg = pygame.image.load("images\Menu Screen.png")
instructionButtonPressed = False
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
            elif 100 <= mouse[0] <= 240 and 265 <= mouse[1] <= 315:
                print("Quit button was pressed")
                pygame.quit()
                sys.exit
                break
            elif 260 <= mouse[0] <= 400 and 265 <= mouse[1] <= 315:
                print("Instruction button was pressed")
                instructionButtonPressed = True
            elif 5 <= mouse[0] <= 55 and 5 <= mouse[1] <= 55:
                instructionButtonPressed = False

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
    
    if instructionButtonPressed == True:
        pygame.draw.rect(screen, (255,255,255),(0,0,500,500))
        instructiontext1 = uiFont.render("INSTRUCTIONS", True, (0,0,0))
        screen.blit(instructiontext1, (160,45))

        instructiontext2 = uiFont.render("A = Move Left   D = Move Right", True, (0,0,0))
        screen.blit(instructiontext2, (70,115))

        instructiontext3 = uiFont.render("SPACE = Jump   SHIFT = Sprint", True, (0,0,0))
        screen.blit(instructiontext3, (70,185))

        instructiontext4 = uiFont.render("1 = EQUIP BAT  2 =  EQUIP PISTOL", True, (0,0,0))
        screen.blit(instructiontext4, (50,255))

        instructiontext5 = uiFont.render("CLICK = Use Weapon", True, (0,0,0))
        screen.blit(instructiontext5, (120,325))

        pygame.draw.rect(screen, (238, 75, 43), (5,5,50,50))
    
    pygame.display.flip()

    