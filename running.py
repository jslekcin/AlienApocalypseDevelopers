import pygame, sys
from event_system import Event_system
import level1
import main_menu
import death_screen
import intructions
import tutorial

level = "level1"
prev_level = ""

while level != "quit":
    if level == "main_menu":
        level = main_menu.mainMenuLoop()

    if level == "level1":
        level = level1.level1()

    if level == "death_screen":
        level = death_screen.deathScreenLoop(prev_level)

    if level == "instructions":
        level = intructions.instructionsLoop()
    
    if level == "tutorial":
        level = tutorial.tutorialLoop()

    for event in pygame.event.get():
            if event.type == Event_system.On_Death:
                print("dead")
                prev_level = level
                level = "death_screen"