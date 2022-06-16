import pygame
from sys import exit
import random

# Initialize Pygame
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()

# Game window
screen_width = 1024
screen_height = 576
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

# Variables
background_color = (0, 0, 0)
accent_color = (255, 255, 255)
game_font = pygame.font.Font('freesansbold.ttf', 28)
countdown_font = pygame.font.Font('freesansbold.ttf', 40)

pong_sound = pygame.mixer.Sound('pong.ogg')
score_sound = pygame.mixer.Sound('score.ogg')
middle_strip = pygame.Rect(screen_width / 2 - 2, 0, 4, screen_height)


class Block(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center=(x_pos, y_pos))


class Player(Block):
    def __init__(self, path, x_pos, y_pos, speed):
        super().__init__(path, x_pos, y_pos)
        self.speed = speed
        self.movement = 0

    def screen_constraint(self):
        if self.rect.top <= 10:
            self.rect.top = 10
        if self.rect.bottom >= screen_height - 10:
            self.rect.bottom = screen_height - 10

    def update(self, ball_group):
        self.rect.y += self.movement
        self.screen_constraint()


class Ball(Block):
    def __init__(self, path, x_pos, y_pos, speed_x, speed_y, paddles):
        super().__init__(path, x_pos, y_pos)
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.paddles = paddles
        self.active = False
        self.score_time = 0

    def update(self):
        if self.active:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            self.collisions()
        else:
            self.restart_counter()

    def collisions(self):
        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            pygame.mixer.Sound.play(pong_sound)
            self.speed_y *= -1

        if pygame.sprite.spritecollide(self, self.paddles, False):
            pygame.mixer.Sound.play(pong_sound)
            collision_paddle = pygame.sprite.spritecollide(self, self.paddles, False)[0].rect
            if abs(self.rect.right - collision_paddle.left) < 10 and self.speed_x > 0:
                self.speed_x *= -1
            if abs(self.rect.left - collision_paddle.right) < 10 and self.speed_x < 0:
                self.speed_x *= -1
            if abs(self.rect.top - collision_paddle.bottom) < 10 and self.speed_y < 0:
                self.rect.top = collision_paddle.bottom
                self.speed_y *= -1
            if abs(self.rect.bottom - collision_paddle.top) < 10 and self.speed_y > 0:
                self.rect.bottom = collision_paddle.top
                self.speed_x *= -1

    def reset_ball(self):
        self.active = False
        self.speed_x *= random.choice([1, -1])
        self.speed_y *= random.choice([1, -1])
        self.score_time = pygame.time.get_ticks()
        self.rect.center = (screen_width / 2, screen_height / 2)
        pygame.mixer.Sound.play(score_sound)

    def restart_counter(self):
        current_time = pygame.time.get_ticks()
        countdown_number = 3
        if current_time - self.score_time <= 700:
            countdown_number = 3
        elif 700 < current_time - self.score_time <= 1400:
            countdown_number = 2
        elif 1400 < current_time - self.score_time <= 2100:
            countdown_number = 1
        elif current_time - self.score_time >= 2100:
            self.active = True

        timer_counter = countdown_font.render(str(countdown_number), True, accent_color)
        timer_counter_rect = timer_counter.get_rect(center=(screen_width / 2, screen_height / 2))
        # pygame.draw.rect(screen, accent_color, timer_counter_rect)
        screen.blit(timer_counter, timer_counter_rect)


class Opponent(Block):
    def __init__(self, path, x_pos, y_pos, speed):
        super().__init__(path, x_pos, y_pos)
        self.speed = speed

    def update(self, ball_group):
        if self.rect.top < ball_group.sprite.rect.y:
            self.rect.y += self.speed
        if self.rect.bottom > ball_group.sprite.rect.y:
            self.rect.y -= self.speed
        self.screen_constraint()

    def screen_constraint(self):
        if self.rect.top <= 10:
            self.rect.top = 10
        if self.rect.bottom >= screen_height - 10:
            self.rect.bottom = screen_height - 10


class GameManager:
    def __init__(self, ball_group, paddles):
        self.player_score = 0
        self.opponent_score = 0
        self.ball_group = ball_group
        self.paddle_group = paddles

    def run_game(self):
        # Drawing the game objects
        self.paddle_group.draw(screen)
        self.ball_group.draw(screen)

        # Updating the game objects
        self.paddle_group.update(self.ball_group)
        self.ball_group.update()
        self.reset_ball()
        self.draw_score()

    def reset_ball(self):
        if self.ball_group.sprite.rect.right >= screen_width:
            self.opponent_score += 1
            self.ball_group.sprite.reset_ball()
        if self.ball_group.sprite.rect.left <= 0:
            self.player_score += 1
            self.ball_group.sprite.reset_ball()

    def draw_score(self):
        player_score = game_font.render(str(self.player_score), True, (0, 255, 30))
        opponent_score = game_font.render(str(self.opponent_score), True, (255, 0, 0))

        player_score_rect = player_score.get_rect(midleft=(screen_width / 2 + 40, 40))
        opponent_score_rect = opponent_score.get_rect(midright=(screen_width / 2 - 40, 40))

        screen.blit(player_score, player_score_rect)
        screen.blit(opponent_score, opponent_score_rect)


# Game Objects
player = Player('player.png', screen_width - 20, screen_height / 2, 5)
paddle_group = pygame.sprite.Group()
paddle_group.add(player)
player2 = Player('opponent.png', 20, screen_height / 2, 5)

opponent = Opponent('opponent.png', 20, screen_height / 2, 5)
paddle_group.add(player2)

ball = Ball('Ball.png', screen_width / 2, screen_height / 2, 4, 4, paddle_group)
ball_sprite = pygame.sprite.GroupSingle()
ball_sprite.add(ball)

game_manager = GameManager(ball_sprite, paddle_group)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player.movement += player.speed
            if event.key == pygame.K_UP:
                player.movement -= player.speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player.movement -= player.speed
            if event.key == pygame.K_UP:
                player.movement += player.speed

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                player2.movement += player.speed
            if event.key == pygame.K_w:
                player2.movement -= player.speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                player2.movement -= player.speed
            if event.key == pygame.K_w:
                player2.movement += player.speed
    screen.fill(background_color)
    pygame.draw.rect(screen, accent_color, middle_strip)

    game_manager.run_game()

    # Rendering
    pygame.display.flip()
    clock.tick(120)
