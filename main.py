import pygame, sys, math
from pygame.locals import *
from classes import *

pygame.init()
root = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.key.set_repeat(10, 10)

# definition des objets
clock = pygame.time.Clock()
left_wall = Brick(0, 0, 10, HEIGHT, BLUE, math.inf)
right_wall = Brick(WIDTH-10, 0, 10, HEIGHT, BLUE, math.inf)
top_wall = Brick(0, 0, WIDTH, 10, BLUE, math.inf)
pad = Pad(150, 575, 100, 15, WHITE)
ball = Ball(root.get_width() // 2, root.get_height() // 2, 10, WHITE, vy=-1.2, vx=-1.8)

bricks = []
number_row = 6
for i in range(1, number_row):
    # attribution d'une couleur selon le niveau de la brique
    color = WHITE
    if number_row + 1 -i == 1:
        color = GREEN
    if number_row + 1 -i == 2:
        color = ORANGE
    if number_row + 1 -i == 3:
        color = PINK
    if number_row + 1 -i == 4:
        color = YELLOW
    if number_row + 1 -i == 5:
        color = BLUE
    if number_row + 1 -i == 6:
        color = RED

    # remplissage de briques
    hauteur = 30 * i
    bricks.append(Brick(30, hauteur, 40, 20, color, number_row + 1 -i))
    bricks.append(Brick(80, hauteur, 40, 20, color, number_row + 1 -i))
    bricks.append(Brick(130, hauteur, 40, 20, color, number_row + 1 -i))
    bricks.append(Brick(180, hauteur, 40, 20, color, number_row + 1 -i))
    bricks.append(Brick(230, hauteur, 40, 20, color, number_row + 1 -i))
    bricks.append(Brick(280, hauteur, 40, 20, color, number_row + 1 -i))
    bricks.append(Brick(330, hauteur, 40, 20, color, number_row + 1 -i))

def update():
    global done, ball

    # gestion des evenements (bouger la barre, quitter l'appli)
    for event in pygame.event.get():
        if event.type == QUIT: done = True
        if event.type == KEYDOWN:
            if event.key == K_RIGHT and pad.x < right_wall.x - pad.w:
                pad.x += 5
            if event.key == K_LEFT and pad.x > left_wall.w:
                pad.x -= 5

        #region a supprimer
            if event.key == K_UP:
                ball.speed += 0.2
            if event.key == K_DOWN:
                ball.speed -= 0.2
        if event.type == KEYUP and event.key == K_r:
            ball = Ball(root.get_width() // 2, root.get_height() // 2, 10, WHITE, vy=-1.2, vx=-1.8)
        #endregion

    # gestion du mouvement de la balle
    ball.update(left_wall, top_wall, right_wall, pad)

def draw():
    top_wall.draw(root)
    right_wall.draw(root)
    left_wall.draw(root)

    pad.draw(root)
    ball.draw(root)

    for brick in bricks:
        brick.draw(root)

done = False
while not done:
    root.fill(BLACK)
    update()
    draw()
    pygame.display.update()
    clock.tick(60) # permet de bloquer le framerate a 60 images par secondes

pygame.quit()
