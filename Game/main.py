import pygame
from random import randint

pygame.init()

# Спрайты
name_game = pygame.image.load(r'name_game.png')
menu_background = pygame.image.load(r'bg_menu.jpg')
bg = pygame.image.load(r'background.jpg')
erythrocytes = [pygame.image.load(r'sprites/erythrocyte1.png'), pygame.image.load(r'sprites/erythrocyte2.png'),
                pygame.image.load(r'sprites/erythrocyte3.png'), pygame.image.load(r'sprites/erythrocyte4.png')]
green_virus = [pygame.image.load(r'sprites/green_virus1.png'), pygame.image.load(r'sprites/green_virus2.png')]
pink_virus = pygame.image.load(r'sprites/pink_virus.png')
black_virus = pygame.image.load(r'sprites/black_virus.png')
virus_boss = pygame.image.load(r'sprites/boss_virus.png')

# Звуки
music_count = 0
pygame.mixer.music.set_volume(0.5)
volume = 1
v_text = ['On', 'Off']
pos_on_button = pygame.mixer.Sound(r'sounds/pos_on_button.mp3')
click_on_button = pygame.mixer.Sound(r'sounds/click_on_button.mp3')
hit_virus = pygame.mixer.Sound(r'sounds/hit_virus.mp3')

# Настройки игры при входе
display_width = 1920
display_height = 1080
display = pygame.display.set_mode((display_width, display_height), pygame.FULLSCREEN)
pygame.display.set_caption('Hit this virus!')
logo = pygame.image.load(r'logo.png')
pygame.display.set_icon(logo)
resolution = "1920x1080"
R = 1
language = []


# Игровая механика
score = 0
x_spawn = 0
y_spawn = 0
random_scale = 500
A = 0

clock = pygame.time.Clock()


# Класс для создания кнопок (главное меню и др.)
class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_color = (11, 111, 122)
        self.active_color = (23, 189, 122)

    def draw(self, x, y, message=None, action=None, font_size=30):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(display, self.active_color, (x, y, int(self.width / R), int(self.height / R)))

            if click[0] == 1 and action is not None:
                pygame.mixer.Sound.play(click_on_button)
                pygame.time.delay(300)
                action()

        else:
            pygame.draw.rect(display, self.inactive_color, (x, y, int(self.width / R), int(self.height / R)))

        print_text(message=message, x=x, y=y-int(30 / R), font_size=font_size)


# Функция для печати текста
def print_text(message, x, y, font_color=(0, 0, 0), font_type=r'fonts/comicbd.ttf', font_size=int(30 / R)):
    font_type = pygame.font.Font(font_type, int(font_size / R))
    text = font_type.render(message, True, font_color)
    display.blit(text, (x, y))


# Главное меню
def show_menu():
    if music_count == 0:
        pygame.mixer.music.load(r'sounds/main_theme.mp3')
        pygame.mixer.music.play(-1)
    start_button = Button(240, 90)
    settings_button = Button(360, 90)
    quit_button = Button(195, 90)
    show = True

    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        display.blit(menu_background, (0, 0))
        display.blit(name_game, (30, 30))
        start_button.draw((display_width / 2) - (start_button.width / 2), (display_height / 3), 'Start', start_game, 90)
        settings_button.draw((display_width / 2) - (start_button.width / 2), (display_height / 2.25), 'Settings', settings_game, 90)
        quit_button.draw((display_width / 2) - (start_button.width / 2), (display_height / 1.8), 'Quit', quit, 90)
        pygame.display.update()
        clock.tick(60)


# Настройки игры
def settings_game():
    global music_count, resolution
    music_count = 1
    show = True
    esc_button = Button(175, 80)
    screen_button = Button(440, 65)
    volume_button = Button(140, 65)
    language_button = Button(270, 65)

    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    show_menu()

        display.blit(menu_background, (0, 0))
        print_text('Settings', (display_width / 2.95), (display_height / 13.5), font_size=150)

        print_text('Screen', (display_width / 3.76), (display_height / 2.8), font_size=90)
        screen_button.draw((display_width / 2), (display_height / 2.49), resolution, change_resolution, 80)

        print_text('Music', (display_width / 3.76), (display_height / 2), font_size=90)
        volume_button.draw((display_width / 2), (display_height / 1.85), v_text[0], change_sounds, 80)

        print_text('Language', (display_width / 3.76), (display_height / 1.55), font_size=90)
        language_button.draw((display_width / 2), (display_height / 1.46), 'English', show_menu, 80)

        esc_button.draw((display_width / 38.4), (display_height / 21.6), 'ESC', show_menu, 90)

        pygame.display.update()
        clock.tick(60)


# Изменение разрешения
def change_resolution():
    global display_width, display_height, resolution, display, bg, menu_background, R
    if resolution == "1920x1080":
        display_width = int(display_width / 1.5)
        display_height = int(display_height / 1.5)
        R = 1.5
        bg = pygame.transform.scale(bg, (1280, 720))
        menu_background = pygame.transform.scale(menu_background, (1280, 720))
        display = pygame.display.set_mode((display_width, display_height), pygame.FULLSCREEN)
        resolution = "1280x720"
    else:
        display_width = int(display_width * 1.5)
        display_height = int(display_height * 1.5)
        R = 1
        bg = pygame.transform.scale(bg, (1920, 1080))
        menu_background = pygame.transform.scale(menu_background, (1920, 1080))
        display = pygame.display.set_mode((display_width, display_height), pygame.FULLSCREEN)
        resolution = "1920x1080"


# Изменение звука
def change_sounds():
    global volume, v_text
    if volume == 1:
        pygame.mixer.music.set_volume(0)
        volume = 0
        v_text[0], v_text[1] = v_text[1], v_text[0]
    else:
        pygame.mixer.music.set_volume(0.4)
        volume = 1
        v_text[1], v_text[0] = v_text[0], v_text[1]


#
def translation():
    global language


# Спавн вирусов
def new_virus():
    global x_spawn, y_spawn, random_scale, A
    x_spawn = randint(100, display_width - 500)
    y_spawn = randint(100, display_height - 500)
    random_scale = int(randint(200, 400) / R)
    A = 100 * (random_scale / 500)
    pink_virus_scaled = pygame.transform.smoothscale(pink_virus, (random_scale, random_scale))
    black_virus_scaled = pygame.transform.smoothscale(black_virus, (random_scale, random_scale))
    green_virus_scaled = [green_virus[0], green_virus[1]]
    green_virus_scaled[0] = pygame.transform.smoothscale(green_virus[0], (random_scale, random_scale))
    green_virus_scaled[1] = pygame.transform.smoothscale(green_virus[1], (random_scale, random_scale))
    c = randint(-10, 3)
    if c > 0:
        display.blit(pink_virus_scaled, (x_spawn, y_spawn))
    elif c == 0:
        display.blit(black_virus_scaled, (x_spawn, y_spawn))
    else:
        display.blit(green_virus_scaled[randint(0, 1)], (x_spawn, y_spawn))


def hit():
    global score
    mouse = pygame.mouse.get_pos()
    if x_spawn + A < mouse[0] < x_spawn + A + random_scale - A*1.7 and y_spawn + A < mouse[1] < y_spawn + A + random_scale - A*1.7:
        pygame.mixer.Sound.play(hit_virus)
        display.blit(bg, (0, 0))
        new_virus()
        score += 1


# Функция для запуска основного цикла
def start_game():
    while game_cycle():
        pass


# Основной цикл игры
def game_cycle():
    global music_count, score
    running = True
    music_count = 0
    score = 0
    display.blit(bg, (0, 0))
    pygame.mixer.music.load('sounds/main_theme.mp3')
    new_virus()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    hit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    show_menu()

        print_text('Score:' + str(score), (display_width / 1.23), (display_height / 54), font_color=(255, 255, 255), font_size=70)
        pygame.display.update()
        clock.tick(60)


show_menu()
pygame.quit()
quit()
