import pygame
import random
import math
from pygame import mixer


pygame.init()

# Screen stuff
screen = pygame.display.set_mode((800,600))
background = pygame.image.load("spaceimage.jpg")

# Music
mixer.music.load("C:/Users/vince/YouTube/YouTube Music/Movie Tracks/Star Wars/Duel Of The Fates (How to spoon) MIDI Edition.mp3")
mixer.music.play(-1)    # allows the music to loop

# Title and Icon
pygame.display.set_caption("UniWars")
icon = pygame.image.load("game_icon.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemies = 6

for i in range(num_enemies):
    enemyImg.append(pygame.image.load("tiefighter.png"))
    enemyX.append(random.randint(0, 735))    # spawns @ random spot
    enemyY.append(random.randint(30,60))
    enemyX_change.append(2)
    enemyY_change.append(40)

# Enemy 2 (Alien Ship)
# alienShipImg = pygame.image.load("alienship.png")
# alienShipX = 370
# alienShipY = 480
# alienShipX_change = 0

# Bullet 1
# ready = cannot see bullet, fire = currently moving
bullet1Img = pygame.image.load("bullet_1.png")
bullet1X = 0
bullet1Y = 480  # same as player y-axis
bullet1X_change = 0
bullet1Y_change = 10
bullet1_state = "ready"

# Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10

# Game Over Text Display
game_over_font = pygame.font.Font("freesansbold.ttf", 64)

def showScore(x, y):
    score = font.render("Score: {:d}".format(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def gameOver():
    game_over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over_text, (200, 250))    

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

# def alienship(x, y):
#     screen.blit(alienShipImg, (x, y))

def fire(x, y):
    global bullet1_state
    bullet1_state = "fire"
    screen.blit(bullet1Img, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bullet1X, bullet1Y):
    distance = math.sqrt((math.pow(enemyX - bullet1X, 2)) + (math.pow(enemyY - bullet1Y, 2)))
    return distance < 27



# Game loop
running = True
while running:
    # Background
    screen.fill((55, 0, 97))
    # Background image
    screen.blit(background, (0,0))

    for event in pygame.event.get():
        # check if quitting
        if event.type == pygame.QUIT:
            running = False
        #  check if pressing buttons
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change -= 5
            if event.key == pygame.K_RIGHT:
                playerX_change += 5
            if event.key == pygame.K_SPACE:
                if bullet1_state is "ready":
                    bulletSound = mixer.Sound("x_wing_blaster.wav")
                    bulletSound.play()
                    bullet1X = playerX
                    fire(bullet1X, bullet1Y)


        #  check if letting go of buttons
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0


    # boundary control
    playerX += playerX_change   # doesn't matter if add or subtract since it depends on the last operation
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # enemy movement
    for i in range(num_enemies):
        # Game Over
        if enemyY[i] > 440:
            for j in range(num_enemies):
                enemyY[j] = 2000
            gameOver()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bullet1X, bullet1Y)
        if collision:
            explosionSound = mixer.Sound("tiefighter_explosion.wav")
            explosionSound.play()
            bullet1Y = 480
            bullet1_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)    # spawns @ random spot once shot
            enemyY[i] = random.randint(30,60)
        enemy(enemyX[i], enemyY[i], i)


    # bullet movement
    if bullet1Y <= 0:
        bullet1Y = 480
        bullet1_state = "ready"

    if bullet1_state is "fire":
        fire(bullet1X, bullet1Y)
        bullet1Y -= bullet1Y_change


    player(playerX, playerY)
    showScore(textX, textY)
    pygame.display.update()
