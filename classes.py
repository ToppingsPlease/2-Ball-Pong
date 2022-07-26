import pygame
from random import randint


class Player:
    def __init__(self):
        self.image = pygame.image.load('graphics/BluePaddle.PNG').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, .3)
        self.rect = self.image.get_rect(midleft=(25, 540))

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= 15
        elif keys[pygame.K_DOWN] and self.rect.bottom < 1080:
            self.rect.y += 15

    def update(self):
        self.player_input()


class Enemy:
    def __init__(self, balls):
        self.image = pygame.image.load('graphics/RedPaddle.PNG').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, .652)
        self.rect = self.image.get_rect(midright=(1895, 540))

        self.balls = balls

        self.ball_to_enemy = [0, 0]
        self.closest_ball = 0

    # finds the ball that's closest to the enemy paddle
    def check_distance(self):
        from pong import distance
        for ball in self.balls:
            if ball.specific_value == 1:
                self.ball_to_enemy[0] = distance(ball.rect.centerx, self.rect.centery)
            elif ball.specific_value == 2:
                self.ball_to_enemy[1] = distance(ball.rect.centerx, self.rect.centery)
            self.closest_ball = min(self.ball_to_enemy)

    # follows the closest ball
    def follow_ball(self):
        if self.ball_to_enemy.index(self.closest_ball) == 0:
            self.rect.centery = self.balls[1].rect.centery
        elif self.ball_to_enemy.index(self.closest_ball) == 1:
            self.rect.centery = self.balls[0].rect.centery

        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > 1080:
            self.rect.bottom = 1080

    def update(self):
        self.check_distance()
        self.follow_ball()


class Ball:
    def __init__(self, helper_num):
        self.image = pygame.image.load('graphics/ping-pong-ball.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, .1)
        self.rect = self.image.get_rect(center=(960, 540))

        self.helper_num = helper_num

        self.collision_hitsound = pygame.mixer.Sound('audio/hitsound.wav')
        self.collision_hitsound.set_volume(.1)

        self.additional_speed = 0

        self.active = True

        self.dir_y = randint(-10, 11)

        # first ball goes left; second ball goes right
        if self.helper_num == 1:
            self.dir_x = 10
        else:
            self.dir_x = -10

    def collisions(self, player, enemy):
        # non-paddle collisions
        if self.rect.top <= 0 or self.rect.bottom >= 1080:
            self.dir_y *= -1
            self.collision_hitsound.play()

        # paddle collisions
        if self.rect.colliderect(player.rect) or self.rect.colliderect(enemy.rect):
            self.collision_hitsound.play()

            self.dir_y = randint(-10, 11)
            if self.dir_y <= 0:
                self.dir_y -= self.additional_speed
            else:
                self.dir_y += self.additional_speed

            self.dir_x *= -1
            if self.rect.colliderect(player.rect):
                self.rect.left = player.rect.right + 1
                self.dir_x = randint(7, 11) + self.additional_speed

            elif self.rect.colliderect(enemy.rect):
                self.rect.right = enemy.rect.left - 1
                self.dir_x = randint(-10, -6) - self.additional_speed

    def motion(self):
        self.rect.x += self.dir_x
        self.rect.y += self.dir_y

    def increase_speed(self):
        self.additional_speed += .2

    def update(self, player, enemy):
        if self.active:
            self.collisions(player, enemy)
            self.motion()
        else:
            self.rect.right = -1
