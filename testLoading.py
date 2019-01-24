import pygame, os, random, math, sys

pygame.init()

win_width = 1280
win_height = 720

win_size = win_width, win_height
window = pygame.display.set_mode(win_size)


loadingScreen = pygame.image.load('images/backgrounds/loadingScreen.png')

def gameOverRect(win_width, win_height, font = None):
    myfont = pygame.font.SysFont(None,84)
    gameOverSurface = myfont.render("GAME OVER", False, (255,255,255))
    gameOverRect = gameOverSurface.get_rect()

    gameOverRect.centerx = win_width / 2
    gameOverRect.centery = win_height / 11

    return (gameOverSurface, gameOverRect)

gameOverSurface = gameOverRect(win_width, win_height)

while True:

    window.blit(loadingScreen, (0,0))
    window.blit(gameOverSurface[0], gameOverSurface[1])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.flip()
