import pygame
import random
import time
import os

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        original_image = pygame.image.load("assets/gracz.jpg").convert_alpha()
        self.image = pygame.transform.scale(original_image, (50, 50))  # dopasuj rozmiar
        self.rect = self.image.get_rect(center=(400, 550))
        self.speed = 5
        self.lives = 3
        self.powered_up = False
        self.power_timer = 0
        self.shoot_cooldown = 0

    def update(self, keys, left_key, right_key, up_key, down_key, enemies):
        old_rect = self.rect.copy()

        if keys[left_key]:
            self.rect.x -= self.speed
        if keys[right_key]:
            self.rect.x += self.speed
        if keys[up_key]:
            self.rect.y -= self.speed
        if keys[down_key]:
            self.rect.y += self.speed

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 800:
            self.rect.right = 800
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 600:
            self.rect.bottom = 600

        if pygame.sprite.spritecollide(self, enemies, False):
            self.rect = old_rect

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        if self.powered_up:
            self.power_timer -= 1
            if self.power_timer <= 0:
                self.powered_up = False
class LifeUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        original_image = pygame.image.load("assets/zycie.jpg").convert_alpha()
        self.image = pygame.transform.scale(original_image, (25, 25))  # dopasuj rozmiar do gry
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 2

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        original_image = pygame.image.load("assets/przeciwnik.jpg").convert_alpha()
        self.image = pygame.transform.scale(original_image, (40, 30))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = random.randint(1, 3)
        self.direction = random.choice([-1, 1])
        self.shoot_chance = 0.002
        self.max_y = 300

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.right >= 800 or self.rect.left <= 0:
            self.direction *= -1
            if self.rect.y + 20 <= self.max_y:
                self.rect.y += 20
        if random.random() < self.shoot_chance:
            return True
        return False


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, color=WHITE):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -7

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.kill()

class Wall(pygame.sprite.Sprite):
    def __init__(self, player_rect):
        super().__init__()
        self.width = int(player_rect.width * 2.5)
        self.height = 15
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(midbottom=(player_rect.centerx, player_rect.top - 10))
        self.speed = 2
        self.direction = 1

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.left <= 0 or self.rect.right >= 800:
            self.direction *= -1

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        original_image = pygame.image.load("assets/power_up.png").convert_alpha()
        self.image = pygame.transform.scale(original_image, (25, 25))  # dostosuj rozmiar do gry
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 2

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.kill()


def get_key_code(key_name, default_key):
    try:
        return pygame.key.key_code(key_name.lower())
    except Exception:
        print(f"Nieprawidłowy klawisz: {key_name}. Użyto domyślnego.")
        return default_key

def run_game(screen, settings, difficulty):
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    # Wczytanie tła
    background = pygame.image.load("assets/tlo_poziomu.jpg").convert()
    background = pygame.transform.scale(background, (800, 600))

    player = Player()
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    powerups = pygame.sprite.Group()

    all_sprites.add(player)

    rows = {"easy": 2, "medium": 4, "hard": 6}[difficulty]
    for row in range(rows):
        for col in range(10):
            enemy = Enemy(60 + col * 60, 50 + row * 40)
            if difficulty == "hard":
                enemy.shoot_chance = 0.01
            elif difficulty == "medium":
                enemy.shoot_chance = 0.005
            enemies.add(enemy)
            all_sprites.add(enemy)

    wall = None
    if difficulty == "hard":
        wall = Wall(player.rect)
        all_sprites.add(wall)

    left_key = get_key_code(settings.get("key_left", "left"), pygame.K_LEFT)
    right_key = get_key_code(settings.get("key_right", "right"), pygame.K_RIGHT)
    up_key = get_key_code(settings.get("key_up", "up"), pygame.K_UP)
    down_key = get_key_code(settings.get("key_down", "down"), pygame.K_DOWN)
    fire_key = get_key_code(settings.get("key_fire", "space"), pygame.K_SPACE)

    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")
    last_screenshot_time = time.time()

    score = 0
    start_time = time.time()
    running = True
    while running:
        now = time.time()
        if now - last_screenshot_time >= 15:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            pygame.image.save(screen, f"screenshots/screenshot_{timestamp}.png")
            last_screenshot_time = now

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == fire_key and player.shoot_cooldown <= 0:
                    color = YELLOW if player.powered_up else WHITE
                    bullet = Bullet(player.rect.centerx, player.rect.top, color)
                    bullets.add(bullet)
                    all_sprites.add(bullet)
                    player.shoot_cooldown = 5 if player.powered_up else 15

        keys = pygame.key.get_pressed()
        player.update(keys, left_key, right_key, up_key, down_key, enemies)

        if wall:
            wall.update()
            if player.rect.colliderect(wall.rect):
                if player.rect.centerx < wall.rect.centerx:
                    player.rect.right = wall.rect.left
                else:
                    player.rect.left = wall.rect.right
            for bullet in bullets:
                if bullet.rect.colliderect(wall.rect):
                    bullet.kill()
            for bullet in enemy_bullets:
                if bullet.rect.colliderect(wall.rect):
                    bullet.kill()

        for enemy in enemies:
            if enemy.update():
                bullet = EnemyBullet(enemy.rect.centerx, enemy.rect.bottom)
                enemy_bullets.add(bullet)
                all_sprites.add(bullet)

        bullets.update()
        enemy_bullets.update()
        powerups.update()

        for bullet in bullets:
            hits = pygame.sprite.spritecollide(bullet, enemies, True)
            if hits:
                bullet.kill()
                score += 10
                if random.random() < 0.2:  # 20% szans na power-up
                    hit = hits[0]
                    if random.random() < 0.5:  # 50% szansy na LifeUp
                        lifeup = LifeUp(hit.rect.centerx, hit.rect.centery)
                        powerups.add(lifeup)
                        all_sprites.add(lifeup)
                    else:
                        powerup = PowerUp(hit.rect.centerx, hit.rect.centery)
                        powerups.add(powerup)
                        all_sprites.add(powerup)

        powerup_hits = pygame.sprite.spritecollide(player, powerups, True)
        for powerup in powerup_hits:
            if isinstance(powerup, PowerUp):
                player.powered_up = True
                player.power_timer = 600
                player.shoot_cooldown = 0
            elif isinstance(powerup, LifeUp):
                if player.lives < 5:
                    player.lives += 1

        if pygame.sprite.spritecollide(player, enemy_bullets, True):
            player.lives -= 1
            if player.lives <= 0:
                screen.fill(BLACK)
                death_font = pygame.font.Font(None, 100)
                death_text = death_font.render("You DIED", True, RED)
                retry_font = pygame.font.Font(None, 50)
                retry_text = retry_font.render("Spróbuj ponownie (naciśnij dowolny klawisz)", True, WHITE)
                screen.blit(death_text, (400 - death_text.get_width() // 2, 250))
                screen.blit(retry_text, (400 - retry_text.get_width() // 2, 350))
                pygame.display.flip()
                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                        elif event.type == pygame.KEYDOWN:
                            waiting = False
                running = False
                break

        if len(enemies) == 0:
            total_time = int(time.time() - start_time)
            name = ""
            input_active = True
            input_box = pygame.Rect(200, 300, 400, 50)
            while input_active:
                screen.fill(BLACK)
                txt = font.render("Wpisz swój nick i wciśnij Enter:", True, WHITE)
                screen.blit(txt, (200, 250))
                txt_surface = font.render(name, True, WHITE)
                screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
                pygame.draw.rect(screen, WHITE, input_box, 2)
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN and name.strip():
                            with open("scores.txt", "a") as f:
                                f.write(f"{name.strip()} - {score} pkt - {total_time} sek\n")
                            input_active = False
                        elif event.key == pygame.K_BACKSPACE:
                            name = name[:-1]
                        else:
                            if len(name) < 15 and event.unicode.isprintable():
                                name += event.unicode
            running = False
            break

        # Zamiast screen.fill(BLACK) rysujemy tło:
        screen.blit(background, (0, 0))
        all_sprites.draw(screen)
        elapsed_time = int(time.time() - start_time)
        screen.blit(font.render(f"Czas: {elapsed_time}s", True, WHITE), (10, 560))
        screen.blit(font.render(f"Wynik: {score}", True, WHITE), (10, 10))
        screen.blit(font.render(f"Życia: {player.lives}", True, WHITE), (10, 40))
        if player.powered_up:
            screen.blit(font.render(f"Power: {player.power_timer // 60}s", True, YELLOW), (10, 70))
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Space Invaders")

    settings = {
        "key_left": "left",
        "key_right": "right",
        "key_up": "up",
        "key_down": "down",
        "key_fire": "space"
    }

    difficulty = "hard"
    run_game(screen, settings, difficulty)