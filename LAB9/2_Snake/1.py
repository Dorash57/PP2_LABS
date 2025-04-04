import pygame                           
from color_paletta import *            
import random                        
import time                              

pygame.init()                         

#Размеры поля и клеток
WIDTH = 600                            # Ширина окна
HEIGHT = 600                           # Высота окна
CELL = 30                              # Размер клетки

#Создаем окно
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Создаем экран для отображения
pygame.display.set_caption("Snake with Levels and Food Timer")  # Устанавливаем заголовок

#Функция сетки

def draw_grid():
    for i in range(HEIGHT // CELL):
        for j in range(WIDTH // CELL):
            pygame.draw.rect(screen, colorGRAY, (i * CELL, j * CELL, CELL, CELL), 1)  # Рисуем сетку


#Класс точки
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.x}, {self.y}"  # Строковое представление точки

#Класс змеи
class Snake:
    def __init__(self):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]  # Исходное тело
        self.dx = 1  # Движение по X (вправо)
        self.dy = 0  # Без движения по Y

    def move(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        self.body[0].x += self.dx  # Движение головы
        self.body[0].y += self.dy

    def draw(self):
        head = self.body[0]  # Голова
        pygame.draw.rect(screen, colorRED, (head.x * CELL, head.y * CELL, CELL, CELL))
        for segment in self.body[1:]:
            pygame.draw.rect(screen, colorYELLOW, (segment.x * CELL, segment.y * CELL, CELL, CELL))

    def check_collision(self, food):
        global score, level, FPS
        head = self.body[0]
        if head.x == food.pos.x and head.y == food.pos.y:  # Если змея нашла еду
            for _ in range(food.weight):  # Вес еды = сколько расти змейка
                tail = self.body[-1]
                self.body.append(Point(tail.x, tail.y))
            score += food.weight

            if score % 4 == 0:
                level += 1
                FPS += 2  # Увеличить скорость

            food.generate_random_pos(self.body)
            food.reset_timer()

    def check_wall_collision(self):
        head = self.body[0]
        return (
            head.x < 0 or head.x >= WIDTH // CELL or
            head.y < 0 or head.y >= HEIGHT // CELL
        )

    def check_self_collision(self):
        head = self.body[0]
        for segment in self.body[1:]:
            if head.x == segment.x and head.y == segment.y:
                return True
        return False

#Класс еды с таймером
class Food:
    def __init__(self):
        self.pos = Point(9, 9)
        self.weight = random.randint(1, 3)  # Вес еды (1-3)
        self.spawn_time = time.time()       # Время создания

    def draw(self):
        pygame.draw.rect(screen, colorGREEN, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))
        text = font.render(str(self.weight), True, colorWHITE)
        screen.blit(text, (self.pos.x * CELL + 5, self.pos.y * CELL + 2))

    def generate_random_pos(self, snake_body):
        while True:
            x = random.randint(0, WIDTH // CELL - 1)
            y = random.randint(0, HEIGHT // CELL - 1)
            conflict = False
            for segment in snake_body:
                if segment.x == x and segment.y == y:
                    conflict = True
                    break
            if not conflict:
                self.pos = Point(x, y)
                self.weight = random.randint(1, 3)
                self.spawn_time = time.time()
                break

    def reset_timer(self):
        self.spawn_time = time.time()

    def is_expired(self):
        return time.time() - self.spawn_time > 5  # Еда исчезает через 5 секунд

#Параметры игры
FPS = 5
clock = pygame.time.Clock()

food = Food()
snake = Snake()
food.generate_random_pos(snake.body)

score = 0
level = 1
font = pygame.font.SysFont("Verdana", 20)

#Главный цикл игры
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and snake.dx != -1:
                snake.dx = 1
                snake.dy = 0
            elif event.key == pygame.K_LEFT and snake.dx != 1:
                snake.dx = -1
                snake.dy = 0
            elif event.key == pygame.K_DOWN and snake.dy != -1:
                snake.dx = 0
                snake.dy = 1
            elif event.key == pygame.K_UP and snake.dy != 1:
                snake.dx = 0
                snake.dy = -1

    screen.fill(colorBLACK)
    draw_grid()

    snake.move()
    snake.check_collision(food)

    if snake.check_wall_collision() or snake.check_self_collision():
        print("Game Over!")
        running = False

    if food.is_expired():
        food.generate_random_pos(snake.body)

    snake.draw()
    food.draw()

    score_text = font.render(f"Score: {score}", True, colorWHITE)
    level_text = font.render(f"Level: {level}", True, colorWHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (WIDTH - 110, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
