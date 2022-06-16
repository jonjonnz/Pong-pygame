import pygame
from sys import exit
import random

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

clock = pygame.time.Clock()

screen_width = 1024
screen_height = 576
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

ball = pygame.Rect(screen_width / 2 - 20, screen_height / 2 - 20, 40, 40)
ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
player = pygame.Rect(screen_width - 30, screen_height / 2 - 70, 20, 140)
player_speed = 0
opponent = pygame.Rect(10, screen_height / 2 - 70, 20, 140)
opponent_speed = 10

background_color = pygame.Color('grey12')
light_grey = (150, 150, 150)

player_score = 0
opponent_score = 0
game_font = pygame.font.Font('freesansbold.ttf', 32)

score_time = 1

pong_sound = pygame.mixer.Sound('pong.ogg')
score_sound = pygame.mixer.Sound('score.ogg')


def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        pygame.mixer.Sound.play(pong_sound)
        ball_speed_y *= -1

    if ball.left <= 0:
        pygame.mixer.Sound.play(score_sound)
        player_score += 1
        score_time = pygame.time.get_ticks()
    if ball.right >= screen_width:
        pygame.mixer.Sound.play(score_sound)
        opponent_score += 1
        score_time = pygame.time.get_ticks()

    if ball.colliderect(player) and ball_speed_x > 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.right - player.left) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 10:
            ball_speed_y *= -1
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 10:
            ball_speed_y *= -1
    if ball.colliderect(opponent) and ball_speed_x < 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.left - opponent.right) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 10:
            ball_speed_y *= -1
        elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 10:
            ball_speed_y *= -1


def ball_restart():
    global ball_speed_x, ball_speed_y, score_time
    ball.center = (screen_width / 2, screen_height / 2)

    current_time = pygame.time.get_ticks()

    if current_time - score_time < 700:
        number = game_font.render('3', False, (255, 255, 255))
        screen.blit(number, (screen_width / 2 - 7, screen_height / 2 - 14))

    if 700 < current_time - score_time < 1400:
        number = game_font.render('2', False, (255, 255, 255))
        screen.blit(number, (screen_width / 2 - 7, screen_height / 2 - 14))

    if 1400 < current_time - score_time < 2100:
        number = game_font.render('1', False, (255, 255, 255))
        screen.blit(number, (screen_width / 2 - 7, screen_height / 2 - 14))

    if current_time - score_time < 2100:
        ball_speed_x, ball_speed_y = 0, 0
    else:
        ball_speed_y = 7 * random.choice((1, -1))
        ball_speed_x = 7 * random.choice((1, -1))
        score_time = None


def player_animation():
    player.y += player_speed

    if player.top <= 10:
        player.top = 10
    if player.bottom >= screen_height - 10:
        player.bottom = screen_height - 10


def opponent_animation():
    if opponent.top <= 10:
        opponent.top = 10
    if opponent.bottom >= screen_height - 10:
        opponent.bottom = screen_height - 10
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7
            if event.key == pygame.K_UP:
                player_speed -= 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            if event.key == pygame.K_UP:
                player_speed += 7

    ball_animation()
    player_animation()
    opponent_animation()

    screen.fill(background_color)
    pygame.draw.aaline(screen, (255, 255, 255), (screen_width / 2, 0), (screen_width / 2, screen_height))
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)

    player_text = game_font.render(f"{player_score}", False, (255, 255, 255))
    screen.blit(player_text, (screen_width / 2 + 20, 20))
    opponent_text = game_font.render(f"{opponent_score}", False, (255, 255, 255))
    screen.blit(opponent_text, (screen_width / 2 - 20 - 16, 20))

    if score_time:
        ball_restart()

    pygame.display.flip()
    clock.tick(120)
