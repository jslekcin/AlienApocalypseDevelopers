import sys, pygame, math, random
import instructions

from pygame.constants import K_2

pygame.init()
pygame.font.init()

size = width, height = 750, 750 

uiFont = pygame.font.Font(None, 36)
titleFont = pygame.font.Font(None, 45)
screen = pygame.display.set_mode(size)

bg = pygame.image.load("images\Menu Screen.png")
bg = pygame.transform.scale(bg, size)

startButtonPressed = False
def mainMenuLoop():
    pygame.mixer.music.load('GameMusic/menu.mp3')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

    while 1:
        for event in pygame.event.get(pygame.QUIT):
            pygame.quit()
            sys.exit
            break
        
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 200 <= mouse[0] <= 500 and 275 <= mouse[1] <= 325:
                    print("Start button was pressed")
                    return "tutorial"
                elif 200 <= mouse[0] <= 340 and 340 <= mouse[1] <= 390:
                    print("Quit button was pressed")
                    pygame.quit()
                    #sys.exit
                    return "quit"
                elif 360 <= mouse[0] <= 500 and 340 <= mouse[1] <= 390:
                    print("Instruction button was pressed")
                    credits = instructions.instructionsLoop()
                    if credits == "quit":
                        return "quit"

        screen.blit(bg,(0,0))
        
        startButton = pygame.draw.rect(screen, (255,255,255), pygame.Rect(200, 275, 300, 50))#100, 200, 300, 50
        quitButton = pygame.draw.rect(screen, (255,255,255), pygame.Rect(200, 340, 140, 50))#100, 265, 140, 50
        instructionButton = pygame.draw.rect(screen, (255,255,255), pygame.Rect(360, 340, 140, 50))#260, 265, 140, 50

        startText = uiFont.render("Start", True, (0,0,0))
        quitText = uiFont.render("Quit Game", True, (0,0,0))
        instructionText = uiFont.render("Credits", True, (0,0,0))

        TitleText = titleFont.render("Ailen Apocalypse",True,(255,0,0))

        screen.blit(startText, (325, 290))#225, 215
        screen.blit(quitText, (205, 355))#105, 280
        screen.blit(instructionText, (385, 355))#260, 280

        screen.blit(TitleText, (215, 55))#145, 150

        pygame.display.flip()

if __name__ == "__main__":
    mainMenuLoop()



    