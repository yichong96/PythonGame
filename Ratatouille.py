import turtle
import math
import random
import time




# create window. Turtle module, screen method.
wn = turtle.Screen()

# change background color to black
wn.bgcolor("black")

# change title bar
wn.title("Ratatouille Maze")

# 700x700 pixels
wn.setup(700,700)

turtle.register_shape("remy_24pixel_black.gif")
turtle.register_shape("chefSkinner.gif")
###(1)Make enemies move Resolved
###(2)Create static obstacles
###(3)Create Hidden traps

# Class Pen inherits from turtle.Turtle class
# Represents a wall
class Pen(turtle.Turtle):
    def __init__(self):
        # borrow super class constructor
        turtle.Turtle.__init__(self)

        self.shape("square")

        self.color("white")
        # turtle draws when you move to new coordinates. Default is pendown()
        self.penup()
        # animation speed
        self.speed(0)

class Player(turtle.Turtle):
    def __init__(self):
        # initialize parent class
        turtle.Turtle.__init__(self)
        # instance shape will be square
        self.shape("remy_24pixel_black.gif")

        self.color("blue")
        self.penup()
        # animation speed = 0
        self.speed(0)
        self.score = 0

    def go_up(self):
        move_to_x = player.xcor()
        move_to_y = player.ycor() + 24

        # if coordinates of wall is inside the walls list, then dont move up further
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_down(self):
        move_to_x = player.xcor()
        move_to_y = player.ycor() - 24

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_left(self):
        move_to_x = player.xcor() - 24
        move_to_y = player.ycor()

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_right(self):
        move_to_x = player.xcor() + 24
        move_to_y = player.ycor()

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def is_collision(self,other):
        a = self.xcor()-other.xcor()
        b = self.ycor()-other.ycor()
        distance = math.sqrt ( (a ** 2) + (b ** 2) )

        # is the location of self and other really close ? If they are then there is likely to have a collision
        if distance < 5:
            return True
        else:
            return False

class Ingredient(turtle.Turtle):
    def __init__(self, x, y):
            turtle.Turtle.__init__(self)
            self.shape("circle")
            self.color("gold")
            self.penup()
            self.speed(0)
            self.score = 10
            self.goto(x, y)

    def destroy(self):
        self.goto(2000,2000)
        self.hideturtle()

class Enemy(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("chefSkinner.gif")
        self.color("red")
        self.penup()
        self.speed(0)
        self.goto(x,y)
        self.direction = random.choice(["up", "down", "left", "right"])

    def move(self):
        if self.direction == "up":
            dx = 0
            dy = 24
        elif self.direction == "down":
            dx = 0
            dy = -24
        elif self.direction == "left":
            dx = -24
            dy = 0
        elif self.direction == "right":
            dx = 24
            dy = 0
        else:
            dx = 0
            dy = 0

        move_to_x = self.xcor() + dx
        move_to_y = self.ycor() + dy

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
        else:
            self.direction = random.choice(["up","down", "left", "right"])

        turtle.ontimer(self.move, t = random.randint(90,200))

    def destroy(self):
        self.goto(2000,2000)
        self.hideturtle()

class Portal(turtle.Turtle):
    def __init__(self,x,y):
        turtle.Turtle.__init__(self)
        self.shape("triangle")
        self.color("green")
        self.penup()
        self.speed(0)
        self.goto(x,y)




# to avoid confusion for levls[0] being level 1
levels=[""]



level_1 = [
"XXXXXXXXXXXXXXXXXXXXXXXXXX",
"XP XXXXXXXXE XXXXXXXXXXXXX",
"X  XXXXXXXX  XXXXXXXXXXXXX",
"X        XX  XXXXXXXXXXXXX",
"XXXXXD   XX  XX  XXXXXXXXX",
"XXXXXX   XX  XX  XXXXXXXXX",
"XI XXX    X  XX     EXXXXX",
"X                   XXXXXX",
"X        XXXXXX      XXXXX",
"XXXXX    XXXXXX  XXXXXXXXX",
"XXXXXXX   XXXXX   XXXXXXXX",
"XXXXXI    XXXXX  XXXXXXXXX",
"XXXXXXXXXXXXXXX    XXXXXX",
"XXXXXXXXXXXXXXX         XX",
"XXXXXXXXXXXXXXXXXXXXXXXXXX"
]

levels.append(level_1)

level_2 = [
"XXXXXXXXXXXXXXXXXXXXXXXXXX",
"XP XXXXXXXX  XXXXXXXXXXXXX",
"X  XXXXXXXX  XXXXXXXXXXXXX",
"X        XX  XXXXXXXXXXXXX",
"XXXXXX   XX  XX XXXXXXXXX",
"XXXXXX   XX  XX  XXXXXXXXX",
"X  XXX    X  XX     EXXXXX",
"X                   XXXXXX",
"X        XXXXXX    PXXXXX",
"XXXXX    XXXXXX  XXXXXXXXX",
"XXXXXXX   XXXXX   XXXXXXXX",
"XXXXXI    XXXXX  XXXXXXXXX",
"XXXXXXXXXXXXXXX    IXXXXXX",
"XXXXXXXXXXXXXXX   XXXXXXXX",
"XXXXXXXXXXXXXXXXXXXXXXXXXX"
]

levels.append(level_2)

##n = iter(levels)
##print(n)

#create class instances
pen = Pen()
player = Player()

# create object coordinate list
walls = []  # add (x,y) coordinate of every block of wall.
ingredients = []    # add (x,y) coordinate of ingredient to ingredients list
enemies = []
portals = []

def setup_maze(level):
    # for each rows in the level
    for y in range(len(level)):
        # for each columns in the level
        for x in range(len(level[y])):
            character = level[y][x] # coordinates of the character on map (rows,columns)
            # translation to actual screen coordinates. Top left corner coordinates = (-288,288)
            screen_x = -288 + (x * 24)
            screen_y = 288 - (y * 24)

            # going through every single cell
            if character == "X":
                # if encounter a wall, make your pen go to that coordinate
                pen.goto(screen_x, screen_y)
                # stamp the wall
                pen.stamp()
                # adding (x,y) coordinate pairs of walls to wall list
                walls.append((screen_x, screen_y))

            if character == "P":
                 # if character is a P, you move the player to that coordinates
                 player.goto(screen_x, screen_y)

            if character == "I":
                ingredients.append(Ingredient(screen_x, screen_y))

            if character == "E":
                enemy = Enemy(screen_x,screen_y)
                enemies.append(enemy)

            if character == "D":
                portals.append(Portal(screen_x, screen_y))


setup_maze(levels[1])

print(portals)


for Enemy in enemies:
    turtle.ontimer(Enemy.move, t=250)



turtle.listen()
turtle.onkey(player.go_left, "Left")
turtle.onkey(player.go_right, "Right")
turtle.onkey(player.go_up, "Up")
turtle.onkey(player.go_down, "Down")

wn.tracer(0) #turn off screen update delay

#Main Game Loop
while True:
    for Ingredient in ingredients:
        if player.is_collision(Ingredient):
            player.score += Ingredient.score
            print ("Player Score: {}".format(player.score))
            Ingredient.destroy()
            ingredients.remove(Ingredient)

    for Enemy in enemies:
        if player.is_collision(Enemy):
            print("enemy")
            print("Player dies!")
            turtle.bye()

    for portal in portals:
        if player.is_collision(portal):
            print("here")
            wn.clearscreen()
            wn.bgcolor("black")
            break


##    for Portal in portals:
##
##        if player.is_collision(Portal):
##                    if Portal in levels[n]:
##                        setup_maze[n+1]
####        else:
####            print("Congratulations! You have completed the game!")
####            turtle.bye()
##



    wn.update() # Update Screen


time.sleep(5)
