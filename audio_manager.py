import sys, pygame
pygame.mixer.init()

class sounds:
    dictionary = {
        "gunshot":(pygame.mixer.Sound('sounds\gunshot.mp3'),0.3),
        "batSwing":(pygame.mixer.Sound('sounds\BatSwing.mp3'),0.3),
        "gatlingGun":(pygame.mixer.Sound('sounds\GatlingGun.mp3'),0.3),
        "placePortal":(pygame.mixer.Sound('sounds\PlacePortal.mp3'),0.3),
        "poisonBossLaser":(pygame.mixer.Sound('sounds\PoisonBossLaser.mp3'),0.3),
        "poisonProjectile":(pygame.mixer.Sound('sounds\PoisonProjectile.mp3'),0.3),
        "splash1":(pygame.mixer.Sound('sounds\PoisonSplash1.mp3'),0.3),
        "splash2":(pygame.mixer.Sound('sounds\PoisonSplash2.mp3'),0.3),
        "swordImpact":(pygame.mixer.Sound('sounds\SwordImpact.mp3'),0.3),
        "swordSwing":(pygame.mixer.Sound('sounds\SwordSwing.mp3'),0.3),
        "teleport":(pygame.mixer.Sound('sounds\Teleport.mp3'),0.3),
        "UFOBomb":(pygame.mixer.Sound('sounds\UFOBomb2.wav'),0.3),
        "UFOLaser":(pygame.mixer.Sound('sounds\UFOLaser.wav'),0.3),
                  }
    def playsound(sound):
        sounds.dictionary[sound][0].set_volume(sounds.dictionary[sound][1])
        sounds.dictionary[sound][0].play()
