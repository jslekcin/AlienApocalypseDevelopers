import sys, pygame, math, random
from pygame.constants import K_2

from event_system import Event_system


def level1():
    loadFile = True

    pygame.init()
    pygame.font.init()
    pygame.mixer.init()

    #from main_menu import mainMenuLoop

    uiFont = pygame.font.Font(None, 32)

    size = width, height = 500, 500 # TODO: Decide on final window size
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
        rect = image.get_rect()
        # Creates a static rect to display in the center of the screen
        renderRect = image.get_rect()
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
        stamina = maxStamina
        sprintCooldown = False
        maxWalkSpeed = 6
        maxRunSpeed = 12
        # Stats
        maxHealth = 100
        isPoisoned = False
        health = maxHealth
        portalPlaced = False
        poisonTimer = fps * 2
        # Equipment
        weapon = None
        alien_gems = 5
        attackCooldown = 0
        

        def update():
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
            if pygame.key.get_pressed()[pygame.K_1]:
                Player.weapon = Bat()
            elif pygame.key.get_pressed()[pygame.K_2]:
                Player.weapon = Gun()
            elif pygame.key.get_pressed()[pygame.K_3]:
                Player.weapon = Sword()

            # Attack if player clicks
            if Player.attackCooldown > 0:
                Player.attackCooldown -= 1
            elif pygame.mouse.get_pressed(3)[0]:
                Player.weapon.attack()

            if Player.isPoisoned == True:
                print(Player.poisonTimer, Player.isPoisoned)
                Player.poisonTimer -= 1
                Player.health -= 0.05
                #print(self.poisonTimer)
                if Player.poisonTimer <= 0:
                    Player.isPoisoned = False
                

            if pygame.key.get_pressed()[pygame.K_p] and Player.alien_gems >= 5 and Player.portalPlaced == False:
                Player.portalPlaced = True
                print("portal placed")
                Player.alien_gems -= 5

            Player.renderRect.center = (width/2 - Player.xSpeed // 1, height/2 - Player.ySpeed // 1)

        def applyPoison():
            Player.poisonTimer = fps * 2

        def render():
            if Player.isPoisoned == False:
                screen.blit(Player.image, Player.renderRect)
            elif Player.isPoisoned:
                screen.blit(Player.poisonImage, Player.renderRect)
            Player.weapon.render()

    class Portal:
        def __init__(self):
            self.image = pygame.image.load("Images/BossFightPortal.png")
            self.image = pygame.transform.scale(self.image, (100,75))
            self.rect = self.image.get_rect()
            self.rect.bottom = Player.rect.bottom
            self.rect[0] = Player.rect[0] - 150

        def update(self):
            if Player.portalPlaced == False:
                self.rect.bottom = Player.rect.bottom
                self.rect[0] = Player.rect[0] - 150
            elif Player.portalPlaced == True:
                if self.rect.colliderect(Player.rect):
                    print("collided")
                    import boss_fight

        def render(self):
            adjustedRect = self.rect.move(-Player.rect[0] + Player.renderRect[0], -Player.rect[1] + Player.renderRect[1])
            screen.blit(self.image, adjustedRect)


    class Weapon:
        def __init__(self):
            self.name = 'None'

        def attack(self):
            print("Attacking with weapon")

        def render(self):
            pass
    class Sword(Weapon):
        def __init__(self):
            self.name = 'Sword'
            self.damage = 8
            self.attackSpeed = .3
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
            self.damage = 10
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
            
        def update(self):
            self.rect = self.rect.move(self.xSpeed, self.ySpeed)
            for enemy in enemies:
                if self.rect.colliderect(enemy.rect):
                    enemy.health -= 5
                    projectiles.remove(self)
                    return
        def render(self):
            # Modifys the position based on the centered player position
            adjustedRect = self.rect.move(-Player.rect[0] + Player.renderRect[0], -Player.rect[1] + Player.renderRect[1])
            # Renders wall using modified rect
            screen.blit(self.image, adjustedRect)


    class Bat(Weapon):
        def __init__(self):
            self.name = 'Bat'
            self.damage = 10
            self.range = 32 #irection we are facing and create a rect in that direction
            self.attackSpeed = .5
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

    Player.weapon = Bat()
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
                number = random.randint(1,10)
                if number == 1:
                    gems.append(Gem(self.rect.x,self.rect.bottom))

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
                number = random.randint(1,10)
                if number == 1:
                    gems.append(Gem(self.rect.x,self.rect.bottom))

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
                Player.health -= self.damage
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
            self.health = 7
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
                number = random.randint(1,10)
                if number == 1:
                    gems.append(Gem(self.rect.x,self.rect.bottom))

            if move5 == True:
                self.rect = self.rect.move(0,5)
            elif move1 == True:
                self.rect = self.rect.move(0,1)
            
        def render(self): # Show the enemy and visual effects
            adjustedRect = self.rect.move(-Player.rect[0] + Player.renderRect[0], -Player.rect[1] + Player.renderRect[1])
            screen.blit(self.image, adjustedRect)
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
        def update(self):
            # Check if it hits anything
            hit = False
            for wall in walls:
                if self.rect.colliderect(wall.rect):
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
                print("Player hit")
                if hit == False:
                    Player.health -= 4
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
            self.health = 10
            self.cooldown = 0

            self.invisiblity = 0
        def update(self): # Change the enemies variables (like position)
            if self.cooldown == 0:
                distToPlayer = ((Player.rect.x - self.rect.x)**2 + (Player.rect.y - self.rect.y)**2)**.5
                if distToPlayer < 50:
                    # Attack player
                    self.cooldown = 15 * fps
                    Player.health -= self.damage
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

    class FlyingAilenEnemy:
        def __init__(self,worldPos,image,size):
            self.rect = pygame.Rect(worldPos,size)
            self.rect.center = (Player.rect.centerx+200,Player.rect.centery-200)
            self.size = size
            self.image = pygame.transform.scale(image, self.size)
            self.damage = 5
            self.speed = 2
            self.health = 10
            self.maxCooldown = 75
            self.cooldown = self.maxCooldown
            self.onCooldown = True
            self.topright = (Player.rect.centerx+200,Player.rect.centery-200)
            self.topleft = (Player.rect.centerx-200,Player.rect.centery-200)
            self.xpos = 200
            self.rect.center = self.topleft
            self.onRight = False
            self.moving = False

            self.projectileSpeed = 10
        def update(self):
            self.topright = (Player.rect.centerx+200,Player.rect.centery-200)
            self.topleft = (Player.rect.centerx-200,Player.rect.centery-200)
            self.pos = (Player.rect.centerx+self.xpos,Player.rect.centery-200)
            
            #Attacking
            
            if self.onCooldown == False:
                print("attack")

                #fire projectile
                dx = Player.rect.centerx - self.rect.x
                dy = Player.rect.centery - self.rect.y
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
                if self.rect.centerx == (Player.rect.centerx-200):
                    self.onRight = False
                
                elif self.rect.centerx == (Player.rect.centerx+200):
                    self.onRight = True

                

                
                    
                #reset cooldown
                self.onCooldown = True
                self.cooldown = self.maxCooldown
            else:
                self.rect.center = self.pos
                self.cooldown -= 1
            if self.cooldown <= 0:
                if self.moving:
                    if self.onRight:
                        self.xpos -= 4
                        self.pos = (Player.rect.centerx+self.xpos,Player.rect.centery-200)
                        if self.rect.centerx == (Player.rect.centerx-200):
                            self.moving = False
                            self.onRight = False
                    elif self.onRight == False:
                        self.xpos += 4
                        self.pos = (Player.rect.centerx+self.xpos,Player.rect.centery-200)
                        if self.rect.centerx == (Player.rect.centerx+200):
                            self.moving = False
                            self.onRight = True

                else:
                    self.onCooldown = False
                
                

                #move closer to the player
            

                
            """if self.onCooldown == False:
                print("Attacked")
                Player.health -= self.damage
                self.cooldown = fps"""
            

            if self.health <= 0:
                enemies.remove(self)
                number = random.randint(1,10)
                if number == 1:
                    gems.append(Gem(self.rect.x,self.rect.bottom))
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

    class FlyingEnemyProjectile:
        def __init__(self, xSpeed, ySpeed,center):
            self.image = pygame.Surface((30,30))
            self.image.fill((0,255,0))
            self.rect = self.image.get_rect()
            self.xSpeed = xSpeed
            self.ySpeed = ySpeed
            self.rect.center = center
        def update(self):
            self.rect = self.rect.move(self.xSpeed, self.ySpeed)
            if self.rect.colliderect(Player.rect):
                Player.health -= 5
                projectiles.remove(self)
        def render(self):
            # Modifys the position based on the centered player position
            adjustedRect = self.rect.move(-Player.rect[0] + Player.renderRect[0], -Player.rect[1] + Player.renderRect[1])
            # Renders wall using modified rect
            screen.blit(self.image, adjustedRect)

    class Gem:
        def __init__(self,x,bottom):
            self.image = pygame.Surface((30,30))
            self.image.fill((255,0,0))
            self.rect = self.image.get_rect()
            self.rect.x,self.rect.bottom = x,bottom
            self.collected = False
        def update(self):
            if self.rect.colliderect(Player.rect):
                print("gem collected")
                Player.alien_gems += 1
                gems.remove(self)
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

    '''
    for i in range(int(2700/5)):
        h = 700
        page = Wall((5*i,h), pygame.image.load('Images/Ground.png'), (5,h))
        walls.append(page)
    '''

    def saveMap():
        global walls
        print('saving')
        '''
        book = []
        walls2 = []
        for page in walls:
            if book == []:
                book.append(page)
            else:
                h0 = book[0].rect.h
                h  = page.rect.h
                y0 = book[0].rect.y
                y  = page.rect.y
                if h0 == h and y0 == y:
                    book.append(page)
                else:
                    combinedPages = Wall(book[0].rect.topleft, pygame.image.load('Images/Ground.png'), (pageSize*len(book),h0))
                    walls2.append(combinedPages)
                    book = []
                    book.append(page)
                    
        combinedPages = Wall(book[0].rect.topleft, pygame.image.load('Images/Ground.png'), (pageSize*len(book),h0))
        walls2.append(combinedPages)
        
        walls = walls2
        '''
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
    portal = Portal()
    enemies = [ReaperEnemy((367, 805), pygame.image.load('Images\Reaper.png'), (64,100)),PoisonShooterEnemy((-819, 854), pygame.image.load('Images\Posion Shooter Design.PNG'), (64,100)),FlyingAilenEnemy((-1126, 818),pygame.image.load('Images\Ailen.png'), (100,100))]
    projectiles = []
    foreground = [Wall((200,-100), pygame.image.load('Images\Bush.png'), (100,100), -1), Wall((200,0), pygame.image.load('Images\Bird.png'), (100,100), -1), Wall((200,-100), pygame.image.load('Images\Tree.png'), (100,100), -1)]
    midground = [Wall((200,-100), pygame.image.load('Images\Bush.png'), (100,100), -1), Wall((200,0), pygame.image.load('Images\Bird.png'), (100,100), -1), Wall((200,-100), pygame.image.load('Images\Tree.png'), (100,100), -1)]

    generatingMap = not loadFile
    editPageNum = len(walls)-1
    editCooldown = 0

    tileSize = 25
    blockImages = [pygame.image.load('Images\Ground.png'), pygame.Surface((25,25)), pygame.Surface((25,25)), pygame.Surface((25,25)), pygame.Surface((25,25)), pygame.Surface((25,25)), pygame.image.load('Images\stone.PNG')]
    blockImages[1].fill((255,255,255))
    blockImages[2].fill((255,0,0))
    blockImages[3].fill((0,255,0))
    blockImages[4].fill((0,0,255))  
    blockImages[5].fill((0,0,0))
    print(blockImages[1])
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
            wall = Wall((int(line[0]),int(line[1])), blockImages[int(line[4])], (int(line[2]),int(line[3])), int(line[4]))
            walls.append(wall)

    def enemyRespawn(enemies):
        enemies = [ReaperEnemy((367, 805), pygame.image.load('Images\Reaper.png'), (64,100)),PoisonShooterEnemy((-819, 854), pygame.image.load('Images\Posion Shooter Design.PNG'), (64,100))]
        return enemies

    doubleHealth = 10
    level = 1

    while 1:
        # The Great Clock #3
        deltaTime = clock.tick(fps)


        # Inputs Processing Code
        for event in pygame.event.get(pygame.QUIT):
            pygame.quit()
            sys.exit
            break

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
                if pygame.key.get_pressed()[pygame.K_h]:
                    Player.health = Player.maxHealth
                    
            #doubleHealth = 10
            if len(enemies) <= 0:
                level += 1
                enemies = enemyRespawn(enemies)
                #enemies = [ReaperEnemy((367, 805), pygame.image.load('Images\Reaper.png'), (64,100)),PoisonShooterEnemy((-819, 854), pygame.image.load('Images\Posion Shooter Design.PNG'), (64,100))]
                doubleHealth = doubleHealth * 2
                #print("Level:", level)
                """for enemy in enemies:
                    enemy.health = doubleHealth"""

            #draw player renderrect
            pygame.draw.rect(screen,(0,255,0),Player.renderRect)
            # update
            Player.update()


            portal.update()

            for gem in gems:
                gem.update()

            for wall in walls:
                wall.update()

            for projectile in projectiles:
                projectile.update()

            for enemy in enemies:
                enemy.update()
            
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
                        tile = Wall((tile[0]*25,tile[1]*25), blockImages[blockImageIndex], (25,25), blockImageIndex)
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
                    if blockImageIndex >= len(blockImages):
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

            for decor in foreground:
                decor.render()

            for decor in midground:
                decor.render()

            for projectile in projectiles:
                projectile.render()
            
            for enemy in enemies:
                enemy.render()

                
            for gem in gems:
                gem.render()

            if Player.portalPlaced:
                portal.render()

            Player.render()

            if Player.health <= 0:
                pygame.event.post(pygame.event.Event(Event_system.On_Death))
                return "level1"
            
            # Draw Health Bar
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(150,5,200,30))
            pygame.draw.rect(screen, (255,0,0), pygame.Rect(150,5,Player.health / Player.maxHealth * 200,30))
            hpText = uiFont.render(f'{Player.health:0.2f} / 100', True, (255, 255, 255))
            screen.blit(hpText, (250 - hpText.get_width() / 2,10))
            # Draw Stamina Bar
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(150,35,200,30))
            pygame.draw.rect(screen, (0,0,255), pygame.Rect(150,35,Player.stamina / Player.maxStamina * 200,30))
            staminaText = uiFont.render(f'{Player.stamina} / {Player.maxStamina}', True, (255, 255, 255))
            screen.blit(staminaText, (250 - staminaText.get_width() / 2,40))

            
            weaponText = uiFont.render(Player.weapon.name, True, (255, 255, 255))
            levelText = uiFont.render(str(level), True, (255,255,255))
            gemText = uiFont.render("Alien_Gems:"+str(Player.alien_gems), True, (255,255,255))
            screen.blit(weaponText, (10, 10))
            screen.blit(levelText, (400, 10))
            screen.blit(gemText, (0, 40))

            if generatingMap:
                screen.blit(pygame.transform.scale(blockImages[blockImageIndex], (25,25)), (220,220))

            # print('TODO: Gameplay')

            #print(mousePos)
            pygame.display.flip()

if __name__ == "__main__":
    level1()
