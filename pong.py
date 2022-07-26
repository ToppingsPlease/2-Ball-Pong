
# up arrow key to move player paddle up
# down arrow key to move player down
# "r" key to restart

import pygame
from sys import exit
from random import randint

from classes import Player, Enemy, Ball


# calculates the distance between 2 points
def distance(a, b):
    c = (a ** 2 + b ** 2) ** (1 / 2)
    return c


# activates when both balls go off the left edge of the screen
def on_death():
    if balls[0].rect.right < 0 and balls[1].rect.right < 0:
        return False
    else:
        return True


# activates when the user restarts the game
def reset_balls():
    for ball in balls:
        ball.additional_speed = 0
        ball.rect.centerx, ball.rect.centery = 960, 540
        ball.dir_y = randint(-10, 11)
        if ball.specific_value == 1:
            ball.dir_x = 10
        else:
            ball.dir_x = -10
        ball.active = True


# turns off the physics for balls that leave the play-field
def correct_balls():
    if ball.rect.right < 0:
        ball.active = False


pygame.init()

screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()

pygame.display.set_caption('Pong')

pygame.time.get_ticks()

pygame.mouse.set_visible(False)

player = Player()

ball1 = Ball(helper_num=1)
ball2 = Ball(helper_num=2)
balls = (ball1, ball2)

# gives each ball its own unique value
num = 1
for ball in balls:
    ball.specific_value = num
    num += 1

enemy = Enemy(balls)

increase_speed_timer = pygame.USEREVENT + 0
pygame.time.set_timer(increase_speed_timer, 1500)

reset_speed_timer = True
game_active = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            exit()

        if event.type == increase_speed_timer:
            for ball in balls:
                ball.increase_speed()
                reset_speed_timer = True

    if game_active:
        screen.fill('black')
        screen.blit(player.image, player.rect)
        player.update()

        screen.blit(enemy.image, enemy.rect)
        enemy.update()

        for ball in balls:
            screen.blit(ball.image, ball.rect)
            ball.update(player, enemy)
            correct_balls()

        game_active = on_death()

        pygame.display.flip()

    else:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            reset_balls()
            player.rect.centery = 540
            reset_speed_timer = True
            game_active = True

    clock.tick(60)
