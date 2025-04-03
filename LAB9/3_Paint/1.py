import pygame
import math

# Основная функция

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()

    radius = 15
    color = (0, 0, 255)  # Синий по умолчанию
    tool = 'free'  # Инструмент: 'free', 'circle', 'rect', 'eraser', 'square', 'right_triangle', 'equilateral_triangle', 'rhombus'
    points = []

    while True:
        pressed = pygame.key.get_pressed()
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_ESCAPE:
                    return

                # Переключение цвета
                if event.key == pygame.K_r:
                    color = (255, 0, 0)
                    tool = 'free'
                elif event.key == pygame.K_g:
                    color = (0, 255, 0)
                    tool = 'free'
                elif event.key == pygame.K_b:
                    color = (0, 0, 255)
                    tool = 'free'
                elif event.key == pygame.K_y:
                    color = (255, 255, 0)
                    tool = 'free'
                elif event.key == pygame.K_e:  # Ластик
                    color = (0, 0, 0)
                    tool = 'eraser'
                elif event.key == pygame.K_c:  # Круг
                    tool = 'circle'
                elif event.key == pygame.K_t:  # Прямоугольник
                    tool = 'rect'
                elif event.key == pygame.K_q:  # Квадрат
                    tool = 'square'
                elif event.key == pygame.K_w:  # Прямоугольный треугольник
                    tool = 'right_triangle'
                elif event.key == pygame.K_z:  # Равносторонний треугольник
                    tool = 'equilateral_triangle'
                elif event.key == pygame.K_v:  # Ромб
                    tool = 'rhombus'

            #Работа мыши
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    radius = min(200, radius + 1)
                elif event.button == 5:
                    radius = max(1, radius - 1)
                elif event.button == 1:
                    start_pos = event.pos
                    if tool == 'circle':
                        pygame.draw.circle(screen, color, start_pos, radius)
                    elif tool == 'rect':
                        pygame.draw.rect(screen, color, (*start_pos, radius * 2, radius))
                    elif tool == 'square':
                        draw_square(screen, start_pos, radius, color)
                    elif tool == 'right_triangle':
                        draw_right_triangle(screen, start_pos, radius, color)
                    elif tool == 'equilateral_triangle':
                        draw_equilateral_triangle(screen, start_pos, radius, color)
                    elif tool == 'rhombus':
                        draw_rhombus(screen, start_pos, radius, color)
                    else:
                        points.append(start_pos)
                        points = points[-256:]

            if event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
                position = event.pos
                if tool == 'free' or tool == 'eraser':
                    points.append(position)
                    points = points[-256:]

        # Отрисовка линий мыши
        i = 0
        while i < len(points) - 1:
            drawLineBetween(screen, i, points[i], points[i + 1], radius, color)
            i += 1

        pygame.display.flip()
        clock.tick(60)

#Рисование линии между двумя точками

def drawLineBetween(screen, index, start, end, width, color):
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))

    for i in range(iterations):
        progress = i / iterations
        aprogress = 1 - progress
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        pygame.draw.circle(screen, color, (x, y), width)

#Рисуем квадрат

def draw_square(screen, center, size, color):
    x, y = center
    side = size * 2
    pygame.draw.rect(screen, color, (x - size, y - size, side, side), 2)

#Рисуем прямоугольный треугольник

def draw_right_triangle(screen, center, size, color):
    x, y = center
    points = [(x, y), (x, y + size), (x + size, y + size)]
    pygame.draw.polygon(screen, color, points, 2)

#Рисуем равносторонний треугольник

def draw_equilateral_triangle(screen, center, size, color):
    x, y = center
    h = size * math.sqrt(3)
    points = [
        (x, y - h / 2),
        (x - size, y + h / 2),
        (x + size, y + h / 2)
    ]
    pygame.draw.polygon(screen, color, points, 2)

#Рисуем ромб

def draw_rhombus(screen, center, size, color):
    x, y = center
    points = [
        (x, y - size),
        (x + size, y),
        (x, y + size),
        (x - size, y)
    ]
    pygame.draw.polygon(screen, color, points, 2)

#Запускаем
main()
