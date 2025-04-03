import pygame, sys
from pygame.locals import *
import random, time

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()


BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Размеры экрана
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Начальные параметры игры
SPEED = 5
SCORE = 0
COINS_COLLECTED = 0
NEXT_SPEEDUP_THRESHOLD = 5  # каждые 5 монет увеличиваем скорость

#Шрифты
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

#Фон
background = pygame.image.load("LAB8/1_racer/resources/AnimatedStreet.png")

# Экран
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

# Загружаем и масштабируем монету
coin_image = pygame.image.load("LAB8/1_racer/resources/Coin.png")
coin_image = pygame.transform.scale(coin_image, (50, 50))

# Класс врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("LAB8/1_racer/resources/Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.bottom > 600:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("LAB8/1_racer/resources/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

# Класс монеты
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = coin_image
        self.rect = self.image.get_rect()
        self.value = random.choice([1, 2, 3])  # вес монеты
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.bottom > 600:
            self.reset_position()

    def reset_position(self):
        self.rect.top = 0
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
        self.value = random.choice([1, 2, 3])  # новая случайная ценность

# Создаем игровые объекты
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Группы спрайтов
enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

# Увеличение скорости каждые 1 секунда (по времени)
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Главный цикл игры
while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5  # автоускорение (можно отключить)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Фон
    DISPLAYSURF.blit(background, (0, 0))

    # Отображение счёта и монет
    scores = font_small.render("Score: " + str(SCORE), True, BLACK)
    coins_text = font_small.render("Coins: " + str(COINS_COLLECTED), True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))
    DISPLAYSURF.blit(coins_text, (SCREEN_WIDTH - 120, 10))

    # Обработка всех объектов
    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)

    # Столкновение игрока с врагом — игра окончена
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('LAB8/1_racer/resources/crash.wav').play()
        time.sleep(1)

        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()

        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    # Столкновение игрока с монетой
    if pygame.sprite.spritecollideany(P1, coins):
        COINS_COLLECTED += C1.value
        C1.reset_position()

        # Увеличение скорости врага каждые 5 монет
        if COINS_COLLECTED >= NEXT_SPEEDUP_THRESHOLD:
            SPEED += 0.3
            NEXT_SPEEDUP_THRESHOLD += 5  

    # Обновление экрана
    pygame.display.update()
    FramePerSec.tick(FPS)
