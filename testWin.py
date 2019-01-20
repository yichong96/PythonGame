import pygame, sys, time

import pygame_textinput
import os


# File I/O
HS_FILE = "highscore.txt"
SCORE = 100
FONT = 'freesandsbold.ttf'
def load_data():
    # load high score
    dir = path.dirname(__file__)
    print(dir)
    print("path " + path.join(dir,HS_FILE))
    with open(path.join(dir, HS_FILE), 'w') as f:    # if file doesnt exist it will create the file
        try:
            highscore = int(f.read())
        except:
            highscore = 0

#load_data()
pygame.init()








    #def update(self):
    #    self.index += 1
    #    if self.index >= len(self.images):
    #        self.index = 0
    #    self.image = self.images[self.index]

"""
win_width, win_height = 1024, 768
win_size = win_width, win_height
screen = pygame.display.set_mode(win_size)
screen.fill((225,225,225))
"""

class GameOverWindow:

    def __init__(self, message, win_width, win_height, FONT, leaderboardFile, score, level):

        self.message = message

        self.win_width = win_width

        self.win_height = win_height

        self.font = FONT

        self.score = score

        self.level = level

        (self.gameOverSurface, self.gameOverRect)= self.gameOverRect(win_width, win_height,self.font)


        (self.myScoreSurface, self.myScoreRect)= self.myScoreRect(win_width, win_height, self.gameOverRect, self.font)

        (self.myUserSurface, self.myUserRect) = self.myUserRect(self.myScoreRect)

        self.enterUserRect = pygame.Rect((self.myUserRect.right + 30, self.myUserRect.top), (200, 0))

        self.enterUserRect.h = self.myUserRect.h

        win_size = (win_width, win_height)

        (self.leaderBoardSurface, self.leaderBoardRect) = self.leaderBoardRect(self.myUserRect)

        self.screen = pygame.display.set_mode(win_size)

        self.leaderBoardContainer = self.createLeaderboardRect()

        self.leaderBoardFile = leaderboardFile

        self.mySaveRect = None

        self.myTryAgainRect = None





    class User: # encapsulates information relating to each leaderboard
        def __init__(self, name, score, level):
            self.name = name
            self.score = score
            self.level = "Level " + str(level)






    class TestSprite(pygame.sprite.Sprite):

        def __init__(self, win_width, win_height):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load('fatRat1_burned.png')
            """
            self.images = []
            self.images.append(load_image('Rat4_1_150x150.png'))
            self.images.append(load_image('Rat5_150x150.png'))
            self.images.append(load_image('Rat6_150x150.png'))

            self.index = 0
            self.image = self.images[self.index]
            """
            self.rect = pygame.Rect(5, 5, 200, 200)
            self.rect.centerx = win_width / 2 + 70
            self.rect.centery = win_height / 8 * 7



    def gameOverRect(self, win_width, win_height, font = FONT):
        myfont = pygame.font.SysFont(FONT, 84)
        gameOverSurface = myfont.render(self.message, False, (150,150,150))
        gameOverRect = gameOverSurface.get_rect()

        gameOverRect.centerx = win_width / 2
        gameOverRect.centery = win_height / 11

        return (gameOverSurface, gameOverRect)

    def myScoreRect(self, win_width, win_height, gameOverRect, font = FONT):
        myfont = pygame.font.SysFont(FONT, 50)
        myScoreSurface = myfont.render("Score:   " + str(self.score), False, (150,150,150))
        myScoreRect = myScoreSurface.get_rect()

        myScoreRect.left = gameOverRect.left + 5
        myScoreRect.top = gameOverRect.top + 100

        return (myScoreSurface, myScoreRect)

    def myUserRect(self ,myScoreRect):
        myfont = pygame.font.SysFont(FONT, 50)
        myUserSurface = myfont.render("Username: " , False, (150,150,150))
        myUserRect = myUserSurface.get_rect()

        myUserRect.top = myScoreRect.top + 50
        myUserRect.left = myScoreRect.left

        return (myUserSurface, myUserRect)

    def leaderBoardRect(self, myUserRect):
        myfont = pygame.font.SysFont(FONT, 50)
        myLeaderBoardSurface = myfont.render("Leaderboard " , False, (150,150,150))
        myLeaderBoardRect = myLeaderBoardSurface.get_rect()

        myLeaderBoardRect.left = self.myUserRect.left
        myLeaderBoardRect.top = self.myUserRect.top + 50

        return (myLeaderBoardSurface, myLeaderBoardRect)

    def createLeaderboardRect(self):
        return  pygame.Rect((self.leaderBoardRect.left, self.leaderBoardRect.top + 50), (self.win_width / 2, self.win_height / 3 ))


    def readLeaderBoard(self, leaderBoardFile):
        # read the high scores as a list of users
        user_list = []
        with open(leaderBoardFile, "r") as f:
            for line in f:
                print(line)
                string_arr = line.split(",")
                user = self.User(string_arr[0], int(string_arr[1]), int(string_arr[2]))
                user_list.append(user)

        print(len(user_list))

        return user_list





    def showLeaderBoard(self, leaderBoardContainer, list_of_users):
        # sort list of users
        users_list = self.readLeaderBoard(self.leaderBoardFile)
        for user in users_list:
            print(user.name + " " + str(user.score))

        users_list = sorted(users_list, key = lambda x: x.score, reverse = True)

        users_list = users_list[:5]

        for user in users_list:
            print(user.name + " " + str(user.score))

        start_top = leaderBoardContainer.h + 50
        user_left = leaderBoardContainer.left + 10


        score_left = self.leaderBoardContainer.w / 4 * 2 + self.leaderBoardContainer.left


        level_left = self.leaderBoardContainer.w / 5 * 4 + self.leaderBoardContainer.left




        list_rect = []

        for i in range(len(users_list)):  # go through the top 5 leaderboard

            # append username onto screen
            myfont = pygame.font.SysFont(FONT, 40)
            userSurface = myfont.render(str(i + 1) + ". " + str(users_list[i].name), False, (150, 150, 150))
            userSurfaceRect = userSurface.get_rect()

            userSurfaceRect.left = user_left
            userSurfaceRect.top = start_top


            # append score onto screen
            myfont = pygame.font.SysFont(FONT, 40)
            myScoreSurface = myfont.render(str(users_list[i].score), False, (150, 150, 150))
            myScoreRect = myScoreSurface.get_rect()

            myScoreRect.left = score_left
            myScoreRect.top = start_top


            myfont = pygame.font.SysFont(FONT, 40)
            myLevelSurface = myfont.render(str(users_list[i].level), False, (150, 150, 150))
            myLevelRect = myLevelSurface.get_rect()

            myLevelRect.left = level_left
            myLevelRect.top = start_top

            start_top += 50

            list_rect.append((userSurface, userSurfaceRect))
            list_rect.append((myScoreSurface, myScoreRect))
            list_rect.append((myLevelSurface, myLevelRect))

        for leaders in list_rect:
            self.screen.blit(leaders[0], leaders[1])


    def drawSaveButton(self):
        saveRect = pygame.Rect((self.leaderBoardContainer.left, self.leaderBoardContainer.bottom + 100 , 100, 50))
        pygame.draw.rect(self.screen, (255,255,0), saveRect)

        myfont = pygame.font.SysFont(FONT, 32)
        mySaveSurface = myfont.render("Save " , False, (10,10,10))
        self.mySaveRect = mySaveSurface.get_rect()

        self.mySaveRect.centerx = saveRect.centerx
        self.mySaveRect.centery = saveRect.centery

        self.screen.blit(mySaveSurface, self.mySaveRect)



    def drawTryAgainButton(self):
        rect = pygame.Rect(0,0,110,50)
        rect.right = self.leaderBoardContainer.right
        rect.top = self.leaderBoardContainer.bottom + 100

        pygame.draw.rect(self.screen, (1,200,32), rect)

        myfont = pygame.font.SysFont(FONT, 32)
        myTryAgainSurface = myfont.render("Try again " , False, (10,10,10))
        self.myTryAgainRect = myTryAgainSurface.get_rect()

        self.myTryAgainRect.centerx = rect.centerx + 5
        self.myTryAgainRect.centery = rect.centery

        self.screen.blit(myTryAgainSurface, self.myTryAgainRect)


    def write_to_file(self, leaderBoardFile, message):
        with open(leaderBoardFile, "a") as f:
            f.write(message + "\n")
        print("message added ")






    def drawAllUI(self, my_group):
        self.screen.fill((225,225,225))
        self.screen.blit(self.gameOverSurface, self.gameOverRect)
        my_group.draw(self.screen)
        pygame.draw.rect(self.screen, (0,0,255), self.enterUserRect, 2)
        pygame.draw.rect(self.screen, (0,0,255), self.leaderBoardContainer, 2)
        self.screen.blit(self.myScoreSurface, self.myScoreRect)
        self.screen.blit(self.myUserSurface, self.myUserRect)
        self.screen.blit(self.leaderBoardSurface, self.leaderBoardRect)
        self.showLeaderBoard(self.leaderBoardContainer, [10,20,30,40,50])



        self.drawSaveButton()
        self.drawTryAgainButton()




    def run(self):
        mySprite = self.TestSprite(self.win_width, self.win_height)
        my_group = pygame.sprite.Group(mySprite)
        textinput = pygame_textinput.TextInput()


        while True:

            self.drawAllUI(my_group)

            #pygame.draw.rect(self.screen, (0,255,0), (self.leaderBoardContainer.left, self.leaderBoardContainer.bottom + 100 , 100, 50))

            #pygame.draw.rect(self.screen, (255,255,0), (self.leaderBoardContainer.left, self.leaderBoardContainer.bottom + 100 , 100, 50))
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.mySaveRect.collidepoint(pygame.mouse.get_pos()):
                        assert textinput.get_text() != ""
                        user = textinput.get_text()
                        append_line = user + ", " + str(self.score) + ", " + str(self.level)
                        self.write_to_file(self.leaderBoardFile, append_line)

                    elif self.myTryAgainRect.collidepoint(pygame.mouse.get_pos()):
                        os.execv(sys.executable, [sys.executable, "Maze_v5.py"] + sys.argv)


            if textinput.update(events):
                my_text = textinput.get_text()
                print(my_text)
                break

            self.screen.blit(textinput.get_surface(), (self.enterUserRect.left + 5, self.enterUserRect.top + 5))
            pygame.display.update()

#gameOverWindow = GameOverWindow(1024,768,FONT, "highscore.txt", 200, 4)
#gameOverWindow.run()



#enterUserRect = pygame.Rect((myUserRect.right + 30, myUserRect.top), (200, 35))
