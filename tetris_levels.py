from tetris_config import *


# -------------------------------------------------------------------------------
# Definizione di un livello di gioco
class GameLevel:

    def __init__(self, goal):
        self.fallSpeed = FALL_SPEED  # ritardo nella velocità di caduta dei tetramini
        self.goal = goal  # linee da completare per superare il livello
        self.filledLines = []  # linee sul fondo con celle già occupata

    def inc_speed(self, delta):
        self.fallSpeed -= delta
        if self.fallSpeed < 50:
            self.fallSpeed = 50
        return self

    def inc_goal(self, delta):
        self.goal += delta
        return self


# -------------------------------------------------------------------------------
# Definizione dei livelli di gioco
class GameLevels:

    def __init__(self):
        self.levels = []
        self.currentLevel = 0
        self.load_levels()

    def levels_count(self):
        return len(self.levels)

    # Aggiunge un livello alla lista dei livelli di gioco
    def add(self, goal):
        level = GameLevel(goal)
        self.levels.append(level)
        return level

    # Torna il livello successivo a quello corrente (torna l'oggetto), da chiamare sempre, anche a inizio partita per
    # recuperare il primo livello Indipendentemente da quanti livelli sono definiti questo metodo simula la presenza
    # di un numero di livelli infiniti (ripetendoli ciclicamente)
    def next(self):
        self.currentLevel += 1
        multip = self.currentLevel // self.levels_count()  # quante volte sono stati completati tutti i livelli nella lista
        offset = self.currentLevel % self.levels_count()  # indice nella lista per recuperare il livello corrente
        if offset == 0:
            offset = self.levels_count()

        level = self.levels[offset - 1]
        if multip > 0:  # simula livelli infiniti: ricomincia dall'inizio applicando alcune varianti
            level.inc_speed(50 * multip)
            level.inc_goal(5 * multip)

        return level

    # Inizializza la lista dei livelli: aggiornare questo metodo per inventare nuovi livelli
    def load_levels(self):
        self.add(5)
        self.add(10).inc_speed(50)
        self.add(10).inc_speed(70).filledLines = [
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 2]]
        self.add(15).inc_speed(90).filledLines = [
            [0, 0, 0, 4, 6, 7, 3, 0, 0, 0],
            [1, 0, 3, 0, 0, 2, 0, 0, 4, 0]]
        self.add(15).inc_speed(100).filledLines = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [2, 4, 1, 0, 3, 6, 0, 7, 0, 2]]
        self.add(15).inc_speed(120).filledLines = [
            [0, 7, 3, 2, 1, 1, 2, 3, 6, 0],
            [0, 0, 4, 1, 2, 2, 1, 5, 0, 0],
            [0, 0, 0, 4, 6, 7, 3, 0, 0, 0],
            [0, 0, 0, 0, 2, 1, 0, 0, 0, 0]]
        self.add(15).inc_speed(120).filledLines = [
            [1, 0, 3, 0, 0, 2, 0, 0, 4, 0],
            [0, 0, 3, 0, 2, 0, 0, 1, 0, 0],
            [0, 5, 0, 0, 0, 0, 0, 0, 0, 6],
            [0, 0, 0, 1, 0, 0, 4, 0, 0, 0]]
        self.add(15).inc_speed(120).filledLines = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [2, 4, 1, 5, 3, 6, 4, 7, 1, 2]]


# -------------------------------------------------------------------------------
if __name__ == '__main__':
    print('you must run tetris.py')
