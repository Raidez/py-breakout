#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame, math, copy, random
from pygame.locals import *
from utils import *

class Scene(pygame.Surface):
    """ Permet de gérer l'affichage et l'interaction d'éléments dans un seul objet.
    La fonction 'update' renvoi un boolèen indiquant si le traitement doit s'arrêter """
    def __init__(self, width: int, height: int):
        super().__init__((width, height))

    def update(self, delta: float, events: list) -> bool:
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

        self.pad = Pad((WIDTH/2 - 50), HEIGHT - 25, 100, 15, Color.WHITE)
        # self.pad = Pad(0, HEIGHT - 25, WIDTH, 15, Color.WHITE) # DEBUG: barre faisant toute la longueur de l'écran

        vx = lambda: random.randint(-20, 20) / 100
        vy = lambda: random.choice([-100, 100]) / 100
        self._ball = Ball(width // 2, height // 2, 10, Color.WHITE, vx=vx(), vy=vy(), speed=200.0) # conservation de la configuration initiale de la balle
        self.ball = copy.deepcopy(self._ball)

        # génération des briques qui seront visible dans le tableau
        self.bricks = generation_bricks(4)

        self.score = 0
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.text = self.font.render(f'Score : {self.score}', True, Color.WHITE, Color.RED)

    def update(self, delta, events):
        # gestion des événements (bouger la barre, modifier la vitesse de la balle)
        for event in events:
            if event.type == KEYDOWN:
                ## blocage de la barre sur le mur de gauche et de droite
                if event.key == K_RIGHT and self.pad.x < self.walls[2].x - self.pad.w: self.pad.x += 5
                if event.key == K_LEFT and self.pad.x > self.walls[0].w: self.pad.x -= 5

                ## contrôle de l'accélération de la balle
                if event.key == K_UP: self.ball.speed += 10.0
                if event.key == K_DOWN: self.ball.speed -= 10.0
            if event.type == KEYUP and event.key == K_r:
                del self.ball
                self.ball = copy.deepcopy(self._ball) # reset de la balle

        # gestion du mouvement de la balle
        ## vérification collision (murs, barre et briques)
        for wall in self.walls:
            self.ball.rebound(*self.ball.collide(wall, delta))

        ## changement de l'angle selon l'endroit toucher sur la barre
        has_collide, collide_dir = self.ball.collide(self.pad, delta)
        if has_collide:
            if "t" in collide_dir:
                ### on calcule le pourcentage sur lequel la balle touche et on applique le complément pour obtenir le nouveau vecteur
                percent = (self.ball.cx - self.pad.left) / (self.pad.right - self.pad.left)
                vx = -1.0 + percent * 2
                self.ball.vx = vx
                self.ball.rebound_vertical()
            else:
                self.ball.rebound(has_collide, collide_dir)

        for brick in self.bricks:
            has_collide, collide_dir = self.ball.collide(brick, delta)
            if has_collide:
                self.ball.rebound(has_collide, collide_dir)

                brick.hp -= 1 # on enlève 1 HP à chaque touche
                # if pygame.mixer.get_busy(): pygame.mixer.stop()
                # self.coin_sound.play()
                self.score += 10

        ## déplacement effectif de la ball
        self.ball.update(delta)
        self.ball.move()

        # on récupère les briques ayant encore des PV
        self.bricks = [brick for brick in self.bricks if brick.hp > 0]

        return False

    def draw(self):
        self.fill(Color.BLACK)

        for wall in self.walls:
            wall.draw(self)
        for brick in self.bricks:
            brick.draw(self)

        # on dessine la balle et la barre en dernier pour voir s'il y'a un soucis (balle qui traverse un élément)
        self.pad.draw(self)
        self.ball.draw(self)




# initialisation de la scène de victoire
class WinScene(Scene):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.music = pygame.mixer.Sound("sound/ff_victory.ogg")
        font = pygame.font.Font('freesansbold.ttf', 32)
        self.text = font.render('Winner', True, Color.BLACK, Color.WHITE)
        self.once = True
        self.restart = False

    def update(self, delta, events):
        # vérifie si le son n'a pas déjà été joué
        if not pygame.mixer.get_busy() and self.once:
            self.music.play()
            self.once = False

        for event in events:
            if not self.restart and event.type == KEYUP and event.key == K_RETURN:
                self.restart = True

    def draw(self):
        self.fill(Color.WHITE)
        text_rect = self.text.get_rect()
        text_rect.center = (self.get_width() // 2, self.get_height() // 2)
        self.blit(self.text, text_rect)

# initialisation de la scène de lose
class LoseScene(Scene):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.lives = 3
        self.music = pygame.mixer.Sound("sound/fatality.ogg")
        font = pygame.font.Font('freesansbold.ttf', 32)
        self.font2 = pygame.font.Font('freesansbold.ttf', 20)
        self.text = font.render('Lose', True, Color.WHITE, Color.RED)
        self.text2 = self.font2.render(f'Remain lives : {self.lives}', True, Color.WHITE, Color.RED)
        self.text3 = self.font2.render('Please exit the game', True, Color.WHITE, Color.RED)
        self.once = True
        self.restart = False

    def update(self, delta, events):
        # vérifie si le son n'a pas déjà été joué
        if not pygame.mixer.get_busy() and self.once:
            self.music.play()
            self.once = False

        for event in events:
            if not self.restart and event.type == KEYUP and event.key == K_RETURN:
                self.restart = True

    def draw(self):
        self.fill(Color.RED)
        text_rect = self.text.get_rect()
        text_rect2 = self.text2.get_rect()
        text_rect.center = (self.get_width() // 2, self.get_height() // 3)
        text_rect2.center = (self.get_width() // 2, self.get_height() // 2)
        self.blit(self.text, text_rect)
        self.blit(self.text2, text_rect2)

        if self.lives == 0:
            text_rect3 = self.text3.get_rect()
            text_rect3.center = (self.get_width() // 2, (self.get_height() // 3) * 2)
            self.blit(self.text3, text_rect3)

class ScoreScene(Scene):
    def __init__(self, width, height, game_scene):
        super().__init__(width, height)
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.text = self.font.render(f'Score : {game_scene.score}', True, Color.WHITE, Color.BLACK)

    def update_score(self, game_scene):
        self.text = self.font.render(f'Score : {game_scene.score}', True, Color.WHITE, Color.BLACK)

    def draw(self):
        # self.fill(Color.RED)
        text_rect = self.text.get_rect()
        text_rect.center = (self.get_width() // 2, self.get_height() // 2)
        text_rect.fit(self.get_rect())
        self.blit(self.text, text_rect)
