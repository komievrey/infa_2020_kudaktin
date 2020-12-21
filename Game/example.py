# РРіСЂР° Shmup - 3 С‡Р°СЃС‚СЊ
# CС‚РѕР»РєРЅРѕРІРµРЅРёСЏ Рё СЃС‚СЂРµР»СЊР±Р°
import pygame
import random

WIDTH = 1920
HEIGHT = 1080
FPS = 60

# Р—Р°РґР°РµРј С†РІРµС‚Р°
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# РЎРѕР·РґР°РµРј РёРіСЂСѓ Рё РѕРєРЅРѕ
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # СѓР±РёС‚СЊ, РµСЃР»Рё РѕРЅ Р·Р°С…РѕРґРёС‚ Р·Р° РІРµСЂС…РЅСЋСЋ С‡Р°СЃС‚СЊ СЌРєСЂР°РЅР°
        if self.rect.bottom < 0:
            self.kill()

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

# Р¦РёРєР» РёРіСЂС‹
running = True
while running:
    # Р”РµСЂР¶РёРј С†РёРєР» РЅР° РїСЂР°РІРёР»СЊРЅРѕР№ СЃРєРѕСЂРѕСЃС‚Рё
    clock.tick(FPS)
    # Р’РІРѕРґ РїСЂРѕС†РµСЃСЃР° (СЃРѕР±С‹С‚РёСЏ)
    for event in pygame.event.get():
        # РїСЂРѕРІРµСЂРєР° РґР»СЏ Р·Р°РєСЂС‹С‚РёСЏ РѕРєРЅР°
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
            if event.key == pygame.K_ESCAPE:
                running = False


    # РћР±РЅРѕРІР»РµРЅРёРµ
    all_sprites.update()

    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

    # РџСЂРѕРІРµСЂРєР°, РЅРµ СѓРґР°СЂРёР» Р»Рё РјРѕР± РёРіСЂРѕРєР°
    hits = pygame.sprite.spritecollide(player, mobs, False)
    if hits:
        running = False

    # Р РµРЅРґРµСЂРёРЅРі
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # РџРѕСЃР»Рµ РѕС‚СЂРёСЃРѕРІРєРё РІСЃРµРіРѕ, РїРµСЂРµРІРѕСЂР°С‡РёРІР°РµРј СЌРєСЂР°РЅ
    pygame.display.flip()

pygame.quit()
