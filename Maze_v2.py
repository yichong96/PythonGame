import pygame, os, random

# Set up window
#####################################################################
pygame.init()

win_width, win_height = 1024, 768
win_size = win_width, win_height
window = pygame.display.set_mode(win_size, pygame.RESIZABLE)

pygame.display.set_caption("MazeGame")
clock = pygame.time.Clock()
fps = 60
######################################################################

def loadImageListInDict(path):
    '''
        Create a list for every sub_dir, and load the files(only images) 
        under the sub_dir into the the list.
        Store the lists into a dictionary and return.
        Directory is needed as argument.
    '''
    listsDict = {}
    for folder in os.listdir(path):
        subPath = os.path.join(path, folder)
        if os.path.isdir(subPath):
            listsDict[folder] = []
            for image in os.listdir(subPath):
                if os.path.isfile(os.path.join(subPath,image)):
                    listsDict[folder].append(pygame.image.load(os.path.join(subPath,image)))
    return listsDict

def loadImageDict(path):
    '''
        Load all the files(only images) under the directory into a dictionary and return.
        Directory is needed as argument.
    '''
    imageDict = {}
    for image in os.listdir(path):
        subPath = os.path.join(path, image)
        if os.path.isfile(subPath):
            imageDict[os.path.splitext(image)[0]] = pygame.image.load(subPath)
    return imageDict

class Player(pygame.sprite.Sprite):
    def __init__(self, color = pygame.Color.b, width = 32, height = 32):

        super().__init__()
        # self.image = pygame.Surface((width, height))
        # self.image.fill((255,0,0))

        self.image = pygame.image.load('rat.png')
        self.rect = self.image.get_rect()
        self.hSpeed = 0
        self.vSpeed = 0
        self.speed = 5

        self.walkCount = 0
        self.isNextStage = False
    
    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def update(self, collidable = pygame.sprite.Group(), treasures = pygame.sprite.Group(),\
               portal = pygame.sprite.Group(), event = None):
        self.move(collidable, event)
        self.isCollided_with_treasures(treasures)
        self.isNextStage = self.isCollided_with_portal(portal)

    def move(self, collidable, event = None):
        keys = pygame.key.get_pressed()
        if(keys[pygame.K_LEFT]):
            self.hSpeed = -self.speed
            # self.image = spriteLists[]

        elif (keys[pygame.K_RIGHT]):
            self.hSpeed = self.speed
        
        else:
            self.hSpeed = 0

        if (keys[pygame.K_UP]):
            self.vSpeed = -self.speed

        elif (keys[pygame.K_DOWN]):
            self.vSpeed = self.speed

        else:
            self.vSpeed = 0

    
        self.isCollided(collidable)       
        
    def isCollided(self, collidable):
        self.rect.x += self.hSpeed
        collision_list = pygame.sprite.spritecollide(self, collidable, False)

        for collided_object in collision_list:
            # if (self.rect.bottom <= collided_object.rect.top or self.rect.top >= collided_object.rect.bottom):
            if (self.hSpeed > 0):
                self.rect.right = collided_object.rect.left
                self.hSpeed = 0

            elif (self.hSpeed < 0):
                self.rect.left = collided_object.rect.right
                self.hSpeed = 0

        self.rect.y += self.vSpeed
        collision_list = pygame.sprite.spritecollide(self, collidable, False)
        for collided_object in collision_list:
            # if (self.rect.left <= collided_object.rect.right or self.rect.right >= collided_object.rect.left):
                # Moving down
            if (self. vSpeed > 0):

                self.rect.bottom= collided_object.rect.top
                self.vSpeed = 0
            # Moving up
            if (self. vSpeed < 0):

                self.rect.top = collided_object.rect.bottom
                self.vSpeed = 0
    
    def isCollided_with_treasures(self, treasures):
        collision_list = pygame.sprite.spritecollide(self, treasures, True)

    def isCollided_with_portal(self, portal):
        if pygame.sprite.spritecollide(self, portal, True):
            return True
        else:
            return False

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):

        super().__init__()
        self.image = pygame.image.load('enemyA.png')
        # self.image = pygame.Surface((64, 64))
        # self.image.fill((255,0,0))

        # self.image = pygame.image.load('rat.png')
        self.rect = self.image.get_rect()
        
        self.rect.x = x 
        self.rect.y = y 
        
        self.speed = 3
        
        self.direction = random.choice(["up", "down", "left", "right"])
    
    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y
    
    def update(self, collidable = pygame.sprite.Group()):
        self.move()
        self.isCollided(collidable)

    def move(self):
        if self.direction == "up":
            self.dx = 0
            self.dy = -self.speed

        elif self.direction == "down":
            self.dx = 0
            self.dy = self.speed

        elif self.direction == "left":
            self.dx = -self.speed
            self.dy = 0

        elif self.direction == "right":
            self.dx = self.speed
            self.dy = 0

        else:
            self.dx = 0
            self.dy = 0
        
        self.rect.x += self.dx
        self.rect.y += self.dy

    def isCollided(self, collidable):
        collision_list = pygame.sprite.spritecollide(self, collidable, False)
        for collided_object in collision_list:
            # Moving right
            if (self.dx > 0):
                self.rect.right = collided_object.rect.left
                self.dx = 0
                self.direction = random.choice(["up", "down", "left"])

            # Moving Left
            if (self.dx < 0):
                self.rect.left = collided_object.rect.right
                self.dx = 0
                self.direction = random.choice(["up", "down", "right"])

            # Moving down
            if (self.dy > 0):
                self.rect.bottom= collided_object.rect.top 
                self.dy = 0
                self.direction = random.choice(["up", "left", "right"])
            # Moving up
            if (self.dy < 0):
                self.dx = 0
                self.rect.top = collided_object.rect.bottom
                self.direction = random.choice(["down", "left", "right"])

    def shift_world(self, shift_x, shift_y): 
        self.set_position(self.rect.x + shift_x, self.rect.y + shift_y)

class Wall(pygame.sprite.Sprite):

    def __init__(self, x, y, width = 64, height = 64):

        super().__init__()
        self.image = pygame.image.load('wall.png')
        
        # self.image = pygame.Surface((width, height))
        # self.image.fill((255,100,180))

        self.rect = self.image.get_rect()

        self.rect.x = x 
        self.rect.y = y 
    
    def shift_world(self, shift_x, shift_y): 
        self.rect.x += shift_x
        self.rect.y += shift_y

class Treasure(pygame.sprite.Sprite):

    def __init__(self, x, y, width = 64, height = 64):

        super().__init__()
        self.image = pygame.image.load('Treasure.png')
        
        # self.image = pygame.Surface((width, height))
        # self.image.fill((255,100,180))

        self.rect = self.image.get_rect()

        self.rect.x = x 
        self.rect.y = y 
    
    def shift_world(self, shift_x, shift_y): 
        self.rect.x += shift_x
        self.rect.y += shift_y        

class Portal(pygame.sprite.Sprite):

    def __init__(self, x, y, width = 64, height = 64):

        super().__init__()
        self.image = pygame.image.load('portal.png')
        
        # self.image = pygame.Surface((width, height))
        # self.image.fill((255,100,180))
        self.rect = self.image.get_rect()

        self.rect.x = x 
        self.rect.y = y 
    
    def shift_world(self, shift_x, shift_y): 
        self.rect.x += shift_x
        self.rect.y += shift_y     

class MiniMap(object):
    def __init__(self, win_width, win_height):
        super().__init__()
        # self.image = pygame.image.load('wall.png')

        self.width, self.height = 170, 170
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((255,255,255))

        self.rect = self.image.get_rect()

        self.rect.x = win_width - self.width
        self.rect.y = win_height - self.height
    
    def draw(self, window):
        window.blit(self.image,(self.rect.x, self.rect.y))

class MiniWall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.image.load('miniWall.png')

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

class Fog(pygame.sprite.Sprite):
    def __init__(self):

        super().__init__()
        self.image = pygame.image.load('fog.png')
        
        # self.image = pygame.Surface((width, height))
        # self.image.fill((255,100,180))

        self.rect = self.image.get_rect()

    def update(self, player_x, player_y):
        self.rect.centerx = player_x + 32
        self.rect.centery = player_y + 32

def create_instances():
    global current_level, running, player, player_group, miniMap, miniWalls_group, fog_group
    global walls_group, enemies_group, treasures_group, portal_group
    global win_width, win_height

    current_level = 0
    running = True

    player = Player()
    player_group = pygame.sprite.Group()
    player_group.add(player)

    walls_group = pygame.sprite.Group()
    enemies_group = pygame.sprite.Group()
    treasures_group = pygame.sprite.Group()
    portal_group = pygame.sprite.Group()
    miniWalls_group = pygame.sprite.Group()

    fog_group = pygame.sprite.Group()
    fog_group.add(Fog())

    miniMap = MiniMap(win_width, win_height)


def run_viewbox(player_x, player_y):
    global player, walls_Group, enemies_Group, treasures_group, portal_group
    left_viewbox = win_width/2 - win_width/8
    right_viewbox = win_width/2 + win_width/8
    top_viewbox = win_height/2 - win_height/8
    bottom_viewbox = win_height/2 + win_height/8
    dx, dy = 0, 0

    if(player_x < left_viewbox):
        dx = left_viewbox - player_x
        player.set_position(left_viewbox, player.rect.y)
    
    elif(player_x > right_viewbox):
        dx = right_viewbox - player_x
        player.set_position(right_viewbox, player.rect.y)

    if(player_y < top_viewbox):
        dy = top_viewbox - player_y
        player.set_position(player.rect.x, top_viewbox)
    
    elif(player_y > bottom_viewbox):
        dy = bottom_viewbox - player_y
        player.set_position(player.rect.x, bottom_viewbox)

    if (dx != 0 or dy != 0):
        for wall in walls_group:
            wall.shift_world(dx, dy)
        
        for enemy in enemies_group:
            enemy.shift_world(dx, dy)
        
        for treasure in treasures_group:
            treasure.shift_world(dx, dy)
        
        for portal in portal_group:
            portal.shift_world(dx, dy)

def define_maze():
    global levels
    level_1 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXX EXXX XXXXX XX  XXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXX EXXX XXXXE XX  XXXXXX    XXXXXXXXXXXXXXXXXXX",
    "XXXXXTTXXX XXXX  XX     TXX    XXXXXXXXXXXXXXXXXXX",
    "XXXXXP       XX  XX      XX    XXXXXXXXXXXXXXXXXXX",
    "XXXXXU       XX  XX  XXXXXX    XXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXX  XX     XXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXT        XX     XXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXX         XX TX     XXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XX     XXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XX     XXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XX     XXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XX     XXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XX     XXXXXXXXXXXXXXXX",    
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX     XXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XX     XXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XX     XXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XX     XXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XX     XXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XX     XXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XX     XXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XX     XXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XX     XXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XX     XXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XX     XXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XX     XXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XX     XXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XX     XXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XX     XXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XX     XXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XX     XXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XX     XXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XX XXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XX XXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XX XXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XX XXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XX XXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XX XXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XX XXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XX XXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XX XXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XX XXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XX XXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XX XXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XX XXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XX XXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX"
    ]

    level_2 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX      XXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX         XXXXXXXXXX",
    "XXXXXXT XXXXXXXT  XX               XXXXXXXXXXXXXXX",
    "XXXXXX  XXXXXXX   XX               XXXXXXXXXXXXXXX",
    "XXXXXX        XX  XX   XXXX        XXXXXXXXXXXXXXX",
    "XXXXXXXXXXX   XX  XX   XXXX        XXXXXXXXXXXXXXX",
    "XXXXXXP XXX   XX  XX   XXXX T      XXXXXXXXXXXXXXX",
    "XXXXXX   U    XX  XX   XXXXXX      XXXXXXXXXXXXXXX",
    "XXXXXX  T  E                       XXXXXXXXXXXXXXX",
    "XXXXXXXXXXXX                       XXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXX                XXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXX                XXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXX                XXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXX                XXXXXXXXXXXXXXXXX",    
    "XXXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXX                XXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXX                XXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXX                         XXXXXXXX",
    "XXXXXXX   XXXXXXX                         XXXXXXXX",
    "XXXXXXX   XXXXXXX                         XXXXXXXX",
    "XXXXXXX   XXXXXXX                         XXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX                XXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX                XXXXXXXX",
    "XXXXXXX              XXXXX                XXXXXXXX",
    "XXXXXXX              XXXXX                XXXXXXXX",
    "XXXXXXX              XXXXX                XXXXXXXX",
    "XXXXXXX              XXXXX                XXXXXXXX",
    "XXXXXXX              XXXXX                XXXXXXXX",
    "XXXXXXX              XXXXX                XXXXXXXX",
    "XXXXXXX              XXXXX                XXXXXXXX",
    "XXXXXXX              XXXXX                XXXXXXXX",
    "XXXXXXX              XXXXX                XXXXXXXX",
    "XXXXXXX              XXXXX                XXXXXXXX",
    "XXXXXXX              XXXXX                XXXXXXXX",
    "XXXXXXX              XXXXX                XXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX                XXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX                XXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX                XXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX                XXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX"
    ]

    level_3 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXX      XXXXXXXXXXXXXXXXXX",
    "XXXXXXT XXXXXXXT  XX               XXXXXXXXXXXXXXX",
    "XXXXXX  XXXXXXX   XX               XXXXXXXXXXXXXXX",
    "XXXXXX        XX  XX   XXX      X  XXXXXXXXXXXXXXX",
    "XXXXXXXXXXX   XX  XX   XXX      X  XXXXXXXXXXXXXXX",
    "XXXXXX  XXX   XX  XX   XXX      X TXXXXXXXXXXXXXXX",
    "XXXXXX        XX  XX   XXX      XXXXXXXXXXXXXXXXXX",
    "XXXXXX         T    P U            XXXXXXXXXXXXXXX",
    "XXXXXXXXXXXX       T    E          XXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",    
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXX   XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX"
    ]    

    levels = [level_1, level_2, level_3]

def setup_maze(current_level):
    global levels, player, walls_group, enemies_group, treasures_group, portal_group
    global win_height, win_width

    for y in range(len(levels[current_level])):
        for x in range(len(levels[current_level][y])):
            character = levels[current_level][y][x]
            pos_x = (x*64)
            pos_y = (y*64)

            if character == "X":
                #Update wall coordinates
                walls_group.add(Wall(pos_x, pos_y))
                miniWalls_group.add(MiniWall(win_width - 160 + (x * 3), win_height - 160 + (y * 3)))

            elif character == "P":
                player.set_position(pos_x, pos_y)

            elif character == "E":
                #Update enemy coordinates
                enemies_group.add(Enemy(pos_x, pos_y))
            
            elif character == "T":
                #Update enemy coordinates
                treasures_group.add(Treasure(pos_x, pos_y))
            
            elif character == "U":
                #Update enemy coordinates
                portal_group.add(Portal(pos_x, pos_y))

def clear_maze():
    global player, walls_group, enemies_group, treasures_group, portal_group, miniWalls_group
    walls_group.empty()
    enemies_group.empty()
    treasures_group.empty()
    portal_group.empty()
    miniWalls_group.empty()

    player.isNextStage = False

def nextStage(isNextStage):
    global current_level
    if isNextStage:
        current_level += 1
        print(current_level)
        if current_level == 3:
            pygame.quit()
        clear_maze()
        setup_maze(current_level)

#Initialize Game
#######################################################################################
# bgDict = loadImageDict('image/backgrounds')
# featureDict = loadImageDict('image/features')
# spriteLists = loadImageListInDict('image/sprites')

create_instances()
define_maze()
setup_maze(current_level)


################################################################################

while running:
    for event in pygame.event.get():
        if(event.type == pygame.QUIT) or \
        (event.type == pygame.KEYDOWN \
         and (event.key == pygame.K_ESCAPE or event.key == pygame.K_q )):
         running = False

    # Update objects
    player_group.update(walls_group, treasures_group, portal_group, event)
    event = None
    enemies_group.update(walls_group)
    nextStage(player.isNextStage)
    fog_group.update(player.rect.x, player.rect.y)
    
    # Update viewbox
    run_viewbox(player.rect.x, player.rect.y)

    # Draw 
    window.fill((0,0,0))

    walls_group.draw(window)
    portal_group.draw(window)
    treasures_group.draw(window)
    player_group.draw(window)
    enemies_group.draw(window)
    
    if current_level >= 1:
        fog_group.draw(window)

    miniMap.draw(window)
    miniWalls_group.draw(window)
    
    # Delay & Update Screen
    clock.tick(fps)
    pygame.display.update()

pygame.quit()