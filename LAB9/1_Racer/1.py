import pygame, sys                   
from pygame.locals import *         
import random, time                 

pygame.init()

#Запуск фоновой музыки
pygame.mixer.music.load("LAB8/1_racer/resources/background.wav")  # Загружаем фоновую музыку
pygame.mixer.music.play(-1)  # Воспроизводим бесконечно ()

#Настройка кадров в секунду
FPS = 60                                  # Количество кадров в секунду
FramePerSec = pygame.time.Clock()         # Объект для ограничения FPS

BLUE  = (0, 0, 255)                        # Синий
RED   = (255, 0, 0)                        # Красный
GREEN = (0, 255, 0)                        # Зелёный
BLACK = (0, 0, 0)                          # Чёрный
WHITE = (255, 255, 255)                   # Белый

SCREEN_WIDTH = 400                        # Ширина окна
SCREEN_HEIGHT = 600                       # Высота окна

#Переменные игры
SPEED = 5                                 # Начальная скорость врагов и монет
SCORE = 0                                 # Очки за пропущенных врагов
COINS_COLLECTED = 0                       # Счётчик монет
NEXT_SPEEDUP_THRESHOLD = 5               # Через сколько монет повышать скорость

#Шрифты
font = pygame.font.SysFont("Verdana", 60)             # Шрифт для "Game Over"
font_small = pygame.font.SysFont("Verdana", 20)       # Шрифт для очков и монет
game_over = font.render("Game Over", True, BLACK)      # Готовое изображение текста Game Over

#Загрузка фона
background = pygame.image.load("LAB8/1_racer/resources/AnimatedStreet.png")  # Фоновая картинка

#Настройка окна
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Установка окна
DISPLAYSURF.fill(WHITE)                       # Белый фон
pygame.display.set_caption("Game")            # Название окна

#Загрузка и масштабирование монеты
coin_image = pygame.image.load("LAB8/1_racer/resources/Coin.png")       # Загрузка картинки монеты
coin_image = pygame.transform.scale(coin_image, (50, 50))               # Изменение размера монеты

#Класс врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()                                                   # Инициализация Sprite
        self.image = pygame.image.load("LAB8/1_racer/resources/Enemy.png")  # Картинка врага
        self.rect = self.image.get_rect()                                   # Прямоугольник картинки
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)       # Случайная X-позиция сверху

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)                                         # Движение вниз
        if self.rect.bottom > 600:                                          # Если вышел за экран
            SCORE += 1                                                      # Добавляем очко
            self.rect.top = 0                                               
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)   # Случайное новое положение

#Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()                                                  # Инициализация Sprite
        self.image = pygame.image.load("LAB8/1_racer/resources/Player.png")  # Картинка игрока
        self.rect = self.image.get_rect()                                   # Прямоугольник игрока
        self.rect.center = (160, 520)                                       # Начальная позиция

    def move(self):
        pressed_keys = pygame.key.get_pressed()                             # Получаем нажатые клавиши
        if self.rect.left > 0 and pressed_keys[K_LEFT]:                     # Движение влево
            self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:       # Движение вправо
            self.rect.move_ip(5, 0)

#Класс монеты
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = coin_image                                             # Картинка монеты
        self.rect = self.image.get_rect()
        self.value = random.choice([1, 2, 3])                               # Случайная стоимость монеты
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)      # Случайное положение сверху

    def move(self):
        self.rect.move_ip(0, SPEED)                                        # Движение вниз
        if self.rect.bottom > 600:
            self.reset_position()                                          # Сброс при выходе за экран

    def reset_position(self):
        self.rect.top = 0                                                  # Переместить вверх
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)     # Случайное X
        self.value = random.choice([1, 2, 3])                              # Новое значение монеты

#Создание игровых объектов
P1 = Player()
E1 = Enemy()
C1 = Coin()

#Создание групп спрайтов
enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1, C1)

#Событие повышения скорости по времени
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)    # Каждую секунду увеличиваем скорость

#Главный игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5                         # Постепенное ускорение игры
        if event.type == QUIT:
            pygame.quit()                        # Закрытие окна
            sys.exit()

    DISPLAYSURF.blit(background, (0, 0))         # Отображаем фон

    #Отображение счёта и монет
    scores = font_small.render("Score: " + str(SCORE), True, BLACK)
    coins_text = font_small.render("Coins: " + str(COINS_COLLECTED), True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))
    DISPLAYSURF.blit(coins_text, (SCREEN_WIDTH - 120, 10))

    # Обработка движения объектов
    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)

    # Проверка столкновения с врагом
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.music.stop()                                       # Остановить музыку
        crash_sound = pygame.mixer.Sound("LAB8/1_racer/resources/crash.wav")  # Звук аварии
        crash_sound.play()                                              # Проиграть звук
        time.sleep(1)                                                   # Подождать

        DISPLAYSURF.fill(RED)                                           # Залить экран красным
        DISPLAYSURF.blit(game_over, (30, 250))                          # Отобразить текст
        pygame.display.update()

        for entity in all_sprites:
            entity.kill()                                               # Удалить объекты
        time.sleep(2)
        pygame.quit()
        sys.exit()

    #Проверка столкновения с монетой
    if pygame.sprite.spritecollideany(P1, coins):
        COINS_COLLECTED += C1.value             # Увеличить счётчик монет
        C1.reset_position()                     # Переместить монету

        if COINS_COLLECTED >= NEXT_SPEEDUP_THRESHOLD:
            SPEED += 0.3                         # Повысить скорость
            NEXT_SPEEDUP_THRESHOLD += 5         # Обновить порог

    pygame.display.update()                     # Обновить экран
    FramePerSec.tick(FPS)                       # Ограничение FPS
