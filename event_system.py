import pygame, sys

class Event_system:
    On_Death = pygame.USEREVENT+1
    On_Blob_Death = pygame.USEREVENT+2
    On_Portal_Collision = pygame.USEREVENT+3