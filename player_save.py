import sys, pygame

class Save:
    starting_pos = 0, 0
    health = 100
    stamina = 120
    gems = [0] * 5
    gems[0] = 0
    boss_defeated = [False] * 5
    portal_activated = [False] * 5

    #portal_activated[1] = True
    #boss_defeated[0] = True

    maxCoolDownBar = 100
    coolDownBar = 0
    onCoolDown = False


    weapons = {"Bat":False,"Sword":False,"Gun":False,"LaserGun":False}

    DeathScreens = {"FlyingEnemy":pygame.image.load('Images/FlyingDeath.png'), "PoisonShooterEnemy":pygame.image.load("Images/PoisonDeath.png"), "ReaperEnemy":pygame.image.load("Images/ReaperDeath.png"), "UFOBoss": pygame.image.load("Images/UFODeath.png"), "poison_blob": pygame.image.load("Images/PoisonBlobDeath.png"), "NewPoisonShooter":pygame.image.load("Images/NewPoisonDeath.png"), "WizardEnemy":pygame.image.load("Images/WizardDeath.png"), "FinalBoss":pygame.image.load("Images/FinalBossDeath.png")}
    
    LastDamageSource = ()