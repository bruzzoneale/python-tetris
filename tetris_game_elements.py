# -------------------------------------------------------------------------------
# import basic python modules
import random
from enum import Enum
from tetris_config import *


# -------------------------------------------------------------------------------
# Classe che definisce le azioni che possono essere eseguite su un tetramino
class TetramineAction(Enum):
    MOVE_LEFT = 1
    MOVE_RIGHT = 2
    ROTATE = 3
    FALL = 4


# -------------------------------------------------------------------------------
# Classe che definisce la coordinata di una cella all'interno dell'area di gioco
class GameCell:
    def __init__(self, row, col):
        self.row = row
        self.col = col


# -------------------------------------------------------------------------------
# Classe che definisce un tetramino
class Tetramine:

    def __init__(self):
        self.figureNumber = random.randrange(0, len(FIGURES))  # crea un tetramino a caso
        self.position = []
        for i in range(0, FIGURE_SIZE):
            a = GameCell(
                START_LINE   + int(FIGURES[self.figureNumber][i] / 2) - 1,  # riga
                START_COLUMN + int(FIGURES[self.figureNumber][i] % 2) - 1   # colonna
            )
            self.position.append(a)

    # sposta la posizione del tetramino sull'asse x, direction puo' essere + o -
    def move(self, direction):
        for i in range(0, FIGURE_SIZE):
            self.position[i].col += direction

    # sposta la posizione del tetramino sull'asse y (caduta)
    def fall(self):
        for i in range(0, FIGURE_SIZE):
            self.position[i].row += 1

    # ruota un tetramino
    def rotate(self):
        idx = FIGURES_ROTATIONPOINT[self.figureNumber]
        if idx > 0:
            p = GameCell(self.position[idx].row, self.position[idx].col)  # punto di rotazione
            for i in range(0, FIGURE_SIZE):
                x = self.position[i].row - p.row
                y = self.position[i].col - p.col
                self.position[i].col = p.col - x
                self.position[i].row = p.row + y
            # ci si assicura che il tetramino non finisca fuori dai bordi
            delta = 0
            lastCol = BOARD_COLUMNS - 1
            for i in range(0, FIGURE_SIZE):
                if (self.position[i].col < 0) and (self.position[i].col < delta):
                    delta = self.position[i].col
                if (self.position[i].col > lastCol) and (self.position[i].col - lastCol > delta):
                    delta = self.position[i].col - lastCol
            if delta != 0:
                for i in range(0, FIGURE_SIZE):
                    self.position[i].col -= delta

    # esegue un'azione predefinita sul tetramino
    def do_action(self, action):
        if action == TetramineAction.MOVE_LEFT:
            self.move(-1)
        elif action == TetramineAction.MOVE_RIGHT:
            self.move(1)
        elif action == TetramineAction.FALL:
            self.fall()
        elif action == TetramineAction.ROTATE:
            self.rotate()

    # copia le impostazioni da un altro tetramino (per clonare un oggetto)
    def copy_from(self, piece):
        self.figureNumber = piece.figureNumber
        for i in range(0, FIGURE_SIZE):
            self.position[i].row = piece.position[i].row
            self.position[i].col = piece.position[i].col

    # Verifica se il tetramino e' "entrato" interamente all'interno dell'area di gioco
    def is_onboard(self):
        for i in range(0, FIGURE_SIZE):
            if self.position[i].row < 0:
                return False
        return True


# -------------------------------------------------------------------------------
# Definzione dell'area di gioco
# si tiene in memoria una matrice che corrisponde a tutte le caselle che
# andranno ad occupare gli elementi dei vari tetramini che si depositano sul fondo
class GameArea:

    def __init__(self):
        self.board = []
        for y in range(0, BOARD_LINES):
            self.board.append([0] * BOARD_COLUMNS)

    # azzera l'area di gioco
    def clear(self):
        for y in range(0, BOARD_LINES):
            for x in range(0, BOARD_COLUMNS):
                self.board[y][x] = 0

    # elimina la riga indicata
    def remove_line(self, line):
        # tutte le righe precedenti alla riga indicata slittano di una posizione (caduta)
        for i in range(line, 0, -1):
            for x in range(0, BOARD_COLUMNS):
                self.board[i][x] = self.board[i - 1][x]
        # libero la prima riga azzerando il contenuto delle celle
        for x in range(0, BOARD_COLUMNS):
            self.board[0][x] = 0

    # verifica se una riga e' stata completamente occupata
    def is_filled_line(self, line):
        for x in range(0, BOARD_COLUMNS):
            if self.board[line][x] == 0:
                return False
        return True

    # verifica se una riga è completamente libera (per i bonus)
    def is_empty_line(self, line):
        for x in range(0, BOARD_COLUMNS):
            if self.board[line][x] > 0:
                return False
        return True

    # Verifica se la posizione relativa ad una cella e' utilizzabile per uno spostamento
    def can_move_to_cell(self, row, col):
        result = True
        # fuori dai limiti dell'area di gioco
        if (col < 0) or (col > BOARD_COLUMNS - 1) or (row > BOARD_LINES - 1):
            result = False
        else:
            if (row >= 0) and (self.board[row][col] > 0):  # cella gia' occupata
                result = False
        return result

    # Verifica se per il tetramino c'e' spazio libero per spostarsi in base ad un'azione
    # il test viene eseguito su una copia del tetramino indicato
    def can_move_tetramine(self, piece, action):
        p = Tetramine()
        p.copy_from(piece)
        p.do_action(action)
        for i in range(0, FIGURE_SIZE):
            if not self.can_move_to_cell(p.position[i].row, p.position[i].col):
                return False
        return True

    # Occupa le posizioni degli elementi del tetrmino indicato nelle rispettive celle dell'area di gioco
    def set_tetramine_position(self, piece):
        for i in range(0, FIGURE_SIZE):
            x = piece.position[i].col
            y = piece.position[i].row
            self.board[y][x] = piece.figureNumber + 1


# -------------------------------------------------------------------------------
if __name__ == '__main__':
    print('you must run tetris.py')
