import pygame
import sys
import copy
import random
import time
import os
import sqlite3
import tkinter as tk
from tkinter import simpledialog, ttk, messagebox
import threading

pygame.init()

# Параметры игры
scale = 32
score = 0
level = 0
SPEED = 10
WIDTH = 640
HEIGHT = 640

# Графика
background_img = pygame.image.load("D:/PP2/lab9/background.png")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
apple_path = "D:/PP2/lab9"
apple_img = pygame.image.load(os.path.join(apple_path, "apple.png"))
gold_apple_img = pygame.image.load(os.path.join(apple_path, "apple_gold.png"))
apple_img = pygame.transform.scale(apple_img, (32, 32))
gold_apple_img = pygame.transform.scale(gold_apple_img, (32, 32))

display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Цвета
snake_colour = (255, 137, 0)
snake_head = (255, 247, 0)
font_colour = (255, 255, 255)
defeat_colour = (255, 0, 0)
button_colour = (30, 144, 255)
hover_colour = (70, 160, 255)

# БД
conn = sqlite3.connect("scorebook.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    score INTEGER DEFAULT 0,
    level INTEGER DEFAULT 0
)
""")
conn.commit()

# Получение пользователя
root = tk.Tk()
root.withdraw()
username = None
while not username:
    username = simpledialog.askstring("Login", "Enter your username:")
    if username is None:
        pygame.quit()
        sys.exit()

cursor.execute("SELECT * FROM users WHERE name = ?", (username,))
user = cursor.fetchone()
if not user:
    cursor.execute("INSERT INTO users (name, score, level) VALUES (?, 0, 0)", (username,))
    conn.commit()
    cursor.execute("SELECT * FROM users WHERE name = ?", (username,))
    user = cursor.fetchone()
user_id = user[0]

# Классы
class Snake:
    def __init__(self, x_start, y_start):
        self.x = int(x_start)
        self.y = int(y_start)
        self.w = scale
        self.h = scale
        self.x_dir = 1
        self.y_dir = 0
        self.history = [[self.x, self.y]]
        self.length = 1

    def show(self):
        for i in range(self.length):
            color = snake_colour if i != 0 else snake_head
            pygame.draw.rect(display, color, (self.history[i][0], self.history[i][1], self.w, self.h))

    def check_eaten(self, food):
        return abs(self.history[0][0] - food.x) < self.w and abs(self.history[0][1] - food.y) < self.h

    def grow(self):
        self.length += 1
        self.history.append(copy.deepcopy(self.history[-1]))

    def death(self):
        if self.length < 4:
            return False
        for i in range(4, self.length):
            if self.history[0] == self.history[i]:
                return True
        return False

    def update(self):
        for i in range(self.length - 1, 0, -1):
            self.history[i] = copy.deepcopy(self.history[i - 1])
        self.history[0][0] += self.x_dir * scale
        self.history[0][1] += self.y_dir * scale

class Food:
    def __init__(self):
        self.new_location()

    def new_location(self, snake_body=None):
        while True:
            self.x = random.randrange(0, WIDTH // scale) * scale
            self.y = random.randrange(0, HEIGHT // scale) * scale
            if not snake_body or [self.x, self.y] not in snake_body:
                break
        self.spawn_time = time.time()
        self.value = random.choice([1, 1, 1, 1, 3])
        self.image = apple_img if self.value == 1 else gold_apple_img

    def show(self):
        display.blit(self.image, (self.x, self.y))

    def is_expired(self):
        return time.time() - self.spawn_time > 10

# UI
def draw_text(text, size, color, x, y, center=True):
    font = pygame.font.SysFont(None, size)
    rendered = font.render(text, True, color)
    rect = rendered.get_rect()
    rect.center = (x, y) if center else (x, y)
    display.blit(rendered, rect)
    return rect

def draw_button(text, x, y, w, h):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    hovered = x < mouse[0] < x + w and y < mouse[1] < y + h
    color = hover_colour if hovered else button_colour
    pygame.draw.rect(display, color, (x, y, w, h), border_radius=10)
    draw_text(text, 30, (255, 255, 255), x + w // 2, y + h // 2)
    return hovered and click[0]

def show_score():
    draw_text("Score: " + str(score), 20, font_colour, scale, scale, center=False)

def show_level():
    draw_text("Level: " + str(level), 20, font_colour, 120, scale, center=False)

def game_over_screen():
    display.fill((30, 0, 0))
    draw_text("GAME OVER", 60, defeat_colour, WIDTH // 2, 180)
    draw_text("Press any key to return to menu", 30, font_colour, WIDTH // 2, 260)
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False

def save_progress():
    cursor.execute("UPDATE users SET score = ?, level = ? WHERE id = ?", (score, level, user_id))
    conn.commit()

# Таблица пользователей
def show_users_table():
    def refresh():
        for item in tree.get_children():
            tree.delete(item)
        cur.execute("SELECT id, name, score, level FROM users")
        for row in cur.fetchall():
            tree.insert("", tk.END, values=row)

    def add_user():
        name = entry_name.get().strip()
        try:
            score = int(entry_score.get())
            lvl = int(entry_level.get())
        except ValueError:
            messagebox.showwarning("Invalid", "Score and Level must be numbers!")
            return

        if name:
            try:
                cur.execute("INSERT INTO users (name, score, level) VALUES (?, ?, ?)", (name, score, lvl))
                conn_local.commit()
                refresh()
            except sqlite3.IntegrityError:
                messagebox.showerror("Ошибка", f"Пользователь '{name}' уже существует!")

    def delete_user():
        selected = tree.selection()
        if selected:
            item = tree.item(selected[0])
            user_id = item["values"][0]
            cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn_local.commit()
            refresh()
        else:
            messagebox.showwarning("Выбор", "Выберите пользователя для удаления")

    # --- GUI ---
    conn_local = sqlite3.connect("scorebook.db")
    cur = conn_local.cursor()

    window = tk.Tk()
    window.title("All Users")

    tree = ttk.Treeview(window, columns=("ID", "Name", "Score", "Level"), show="headings")
    for col in ("ID", "Name", "Score", "Level"):
        tree.heading(col, text=col)
    tree.pack(fill="both", expand=True)

    # Entry fields
    frm = tk.Frame(window)
    frm.pack(pady=5)

    tk.Label(frm, text="Name").grid(row=0, column=0)
    entry_name = tk.Entry(frm, width=15)
    entry_name.grid(row=0, column=1)

    tk.Label(frm, text="Score").grid(row=0, column=2)
    entry_score = tk.Entry(frm, width=5)
    entry_score.grid(row=0, column=3)

    tk.Label(frm, text="Level").grid(row=0, column=4)
    entry_level = tk.Entry(frm, width=5)
    entry_level.grid(row=0, column=5)

    # Buttons
    btns = tk.Frame(window)
    btns.pack(pady=5)

    tk.Button(btns, text="Add User", command=add_user).grid(row=0, column=0, padx=10)
    tk.Button(btns, text="Delete Selected", command=delete_user).grid(row=0, column=1, padx=10)
    tk.Button(btns, text="Refresh", command=refresh).grid(row=0, column=2, padx=10)

    refresh()
    window.mainloop()
    conn_local.close()

# Главное меню
def main_menu():
    while True:
        display.fill((10, 10, 30))
        draw_text("SNAKE GAME", 60, font_colour, WIDTH // 2, 150)
        if draw_button("Start Game", WIDTH // 2 - 100, 250, 200, 60):
            return
        if draw_button("Show Users", WIDTH // 2 - 100, 340, 200, 60):
            threading.Thread(target=show_users_table).start()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# Основной цикл игры
def game_loop():
    global score, level, SPEED
    score = 0
    level = 0
    SPEED = 8

    snake = Snake(WIDTH // 2, HEIGHT // 2)
    food = Food()
    food.new_location(snake.history)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_progress()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    save_progress()
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_UP and snake.y_dir != 1:
                    snake.x_dir = 0
                    snake.y_dir = -1
                elif event.key == pygame.K_DOWN and snake.y_dir != -1:
                    snake.x_dir = 0
                    snake.y_dir = 1
                elif event.key == pygame.K_LEFT and snake.x_dir != 1:
                    snake.x_dir = -1
                    snake.y_dir = 0
                elif event.key == pygame.K_RIGHT and snake.x_dir != -1:
                    snake.x_dir = 1
                    snake.y_dir = 0

        display.blit(background_img, (0, 0))
        snake.update()

        if snake.check_eaten(food):
            score += food.value
            snake.grow()
            food.new_location(snake.history)

        new_level = score // 10
        if new_level > level:
            level = new_level
            SPEED += 1

        if food.is_expired():
            food.new_location(snake.history)

        if snake.death() or not (0 <= snake.history[0][0] < WIDTH) or not (0 <= snake.history[0][1] < HEIGHT):
            save_progress()
            game_over_screen()
            return

        snake.show()
        food.show()
        show_score()
        show_level()
        pygame.display.update()
        clock.tick(SPEED)

# Запуск
while True:
    main_menu()
    game_loop()