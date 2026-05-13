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
GRAY = (120, 120, 120)
GOLD = (255, 210, 50)

# Функция для загрузки и опционального масштабирования изображений
def load_image(filename, scale=None):

    path = os.path.join(IMAGE_DIR, filename)

    if not os.path.exists(path):
        print("Нет файла:", path)
        return None

    image = pygame.image.load(path).convert_alpha()

    if scale:
        image = pygame.transform.smoothscale(image, scale)

    return image

# Загрузка изображений объектов
pot_img = load_image("pot.png", (81, 74))

# Класс, описывающий отдельное растение в горшке
class Plant:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.level = 0
        self.stage = 0

        self.hydration = 100

        self.dead = False


    # Метод получения нужной картинки в зависимости от стадии роста
    def get_image(self):

        if self.stage == 0:
            return pot_img
        # Остальные стадии будут добавлены при загрузке всех ассетов
        return pot_img


    # Метод получения физических границ (hitbox) растения
    def get_rect(self):

        img = self.get_image()
        rect = img.get_rect()

        rect.midbottom = (self.x, self.y)

        return rect


    # Отрисовка растения и интерфейса увлажнения
    def draw(self):

        img = self.get_image()
        rect = img.get_rect()
        rect.midbottom = (self.x, self.y)

        screen.blit(img, rect)


    # Обновление состояния растения (потеря влажности со временем)
    def update(self):

        if self.stage > 0:
            # Логика снижения влажности будет привязана к характеристикам в след. коммите
            self.hydration -= 0.5

            if self.hydration <= 0:
                self.dead = True

# Инициализация списка всех растений на игровом поле
plants = []

# Координаты полок и горшков на них
shelf_y = [200, 390, 580]
pot_x = [230, 500, 770]

# Размещение растений (горшков) по заданным координатам
for y in shelf_y:
    for x in pot_x:
        plants.append(
            Plant(x, y - 10)
        )

# Главный игровой цикл
running = True

while running:

    clock.tick(FPS)

    # Обработка пользовательских событий
    for event in pygame.event.get():

        # Событие закрытия окна
        if event.type == pygame.QUIT:
            running = False

    # Очистка экрана
    screen.fill(BLACK)
    
    # Отрисовка всех растений
    for p in plants:
        p.draw()

    # Обновление всего экрана
    pygame.display.flip()

# Корректное завершение программы
pygame.quit()
sys.exit()
