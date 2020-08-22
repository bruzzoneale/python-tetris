from pygame.locals import *
from commons import Point

# -------------------------------------------------------------------------------
# dimensioni e caratteristiche di default del tabellone di gioco
# tutte queste variabili possono essere poi parametrizzati nell'ambito
# dei livelli di gioco
SCREEN_MODE = 0  # modalità di avvio, 0 | FULLSCREEN
SCREEN_BACKGROUND = 'background_800.jpg'
SCREEN_RECT = Rect(0, 0, 800, 540)  # dimensione della finestra (pari alla dimensione dell'immagine di background)
SCREEN_FONTSIZE = 48
SCREEN_FONTNAME = 'freesansbold.ttf'
SCREEN_OFFSET = Point(282, 39)  # origine grafica dell'area di gioco

NEXTFIGURE_OFFSET = Point(620, 250)  # origine grafica per la visualizzazione del tetramino successivo

SCOREBOARD_OFFSET = Point(50, 250)  # origine grafica per la visualizzazione del punteggio
SCOREBOARD_RECT = Rect(0, 0, 150, 150)
SCOREBOARD_FONTSIZE = 24
SCOREBOARD_FONTNAME = 'freesansbold.ttf'

TILE_SIZE = 24
TILERECT = Rect(0, 0, TILE_SIZE, TILE_SIZE)
TILES_IMAGES = 'tiles_24.png'

BOARD_LINES = 20
BOARD_COLUMNS = 10
FIGURES_COUNT = 7
START_COLUMN = 5  # colonna iniziale da dove partono i tetramini
START_LINE = -4  # riga iniziale da dove partono i tetramini
FALL_SPEED = 500  # tempo in millisecondi che impiega un tetramino a cadere di una cella

SOUNDS_ENABLED = True  # suoni abilitati allo startup
SOUND_FALL = 'fall.wav'
SOUND_LINE = 'line.wav'
SOUND_GAMEOVER = 'gameover.wav'
SOUND_SUCCESS = 'success.wav'
SOUND_BONUSLINE = 'speciallineclear.ogg'

# -------------------------------------------------------------------------------
# Definizione delle forme standard dei tetramini
# ogni tetramino e' formato da 4 elementi (TILE) qui sono definte le celle
# occupate da ogni elemento in una matrice di questo tipo:
#   0  1
#   2  3
#   4  5
#   6  7
FIGURE_SIZE = 4

FIGURES = [
    [2, 3, 4, 5],  # O
    [2, 4, 5, 7],  # Z
    [1, 3, 5, 7],  # I
    [3, 4, 5, 7],  # T
    [2, 3, 5, 7],  # L
    [3, 4, 5, 6],  # S
    [3, 5, 6, 7]   # J
]

FIGURES_ROTATIONPOINT = [
    0,  # O
    1,  # Z
    2,  # I
    2,  # T
    1,  # L
    1,  # S
    1   # J
]


# -------------------------------------------------------------------------------
if __name__ == '__main__':
    print('you must run tetris.py')
