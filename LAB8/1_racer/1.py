import pygame, sys                    
from pygame.locals import *           
import random, time                   


pygame.init()


FPS = 60                              # Количество кадров в секунду
FramePerSec = pygame.time.Clock()     # Объект таймера для управления FPS

#Цвета в формате RGB
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Размеры экрана и игровые переменные
SCREEN_WIDTH = 400                   # Ширина окна
SCREEN_HEIGHT = 600                  # Высота окна
SPEED = 5                            # Начальная скорость врагов и монет
SCORE = 0                            # Очки за увернувшихся врагов
COINS_COLLECTED = 0                  # Количество собранных монет

#Настройка шрифтов
font = pygame.font.SysFont("Verdana", 60)           # Большой шрифт (для Game Over)
font_small = pygame.font.SysFont("Verdana", 20)     # Маленький шрифт (для очков и монет)
game_over = font.render("Game Over", True, BLACK)   # Готовое изображение текста "Game Over"

#Загрузка фона
background = pygame.image.load("LAB8/1_racer/resources/AnimatedStreet.png")  # Фоновая картинка дороги

#Загрузка фоновой музыки и запуск
pygame.mixer.music.load("LAB8/1_racer/resources/background.wav")  # Загружаем музыку
pygame.mixer.music.play(-1)  # Воспроизводим бесконечно 

#Создание окна
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Устанавливаем размеры окна
DISPLAYSURF.fill(WHITE)                                               # Закрашиваем фон белым
pygame.display.set_caption("Game")                                    # Название окна

#Загрузка изображения монеты и изменение её размера
coin_image = pygame.image.load("LAB8/1_racer/resources/Coin.png")     # Загружаем изображение монеты
coin_image = pygame.transform.scale(coin_image, (50, 50))             # Изменяем размер на 50x50 пикселей

#Класс врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()  # Инициализация базового класса Sprite
        self.image = pygame.image.load("LAB8/1_racer/resources/Enemy.png")  # Картинка врага
        self.rect = self.image.get_rect()  # Границы объекта
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)  # Рандомная X-позиция сверху

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)  # Движение вниз со скоростью SPEED
        if self.rect.bottom > SCREEN_HEIGHT:  # Если враг вышел за экран
            SCORE += 1                        # Увеличить счёт
            self.rect.top = 0                 # Переместить обратно наверх
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

#Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("LAB8/1_racer/resources/Player.png")  # Картинка игрока
        self.rect = self.image.get_rect()# Получаем прямоугольник игрока
        self.rect.center = (160, 520)  # Начальная позиция внизу по центру

    def move(self):
        pressed_keys = pygame.key.get_pressed()  # Проверяем, какие клавиши нажаты

        # Движение влево
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:# Если нажата стрелка влево
                self.rect.move_ip(-5, 0) # Двигаем игрока влево

        # Движение вправо
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]: # Если нажата стрелка вправо
                self.rect.move_ip(5, 0) # Двигаем игрока вправо

#Класс монеты
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = coin_image # Устанавливаем изображение монеты
        self.rect = self.image.get_rect() # Получаем прямоугольник монеты
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0) # Случайная позиция по X, сверху

    def move(self):
        self.rect.move_ip(0, SPEED)  # Движение вниз
        if self.rect.bottom > SCREEN_HEIGHT:  # Если вышла за экран
            self.rect.top = 0 # Перемещаем наверх
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0) # Новая случайная позиция

#Создание объектов игрока, врага и монеты
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

#для увеличения скорости
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)  # Каждую 1 секунду будет приходить событие увеличения скорости

#Главный игровой цикл
while True:
    for event in pygame.event.get():          # Получение событий
        if event.type == INC_SPEED:           # Если пришло событие увеличения скорости
            SPEED += 0.5                      # Увеличиваем скорость
        if event.type == QUIT:                # Если игрок нажал на [X]
            pygame.quit()                     # Выход из Pygame
            sys.exit()                        # Завершение программы

    #Отрисовка фона
    DISPLAYSURF.blit(background, (0, 0))

    #Отображение очков 
    scores = font_small.render("Score: " + str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))

    # Отображение собранных монет
    coin_score = font_small.render("Coins: " + str(COINS_COLLECTED), True, BLACK)
    DISPLAYSURF.blit(coin_score, (SCREEN_WIDTH - 100, 10))

    #Движение всех объектов и их отображение
    for entity in all_sprites:
        entity.move() # Двигаем каждый объект
        DISPLAYSURF.blit(entity.image, entity.rect)  # Отображаем его

    #Проверка столкновения игрока с врагом
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.music.stop()  # Остановить фоновую музыку
        crash_sound = pygame.mixer.Sound("LAB8/1_racer/resources/crash.wav")  # Звук столкновения
        crash_sound.play()  # Воспроизведение
        time.sleep(1)       # Короткая пауза

        #Отображение Game Over
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()

        #Удаление всех объектов и завершение
        for entity in all_sprites:
            entity.kill()

        time.sleep(2)
        pygame.quit()
        sys.exit()

    #Проверка столкновения игрока с монетой
    if pygame.sprite.spritecollideany(P1, coins):
        COINS_COLLECTED += 1  # Увеличить количество монет
        C1.rect.top = 0       # Переместить монету наверх
        C1.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    #Обновление экрана и FPS
    pygame.display.update()
    FramePerSec.tick(FPS)
