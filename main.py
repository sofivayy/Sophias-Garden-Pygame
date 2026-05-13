# Импорт необходимых библиотек
import pygame
import sys
import os
import random

# Инициализация библиотеки Pygame и ее звукового модуля
pygame.init()
pygame.mixer.init()

# Определение путей к директориям с ресурсами игры
BASE_DIR = os.path.dirname(__file__)

IMAGE_DIR = os.path.join(BASE_DIR, "assets", "images")
SOUND_DIR = os.path.join(BASE_DIR, "assets", "sounds")
FONT_DIR = os.path.join(BASE_DIR, "assets", "fonts")

# Размеры окна и количество кадров в секунду
WIDTH = 1000
HEIGHT = 700

FPS = 60

# Создание окна игры и установка названия
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sophia's Garden")

# Часы для контроля частоты кадров
clock = pygame.time.Clock()

# Цветовые константы в формате RGB
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 70, 70)
CYAN = (80, 220, 255)
GOLD = (255, 210, 50)

# Функция для загрузки шрифта заданного размера
def load_font(size):
    # Путь будет работать, когда ты добавишь папку fonts
    font_path = os.path.join(FONT_DIR, "ui_font.ttf")
    try:
        return pygame.font.Font(font_path, size)
    except:
        return pygame.font.SysFont("Arial", size)

# Загрузка шрифтов разных размеров для интерфейса
font = load_font(18)
small_font = load_font(10)

# Характеристики всех доступных растений (название, цена, награда, скорость высыхания)
PLANTS = {
    1: {"name": "Ромашка", "price": 0, "reward": 5, "speed": 0.3},
    2: {"name": "Кактус", "price": 10, "reward": 0, "speed": 0.6},
    3: {"name": "Подсолнух", "price": 20, "reward": 0, "speed": 1.0},
    4: {"name": "Роза", "price": 30, "reward": 0, "speed": 1.5},
    5: {"name": "Золотая Орхидея", "price": 50, "reward": 0, "speed": 2.0},
}

# Текущее выбранное растение для посадки
selected_plant = 1

# Игровые переменные состояния
coins = 0
score = 0

# Функция для загрузки изображений
def load_image(filename, scale=None):
    path = os.path.join(IMAGE_DIR, filename)
    if not os.path.exists(path):
        return None
    image = pygame.image.load(path).convert_alpha()
    if scale:
        image = pygame.transform.smoothscale(image, scale)
    return image

pot_img = load_image("pot.png", (81, 74))

class Plant:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.level = 0
        self.stage = 0
        self.hydration = 100
        self.dead = False

    def get_image(self):
        return pot_img

    def draw(self):
        img = self.get_image()
        rect = img.get_rect(midbottom=(self.x, self.y))
        screen.blit(img, rect)

# Инициализация списка всех растений
plants = [Plant(x, y - 10) for y in [200, 390, 580] for x in [230, 500, 770]]

# Инициализация кнопок магазина в нижней части экрана
shop_buttons = [pygame.Rect(73 + i * 180, 620, 140, 60) for i in range(5)]

# Главный игровой цикл
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            # Проверка клика по кнопкам магазина
            for i, btn in enumerate(shop_buttons):
                if btn.collidepoint(mx, my):
                    selected_plant = i + 1

    screen.fill((60, 60, 60))
    
    # Отрисовка растений
    for p in plants:
        p.draw()

    # Отрисовка интерфейса магазина
    for i, btn in enumerate(shop_buttons):
        color = (139, 69, 19) if selected_plant == i + 1 else (244, 164, 96)
        pygame.draw.rect(screen, color, btn, border_radius=10)
        name_txt = small_font.render(PLANTS[i+1]["name"], True, BLACK)
        screen.blit(name_txt, (btn.x + 10, btn.y + 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
