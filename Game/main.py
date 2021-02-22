from random import randint, choice

import pygame
import re
import tkinter

# from moviepy.editor import *

тут есть игра

pygame.init()

# Спрайты
name_game = pygame.image.load(r'name_game.png')
menu_background = pygame.image.load(r'bg_menu.jpg')
bg = pygame.image.load(r'background.jpg')
rec_list = pygame.image.load(r'records_list.png')
rec_list = pygame.transform.smoothscale(rec_list, (1200, 1200))
erythrocytes = [pygame.image.load(r'sprites/erythrocyte1.png'), pygame.image.load(r'sprites/erythrocyte2.png'),
                pygame.image.load(r'sprites/erythrocyte3.png'), pygame.image.load(r'sprites/erythrocyte4.png')]
green_virus = [pygame.image.load(r'sprites/green_virus1.png'), pygame.image.load(r'sprites/green_virus2.png')]
pink_virus = pygame.image.load(r'sprites/pink_virus.png')
black_virus = pygame.image.load(r'sprites/black_virus.png')
virus_boss = pygame.image.load(r'sprites/boss_virus.png')
leukocyte = pygame.image.load(r'sprites/leukocyte.png')
bonuses = [pygame.image.load(r'sprites/shield.png')]
animations = [[pygame.image.load(r'animations/shield/shield0.png'), pygame.image.load(r'animations/shield/shield1.png'),
               pygame.image.load(r'animations/shield/shield2.png'), pygame.image.load(r'animations/shield/shield3.png'),
               pygame.image.load(r'animations/shield/shield_hit0.png'),
               pygame.image.load(r'animations/shield/shield_hit1.png'),
               pygame.image.load(r'animations/shield/shield_hit2.png'),
               pygame.image.load(r'animations/shield/shield_hit3.png'),
               pygame.image.load(r'animations/shield/shield0_test.png')
               ]]

# Настройки игры при входе
start_settings = open('start_settings.txt', 'r', encoding='utf8')
start_count = re.split(r'[\n]', start_settings.read())
start_settings.close()
start_change = [start_count[0], start_count[1], start_count[2], start_count[3],
                start_count[4], start_count[5], start_count[6]]
root = tkinter.Tk()
root.withdraw()
display_width, display_height = root.winfo_screenwidth(), root.winfo_screenheight()
display = pygame.display.set_mode((display_width, display_height), pygame.FULLSCREEN)
pygame.display.set_caption('Hit this virus!')
logo = pygame.image.load(r'logo.png')
pygame.display.set_icon(logo)
resolution = str(display_width)+"x"+str(display_height)
R = 1920 / display_width
R2 = 1080 / display_height
R_Scale = 1920 / display_width
language_c = int(start_count[5])
resolution_c = int(start_count[6])
langOut = open('language.txt', 'r', encoding='utf8')
language = re.split(r'[\n=]', langOut.read())
recordsOut = open('records.txt', 'r', encoding='utf8')
records_temp = re.split(r'[\n=]', recordsOut.read())
records = [['Player', '0']]
if records_temp[-1] == "":
    del records_temp[-1]
if len(records_temp) > 1:
    for rec in range(0, len(records_temp), 2):
        records.append([records_temp[rec], records_temp[rec + 1]])
records.sort(key=lambda l: int(l[1]), reverse=True)
recordsOut.close()
recordsOut = open('records.txt', 'a+', encoding='utf8')

# Звуки
music_count = 0
volume = int(str(start_count[4]))
v_text = ['On', 'Off']
pos_on_button = pygame.mixer.Sound(r'sounds/pos_on_button.mp3')
click_on_button = pygame.mixer.Sound(r'sounds/click_on_button.mp3')
hit_virus = pygame.mixer.Sound(r'sounds/hit_virus.mp3')
hit_virus.set_volume(0.5)
if volume == 1:
    pygame.mixer.music.set_volume(0.5)
else:
    pygame.mixer.music.set_volume(0)
if volume == 1 and language_c == 0:
    v_text[0], v_text[1] = language[12], language[14]
else:
    v_text[0], v_text[1] = language[14], language[12]

# Игровая механика
<<<<<<< HEAD
total_score = 0
com = 0
colony = []
bonus = []
spawn_cordX = []
spawn_cordY = []
effect = 0
=======
score = 0
com = 0
colony = []
random_scale = 0
spawn_cordX = []
spawn_cordY = []
>>>>>>> a6fcb3823e17d6c1dfd179de9d0f7885775c403d
clock = pygame.time.Clock()
ticks = clock.get_fps()


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
            pygame.draw.rect(display, self.active_color, (x, y, int(self.width / R), int(self.height / R2)))

            if click[0] == 1 and action is not None:
                pygame.mixer.Sound.play(click_on_button)
                pygame.time.delay(300)
                action()

        else:
            pygame.draw.rect(display, self.inactive_color, (x, y, int(self.width / R), int(self.height / R2)))

        print_text(message=message, x=x, y=y - int(30 / R2), font_size=font_size)


# Класс для создания моба
class Virus:
    def __init__(self, X, Y, scale, color, speed, score, spec_effect):
        self.X = X
        self.Y = Y
        self.scale = scale
        self.color = color
        self.speed_x = speed
        self.speed_y = choice((-1, 1)) * randint(1, speed + 1)
        self.score = score
        self.spec_effect = spec_effect

    def get_x(self):
        return self.X

    def get_y(self):
        return self.Y

    def get_scale(self):
        return self.scale

    def get_score(self):
        return self.score

    def get_spec_effect(self):
        return self.spec_effect

    def spawn(self):
        display.blit(self.color, (self.X, self.Y))

    def move(self):
        global effect, total_score
        self.X -= self.speed_x
        self.Y -= self.speed_y
        if self.Y < 0 + self.speed_y:
            self.speed_y = -self.speed_y
        if self.Y > (display_height - self.scale) + self.speed_y:
            self.speed_y = -self.speed_y
        if self.X < -150:
            end_game()
        if self.X < 100 and effect != 0:
            total_score += self.score
            pygame.mixer.Sound.play(hit_virus)
            display.blit(bg, (0, 0))
            colony.remove(self)
            start_to_spawn()
            effect = 0

    def special(self):
        if self.spec_effect == 10:
            give_effect()


class Virus:
    def __init__(self, X, Y, scale):
        self.X = X
        self.Y = Y
        self.scale = scale
        self.pink_virus_scaled = pygame.transform.smoothscale(pink_virus, (self.scale, self.scale))
        self.black_virus_scaled = pygame.transform.smoothscale(black_virus, (self.scale, self.scale))
        self.green_virus_scaled = [green_virus[0], green_virus[1]]
        self.green_virus_scaled[0] = pygame.transform.smoothscale(green_virus[0], (self.scale, self.scale))
        self.green_virus_scaled[1] = pygame.transform.smoothscale(green_virus[1], (self.scale, self.scale))

    def get_x(self):
        return self.X

    def get_y(self):
        return self.Y

    def get_scale(self):
        return self.scale

    def spawn(self):
        c = randint(-10, 3)
        if c > 0:
            display.blit(self.pink_virus_scaled, (self.X, self.Y))
        elif c == 0:
            display.blit(self.black_virus_scaled, (self.X, self.Y))
        else:
            display.blit(self.green_virus_scaled[randint(0, 1)], (self.X, self.Y))


# Функция для печати текста
def print_text(message, x, y, font_color=(0, 0, 0), font_type=r'fonts/comicbd.ttf', font_size=int(30 / R_Scale)):
    font_type = pygame.font.Font(font_type, int(font_size / R_Scale))
    text = font_type.render(message, True, font_color)
    display.blit(text, (x, y))


class Nickname:
    def __init__(self, X, Y, count_min=None, count_max=None):
        self.X = X
        self.Y = Y
        self.count_min = count_min
        self.count_max = count_max
        self.letters = ["P", "l", "a", "y", "e", "r"]
        self.count = 0

    # Функция для печати текста пользователем
    def enter_letter(self, letter):

        if self.count_max - len(self.letters) == 0 and self.count_max is not None:
            return
        self.letters.append(letter)

    def del_letter(self):
        if len(self.letters) != 0:
            del self.letters[-1]
        else:
            return

    def show_text(self, font_color=(0, 0, 0), font_type=r'fonts/comicbd.ttf', font_size=int(30 / R_Scale)):
        font_type = pygame.font.Font(font_type, int(font_size / R_Scale))
        if self.count <= 15:
            text = font_type.render((''.join(self.letters) + "|"), True, font_color)
            display.blit(text, (self.X, self.Y))
            self.count += 1
        elif 15 < self.count <= 30:
            text = font_type.render(''.join(self.letters), True, font_color)
            display.blit(text, (self.X, self.Y))
            self.count += 1
            if self.count == 30:
                self.count = 0

    def get_nickname(self):
        return ''.join(self.letters)

    def get_min_count(self):
        return self.count_min

    def get_max_count(self):
        return self.count_max


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
        start_button.draw((display_width / 2) - (start_button.width / 2), (display_height / 3), language[0], start_game,
                          90)
        settings_button.draw((display_width / 2) - (start_button.width / 2), (display_height / 2.25), language[2],
                             settings_game, 90)
        quit_button.draw((display_width / 2) - (start_button.width / 2), (display_height / 1.8), language[4], exit_game,
                         90)
        pygame.display.update()
        clock.tick(60)


def exit_game():
    with open(r"start_settings.txt", "w") as file:
        for line in start_change:
            file.write(line + '\n')
    start_settings.close()
    langOut.close()
    recordsOut.close()
    quit()


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
        print_text(language[2], (display_width / 2.95), (display_height / 13.5), font_size=150)

        print_text(language[6], (display_width / 3.76), (display_height / 2.8), font_size=90)
        screen_button.draw((display_width / 2), (display_height / 2.49), resolution, change_resolution, 80)

        print_text(language[8], (display_width / 3.76), (display_height / 2), font_size=90)
        volume_button.draw((display_width / 2), (display_height / 1.85), v_text[0], change_sounds, 80)

        print_text(language[10], (display_width / 3.76), (display_height / 1.55), font_size=90)
        language_button.draw((display_width / 2), (display_height / 1.46), language[16], translation, 80)

        esc_button.draw((display_width / 38.4), (display_height / 21.6), 'ESC', show_menu, 90)

        pygame.display.update()
        clock.tick(60)


# Изменение разрешения
def change_resolution():
    global display_width, display_height, resolution, display, name_game,\
        bg, menu_background, R, R2, R_Scale, resolution_c, rec_list
    if resolution == "1920x1080":
        R = 1920 / 1280
        R2 = 1080 / 720
        R_Scale = 1920 / 1280
        display_width = int(display_width / R)
        display_height = int(display_height / R2)
        bg = pygame.transform.scale(bg, (1280, 720))
        name_game = pygame.transform.smoothscale(name_game, (int(980 / R), int(446 / R2)))
        menu_background = pygame.transform.scale(menu_background, (1280, 720))
        rec_list = pygame.transform.smoothscale(rec_list, (int(1100 / R), int(1100 / R2)))
        display = pygame.display.set_mode((display_width, display_height), pygame.FULLSCREEN)
        resolution = "1280x720"
        start_change[0] = "1280"
        start_change[1] = "720"
        start_change[2] = "1280x720"
        start_change[3] = "1.5"
    else:
        display_width = int(display_width * R)
        display_height = int(display_height * R2)
        R = 1920 / 1920
        R2 = 1080 / 1080
        R_Scale = 1920 / 1920
        bg = pygame.transform.scale(bg, (1920, 1080))
        name_game = pygame.transform.smoothscale(name_game, (int(980 / R), int(446 / R2)))
        menu_background = pygame.transform.scale(menu_background, (1920, 1080))
        display = pygame.display.set_mode((display_width, display_height), pygame.FULLSCREEN)
        resolution = "1920x1080"
        start_change[0] = "1920"
        start_change[1] = "1080"
        start_change[2] = "1920x1080"
        start_change[3] = "1"
    if resolution_c == 0:
        start_change[6] = "1"
        resolution_c = 1
    else:
        start_change[6] = "0"
        resolution_c = 0


# Изменение звука
def change_sounds():
    global volume, v_text
    if volume == 1:
        pygame.mixer.music.set_volume(0)
        volume = 0
        v_text[0], v_text[1] = v_text[1], v_text[0]
        start_change[4] = "0"
    else:
        pygame.mixer.music.set_volume(0.5)
        volume = 1
        v_text[1], v_text[0] = v_text[0], v_text[1]
        start_change[4] = "1"


# Изменение языка
def translation():
    global language, volume, language_c
    if volume == 1:
        v_text[0], v_text[1] = language[13], language[15]
    else:
        v_text[0], v_text[1] = language[15], language[13]
    for i in range(0, len(language) - 1, 2):
        language[i], language[i + 1] = language[i + 1], language[i]
<<<<<<< HEAD
    if language_c == 0:
        start_change[5] = "1"
        language_c = 1
    else:
        start_change[5] = "0"
        language_c = 0


def start_to_spawn():
    rand_bonus = randint(0, 5)
    shield_scaled = pygame.transform.smoothscale(bonuses[0], (150, 150))
    for _ in (range(3 - len(colony))):
        random_scale = int(randint(200, 300) / R_Scale)
        x_spawn = randint(int(1920 / R), int(2100 / R))
        y_spawn = randint(100, (int(780 / R2)))
        boss_virus_scaled = pygame.transform.smoothscale(virus_boss, (random_scale, random_scale))
        pink_virus_scaled = pygame.transform.smoothscale(pink_virus, (random_scale, random_scale))
        black_virus_scaled = pygame.transform.smoothscale(black_virus, (random_scale, random_scale))
        green_virus_scaled = [green_virus[0], green_virus[1]]
        green_virus_scaled[0] = pygame.transform.smoothscale(green_virus[0], (random_scale, random_scale))
        green_virus_scaled[1] = pygame.transform.smoothscale(green_virus[1], (random_scale, random_scale))
        rand_color = randint(-10, 3)
        if total_score == 50:
            color_v = boss_virus_scaled
            speed = 6
            score = 10
            spec_effect = 10
        elif rand_color > 0:
            color_v = pink_virus_scaled
            speed = 11
            score = 2
            spec_effect = 0
        elif rand_color == 0:
            color_v = black_virus_scaled
            speed = 5
            score = 1
            spec_effect = 0
        else:
            color_v = green_virus_scaled[randint(0, 1)]
            speed = 8
            score = 1
            spec_effect = 0
        colony.append(Virus(x_spawn, y_spawn, random_scale, color_v, speed, score, spec_effect))

    if rand_bonus == 1 and len(bonus) == 0:
        x_spawn = randint(int(820 / R), int(1700 / R))
        y_spawn = randint(100, (int(880 / R2)))
        bonus.append(Virus(x_spawn, y_spawn, scale=150, color=shield_scaled, speed=0, score=0, spec_effect=10))
    elif rand_bonus == 0 and len(bonus) == 1:
        bonus.pop()
=======

'''
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
'''


def rino():
    for i in range(3):
        random_scale = randint(200, 400)
        x_spawn = randint(100, 1620)
        y_spawn = randint(100, 780)
        colony.append(Virus(x_spawn, y_spawn, random_scale))
>>>>>>> a6fcb3823e17d6c1dfd179de9d0f7885775c403d


# Удар по вирусу
def hit():
<<<<<<< HEAD
    global total_score
    for i in range(len(colony)):
        mouse = pygame.mouse.get_pos()

        if (colony[i].get_x() + (60 // (300 / colony[i].get_scale()))) < mouse[0] \
                < colony[i].get_x() + (colony[i].get_scale() - (60 // (300 / colony[i].get_scale()))) and \
                (colony[i].get_y() + (60 // (300 / colony[i].get_scale()))) < mouse[1] \
                < colony[i].get_y() + (colony[i].get_scale() - (60 // (300 / colony[i].get_scale()))):
            total_score += colony[i].get_score()
            pygame.mixer.Sound.play(hit_virus)
            colony[i].special()
            display.blit(bg, (0, 0))
            colony.remove(colony[i])
            start_to_spawn()

    for i in range(len(bonus)):
        mouse = pygame.mouse.get_pos()

        if (bonus[i].get_x() + (10 // (300 / bonus[i].get_scale()))) < mouse[0] \
                < bonus[i].get_x() + (bonus[i].get_scale() - (10 // (300 / bonus[i].get_scale()))) and \
                (bonus[i].get_y() + (10 // (300 / bonus[i].get_scale()))) < mouse[1] \
                < bonus[i].get_y() + (bonus[i].get_scale() - (10 // (300 / bonus[i].get_scale()))):
            pygame.mixer.Sound.play(hit_virus)
            bonus[i].special()
            display.blit(bg, (0, 0))
            bonus.remove(bonus[i])


def give_effect():
    global effect
    effect = 1
=======
    global score
    for i in range(len(colony)):
        mouse = pygame.mouse.get_pos()

        if colony[i].get_x() < mouse[0] < colony[i].get_x() + colony[i].get_scale() and \
                colony[i].get_y() < mouse[1] < colony[i].get_y() + colony[i].get_scale():
            pygame.mixer.Sound.play(hit_virus)
            display.blit(bg, (0, 0))
            colony.remove(colony[i])
            random_scale = randint(200, 400)
            x_spawn = randint(100, 1620)
            y_spawn = randint(100, 780)
            colony.append(Virus(x_spawn, y_spawn, random_scale))
            for virus in colony:
                virus.spawn()
            score += 1
>>>>>>> a6fcb3823e17d6c1dfd179de9d0f7885775c403d


# Функция для запуска основного цикла
def start_game():
    while game_cycle():
        pass


def end_game():
    result_but = Button(406, 75)
    show = True
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    colony.clear()
                    bonus.clear()

                    show_menu()
        pygame.draw.rect(display, (100, 200, 100), (display_width - 1620, display_height - 880, 1320, 450))
        print_text(language[20], display_width // 3, display_height // 6, font_color=(0, 0, 0), font_size=150)
        print_text(language[22], display_width // 3.8, display_height // 3, font_color=(0, 0, 0),
                   font_size=60)
        result_but.draw(display_width // 2 - 203, display_height // 2, language[24], print_result, font_size=85)
        pygame.display.update()
        clock.tick(0)


def print_result():
    show = True
    letter_name = Nickname(display_width // 2.55, display_height // 1.29, count_min=3, count_max=13)
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.__dict__.get('unicode') != "":
                    letter_name.enter_letter(event.__dict__.get('unicode'))
                if event.key == pygame.K_ESCAPE:
                    colony.clear()
                    bonus.clear()
                    show_menu()
                if event.key == pygame.K_RETURN:
                    recordsOut.write('\n' + str(str(''.join(letter_name.get_nickname())) + "=" + str(total_score)))
                    records.append([letter_name.get_nickname(), str(total_score)])
                    records.sort(key=lambda l: int(l[1]), reverse=True)

        display.blit(bg, (0, 0))
        display.blit(rec_list, ((display_width // 2) - (600 // R), 0 - (55 // R)))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_BACKSPACE]:
            pygame.time.delay(100)
            letter_name.del_letter()
        print_text(language[24], display_width // 2.4, display_height // 17, font_color=(0, 0, 0), font_size=70)
        print_text(language[26], display_width // 2.4, display_height // 1.4, font_color=(0, 0, 0), font_size=40)
        if len(records) < 10:
            for i in range(0, 10):
                print_text(str(i + 1) + ".", display_width // 3.1, display_height // 4.5 + (45 * i), font_size=50)
                print_text((records[i][0]), display_width // 2.7, display_height // 4.5 + (45 * i), font_size=50)
                print_text(records[i][1], display_width // 1.6, display_height // 4.5 + (45 * i), font_size=50)
        else:
            for i in range(0, 10):
                print_text(str(i + 1) + ".", display_width // 3.1, display_height // 4.5 + (45 * i), font_size=50)
                print_text((records[i][0]), display_width // 2.7, display_height // 4.5 + (45 * i), font_size=50)
                print_text(records[i][1], display_width // 1.6, display_height // 4.5 + (45 * i), font_size=50)
        letter_name.show_text(font_size=50)
        pygame.display.update()
        clock.tick(60)


'''
def loading_screen():
    clip = VideoFileClip('Welcome.mpg')
    clip = clip.volumex(0.1)
    clip.preview(fps=30)
    show_menu()
'''


# Основной цикл игры
def game_cycle():
    global music_count, total_score
    running = True
    music_count = 0
    total_score = 0
    display.blit(bg, (0, 0))
    pygame.mixer.music.load('sounds/main_theme.mp3')
<<<<<<< HEAD
    start_to_spawn()
=======
    rino()
    for v in colony:
        v.spawn()
>>>>>>> a6fcb3823e17d6c1dfd179de9d0f7885775c403d
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
                    colony.clear()
<<<<<<< HEAD
                    bonus.clear()
=======
>>>>>>> a6fcb3823e17d6c1dfd179de9d0f7885775c403d
                    show_menu()

        for virus in colony:
            virus.move()
        display.blit(bg, (0, 0))
        for virus in colony:
            virus.spawn()
        for element in bonus:
            element.spawn()
        if effect != 0:
            display.blit(animations[0][8], (0, 0))

        print_text((language[18] + ': ') + str(total_score), (display_width / 1.23),
                   (display_height / 54), font_color=(255, 255, 255), font_size=70)
        print_text('FPS: ' + str(ticks), 50,
                   (display_height / 54), font_color=(255, 255, 255), font_size=70)
        pygame.display.update()
        clock.tick(60)


if language_c == 1:
    language_c = 0
    translation()
if resolution_c == 1:
    resolution_c = 0
    change_resolution()
show_menu()
pygame.quit()
quit()
