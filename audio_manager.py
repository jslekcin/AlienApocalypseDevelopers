import sys, pygame
pygame.mixer.init()

class sounds:
    dictionary = {"gunshot":(pygame.mixer.Sound('sounds\gunshot.mp3'),0.3)}
    def playsound(sound):
        sounds.dictionary[sound][0].set_volume(sounds.dictionary[sound][1])
        sounds.dictionary[sound][0].play()
