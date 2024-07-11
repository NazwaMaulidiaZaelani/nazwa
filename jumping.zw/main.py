import pygame
import random
import sys

# Inisialisasi Pygame
pygame.init()

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Ukuran layar
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("JUMPING GAME")

# Font untuk menampilkan skor dan pesan game over
font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font(None, 72)

# FPS
clock = pygame.time.Clock()
FPS = 60

# Fungsi untuk memuat gambar
def load_image(name, width=None, height=None):
    try:
        image = pygame.image.load(name)
        if width and height:
            image = pygame.transform.smoothscale(image, (width, height))
        return image
    except pygame.error as e:
        print(f"Tidak dapat memuat gambar {name}: {e}")
        sys.exit()

# Muat dan mainkan backsound
pygame.mixer.music.load("backsound.mp3")
pygame.mixer.music.play(-1)  # -1 berarti musik akan diulang terus-menerus

# Tombol Start
soundstart = pygame.mixer.Sound("sound.mp3")
soundstart.set_volume(1.0)  # Mengatur volume ke 100%
start_button_image = pygame.image.load("start.png").convert_alpha()
start_button_image = pygame.transform.smoothscale(start_button_image, (220, 200))
start_button_rect = start_button_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))

# Tombol Play Again
playagain_button_image = pygame.image.load("start.png").convert_alpha()
playagain_button_image = pygame.transform.smoothscale(playagain_button_image, (220, 200))
playagain_button_rect = playagain_button_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 10))

# Muat gambar latar belakang, dino, dan kaktus
background_img = load_image('background.jpeg', SCREEN_WIDTH, SCREEN_HEIGHT)
dino_img = load_image('player.png', 95, 95)
cactus_img = load_image('cactus.png', 95, 95)
cactus2_img = load_image('cactus 2.png', 95, 95)
cloud_img = load_image('cloud.png', 577, 135)  # Gambar awan

# Variabel untuk dino
dino_x = 50
dino_y = SCREEN_HEIGHT - 80
dino_vel_y = 0
dino_is_jumping = False

# Daftar untuk kaktus dan awan
cacti = []
clouds = []

class Cloud:
    def __init__(self, x, y, vel_x, speed):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.image = cloud_img
        self.speed = speed  # Kecepatan horizontal awan

    def update(self):
        self.x += self.vel_x * self.speed
        if self.x < -self.image.get_width():
            self.x = SCREEN_WIDTH  # Reset posisi awan ke sebelah kanan layar

    def draw(self):
        SCREEN.blit(self.image, (self.x, self.y))

def spawn_cactus():
    cactus_x = SCREEN_WIDTH
    cactus_y = SCREEN_HEIGHT - 80
    cactus_vel_x = -10  # Kecepatan horizontal kaktus
    cactus_image = random.choice([cactus_img, cactus2_img])  # Pilih secara acak antara cactus_img dan cactus2_img
    cacti.append({"x": cactus_x, "y": cactus_y, "vel_x": cactus_vel_x, "image": cactus_image})

def spawn_cloud():
    cloud_x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH * 2)  # Spawn di luar layar
    cloud_y = random.randint(50, 100)  # Atur tinggi awan secara acak
    cloud_vel_x = -1  # Kecepatan horizontal awan
    cloud_speed = random.uniform(0.2, 2.0)  # Kecepatan acak untuk awan
    clouds.append(Cloud(cloud_x, cloud_y, cloud_vel_x, cloud_speed))

# Spawning initial cactus dan cloud
spawn_cactus()
for _ in range(5):  # Spawn beberapa awan awal
    spawn_cloud()

# Variabel untuk skor
score = 0

# Fungsi untuk menggambar dino
def draw_dino():
    SCREEN.blit(dino_img, (dino_x, dino_y))

# Fungsi untuk menggambar kaktus
def draw_cacti():
    for cactus in cacti:
        SCREEN.blit(cactus["image"], (cactus["x"], cactus["y"]))

# Fungsi untuk menggambar awan
def draw_clouds():
    for cloud in clouds:
        cloud.draw()

# Fungsi untuk menggambar skor
def draw_score(score):
    score_text = font.render(f'Score: {score}', True, (30, 144, 255))
    SCREEN.blit(score_text, (10, 10))

# Fungsi untuk menggambar tombol
def draw_button(image, rect):
    SCREEN.blit(image, rect)

# Fungsi untuk memeriksa apakah tombol diklik
def button_clicked(rect, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if rect.collidepoint(event.pos):
            return True
    return False

# Fungsi untuk menampilkan layar start
def show_start_screen():
    start_screen = True
    while start_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if button_clicked(start_button_rect, event):
                soundstart.play()
                start_screen = False

        SCREEN.fill(WHITE)
        draw_button(start_button_image, start_button_rect)
        pygame.display.update()
        clock.tick(FPS)

# Fungsi utama
def main():
    global dino_y, dino_vel_y, dino_is_jumping, score

    show_start_screen()

    run = True
    game_over = False
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not dino_is_jumping and not game_over:
                    dino_is_jumping = True
                    dino_vel_y = -15
                    score += 10  # Tambah skor setiap kali melompat

        if not game_over:
            # Logika lompatan dino
            if dino_is_jumping:
                dino_vel_y += 1
                dino_y += dino_vel_y
                if dino_y >= SCREEN_HEIGHT - 80:
                    dino_y = SCREEN_HEIGHT - 80
                    dino_is_jumping = False

            # Pindahkan kaktus
            for cactus in cacti:
                cactus["x"] += cactus["vel_x"]
                if cactus["x"] < -10:
                    cacti.remove(cactus)
                    score += 10  # Tambah skor saat berhasil menghindari kaktus

            # Pindahkan awan
            for cloud in clouds:
                cloud.update()
                if cloud.x < -cloud.image.get_width():
                    clouds.remove(cloud)
                    spawn_cloud()

            # Spawn kaktus baru secara acak
            if random.randint(1, 60) == 1:  # 1/60 kemungkinan per frame
                spawn_cactus()

            # Periksa tabrakan
            dino_rect = pygame.Rect(dino_x, dino_y, 40, 40)
            for cactus in cacti:
                cactus_rect = pygame.Rect(cactus["x"], cactus["y"], 20, 40)
                if dino_rect.colliderect(cactus_rect):
                    game_over = True

        # Gambar background
        SCREEN.blit(background_img, (0, 0))

        # Gambar dino, kaktus, dan awan
        draw_dino()
        draw_cacti()
        draw_clouds()

        # Gambar skor
        draw_score(score)

        # Gambar pesan game over
        if game_over:
            game_over_text = game_over_font.render("Game Over", True, (225, 0, 0))
            SCREEN.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))

        # Update layar
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
