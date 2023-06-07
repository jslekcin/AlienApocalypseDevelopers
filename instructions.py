import pygame, sys
def instructionsLoop():
    pygame.init()
    pygame.font.init()

    size = width, height = 750, 750 

    uiFont = pygame.font.Font(None, 80)
    screen = pygame.display.set_mode(size)

    
    while 1:
        """for event in pygame.event.get(pygame.QUIT):
            return "quit"
            break"""

        win_image = pygame.image.load('Images/credits.png')
        win_image = pygame.transform.scale(win_image,[750,750])
        screen.blit(win_image,(0,0))

        returnRect = pygame.Rect(0,0,187.5,93.75)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if returnRect.collidepoint(event.pos):
                    return "main_menu"
            if event.type == pygame.QUIT:
                return "quit"

        #pygame.draw.rect(screen,(255,0,0),returnRect)
    
        pygame.display.flip()

if __name__ == "__main__":
    instructionsLoop()