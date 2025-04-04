import pygame

#Главная функция, запускающая графический редактор
def main():
    pygame.init()  

    screen = pygame.display.set_mode((640, 480))  # Создаём окно 
    clock = pygame.time.Clock()  # Создаём таймер для ограничения FPS

    radius = 15  # Начальный радиус кисти
    color = (0, 0, 255)  # Начальный цвет (синий)
    tool = 'free'  # Текущий инструмент: 'free' (свободное рисование), 'circle', 'rect', 'eraser'
    points = []  # Список точек для рисования линий

    #Главный игровой цикл
    while True:
        pressed = pygame.key.get_pressed()  # Получаем список всех нажатых клавиш
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]  # Проверка, удерживается ли Alt
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]  # Проверка, удерживается ли Ctrl

        # Обработка всех событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Закрытие окна
                return

            if event.type == pygame.KEYDOWN:  # Нажатие клавиши
                if event.key == pygame.K_w and ctrl_held:  # Ctrl + W — выход
                    return
                if event.key == pygame.K_F4 and alt_held:  # Alt + F4 — выход
                    return
                if event.key == pygame.K_ESCAPE:  # ESC — выход
                    return

                #Переключение цвета и инструмента
                if event.key == pygame.K_r:  # Клавиша R — красный цвет
                    color = (255, 0, 0)
                    tool = 'free'
                elif event.key == pygame.K_g:  # G — зелёный
                    color = (0, 255, 0)
                    tool = 'free'
                elif event.key == pygame.K_b:  # B — синий
                    color = (0, 0, 255)
                    tool = 'free'
                elif event.key == pygame.K_y:  # Y — жёлтый
                    color = (255, 255, 0)
                    tool = 'free'
                elif event.key == pygame.K_e:  # E — ластик (рисует чёрным)
                    color = (0, 0, 0)
                    tool = 'eraser'
                elif event.key == pygame.K_c:  # C — инструмент "круг"
                    tool = 'circle'
                elif event.key == pygame.K_t:  # T — инструмент "прямоугольник"
                    tool = 'rect'

            #Обработка нажатий мыши
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Колесо мыши вверх — увеличить радиус
                    radius = min(200, radius + 1)
                elif event.button == 5:  # Колесо вниз — уменьшить радиус
                    radius = max(1, radius - 1)
                elif event.button == 1:  # Левая кнопка мыши
                    start_pos = event.pos  # Сохраняем координаты клика

                    #В зависимости от инструмента — разные действия
                    if tool == 'circle':  # Нарисовать круг
                        pygame.draw.circle(screen, color, start_pos, radius)
                    elif tool == 'rect':  # Нарисовать прямоугольник
                        pygame.draw.rect(screen, color, (*start_pos, radius * 2, radius * 2))
                    else:
                        # Если рисуем свободно — добавляем точку
                        points.append(start_pos)
                        points = points[-256:]  # Обрезаем список до последних 256 точек

            #Движение мыши с зажатой левой кнопкой (рисуем линии)
            if event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
                position = event.pos  # Текущая позиция мыши
                if tool == 'free' or tool == 'eraser':  # Только для этих инструментов
                    points.append(position)  # Добавляем точку
                    points = points[-256:]  # Храним не более 256 точек

        #Отрисовка линий между точками (сглаживание кисти)
        i = 0
        while i < len(points) - 1:
            drawLineBetween(screen, i, points[i], points[i + 1], radius, color)  # Рисуем линию между точками
            i += 1

        pygame.display.flip()  
        clock.tick(60)  # Ограничиваем до 60 кадров в секунду

#Функция сглаживания линии между двумя точками
def drawLineBetween(screen, index, start, end, width, color):
    dx = start[0] - end[0]  # Разница по X
    dy = start[1] - end[1]  # Разница по Y
    iterations = max(abs(dx), abs(dy))  # Определяем количество шагов

    for i in range(iterations):  # Рисуем точку на каждом шаге
        progress = i / iterations  # От 0 до 1
        aprogress = 1 - progress  # Обратный прогресс
        x = int(aprogress * start[0] + progress * end[0])  # Интерполяция координаты X
        y = int(aprogress * start[1] + progress * end[1])  # Интерполяция координаты Y
        pygame.draw.circle(screen, color, (x, y), width)  # Рисуем круг в промежуточной точке

main()
