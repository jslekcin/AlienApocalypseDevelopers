import sys, pygame

class Save:
    starting_pos = 0, 0
    health = 100
    stamina = 120
    gems = [0] * 5
    gems[0] = 5
    boss_defeated = [False] * 5
    #boss_defeated[0] = True
    portal_activated = [False] * 5


    weapons = {"Bat":False,"Sword":True,"Gun":True,"LaserGun":False}

    