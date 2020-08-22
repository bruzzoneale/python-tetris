# -------------------------------------------------------------------------------
# import basic python modules
import os.path
# import basic pygame modules
import pygame

# -------------------------------------------------------------------------------
MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]
IMAGES_DIR = 'images'  # cartella dove si trovano le immagini
SOUNDS_DIR = 'sounds'  # cartella dove si trovano gli effetti sonori

COLOR_WHITE = (255, 255, 255)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE  = (0, 0, 128)


# Funzione generica per il caricamento di un'immagine da file
def load_image(file):
    file = os.path.join(MAIN_DIR, IMAGES_DIR, file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s' % (file, pygame.get_error()))
    return surface.convert()


# Classe sound fittizia (non esegue alcun suono) si usa in caso di errore
# (non si riproducono suoni senza mandare in errore il programma)
class DummySound:

    def __init__(self):
        pass

    def play(self): pass


# -------------------------------------------------------------------------------
# Classe che riproduce un suono
class GameSound:
    Enabled = False  # variabile di classe: condivisa da tutti gli oggetti GameSound

    def __init__(self, file):
        self.sound = GameSound.load_sound(file)

    def play(self):
        if GameSound.Enabled:
            self.sound.play()

    @staticmethod
    def toggle_sound():  # attiva / disattiva l'audio
        GameSound.Enabled = not GameSound.Enabled

    # Funzione generica per il caricamento di un suono
    @staticmethod
    def load_sound(file):
        if not pygame.mixer:
            return DummySound()
        file = os.path.join(MAIN_DIR, SOUNDS_DIR, file)
        try:
            sound = pygame.mixer.Sound(file)
            return sound
        except pygame.error:
            print('Warning, unable to load, %s' % file)
        return DummySound()


def toggle_sound():
    GameSound.toggle_sound()


# -------------------------------------------------------------------------------
# Classe che definisce una coordinata generica per lo schermo (in pixel)
class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y
# -------------------------------------------------------------------------------
