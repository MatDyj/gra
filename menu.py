import pygame
from settings_manager import save_settings

pygame.font.init()
pygame.mixer.init()

font = pygame.font.Font(None, 36)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

DIFFICULTY_LEVELS = ["easy", "medium", "hard"]

def play_music_for_level(level):
    music_files = {
        "easy": "sounds/epic-war-background-music-336297.mp3",
        "medium": "sounds/epic-war-music-354041.mp3",
        "hard": "sounds/war-epic-background-music-354155.mp3"
    }
    music_path = music_files.get(level)
    if music_path:
        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"Nie można załadować muzyki: {music_path}\n{e}")
    else:
        pygame.mixer.music.stop()

def show_hall_of_fame(screen):
    clock = pygame.time.Clock()
    with open("scores.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    while True:
        screen.blit(background, (0, 0))  # Rysujemy tło

        title = font.render("Ściana Chwały", True, WHITE)
        screen.blit(title, (300, 50))
        for i, line in enumerate(lines[-10:]):
            txt = font.render(line.strip(), True, WHITE)
            screen.blit(txt, (150, 120 + i * 30))
        info = font.render("Naciśnij ESC aby wrócić", True, WHITE)
        screen.blit(info, (250, 500))
        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

def show_main_menu(screen, settings):
    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()
    selected_option = 0
    options = ["Start", "Ustawienia", "Ściana Chwały", "Wyjście"]

    try:
        pygame.mixer.music.load("sounds/cosmic-soundscapes_1-334062.mp3")
        pygame.mixer.music.set_volume(0.3)  
        pygame.mixer.music.play(-1)
    except pygame.error as e:
        print(f"Błąd odtwarzania muzyki menu: {e}")

    title_font = pygame.font.Font(None, 100)
    author_font = pygame.font.Font(None, 36)
    blink_timer = 0
    blink_visible = True
    float_offset = 0
    float_direction = 1

    while True:
        screen.blit(background, (0, 0))  # Rysujemy tło

        neon_color = (0, 255, 100)
        glow_color = (0, 100, 50)

        blink_timer += clock.get_time()
        if blink_timer >= 500:
            blink_visible = not blink_visible
            blink_timer = 0

        float_offset += float_direction * 0.5
        if abs(float_offset) > 5:
            float_direction *= -1

        if blink_visible:
            title_surface = title_font.render("Space Invaders", True, neon_color)
            glow_surface = title_font.render("Space Invaders", True, glow_color)
            screen.blit(glow_surface, (WIDTH // 2 - glow_surface.get_width() // 2 + 2,
                                       40 + int(float_offset) + 2))
            screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2,
                                        40 + int(float_offset)))

        author_text = author_font.render("made by Matthew Dyjak", True, neon_color)
        screen.blit(author_text, (WIDTH // 2 - author_text.get_width() // 2,
                                  130 + int(float_offset)))

        for i, option in enumerate(options):
            color = WHITE if i == selected_option else (100, 100, 100)
            text = font.render(option, True, color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 200 + i * 50))

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if options[selected_option] == "Start":
                        pygame.mixer.music.stop()
                        return settings.get("difficulty", "medium")
                    elif options[selected_option] == "Ustawienia":
                        show_settings_menu(screen, settings)
                    elif options[selected_option] == "Ściana Chwały":
                        show_hall_of_fame(screen)
                    elif options[selected_option] == "Wyjście":
                        pygame.mixer.music.stop()
                        exit()

def show_settings_menu(screen, settings):
    clock = pygame.time.Clock()
    selected_setting = 0
    options = [
        "Sterowanie: Lewo",
        "Sterowanie: Prawo",
        "Sterowanie: Góra",
        "Sterowanie: Dół",
        "Strzał",
        "Dźwięk",
        "Poziom trudności",
        "Powrót"
    ]

    while True:
        screen.blit(background, (0, 0))  # Rysujemy tło

        for i, option in enumerate(options):
            color = WHITE if i == selected_setting else (100, 100, 100)
            label = option
            if "Lewo" in option:
                label += f" [{settings['key_left']}]"
            elif "Prawo" in option:
                label += f" [{settings['key_right']}]"
            elif "Góra" in option:
                label += f" [{settings.get('key_up')}]"
            elif "Dół" in option:
                label += f" [{settings.get('key_down')}]"
            elif "Strzał" in option:
                label += f" [{settings['key_fire']}]"
            elif "Dźwięk" in option:
                label += f" [{'ON' if settings['sound'] else 'OFF'}]"
            elif "trudności" in option:
                label += f" [{settings['difficulty'].capitalize()}]"
            text = font.render(label, True, color)
            screen.blit(text, (200, 150 + i * 40))

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_setting = (selected_setting - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_setting = (selected_setting + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected_setting == 0:
                        settings['key_left'] = prompt_for_key(screen, "Lewo")
                    elif selected_setting == 1:
                        settings['key_right'] = prompt_for_key(screen, "Prawo")
                    elif selected_setting == 2:
                        settings['key_up'] = prompt_for_key(screen, "Góra")
                    elif selected_setting == 3:
                        settings['key_down'] = prompt_for_key(screen, "Dół")
                    elif selected_setting == 4:
                        settings['key_fire'] = prompt_for_key(screen, "Strzał")
                    elif selected_setting == 5:
                        settings['sound'] = not settings['sound']
                    elif selected_setting == 6:
                        idx = DIFFICULTY_LEVELS.index(settings['difficulty'])
                        settings['difficulty'] = DIFFICULTY_LEVELS[(idx + 1) % len(DIFFICULTY_LEVELS)]
                    elif selected_setting == 7:
                        save_settings(settings)
                        return

def prompt_for_key(screen, label):
    clock = pygame.time.Clock()
    font_big = pygame.font.Font(None, 48)

    while True:
        screen.blit(background, (0, 0))  # Rysujemy tło

        msg = font_big.render(f"Naciśnij klawisz dla: {label}", True, WHITE)
        screen.blit(msg, (150, 300))
        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                return pygame.key.name(event.key).upper()

# --- Inicjalizacja pygame i tła ---
pygame.init()
screen = pygame.display.set_mode((800, 600))  # Przykładowy rozmiar okna
background = pygame.image.load("assets/background.jpg").convert()
background = pygame.transform.scale(background, screen.get_size())

# Przykładowe ustawienia (musisz mieć je gdzieś w programie)
settings = {
    "key_left": "LEFT",
    "key_right": "RIGHT",
    "key_up": "UP",
    "key_down": "DOWN",
    "key_fire": "SPACE",
    "sound": True,
    "difficulty": "medium"
}

# Uruchom menu
difficulty = show_main_menu(screen, settings)

# Po wybraniu poziomu uruchom muzykę dla tego poziomu
if settings["sound"]:
    play_music_for_level(difficulty)
