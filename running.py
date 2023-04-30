import pygame, sys
from event_system import Event_system
import level1
import main_menu
import death_screen
import intructions
import tutorial
import boss_fight
import poison_level
import poison_boss
import win_screen
from player_save import Save

level = "tutorial"
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
    
    if level == "boss_fight":
        level = boss_fight.boss_fight_loop()

    if level == "poison_level":
        level = poison_level.poisonLevelLoop()

    if level == "poison_boss":
        level = poison_boss.poison_boss_loop()

    if level == "win_screen":
        level = win_screen.WinScreenLoop()

    for event in pygame.event.get():
            if event.type == Event_system.On_Death:
                print("dead")
                Save.health = 100
                Save.stamina = 120
                prev_level = level
                level = "death_screen"