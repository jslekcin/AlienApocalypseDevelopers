import pygame
import level1
import main_menu
import death_screen
import intructions

level = "main_menu"

while level != "quit":
    if level == "main_menu":
        level = main_menu.mainMenuLoop()

    if level == "level1":
        level = level1.level1()

    if level == "death_screen":
        level = death_screen.deathScreenLoop()

    if level == "instructions":
        level = intructions.instructionsLoop()