import pygame
def instructionsLoop():
    pygame.init()
    pygame.font.init()

    size = width, height = 750, 750 

    uiFont = pygame.font.Font(None, 80)
    screen = pygame.display.set_mode(size)

    
    while 1:
        for event in pygame.event.get(pygame.QUIT):
            pygame.quit()
            break

        returnRect = pygame.Rect(0,0,100,100)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if returnRect.collidepoint(event.pos):
                    return "main_menu"
        
        
        screen.fill((255,255,255))

        pygame.draw.rect(screen,(255,0,0),returnRect)
    
        pygame.display.flip()

if __name__ == "__main__":
    instructionsLoop()