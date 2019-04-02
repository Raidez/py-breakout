#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame, math
from utils import *
from pygame.locals import *

class Scene(pygame.Surface):
    def __init__(self, width, height):
        super().__init__((width, height))

    def update(self, events):
        return False

    def draw(self):
        pass

# initialisation de la scène de jeu
class GameScene(Scene):
    def __init__(self, width, height):
        super().__init__(width, height)

        self.left_wall = Brick(0, 0, 10, height, math.inf)
        self.right_wall = Brick(width-10, 0, 10, height, math.inf)
        self.top_wall = Brick(0, 0, width, 10, math.inf)

        self.pad = Pad(150, 575, 100, 15, WHITE)
        self.ball = Ball(width // 2, height // 2, 10, WHITE, vy=-1.2, vx=-1.8)

        self.bricks = []
        number_row = 2
        for i in range(1, number_row):
            # remplissage des briques
            height = 30 * i
            self.bricks.append(Brick(30, height, 40, 20, number_row + 1 -i))

    def update(self, events):
        # gestion des événements (bouger la barre, quitter l'appli)
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_RIGHT and self.pad.x < self.right_wall.x - self.pad.w:
                    self.pad.x += 5
                if event.key == K_LEFT and self.pad.x > self.left_wall.w:
                    self.pad.x -= 5
                if event.key == K_UP:
                    self.ball.speed += 0.2
                if event.key == K_DOWN:
                    self.ball.speed -= 0.2
            if event.type == KEYUP and event.key == K_r:
                self.ball = Ball(self.get_width() // 2, self.get_height() // 2, 10, WHITE, vy=-1.2, vx=-1.8)

        # gestion du mouvement de la balle
        self.ball.update(self.left_wall, self.top_wall, self.right_wall, self.pad)

        # on enlève 1 HP à chaque touche
        for index in self.ball.hitbox.collidelistall(self.bricks):
            self.ball.rebound_vertical()
            brick = self.bricks[index]
            brick.hp -= 1

            if brick.hp <= 0:
                del self.bricks[index]

        return False

    def draw(self):
        self.fill(BLACK)

        self.top_wall.draw(self)
        self.right_wall.draw(self)
        self.left_wall.draw(self)

        self.pad.draw(self)
        self.ball.draw(self)

        for brick in self.bricks:
            brick.draw(self)


# initialisation de la scène de victoire
class WinScene(Scene):
    def __init__(self, width, height):
        super().__init__(width, height)

        font = pygame.font.Font('freesansbold.ttf', 32)
        self.text = font.render('Winner', True, BLACK, WHITE)
        self.music = pygame.mixer.Sound("ff_victory.ogg")
        self.once = True

    def update(self, events):
        if not pygame.mixer.get_busy() and self.once:
            self.music.play()
            self.once = False

    def draw(self):
        self.fill(WHITE)
        text_rect = self.text.get_rect()
        text_rect.center = (self.get_width() // 2, self.get_height() // 2)
        self.blit(self.text, text_rect)

# initialisation de la scène de lose
class LoseScene(Scene):
    def __init__(self, width, height):
        super().__init__(width, height)

        font = pygame.font.Font('freesansbold.ttf', 32)
        self.text = font.render('Lose', True, WHITE, RED)

    def draw(self):
        self.fill(RED)
        text_rect = self.text.get_rect()
        text_rect.center = (self.get_width() // 2, self.get_height() // 2)
        self.blit(self.text, text_rect)
