import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    
    radius = 15
    color = (0, 0, 255)  # default blue
    tool = 'free'  # current tool: 'free', 'circle', 'rect', 'eraser'
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

                # Цвета
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

            # Изменение радиуса
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # колесо вверх
                    radius = min(200, radius + 1)
                elif event.button == 5:  # колесо вниз
                    radius = max(1, radius - 1)
                elif event.button == 1:  # левая кнопка
                    start_pos = event.pos
                    if tool == 'circle':
                        pygame.draw.circle(screen, color, start_pos, radius)
                    elif tool == 'rect':
                        pygame.draw.rect(screen, color, (*start_pos, radius * 2, radius * 2))
                    else:
                        points.append(start_pos)
                        points = points[-256:]

            if event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
                position = event.pos
                if tool == 'free' or tool == 'eraser':
                    points.append(position)
                    points = points[-256:]

        # Отрисовка
        i = 0
        while i < len(points) - 1:
            drawLineBetween(screen, i, points[i], points[i + 1], radius, color)
            i += 1

        pygame.display.flip()
        clock.tick(60)

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

main()
