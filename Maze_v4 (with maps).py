import pygame, os, random, math

# Set up window
#####################################################################
pygame.init()

 # size of the game window
win_width, win_height = 1024, 768


# win_size = (win_width, win_height)
win_size = win_width, win_height

"""
set_mode(resolution=(0,0), flags=0, depth=0) -> Surface
This function will create a display Surface. The arguments passed in are requests for a display type.
The actual created display will be the best possible match supported by the system.The resolution argument is a pair of
numbers representing the width and height. The flags argument is a collection of additional options.
The depth argument represents the number of bits to use for color.
The Surface that gets returned can be drawn to like a regular Surface but changes will eventually be seen on the monitor.
"""
window = pygame.display.set_mode(win_size)


# set_caption(title, icontitle=None) -> None
#If the display has a window title, this function will change the name on the window
pygame.display.set_caption("MazeGame")

# create an object to help track time
clock = pygame.time.Clock()

fps = 30
######################################################################

def loadImageListInDict(path):
    # Create a list for every sub_dir, and load the images under the sub_dir into the the list.
    # Store the lists into a dictionary and return.
    listsDict = {}
    for folder in os.listdir(path):
        subPath = os.path.join(path, folder)
        if os.path.isdir(subPath):
            listsDict[folder] = []
            print(subPath)
            for image in os.listdir(subPath):
                print(image)
                if os.path.isfile(os.path.join(subPath,image)):
                    listsDict[folder].append(pygame.image.load(os.path.join(subPath,image)).convert_alpha())

    return listsDict

def loadImageInDict(path):
    # Load all the files(only images) under the directory into a dictionary and return.
    imageDict = {}
    for image in os.listdir(path):
        subPath = os.path.join(path, image)
        if os.path.isfile(subPath):
            imageDict[os.path.splitext(image)[0]] = pygame.image.load(subPath).convert_alpha()
    return imageDict

def loadImageInList(path):
    # Load all the files(only images) under the directory into a list and return.
    imageList = []
    for image in os.listdir(path):
        subPath = os.path.join(path, image)
        if os.path.isfile(subPath):
            imageList.append(pygame.image.load(subPath).convert_alpha())
    return imageList

# pygame.sprite.Sprite -> The base class for visible game objects
class Player(pygame.sprite.Sprite):
    # set image to be 32 x 32
    def __init__(self, color = pygame.Color.b, imageLists = {}, ghostImageList = [], width = 32, height = 32):

        # super function allows the use of pygame.Rect object
        super().__init__()

        # set rat image for this player
        self.image = imageLists['south'][0]

        # fetch rectangle object that has dimension of the image
        self.rect = self.image.get_rect()

        self.hSpeed = 0
        self.vSpeed = 0
        self.speed = 8
        self.imageLists = imageLists
        self.ghostImageList = ghostImageList
        self.isNextStage = False
        self.walkCount = 0
        
        self.direction = 'S'

        self.ghostWalkCount = 0
        self.invulnerable = False
        self.invulnerable_count = 0

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def set_absolute_position(self, x, y):
        self.abs_x = x
        self.abs_y = y

    # update function, every loop this function will be called
    def update(self, collidable = pygame.sprite.Group(), treasures = pygame.sprite.Group(),\
               portal = pygame.sprite.Group(), traps = pygame.sprite.Group(), enemies = pygame.sprite.Group(), spikes = pygame.sprite.Group()):
        self.move(collidable)
        self.isCollided_with_treasures(treasures)
        self.isNextStage = self.isCollided_with_portal(portal)
        if self.invulnerable:
            if self.invulnerable_count >= 90:
                self.invulnerable_count = 0
                self.invulnerable = False
            else:
                self.invulnerable_count += 1

        self.isCollided_with_damage_source(traps)
        self.isCollided_with_damage_source(enemies)
        self.isCollided_with_damage_source(spikes)

        # Implement animation
        self.walkAnimation()

    def move(self, collidable):
        # get key pressed by user
        keys = pygame.key.get_pressed()

        # If any direction key is pressed
        if(keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]):

            # account for horizontal movement if pressed left key
            if(keys[pygame.K_LEFT]):
                # left = negative speed, right = positive speed
                self.hSpeed = -self.speed

            elif (keys[pygame.K_RIGHT]):
                # self.image = spriteLists[]
                self.hSpeed = self.speed

            else:
                self.hSpeed = 0

            # account for vertical movement
            if (keys[pygame.K_UP]):
                self.vSpeed = -self.speed

            elif (keys[pygame.K_DOWN]):
                self.vSpeed = self.speed

            else:
                self.vSpeed = 0

            # Redefine direction
            if self.hSpeed > 0:
                if self.vSpeed > 0:
                    self.direction = 'SE'
                elif self.vSpeed < 0:
                    self.direction = 'NE'
                else:
                    self.direction = 'E'

            elif self.hSpeed < 0:
                if self.vSpeed > 0:
                    self.direction = 'SW'
                elif self.vSpeed < 0:
                    self.direction = 'NW'
                else:
                    self.direction = 'W'
            else:
                if self.vSpeed > 0:
                    self.direction = 'S'
                elif self.vSpeed < 0:
                    self.direction = 'N'

        # If all direction keys are not pressed
        else:
            self.hSpeed = 0
            self.vSpeed = 0

        # after determining the direction of player, check if there is any collision
        self.isCollided(collidable)

    def walkAnimation(self):
 
        if self.invulnerable == False:
           
            self.walkCount += 1
            
            if self.walkCount >= 18:
                self.walkCount = 0
            
            if self.direction == 'E':
                self.image = self.imageLists['east'][self.walkCount // 6]
            elif self.direction == 'N':
                self.image = self.imageLists['north'][self.walkCount // 6]
            elif self.direction == 'NE':
                self.image = self.imageLists['northeast'][self.walkCount // 6]
            elif self.direction == 'NW':
                self.image = self.imageLists['northwest'][self.walkCount // 6]
            elif self.direction == 'S':
                self.image = self.imageLists['south'][self.walkCount // 6]
            elif self.direction == 'SE':
                self.image = self.imageLists['southeast'][self.walkCount // 6]
            elif self.direction == 'SW':
                self.image = self.imageLists['southwest'][self.walkCount // 6]
            elif self.direction == 'W':
                self.image = self.imageLists['west'][self.walkCount // 6]
        
        else:
            self.ghostWalkCount += 1
            if self.ghostWalkCount >= 36:
                self.ghostWalkCount = 0
            self.image = self.ghostImageList[self.ghostWalkCount // 6]

    def isCollided(self, collidable):
        # Find sprites in a group that intersect another sprite.
        # spritecollide(sprite, group, dokill, collided = None)
        # Intersection is determined by comparing the Sprite.rect attribute of each Spri

        self.rect.x += self.hSpeed
        self.abs_x += self.hSpeed

        # Find sprites in a group that intersect another sprite.
        # spritecollide(sprite, group, dokill, collided = None)
        # Intersection is determined by comparing the Sprite.rect attribute of each Spri
        collision_list = pygame.sprite.spritecollide(self, collidable, False)

        # if intersection with collidable object in collision_list ( horizontal x direction )
        for collided_object in collision_list:
            # if (self.rect.bottom <= collided_object.rect.top or self.rect.top >= collided_object.rect.bottom):
            if (self.hSpeed > 0):
                # Update Absoulte position
                hDiff = collided_object.rect.left - self.rect.right
                self.abs_x += hDiff
                # Update relative position
                self.rect.right = collided_object.rect.left
                self.hSpeed = 0

            elif (self.hSpeed < 0):
                # Update Absoulte position
                hDiff = collided_object.rect.right - self.rect.left
                self.abs_x += hDiff
                # Update relative position
                self.rect.left = collided_object.rect.right
                self.hSpeed = 0

        self.rect.y += self.vSpeed
        self.abs_y += self.vSpeed
        # if intersection with collidable object in y direction
        collision_list = pygame.sprite.spritecollide(self, collidable, False)
        for collided_object in collision_list:
            # Moving down
            if (self. vSpeed > 0):
                # Update Absoulte position
                vDiff = collided_object.rect.top - self.rect.bottom
                self.abs_y += vDiff
                
                # Update relative position
                self.rect.bottom= collided_object.rect.top
                self.vSpeed = 0
            # Moving up
            elif (self. vSpeed < 0):
                # Update Absoulte position
                vDiff = collided_object.rect.bottom - self.rect.top
                self.abs_y += vDiff

                # Update relative position
                self.rect.top = collided_object.rect.bottom
                self.vSpeed = 0

    def isCollided_with_treasures(self, treasures):
        if (pygame.sprite.spritecollide(self, treasures, True)):
            food_collision.play()

    def isCollided_with_portal(self, portals):
        collision_list = pygame.sprite.spritecollide(self, portals, False)
        for portal in collision_list:
            if (self.rect.collidepoint(portal.rect.centerx, portal.rect.centery)):
                portal_collision.play()
                return True
    
    def isCollided_with_damage_source(self, damage_source):
        if (pygame.sprite.spritecollide(self, damage_source, False))\
           and (self.invulnerable == False):
            self.invulnerable = True
            enemy_collision.play()
            return True

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, imageLists):

        super().__init__()

        self.imageLists = imageLists
        self.image = self.imageLists['down'][0]

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.speed = 4
        self.direction = random.choice(["up", "down", "left", "right"])
        self.walkCount = 0

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
        
        self.walkAnimation()

        self.rect.x += self.dx
        self.rect.y += self.dy

    def walkAnimation(self):
        self.walkCount += 1
        if self.walkCount >= 6:
            self.walkCount = 0
        
        if self.direction == 'up':
            self.image = self.imageLists['up'][self.walkCount // 2]
        elif self.direction == 'down':
            self.image = self.imageLists['down'][self.walkCount // 2]
        elif self.direction == 'left':
            self.image = self.imageLists['left'][self.walkCount // 2]
        elif self.direction == 'right':
            self.image = self.imageLists['right'][self.walkCount // 2]


    def isCollided(self, collidable):
        # check for any enemy collision with walls_Group, if there is a collision, set the
        # enemy to move in a random direction
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
        self.rect.x += shift_x
        self.rect.y += shift_y

class Wall(pygame.sprite.Sprite):

    def __init__(self, x, y, width = 32, height = 32):

        super().__init__()
        self.image = pygame.image.load('wall_small.png').convert_alpha()

        # self.image = pygame.Surface((width, height))
        # self.image.fill((255,100,180))

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

    def shift_world(self, shift_x, shift_y):
        self.rect.x += shift_x
        self.rect.y += shift_y

    def draw(self, window):

        window.blit(self.image,(self.rect.x, self.rect.y))

class Treasure(pygame.sprite.Sprite):

    def __init__(self, x, y, width = 64, height = 64):

        super().__init__()
        self.image = pygame.image.load('foodA.png').convert_alpha()

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

    def shift_world(self, shift_x, shift_y):
        self.rect.x += shift_x
        self.rect.y += shift_y

class Trap(pygame.sprite.Sprite):

    def __init__(self, x, y, width = 64, height = 64):

        super().__init__()
        self.food_image = pygame.image.load('foodA.png').convert_alpha()
        self.trap_image = pygame.image.load('cage.png').convert_alpha()
        self.image = self.food_image

        self.rect = self.food_image.get_rect()

        self.rect.x = x
        self.rect.y = y

    def shift_world(self, shift_x, shift_y):
        self.rect.x += shift_x
        self.rect.y += shift_y

    def update(self, player_center_x, player_center_y):
        a = self.rect.centerx - player_center_x
        b = self.rect.centery - player_center_y
        
        distance = math.sqrt((a ** 2) + (b **2))

        if distance <= 50:
            self.image =  self.trap_image
        else:
            self.image = self.food_image

class Spike(pygame.sprite.Sprite):

    def __init__(self, x, y, imageList, width = 64, height = 64):

        super().__init__()

        self.imageList = imageList
        self.image = self.imageList[0]

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.count = 0

    def shift_world(self, shift_x, shift_y):
        self.rect.x += shift_x
        self.rect.y += shift_y

    def update(self):
        self.animation()

    def animation(self):
        self.count += 1
        if self.count >= 18:
            self.count = 0

        self.image = self.imageList[self.count // 3]

class Portal(pygame.sprite.Sprite):

    def __init__(self, x, y, imageList = None, width = 64, height = 64):

        super().__init__()
        self.image = pygame.image.load('portal.png').convert_alpha()
        self.imageList = imageList
        self.image = imageList[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.count = 0

    def update(self):
        self.animation()

    def animation(self):
        self.count += 1
        if self.count >= 50:
            self.count = 0

        self.image = self.imageList[self.count // 10]

    def shift_world(self, shift_x, shift_y):
        self.rect.x += shift_x
        self.rect.y += shift_y

class MiniMap(object):
    def __init__(self, win_width, win_height):
        super().__init__()

        self.width, self.height = 190, 190

        self.image = pygame.image.load('images/features/miniFrame.png').convert_alpha()
        self.rect = self.image.get_rect()

        self.bg = pygame.Surface((self.width - 20, self.height - 20))
        self.bg.fill((0,0,0))

        self.rect.x = win_width - self.width
        self.rect.y = win_height - self.height

    def draw(self, window):
        window.blit(self.bg,(self.rect.x + 10, self.rect.y + 10))
        window.blit(self.image,(self.rect.x, self.rect.y))

class MiniWall(pygame.sprite.Sprite):
    def __init__(self, x, y):

        super().__init__()

        self.image = pygame.image.load('miniWall.png').convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class MiniPlayer (object):
    def __init__(self, player_abs_x = 0, player_abs_y = 0, win_width = 1024, win_height = 768):

        super().__init__()

        self.image = pygame.image.load('images/features/miniPlayer.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.win_width = win_width
        self.win_height = win_height

    def update(self, player_abs_x, player_abs_y):
        mini_x = 150 / (32 * 50) * player_abs_x
        mini_y = 150 / (32 * 50) * player_abs_y
        
        self.rect.x = self.win_width - 170 + mini_x
        self.rect.y = self.win_height - 170 + mini_y

    def draw(self, window):
        window.blit(self.image, (self.rect.x - 5, self.rect.y - 5))

class Fog(pygame.sprite.Sprite):
    def __init__(self):

        super().__init__()
        self.image = pygame.image.load('fog.png').convert_alpha()

        self.rect = self.image.get_rect()

    def update(self, player_x, player_y):
        self.rect.centerx = player_x + 32
        self.rect.centery = player_y + 32

# Initialize all objects relevant to the game.
def create_instances():
    global current_level, running, player, player_group, miniMap, miniPlayer, miniWalls_group, fog_group
    global walls_group, enemies_group, treasures_group, portal_group, traps_group, spikes_group
    global win_width, win_height

    current_level = 0
    running = True

    player = Player(imageLists = ratImageLists, ghostImageList = ghostList)
    player_group = pygame.sprite.Group()
    player_group.add(player)

    walls_group = pygame.sprite.Group()
    enemies_group = pygame.sprite.Group()
    treasures_group = pygame.sprite.Group()
    portal_group = pygame.sprite.Group()
    traps_group = pygame.sprite.Group()
    spikes_group = pygame.sprite.Group()

    fog_group = pygame.sprite.Group()
    fog_group.add(Fog())

    miniMap = MiniMap(win_width, win_height)
    miniPlayer = MiniPlayer()
    miniWalls_group = pygame.sprite.Group()

def run_viewbox(player_x, player_y):
    # global player, walls_Group, enemies_Group, treasures_group, portal_group, spikes_group, traps_group

    left_viewbox = win_width/2 - win_width/8
    right_viewbox = win_width/2 + win_width/8
    top_viewbox = win_height/2 - win_height/8
    bottom_viewbox = win_height/2 + win_height/8
    dx, dy = 0, 0

    if(player_x <= left_viewbox):
        dx = left_viewbox - player_x
        player.set_position(left_viewbox, player.rect.y)

    elif(player_x >= right_viewbox):
        dx = right_viewbox - player_x
        player.set_position(right_viewbox, player.rect.y)

    if(player_y <= top_viewbox):
        dy = top_viewbox - player_y
        player.set_position(player.rect.x, top_viewbox)

    elif(player_y >= bottom_viewbox):
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

        for trap in traps_group:
            trap.shift_world(dx, dy)
        
        for spike in spikes_group:
            spike.shift_world(dx, dy)

def define_maze():
    global levels
    level_1 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX   T   XXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX    E    XXXXXX",
    "XXXXXXXX   TXXXXXXXXXXXXXXXXXXXXXX   XXXXX    XXXX",
    "XXXXXXXX    XXXXXXXXXXXXXXXXXXXXX   XXXXXXX    XXX",
    "XXXXXXXX    XXXXXXXXXXXXXXXXXXXX   XXXXXXXXXT  XXX",
    "XXXXXXXX    XXXXXXXXXXXXXXXXXXX   XXXXXXXXX   XXXX",
    "XXXXXXX  E   XXXXXXXXXXXXXXXXX   XXXXXXXXX   XXXXX",
    "XXXXXX   XX   XXXXXXXXXXXXXXX   XXXXXXXXX   XXXXXX",
    "XXXXX   XXXX   XXXXXXXXXXXXX   XXXXXXXXX   XXXXXXX",
    "XXXX   XXXXXX   XXXXXXXXXXX   XXXXXXXXX   XXXXXXXX",
    "XXX   XXXXXXXX   XXXXXXXXX   XXXXXXXXX   XXXXXXXXX",
    "XX   XXXXXXXXXX   XXXXXXX   XXXXXXXXX   XXXXXXXXXX",
    "XX   XXXXXXXXXXX   XXXXX   XXXXXXXXXX   XXXXXXXXXX",
    "XX   XXXXXXXXXXXX   XXX   XXXXXXXXXXX    XXXXXXXXX",
    "XX   XXXXXXXXXXXXX      TXXXXXXXXXXXXXX   XXXXXXXX",
    "XX   XXXXXXXXXXXXXX     XXXXXXXXXXXXXXXX  U XXXXXX",
    "XX   XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XX   XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XX   XXXP                        XXX    T      XXX",
    "XX   XXX                         XXX           XXX",
    "XX   XXX       T                 XXX   XXXXX   XXX",
    "XX   XXX                         XXX   XXXXX   XXX",
    "XX   XXX                         XXX   XXXXX   XXX",
    "XX   XXX                               XXXXX   XXX",
    "XX   XXX                      TXX      XXXXX   XXX",
    "XXXT  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX   XXX",
    "XXXX    XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX   XXX",
    "XXXXX    XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX   XXX",
    "XXXXXX                 T          XXXXXXXXXX  TXXX",
    "XXXXXXX               E            XXXXXXXXX   XXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX   XXXXXXXX   XXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX   XXXXXXX   XXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX   XXXXXX   XXX",
    "XXXXXXXXXXXXXXXXXXX                   XXXXXX   XXX",
    "XXXXXXXXXXXXXXXXXX                   TXXXXXX   XXX",
    "XXXXXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXXXXXXXXX   XXX",
    "XXXXXXXXXXXXXXXX   XXXXXXXXXXXX                XXX",
    "XXXXXXXXXXXXXXX   XXXXXXXXXXXXX                XXX",
    "XXXXXXXXXXXXXX   XXXXXXXXXXXXXX   XXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXX   XXXXXXXXXXXXXXX    XXXXXXXXXXXXXXX",
    "XXXXXXXXXXXX   XXXXXXXXXXXXXXXXXX   XXXXXXXXXXXXXX",
    "XXXXXXXXXXXT  XXXXXXXXXXT    XXXXX        TXXXXXXX",
    "XXXXXXXXXXXX   XXXXXXXX       XXXXXXX     XXXXXXXX",
    "XXXXXXXXXXXXX   XXXXXX   XXX   XXXXXXX   XXXXXXXXX",
    "XXXXXXXXXXXXXX   XXXX   XXXXX   XXXXX   XXXXXXXXXX",
    "XXXXXXXXXXXXXXX        XXXXXXX         XXXXXXXXXXX",
    "XXXXXXXXXXXXXXXX      XXXXXXXXX       XXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    ]

    level_2 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XU          XXXXXXXX   XXXXXXXX            XXXXXXX",
    "X     E     XXXXXXX   XXXXXXXX          E   XXXXXX",
    "XXXXXXXX    XXXXXX  EXXXXXXXXX XXXXXXXXXXX    XXXX",
    "XXXXXXXX    XXXXX   XXXXXXXXXX XT   XXXXXXX    XXX",
    "XXXXXXXX    XXXX   XXXXXXXXXXXX      XXXXXXX   XXX",
    "XXXXXXXX    XXX   XXXXXXXXXXXX   XX   XXXXXXX   XX",
    "XXXXXXX     XX   XXXXXXXXXXXX   XXXX   XXXXXX   XX",
    "XXXXXX       T     XXXXXXXXX   XXXXXX   XXXXX   XX",
    "XXXXX   XXXXXXXXX  XXXXXXXX   XXXXXXXX   XXX  TXXX",
    "XXXX   XXXXXXXXXX  XXXXXXX   XXXXXXXXXX   X   XXXX",
    "XXX   XXXXXXXXXXX  XXXXXX   XXXXXXXXXXXX     XXXXX",
    "XX   XXXXXXXXXXXX  XXXXXX   XXXXXXXXXXXXX   XXXXXX",
    "XX   XXXXXXXXXXE   XXXXXX   XXXXT          XXXXXXX",
    "XX   XXXXXXXXXX    XXXXXX   XXXX         XXXXXXXXX",
    "XX   XXXXXXXXXXXXXXXXXXXX   XXXX         XXXXXXXXX",
    "XX   XXXXXXXXXXXXXXXXXXXX   XXXX        P XXXXXXXX",
    "XX   XXXXXXXXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXXXXXXX",
    "XX   XXXXXXXXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXXXXXXX",
    "XX   XXXXXXXXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXXXXXXX",
    "XX   XXXXXXXXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXXXXXXX",
    "XX   XXXXXXXXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXXXXXXX",
    "XX   XXXXXXXXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXXXXXXX",
    "XX   XXXXXXXXXX                                XXX",
    "XX   XXXXXXXXXX                                XXX",
    "XX   XXXXXXXXXX   XXXXXXXXXXXXXXXXXXXXXXXXXX   XXX",
    "XXXT  XXXXXXXXXX   XXXXXXXXXXXXXXXXXXXXXXXXX   XXX",
    "XXXX    XXXXXXXXX   XXXXXXXXX  T  XXXXXXXXXX   XXX",
    "XXXXX    XXXXXXXXX   XXXXXXX   E   XXXXXXXXX   XXX",
    "XXXXXX    XXXXXXXXX   XXXXXX   XX              XXX",
    "XXXXXXX    XXXXXXXXX   XXXXX   XX      T       XXX",
    "XXX   XXX XXXXXXXXXXX          XX    XXXXXXX   XXX",
    "XXX   XXX         XXXX                XXXXXX   XXX",
    "XXX   XXXXXXXXXX  XXXXXXXXXXXXXXXXX   XXXXXX   XXX",
    "XXXX   XXXXXXXXX  XXXXXXXXXXXXXXXXX   XXXXXX   XXX",
    "XXXXX   XXXXXXXX  XXXXXXXXXXXXXXXXX   XXXXXX   XXX",
    "XXXXXX   XXXXXXX    XXXXXXXXXXXXXX   XXXXXXX   XXX",
    "XXXXXXX    T        XXXXXXXXXXXX   XXXXXXXXX   XXX",
    "XXXXXXXXX       XX   XXXXXXXXXXX    XXXXXXXX   XXX",
    "XXXXXXXX       XXXX  TXXXXXXXXX   XXXXXXXXXX   XXX",
    "XXXXXXX   XXXXXXXXXX              XXXXXXXXXX   XXX",
    "XXXXXX   XXXXXXXXXXXX             XXXXXXXXXX   XXX",
    "XXXXX   XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX   XXX",
    "XXXX   XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX    XXX",
    "XXXX   XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX   XXXXX",
    "XXXX   XXXXXXXXX             XXXXXXXXXXXX   XXXXXX",
    "XXXX   XXXXXXXXX              XXXXXXXXX    XXXXXXX",
    "XXXX   XXXXXXXXX   XXXXXXXXX   XXXXXXX   XXXXXXXXX",
    "XXXX               XXXXXXXXXX            XXXXXXXX",
    "XXXX               XXXXXXXXXXX      T    XXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    ]

    level_3 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XP         E       XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X                  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXX S   XXT                   E       X",
    "XXXXXXXXXXXXXX  S               E                X",
    "X           TX     XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XE                 XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X  XXXXXXXXXXX     XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X  XXXXXXXXXXX     XXXXXX         T              X",
    "XXX       E        XXXXXX S       E              X",
    "X                 TXXXXXX    XXXXXXXXXXXXXXXX  XXX",
    "X  S XXXXXXXXXXXXXXXXXXXE   XXXXXXXXXXXXXXXXX  XXX",
    "X   XXXXXXXXXXXXXXT       XXXXXXXXXXXXXXXXXXX  XXX",
    "X  XXXXXXXXXXXXXXX      XXXX                S  XXX",
    "X EXXXXXXXXXXXXXXX     XXXXX     E             XXX",
    "X  XXXXXXXXXXXXXXX    XX       TXXXXXXXXXXXXX  XXX",
    "X  XXXXXXXXXXXXXXX   XXX  XXXXXXX   XXXXXXXXXT XXX",
    "X                 S  XXX  XXXXXXX   XXXXXXXXX  XXX",
    "X                  E XXX      EXX   XXXXXXXXX  XXX",
    "X  XXXXXXXXXXXXXXXXXXXXXXXXX   XX  E           XXX",
    "X TXXXX                   XX   XX   E           XX",
    "X  XXXX                 E XX   XXXXXXXXXXXXXXXXXXX",
    "X  XXXXXXXXXXXXXXXXXXX    XX   XXXXXXXXXXXXXXXXXXX",
    "X  XXXXXXXXXXXXXXXXXXX    XXES XXXXXXXXXXXXXXXXXXX",
    "X                         XXXX                 TXX",
    "X                 E       XXXXXE                XX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  XX",
    "XE        XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  XX",
    "XXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  XX",
    "XXXXXXXXX       XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  XX",
    "XXXXXXXXXXXXXXX  XXXXXXXXXX        E        S   XX",
    "XX         XXXXX  XXXXXXXXX          E          XX",
    "XXEXXXXXXX XXXXX          XX  XXXXXXXXXXXXXXXX  XX",
    "XX XXXXXXXT XXXXXXXXXXXX  XX  XXXXXXXXXXXXXXXXX XX",
    "XXU XXXXXX  XXXXXXXXXXX  XXX   XXXXXXXXXXXXXXXT XX",
    "XXXXXXXXXX  XXXXXXXXXXXXT XXX   XXXXXXXXX  XXXEEXX",
    "XXXXXXXXXX  XXXXXXXXXXXX  XXXX   XXXXXXXX  XXX  XX",
    "XXXT        S         TS  XXXXX   XXXXXXX  XXX  XX",
    "XXX  E                    XXXXX     E      XXX  XX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXEXXXXXXXXXXXXXXXXXXXX  XX",
    "X                     XX                   TS   XX",
    "X  XXXXXXXXXXXXXXXXX  XX                   E    XX",
    "X  XX            EXX  XXXXXXXXXX  XXXXXXXXXXXX  XX",
    "X  XX XXXXXXXXXXX XX  XXXXXXXXXT XXXXXXXXXXXXX  XX",
    "X  XX XXXXXXXXXXX XX  XXXXXXXX  XXXXXXXXXXXXXX  XX",
    "X  XX XXXXXXXXXXX XX  XXXXXXX  XXXXXXXXXXXXXXX  XX",
    "X  XX XXXXXXXXXXX XX  XXXXXX  XXXXXXXXXXXXXXXX  XX",
    "X  XX XXXXXXXXXXX XX     E   S                  XX",
    "X  XX XXXXXXXXXXX XX         E                 TXX",
    "X                 XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    ]

    level_4 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XP           E                  XXXXXX           X",
    "X                               XXXXXX           X",
    "X  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  X",
    "X  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  X",
    "X  XX          E             XXT            CXX  X",
    "X  XX         S              XX              XX  X",
    "X EXX SXXXXXXXXXXXXXC XXXXXXXXXXXXX  XXXXXXS XX SX",
    "X  XX  XXXXXXXXXXXXX  XXXXXXXXXXXXXS XXXXXX  XX  X",
    "XS XX  XX      E                 XX      XX  XX  X",
    "X  XX  XX  E                     XX      XX  XXS X",
    "X  XX  XX  XXXXXXXXXXXXXXXXXXXXXXXXXXXX  XXE XX  X",
    "X  XX  XX  XXXXXXXXXXXXXXXXXXXXXXXXXXXX  XX  XX  X",
    "X  XX  XX  XX           E  S          T  XX      X",
    "X  XX  XX  XX          S      CS         XX   E  X",
    "X  XX  XX  XX  XXXXXXXXXXXXXXXXXXXX  XX  XX  XX  X",
    "X  XX  XX  XX  XXXXXXXXXXXXXXXXXXXX  XX  XX  XX  X",
    "X  XX  XX  XX  XX            XX  XX  XX  XXT XX  X",
    "X  XX  XX  XX  XX   E      X XX  XX  XX  XXE XX  X",
    "X  XX  XXXXXX  XXS XX  XXXX XXX  XX  XX  XX  XX  X",
    "X  XX  XXXXXX  XX  XX XXXXX XXX  XX  XX  XX  XX  X",
    "X  XXE XX      XX  XX XXXXX  XX  XXXXXX  XX  XXS X",
    "X  XX  XX      XX  XX  X  X  XX  XXXXXX  XX  XX  X",
    "X  XX  XX SXX  XX  XXX  SX   XX  E   XXXXXX EXX SX",
    "X  XX  XX  XX  XX  XXCX  X X XX  X   XXXXXX  XX  X",
    "X  XX  XXS XX  XX  XX   X X  XX  XX  XX  XXXXXXS X",
    "X  XX  XX  XXE XX  XXTXX    XXX  XX  XXC XXXXXX  X",
    "X  XX  XX SXX  XX  XX     X  XX  XXS     XX  XX TX",
    "X  XX  XX  XX  XX  XX   X X      XX      XX  XX  X",
    "X  XX  XX  XX  XX  XX    X   X   XX  XX      XX  X",
    "X  XX  XX  XX  XX  XX  XXXXXXXXXXXXC XXE     XX  X",
    "X  XX  XX  XX  XX  XXXXXXXXXXXXXXXXE XX  XX  XX  X",
    "X  XX  XX  XX  XX   E            XX  XX  XX SXX  X",
    "X  XX  XX  XX EXX                XX  XX  XX      X",
    "X  XX  XX EXX  XXXXXXXXXXXXX SXXXXXXXXXXXXX      X",
    "X  XX  XX  XX  XXXXXXXXXXXXX SXXXXXXXXXXXXXC XX  X",
    "X  XX  XX  XX        XX            E     XX  XX EX",
    "X  XX  XX  XX  C     XX      E           XX  XX  X",
    "X  XX  XX  XXXXXXXXXXXXXXXXXXXXXXXXXXXX  XXXXXX  X",
    "X  XX  XXE XXXXXXXXXXXXXXXXXXXXXXXXXXXX  XXXXXXXXX",
    "X  XX  XX        XX       E        XX    C   XXXXX",
    "X  XX  XX        XXC               XXE       XXXXX",
    "X  XX  XX  XXXXXXXXXXXXXXXXXXX  XXXXXXXXXXX  XXXXX",
    "X  XX  XX  XXXXXXXXXXXXXXXXXXX  XXXXXXXXXXX  XXC X",
    "X  SS  XX       E         T          XX      XX  X",
    "X     TXX                 S          XX      XX  X",
    "X  XXXXXXXXXXXXXXXXXXX  XXXXXXXXXXXXXXXXX SXXXX  X",
    "X  XXXXXXXXXXXXXXXXXXX  XXXXXXXXXXXXXXXXXE XXXX  X",
    "X                                  XXXX          X",
    "X                     E            XXXXT      TU X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    ]

    levels = [level_1, level_2, level_3, level_4]
def setup_maze(current_level):

    for y in range(len(levels[current_level])):
        for x in range(len(levels[current_level][y])):
            character = levels[current_level][y][x]
            pos_x = (x*32)
            pos_y = (y*32)

            if character == "X":
                #Update wall coordinates
                walls_group.add(Wall(pos_x, pos_y))
                miniWalls_group.add(MiniWall(win_width - 170 + (x * 3), win_height - 170 + (y * 3)))

            elif character == "P":
                player.set_position(pos_x, pos_y)
                player.set_absolute_position(pos_x, pos_y)
                miniPlayer.update(pos_x, pos_y)

            elif character == "E":
                #Update enemy coordinates
                enemies_group.add(Enemy(pos_x, pos_y, chefImageLists))

            elif character == "T":
                #Update treasure coordinates
                treasures_group.add(Treasure(pos_x, pos_y))

            elif character == "U":
                #Update portal coordinates
                portal_group.add(Portal(pos_x, pos_y, portalList))
            
            elif character == "C":
                #Update trap coordinates
                traps_group.add(Trap(pos_x, pos_y))
            
            elif character == "S":
                #Update spike coordinates
                spikes_group.add(Spike(pos_x, pos_y, spikeList))

# Empty the maze
def clear_maze():
    walls_group.empty()
    enemies_group.empty()
    treasures_group.empty()
    traps_group.empty()
    spikes_group.empty()
    portal_group.empty()
    miniWalls_group.empty()

    player.isNextStage = False

def nextStage(isNextStage):
    global current_level
    if isNextStage:
        current_level += 1
        print(current_level)
        if current_level == 4:
            pygame.quit()
        clear_maze()
        setup_maze(current_level)

#Initialize Game
#######################################################################################

# Load images
ratImageLists = loadImageListInDict('images/rat')
chefImageLists = loadImageListInDict('images/chef')

ghostList = loadImageInList('images/ghost')
portalList = loadImageInList('images/portal')
spikeList = loadImageInList('images/spike')

# Load musics & sound
music = pygame.mixer.music.load(os.path.join('audios','Background_Music.mp3'))
pygame.mixer.music.play(-1)
food_collision = pygame.mixer.Sound(os.path.join('audios','Food_Collision.wav'))
enemy_collision = pygame.mixer.Sound(os.path.join('audios','Enemy_Collision.wav'))
portal_collision = pygame.mixer.Sound(os.path.join('audios','Portal_Collision.wav'))


# Initialise the maze
create_instances()
define_maze()
setup_maze(current_level)

################################################################################
"""
    Pygame handles all its event messaging through an event queue.
    The routines in this module help you manage that event queue.
    The input queue is heavily dependent on the pygame display module.
    If the display has not been initialized and a video mode not set, the event queue will not really work.
    The queue is a regular queue of pygame.event.EventTypepygame object for representing SDL events event objects,
    there are a variety of ways to access
"""
while running:
    for event in pygame.event.get():
        if(event.type == pygame.QUIT) or \
        (event.type == pygame.KEYDOWN \
         and (event.key == pygame.K_ESCAPE or event.key == pygame.K_q )):
         running = False

    # Update objects

    # player move -> check for collision with treasure / portal / enemy
    player_group.update(walls_group, treasures_group, portal_group, traps_group, enemies_group, spikes_group)

    # from player group update -> check if collide with portal to advance to next stage
    nextStage(player.isNextStage)
    
    portal_group.update()
    enemies_group.update(walls_group)
    traps_group.update(player.rect.centerx, player.rect.centery)
    spikes_group.update()

    fog_group.update(player.rect.x, player.rect.y)
    miniPlayer.update(player.abs_x, player.abs_y)
    
    # Update view camera
    run_viewbox(player.rect.x, player.rect.y)
    # Draw

    # Fill background with black color
    window.fill((0,0,0))

    for wall in walls_group:
        if (wall.rect.x < win_width) and (wall.rect.y < win_height):
            wall.draw(window)
    
    portal_group.draw(window)
    treasures_group.draw(window)
    player_group.draw(window)
    enemies_group.draw(window)
    traps_group.draw(window)
    spikes_group.draw(window)

    # Implement fog from level 2 onwards
    if current_level >= 1:
        fog_group.draw(window)

    miniMap.draw(window)
    miniWalls_group.draw(window)
    miniPlayer.draw(window)

    # Delay & Update Screen
    pygame.display.flip()
    clock.tick_busy_loop(fps)

pygame.quit()
