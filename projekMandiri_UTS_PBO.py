import pygame
import random
import sys

pygame.init()

WIDTH = 600
HEIGHT = 400

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Hindari Musuh")

WHITE = (255,255,255)
BLUE = (18,29,68)
PINK = (247,154,139)
BLACK = (0,0,0)

font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 72)
countdown_font = pygame.font.SysFont(None, 120)

try:
    GAMBAR_BG = pygame.image.load("background.png").convert()
    GAMBAR_BG = pygame.transform.scale(GAMBAR_BG, (WIDTH, HEIGHT))

    GAMBAR_PLAYER = pygame.image.load("player.png").convert_alpha()
    GAMBAR_PLAYER = pygame.transform.scale(GAMBAR_PLAYER, (130, 130))

    GAMBAR_MUSUH = pygame.image.load("musuh.png").convert_alpha()
    GAMBAR_MUSUH = pygame.transform.scale(GAMBAR_MUSUH, (130, 130))

except Exception as e:
    print("Beberapa aset gambar tidak ditemukan!")
    print(e)

    GAMBAR_BG = None
    GAMBAR_PLAYER = None
    GAMBAR_MUSUH = None

class Character:

    def __init__(self, x, y, size, color):
        self.x = x
        self.y = y
        self.width = size
        self.height = size
        self.speed = 5
        self.color = color

    def draw(self, surface, gambar=None):
        if gambar:
            surface.blit(gambar, (self.x, self.y))
        else:
            pygame.draw.rect(surface, self.color,
                             (self.x, self.y, self.width, self.height))

    def get_rect(self):
        return pygame.Rect(
            self.x + 30,
            self.y + 30,
            self.width - 60,
            self.height - 60
        )


class Player(Character):

    def move(self):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed

        if keys[pygame.K_RIGHT]:
            self.x += self.speed


    def batas(self):
        if self.x < 0:
            self.x = 0
        if self.x + self.width > WIDTH:
            self.x = WIDTH - self.width

        if self.y < 0:
            self.y = 0
        if self.y + self.height > HEIGHT:
            self.y = HEIGHT - self.height


class Musuh(Character):

    def move(self):
        self.y += 5

        if self.y > HEIGHT:

            self.y = 0
            self.x = random.randint(0, WIDTH - self.width)

player = Player(235, 260, 130, BLUE)
musuh = Musuh(random.randint(0, 470), 0, 130, PINK)

clock = pygame.time.Clock()

score = 0
running = True
game_over = False
start_screen = True
countdown_active = False

start_time = 0
countdown_start = 0
waktu = 0

while running:
    clock.tick(60)

    if GAMBAR_BG:
        screen.blit(GAMBAR_BG, (0, 0))
    else:
        screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if start_screen or game_over:

                    start_screen = False
                    game_over = False
                    countdown_active = True

                    score = 0
                    waktu = 0

                    player.x = 235
                    player.y = 260

                    musuh.y = 0
                    musuh.x = random.randint(0, WIDTH - musuh.width)

                    countdown_start = pygame.time.get_ticks()

    keys = pygame.key.get_pressed()

    if countdown_active:
        elapsed = (pygame.time.get_ticks() - countdown_start) // 1000
        if elapsed < 3:
            text = countdown_font.render(str(3 - elapsed), True, BLACK)
            screen.blit(text, (WIDTH // 2 - 30, HEIGHT // 2 - 60))
        elif elapsed == 3:
            text = countdown_font.render("GO!", True, BLACK)
            screen.blit(text, (WIDTH // 2 - 80, HEIGHT // 2 - 60))
        else:
            countdown_active = False
            start_time = pygame.time.get_ticks()

    elif not start_screen and not game_over:

        waktu = (pygame.time.get_ticks() - start_time) // 1000

        player.move()
        player.batas()

        musuh.move()

        score += 1

        if player.get_rect().colliderect(musuh.get_rect()):
            game_over = True

        score_text = font.render("Score: " + str(score), True, BLACK)
        time_text = font.render("Waktu: " + str(waktu) + " detik", True, BLACK)

        screen.blit(score_text, (10, 10))
        screen.blit(time_text, (10, 40))

        player.draw(screen, GAMBAR_PLAYER)
        musuh.draw(screen, GAMBAR_MUSUH)

    elif game_over:

        text = big_font.render("GAME OVER", True, BLACK)
        score_text = font.render("Score akhir: " + str(score), True, BLACK)
        time_text = font.render("Waktu bermain: " + str(waktu) + " detik", True, BLACK)
        restart_text = font.render("Tekan ENTER untuk restart", True, BLACK)

        screen.blit(text, (150, 120))
        screen.blit(score_text, (190, 190))
        screen.blit(time_text, (160, 230))
        screen.blit(restart_text, (150, 270))

    else:
        title = font.render("Tekan ENTER untuk mulai", True, BLACK)
        screen.blit(title, (180, 200))

    pygame.display.flip()