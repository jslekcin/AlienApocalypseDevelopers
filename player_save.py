import sys, pygame

class Save:
    starting_pos = 0, 0
    health = 100
    stamina = 120
    gems = [0] * 5
    gems[0] = 5
    boss_defeated = [False] * 5
    portal_activated = [False] * 5

    #portal_activated[1] = True
    #boss_defeated[0] = True

    maxCoolDownBar = 100
    coolDownBar = 0
    onCoolDown = False


    weapons = {"Bat":True,"Sword":True,"Gun":True,"LaserGun":True}

    