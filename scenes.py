#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame, math, copy, random
from utils import *
from pygame.locals import *

class Scene(pygame.Surface):
    """ Permet de gérer l'affichage et l'interaction d'éléments dans un seul objet.
    La fonction 'update' renvoi un boolèen indiquant si le traitement doit s'arrêter"""
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

        # création des murs (gauche, haut, droite) pour stopper la balle et la barre
        self.walls = []
        self.walls.append(Brick(0, 0, 10, height, math.inf))
        self.walls.append(Brick(0, 0, width, 10, math.inf))
        self.walls.append(Brick(width-10, 0, 10, height, math.inf))

        self.pad = Pad((WIDTH/2 - 50), HEIGHT - 25, 100, 15, WHITE)
        vx = random.randint(-100, 100) / 100
        vy = random.randint(-100, 100) / 100
        self._ball = Ball(width // 2, height // 2, 10, WHITE, vx=vx, vy=vy)
        self.ball = copy.deepcopy(self._ball)

        # génération des briques qui seront visible dans le tableau
        self.bricks = []
        self.bricks = generation_bricks(12)

    def update(self, events):
        # gestion des événements (bouger la barre, modifier la vitesse de la balle)
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_RIGHT and self.pad.x < self.walls[2].x - self.pad.w:
                    self.pad.x += 5
                if event.key == K_LEFT and self.pad.x > self.walls[0].w:
                    self.pad.x -= 5
                if event.key == K_UP:
                    self.ball.speed += 0.2
                if event.key == K_DOWN:
                    self.ball.speed -= 0.2
            if event.type == KEYUP and event.key == K_r:
                self.ball = copy.deepcopy(self._ball) # reset de la balle

        # gestion du mouvement de la balle
        ## vérification collision (murs, barre et briques)
        for wall in self.walls:
            self.ball.rebound(*self.ball.collide(wall))

        self.ball.rebound(*self.ball.collide(self.pad))

        for brick in self.bricks:
            has_collide, collide_dir = self.ball.collide(brick)
            if has_collide:
                self.ball.rebound(has_collide, collide_dir)
                brick.hp -= 1 # on enlève 1 HP à chaque touche

        ## déplacement effectif de la ball
        self.ball.update()
        self.ball.move()

        # on récupère les briques ayant encore des PV
        self.bricks = [brick for brick in self.bricks if brick.hp > 0]

        return False

    def draw(self):
        self.fill(BLACK)

        for wall in self.walls:
            wall.draw(self)

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
        # vérifie si le son n'a pas déjà été joué
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
        self.music = pygame.mixer.Sound("fatality.ogg")
        self.once = True
        self.restart = False


    def update(self, events):
        # vérifie si le son n'a pas déjà été joué
        if not pygame.mixer.get_busy() and self.once:
            self.music.play()
            self.once = False

        for event in events:
            if not self.restart and event.type == KEYUP and event.key == K_RETURN:
                self.restart = True

    def draw(self):
        self.fill(RED)
        text_rect = self.text.get_rect()
        text_rect.center = (self.get_width() // 2, self.get_height() // 2)
        self.blit(self.text, text_rect)
