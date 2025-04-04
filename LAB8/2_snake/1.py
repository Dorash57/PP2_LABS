import pygame                       
from color_paletta import *         
import random                       

pygame.init()

WIDTH = 600                         # Ширина окна в пикселях
HEIGHT = 600                        # Высота окна в пикселях
CELL = 30                           # Размер одной клетки сетки


screen = pygame.display.set_mode((WIDTH, HEIGHT))       # Устанавливаем размеры окна
pygame.display.set_caption("Snake with Levels and Wall Collision")  # Заголовок окна

#Функция для рисования обычной сетки
def draw_grid():
    for i in range(HEIGHT // CELL):                     # Проходим по вертикали
        for j in range(WIDTH // CELL):                  # Проходим по горизонтали
            pygame.draw.rect(screen, colorGRAY, (i * CELL, j * CELL, CELL, CELL), 1)  # Рисуем границу клетки


#Класс точки (используется для координат змеи и еды)
class Point:
    def __init__(self, x, y):
        self.x = x                                      # Положение по X
        self.y = y                                      # Положение по Y

    def __str__(self):
        return f"{self.x}, {self.y}"                    # Отображение точки в виде строки (5, 3)

#Класс змейки
class Snake:
    def __init__(self):
        self.body = [                                   # Список сегментов тела змеи (с головы до хвоста)
            Point(10, 11),
            Point(10, 12),
            Point(10, 13)
        ]
        self.dx = 1                                     # Направление по X (вправо)
        self.dy = 0                                     # Направление по Y (не двигается вверх/вниз)

    def move(self):
        # Двигаем тело от хвоста к голове
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x         # Каждому сегменту задаем позицию предыдущего
            self.body[i].y = self.body[i - 1].y

        # Двигаем голову змеи
        self.body[0].x += self.dx                       # Добавляем направление по X
        self.body[0].y += self.dy                       # Добавляем направление по Y

    def draw(self):
        head = self.body[0]                             # Получаем голову змеи
        pygame.draw.rect(screen, colorRED, (head.x * CELL, head.y * CELL, CELL, CELL))  # Рисуем голову
        for segment in self.body[1:]:                   # Рисуем оставшиеся сегменты тела
            pygame.draw.rect(screen, colorYELLOW, (segment.x * CELL, segment.y * CELL, CELL, CELL))

    def check_collision(self, food):
        global score, level, FPS                        # Используем глобальные переменные
        head = self.body[0]                             # Получаем голову змеи
        if head.x == food.pos.x and head.y == food.pos.y:  # Если координаты головы и еды совпадают
            print("Got food!")                          # Сообщаем, что еда съедена
            tail = self.body[-1]                        # Получаем хвост
            self.body.append(Point(tail.x, tail.y))     # Удлиняем змейку, добавляя сегмент на место хвоста
            score += 1                                  # Увеличиваем счёт

            if score % 4 == 0:                          # Каждые 4 очка — новый уровень
                level += 1                              # Увеличиваем уровень
                FPS += 2                                # Увеличиваем скорость игры

            food.generate_random_pos(self.body)         # Генерируем новую позицию еды

    def check_wall_collision(self):
        head = self.body[0]                             # Получаем голову
        return (
            head.x < 0 or                               # Вышел за левую границу
            head.x >= WIDTH // CELL or                  # Вышел за правую границу
            head.y < 0 or                               # Вышел за верхнюю границу
            head.y >= HEIGHT // CELL                    # Вышел за нижнюю границу
        )

    def check_self_collision(self):
        head = self.body[0]                             # Получаем голову
        for segment in self.body[1:]:                   # Проверяем каждое тело
            if head.x == segment.x and head.y == segment.y:
                return True                             # Столкнулся с собой
        return False                                    # Не столкнулся

#Класс еды
class Food:
    def __init__(self):
        self.pos = Point(9, 9)                          # Начальная позиция еды

    def draw(self):
        pygame.draw.rect(screen, colorGREEN, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))  # Рисуем еду

    def generate_random_pos(self, snake_body):
        while True:
            x = random.randint(0, WIDTH // CELL - 1)    # Случайный X
            y = random.randint(0, HEIGHT // CELL - 1)   # Случайный Y
            conflict = False                            # Флаг на совпадение с телом змеи
            for segment in snake_body:
                if segment.x == x and segment.y == y:
                    conflict = True                     # Найден конфликт — еда попала на змею
                    break
            if not conflict:
                self.pos = Point(x, y)                  # Задаём новую позицию
                break                                   # Выход из цикла

#Основные параметры игры
FPS = 5                                                # Начальная скорость (кадров в секунду)
clock = pygame.time.Clock()                            # Объект для ограничения FPS

#Создание объектов еды и змеи
food = Food()
snake = Snake()
food.generate_random_pos(snake.body)                   # Сразу задаём позицию еды

#Начальные значения очков и уровня
score = 0
level = 1
font = pygame.font.SysFont("Verdana", 20)              # Шрифт для текста

#Главный игровой цикл
running = True
while running:
    for event in pygame.event.get():                   # Обработка событий (клавиши, выход)
        if event.type == pygame.QUIT:                  # Кнопка [X] — закрыть окно
            running = False
        if event.type == pygame.KEYDOWN:               # Обработка клавиш
            if event.key == pygame.K_RIGHT and snake.dx != -1:  # Если нажата "вправо" и змея не идёт влево
                snake.dx = 1
                snake.dy = 0
            elif event.key == pygame.K_LEFT and snake.dx != 1:  # Влево
                snake.dx = -1
                snake.dy = 0
            elif event.key == pygame.K_DOWN and snake.dy != -1:  # Вниз
                snake.dx = 0
                snake.dy = 1
            elif event.key == pygame.K_UP and snake.dy != 1:     # Вверх
                snake.dx = 0
                snake.dy = -1

    screen.fill(colorBLACK)                          # Очистка экрана (фон чёрный)
    draw_grid()                                      # Отрисовка сетки

    snake.move()                                     # Перемещение змеи
    snake.check_collision(food)                      # Проверка, съедена ли еда

    #Проверка на проигрыш — столкновение со стеной или с собой
    if snake.check_wall_collision() or snake.check_self_collision():
        print("Game Over!")                          # Вывод в консоль
        running = False                              # Остановка игрового цикла

    snake.draw()                                     # Отрисовка змеи
    food.draw()                                      # Отрисовка еды

    # Отображение счёта и уровня на экране
    score_text = font.render(f"Score: {score}", True, colorWHITE)
    level_text = font.render(f"Level: {level}", True, colorWHITE)
    screen.blit(score_text, (10, 10))                # Отображение очков слева вверху
    screen.blit(level_text, (WIDTH - 110, 10))       # Отображение уровня справа вверху

    pygame.display.flip()                            # Обновляем весь экран
    clock.tick(FPS)                                  # Устанавливаем частоту обновления игры


pygame.quit()
