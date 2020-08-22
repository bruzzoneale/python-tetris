# -------------------------------------------------------------------------------
# variabili e funzioni di uso comune
from commons import *
# configurazione e definizione dei livelli di gioco
from tetris_levels import *
# business logic del gioco
from tetris_game_elements import *


# -------------------------------------------------------------------------------
# Gestione del tabellone di gioco
class GameBoard:

    def __init__(self):
        self.area = GameArea()
        self.levels = GameLevels()
        self.level = None
        self.score = 0
        self.levelNum = 0
        self.linesLeft = 0
        self.nextPiece = None
        self.tilesImg = []  # elenco di tutti i blocchi grafici che occupano una cella
        img = load_image(TILES_IMAGES)  # carica tutti i blocchi in un unica immagine (devono essere quadrati)
        # scompone l'immagine in singoli blocchi (un colore per ogni forma + 1 blocco extra per le celle bonus)
        for i in range(0, len(FIGURES) + 1):
            tile = pygame.Surface(TILERECT.size)
            tile.blit(img, (0, 0), (i * TILE_SIZE, 0, TILE_SIZE, TILE_SIZE))
            self.tilesImg.append(tile)
        # Carica in memoria l'immagine da usare come sfondo
        bgdimg = load_image(SCREEN_BACKGROUND)
        self.background = pygame.Surface(SCREEN_RECT.size)
        self.background.blit(bgdimg, (0, 0))
        # font da usare per il punteggio
        self.font = pygame.font.Font(SCOREBOARD_FONTNAME, SCOREBOARD_FONTSIZE)
        self.next_level()

    # Predispone il tabellone per una nuova partita
    def new_game(self):
        self.score = 0
        self.levels = GameLevels()
        self.next_level()

    # Predispone il tabellone per un nuovo livello
    def next_level(self):
        self.area.clear()
        self.level = self.levels.next()
        self.levelNum = self.levels.currentLevel
        self.linesLeft = self.level.goal
        self.nextPiece = Tetramine()
        # caselle già occupate (si parte sempre dal fondo)
        for row in range(0, len(self.level.filledLines)):
            self.area.board[BOARD_LINES - row - 1] = self.level.filledLines[row]

    # Torna l'area occupata dal testo indicato (per calcolo dimensioni)
    def get_text_rect(self, text):
        obj = self.font.render(text, True, COLOR_WHITE)
        textrect = obj.get_rect()
        return textrect

    # Visualizza un testo sul tabellone (in trasparenza)
    def draw_text(self, screen, x, y, text):
        obj = self.font.render(text, True, COLOR_WHITE)
        textrect = obj.get_rect()
        screen.blit(obj, (x, y))
        return textrect

    # Visualizza il tabellone allo stato corrente
    def draw_background(self, screen, draw_scoreboard=True):
        # Visualizza l'immagine di sfondo
        screen.blit(self.background, (0, 0))
        # Visualizza le caselle già occupate nell'area di gioco
        for row in range(0, BOARD_LINES):
            for col in range(0, BOARD_COLUMNS):
                if self.area.board[row][col] > 0:
                    x = col * TILE_SIZE
                    y = row * TILE_SIZE
                    tile = self.tilesImg[self.area.board[row][col] - 1]
                    screen.blit(tile, (SCREEN_OFFSET.x + x, SCREEN_OFFSET.y + y))
        if draw_scoreboard:
            self.draw_scoreboard(screen)

    # Visualizza il punteggio
    def draw_scoreboard(self, screen):
        # coordinate di partenza per i testi dei punteggi
        x = SCOREBOARD_OFFSET.x
        y = SCOREBOARD_OFFSET.y
        # coordinate di partenza per i punteggi
        textrect = self.get_text_rect('MMMMMMM')
        x1 = x + textrect.width
        # Visualizza il livello
        self.draw_text(screen, x1, y, str(self.levelNum))
        textrect = self.draw_text(screen, x, y, 'Level')
        y += textrect.height + 5
        # Visualizza l'obietivo
        self.draw_text(screen, x1, y, str(self.linesLeft))
        textrect = self.draw_text(screen, x, y, 'Lines left')
        y += textrect.height + 5
        # Visualizza il punteggio
        self.draw_text(screen, x1, y, str(self.score))
        textrect = self.draw_text(screen, x, y, 'Score')
        y += textrect.height + 5
        # Visualizza il tetramino successivo
        x = NEXTFIGURE_OFFSET.x
        y = NEXTFIGURE_OFFSET.y
        tile = self.tilesImg[self.nextPiece.figureNumber]
        for i in range(0, 4):
            y2 = (self.nextPiece.position[i].row - START_LINE) * TILE_SIZE
            x2 = (self.nextPiece.position[i].col - START_COLUMN) * TILE_SIZE
            screen.blit(tile, (x + x2, y + y2))

    # Visualizza un tetramino nell'area di gioco
    def draw_tetramine(self, screen, piece):
        tile = self.tilesImg[piece.figureNumber]
        for i in range(0, FIGURE_SIZE):
            x = piece.position[i].col * TILE_SIZE
            y = piece.position[i].row * TILE_SIZE
            screen.blit(tile, (SCREEN_OFFSET.x + x, SCREEN_OFFSET.y + y))

    # Torna un nuovo tetramino creando già il successivo (per indicarlo sul tabellone)
    def get_new_tetramine(self):
        piece = self.nextPiece
        self.nextPiece = Tetramine()  # crea subito il tetramino successivo
        return piece

    # Sposta un tetramino sull'asse X se c'e' spazio libero nelle celle
    # torna TRUE se effettivamente il pezzo e' stato spostato
    def move_tetramine(self, piece, direction):
        if direction > 0:
            action = TetramineAction.MOVE_RIGHT
        else:
            action = TetramineAction.MOVE_LEFT
        if self.area.can_move_tetramine(piece, action):
            piece.move(direction)
            return True
        else:
            return False

    # Sposta un tetramino sull'asse Y (caduta) se c'e' spazio libero nelle celle
    # torna TRUE se effettivamente il pezzo e' stato spostato
    def fall_tetramine(self, piece):
        if self.area.can_move_tetramine(piece, TetramineAction.FALL):
            piece.fall()
            return True
        else:
            return False

    # Esegue la rotazione del tetramino se c'e' spazio libero nelle celle
    # Torna TRUE se effettivamente il pezzo e' stato spostato
    def rotate_tetramine(self, piece):
        if self.area.can_move_tetramine(piece, TetramineAction.ROTATE):
            piece.rotate()
            return True
        else:
            return False

    # Fissa un tetramino sul tabellone
    def place_tetramine(self, piece):
        self.area.set_tetramine_position(piece)

    # Rimuove una linea se completata
    def try_remove_line(self, row):
        if self.area.is_filled_line(row):
            self.area.remove_line(row)
            self.score += 50
            self.linesLeft -= 1
            return True
        else:
            return False

    # Se una riga è rimasta libera aumenta il punteggio (bonus) e la evidenzia
    def try_add_bonus_line(self, row):
        if self.area.is_empty_line(row):
            self.score += 10
            for col in range(0, BOARD_COLUMNS):
                self.area.board[row][col] = 8
            return True
        else:
            return False


# -------------------------------------------------------------------------------
# Gestione dei suoni
class TetrisSounds:

    def __init__(self):
        self.fall = GameSound(SOUND_FALL)
        self.line = GameSound(SOUND_LINE)
        self.gameover = GameSound(SOUND_GAMEOVER)
        self.success = GameSound(SOUND_SUCCESS)
        self.bonusline = GameSound(SOUND_BONUSLINE)


# -------------------------------------------------------------------------------
#  CLASSE PRINCIPALE
# -------------------------------------------------------------------------------
class TetrisGame:

    def __init__(self):
        # Inizializzazione pygame
        if pygame.get_sdl_version()[0] == 2:
            pygame.mixer.pre_init(44100, 32, 2, 1024)
        pygame.init()
        if pygame.mixer and not pygame.mixer.get_init():
            print('Warning, no sound')
            pygame.mixer = None

        # Impostazione finestra pygame
        bestdepth = pygame.display.mode_ok(SCREEN_RECT.size, SCREEN_MODE, 32)
        self.screen = pygame.display.set_mode(SCREEN_RECT.size, SCREEN_MODE, bestdepth)
        self.clock = pygame.time.Clock()
        # Font per i messaggi principali
        self.font1 = pygame.font.Font(SCREEN_FONTNAME, SCREEN_FONTSIZE)
        # Effetti sonori
        self.sounds = TetrisSounds()
        # Creazione tabellone di gioco
        self.mainboard = GameBoard()

    # Avvio del gioco
    def start(self):
        gameOver = True
        gameComplete = False
        gameStart = False
        GameSound.Enabled = SOUNDS_ENABLED
        user_message = 'Press ENTER to Start!'

        pygame.display.set_caption('Python Tetris !')
        self.mainboard.draw_background(self.screen, not gameOver)
        pygame.display.flip()

        while 1:
            # Gestione eventi
            for event in pygame.event.get():
                if event.type == QUIT or \
                        (event.type == KEYDOWN and event.key == K_ESCAPE):
                    return
                # Premendo il tasto INVIO iniziamo una nuova partita
                if event.type == KEYDOWN and event.key == K_RETURN and (gameOver or gameComplete):
                    gameStart = True

                # Premendo il tasto 'S' Attiva/Disattiva i suoni
                if event.type == KEYUP and event.key == K_s:
                    toggle_sound()

            # Inizia automaticamente il nuovo livello se non si preme invio entro 2 secondi
            if gameComplete and not gameStart:
                if pygame.time.get_ticks() - timeStart >= 2000:
                    gameStart = True

            # La partita deve ancora iniziare
            if (gameOver or gameComplete) and not gameStart:
                text = self.font1.render(user_message, True, COLOR_GREEN, COLOR_BLUE)
                textRect = text.get_rect()
                textRect.center = (SCREEN_RECT.width // 2, SCREEN_RECT.height // 2)
                self.screen.blit(text, textRect)
                pygame.display.flip()
                self.clock.tick(60)
                continue

            # Avvio di una nuova partita/livello
            if gameStart:
                gameStart = False
                if gameOver:
                    self.mainboard.new_game()
                else:
                    self.mainboard.next_level()

                gameOver = False
                gameComplete = False
                timeStart = pygame.time.get_ticks()
                self.mainboard.draw_background(self.screen)
                # crea il primo tetramino
                piece = Tetramine()
                self.mainboard.draw_tetramine(self.screen, piece)
                alreadyRotated = False  # per evitare di ruotare continuamente se si tiene premuto lo spazio

            # ------------- SVOLGIMENTO DEL GIOCO ----------------------------------

            speed = self.mainboard.level.fallSpeed  # velocita' di caduta del livello corrente
            drawPiece = False  # indica se il pezzo e' stato spostato e quindi da ridisegnare
            keystate = pygame.key.get_pressed()  # tasto premuto

            # Spostamento del tetramino
            direction = keystate[K_RIGHT] - keystate[K_LEFT]
            if direction != 0:
                if self.mainboard.move_tetramine(piece, direction):
                    drawPiece = True
                    self.clock.tick(10)

            # Rotazione del tetramino
            if keystate[K_SPACE]:
                if not alreadyRotated:
                    alreadyRotated = True  # per evitare di ruotare continuamente se si tiene premuto il tasto
                    if self.mainboard.rotate_tetramine(piece):
                        drawPiece = True
                        self.clock.tick(30)
            else:
                alreadyRotated = False

            # Cambia la velocita' di caduta
            if keystate[K_DOWN]:
                speed = 30

            # verifico se e' ora di far cadere il tetramino
            if pygame.time.get_ticks() - timeStart >= speed:
                timeStart = pygame.time.get_ticks()
                drawPiece = True
                if self.mainboard.fall_tetramine(piece):  # il tetramino e' sceso
                    # verifica subito se atterrato (solo per sincronizzare il suono con l'immagine)
                    if not self.mainboard.area.can_move_tetramine(piece, TetramineAction.FALL):
                        self.sounds.fall.play()
                else:  # il tetramino non puo' piu' scendere
                    if not piece.is_onboard():  # il tetramino deve rimanere nell'area di gioco per continuare
                        gameOver = True
                        user_message = 'Game Over!'
                        self.sounds.gameover.play()
                    else:
                        self.mainboard.place_tetramine(piece)  # lo fisso sul tabellone
                        piece = self.mainboard.get_new_tetramine()  # recupero il nuovo tetramino da far scendere
                        # verifico le righe completate (partendo dal fondo)
                        bonusMultiLines = 0
                        loopLines = True
                        while loopLines:
                            loopLines = False
                            for i in range(BOARD_LINES - 1, -1, -1):
                                if self.mainboard.try_remove_line(i):
                                    self.mainboard.score += bonusMultiLines
                                    self.sounds.line.play()
                                    self.mainboard.draw_background(self.screen)
                                    pygame.display.flip()
                                    self.clock.tick(10)
                                    if self.mainboard.linesLeft > 0:
                                        loopLines = True  # si analizza il tabellone finche' ci sono righe complete
                                        bonusMultiLines += 10
                                    break
                        # raggiunto l'obiettivo del livello corrente
                        if self.mainboard.linesLeft < 1:
                            gameComplete = True
                            user_message = 'Level Complete!'
                            self.sounds.success.play()
                            pygame.time.wait(2000)
                            self.check_bonus_lines()  # conteggio bonus punti per tutte le righe rimaste vuote
                            drawPiece = False
                            timeStart = pygame.time.get_ticks()

            if drawPiece:
                self.mainboard.draw_background(self.screen)
                self.mainboard.draw_tetramine(self.screen, piece)

            pygame.display.flip()
            self.clock.tick(60)

    # Esegue il conteggio del bonus a livello completato
    def check_bonus_lines(self):
        for row in range(0, BOARD_LINES):
            if self.mainboard.try_add_bonus_line(row):
                self.sounds.bonusline.play()
                self.mainboard.draw_background(self.screen)
                pygame.display.flip()
                self.clock.tick(10)


# -------------------------------------------------------------------------------
if __name__ == '__main__':
    TetrisGame().start()
