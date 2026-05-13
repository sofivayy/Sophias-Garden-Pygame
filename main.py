# Импорт необходимых библиотек
import pygame
import sys
import os
import random

# Инициализация библиотеки Pygame и ее звукового модуля
pygame.init()
pygame.mixer.init()

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

    # Обновление всего экрана
    pygame.display.flip()

# Корректное завершение программы
pygame.quit()
sys.exit()
