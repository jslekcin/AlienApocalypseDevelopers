loadFile = True

import sys, pygame, math, random


from pygame.constants import K_2
#from sympy import false

pygame.init()
pygame.font.init()
pygame.mixer.init()


uiFont = pygame.font.Font(None, 32)

size = width, height = 500, 500 # TODO: Decide on final window size
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
    # Stats
    maxHealth = 100
    isPoisned = False
    health = maxHealth
    # Equipment
    weapon = None
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

            # Attack if player clicks
        if Player.attackCooldown > 0:
            Player.attackCooldown -= 1
        elif pygame.mouse.get_pressed(3)[0]:
            Player.weapon.attack()

        Player.renderRect.center = (width/2 - Player.xSpeed // 1, height/2 - Player.ySpeed // 1)

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
        self.damage = 10
        self.attackSpeed = 1
        self.projectileSpeed = 15
    def attack(self):
        #gunshot sound
        pygame.mixer.music.load('sounds\gunshot.mp3')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play()

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

class LaserGun(Weapon):
    def __init__(self):
        self.name = 'LaserGatlingGun'
        self.damage = 10
        self.attackSpeed = 0.1
        self.projectileSpeed = 15
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
        pygame.draw.line(screen, (0,255,0), Player.renderRect.center, pygame.mouse.get_pos())

class LaserBullet:
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
            if attackBox.colliderect(enemy.rect):12
                enemy.health -= self.damage
                print("Bat has hit")

        Player.attackCooldown = self.attackSpeed * fps

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

def render(self):
        # Modifys the position based on the centered player position
        adjustedRect = self.rect.move(-Player.rect[0] + Player.renderRect[0], -Player.rect[1] + Player.renderRect[1])
        healthRect = pygame.Rect(adjustedRect.x, adjustedRect.y - 10, self.health / self.maxHealth * adjustedRect.w, 10)
        # Renders wall using modified rect
        screen.blit(self.image, adjustedRect)
        pygame.draw.rect(screen, (0,255,0), healthRect)


class UFO_Boss:
    def __init__(self,worldPos,image,size):
        self.rect = pygame.Rect(worldPos,size)
        self.speed = 3
        self.size = size
        self.image = pygame.transform.scale(image, self.size)
        self.health = 50
        self.damage = 5

    def render(self):
        adjustedRect = self.rect.move(-Player.rect[0] + Player.renderRect[0], -Player.rect[1] + Player.renderRect[1])
        screen.blit(self.image, adjustedRect)

# worldPos, image, sized )
enemies = []
projectiles = []
foreground = [Wall((200,-100), pygame.image.load('Images\Bush.png'), (100,100), -1), Wall((200,0), pygame.image.load('Images\Bird.png'), (100,100), -1), Wall((200,-100), pygame.image.load('Images\Tree.png'), (100,100), -1)]
midground = [Wall((200,-100), pygame.image.load('Images\Bush.png'), (100,100), -1), Wall((200,0), pygame.image.load('Images\Bird.png'), (100,100), -1), Wall((200,-100), pygame.image.load('Images\Tree.png'), (100,100), -1)]


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

clock = pygame.time.Clock()

while 1:
    clock.tick(fps) 
    
    for event in pygame.event.get(pygame.QUIT):
        pygame.quit()
        sys.exit
        break

    screen.blit(background, (0,0))

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

    for decor in foreground:
        decor.render()

    for decor in midground:
        decor.render()

    for projectile in projectiles:
        projectile.render()
        
    for enemy in enemies:
        enemy.render()

    Player.render()

    # Draw Health Bar
    pygame.draw.rect(screen, (0,0,0), pygame.Rect(150,5,200,30))
    pygame.draw.rect(screen, (255,0,0), pygame.Rect(150,5,Player.health / Player.maxHealth * 200,30))
    hpText = uiFont.render(f'{Player.health} / 100', True, (255, 255, 255))
    screen.blit(hpText, (250 - hpText.get_width() / 2,10))
    # Draw Stamina Bar
    pygame.draw.rect(screen, (0,0,0), pygame.Rect(150,35,200,30))
    pygame.draw.rect(screen, (0,0,255), pygame.Rect(150,35,Player.stamina / Player.maxStamina * 200,30))
    staminaText = uiFont.render(f'{Player.stamina} / {Player.maxStamina}', True, (255, 255, 255))
    screen.blit(staminaText, (250 - staminaText.get_width() / 2,40))

        
    weaponText = uiFont.render(Player.weapon.name, True, (255, 255, 255))
    #levelText = uiFont.render(str(level), True, (255,255,255))
    screen.blit(weaponText, (10, 10))
    #screen.blit(levelText, (400, 10))

    # print('TODO: Gameplay')
    pygame.display.flip()
    
        

   



    



