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

# Переменные для анимации заголовка в меню
menu_alpha = 255
title_offset = 0
title_dir = 1

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


# Функция для загрузки шрифта заданного размера
def load_font(size):

    font_path = os.path.join(FONT_DIR, "ui_font.ttf")

    return pygame.font.Font(font_path, size)

# Загрузка шрифтов разных размеров для интерфейса
title_font = load_font(56)
font = load_font(18)
small_font = load_font(10)
rules_font = load_font(13)

# Функция для отрисовки текста с простой тенью
def draw_ui_text(text, x, y, color):

    shadow = font.render(text, True, (0, 0, 0))
    screen.blit(shadow, (x + 2, y + 2))

    main = font.render(text, True, color)
    screen.blit(main, (x, y))

# Функция для отрисовки текста с полной обводкой вокруг букв
def draw_text_with_outline(text, font, x, y, text_color, outline_color=(0, 0, 0)):

    for dx in [-2, 0, 2]:
        for dy in [-2, 0, 2]:

            if dx != 0 or dy != 0:

                outline = font.render(text, True, outline_color)
                screen.blit(outline, (x + dx, y + dy))

    main_text = font.render(text, True, text_color)
    screen.blit(main_text, (x, y))


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


# Загрузка изображений фона
background = load_image("game_background.png", (WIDTH, HEIGHT))
menu_bg = load_image("menu_background.png", (WIDTH, HEIGHT))

# Загрузка изображений объектов
shelf_img = load_image("shelf.png", (720, 50))
pot_img = load_image("pot.png", (81, 74))

# Загрузка стадий роста растений (ростки и финальные формы)
sprout_1 = load_image("sprout_1.png")
sprout_2 = load_image("sprout_2.png")
sprout_3 = load_image("sprout_3.png")
final_plants = {
    1: load_image("plant_1.png", (80, 140)),
    2: load_image("plant_2.png", (81, 118)),
    3: load_image("plant_3.png", (83, 160)),
    4: load_image("plant_4.png", (87, 165)),
    5: load_image("plant_5.png", (90, 193)),
}

# Загрузка звуковых эффектов
water_sound = pygame.mixer.Sound(
    os.path.join(SOUND_DIR, "water.wav")
)

grow_sound = pygame.mixer.Sound(
    os.path.join(SOUND_DIR, "grow.wav")
)

collect_sound = pygame.mixer.Sound(
    os.path.join(SOUND_DIR, "collect.wav")
)

dead_sound = pygame.mixer.Sound(
    os.path.join(SOUND_DIR, "dead.wav")
)

click_sound = pygame.mixer.Sound(
    os.path.join(SOUND_DIR, "click.wav")
)
# Загрузка фоновой музыки
pygame.mixer.music.load(os.path.join(SOUND_DIR, "background_music.mp3"))
pygame.mixer.music.set_volume(0.3)

# Настройка громкости звуков
water_sound.set_volume(1)
grow_sound.set_volume(0.1)
collect_sound.set_volume(0.5)



# Загрузка изображений для кнопок интерфейса
start_button_img = load_image("start_button.png", (300, 90))
rules_button_img = load_image("start_button.png", (300, 90))

record_plate_img = load_image("start_button.png", (300, 90))


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
highscore = 0
sound_on = True  # По умолчанию звук включен
show_rules = False
game_state = "menu"


# Прямоугольники кнопки "Старт" и "Правила" в главном меню
start_button = pygame.Rect(
    WIDTH // 2 - 150,
    320,
    300,
    90
)
rules_menu_button = pygame.Rect(
    WIDTH // 2 - 150,
    429, 
    300, 
    90
)


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

        if self.stage == 1:
            return pygame.transform.smoothscale(sprout_1, (80, 100))

        if self.stage == 2:
            return pygame.transform.smoothscale(sprout_2, (80, 140))

        if self.stage == 3:
            return pygame.transform.smoothscale(sprout_3, (100, 180))

        if self.stage >= 4:
            return final_plants[self.level]


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

        shake_x = 0
        shake_y = 0

        # Небольшая случайная тряска для взрослого растения
        if self.stage >= 4:
            rect.x += random.randint(0, 1)

        rect = rect.copy()
        rect.x += shake_x
        rect.y += shake_y

        # Тряска, когда растение близко к засыханию
        if 0 < self.hydration < 15:
            rect.x += random.randint(-2, 2)

        screen.blit(img, rect)

        # Отрисовка шкалы влажности (hydration bar), если растение растет
        if self.stage > 0 and self.stage < 4:

            bar_x = rect.centerx - 30
            bar_y = rect.top - 14
            bar_w = 60
            bar_h = 8

            # Фон шкалы влажности
            pygame.draw.rect(
                screen,
                (30, 30, 30),
                (bar_x, bar_y, bar_w, bar_h),
                border_radius=4
            )

            # Синяя полоса заполнения (текущая влажность)
            water_width = int(max(0, self.hydration) / 100 * bar_w)

            pygame.draw.rect(
                screen,
                (80, 180, 255),
                (bar_x, bar_y, water_width, bar_h),
                border_radius=4
            )

            # Зеленая зона "идеального полива"
            perfect_start = int(bar_w * 0.2)
            perfect_end = int(bar_w * 0.4)

            if water_width > perfect_start:

                visible_width = min(water_width, perfect_end) - perfect_start

                if visible_width > 0:

                    pygame.draw.rect(
                        screen,
                        (0, 255, 120),
                        (
                            bar_x + perfect_start,
                            bar_y,
                            visible_width,
                            bar_h
                        ),
                        border_radius=4
                    )

            


    # Обновление состояния растения (потеря влажности со временем)
    def update(self):

        if self.stage > 0:

            self.hydration -= PLANTS[self.level]["speed"]

            if self.hydration <= 0:
                self.dead = True


    # Обработка клика по растению
    def click(self):

        global coins, score

        # Посадка семечка в пустой горшок, если хватает монет
        if self.stage == 0:

            price = PLANTS[selected_plant]["price"]

            if coins >= price:

                coins -= price

                self.level = selected_plant
                self.stage = 1
                self.hydration = 100

        # Сбор урожая взрослого растения (начисление наград)
        elif self.stage >= 4:

            coins += PLANTS[self.level]["reward"]
            score += self.level
            collect_sound.play()

            self.level = 0
            self.stage = 0
            self.hydration = 100

        # Полив растения во время роста
        else:

            # Идеальный полив (переход на следующую стадию роста)
            if 20 <= self.hydration <= 40:

                self.stage += 1
                water_sound.play()
                grow_sound.play()
                self.hydration = 100

            # Обычный полив (восстановление воды)
            else:
                self.hydration = 100
                water_sound.play()



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


# Инициализация кнопок магазина в нижней части экрана
shop_buttons = []

for i in range(5):

    rect = pygame.Rect(
        73 + i * 180,
        620,
        140,
        60
    )

    shop_buttons.append(rect)

# Прямоугольник для кнопки выхода в меню (справа сверху)
exit_button_rect = pygame.Rect(WIDTH - 130, 20, 70, 45)
# Кнопка звука (справа снизу)
mute_button_rect = pygame.Rect(WIDTH - 125, HEIGHT - 150, 50, 50)

# Главный игровой цикл
running = True
pygame.mixer.music.play(-1)
while running:

    clock.tick(FPS)


    # Обработка пользовательских событий
    for event in pygame.event.get():

        # Событие закрытия окна
        if event.type == pygame.QUIT:
            running = False

        # Обработка кликов мыши
        if event.type == pygame.MOUSEBUTTONDOWN:

            mx, my = pygame.mouse.get_pos()
            if show_rules:
                show_rules = False
                click_sound.play()
                continue

            # Логика кликов в главном меню
            if game_state == "menu":
        
                if start_button.collidepoint(mx, my):
                    click_sound.play()
                    game_state = "game"
                    

                    # Сброс прогресса для новой игры
                    score = 0
                    coins = 0

                    for p in plants:
                        p.level = 0
                        p.stage = 0
                        p.hydration = 100
                        p.dead = False
                
                elif rules_menu_button.collidepoint(mx, my):
                    click_sound.play()
                    show_rules = True


            # Логика кликов во время самого игрового процесса
            elif game_state == "game":
                # Проверка клика по кнопке "В МЕНЮ"
                if exit_button_rect.collidepoint(mx, my):
                    click_sound.play()
                    game_state = "menu"
                    continue # Прерываем текущую итерацию, чтобы клик не "прошиб" насквозь к горшку

                # Проверка клика по кнопкам магазина
                for i, btn in enumerate(shop_buttons):

                    if btn.collidepoint(mx, my):
                        click_sound.play()
                        selected_plant = i + 1

                # Проверка клика по растениям (полив/сбор/посадка)
                for p in plants:

                    if p.get_rect().collidepoint(mx, my):
                        p.click()
                # Проверка клика по кнопке звука
                if mute_button_rect.collidepoint(mx, my):
                    sound_on = not sound_on
                    volume = 1.0 if sound_on else 0.0
                    

                    water_sound.set_volume(volume)
                    grow_sound.set_volume(volume * 0.1)
                    collect_sound.set_volume(volume * 0.5)
                    dead_sound.set_volume(volume)
                    click_sound.set_volume(volume)
                    
                    #Управление фоновой музыкой ---
                    if sound_on:
                        pygame.mixer.music.set_volume(0.3) 
                        pygame.mixer.music.unpause()      
                    else:
                        pygame.mixer.music.set_volume(0)   
                        pygame.mixer.music.pause()         
                    
                    continue


            # Логика возврата из окна "Game Over" в меню
            elif game_state == "game_over":

                game_state = "menu"


    # Логика обновления игровых объектов, если игра активна
    if game_state == "game":

        for p in plants:

            p.update()

            # Обработка проигрыша при смерти растения
            if p.dead:

                if score > highscore:
                    highscore = score
                dead_sound.play()
                game_state = "game_over"

    # Отрисовка состояния "Главное меню"
    if game_state == "menu":

        # Отрисовка фона
        if menu_bg:
            screen.blit(menu_bg, (0, 0))
        else:
            screen.fill((30, 30, 30))

        # Затемняющий слой поверх фона
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(120)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        # Отрисовка заголовка
        draw_text_with_outline(
            "SOPHIA'S GARDEN",
            title_font,
            WIDTH // 10 - 30,
            150,
            WHITE,
            BLACK
        )


        # Отрисовка кнопки "Начать игру"
        if start_button_img:
            screen.blit(start_button_img, start_button.topleft)
        else:
            pygame.draw.rect(screen, (200, 80, 80), start_button)

        mouse = pygame.mouse.get_pos()
        hover = start_button.collidepoint(mouse)

        text_color = WHITE

        if hover:
            text_color = (220, 20, 60)

        draw_text_with_outline("НАЧАТЬ ИГРУ", font,start_button.centerx - 105, start_button.centery - 15, text_color)

        if start_button_img:
            screen.blit(start_button_img, rules_menu_button.topleft)
        
        # Определяем цвет текста при наведении
        rules_hover = rules_menu_button.collidepoint(pygame.mouse.get_pos())
        rules_text_color = (220, 20, 60) if rules_hover else WHITE
        
        draw_text_with_outline("ПРАВИЛА", font, 
                               rules_menu_button.centerx - 75, 
                               rules_menu_button.centery - 15, 
                               rules_text_color)
        


        # Отрисовка таблички с рекордом
        if record_plate_img:

            record_rect = record_plate_img.get_rect(
                center=(WIDTH // 2, 580)
            )

            screen.blit(record_plate_img, record_rect)

        else:

            record_rect = pygame.Rect(
                WIDTH // 2 - 150,
                470,
                300,
                90
            )

        draw_text_with_outline(f"РЕКОРД: {highscore}", font, record_rect.centerx - 105, record_rect.centery - 15, GOLD)


    # Отрисовка состояния "В игре"
    elif game_state == "game":

        # Отрисовка игрового фона
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill((60, 60, 60))

        # Отрисовка полок
        for y in shelf_y:

            if shelf_img:

                rect = shelf_img.get_rect(center=((WIDTH // 2) + 5, y))
                screen.blit(shelf_img, rect)

        # Отрисовка всех растений
        for p in plants:
            p.draw()

        # Отрисовка интерфейса пользователя (монеты, счет)
        draw_ui_text(f"Монеты: {coins}(С)", 270, 35, GOLD)
        draw_ui_text(f"Счёт: {score}", 580, 35, WHITE)



        # Отрисовка нижнего меню-магазина с кнопками
        for i, btn in enumerate(shop_buttons):

            level = i + 1

            color = (244, 164, 96)

            # Выделение выбранного растения
            if selected_plant == level:
                color = (139, 69, 19)

            mouse = pygame.mouse.get_pos()

            hover = btn.collidepoint(mouse)

            btn_color = color

            # Эффект наведения мыши
            if hover:
                btn_color = (160, 82, 45)

            # Тень кнопки
            pygame.draw.rect(
                screen,
                (20, 20, 20),
                btn.move(2, 2),
                border_radius=10
            )

            # Сама кнопка
            pygame.draw.rect(
                screen,
                btn_color,
                btn,
                border_radius=10
            )

            # Получение информации о растении для отрисовки текста на кнопке
            name = PLANTS[level]["name"]
            price = PLANTS[level]["price"]

            words = name.split(" ")

            y_offset = 6    

            for i, word in enumerate(words):
                txt = small_font.render(word, True, (0, 0, 0))
                screen.blit(txt, (btn.x + 12, btn.y + y_offset + i * 16))

            price_txt = small_font.render(f"{price}(C)", True, (139, 0, 0))
            screen.blit(price_txt, (btn.x + 50, btn.y + 37))

        # Отрисовка кнопки "В МЕНЮ"
        pygame.draw.rect(screen, (180, 60, 60), exit_button_rect, border_radius=100) # Темно-красный фон
        
        # Проверяем наведение мышки для эффекта подсветки
        if exit_button_rect.collidepoint(pygame.mouse.get_pos()):
             pygame.draw.rect(screen, (220, 80, 80), exit_button_rect, border_radius=10) # Светлее при наведении
        
        # Текст на кнопке
        exit_text = small_font.render("выход", True, BLACK)
        screen.blit(exit_text, (exit_button_rect.centerx - exit_text.get_width() // 2, 
                               exit_button_rect.centery - exit_text.get_height() // 2))
    
    # Отрисовка кнопки звука
        color = (100, 200, 100) if sound_on else (200, 100, 100) # Зеленый если ВКЛ, красный если ВЫКЛ
        pygame.draw.circle(screen, color, mute_button_rect.center, 25)
        pygame.draw.circle(screen, BLACK, mute_button_rect.center, 25, 2) # Ободок
        
        # Текстовая заглушка вместо иконки (можно заменить на картинку динамика)
        sound_label = "SND" if sound_on else "MUT"
        label_surf = small_font.render(sound_label, True, BLACK)
        screen.blit(label_surf, (mute_button_rect.centerx - label_surf.get_width() // 2, 
                                mute_button_rect.centery - label_surf.get_height() // 2))



    # Отрисовка состояния "Конец игры"
    elif game_state == "game_over":

        if background:
            screen.blit(background, (0, 0))

        # Сильное затемнение экрана
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        # Вывод надписи Game Over
        over = title_font.render("GAME OVER", True, WHITE)

        screen.blit(
            over,
            (WIDTH // 2 - over.get_width() // 2, 220)
        )

        # Вывод итогового счета
        sc = font.render(
            f"СЧЕТ: {score}",
            True,
            GOLD
        )

        screen.blit(
            sc,
            (WIDTH // 2 - sc.get_width() // 2, 330)
        )

        # Инструкция для продолжения
        click = small_font.render(
            "Нажмите мышкой чтобы вернуться",
            True,
            WHITE
        )

        screen.blit(
            click,
            (WIDTH // 2 - click.get_width() // 2, 420)
        )
        
    if show_rules:
        # 1. Затемняем весь экран (и меню, и игру)
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        # 2. Рисуем подложку окна
        rules_box = pygame.Rect(WIDTH // 2 - 300, HEIGHT // 2 - 200, 600, 400)
        pygame.draw.rect(screen, (50, 50, 50), rules_box, border_radius=20)
        pygame.draw.rect(screen, GOLD, rules_box, 3, border_radius=20)

        # 3. Пишем текст правил
        lines = [
            "ПРАВИЛА САДА",
            "все действия левой кнопкой мыши",
            "1. Выбирай семена, кликая на нужные снизу",
            "2. Сажай их в пустые горшки на полках,",
            "кликая на них.",
            "3. Поливай, кликая на горшок, когда шкала",
            "в ЗЕЛЕНОЙ, либо ГОЛУБОЙ зоне.",
            "4. Полив в ЗЕЛЕНОЙ зоне ускоряет рост.",
            "5. Не дай ни одному цветку засохнуть!",
            "",
            "",
            "Кликни в любом месте, чтобы закрыть."
        ]
        
        for i, line in enumerate(lines):
            # Заголовок золотой, остальное белое
            c = GOLD if i == 0 else WHITE
            # Используем font (размер 18), который у тебя уже создан
            txt = rules_font.render(line, True, c)
            screen.blit(txt, (rules_box.x + 40, rules_box.y + 50 + i * 35))
            
    # Обновление всего экрана
    pygame.display.flip()

# Корректное завершение программы
pygame.quit()
sys.exit()
