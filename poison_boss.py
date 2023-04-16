import sys, pygame, math, random
from pygame.constants import K_2

from event_system import Event_system
from player_save import Save
from wall_save import WallSave

def poison_boss_loop():
    loadFile = True

    pygame.init()
    pygame.font.init()
    pygame.mixer.init()

    #from main_menu import mainMenuLoop

    uiFont = pygame.font.Font(None, 32)

    size = width, height = 750, 750 # TODO: Decide on final window size
    screen = pygame.display.set_mode(size) 
    fps = 60

    black = (0,0,0)
    background = pygame.image.load('Images/purple_screen.png')
    background = pygame.transform.scale(background, size)
    gameState = 1

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
            maxWalkSpeed = 6
            maxRunSpeed = 12
            # Sprinting Variables
            maxStamina = 120
            staminaRegen = .5
            stamina = maxStamina
            sprintCooldown = False
            # Stats
            maxHealth = 100
            isPoisned = False
            health = maxHealth
            portalPlaced = False
            regenTimer = fps * 10
            prev_health = health
            isPoisoned = False
            poisonTimer = fps * 2
            poisonCounter = 0
            # Equipment
            weapon = None
            #alien_gems = 5
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
                if pygame.key.get_pressed()[pygame.K_1]:
                    #Player.weapon = Bat()
                    pass

                # Attack if player clicks
                if Player.attackCooldown > 0:
                    Player.attackCooldown -= 1
                elif pygame.mouse.get_pressed(3)[0]:
                    Player.weapon.attack()

                if Player.isPoisoned == True:
                    #print(Player.poisonTimer, Player.isPoisoned)
                    Player.poisonTimer -= 1
                    Player.health -= 0.015 * Player.poisonCounter
                    #print(self.poisonTimer)
                    if Player.poisonTimer <= 0:
                        Player.isPoisoned = False
                        Player.poisonCounter = 0

                Player.renderRect.center = (width/2 - Player.xSpeed // 1, height/2 - Player.ySpeed // 1)

                Player.prev_health = Player.health

                #pygame.draw.rect(screen, (0,0,0), Player.renderRect)

            def applyPoison():
                Player.poisonTimer = fps * 2

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
                print("Attacking with weapon")

            def render(self):
                pass

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

    class PoisonBoss:
        def __init__(self,worldPos,size):
            self.speed = 3
            self.size = size
            self.image = pygame.image.load('Images\Poison Boss Right.png')
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = 198, 1209
            #self.rect = self.image.get_rect()
            self.maxHealth = 200
            self.health = self.maxHealth
            self.damage = 5

            self.facingLeft = False

            #Phase 1
            self.timer = 10
            self.projectileSpeed = 10
            self.shootingDirection = 0

            self.approachRange = 300
            self.attackRange = 200
            self.fleeRange = 100

            self.counter = 0

            self.state = 1

            self.attackCounter = 0

            #Phase 2
            self.meleeTimer = fps * 2

            self.laserTimer = fps * 7
            
            self.dist = 0

            
        def update(self):
            self.stateProcess()
            self.stateChange()

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

        

        def stateProcess(self):
            if self.state == 1:
                self.attackP1()
                self.moveP1()
            elif self.state == 2:
                self.moveP2()
                self.attackP2()
            elif self.state == 3:
                self.attack3()
        
        def stateChange(self):
            if self.health <= self.maxHealth/2:
                self.state = 2
                self.speed = 5
            if self.laserTimer <= fps * 2:
                self.state = 3
            
            if self.laserTimer <= 0:
                self.state = 2
                self.laserTimer = fps * 7

        def attackP1(self):
            if self.timer <= 0:
                if self.attackCounter < 4:
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
                    projectiles.append(RangedPoisonProjectile(xSpeed,ySpeed,center))

                    self.attackCounter += 1
                elif self.attackCounter >= 4:
                    # Aiming
                    xdist = Player.rect.centerx - self.rect.centerx
                    ydist = Player.rect.centery - self.rect.centery
                    #angle = math.degrees(math.atan2(ydist,xdist))
                    #angle = math.radians(angle)
                    angle = 3 * math.pi/4 if math.copysign(1,xdist) < 0 else math.pi/4
                    speed = math.sqrt(abs(xdist) * 0.05) * 1.2

                    print(xdist, angle, speed)

                    projectiles.append(PoisonPuddle(self.rect.center, 5, speed, angle))

                    self.attackCounter = 0

                self.timer = 50
            self.timer -= 1

        def moveP1(self):
            # Check that enemy is on screen
            distToPlayer = abs(Player.rect.x - self.rect.x)
            if distToPlayer <= self.approachRange and distToPlayer >= self.attackRange or distToPlayer < self.fleeRange:
                if distToPlayer >= self.attackRange:
                    # Set the direction enemy is facing
                    if self.rect.x < Player.rect.x:
                        self.image = pygame.image.load('Images\Poison Boss Right.png')
                        self.facingLeft = False
                    else:
                        self.image = pygame.image.load('Images\Poison Boss Left.png')
                        self.facingLeft = True
                else:
                    # Set the direction enemy is facing
                    if self.rect.x < Player.rect.x:
                        self.image = pygame.image.load('Images\Poison Boss Right.png')
                        self.facingLeft = True
                    else:
                        self.image = pygame.image.load('Images\Poison Boss Left.png')
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
            

        def moveP2(self):
            #Set the direction
            if self.rect.x < Player.rect.x:
                self.facingLeft = False
                self.image = pygame.image.load('Images\Poison Boss Right.png')
            else:
                self.facingLeft = True
                self.image = pygame.image.load('Images\Poison Boss Left.png')

            #movement
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

        def attackP2(self):
            #melee attack
            attackRect = self.rect.copy()
            attackRect.w += 16
            attackRect.x -= 8
            attackRect.h -= 15
            attackRect.y += 15

            if self.meleeTimer <= 0 and attackRect.colliderect(Player.rect):
                    # Attack player
                    print("attack")
                    self.meleeTimer = fps * 1.5
                    Player.applyDamage(self.damage)

            self.laserTimer -= 1
            self.meleeTimer -= 1


            adjustedRect1 = attackRect.move(-Player.rect[0] + Player.renderRect[0], -Player.rect[1] + Player.renderRect[1])
            
            pygame.draw.rect(screen,(255,255,255),adjustedRect1) #attackRect

        def attack3(self):
            laserRect = self.rect.copy()

            if self.laserTimer > 15:
                self.dist = abs(Player.rect.centerx - self.rect.centerx)
                laserRect.h -= 120 - (fps * 2 - self.laserTimer)/2
                laserRect.y += 35 - (fps * 2 - self.laserTimer)/4
                laserRect.w = self.dist
            else:
                laserRect.h -= 120 - (fps * 2 - 15)/2
                laserRect.y += 35 - (fps * 2 - 15)/4
                laserRect.w = self.dist
            if self.facingLeft:
                laserRect.right = self.rect.left
            else:
                laserRect.left = self.rect.right

            adjustedRect2 = laserRect.move(-Player.rect[0] + Player.renderRect[0], -Player.rect[1] + Player.renderRect[1])

            if self.laserTimer > 15:
                pygame.draw.rect(screen,(200,50,50),adjustedRect2)
            elif self.laserTimer <= 15:
                pygame.draw.rect(screen,(0,255,0),adjustedRect2)
                if laserRect.colliderect(Player.rect):
                    Player.applyDamage(2)

            self.laserTimer -= 1


            
        def render(self):
            # Modifys the position based on the centered player position
            adjustedRect = self.rect.move(-Player.rect[0] + Player.renderRect[0], -Player.rect[1] + Player.renderRect[1])
            # Renders wall using modified rect
            screen.blit(self.image, adjustedRect)   

    class RangedPoisonProjectile:
            def __init__(self, xSpeed, ySpeed,center):
                self.image = pygame.Surface((30,30))
                self.image.fill((180,0,255))
                self.rect = self.image.get_rect()
                self.xSpeed = xSpeed
                self.ySpeed = ySpeed
                self.rect.center = center
                self.deathTimer = 120
            def update(self):
                self.rect = self.rect.move(self.xSpeed, self.ySpeed)
                if self.rect.colliderect(Player.rect):
                    Player.applyDamage(5)
                    projectiles.remove(self)
                else:
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
    class PoisonPuddle:
        # When it hits somthing it will stay for a while
        def __init__(self, location, damage, speed, angle):
            #self.image = pygame.Surface((20,20))
            #pygame.draw.circle(self.image, (23,52,200), (10,10), 10)
            self.image = pygame.image.load("Images/Posion Projectile.PNG")
            self.image = pygame.transform.scale(self.image, (50,50))
            self.rect = self.image.get_rect()
            self.rect.center = location
            self.damage = damage
            self.dx = speed * math.cos(angle)
            self.dy = -speed * math.sin(angle)
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
                self.image = pygame.transform.scale(self.image, (150,50))
                #self.rect = self.image.get_rect()
                self.timer -= 1
                if self.timer <= 0:
                    projectiles.remove(self)
            else:
                # Moving the projectile
                self.dy += 0.05
                self.rect = self.rect.move(self.dx,self.dy)

            if self.rect.colliderect(Player.rect):
                # Do damage if it does
                Player.poisonCounter += 1
                print("Player hit", Player.poisonCounter)
                if hit == False:
                    Player.applyDamage(4)
                Player.isPoisoned = True
                Player.applyPoison()
                projectiles.remove(self)
            

        def render(self):
            # Modifys the position based on the centered player position
            adjustedRect = self.rect.move(-Player.rect[0] + Player.renderRect[0], -Player.rect[1] + Player.renderRect[1])
            # Renders wall using modified rect
            screen.blit(self.image, adjustedRect)   


    # worldPos, image, sized )
    boss = PoisonBoss((322, 1242),(70,70))
    enemies = [boss]
    projectiles = []
    foreground = [Wall((200,-100), pygame.image.load('Images\Bush.png'), (100,100), -1), Wall((200,0), pygame.image.load('Images\Bird.png'), (100,100), -1), Wall((200,-100), pygame.image.load('Images\Tree.png'), (100,100), -1)]
    midground = [Wall((200,-100), pygame.image.load('Images\Bush.png'), (100,100), -1), Wall((200,0), pygame.image.load('Images\Bird.png'), (100,100), -1), Wall((200,-100), pygame.image.load('Images\Tree.png'), (100,100), -1)]


    pageSize = 10
    # Creates pagse for the player platform
    for i in range(int(70/pageSize)):
        h = 1000
        page = Wall((pageSize*i,h), pygame.image.load('Images\Ground.png'), (pageSize,h), 0)
        walls.append(page)

    map = "poisonBoss.txt"

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
        file = open(map, "w")
        file.write(out)
        file.close()



    generatingMap = not loadFile
    editPageNum = len(walls)-1
    editCooldown = 0

    tileSize = 25
    blockImagesAll = [pygame.image.load('Images\Grass.png').convert(), pygame.Surface((25,25)), pygame.Surface((25,25)), pygame.Surface((25,25)), pygame.Surface((25,25)), pygame.Surface((25,25)), pygame.image.load('Images\stone.PNG').convert(), pygame.image.load('Images/pg.png').convert(), pygame.image.load('Images/poison.png').convert(), pygame.image.load('Images/ps.png').convert(), pygame.image.load('Images/Dirt3.png').convert()]
    blockImagesAll[1].fill((255,255,255))
    blockImagesAll[2].fill((255,0,0))
    blockImagesAll[3].fill((0,255,0))
    blockImagesAll[4].fill((0,0,255))  
    blockImagesAll[5].fill((0,0,0))

    blockImages = [blockImagesAll[6], blockImagesAll[7], blockImagesAll[8], blockImagesAll[9]]

    blockIndexs = [6, 7, 8, 9]

    blockImageIndex = 0

    if loadFile:
        walls = []
        file = open(map, "r")
        fileData = file.read().split('\n')
        file.close()
        for line in fileData:
            if line == '':
                break
            line = line.split()
            wall = Wall((int(line[0]),int(line[1])), blockImagesAll[int(line[4])], (int(line[2]),int(line[3])), int(line[4]))
            walls.append(wall)

    clock = pygame.time.Clock()
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
                        tile = Wall((tile[0]*25,tile[1]*25), blockImages[blockImageIndex], (25,25), blockIndexs[blockImageIndex])
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

            # update
        Player.update()

        for wall in walls:
            wall.update()

        for projectile in projectiles:
            projectile.update()

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

        Player.render()    

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
        # Draw Boss Health
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(168,31,400,37))
        pygame.draw.rect(screen, (200,50,200), pygame.Rect(168,34,boss.health / boss.maxHealth * 405,37))
        bossHealthText = uiFont.render(f'{boss.health} / {boss.maxHealth}', True, (255, 255, 255))
        screen.blit(bossHealthText, (370 - bossHealthText.get_width() / 2,40))

            
        weaponText = uiFont.render(Player.weapon.name, True, (255, 255, 255))
        #levelText = uiFont.render(str(level), True, (255,255,255))
        screen.blit(weaponText, (10, 10))
        #screen.blit(levelText, (400, 10))

        if pygame.mouse.get_pressed(3)[0]:
                print(mousePosW)

        pygame.display.flip()
