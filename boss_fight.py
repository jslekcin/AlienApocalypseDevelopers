
import sys, pygame, math, random, time
from pygame.constants import K_2

from event_system import Event_system
from player_save import Save
from wall_save import WallSave
#from sympy import false

def boss_fight_loop():
    loadFile = True

    pygame.init()
    pygame.font.init()
    pygame.mixer.init()

    uiFont = pygame.font.Font(None, 32)
    levelFont = pygame.font.Font(None, 64)
    borderFont = pygame.font.Font(None, 66)

    size = width, height=750, 750 # TODO: Decide on final window size
    screen = pygame.display.set_mode(size) 

    fps = 60

    black = (0,0,0)
    background = pygame.image.load('Images/red_sky.png')
    background = pygame.transform.scale(background, size)
    gameState = 1


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
        isPoisned = False
        health = Save.health
        regenTimer = fps * 10
        prev_health = health
        # Equipment
        weapon = None
        attackCooldown = 0

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

            pygame.draw.rect(screen, (255,0,0), belowRect.move(-Player.rect[0] + Player.renderRect[0], -Player.rect[1] + Player.renderRect[1]-5))
            pygame.draw.rect(screen, (255,0,0), leftRect.move(-Player.rect[0] + Player.renderRect[0], -Player.rect[1] + Player.renderRect[1]-5))
            pygame.draw.rect(screen, (255,0,0), rightRect.move(-Player.rect[0] + Player.renderRect[0], -Player.rect[1] + Player.renderRect[1]-5))
            pygame.draw.rect(screen, (255,0,0), topRect.move(-Player.rect[0] + Player.renderRect[0], -Player.rect[1] + Player.renderRect[1]-5))

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

            Player.renderRect.center = (width/2 - Player.xSpeed // 1, height/2 - Player.ySpeed // 1)

            Player.prev_health = Player.health

        def applyDamage(damage):
                Player.health -= damage

        def render():
            if Player.isPoisned == False:
                screen.blit(Player.image, Player.renderRect)
            elif Player.isPoisned:
                screen.blit(Player.poisonImage, Player.renderRect)
            Player.weapon.render()

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
            hitBox = pygame.Rect(0, 0, 45, 64)
            mousePos = pygame.mouse.get_pos()
            if pygame.mouse.get_pos()[0] - Player.renderRect.centerx < 0:
                hitBox.topright = Player.rect.topleft
            else:
                hitBox.topleft = Player.rect.topright
                #do damage to enemies left of the player
            for enemy in enemies:
                if hitBox.colliderect(enemy.rect):
                    enemy.health -= self.damage
                    print("hit")

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
            pygame.mixer.music.load('sounds\gunshot.mp3')
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play()
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
                
            pygame.draw.line(screen, (0,255,0), Player.renderRect.center, pygame.mouse.get_pos())

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
            

            #self.rotated_image_right = pygame.transform.rotate(self.image_right, int(image_angle))
            #self.rect_right = self.image_right.get_rect()#center=(self.rotated_image_right[0], self.rotated_image_right[1])\
            #self.rect_right.center = [self.rotated_image_right[0], self.rotated_image_right[1]]

            #self.rotated_image_right = pygame.transform.rotate(self.image_right, self.angle)
            #self.rotated_rect_right = self.rotated_image_right.get_rect(center = self.image_right.get_rect(center = (Player.renderRect.centerx,Player.renderRect.centery)).center)

            self.damage = 1
            self.attackSpeed = 0.2
            self.projectileSpeed = 20
        def attack(self):

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


    class LaserBullet:
        def __init__(self, xSpeed, ySpeed):
            self.xSpeed = xSpeed
            self.ySpeed = ySpeed
            self.image = pygame.Surface((10,10))
            self.image.fill((200,0,0))#70
            self.rect = self.image.get_rect()
            self.rect.center = Player.rect.center
            
            
        def update(self):
            self.rect = self.rect.move(self.xSpeed, self.ySpeed)
            adjustedRect = self.rect.move(-Player.rect[0] + Player.renderRect[0], -Player.rect[1] + Player.renderRect[1])

            boss_adjustedRect = boss.rect.move(-Player.rect[0] + Player.renderRect[0] + 65, -Player.rect[1] + Player.renderRect[1] + 30)

            collide = pygame.Rect.colliderect(adjustedRect,boss_adjustedRect)
            if collide:
                boss.health -= 1
                projectiles.remove(self)
                return
            range_rect = pygame.Rect((0,0),(500,500))
            range_rect.center = Player.renderRect.center
            #pygame.draw.rect(screen,(255,255,255),range_rect)

            bullet_range = pygame.Rect.colliderect(adjustedRect,range_rect)

            if bullet_range:
                pass
            else:
                projectiles.remove(self)
                

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
            # Figure out which class Bat(Weapon):
            attackBox = pygame.Rect(0, 0, self.range, 64)
            if pygame.mouse.get_pos()[0] - Player.renderRect.centerx < 0:
                attackBox.topright = Player.rect.topleft
            else:
                attackBox.topleft = Player.rect.topright

            # Debug show attack box
            adjustedRect = attackBox.move(-Player.rect[0] + Player.renderRect[0], -Player.rect[1] + Player.renderRect[1])
            pygame.draw.rect(screen, (255,255,255), adjustedRect)

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
            


    class UFO_Boss:
        def __init__(self,worldPos,image,size):
            #self.rect = pygame.Rect(worldPos,size)
            
            self.worldPos = worldPos
            self.speed = 7
            self.size = size
            self.image = pygame.transform.scale(image, self.size)
            self.rect = self.image.get_rect()
            self.maxHealth = 50
            self.health = self.maxHealth
            self.damage = 5
            #self.position = [Player.renderRect.center[0]-160, Player.renderRect.center[1]-215]
            #self.rect.center = self.position
            self.cooldown = -60
            self.randcooldown = 100
            self.laser_cooldown = -30
            self.laser_randcooldown = 50
            self.projectiles = []
            #self.speedtime = -60
            self.rect.centerx = Player.rect.centerx
            self.facingRight = True
            
            
            """if self.speed == 0:
                self.speed = random.randint(-5, 5)

            if self.speedtime > 85:
                self.speed = random.randint(-5, 2)
                self.speedtime = -60
            else:
                self.speedtime =+ 1"""

        def render(self):
            adjustedRect = self.rect.move(-Player.rect[0] + Player.renderRect[0], -Player.rect[1] + Player.renderRect[1])
            screen.blit(self.image, adjustedRect)

        def move(self):
            #self.rect = self.image.get_rect()
            
            #speed = random.randint(-5, 5)
            

            """self.position[0] += self.speed
            
            player_center = [-Player.rect[0] + Player.renderRect[0], -Player.rect[1] + Player.renderRect[1]]

            if self.position[0] >= player_center[0]+400:
            
                self.position[0] = player_center[0]+400

                self.speed = -self.speed

            if self.position[0] <=  player_center[0]-400:

                self.position[0] = player_center[0]-400

                self.speed = -self.speed"""
            
            playerRightRect = pygame.Rect(Player.rect.x+100,Player.rect.centery-200,75,75)
            playerRightRect.centerx, playerRightRect.centery = Player.renderRect.centerx + 400, Player.renderRect.centery - 170
            

            playerLeftRect = pygame.Rect(Player.rect.x+100,Player.rect.centery-200,75,75)
            playerLeftRect.centerx, playerLeftRect.centery = Player.renderRect.centerx - 400, Player.renderRect.centery - 170
                
            
            self.rect.x += self.speed

            adjustedRect = self.rect.move(-Player.rect[0] + Player.renderRect[0] + 65, -Player.rect[1] + Player.renderRect[1] + 30)
            player_adjustedRect = Player.rect.move(-Player.rect[0] + Player.renderRect[0], -Player.rect[1] + Player.renderRect[1])

            
            #pygame.draw.rect(screen,(0,255,0),adjustedRect)
            #pygame.draw.rect(screen,(5,0,250),self.rect)
            #pygame.draw.rect(screen,(0,255,0),Player.renderRect)
            #pygame.draw.rect(screen,(255,255,255),Player.rect)
            #print(Player.rect.x,Player.rect.y)

            #green = player render rect, blue = boss rect, red = boss adjusted rect, black = player left and right rect, white = player.rect


            if adjustedRect.colliderect(playerRightRect) and self.facingRight:
                self.speed = -1 * (abs(self.speed))
                self.facingRight = False
                
                #print("right rect collided")
            
            if adjustedRect.colliderect(playerLeftRect) and self.facingRight == False:
                self.speed = abs(self.speed)
                self.facingRight = True
                
                #print("left rect collided")

            """if adjustedRect.x > Player.renderRect.centerx + 50:
                self.speed = -abs(self.speed)
            
            if adjustedRect.x < Player.renderRect.centerx - 50:
                self.speed = abs(self.speed)"""

        def update(self):
            self.shoot()
            self.move()
            #self.rect.centerx = Player.rect.centerx
            self.rect.centery = Player.rect.centery - 200
            self.rect.w = 205
            self.rect.h = 120
            #pygame.draw.rect(screen,(255,255,255),self.rect)
            #print(self.rect)

            if self.health <= 0:
                enemies.remove(self)
                Save.boss_defeated[0] = True
                

        def shoot(self):
            if self.cooldown >= self.randcooldown:
                projectiles.append(UFO_bomb((self.rect.x+170, self.rect.y+45), 20, 3, 90, "Images/bomb.png"))
                self.cooldown = 0
                self.randcooldown = random.randint(80,105)
            else:
                self.cooldown += 1

            if self.laser_cooldown >= self.laser_randcooldown:
                number = random.randint(1,3)
                projectiles.append(UFO_laser((self.rect.x+165, self.rect.y+140), 5, 4, 90, "Images/beam.png"))
                self.laser_cooldown = 0
                self.laser_randcooldown = random.randint(40,55)
                    
            else:
                self.laser_cooldown += 1

        
    class UFO_bomb:
        def __init__(self, location, damage, speed, angle, image):
            self.image = pygame.image.load(image)
            self.rect = self.image.get_rect()
            self.rect.center = location
            self.explosion_timer = 50
            self.dx = speed * math.cos(angle)
            self.dy = speed * math.sin(angle)
            self.damage = damage
            self.exploded = False
        
        def update(self):
            if self.rect.colliderect(Player.rect) and not self.exploded:
                Player.applyDamage(self.damage)
                projectiles.remove(self)

            else:
                for wall in walls:
                    if self.rect.colliderect(wall.rect) and not self.exploded:
                        self.exploded = True
                        self.image = pygame.image.load("Images/explosion.png")
                        self.image = pygame.transform.scale(self.image, (100,100))
                        self.rect = self.rect.move(0,25)
                        break

            if self.exploded:
                if self.explosion_timer > 0:
                    self.explosion_timer -= 1
                else: 
                    projectiles.remove(self)

            #self.dy += .05
            if not self.exploded:
                self.rect = self.rect.move(self.dx,self.dy)

        def render(self):
            adjustedRect = self.rect.move(-Player.rect[0] + Player.renderRect[0], -Player.rect[1] + Player.renderRect[1])
            screen.blit(self.image, adjustedRect)
                

    class Portal():
        def __init__(self):
            self.image = self.assignImage()
            self.rect = self.image.get_rect()
            self.rect.topleft = (-405, 842)

        def update(self):
            if self.rect.colliderect(Player.rect) and Save.boss_defeated[0]:
                print("collided")
                Save.starting_pos = (-516, 696)
                Save.health = Player.health
                Save.stamina = Player.stamina
                return "level1"
            
            pygame.draw.rect(screen, (0, 0, 0), self.rect)
                
            
        def assignImage(self):
            image = pygame.image.load("Images/BossFightPortal2.png")
            image = pygame.transform.scale(image, (115,35))
            return image

        def render(self):
            adjustedRect = self.rect.move(-Player.rect[0] + Player.renderRect[0], -Player.rect[1] + Player.renderRect[1])
            screen.blit(self.image, adjustedRect)
                #pygame.draw.rect(screen, (0, 0, 0), adjustedRect)
                    
    class UFO_laser:
        def __init__(self, location, damage, speed, angle, image):
            self.image = pygame.image.load(image)
            #self.type = type
            self.rect = self.image.get_rect()
            self.rect.center = location
            self.damage = damage
            self.dx = speed * math.cos(angle)
            self.dy = speed * math.sin(angle)
            #self.timer = 10 * fps
            #self.explosion_timer = 50
            #self.timer = 45
            #self.exploded = False
        
        def update(self):
            # Check if it hits anything
            if self.rect.colliderect(Player.rect):
                Player.applyDamage(self.damage)
                projectiles.remove(self)

            else:
                for wall in walls:
                    if self.rect.colliderect(wall.rect):
                        projectiles.remove(self)
                        break
            
            self.dy += .1
            self.rect = self.rect.move(self.dx,self.dy)

        """def explode(self):
            self.explosion_timer -= 1
            self.dx = 0
            self.dy = 0
            explosion_image = pygame.image.load("Images/explosion.png")
            explosion_image = pygame.transform.scale(explosion_image, [230, 230])
            screen.blit(explosion_image, self.rect.center)"""

        
        def render(self):
            adjustedRect = self.rect.move(-Player.rect[0] + Player.renderRect[0], -Player.rect[1] + Player.renderRect[1])
            screen.blit(self.image, adjustedRect)
            """if self.exploded == True:
                self.image = """""

    class LaserGunItem:
        def __init__(self,worldPos,image,size):
            #Laser Gun item
            self.pos = worldPos
            self.size = size
            self.rect = pygame.Rect(self.pos,self.size)
            self.image = pygame.transform.scale(image, self.size)
            #self.rect = self.image.get_rect()
            
        
        def update(self):
            #print(self.rect)
            self.rect.center = self.pos
            if self.rect.colliderect(Player.rect):
                Save.weapons["LaserGun"] = True

        def render(self):
            #adjust position based on players position
            adjustedRect = self.rect.move(-Player.rect[0] + Player.renderRect[0], -Player.rect[1] + Player.renderRect[1])
            #render image
            if Save.weapons["LaserGun"] == False:
                screen.blit(self.image, adjustedRect)


    pageSize = 10
    # Creates pagse for the player platform
    for i in range(int(70/pageSize)):
        h = 1000
        page = Wall((pageSize*i,h), pygame.image.load('Images\Ground.png'), (pageSize,h), 0)
        walls.append(page)


    def saveMap():
        global walls
        print('saving')

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
        file = open("bossMap.txt", "w")
        file.write(out)
        file.close()

    # worldPos, image, sized 
    boss = UFO_Boss((-360, 650), pygame.image.load('Images/UFO.png'), (400, 200))
    if Save.boss_defeated[0] == False:
        enemies = [boss]
    else:
        enemies = []
    projectiles = []
    portal = Portal()
    boss_projectiles = []
    item = LaserGunItem((-360, 850),pygame.image.load("Images/LaserGatlingGunv2(right).png"),(120,140))
    foreground = [Wall((200,-100), pygame.image.load('Images\Bush.png'), (100,100), -1), Wall((200,0), pygame.image.load('Images\Bird.png'), (100,100), -1), Wall((200,-100), pygame.image.load('Images\Tree.png'), (100,100), -1)]
    midground = [Wall((200,-100), pygame.image.load('Images\Bush.png'), (100,100), -1), Wall((200,0), pygame.image.load('Images\Bird.png'), (100,100), -1), Wall((200,-100), pygame.image.load('Images\Tree.png'), (100,100), -1)]

    generatingMap = not loadFile
    editPageNum = len(walls)-1
    editCooldown = 0

    tileSize = 25
    blockImageIndex = 0

    if loadFile:
        walls = []
        file = open("bossMap.txt", "r")
        fileData = file.read().split('\n')
        file.close()
        for line in fileData:
            if line == '':
                break
            line = line.split()
            wall = Wall((int(line[0]),int(line[1])), WallSave.blockImages[int(line[4])], (int(line[2]),int(line[3])), int(line[4]))
            walls.append(wall)

    clock = pygame.time.Clock()

    titleTimer = fps * 3
    titleInvis = 45

    while 1:
        clock.tick(fps) 
        
        for event in pygame.event.get(pygame.QUIT):
            pygame.quit()
            sys.exit
            break

        screen.blit(background, (0,0))


        #print(pygame.mouse.get_pos())
        
        #pygame.draw.rect(screen,(255,255,255),screen_rect)

        mousePos = pygame.mouse.get_pos()
        mousePosW = (mousePos[0] - Player.renderRect.centerx + Player.rect.centerx, mousePos[1] - Player.renderRect.centery + Player.rect.centery)

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
        

        # update
        Player.update()

        

        item.update()

        for wall in walls:
            wall.update()

        for projectile in projectiles:
            projectile.update()

        #for boss_projectile in boss_projectiles:
            #boss_projectile.update(walls,boss_projectiles)
        
        for enemy in enemies:
            enemy.update()

        # render
        for wall in walls:
            wall.render()

        """for decor in foreground:
            decor.render()
            
        for decor in midground:
            decor.render()"""

        for projectile in projectiles:
            projectile.render()

        for enemy in enemies:
            enemy.render()

        if Save.boss_defeated[0]:
            portal.render()
            if portal.update() == "level1":
                return "level1"
        
        """for projectile in boss.projectiles:
            time_left = projectile.time_decrease()     
            
            if time_left <= 0 and projectile.type == "laser":
                boss.projectiles.remove(projectile)
            if time_left <= 0 and projectile.type =="bomb":
                projectile.exploded = True
                if projectile.explosion_timer <=0:
                    boss.projectiles.remove(projectile)"""

        item.render()

        Player.render()

        if Player.health <= 0:
            pygame.event.post(pygame.event.Event(Event_system.On_Death))
            return "boss_fight"
        

        #boss.shoot()
        #boss.update()
        #boss.move()
        #boss.render()

        

        # Draw Health Bar
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(170,1,200,30))
        pygame.draw.rect(screen, (255,0,0), pygame.Rect(168,1,Player.health / Player.maxHealth * 200,30))
        hpText = uiFont.render(f'{Player.health:0.2f} / 100', True, (255, 255, 255))
        screen.blit(hpText, (250 - hpText.get_width() / 2,7))
        # Draw Stamina Bar
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(370,1,200,30))
        pygame.draw.rect(screen, (0,0,255), pygame.Rect(372,1,Player.stamina / Player.maxStamina * 200,30))
        staminaText = uiFont.render(f'{Player.stamina} / {Player.maxStamina}', True, (255, 255, 255))
        screen.blit(staminaText, (465 - staminaText.get_width() / 2,7))
        # Draw Boss Health
        if Save.boss_defeated[0] == False:
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(168,31,400,37))
            pygame.draw.rect(screen, (255,0,0), pygame.Rect(168,34,boss.health / boss.maxHealth * 405,37))
            bossHealthText = uiFont.render(f'{boss.health} / {boss.maxHealth}', True, (255, 255, 255))
            screen.blit(bossHealthText, (370 - bossHealthText.get_width() / 2,40))


            
        weaponText = uiFont.render(Player.weapon.name, True, (255, 255, 255))
        mapText = levelFont.render("UFO Guard's Domain", True, (255, 255, 255))
        borderText = levelFont.render("UFO Guard's Domain", True, (0, 0, 0))
        #levelText = uiFont.render(str(level), True, (255,255,255))
        screen.blit(weaponText, (10, 10))
        #screen.blit(levelText, (400, 10))
        if titleTimer >= 0:
            mapText.set_alpha(titleInvis/45 * 255)
            borderText.set_alpha(titleInvis/45 * 255)
            screen.blit(borderText, (243,228))
            screen.blit(borderText, (247,232))
            screen.blit(borderText, (243,232))
            screen.blit(borderText, (247,228))
            screen.blit(mapText,(245,230))
            if titleTimer < 45:
                titleInvis -= 1
            titleTimer -= 1

        # print('TODO: Gameplay')
        pygame.display.flip()

        if pygame.mouse.get_pressed(3)[0]:
            print(mousePosW)

