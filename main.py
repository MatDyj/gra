import pygame
from menu import show_main_menu, play_music_for_level
from game import run_game
from settings_manager import load_settings

# Inicjalizacja Pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Ustawienia ekranu
WIDTH, HEIGHT = 800, 600 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Załaduj ustawienia
settings = load_settings()

# Główna pętla aplikacji
running = True
while running:
    # Wyświetl menu główne
    difficulty = show_main_menu(screen, settings)

    # Odtwórz muzykę dla danego poziomu trudności
    play_music_for_level(difficulty)

    # Uruchom grę
    run_game(screen, settings, difficulty)

    # Po zakończeniu gry zatrzymaj muzykę
    pygame.mixer.music.stop()

# Zakończenie
pygame.quit()

