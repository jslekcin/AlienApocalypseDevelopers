from re import L
import sys, pygame, math, random
from pygame.constants import K_2

from pygame.locals import *
from pygame import mixer

from event_system import Event_system
from player_save import Save
from wall_save import WallSave
from audio_manager import sounds


def level1():
    loadFile = True

    pygame.init()
    pygame.font.init()
    pygame.mixer.init()

    pygame.mixer.music.load('GameMusic/main.mp3')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

    #from main_menu import mainMenuLoop

    uiFont = pygame.font.Font(None, 32)
    levelFont = pygame.font.Font(None, 64)

    size = width, height = 750, 750 # TODO: Decide on final window size
    screen = pygame.display.set_mode(size) 
    fps = 60

    black = (0,0,0)
    background = pygame.image.load('Images\sky.png')
    background = pygame.transform.scale(background, size)
    gameState = 1

    clock = pygame.time.Clock()

    # Classes
    class Player:
        # Loads image and creates a rect out of it
        image = pygame.image.load("Images\player.png") 
        poisonImage = pygame.image.load("Images\Posioned Player.PNG")
        rect = image.get_rect(center = Save.starting_pos)
        # Creates a static rect to display in the center of the screen
        renderRect = image.get_rect(center = Save.starting_pos)
        renderRect.center = (width/2, height/2)
        # Create movement variables
        xAcceleration = .1 # Running speed
        xFriction = .2     # How much we slow down
        yAcceleration = .4 # Gravity
        xSpeed = 0
        ySpeed = 0
        # Sprinting Variables
        maxStamina = 120
        staminaRegen = .5
        stamina = Save.stamina
        sprintCooldown = False
        maxWalkSpeed = 6
        maxRunSpeed = 12
        # Stats
        maxHealth = 100
        isPoisoned = False
        health = Save.health
        prev_health = health
        regenTimer = fps * 10
        portalPlaced = False
        poisonTimer = fps * 2
        poisonCounter = 0
        # Equipment
        weapon = None
        attackCooldown = 0
        #LaserGun
        maxCoolDownBar = Save.maxCoolDownBar
        coolDownBar = Save.coolDownBar
        onCoolDown = Save.onCoolDown

        

        def update():
            if Player.health < Player.prev_health:
                Player.regenTimer = fps * 10
            
            else: 
                Player.regenTimer -= 1

            if Player.regenTimer <= 0:
                Player.health += 0.005 
            if Player.health > Player.maxHealth:
                Player.health = 100

            s = .1 * Player.rect.w
            w = .8 * Player.rect.w
            belowRect = pygame.Rect((Player.rect.left + s, Player.rect.bottom), (w, 2))

            leftRect  = pygame.Rect((Player.rect.left - 2, Player.rect.top + s - 10), (2, w * 1.8))

            rightRect = pygame.Rect((Player.rect.right, Player.rect.top + s - 10), (2, w * 1.8))

            topRect   = pygame.Rect((Player.rect.left + s, Player.rect.top - 2), (w, 2))

            #pygame.draw.rect(screen, (255,0,0), belowRect.move(-Player.rect[0] + Player.renderRect[0], -Player.rect[1] + Player.renderRect[1]-5))
            #pygame.draw.rect(screen, (255,0,0), leftRect.move(-Player.rect[0] + Player.renderRect[0], -Player.rect[1] + Player.renderRect[1]-5))
            #pygame.draw.rect(screen, (255,0,0), rightRect.move(-Player.rect[0] + Player.renderRect[0], -Player.rect[1] + Player.renderRect[1]-5))
            #pygame.draw.rect(screen, (255,0,0), topRect.move(-Player.rect[0] + Player.renderRect[0], -Player.rect[1] + Player.renderRect[1]-5))

            # Gets whether or not we are sprinting
            sprinting = False
            if pygame.key.get_pressed()[pygame.K_LSHIFT] and Player.stamina > 0 and Player.sprintCooldown is False:
                sprinting = True
                Player.stamina -= 1
                
            if Player.stamina == 0:
                Player.sprintCooldown = True

            if Player.stamina == Player.maxStamina:
                Player.sprintCooldown = False

            if sprinting == False and Player.stamina < Player.maxStamina:
                Player.stamina += Player.staminaRegen

            # Player.xAcceleration = (-((Player.xSpeed-10)/-.00001)**.25+31.54).real
            
            # TODO: Use this formula for jumping not going side
            # TODO: Fix so that 4th root does not make complex number

            # Checks if we have input to move right
            if pygame.key.get_pressed()[pygame.K_d]:
                Player.xSpeed += Player.xAcceleration + sprinting * Player.xAcceleration
                
            # Checks if we have input to move left
            if pygame.key.get_pressed()[pygame.K_a]:
                Player.xSpeed -= Player.xAcceleration + sprinting * Player.xAcceleration

            if sprinting == False:
                    if Player.xSpeed >= Player.maxWalkSpeed:
                        Player.xSpeed = Player.maxWalkSpeed

                    if Player.xSpeed <= -Player.maxWalkSpeed:
                        Player.xSpeed  = -Player.maxWalkSpeed

            else:
                if Player.xSpeed >= Player.maxRunSpeed:
                    Player.xSpeed = Player.maxRunSpeed

                if Player.xSpeed <= -Player.maxRunSpeed:
                    Player.xSpeed  = -Player.maxRunSpeed
            
            upA    = False
            leftA  = False
            rightA = False
            downA  = False
            if Player.ySpeed < 0:
                upA = True
            if Player.xSpeed < 0:
                leftA = True
            if Player.xSpeed > 0:
                rightA = True
            if Player.ySpeed > 0:
                downA = True

            upC    = False
            leftC  = False
            rightC = False
            downC  = False
            for wall in walls:
                # Standing on floor
                if wall.rect.colliderect(belowRect):
                    downC = True
                    if downA:
                        Player.ySpeed = 0
                        Player.rect.bottom = wall.rect.top
                    # Slows player x movement
                    if Player.xSpeed > 0 and not pygame.key.get_pressed()[pygame.K_d]:
                        Player.xSpeed -= Player.xFriction
                    if Player.xSpeed < 0 and not pygame.key.get_pressed()[pygame.K_a]:
                        Player.xSpeed += Player.xFriction
                    # Jump
                    if pygame.key.get_pressed()[pygame.K_SPACE]:
                        Player.ySpeed = -10
                if wall.rect.colliderect(leftRect):
                    leftC = True
                    if leftA:
                        Player.xSpeed = 0
                        Player.rect.left = wall.rect.right
                if wall.rect.colliderect(rightRect):
                    rightC = True
                    if rightA:
                        Player.xSpeed = 0
                        Player.rect.right = wall.rect.left
                if wall.rect.colliderect(topRect):
                    upC = True
                    if upA:
                        Player.ySpeed = 0
                        Player.rect.top = wall.rect.bottom
            

            Player.rect = Player.rect.move(Player.xSpeed, Player.ySpeed)

            # Updates player y position then the velocity based on acceleration
            Player.ySpeed += Player.yAcceleration

            #Weapon changing function
            if pygame.key.get_pressed()[pygame.K_1] and Save.weapons["Bat"]:
                Player.weapon = Bat()
            elif pygame.key.get_pressed()[pygame.K_2] and Save.weapons["Gun"]:
                Player.weapon = Gun()
            elif pygame.key.get_pressed()[pygame.K_3] and Save.weapons["Sword"]:
                Player.weapon = Sword()
            elif pygame.key.get_pressed()[pygame.K_4] and Save.weapons["LaserGun"]:
                Player.weapon = LaserGun()

            # Attack if player clicks
            if Player.attackCooldown > 0:
                Player.attackCooldown -= 1
            elif pygame.mouse.get_pressed(3)[0]:
                Player.weapon.attack()

            Player.prev_health = Player.health

            #if isinstance(Player.weapon, LaserGun):
                #print(Player.coolDownBar)
            Player.coolDownBar -= 0.2
            if Player.coolDownBar <= 0:
                Player.coolDownBar = 0
                Player.onCoolDown = False

            if Player.isPoisoned == True:
                #print(Player.poisonTimer, Player.isPoisoned)
                Player.poisonTimer -= 1
                Player.health -= 0.015 * Player.poisonCounter
                #print(self.poisonTimer)
                if Player.poisonTimer <= 0:
                    Player.isPoisoned = False
                    Player.poisonCounter = 0
                

            """if pygame.key.get_pressed()[pygame.K_p] and Save.gems[0] >= 5 and Player.portalPlaced == False:
                Player.portalPlaced = True
                print("portal placed")
                Save.gems[0] -= 5"""


            Player.renderRect.center = (width/2 - Player.xSpeed // 1, height/2 - Player.ySpeed // 1)

            

        def applyPoison():
            Player.poisonTimer = fps * 2

        def applyDamage(damage):
            Player.health -= damage

        def render():
            if Player.isPoisoned == False:
                screen.blit(Player.image, Player.renderRect)
            elif Player.isPoisoned:
                screen.blit(Player.poisonImage, Player.renderRect)
            Player.weapon.render()

    class Portal:
        def __init__(self):
            self.image = self.assignImage()
            self.rect = self.image.get_rect()
            #self.rect.bottom = Player.rect.bottom
            #self.rect[0] = Player.rect[0] - 150

        def update(self):
            if Player.portalPlaced == False:
                self.rect.bottom = Player.rect.bottom
                self.rect[0] = Player.rect[0] - 150
            elif Player.portalPlaced == True:
                if self.rect.colliderect(Player.rect):
                    Save.health = Player.health
                    Save.stamina = Player.stamina
                    print("collided")
                

        def assignImage(self):
            pass

        def render(self):
            adjustedRect = self.rect.move(-Player.rect[0] + Player.renderRect[0], -Player.rect[1] + Player.renderRect[1])
            screen.blit(self.image, adjustedRect)

    class UFO_Portal(Portal):
        def __init__(self):
            super().__init__()
            if Save.portal_activated[0] == False:
                self.rect = pygame.Rect(-744, 755, 460, 225)
                
            else:
                self.text = False
                self.image = self.assignImage()
                self.rect = self.image.get_rect()
                self.rect[0], self.rect[1] = -570, 790

        def update(self):
            """if Player.portalPlaced == False:
                self.rect.bottom = Player.rect.bottom
                self.rect[0] = Player.rect[0] - 150
            elif Player.portalPlaced == True:
                if self.rect.colliderect(Player.rect):
                    print("collided")"""
        
            if self.rect.colliderect(Player.rect):
                self.text = True
                if Save.portal_activated[0]:
                    Save.starting_pos = 0, 0
                    Save.health = Player.health
                    Save.stamina = Player.stamina
                    return "boss_fight"
                if pygame.key.get_pressed()[pygame.K_f] and Save.gems[0] >= 5 and Save.portal_activated[0] == False:
                        print("The Portal Has Been Summoned")
                        self.image = self.assignImage()
                        self.rect = self.image.get_rect()
                        self.rect[0], self.rect[1] = -570, 790
                        Save.portal_activated[0] = True
                        Save.gems[0] -= 5
            else:
                self.text = False
            
        def assignImage(self):
            image = pygame.image.load("Images/BossFightPortal2.png")
            image = pygame.transform.scale(image, (115,35))
            return image

        def render(self):
            adjustedRect = self.rect.move(-Player.rect[0] + Player.renderRect[0], -Player.rect[1] + Player.renderRect[1])
            if Save.portal_activated[0]:
                screen.blit(self.image, adjustedRect)
                #pygame.draw.rect(screen, (0, 0, 0), adjustedRect)

    class Poison_Portal(Portal):
        def __init__(self):
            super().__init__()
            self.rect.topleft = (2600, 710)

        def update(self):
            if self.rect.colliderect(Player.rect) and Save.boss_defeated[0]:
                print("collided")
                Save.starting_pos = (528, 609)
                Save.health = Player.health
                Save.stamina = Player.stamina
                Save.maxCoolDownBar = Player.maxCoolDownBar
                Save.coolDownBar = Player.coolDownBar
                Save.onCoolDown = Player.onCoolDown
                return "poison_level"
            
        def assignImage(self):
            if Save.boss_defeated[0]:
                image = pygame.image.load("Images/PoisonPortal.png")
            else:
                image = pygame.image.load("Images/PoisonPortalEmpty.png")
            image = pygame.transform.scale(image, (192,192))
            return image

        def render(self):
            adjustedRect = self.rect.move(-Player.rect[0] + Player.renderRect[0], -Player.rect[1] + Player.renderRect[1])
            screen.blit(self.image, adjustedRect)
                #pygame.draw.rect(screen, (0, 0, 0), adjustedRect)


    class healthItem:
        def __init__(self, worldPos):
            #self.image = pygame.Surface((30,30))
            #self.image.fill((222, 75, 151))
            self.image = pygame.image.load('Images/MedKit.png')
            self.image = pygame.transform.scale(self.image, (30,30))
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = worldPos

        def update(self):
            #self.rect.center = Player.rect.center
            #print(self.rect.x,self.rect.y,"updating")
            
            if self.rect.colliderect(Player.rect):
                Player.health += 20
                items.remove(self)
                print("item collided")
            
            floorCheck = (self.rect.centerx,self.rect.bottom + 5)
            floorCheck2 = (self.rect.centerx,self.rect.bottom + 1)
            move5 = True
            move1 = True
            for wall in walls:
                if wall.rect.collidepoint(floorCheck):
                    move5 = False
                if wall.rect.collidepoint(floorCheck2):
                    move1 = False

            if move5 == True:
                self.rect = self.rect.move(0,5)
            elif move1 == True:
                self.rect = self.rect.move(0,1)
        
        def render(self):
            #print("rendering")
            adjustedRect = self.rect.move(-Player.rect[0] + Player.renderRect[0], -Player.rect[1] + Player.renderRect[1])
            # Renders wall using modified rect
            screen.blit(self.image, adjustedRect)

                

    class Weapon:
        def __init__(self):
            self.name = 'None'

        def attack(self):
            pass

        def render(self):
            pass
    class Sword(Weapon):
        def __init__(self):
            self.name = 'Sword'
            self.damage = 8
            self.attackSpeed = .7
            self.image_left = pygame.image.load("Images/Sword(left).png")
            self.image_left = pygame.transform.scale(self.image_left, (110,140))
            self.image_right = pygame.image.load("Images/Sword(right).png")
            self.image_right = pygame.transform.scale(self.image_right, (110,140))
        def attack(self):
            sounds.playsound("swordSwing")
            hitBox = pygame.Rect(0, 0, 45, 64)
            mousePos = pygame.mouse.get_pos()
            if pygame.mouse.get_pos()[0] - Player.renderRect.centerx < 0:
                hitBox.topright = Player.rect.topleft
            else:
                hitBox.topleft = Player.rect.topright
                #do damage to enemies left of the player
            for enemy in enemies:
                if hitBox.colliderect(enemy.rect):
                    sounds.playsound("swordImpact")
                    enemy.health -= self.damage
                    #print("hit")

            Player.attackCooldown = self.attackSpeed * fps
        def render(self):
            mousePos = pygame.mouse.get_pos()
            if mousePos[0] >= Player.renderRect.centerx:
                #pass
                screen.blit(self.image_right, (Player.renderRect.centerx-18, Player.renderRect.centery-75))
            elif mousePos[0] < Player.renderRect.centerx:
                #pass
                screen.blit(self.image_left, (Player.renderRect.centerx-78, Player.renderRect.centery-80))

    class Gun(Weapon):
        def __init__(self):
            self.name = 'Gun'
            self.image_left = pygame.image.load("Images/gun (left).png")
            self.image_left = pygame.transform.scale(self.image_left, (60,70))
            self.image_right = pygame.image.load("Images/gun (right).png")
            self.image_right = pygame.transform.scale(self.image_right, (60,70)) 
            self.attackSpeed = 1
            self.projectileSpeed = 15
        def attack(self):
            #gunshot sound
            sounds.playsound("gunshot")
            #pygame.mixer.music.load('sounds\gunshot.mp3')
            #pygame.mixer.music.set_volume(0.3)
            #pygame.mixer.music.play()

            mousePos = pygame.mouse.get_pos()
            dx = mousePos[0] - Player.renderRect.centerx
            dy = mousePos[1] - Player.renderRect.centery
            if dx == 0:
                dx = .001
            angle = math.atan(dy/dx)
            if dx < 0:
                angle += math.pi
            xSpeed = self.projectileSpeed * math.cos(angle)
            ySpeed = self.projectileSpeed * math.sin(angle)
            projectiles.append(Bullet(xSpeed, ySpeed))
            Player.attackCooldown = self.attackSpeed * fps
        def render(self):
            mousePos = pygame.mouse.get_pos()
            dx = mousePos[0] - Player.renderRect.centerx
            dy = mousePos[1] - Player.renderRect.centery
            if dx == 0:
                dx = .001
            angle = math.atan(dy/dx)
            if dx < 0:
                angle += math.pi 
            if mousePos[0] >= Player.renderRect.centerx:
                #pass
                screen.blit(self.image_right, (Player.renderRect.centerx+-10, Player.renderRect.centery-35))
            elif mousePos[0] < Player.renderRect.centerx:
                #pass
                screen.blit(self.image_left, (Player.renderRect.centerx-45, Player.renderRect.centery-40))
                
            #pygame.draw.line(screen, (0,255,0), Player.renderRect.center, pygame.mouse.get_pos())

    class Bullet:
        def __init__(self, xSpeed, ySpeed):
            self.xSpeed = xSpeed
            self.ySpeed = ySpeed
            self.image = pygame.Surface((10,10))
            self.image.fill((70,70,70))
            self.rect = self.image.get_rect()
            self.rect.center = Player.rect.center
            self.deathTimer = 120
            self.damage = 10
            
        def update(self):
            self.rect = self.rect.move(self.xSpeed, self.ySpeed)
            for wall in walls:
                if self.rect.colliderect(wall.rect):
                    projectiles.remove(self)
                    return

            for enemy in enemies:
                if self.rect.colliderect(enemy.rect):
                    enemy.health -= self.damage
                    projectiles.remove(self)
                    return
                
            self.deathTimer -= 1
            if self.deathTimer < 1:
                projectiles.remove(self)
                print("disappear")
        def render(self):
            # Modifys the position based on the centered player position
            adjustedRect = self.rect.move(-Player.rect[0] + Player.renderRect[0], -Player.rect[1] + Player.renderRect[1])
            # Renders wall using modified rect
            screen.blit(self.image, adjustedRect)

    class GunItem:
        def __init__(self,worldPos,image,size):
            #Bat Item
            self.pos = worldPos
            self.size = size
            self.rect = pygame.Rect(self.pos,self.size)
            self.image = pygame.transform.scale(image, self.size)
            #self.rect = self.image.get_rect()
            

        def update(self):
            #print(self.rect)
            self.rect.center = self.pos
            if self.rect.colliderect(Player.rect):
                Save.weapons["Gun"] = True

        def render(self):
            #adjust position based on players position
            adjustedRect = self.rect.move(-Player.rect[0] + Player.renderRect[0], -Player.rect[1] + Player.renderRect[1])
            #render image
            if Save.weapons["Gun"] == False:
                screen.blit(self.image, adjustedRect)

    class LaserGun(Weapon):
        def __init__(self):
            self.name = 'LaserGatlingGun'
            mousePos = pygame.mouse.get_pos()
            mouse_x, mouse_y = pygame.mouse.get_pos()
            rel_x, rel_y = mouse_x - Player.renderRect.centerx-85, mouse_y - Player.renderRect.centerx-35
            self.angle = 0
            self.scale = 1
            self.image_angle = math.atan2(rel_y, rel_x)
            self.image_angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
            self.center = (0,0)
            self.renderImage = pygame.image.load("Images/LaserGatlingGunv2(left).png")
            
            #left
            self.image_left = pygame.image.load("Images/LaserGatlingGunv2(left).png")
            self.image_left = pygame.transform.scale(self.image_left, (120,140))
            self.renderImage = pygame.transform.rotozoom(self.image_left, self.angle, self.scale)
            """self.new_rect = self.new_image_left.get_rect()
            self.center=[self.new_rect_left.centerx,self.new_rect_left.centery]"""#center
            
            
            #right
            
            self.image_right = pygame.image.load("Images/LaserGatlingGunv2(right).png")
            self.image_right = pygame.transform.scale(self.image_right, (120,140))
            self.renderImage = pygame.transform.rotozoom(self.image_right, self.angle, self.scale)
            """self.new_rect_right = self.new_image_right.get_rect()
            self.center=[self.new_rect_right.centerx,self.new_rect_right.centery]"""#center

            self.damage = 1
            self.attackSpeed = 0.2
            self.projectileSpeed = 20
            
        def attack(self):
            if Player.onCoolDown == False:
                sounds.playsound("gatlingGun")
                Player.coolDownBar += 7
                if Player.coolDownBar > 100:
                    Player.coolDownBar = 100

                mousePos = pygame.mouse.get_pos()
                dx = mousePos[0] - Player.renderRect.centerx
                dy = mousePos[1] - Player.renderRect.centery
                if dx == 0:
                    dx = .001
                angle = math.atan(dy/dx)
                if dx < 0:
                    angle += math.pi
                
                xSpeed = self.projectileSpeed * math.cos(angle)
                ySpeed = self.projectileSpeed * math.sin(angle)
                projectiles.append(LaserBullet(xSpeed, ySpeed))

                if Player.coolDownBar >= Player.maxCoolDownBar:
                    Player.onCoolDown = True        

                Player.attackCooldown = self.attackSpeed * fps        

        def render(self):
            mousePos = pygame.mouse.get_pos()
            dx = mousePos[0] - Player.renderRect.centerx
            dy = mousePos[1] - Player.renderRect.centery
            if dx == 0:
                dx = .001
            angle = math.atan(dy/dx)
            if dx < 0:
                angle += math.pi
            #image_angle = math.atan(mousePos[1]/mousePos[0])
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            #print(image_angle)
            if mousePos[0] >= Player.renderRect.centerx:
                rel_x, rel_y = mouse_x - Player.renderRect.centerx-35, mouse_y - Player.renderRect.centerx-35
                self.image_angle = math.atan2(rel_y, rel_x)
                self.image_angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)

                self.renderImage = pygame.transform.rotozoom(self.image_right, self.image_angle, self.scale)
                screen.blit(self.renderImage, (Player.renderRect.centerx-35, Player.renderRect.centery-35))#10

            elif mousePos[0] < Player.renderRect.centerx:
                rel_x, rel_y = mouse_x - Player.renderRect.centerx-85, mouse_y - Player.renderRect.centerx-35
                self.image_angle = math.atan2(rel_y, rel_x)
                self.image_angle = (180 / math.pi) * -math.atan2(rel_y, rel_x) - 180
                
                self.renderImage = pygame.transform.rotozoom(self.image_left, self.image_angle, self.scale)
                screen.blit(self.renderImage, (Player.renderRect.centerx-85, Player.renderRect.centery-35))
                
            #pygame.draw.line(screen, (0,255,0), Player.renderRect.center, pygame.mouse.get_pos())


    class LaserBullet(Bullet):
        def __init__(self, xSpeed, ySpeed):
            self.xSpeed = xSpeed
            self.ySpeed = ySpeed
            self.image = pygame.Surface((10,10))
            self.image.fill((200,0,0))#70
            self.rect = self.image.get_rect()
            self.rect.center = Player.rect.center
            self.deathTimer = 120
            
            
        def update(self):
            self.rect = self.rect.move(self.xSpeed, self.ySpeed)
            for wall in walls:
                if self.rect.colliderect(wall.rect):
                    projectiles.remove(self)
                    return

            for enemy in enemies:
                if self.rect.colliderect(enemy.rect):
                    enemy.health -= 3
                    projectiles.remove(self)
                    return
                
            self.deathTimer -= 1
            if self.deathTimer < 1:
                projectiles.remove(self)
                print("disappear")
                

        def render(self):
            # Modifys the position based on the centered player position
            adjustedRect = self.rect.move(-Player.rect[0] + Player.renderRect[0], -Player.rect[1] + Player.renderRect[1])
            # Renders wall using modified rect
            screen.blit(self.image, adjustedRect)

    


    class Bat(Weapon):
        def __init__(self):
            self.name = 'Bat'
            self.damage = 6
            self.range = 32 #irection we are facing and create a rect in that direction
            self.attackSpeed = 1
            self.image = pygame.image.load("Images\Bat3.PNG")
            self.image = pygame.transform.scale(self.image,(120,130))
        def attack(self):
            sounds.playsound("batSwing")
            # Figure out which class Bat(Weapon):
            attackBox = pygame.Rect(0, 0, self.range, 64)
            if pygame.mouse.get_pos()[0] - Player.renderRect.centerx < 0:
                attackBox.topright = Player.rect.topleft
            else:
                attackBox.topleft = Player.rect.topright

            # Debug show attack box
            adjustedRect = attackBox.move(-Player.rect[0] + Player.renderRect[0], -Player.rect[1] + Player.renderRect[1])
            #pygame.draw.rect(screen, (255,255,255), adjustedRect)

            # See if it collides with enemies and if it does, damages it
            for enemy in enemies:
                if attackBox.colliderect(enemy.rect):
                    enemy.health -= self.damage
                    print("Bat has hit")

            Player.attackCooldown = self.attackSpeed * fps
        def render(self):
            mousePos = pygame.mouse.get_pos()
            if mousePos[0] >= Player.renderRect.centerx:
                #pass
                screen.blit(self.image, (Player.renderRect.centerx-40, Player.renderRect.centery-80))
            elif mousePos[0] < Player.renderRect.centerx:
                #pass
                screen.blit(self.image, (Player.renderRect.centerx-85, Player.renderRect.centery-80))

    Player.weapon = Weapon()
    walls = []
    class Wall:
        def __init__(self, worldPos, image, size, imageIndex): 
            # Generates rect from given parameters
            self.image = pygame.transform.scale(image, size)
            self.rect = pygame.Rect(worldPos,size)
            self.imageIndex = imageIndex

        def update(self):
            pass

        def render(self):
            # Modifys the position based on the centered player position
            adjustedRect = self.rect.move(-Player.rect[0] + Player.renderRect[0], -Player.rect[1] + Player.renderRect[1])
            # Renders wall using modified rect
            screen.blit(self.image, adjustedRect)

    class Enemy:
        def __init__(self, worldPos, image, size):
            # Generates rect from given parameters
            self.size = size
            self.image = pygame.transform.scale(image, self.size)
            self.rect = pygame.Rect(worldPos,size)
            
            self.maxHealth = 10
            self.health = self.maxHealth

            # Movement Variables
            self.facingLeft = False
            self.speed = 1

        def update(self):
            # Check that enemy is on screen
            if Player.rect.x - self.rect.x < 500 or Player.rect.x - self.rect.x > -500:
                # Set the direction enemy is facing
                if self.rect.x < Player.rect.x:
                    self.facingLeft = False
                else:
                    self.facingLeft = True

                # Move based on direction facing
                if self.facingLeft:
                    moveable = False
                    collideRect = pygame.Rect(self.rect.x - self.speed, self.rect.y, self.speed, self.rect.h)
                    for wall in walls:
                        if wall.rect.collidepoint((self.rect.left - 1, self.rect.bottom + 1)):
                            moveable = True
                        if wall.rect.colliderect(collideRect):
                            moveable = False
                            break
                    if collideRect.colliderect(Player.rect):
                        moveable = False

                    if moveable:
                        self.rect = self.rect.move(-self.speed, 0)
                else:
                    moveable = False
                    collideRect = pygame.Rect(self.rect.right, self.rect.y, self.speed, self.rect.h)
                    for wall in walls:
                        if wall.rect.collidepoint((self.rect.right + 1, self.rect.bottom + 1)):
                            moveable = True
                        if wall.rect.colliderect(collideRect):
                            moveable = False
                            break
                        if collideRect.colliderect(Player.rect):
                            moveable = False

                    if moveable:
                        self.rect = self.rect.move(self.speed, 0)

            if self.health <= 0:
                enemies.remove(self)
                Save.enemyCounter += 1
                if Save.enemyCounter >= 3:
                    number = 1
                    Save.enemyCounter = 0
                else:
                    number = random.randint(1,10)
                if number == 1 and Save.boss_defeated[0] == False and Save.gems[0] < 5:
                    gems.append(Gem(self.rect.x,self.rect.bottom))
                    Save.enemyCounter = 0
                if number == 2:
                    items.append(healthItem((self.rect.x,self.rect.centery)))
                    

        def render(self):
            # Modifys the position based on the centered player position
            adjustedRect = self.rect.move(-Player.rect[0] + Player.renderRect[0], -Player.rect[1] + Player.renderRect[1])
            healthRect = pygame.Rect(adjustedRect.x, adjustedRect.y - 10, self.health / self.maxHealth * adjustedRect.w, 10)
            # Renders wall using modified rect
            screen.blit(self.image, adjustedRect)
            pygame.draw.rect(screen, (0,255,0), healthRect)

    class RangedEnemy:
        def __init__(self, worldPos, image, size):
            # Generates rect from given parameters
            self.size = size
            self.image = pygame.transform.scale(image, self.size)
            self.rect = pygame.Rect(worldPos,size)
            
            self.maxHealth = 10
            self.health = self.maxHealth

            # Movement Variables
            self.facingLeft = False
            self.speed = 1

            self.fleeRange = 200
            self.attackRange = 400
            self.approachRange = 600

            self.counter = 0

        def update(self):
            # Check that enemy is on screen
            distToPlayer = abs(Player.rect.x - self.rect.x)
            if distToPlayer <= self.approachRange and distToPlayer >= self.attackRange or distToPlayer < self.fleeRange:
                if distToPlayer >= self.attackRange:
                    # Set the direction enemy is facing
                    if self.rect.x < Player.rect.x:
                        self.facingLeft = False
                    else:
                        self.facingLeft = True
                else:
                    # Set the direction enemy is facing
                    if self.rect.x < Player.rect.x:
                        self.facingLeft = True
                    else:
                        self.facingLeft = False

                # Move based on direction facing
                if self.facingLeft:
                    moveable = False
                    collideRect = pygame.Rect(self.rect.x - self.speed, self.rect.y, self.speed, self.rect.h)
                    for wall in walls:
                        if wall.rect.collidepoint((self.rect.left - 1, self.rect.bottom + 1)):
                            moveable = True
                        if wall.rect.colliderect(collideRect):
                            moveable = False
                            break
                    if collideRect.colliderect(Player.rect):
                        moveable = False

                    if moveable:
                        self.rect = self.rect.move(-self.speed, 0)
                else:
                    moveable = False
                    collideRect = pygame.Rect(self.rect.right, self.rect.y, self.speed, self.rect.h)
                    for wall in walls:
                        if wall.rect.collidepoint((self.rect.right + 1, self.rect.bottom + 1)):
                            moveable = True 
                        if wall.rect.colliderect(collideRect):
                            moveable = False
                            break
                        if collideRect.colliderect(Player.rect):
                            moveable = False

                    if moveable:
                        self.rect = self.rect.move(self.speed, 0)

            elif distToPlayer < self.attackRange and distToPlayer >= self.fleeRange:
                # How often they attack
                self.counter += 1
                if self.counter >= 60:
                    self.counter = 0

                    # Aiming
                    xdist = Player.rect.centerx - self.rect.centerx
                    ydist = Player.rect.centery - self.rect.centery
                    angle = math.degrees(math.atan2(ydist,xdist))
                    # Add in inaccuracy
                    angle = angle + random.randint(-40,40)
                    angle = math.radians(angle)
                    projectiles.append(RangedEnemyProjectile(self.rect.center, 5, 5, angle))

            if self.health <= 0:
                enemies.remove(self)
                Save.enemyCounter += 1
                if Save.enemyCounter >= 3:
                    number = 1
                    Save.enemyCounter = 0
                else:
                    number = random.randint(1,10)
                if number == 1 and Save.boss_defeated[0] == False and Save.gems[0] < 5:
                    gems.append(Gem(self.rect.x,self.rect.bottom))
                    Save.enemyCounter = 0
                if number == 2:
                    items.append(healthItem((self.rect.x,self.rect.centery)))

        def render(self):
            # Modifys the position based on the centered player position
            adjustedRect = self.rect.move(-Player.rect[0] + Player.renderRect[0], -Player.rect[1] + Player.renderRect[1])
            healthRect = pygame.Rect(adjustedRect.x, adjustedRect.y - 10, self.health / self.maxHealth * adjustedRect.w, 10)
            # Renders wall using modified rect
            screen.blit(self.image, adjustedRect)
            pygame.draw.rect(screen, (0,255,0), healthRect)
            

    class RangedEnemyProjectile:
        def __init__(self, location, damage, speed, angle):
            self.image = pygame.Surface((20,20))
            pygame.draw.circle(self.image, (23,52,200), (10,10), 10)
            self.rect = self.image.get_rect()
            self.rect.center = location
            self.damage = damage
            self.speed = speed
            self.angle = angle
        def update(self):
            # Moving the projectile
            x = self.speed * math.cos(self.angle)
            y = self.speed * math.sin(self.angle)
            self.rect = self.rect.move(x,y)
            # Check if it hits anything
            if self.rect.colliderect(Player.rect):
                # Do damage if it does
                Player.applyDamage(self.damage)
                projectiles.remove(self)

        def render(self):
            # Modifys the position based on the centered player position
            adjustedRect = self.rect.move(-Player.rect[0] + Player.renderRect[0], -Player.rect[1] + Player.renderRect[1])
            # Renders wall using modified rect
            screen.blit(self.image, adjustedRect)

    class PoisonShooterEnemy: # Jaeho
        def __init__(self, worldPos, image, size): # Create the enemy
            # Generates rect from given parameters
            self.size = size
            self.image = pygame.transform.scale(image, self.size)
            self.rect = pygame.Rect(worldPos,size)
            
            self.damage = 5
            self.maxHealth = 20
            self.health = self.maxHealth
            self.speed  = 4

            self.shootingDirection = 0
            
            self.approachRange = 300
            self.attackRange = 200
            self.fleeRange = 100

            self.counter = 0
            
        def update(self): # Change the enemies variables (like position)
            # Check that enemy is on screen
            distToPlayer = abs(Player.rect.x - self.rect.x)
            if distToPlayer <= self.approachRange and distToPlayer >= self.attackRange or distToPlayer < self.fleeRange:
                if distToPlayer >= self.attackRange:
                    # Set the direction enemy is facing
                    if self.rect.x < Player.rect.x:
                        self.facingLeft = False
                    else:
                        self.facingLeft = True
                else:
                    # Set the direction enemy is facing
                    if self.rect.x < Player.rect.x:
                        self.facingLeft = True
                    else:
                        self.facingLeft = False
            
                # Move based on direction facing
                if self.facingLeft:
                    moveable = False
                    collideRect = pygame.Rect(self.rect.x - self.speed, self.rect.y, self.speed, self.rect.h)
                    for wall in walls:
                        if wall.rect.collidepoint((self.rect.left - 1, self.rect.bottom + 1)):
                            moveable = True
                        if wall.rect.colliderect(collideRect):
                            moveable = False
                            break
                    if collideRect.colliderect(Player.rect):
                        moveable = False

                    if moveable:
                        self.rect = self.rect.move(-self.speed, 0)
                else:
                    moveable = False
                    collideRect = pygame.Rect(self.rect.right, self.rect.y, self.speed, self.rect.h)
                    for wall in walls:
                        if wall.rect.collidepoint((self.rect.right + 1, self.rect.bottom + 1)):
                            moveable = True
                        if wall.rect.colliderect(collideRect):
                            moveable = False
                            break
                        if collideRect.colliderect(Player.rect):
                            moveable = False

                    if moveable:
                        self.rect = self.rect.move(self.speed, 0)
            
            elif distToPlayer < self.attackRange and distToPlayer >= self.fleeRange:
                # How often they attack
                self.counter += 1
                if self.counter >= 60:
                    self.counter = 0

                    # Aiming
                    xdist = Player.rect.centerx - self.rect.centerx
                    ydist = Player.rect.centery - self.rect.centery
                    angle = math.degrees(math.atan2(ydist,xdist))
                    # Add in inaccuracy
                    angle = angle + random.randint(-40,40)
                    angle = math.radians(angle)
                    sounds.playsound("poisonProjectile")
                    projectiles.append(PoisonShooterEnemyProjectile(self.rect.center, 5, 5, angle))
            floorCheck = (self.rect.centerx,self.rect.bottom + 5)
            floorCheck2 = (self.rect.centerx,self.rect.bottom + 1)
            move5 = True
            move1 = True
            for wall in walls:
                if wall.rect.collidepoint(floorCheck):
                    move5 = False
                if wall.rect.collidepoint(floorCheck2):
                    move1 = False

            if self.health <= 0:
                enemies.remove(self)
                Save.enemyCounter += 1
                if Save.enemyCounter >= 3:
                    number = 1
                    Save.enemyCounter = 0
                else:
                    number = random.randint(1,10)
                if number == 1 and Save.boss_defeated[0] == False and Save.gems[0] < 5:
                    gems.append(Gem(self.rect.x,self.rect.bottom))
                    Save.enemyCounter = 0
                if number == 2:
                    items.append(healthItem((self.rect.x,self.rect.centery)))

            if move5 == True:
                self.rect = self.rect.move(0,5)
            elif move1 == True:
                self.rect = self.rect.move(0,1)
            
        def render(self): # Show the enemy and visual effects
            adjustedRect = self.rect.move(-Player.rect[0] + Player.renderRect[0], -Player.rect[1] + Player.renderRect[1])
            screen.blit(self.image, adjustedRect)
            healthRect = pygame.Rect(adjustedRect.x, adjustedRect.y - 10, self.health / self.maxHealth * adjustedRect.w, 10)
            pygame.draw.rect(screen, (0,255,0), healthRect)
            #Render Enemy
            #Render Poison blob

    #class RangedEnemyProjectile:
    class PoisonShooterEnemyProjectile:
        # When it hits somthing it will stay for a while
        def __init__(self, location, damage, speed, angle):
            #self.image = pygame.Surface((20,20))
            #pygame.draw.circle(self.image, (23,52,200), (10,10), 10)
            self.image = pygame.image.load("Images/Posion Projectile.PNG")
            self.rect = self.image.get_rect()
            self.rect.center = location
            self.damage = damage
            self.dx = speed * math.cos(angle)
            self.dy = speed * math.sin(angle)
            self.timer = 10 * fps
            self.poisonTimer = fps * 2
            self.splashed = False
        def update(self):
            # Check if it hits anything
            hit = False
            for wall in walls:
                if self.rect.colliderect(wall.rect):
                    if self.splashed == False:
                        sounds.playsound("splash1")
                        self.splashed = True
                    hit = True
                    break
            if hit:
                # Change image if hit something
                self.image = pygame.image.load("Images/poison puddle.PNG")
                #self.rect = self.image.get_rect()
                self.timer -= 1
                if self.timer <= 0:
                    projectiles.remove(self)
            else:
                # Moving the projectile
                self.dy += .05
                self.rect = self.rect.move(self.dx,self.dy)

            if self.rect.colliderect(Player.rect):
                # Do damage if it does
                Player.poisonCounter += 1
                print("Player hit", Player.poisonCounter)
                if hit == False:
                    Player.applyDamage(4)
                    Save.LastDamageSource = "PoisonShooterEnemy"
                Player.isPoisoned = True
                Player.applyPoison()
                projectiles.remove(self)
            

        def render(self):
            # Modifys the position based on the centered player position
            adjustedRect = self.rect.move(-Player.rect[0] + Player.renderRect[0], -Player.rect[1] + Player.renderRect[1])
            # Renders wall using modified rect
            screen.blit(self.image, adjustedRect)

    class ReaperEnemy: # Chris
        def __init__(self, worldPos, image, size): # Create the enemy
            # Generates rect from given parameters
            self.size = size
            self.image = pygame.transform.scale(image, self.size)
            #world pos might need double check
            self.rect = pygame.Rect(worldPos,size)
            self.damage = 20
            self.speed = 1
            self.maxHealth = 20
            self.health = self.maxHealth
            self.cooldown = 0

            self.invisiblity = 0
        def update(self): # Change the enemies variables (like position)
            if self.cooldown == 0:
                distToPlayer = ((Player.rect.x - self.rect.x)**2 + (Player.rect.y - self.rect.y)**2)**.5
                if distToPlayer < 50:
                    # Attack player
                    self.cooldown = 15 * fps
                    Player.applyDamage(self.damage)
                    Save.LastDamageSource = "ReaperEnemy"
                elif distToPlayer < 100:
                    self.invisibility = 100
                elif distToPlayer < 200:# close 75
                    self.invisibility = 25
                else:
                    self.invisibility = 0
            else:
                self.invisibility = 0
                self.cooldown -= 1
            
            if self.health <= 0:
                enemies.remove(self)
                Save.enemyCounter += 1
                if Save.enemyCounter >= 3:
                    number = 1
                    Save.enemyCounter = 0
                else:
                    number = random.randint(1,10)
                if number == 1 and Save.boss_defeated[0] == False and Save.gems[0] < 5:
                    gems.append(Gem(self.rect.x,self.rect.bottom))
                    Save.enemyCounter = 0
                if number == 2:
                    items.append(healthItem((self.rect.x,self.rect.centery)))
            floorCheck = (self.rect.centerx,self.rect.bottom + 5)
            floorCheck2 = (self.rect.centerx,self.rect.bottom + 1)
            move5 = True
            move1 = True
            for wall in walls:
                if wall.rect.collidepoint(floorCheck):
                    move5 = False
                if wall.rect.collidepoint(floorCheck2):
                    move1 = False

            if move5 == True:
                self.rect = self.rect.move(0,5)
            elif move1 == True:
                self.rect = self.rect.move(0,1)

        def render(self): # Show the enemy and visual effects
            # Modifys the position based on the centered player position
            adjustedRect = self.rect.move(-Player.rect[0] + Player.renderRect[0], -Player.rect[1] + Player.renderRect[1])
            self.image.set_alpha(self.invisibility / 100 * 255)
            # Renders wall using modified rect
            screen.blit(self.image, adjustedRect)
            healthRect = pygame.Rect(adjustedRect.x, adjustedRect.y - 10, self.health / self.maxHealth * adjustedRect.w, 10)
            surf = pygame.Surface(healthRect.size, pygame.SRCALPHA)
            pygame.draw.rect(surf, (0,255,0, self.invisibility / 100 * 255), surf.get_rect())
            screen.blit(surf,healthRect)

    class FlyingAilenEnemy:
        def __init__(self,worldPos,image,size):
            self.rect = pygame.Rect(worldPos,size)
            #self.rect.center = (Player.rect.centerx+200,Player.rect.centery-200)
            self.size = size
            self.image = pygame.transform.scale(image, self.size)
            self.damage = 5
            self.speed = 2
            self.maxHealth = 20
            self.health = self.maxHealth
            self.maxCooldown = 75
            self.cooldown = self.maxCooldown
            self.onCooldown = True
            self.topright = (Player.rect.centerx+200,Player.rect.centery-200)
            self.topleft = (Player.rect.centerx-200,Player.rect.centery-200)
            self.xpos = 200
            self.pos = (self.xpos,736)
            #self.rect.center = self.topleft
            self.onRight = False
            self.moving = False

            self.projectileSpeed = 10

            self.atRange = False
        def update(self):
            #self.topright = (Player.rect.centerx+200,Player.rect.centery-200)
            #self.topleft = (Player.rect.centerx-200,Player.rect.centery-200)
            #self.pos = (Player.rect.centerx+self.xpos,Player.rect.centery-200)
            self.topright = (Player.rect.centerx+200,736)
            self.topleft = (Player.rect.centerx-200,736)
            #self.pos = (Player.rect.centerx+self.xpos,736)
            
            
            #Attacking
            
            if self.onCooldown == False and ((abs(self.xpos-Player.rect.centerx) <= 600 and self.atRange) or self.atRange == False):
                #print("attack")

                #fire projectile
                dx = Player.rect.centerx - self.rect.centerx
                dy = Player.rect.centery - self.rect.centery
                if dx == 0:
                    dx = .001
                angle = math.atan(dy/dx)
                if dx < 0:
                    angle += math.pi
                xSpeed = self.projectileSpeed * math.cos(angle)
                ySpeed = self.projectileSpeed * math.sin(angle)
                center = self.rect.center
                projectiles.append(FlyingEnemyProjectile(xSpeed,ySpeed,center))


                #move positions
                self.moving = True
                if self.rect.centerx <= (Player.rect.centerx-200):
                    self.onRight = False
                
                elif self.rect.centerx >= (Player.rect.centerx+200):
                    self.onRight = True
                
                
                
                else:
                    self.onRight = False

                    
                #reset cooldown
                self.onCooldown = True
                self.cooldown = self.maxCooldown
            else:
                self.rect.center = self.pos
                self.cooldown -= 1
            if self.cooldown <= 0:
                if self.moving:
                    if self.onRight:
                        self.xpos -= 7
                        #self.pos = (Player.rect.centerx+self.xpos,Player.rect.centery-200)
                        self.pos = (self.xpos,736)
                        if self.rect.centerx <= (Player.rect.centerx-200):
                            self.moving = False
                            self.onRight = False
                            
                        

                    elif self.onRight == False:
                        pos2 = self.pos
                        self.xpos += 7
                        #self.pos = (Player.rect.centerx+self.xpos,Player.rect.centery-200)
                        self.pos = (self.xpos,736)
                        if self.rect.centerx >= (Player.rect.centerx+200):
                            self.moving = False
                            self.onRight = True
                        if self.pos[0] > 1037:
                            self.pos = pos2
                            self.xpos -= 7
                            self.moving = False
                            self.atRange = True

                else:
                    self.onCooldown = False
                
                

                #move closer to the player
            

                
            """if self.onCooldown == False:
                print("Attacked")
                Player.health -= self.damage
                self.cooldown = fps"""
            

            if self.health <= 0:
                enemies.remove(self)
                Save.enemyCounter += 1
                if Save.enemyCounter >= 3:
                    number = 1
                    Save.enemyCounter = 0
                else:
                    number = random.randint(1,10)
                if number == 1 and Save.boss_defeated[0] == False and Save.gems[0] < 5:
                    gems.append(Gem(self.rect.x,self.rect.bottom))
                    Save.enemyCounter = 0
                if number == 2:
                    items.append(healthItem((self.rect.x,self.rect.centery)))
            """floorCheck = (self.rect.centerx,self.rect.bottom + 5)
            floorCheck2 = (self.rect.centerx,self.rect.bottom + 1)
            move5 = True
            move1 = True
            for wall in walls:
                if wall.rect.collidepoint(floorCheck):
                    move5 = False
                if wall.rect.collidepoint(floorCheck2):
                    move1 = False

            if move5 == True:
                self.rect = self.rect.move(0,5)
            elif move1 == True:
                self.rect = self.rect.move(0,1)
            self.cooldown -= 1"""

            """if self.rect[1] >= 1500:
                self.rect[1] = 800"""
            
        def render(self):
            adjustedRect = self.rect.move(-Player.rect[0] + Player.renderRect[0], -Player.rect[1] + Player.renderRect[1])
            screen.blit(self.image, adjustedRect)
            healthRect = pygame.Rect(adjustedRect.x + 20, adjustedRect.y - 10, self.health / self.maxHealth * (adjustedRect.w - 45), 10)
            pygame.draw.rect(screen, (0,255,0), healthRect)

    class FlyingEnemyProjectile:
        def __init__(self, xSpeed, ySpeed,center):
            #self.image = pygame.Surface((30,30))
            #self.image.fill((0,255,0))
            self.image = pygame.image.load('Images/flying_proj.png')
            self.image = pygame.transform.scale(self.image, (30,30))
            self.rect = self.image.get_rect()
            self.xSpeed = xSpeed
            self.ySpeed = ySpeed
            self.rect.center = center
            self.deathTimer = 120
        def update(self):
            self.rect = self.rect.move(self.xSpeed, self.ySpeed)
            if self.rect.colliderect(Player.rect):
                Player.applyDamage(5)
                Save.LastDamageSource = "FlyingEnemy"
                projectiles.remove(self)
                return
            for wall in walls:
                if self.rect.colliderect(wall.rect):
                    projectiles.remove(self)
                    return
            self.deathTimer -= 1
            if self.deathTimer < 1:
                projectiles.remove(self)
                print("disappear")
            
            
        def render(self):
            # Modifys the position based on the centered player position
            adjustedRect = self.rect.move(-Player.rect[0] + Player.renderRect[0], -Player.rect[1] + Player.renderRect[1])
            # Renders wall using modified rect
            screen.blit(self.image, adjustedRect)

    class Gem:
        def __init__(self,x,bottom):
            #self.image = pygame.Surface((30,30))
            #self.image.fill((255,0,0))
            self.image = pygame.image.load("images/AlienGem.png")
            self.image = pygame.transform.scale(self.image, (50,50))
            self.rect = self.image.get_rect()
            self.rect.x,self.rect.bottom = x,bottom
            self.collected = False
        def update(self):
            if self.rect.colliderect(Player.rect):
                print("gem collected")
                Save.gems[0] += 1
                gems.remove(self)

            floorCheck = (self.rect.centerx,self.rect.bottom + 5)
            floorCheck2 = (self.rect.centerx,self.rect.bottom + 1)
            move5 = True
            move1 = True
            for wall in walls:
                if wall.rect.collidepoint(floorCheck):
                    move5 = False
                if wall.rect.collidepoint(floorCheck2):
                    move1 = False

            if move5 == True:
                self.rect = self.rect.move(0,5)
            elif move1 == True:
                self.rect = self.rect.move(0,1)
        def render(self):
            adjustedRect = self.rect.move(-Player.rect[0] + Player.renderRect[0], -Player.rect[1] + Player.renderRect[1])
            screen.blit(self.image, adjustedRect)
    # Walls(Pos, Image, Size)

    pageSize = 10
    # Creates pagse for the player platform
    for i in range(int(70/pageSize)):
        h = 1000
        page = Wall((pageSize*i,h), pygame.image.load('Images\Ground.png'), (pageSize,h), 0)
        walls.append(page)

    def saveMap():
        global walls
        print('saving')
        
        # Preparing our data for saving
        out = ''
        for wall in walls:
            out += str(wall.rect.x) + ' '
            out += str(wall.rect.y) + ' '
            out += str(wall.rect.w) + ' '
            out += str(wall.rect.h) + ' '
            out += str(wall.imageIndex) + ' '

            out += '\n'
            
        out = out.rstrip('\n')
            
        print(out)
        # Exporting to json file
        file = open("map.txt", "w")
        file.write(out)
        file.close()

    # worldPos, image, sized )
    gems = []
    ufoPortal = UFO_Portal()
    poisonPortal = Poison_Portal()
    enemies = [ReaperEnemy((367, 805), pygame.image.load('Images\Reaper.png'), (64,100)),PoisonShooterEnemy((-980, 854), pygame.image.load('Images\Posion Shooter Design.PNG'), (64,100)),FlyingAilenEnemy((-1126, 818),pygame.image.load('Images\Ailen.png'), (100,100))]
    projectiles = []
    foreground = [Wall((200,-100), pygame.image.load('Images\Bush.png'), (100,100), -1), Wall((200,0), pygame.image.load('Images\Bird.png'), (100,100), -1), Wall((200,-100), pygame.image.load('Images\Tree.png'), (100,100), -1)]
    midground = [Wall((200,-100), pygame.image.load('Images\Bush.png'), (100,100), -1), Wall((200,0), pygame.image.load('Images\Bird.png'), (100,100), -1), Wall((200,-100), pygame.image.load('Images\Tree.png'), (100,100), -1)]
    items = [healthItem((-1284, 919)), GunItem((1823, 647),pygame.image.load("Images/Gun (left).png"),(102,119))]

    generatingMap = not loadFile
    editPageNum = len(walls)-1
    editCooldown = 0

    tileSize = 25
    blockImageIndex = 0

    if loadFile:
        walls = []
        file = open("map.txt", "r")
        fileData = file.read().split('\n')
        file.close()
        for line in fileData:
            if line == '':
                break
            line = line.split()
            wall = Wall((int(line[0]),int(line[1])), WallSave.blockImages[int(line[4])], (int(line[2]),int(line[3])), int(line[4]))
            walls.append(wall)

    def enemyRespawn(enemies):
        enemies.append(FlyingAilenEnemy((-1126, 818),pygame.image.load('Images\Ailen.png'), (100,100)))
        for i in range(2):
            reaperX = random.randint(-1021,823)
            enemies.append(ReaperEnemy((reaperX, 654), pygame.image.load('Images\Reaper.png'), (64,100)))
        reaperX = random.randint(1194,2391)
        enemies.append(ReaperEnemy((reaperX, 480), pygame.image.load('Images\Reaper.png'), (64,100)))
        for i in range(2):
            poisonX = random.randint(-1121,829)
            enemies.append(PoisonShooterEnemy((poisonX, 654), pygame.image.load('Images\Posion Shooter Design.PNG'), (64,100)))
        poisonX = random.randint(1194,2391)
        enemies.append(PoisonShooterEnemy((poisonX, 480), pygame.image.load('Images\Posion Shooter Design.PNG'), (64,100)))
        #enemies = 
        #return enemies

    doubleHealth = 10
    level = 1
    paused = False

    portalRect = pygame.Rect(-744, 755, 460, 225)
    portalAdjustedRect = portalRect.move(-Player.rect[0] + Player.renderRect[0], -Player.rect[1] + Player.renderRect[1])

    titleTimer = fps * 3
    titleInvis = 45

    while 1:
        """if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            paused = not paused"""

        

        # The Great Clock #3
        deltaTime = clock.tick(fps)


        # Inputs Processing Code
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                break
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                #if event.key == pygame.K_p:
                    #Player.rect.center = 0, 0
                    #Player.ySpeed, Player.xSpeed = 0, 0
                

        if paused:
            pauseText = levelFont.render("Paused", True, (255, 255, 255))
            screen.blit(pauseText,(300,230))
            pygame.display.flip()
            continue

        # Main Menu
        if gameState == 0:
            # input
            #for event in pygame.event.get(pygame.KEYDOWN):
                #if pygame.key.get_pressed()[pygame.K_g]:
                    #gameState += 1
            # update
            # render
            #screen.fill(black)
            # print('TODO: Main Menu')
            #pygame.display.flip()
            #mainMenuLoop(gameState)
            pass


        # Gameplay
        if gameState == 1: 
            screen.blit(background, (0,0))
            # input
            #player.lastPos = player.pos
            for event in pygame.event.get(pygame.KEYDOWN):
                if pygame.key.get_pressed()[pygame.K_g]:
                    gameState += 1
                
                    
            #doubleHealth = 10
            if len(enemies) <= 0:
                level += 1
                enemyRespawn(enemies)
                #enemies = [ReaperEnemy((367, 805), pygame.image.load('Images\Reaper.png'), (64,100)),PoisonShooterEnemy((-819, 854), pygame.image.load('Images\Posion Shooter Design.PNG'), (64,100))]
                doubleHealth = doubleHealth * 2
                #print("Level:", level)
                """for enemy in enemies:
                    enemy.health = doubleHealth"""

            #draw player renderrect
            #pygame.draw.rect(screen,(0,255,0),Player.renderRect)

            portalAdjustedRect = portalRect.move(-Player.rect[0] + Player.renderRect[0], -Player.rect[1] + Player.renderRect[1])
            #pygame.draw.rect(screen, (0,0,0),portalAdjustedRect)
            # update
            Player.update()

            if poisonPortal.update() == "poison_level":
                return "poison_level"

            for gem in gems:
                gem.update()

            for wall in walls:
                wall.update()

            for projectile in projectiles:
                projectile.update()

            for enemy in enemies:
                enemy.update()
            
            for item in items:
                item.update()
            
            mousePos = pygame.mouse.get_pos()
            mousePosW = (mousePos[0] - Player.renderRect.centerx + Player.rect.centerx, mousePos[1] - Player.renderRect.centery + Player.rect.centery)
            
            """if pygame.mouse.get_pressed(3)[0]:
                print(mousePosW)"""
            


            if generatingMap:
                if pygame.mouse.get_pressed(3)[0]:
                    tile = (math.floor(mousePosW[0]/25),math.floor(mousePosW[1]/25))
                    emptySpot = True
                    for wall in walls:
                        if wall.rect.topleft == (tile[0]*25,tile[1]*25):
                            emptySpot = False
                            break
                    if emptySpot == True:
                        tile = Wall((tile[0]*25,tile[1]*25), WallSave.blockImages[blockImageIndex], (25,25), blockImageIndex)
                        walls.append(tile)

                if pygame.mouse.get_pressed(3)[2]:
                    # 1) convert mousePosW into tile space
                    tilePos = (math.floor(mousePosW[0]/25),math.floor(mousePosW[1]/25))
                    # 2) find if there is a tile at selected position
                    for wall in walls:
                        if wall.rect.topleft == (tilePos[0]*25,tilePos[1]*25):
                            # 3) if there is remove it
                            walls.remove(wall)
                            break

                if pygame.mouse.get_pressed(3)[1] or pygame.key.get_pressed()[pygame.K_c] and editCooldown == 0:
                    blockImageIndex += 1
                    if blockImageIndex >= len(WallSave.blockImages):
                        blockImageIndex = 0
                    print(blockImageIndex)
                    editCooldown = 10

                if editCooldown > 0:
                    editCooldown -= 1

                if pygame.key.get_pressed()[pygame.K_TAB]:
                    saveMap()
                    generatingMap = False

            # render
            for wall in walls:
                wall.render()

            """for decor in foreground:
                decor.render()

            for decor in midground:
                decor.render()"""

            for item in items:
                item.render()

            for projectile in projectiles:
                projectile.render()
            
            for enemy in enemies:
                enemy.render()

                
            for gem in gems:
                gem.render()

            poisonPortal.render()
                
            #if Player.portalPlaced:
            if Save.boss_defeated[0] == False:
                if ufoPortal.update() == "boss_fight":
                    return "boss_fight"
                ufoPortal.render()

            Player.render()

            if Player.health <= 0:
                pygame.event.post(pygame.event.Event(Event_system.On_Death))
                return "level1"

            
            
            # Draw Health Bar
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(170,1,200,30))
            pygame.draw.rect(screen, (255,0,0), pygame.Rect(170,1,Player.health / Player.maxHealth * 200,30))
            hpText = uiFont.render(f'{Player.health:0.2f} / 100', True, (255, 255, 255))
            screen.blit(hpText, (250 - hpText.get_width() / 2,7))
            # Draw Stamina Bar
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(372,1,200,30))
            pygame.draw.rect(screen, (0,0,255), pygame.Rect(372,1,Player.stamina / Player.maxStamina * 200,30))
            staminaText = uiFont.render(f'{Player.stamina} / {Player.maxStamina}', True, (255, 255, 255))
            screen.blit(staminaText, (465 - staminaText.get_width() / 2,7))

            #Draw LaserGun Cooldown Bar
            if isinstance(Player.weapon, LaserGun) and Player.coolDownBar > 0:
                pygame.draw.rect(screen, (0,0,0), pygame.Rect(271,32,200,30))
                if Player.onCoolDown:
                    pygame.draw.rect(screen, (200,10,10), pygame.Rect(271,32,Player.coolDownBar / Player.maxCoolDownBar * 200,30))
                else:
                    pygame.draw.rect(screen, (10,200,10), pygame.Rect(271,32,Player.coolDownBar / Player.maxCoolDownBar * 200,30))
                laserText = uiFont.render(f'{Player.coolDownBar:0.2f} / {Player.maxCoolDownBar}', True, (255, 255, 255))
                screen.blit(laserText, (370 - laserText.get_width() / 2,37))

            weaponText = uiFont.render(Player.weapon.name, True, (255, 255, 255))
            levelText = uiFont.render(str(level), True, (255,255,255))
            gemText = uiFont.render("Alien_Gems:"+str(Save.gems[0]), True, (255,255,255))
            mapText = levelFont.render("Alien Outpost", True, (255, 255, 255))
            screen.blit(weaponText, (10, 10))
            #screen.blit(levelText, (720, 6))
            screen.blit(gemText, (0, 40))
            if titleTimer >= 0:
                mapText.set_alpha(titleInvis/45 * 255)
                screen.blit(mapText,(260,230))
                if titleTimer < 45:
                    titleInvis -= 1
                titleTimer -= 1
                

            portalText1 = uiFont.render("Gems Needed "+ str(Save.gems[0]) + "/5.", False, (0, 255, 0))
            portalText2 = uiFont.render("Press 'F' To Summon Portal.", False, (0, 255, 0))
            adjustedRect1 = portalText1.get_rect().move(-604, 777).move(-Player.rect[0] + Player.renderRect[0], -Player.rect[1] + Player.renderRect[1])
            adjustedRect2 = portalText2.get_rect().move(-630, 805).move(-Player.rect[0] + Player.renderRect[0], -Player.rect[1] + Player.renderRect[1])
            if (Save.portal_activated[0] == False and Save.boss_defeated[0] == False and ufoPortal.text):
                screen.blit(portalText1, (adjustedRect1.left, adjustedRect1.top))
                if (Save.gems[0] >= 5):
                    screen.blit(portalText2, (adjustedRect2.left, adjustedRect2.top))
        
                        
            #portalText2 = uiFont.render("The Portal Has Been ", False, (0, 255, 0))

            if generatingMap:
                screen.blit(pygame.transform.scale(WallSave.blockImages[blockImageIndex], (25,25)), (220,220))

            # print('TODO: Gameplay')

            #print(mousePos)
            pygame.display.flip()

            if pygame.mouse.get_pressed(3)[0]:
                print(mousePosW)

if __name__ == "__main__":
    level1()