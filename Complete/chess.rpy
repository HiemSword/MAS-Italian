

default persistent._mas_chess_stats = {"wins": 0, "losses": 0, "draws": 0}


default persistent._mas_chess_quicksave = ""


default persistent._mas_chess_dlg_actions = {}


default persistent._mas_chess_timed_disable = None


default persistent._mas_chess_3_edit_sorry = False


default persistent._mas_chess_mangle_all = False


default persistent._mas_chess_skip_file_checks = False

define mas_chess.CHESS_SAVE_PATH = "/chess_games/"
define mas_chess.CHESS_SAVE_EXT = ".pgn"
define mas_chess.CHESS_SAVE_NAME = "abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ-_0123456789"
define mas_chess.CHESS_PROMPT_FORMAT = "{0} | {1} | Turn: {2} | You: {3}"


init 1 python in mas_chess:
    import os
    import chess.pgn


    quit_game = False


    REL_DIR = "chess_games/"


    CHESS_MENU_X = 680
    CHESS_MENU_Y = 40
    CHESS_MENU_W = 560
    CHESS_MENU_H = 640
    CHESS_MENU_XALIGN = -0.05
    CHESS_MENU_AREA = (CHESS_MENU_X, CHESS_MENU_Y, CHESS_MENU_W, CHESS_MENU_H)

    CHESS_MENU_NEW_GAME_VALUE = "NEWGAME"
    CHESS_MENU_NEW_GAME_ITEM = (
        "Avvia nuova partita",
        CHESS_MENU_NEW_GAME_VALUE,
        True,
        False
    )

    CHESS_MENU_FINAL_VALUE = "NONE"
    CHESS_MENU_FINAL_ITEM = (
        "Ho cambiato idea",
        CHESS_MENU_FINAL_VALUE,
        False,
        False,
        20
    )

    CHESS_MENU_WAIT_VALUE = "MATTE"
    CHESS_MENU_WAIT_ITEM = (
        "Non posso fare questa decisione in questo momento",
        CHESS_MENU_WAIT_VALUE,
        False,
        False,
        20
    )

    CHESS_NO_GAMES_FOUND = "NOGAMES"


    del_files = (
        "chess.rpyc",
    )


    gt_files = (
        "definitions.rpyc",
        "event-handler.rpyc",
        "script-topics.rpyc",
        "script-introduction.rpyc",
        "script-story-events.rpyc",
        "zz_pianokeys.rpyc",
        "zz_music_selector.rpyc"
    )




    chess_strength = (False, 0)



    CHESS_GAME_CONT = "USHO"



    CHESS_GAME_BACKUP = "foundyou"



    CHESS_GAME_FILE = "file"


    loaded_game_filename = None





    QS_LOST = 0




    QF_LOST_OFCN = 1




    QF_LOST_MAYBE = 2




    QF_LOST_ACDNT = 3




    QF_EDIT_YES = 4



    QF_EDIT_NO = 5




    DLG_QF_LOST_OFCN_ENABLE = True
    DLG_QF_LOST_OFCN_CHOICE = "Certo che no!"


    DLG_QF_LOST_MAY_ENABLE = True
    DLG_QF_LOST_MAY_CHOICE = "Forse..."


    DLG_QF_LOST_ACDNT_ENABLE = True
    DLG_QF_LOST_ACDNT_CHOICE = "E' stato un incidente!"


    DLG_CHESS_LOCKED = "mas_chess_dlg_chess_locked"


    DLG_MONIKA_WIN_BASE = "mas_chess_dlg_game_monika_win_{0}"



    DLG_MONIKA_WIN_SURR_BASE = "mas_chess_dlg_game_monika_win_surr_{0}"


    DLG_MONIKA_LOSE_BASE = "mas_chess_dlg_game_monika_lose_{0}"



    monika_loses_mean_quips = None 



    _monika_loses_line_quips = (
        "Hmph.{w} Sei stato fortunato oggi.",
        "...{w}Sto solo avendo una giornata sfortunata.",
        "Ah, quindi {i}sei{/i} capace di vincere...",
        "Credp che tu non sia {i}così{/i} terribile.",
        "Tch-",
        "Vincere non è tutto,sai...",
        "Ahaha,{w} Ti ho fatto vincere dato che continuavi a perdere così tanto.",
        "Oh, hai vinto.{w} Avrei dovuto prendere questa partita seriamente."
        
    )


    _monika_loses_label_quips = (
        "mas_chess_dlg_game_monika_lose_silly",
    )



    monika_wins_mean_quips = None 



    _monika_wins_line_quips = (
        "Ahaha, ma proprio non sai giocare a scacchi?", 
        "Ma sei {i}così tanto{/i} terribile? Non stavo nemmeno prendendo la partita seriamente ."
    )


    _monika_wins_label_quips = (
        "mas_chess_dlg_game_monika_win_rekt",
    )



    monika_wins_surr_mean_quips = None 


    _monika_wins_surr_line_quips = (
        _monika_wins_line_quips[0],
        (
            "Pensavo avresti riunciato. Non riesci a capire quando " +
            "non hai possibilità."
        ),
    )


    _monika_wins_surr_label_quips = (
        "mas_chess_dlg_game_monika_win_surr_resolve",
        "mas_chess_dlg_game_monika_win_surr_trying"
    )




    def _m1_chess__initDLGActions():
        """
        Initailizes the DLG actions dict and updates the persistent
        appriorpately

        ASSUMES:
            renpy.game.persistent._mas_chess_dlg_actions
        """
        
        
        
        dlg_actions = {
            QS_LOST: 0,
            QF_LOST_OFCN: 0,
            QF_LOST_MAYBE: 0,
            QF_LOST_ACDNT: 0,
            QF_EDIT_YES: 0,
            QF_EDIT_NO: 0
        }
        
        
        if len(dlg_actions) != len(renpy.game.persistent._mas_chess_dlg_actions):
            dlg_actions.update(renpy.game.persistent._mas_chess_dlg_actions)
            renpy.game.persistent._mas_chess_dlg_actions = dlg_actions

    def _initQuipLists(MASQL_class):
        """
        Initializes the mas quiplists.

        IN:
            MASQL_class - the MASQuipList class so we can work with it
                even though we arent global
        """
        
        global monika_loses_mean_quips
        global monika_wins_mean_quips
        global monika_wins_surr_mean_quips
        
        
        monika_loses_mean_quips = MASQL_class()
        
        
        for _line in _monika_loses_line_quips:
            monika_loses_mean_quips.addLineQuip(_line)
        
        
        for _label in _monika_loses_label_quips:
            monika_loses_mean_quips.addLabelQuip(_label)
        
        
        monika_loses_mean_quips.addGlitchQuip(40, 2, 3, True)
        
        
        monika_wins_mean_quips = MASQL_class()
        
        
        for _line in _monika_wins_line_quips:
            monika_wins_mean_quips.addLineQuip(_line)
        
        
        for _label in _monika_wins_label_quips:
            monika_wins_mean_quips.addLabelQuip(_label)
        
        
        monika_wins_surr_mean_quips = MASQL_class()
        
        
        for _line in _monika_wins_surr_line_quips:
            monika_wins_surr_mean_quips.addLineQuip(_line)
        
        
        for _label in _monika_wins_surr_label_quips:
            monika_wins_surr_mean_quips.addLabelQuip(_label)


    def _initMASChess(MASQL_class):
        """
        Initializes mas chess stuff that needs to be initalized

        IN:
            MASQL_class - the MASQuipList class so we can work with it
                even though we arent global
        """
        _m1_chess__initDLGActions()
        
        if renpy.game.persistent._mas_chess_3_edit_sorry:
            _initQuipLists(MASQL_class)


    def _checkInProgressGame(pgn_game, mth):
        """
        Checks if the given pgn game is valid and in progress.

        IN:
            pgn_game - pgn game to check
            mth - monika twitter handle. pass it in since I'm too lazy to
                find context from a store

        RETURNS:
            SEE isInProgressGame
        """
        if pgn_game is None:
            return None
        
        if pgn_game.headers["Result"] != "*":
            return None
        
        
        if pgn_game.headers["White"] == mth:
            the_player = "Black"
        elif pgn_game.headers["Black"] == mth:
            the_player = "White"
        else: 
            return None
        
        
        
        
        board = pgn_game.board()
        for move in pgn_game.main_line():
            board.push(move)
        
        return (
            CHESS_PROMPT_FORMAT.format(
                pgn_game.headers["Date"].replace(".","-"),
                pgn_game.headers["Event"],
                board.fullmove_number,
                the_player
            ),
            pgn_game
        )


    def isInProgressGame(filename, mth):
        """
        Checks if the pgn game with the given filename is valid and
        in progress.

        IN:
            filename - filename of the pgn game
            mth - monika twitter handle. pass it in since I'm too lazy to
                find context from a store

        RETURNS:
            tuple of the following format:
                [0]: Text to display on button
                [1]: chess.pgn.Game of the game
            OR NONE if this is not a valid pgn game
        """
        if filename[-4:] != CHESS_SAVE_EXT:
            return None
        
        pgn_game = None
        with open(
            os.path.normcase(CHESS_SAVE_PATH + filename),
            "r"
        ) as loaded_game:
            pgn_game = chess.pgn.read_game(loaded_game)
        
        return _checkInProgressGame(pgn_game, mth)


init 899 python:

    store.mas_chess._initMASChess(MASQuipList)

init:
    python:
        import chess
        import chess.pgn
        import subprocess
        import platform
        import random
        import pygame
        import threading
        import collections
        import os

        ON_POSIX = 'posix' in sys.builtin_module_names

        def enqueue_output(out, queue, lock):
            for line in iter(out.readline, b''):
                lock.acquire()
                queue.appendleft(line)
                lock.release()
            out.close()


        class ArchitectureError(RuntimeError):
            pass

        def is_platform_good_for_chess():
            import platform
            import sys
            if sys.maxsize > 2**32:
                return platform.system() == 'Windows' or platform.system() == 'Linux' or platform.system() == 'Darwin'
            else:
                return platform.system() == 'Windows'

        def get_mouse_pos():
            vw = config.screen_width * 10000
            vh = config.screen_height * 10000
            pw, ph = renpy.get_physical_size()
            dw, dh = pygame.display.get_surface().get_size()
            mx, my = pygame.mouse.get_pos()
            
            
            
            mx = (mx * pw) / dw
            my = (my * ph) / dh
            
            r = None
            
            
            if vw / (vh / 10000) > pw * 10000 / ph:
                r = vw / pw
                my -= (ph - vh / r) / 2
            else:
                r = vh / ph
                mx -= (pw - vw / r) / 2
            
            newx = (mx * r) / 10000
            newy = (my * r) / 10000
            
            return (newx, newy)


        class ChessException(Exception):
            def __init__(self, msg):
                self.msg = msg
            def __str__(self):
                return self.msg


        if is_platform_good_for_chess():
            
            try:
                file_path = os.path.normcase(
                    config.basedir + mas_chess.CHESS_SAVE_PATH
                )
                if not os.access(file_path, os.F_OK):
                    os.mkdir(file_path)
                mas_chess.CHESS_SAVE_PATH = file_path
            except:
                raise ChessException(
                    "Chess game folder could not be created '{0}'".format(
                        file_path
                    )
                )

        class ChessDisplayable(renpy.Displayable):
            COLOR_WHITE = True
            COLOR_BLACK = False
            MONIKA_WAITTIME = 1500
            MONIKA_OPTIMISM = 33
            MONIKA_THREADS = 1
            
            MOUSE_EVENTS = (
                pygame.MOUSEMOTION,
                pygame.MOUSEBUTTONUP,
                pygame.MOUSEBUTTONDOWN
            )
            
            def __init__(self, player_color, pgn_game=None):
                """
                player_color - player color obvi
                pgn_game - previous game to load (chess.pgn.Game)
                """
                import sys
                
                renpy.Displayable.__init__(self)
                
                
                self.pieces_image = Image("mod_assets/chess_pieces.png")
                self.board_image = Image("mod_assets/chess_board.png")
                self.piece_highlight_red_image = Image("mod_assets/piece_highlight_red.png")
                self.piece_highlight_green_image = Image("mod_assets/piece_highlight_green.png")
                self.piece_highlight_yellow_image = Image("mod_assets/piece_highlight_yellow.png")
                self.piece_highlight_magenta_image = Image("mod_assets/piece_highlight_magenta.png")
                self.move_indicator_player = Image("mod_assets/move_indicator_player.png")
                self.move_indicator_monika = Image("mod_assets/move_indicator_monika.png")
                self.player_move_prompt = Text(_("E' il tuo turno, [player]!"), size=36)
                self.num_turns = 0
                self.surrendered = False
                
                
                self.VECTOR_PIECE_POS = {
                    'K': 0,
                    'Q': 1,
                    'R': 2,
                    'B': 3,
                    'N': 4,
                    'P': 5
                }
                self.BOARD_BORDER_WIDTH = 15
                self.BOARD_BORDER_HEIGHT = 15
                self.PIECE_WIDTH = 57
                self.PIECE_HEIGHT = 57
                self.BOARD_WIDTH = self.BOARD_BORDER_WIDTH * 2 + self.PIECE_WIDTH * 8
                self.BOARD_HEIGHT = self.BOARD_BORDER_HEIGHT * 2 + self.PIECE_HEIGHT * 8
                self.INDICATOR_WIDTH = 60
                self.INDICATOR_HEIGHT = 96
                self.BUTTON_WIDTH = 120
                self.BUTTON_HEIGHT = 35
                self.BUTTON_X_SPACING = 10
                self.BUTTON_Y_SPACING = 10
                
                
                button_idle = Image("mod_assets/hkb_idle_background.png")
                button_hover = Image("mod_assets/hkb_hover_background.png")
                button_no = Image("mod_assets/hkb_disabled_background.png")
                
                
                
                button_text_save_idle = Text(
                    "Save",
                    font=gui.default_font,
                    size=gui.text_size,
                    color="#000",
                    outlines=[]
                )
                button_text_giveup_idle = Text(
                    "Give Up",
                    font=gui.default_font,
                    size=gui.text_size,
                    color="#000",
                    outlines=[]
                )
                button_text_done_idle = Text(
                    "Done",
                    font=gui.default_font,
                    size=gui.text_size,
                    color="#000",
                    outlines=[]
                )
                
                
                button_text_save_hover = Text(
                    "Save",
                    font=gui.default_font,
                    size=gui.text_size,
                    color="#fa9",
                    outlines=[]
                )
                button_text_giveup_hover = Text(
                    "Give Up",
                    font=gui.default_font,
                    size=gui.text_size,
                    color="#fa9",
                    outlines=[]
                )
                button_text_done_hover = Text(
                    "Done",
                    font=gui.default_font,
                    size=gui.text_size,
                    color="#fa9",
                    outlines=[]
                )
                
                
                self.drawn_board_x = int((1280 - self.BOARD_WIDTH) / 2)
                self.drawn_board_y=  int((720 - self.BOARD_HEIGHT) / 2)
                drawn_button_x = (
                    1280 - self.drawn_board_x + self.BUTTON_X_SPACING
                )
                drawn_button_y_top = (
                    720 - (
                        (self.BUTTON_HEIGHT * 2) +
                        self.BUTTON_Y_SPACING +
                        self.drawn_board_y
                    )
                )
                drawn_button_y_bot = (
                    720 - (self.BUTTON_HEIGHT + self.drawn_board_y)
                )
                
                
                self._button_save = MASButtonDisplayable(
                    button_text_save_idle,
                    button_text_save_hover,
                    button_text_save_idle,
                    button_idle,
                    button_hover,
                    button_no,
                    drawn_button_x,
                    drawn_button_y_top,
                    self.BUTTON_WIDTH,
                    self.BUTTON_HEIGHT,
                    hover_sound=gui.hover_sound,
                    activate_sound=gui.activate_sound
                )
                self._button_giveup = MASButtonDisplayable(
                    button_text_giveup_idle,
                    button_text_giveup_hover,
                    button_text_giveup_idle,
                    button_idle,
                    button_hover,
                    button_no,
                    drawn_button_x,
                    drawn_button_y_bot,
                    self.BUTTON_WIDTH,
                    self.BUTTON_HEIGHT,
                    hover_sound=gui.hover_sound,
                    activate_sound=gui.activate_sound
                )
                self._button_done = MASButtonDisplayable(
                    button_text_done_idle,
                    button_text_done_hover,
                    button_text_done_idle,
                    button_idle,
                    button_hover,
                    button_no,
                    drawn_button_x,
                    drawn_button_y_bot,
                    self.BUTTON_WIDTH,
                    self.BUTTON_HEIGHT,
                    hover_sound=gui.activate_sound,
                    activate_sound=gui.activate_sound
                )
                
                
                self._visible_buttons = [
                    self._button_save,
                    self._button_giveup
                ]
                self._visible_buttons_winner = [
                    self._button_save,
                    self._button_done
                ]
                
                
                
                if not is_platform_good_for_chess():
                    
                    raise ArchitectureError('Your operating system does not support the chess game.')
                
                def open_stockfish(path,startupinfo=None):
                    return subprocess.Popen([renpy.loader.transfn(path)], stdin=subprocess.PIPE, stdout=subprocess.PIPE,startupinfo=startupinfo)
                
                is_64_bit = sys.maxsize > 2**32
                if platform.system() == 'Windows':
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                    if is_64_bit:
                        self.stockfish = open_stockfish('mod_assets/stockfish_8_windows_x64.exe',startupinfo)
                    else:
                        self.stockfish = open_stockfish('mod_assets/stockfish_8_windows_x32.exe',startupinfo)
                elif platform.system() == 'Linux' and is_64_bit:
                    os.chmod(config.basedir + '/game/mod_assets/stockfish_8_linux_x64',0755)
                    self.stockfish = open_stockfish('mod_assets/stockfish_8_linux_x64')
                elif platform.system() == 'Darwin' and is_64_bit:
                    os.chmod(config.basedir + '/game/mod_assets/stockfish_8_macosx_x64',0755)
                    self.stockfish = open_stockfish('mod_assets/stockfish_8_macosx_x64')
                
                
                self.stockfish.stdin.write("setoption name Skill Level value %d\n" % (persistent.chess_strength))
                self.stockfish.stdin.write("setoption name Contempt value %d\n" % (self.MONIKA_OPTIMISM))
                
                
                self.queue = collections.deque()
                self.lock = threading.Lock()
                thrd = threading.Thread(target=enqueue_output, args=(self.stockfish.stdout, self.queue, self.lock))
                thrd.daemon = True
                thrd.start()
                
                
                
                
                
                
                
                
                
                self.promolist = ["q","r","n","b","r","k"]
                
                
                
                self.music_menu_open = False
                
                
                
                
                
                
                
                self.board = None
                
                
                if pgn_game:
                    
                    self.board = pgn_game.board()
                    for move in pgn_game.main_line():
                        self.board.push(move)
                    
                    
                    if self.board.turn == chess.WHITE:
                        self.current_turn = self.COLOR_WHITE
                    else:
                        self.current_turn = self.COLOR_BLACK
                    
                    
                    if pgn_game.headers["White"] == mas_monika_twitter_handle:
                        self.player_color = self.COLOR_BLACK
                    else:
                        self.player_color = self.COLOR_WHITE
                    
                    
                    last_move = self.board.peek().uci()
                    self.last_move_src = (
                        ord(last_move[0]) - ord('a'),
                        ord(last_move[1]) - ord('1')
                    )
                    self.last_move_dst = (
                        ord(last_move[2]) - ord('a'),
                        ord(last_move[3]) - ord('1')
                    )
                    
                    
                    self.num_turns = self.board.fullmove_number
                
                else:
                    
                    self.board = chess.Board()
                    
                    
                    self.today_date = datetime.date.today().strftime("%Y.%m.%d")
                    self.start_fen = self.board.fen()
                    
                    
                    self.current_turn = self.COLOR_WHITE
                    
                    
                    self.player_color = player_color
                    
                    
                    self.last_move_src = None
                    self.last_move_dst = None
                
                self.selected_piece = None
                self.possible_moves = set([])
                self.winner = None
                self.last_clicked_king = 0.0
                
                
                self.drawn_button_x = 0
                self.drawn_button_y_top = 0
                self.drawn_button_y_bot = 0
                
                
                
                self.pgn_game = pgn_game
                
                
                if player_color != self.current_turn:
                    self.start_monika_analysis()
                    self._button_save.disable()
                    self._button_giveup.disable()
                elif self.board.fullmove_number <= 4:
                    self._button_save.disable()
            
            def start_monika_analysis(self):
                self.stockfish.stdin.write("position fen %s" % (self.board.fen()) + '\n')
                self.stockfish.stdin.write("go movetime %d" % self.MONIKA_WAITTIME + '\n')
            
            def poll_monika_move(self):
                self.lock.acquire()
                res = None
                while self.queue:
                    line = self.queue.pop()
                    match = re.match(r"^bestmove (\w+)", line)
                    if match:
                        res = match.group(1)
                self.lock.release()
                return res
            
            def __del__(self):
                self.stockfish.stdin.close()
                self.stockfish.wait()
            
            @staticmethod
            def coords_to_uci(x, y):
                x = chr(x + ord('a'))
                y += 1
                return str(x) + str(y)
            
            def check_winner(self, current_move):
                if self.board.is_game_over():
                    if self.board.result() == '1/2-1/2':
                        self.winner = 'none'
                    else:
                        self.winner = current_move
            
            def _quitPGN(self, giveup):
                """
                Generates a pgn of the board, and depending on if we are
                doing previous game or not, does appropriate header
                setting

                IN:
                    giveup - True if the player surrendered, False otherwise

                RETURNS: tuple of the following format:
                    [0]: chess.pgn.Game object of this game
                    [1]: True if monika won, False if not
                    [2]: True if player gaveup, False otherwise
                    [3]: number of turns of this game
                """
                new_pgn = chess.pgn.Game.from_board(self.board)
                
                if giveup:
                    if self.player_color == self.COLOR_WHITE:
                        new_pgn.headers["Result"] = "0-1"
                    else:
                        new_pgn.headers["Result"] = "1-0"
                
                if self.pgn_game:
                    
                    new_pgn.headers["Site"] = self.pgn_game.headers["Site"]
                    new_pgn.headers["Date"] = self.pgn_game.headers["Date"]
                    new_pgn.headers["White"] = self.pgn_game.headers["White"]
                    new_pgn.headers["Black"] = self.pgn_game.headers["Black"]
                    
                    old_fen = self.pgn_game.headers.get("FEN", None)
                    if old_fen:
                        new_pgn.headers["FEN"] = old_fen
                        new_pgn.headers["SetUp"] = "1"
                
                else:
                    
                    
                    if player_color == self.COLOR_WHITE:
                        new_pgn.headers["White"] = persistent.playername
                        new_pgn.headers["Black"] = mas_monika_twitter_handle
                    else:
                        new_pgn.headers["White"] = mas_monika_twitter_handle
                        new_pgn.headers["Black"] = persistent.playername
                    
                    
                    
                    new_pgn.headers["Site"] = "MAS"
                    new_pgn.headers["Date"] = self.today_date
                    new_pgn.headers["FEN"] = self.start_fen
                    new_pgn.headers["SetUp"] = "1"
                
                return (
                    new_pgn,
                    (
                        (
                            new_pgn.headers["Result"] == "1-0"
                            and new_pgn.headers["White"] == mas_monika_twitter_handle
                        ) or (
                            new_pgn.headers["Result"] == "0-1"
                            and new_pgn.headers["Black"] == mas_monika_twitter_handle
                        )
                    ),
                    giveup,
                    self.board.fullmove_number
                )
            
            
            def _inButton(self, x, y, button_x, button_y):
                """
                Checks if the given mouse coordinates is in the given button's
                area.

                IN:
                    x - x coordinate
                    y - y coordinate
                    button_x - x coordinate of the button
                    button_y - y coordinate of the button

                RETURNS:
                    True if the mouse coords are in the button,
                    False otherwise
                """
                return (
                    button_x <= x <= button_x + self.BUTTON_WIDTH
                    and button_y <= y <= button_y + self.BUTTON_HEIGHT
                )
            
            
            def render(self, width, height, st, at):
                
                
                if self.current_turn != self.player_color and not self.winner:
                    monika_move = self.poll_monika_move()
                    if monika_move is not None:
                        self.last_move_src = (ord(monika_move[0]) - ord('a'), ord(monika_move[1]) - ord('1'))
                        self.last_move_dst = (ord(monika_move[2]) - ord('a'), ord(monika_move[3]) - ord('1'))
                        self.board.push_uci(monika_move)
                        if self.current_turn == self.COLOR_BLACK:
                            self.num_turns += 1
                        self.current_turn = self.player_color
                        self.winner = self.board.is_game_over()
                        
                        
                        
                        if not self.winner:
                            self._button_giveup.enable()
                            
                            
                            if self.num_turns > 4:
                                self._button_save.enable()
                
                
                r = renpy.Render(width, height)
                
                
                board = renpy.render(self.board_image, 1280, 720, st, at)
                
                
                pieces = renpy.render(self.pieces_image, 1280, 720, st, at)
                
                
                highlight_red = renpy.render(self.piece_highlight_red_image, 1280, 720, st, at)
                highlight_green = renpy.render(self.piece_highlight_green_image, 1280, 720, st, at)
                highlight_yellow = renpy.render(self.piece_highlight_yellow_image, 1280, 720, st, at)
                highlight_magenta = renpy.render(self.piece_highlight_magenta_image, 1280, 720, st, at)
                
                
                mx, my = get_mouse_pos()
                
                
                
                
                
                visible_buttons = list()
                if self.winner:
                    
                    
                    visible_buttons = [
                        (b.render(width, height, st, at), b.xpos, b.ypos)
                        for b in self._visible_buttons_winner
                    ]
                
                else:
                    
                    
                    visible_buttons = [
                        (b.render(width, height, st, at), b.xpos, b.ypos)
                        for b in self._visible_buttons
                    ]
                
                
                r.blit(board, (self.drawn_board_x, self.drawn_board_y))
                indicator_position = (int((width - self.INDICATOR_WIDTH) / 2 + self.BOARD_WIDTH / 2 + 50),
                                      int((height - self.INDICATOR_HEIGHT) / 2))
                
                
                if self.current_turn == self.player_color:
                    r.blit(renpy.render(self.move_indicator_player, 1280, 720, st, at), indicator_position)
                else:
                    r.blit(renpy.render(self.move_indicator_monika, 1280, 720, st, at), indicator_position)
                
                
                for b in visible_buttons:
                    r.blit(b[0], (b[1], b[2]))
                
                def get_piece_render_for_letter(letter):
                    jy = 0 if letter.islower() else 1
                    jx = self.VECTOR_PIECE_POS[letter.upper()]
                    return pieces.subsurface((jx * self.PIECE_WIDTH, jy * self.PIECE_HEIGHT,
                                              self.PIECE_WIDTH, self.PIECE_HEIGHT))
                
                
                for ix in range(8):
                    for iy in range(8):
                        iy_orig = iy
                        ix_orig = ix
                        if self.player_color == self.COLOR_WHITE:
                            iy = 7 - iy
                        else: 
                            ix = 7 - ix
                        x = int((width - (self.BOARD_WIDTH - self.BOARD_BORDER_WIDTH * 2)) / 2  + ix * self.PIECE_WIDTH)
                        y = int((height - (self.BOARD_HEIGHT - self.BOARD_BORDER_HEIGHT * 2)) / 2 + iy * self.PIECE_HEIGHT)
                        
                        def render_move(move):
                            if move is not None and ix_orig == move[0] and iy_orig == move[1]:
                                if self.player_color == self.current_turn:
                                    r.blit(highlight_magenta, (x, y))
                                else:
                                    r.blit(highlight_green, (x, y))
                        
                        render_move(self.last_move_src)
                        render_move(self.last_move_dst)
                        
                        
                        if (self.selected_piece is not None and
                            ix_orig == self.selected_piece[0] and
                            iy_orig == self.selected_piece[1]):
                            r.blit(highlight_green, (x, y))
                            continue
                        
                        piece = self.board.piece_at(iy_orig * 8 + ix_orig)
                        
                        possible_move_str = None
                        blit_rendered = False
                        if self.possible_moves:
                            possible_move_str = (ChessDisplayable.coords_to_uci(self.selected_piece[0], self.selected_piece[1]) +
                                                 ChessDisplayable.coords_to_uci(ix_orig, iy_orig))
                            if chess.Move.from_uci(possible_move_str) in self.possible_moves:
                                r.blit(highlight_yellow, (x, y))
                                blit_rendered = True
                            
                            
                            if not blit_rendered and (iy == 0 or iy == 7):
                                index = 0
                                while (not blit_rendered
                                        and index < len(self.promolist)):
                                    
                                    if (chess.Move.from_uci(
                                        possible_move_str + self.promolist[index])
                                        in self.possible_moves):
                                        r.blit(highlight_yellow, (x, y))
                                        blit_rendered = True
                                    
                                    index += 1
                        
                        if piece is None:
                            continue
                        
                        if (mx >= x and mx < x + self.PIECE_WIDTH and
                            my >= y and my < y + self.PIECE_HEIGHT and
                            bool(str(piece).isupper()) == (self.player_color == self.COLOR_WHITE) and
                            self.current_turn == self.player_color and
                            self.selected_piece is None and
                            not self.winner):
                            r.blit(highlight_green, (x, y))
                        
                        if self.winner:
                            result = self.board.result()
                            
                            
                            if str(piece) == "K" and result == "0-1":
                                r.blit(highlight_red, (x, y))
                            
                            
                            elif str(piece) == "k" and result == "1-0":
                                r.blit(highlight_red, (x, y))
                        
                        r.blit(get_piece_render_for_letter(str(piece)), (x, y))
                
                
                if self.current_turn == self.player_color and not self.winner:
                    
                    prompt = renpy.render(self.player_move_prompt, 1280, 720, st, at)
                    pw, ph = prompt.get_size()
                    bh = (height - self.BOARD_HEIGHT) / 2
                    r.blit(prompt, (int((width - pw) / 2), int(self.BOARD_HEIGHT + bh + (bh - ph) / 2)))
                
                if self.selected_piece is not None:
                    
                    piece = self.board.piece_at(self.selected_piece[1] * 8 + self.selected_piece[0])
                    assert piece is not None
                    px, py = get_mouse_pos()
                    px -= self.PIECE_WIDTH / 2
                    py -= self.PIECE_HEIGHT / 2
                    r.blit(get_piece_render_for_letter(str(piece)), (px, py))
                
                
                renpy.redraw(self, 0)
                
                
                
                return r
            
            
            def event(self, ev, x, y, st):
                
                
                if ev.type in self.MOUSE_EVENTS:
                    
                    
                    
                    if self.winner:
                        
                        if self._button_done.event(ev, x, y, st):
                            
                            return self._quitPGN(False)
                    
                    
                    elif self.current_turn == self.player_color:
                        
                        if self._button_save.event(ev, x, y, st):
                            
                            return self._quitPGN(False)
                        
                        elif self._button_giveup.event(ev, x, y, st):
                            renpy.call_in_new_context("mas_chess_confirm_context")
                            if mas_chess.quit_game:
                                
                                return self._quitPGN(True)
                
                def get_piece_pos():
                    mx, my = get_mouse_pos()
                    mx -= (1280 - (self.BOARD_WIDTH - self.BOARD_BORDER_WIDTH * 2)) / 2
                    my -= (720 - (self.BOARD_HEIGHT - self.BOARD_BORDER_HEIGHT * 2)) / 2
                    px = mx / self.PIECE_WIDTH
                    py = my / self.PIECE_HEIGHT
                    if self.player_color == self.COLOR_WHITE:
                        py = 7 - py
                    else: 
                        px = 7 - px
                    if py >= 0 and py < 8 and px >= 0 and px < 8:
                        return (px, py)
                    return (None, None)
                
                
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    px, py = get_piece_pos()
                    if (
                            px is not None
                            and py is not None
                            and self.board.piece_at(py * 8 + px) is not None
                            and bool(str(self.board.piece_at(py * 8 + px)).isupper())
                                == (self.player_color == self.COLOR_WHITE)
                            and self.current_turn == self.player_color
                        ):
                        
                        piece = str(self.board.piece_at(py * 8 + px))
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        self.possible_moves = self.board.legal_moves
                        self.selected_piece = (px, py)
                
                
                if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                    px, py = get_piece_pos()
                    if px is not None and py is not None and self.selected_piece is not None:
                        move_str = self.coords_to_uci(self.selected_piece[0], self.selected_piece[1]) + self.coords_to_uci(px, py)
                        
                        piece = str(
                            self.board.piece_at(
                                self.selected_piece[1] * 8 +
                                self.selected_piece[0]
                            )
                        )
                        
                        if piece.lower() == 'p' and (py == 0 or py == 7):
                            move_str += "q"
                        if chess.Move.from_uci(move_str) in self.possible_moves:
                            self.last_move_src = self.selected_piece
                            self.last_move_dst = (px, py)
                            self.board.push_uci(move_str)
                            
                            self.winner = self.board.is_game_over()
                            if self.current_turn == self.COLOR_BLACK:
                                self.num_turns += 1
                            self.current_turn = not self.current_turn
                            if not self.winner:
                                self.start_monika_analysis()
                            
                            
                            self._button_save.disable()
                            self._button_giveup.disable()
                    
                    self.selected_piece = None
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    self.possible_moves = set([])
                
                
                if ev.type == pygame.KEYUP:
                    
                    
                    if ev.key == pygame.K_m:
                        
                        
                        if ev.mod & pygame.KMOD_SHIFT:
                            mute_music()
                        elif not self.music_menu_open:
                            self.music_menu_open = True
                            select_music()
                        else: 
                            self.music_menu_open = False
                    
                    
                    if (ev.key == pygame.K_PLUS
                            or ev.key == pygame.K_EQUALS
                            or ev.key == pygame.K_KP_PLUS):
                        inc_musicvol()
                    
                    
                    if (ev.key == pygame.K_MINUS
                            or ev.key == pygame.K_UNDERSCORE
                            or ev.key == pygame.K_KP_MINUS):
                        dec_musicvol()
                
                raise renpy.IgnoreEvent()

label game_chess:
    if persistent._mas_chess_timed_disable is not None:
        call mas_chess_dlg_chess_locked from _mas_chess_dclgc
        return

    hide screen keylistener

    m 1eub "Vuoi giocare a scacchi? Va bene~"


    call demo_minigame_chess from _call_demo_minigame_chess
    return

label demo_minigame_chess:
    $ import store.mas_chess as mas_chess
    $ loaded_game = None
    $ ur_nice_today = True

    if persistent._mas_chess_timed_disable is not None:
        call mas_chess_dlg_chess_locked from _mas_chess_dcldmc
        return

    if not renpy.seen_label("mas_chess_save_selected"):
        call mas_chess_save_migration from _mas_chess_savemg


        if not _return:
            return


        elif _return == mas_chess.CHESS_NO_GAMES_FOUND:
            jump mas_chess_new_game_start


        $ loaded_game = _return




    elif len(persistent._mas_chess_quicksave) > 0:

        python:
            import StringIO 
            import chess.pgn
            import os

            quicksaved_game = chess.pgn.read_game(
                StringIO.StringIO(persistent._mas_chess_quicksave)
            )

            quicksaved_game = mas_chess._checkInProgressGame(
                quicksaved_game,
                mas_monika_twitter_handle
            )


        if quicksaved_game is None:
            $ ur_nice_today = False

            if persistent._mas_chess_3_edit_sorry:
                call mas_chess_dlg_qf_edit_n_3_n_qs from _mas_chess_dlgqfeditn3nqs

                $ persistent._mas_chess_quicksave = ""

                if _return is not None:
                    return
            else:

                python:
                    import os
                    import struct


                    pgn_files = os.listdir(mas_chess.CHESS_SAVE_PATH)
                    if pgn_files:
                        
                        
                        valid_files = list()
                        for filename in pgn_files:
                            in_prog_game = mas_chess.isInProgressGame(
                                filename,
                                mas_monika_twitter_handle
                            )
                            
                            if in_prog_game:
                                valid_files.append((filename, in_prog_game[1]))
                        
                        
                        if len(valid_files) > 0:
                            for filename,pgn_game in valid_files:
                                store._mas_root.mangleFile(
                                    mas_chess.CHESS_SAVE_PATH + filename,
                                    mangle_length=len(str(pgn_game))*2
                                )

                $ persistent._mas_chess_quicksave = ""


                call mas_chess_dlg_qs_lost from _mas_chess_dql_main


                if _return is not None:
                    return

            jump mas_chess_new_game_start


        if persistent._mas_chess_skip_file_checks:
            $ loaded_game = quicksaved_game[1]
            m "Continuiamo la partita che abbiamo lasciato in sospeso."
            jump mas_chess_game_load_check


        python:
            quicksaved_game = quicksaved_game[1]

            quicksaved_filename = (
                quicksaved_game.headers["Event"] + mas_chess.CHESS_SAVE_EXT
            )
            quicksaved_filename_clean = (
                mas_chess.CHESS_SAVE_PATH + quicksaved_filename
            ).replace("\\", "/")

            try:
                if os.access(quicksaved_filename_clean, os.R_OK):
                    quicksaved_file = mas_chess.isInProgressGame(
                        quicksaved_filename,
                        mas_monika_twitter_handle
                    )
                else:
                    store.mas_utils.writelog("Failed to access quickfile.\n")
                    quicksaved_file = None
            except Exception as e:
                store.mas_utils.writelog("QUICKFILE: " + str(e) + "\n")
                quicksaved_file = None


        if quicksaved_file is None:
            $ ur_nice_today = False

            python:

                mas_chess.loaded_game_filename = quicksaved_filename_clean

            call mas_chess_dlg_qf_lost from _mas_chess_dql_main2


            if _return == mas_chess.CHESS_GAME_CONT:
                python:
                    try:
                        if os.access(quicksaved_filename_clean, os.R_OK):
                            quicksaved_file = mas_chess.isInProgressGame(
                                quicksaved_filename,
                                mas_monika_twitter_handle
                            )
                        else:
                            store.mas_utils.writelog(
                                "Failed to access quickfile.\n"
                            )
                            quicksaved_file = None
                    except Exception as e:
                        store.mas_utils.writelog(
                            "QUICKFILE: " + str(e) + "\n"
                        )
                        quicksaved_file = None

                if quicksaved_file is None:
                    call mas_chess_dlg_qf_lost_may_removed from _mas_chess_dqlqfr
                    return


            elif _return == mas_chess.CHESS_GAME_BACKUP:
                $ loaded_game = quicksaved_game
                jump mas_chess_game_load_check
            else:



                $ persistent._mas_chess_quicksave = ""


                if _return is not None:
                    return


                jump mas_chess_new_game_start

        python:


            quicksaved_file = quicksaved_file[1]


            is_same = str(quicksaved_game) == str(quicksaved_file)

        if not is_same:

            $ ur_nice_today = False

            call mas_chess_dlg_qf_edit from _mas_chess_dql_main3


            if _return == mas_chess.CHESS_GAME_BACKUP:
                $ loaded_game = quicksaved_game
                jump mas_chess_game_load_check


            elif _return == mas_chess.CHESS_GAME_FILE:
                $ loaded_game = quicksaved_file
                jump mas_chess_game_load_check


            python:
                persistent._mas_chess_quicksave = ""
                try:
                    os.remove(quicksaved_filename_clean)
                except:
                    pass


            if _return is not None:
                return


            jump mas_chess_new_game_start
        else:




            $ loaded_game = quicksaved_game

            if ur_nice_today:


                m 1eua "Abbiamo ancora una partita in sospeso."
            m "Preparati!"

label mas_chess_game_load_check:

    if loaded_game:

        if loaded_game.headers["White"] == mas_monika_twitter_handle:
            $ player_color = ChessDisplayable.COLOR_BLACK
        else:
            $ player_color = ChessDisplayable.COLOR_WHITE
        jump mas_chess_game_start

label mas_chess_new_game_start:

    if persistent._mas_chess_timed_disable is not None:
        call mas_chess_dlg_chess_locked from _mas_chess_dclngs
        return

    m "Che colore scegli?{nw}"
    $ _history_list.pop()
    menu:
        m "Che colore scegli?{fast}"
        "Bianco.":

            $ player_color = ChessDisplayable.COLOR_WHITE
        "nero.":
            $ player_color = ChessDisplayable.COLOR_BLACK
        "Allora facciamo a sorteggio!":
            $ choice = random.randint(0, 1) == 0
            if choice:
                $ player_color = ChessDisplayable.COLOR_WHITE
                m 2eua "Oh guarda, ho estratto nero! Cominciamo!"
            else:
                $ player_color = ChessDisplayable.COLOR_BLACK
                m 2eua "Oh guarda, ho estratto bianco! Cominciamo!"

label mas_chess_game_start:
    window hide None

    if persistent._mas_chess_timed_disable is not None:
        call mas_chess_dlg_chess_locked from _mas_chess_dclgs
        return

    python:
        ui.add(ChessDisplayable(player_color, pgn_game=loaded_game))
        results = ui.interact(suppress_underlay=True)


        new_pgn_game, is_monika_winner, is_surrender, num_turns = results


        game_result = new_pgn_game.headers["Result"]


        if mas_chess.chess_strength[0]:
            persistent.chess_strength = mas_chess.chess_strength[1]
            mas_chess.chess_strength = (False, 0)






    if game_result == "*":


        call mas_chess_dlg_game_in_progress from _mas_chess_dlggameinprog

        jump mas_chess_savegame

    elif game_result == "1/2-1/2":

        call mas_chess_dlg_game_drawed from _mas_chess_dlggamedrawed
        $ persistent._mas_chess_stats["draws"] += 1

    elif is_monika_winner:
        $ persistent._mas_chess_stats["losses"] += 1
        if is_surrender and num_turns <= 4:


            call mas_chess_dlg_game_monika_win_surr from _mas_chess_dlggmws
        else:


            call mas_chess_dlg_game_monika_win from _mas_chess_dlggmw


        $ persistent.chess_strength -= 1
    else:

        $ persistent._mas_chess_stats["wins"] += 1


        if not persistent.ever_won['chess']:
            $ persistent.ever_won['chess'] = True
            $ grant_xp(xp.WIN_GAME)


        call mas_chess_dlg_game_monika_lose from _mas_chess_dlggml

        $ persistent.chess_strength += 1


    m 1eua "Comunque..."


    if loaded_game:
        jump mas_chess_savegame


    if num_turns > 4:
        m "Vuoi salvare questa partita?{nw}"
        $ _history_list.pop()
        menu:
            m "Vuoi salvare questa partita?{fast}"
            "Yes.":
                jump mas_chess_savegame
            "No.":

                pass

label mas_chess_playagain:
    m "Vuoi giocare di nuovo?{nw}"
    $ _history_list.pop()
    menu:
        m "Vuoi giocare di nuovo?{fast}"
        "Sì.":

            jump mas_chess_new_game_start
        "No.":
            pass

label mas_chess_end:
    $ mas_gainAffection(modifier=0.5)

    if is_monika_winner:
        if renpy.seen_label("mas_chess_dlg_game_monika_win_end"):
            call mas_chess_dlg_game_monika_win_end_quick from _mas_chess_dgmwequick
        else:
            call mas_chess_dlg_game_monika_win_end from _mas_chess_dgmwelong


    elif game_result == "*":
        if renpy.seen_label("mas_chess_dlg_game_in_progress_end"):
            call mas_chess_dlg_game_in_progress_end_quick from _mas_chess_dgmipequick
        else:
            call mas_chess_dlg_game_in_progress_end from _mas_chess_dgmipelong
    else:


        if renpy.seen_label("mas_chess_dlg_game_monika_lose_end"):
            call mas_chess_dlg_game_monika_lose_end_quick from _mas_chess_dgmlequick
        else:
            call mas_chess_dlg_game_monika_lose_end from _mas_chess_dgmlelong

    return


label mas_chess_confirm_context:
    call screen mas_chess_confirm
    $ store.mas_chess.quit_game = _return
    return


label mas_chess_save_migration:
    python:
        import chess.pgn
        import os
        import store.mas_chess as mas_chess

        pgn_files = os.listdir(mas_chess.CHESS_SAVE_PATH)
        sel_game = (mas_chess.CHESS_NO_GAMES_FOUND,)

    if pgn_files:
        python:

            pgn_games = list()
            actual_pgn_games = list()
            game_dex = 0
            for filename in pgn_files:
                in_prog_game = mas_chess.isInProgressGame(
                    filename,
                    mas_monika_twitter_handle
                )
                
                if in_prog_game:
                    pgn_games.append((
                        in_prog_game[0],
                        game_dex,
                        False,
                        False
                    ))
                    actual_pgn_games.append((in_prog_game[1], filename))
                    game_dex += 1

            game_count = len(pgn_games)
            pgn_games.sort()
            pgn_games.reverse()


        if game_count > 1:
            if renpy.seen_label("mas_chess_save_multi_dlg"):
                $ pick_text = "Devi scegliere una partita da tenere."
            else:
                label mas_chess_save_multi_dlg:
                    m 1m "Stavo pensando, [player]..."
                    m "Molte persone che lasciano partite incomplete e non le continuano più."
                    m 1n "Per me non ha senso salvare più di una partita incompleta."
                    m 1p "E dato che abbiamo [game_count] partite non finite..."
                    m 1g "Devo chiederti di tenerne solo una.{w} Mi spiace, [player]."
                    $ pick_text = "Scegli una partita da tenere."
            show monika 1e at t21
            $ renpy.say(m, pick_text, interact=False)

            call screen mas_gen_scrollable_menu(pgn_games, mas_chess.CHESS_MENU_AREA, mas_chess.CHESS_MENU_XALIGN, mas_chess.CHESS_MENU_WAIT_ITEM)

            show monika at t11
            if _return == mas_chess.CHESS_MENU_WAIT_VALUE:

                m 2dsc "Capisco."
                m 2eua "In questo caso, prenditi il tuo tempo."
                m 1eua "Giocheremo di nuovo a scacchi quando avrai scelto."
                return False
            else:

                m 1eua "Va bene."
                python:
                    sel_game = actual_pgn_games.pop(_return)
                    for pgn_game in actual_pgn_games:
                        try:
                            os.remove(os.path.normcase(
                                mas_chess.CHESS_SAVE_PATH + pgn_game[1]
                            ))
                        except:
                            pass


        elif game_count == 1:
            $ sel_game = actual_pgn_games[0]


label mas_chess_save_selected:
    return sel_game[0]

label mas_chess_savegame:
    if loaded_game:
        python:
            new_pgn_game.headers["Event"] = (
                loaded_game.headers["Event"]
            )


            save_filename = (
                new_pgn_game.headers["Event"] +
                mas_chess.CHESS_SAVE_EXT
            )


            file_path = mas_chess.CHESS_SAVE_PATH + save_filename


            loaded_game = None
    else:


        python:

            save_name = ""
            while len(save_name) == 0:
                save_name = renpy.input(
                    "inserisci un nome per questa partita:",
                    allow=mas_chess.CHESS_SAVE_NAME,
                    length=15
                )
            new_pgn_game.headers["Event"] = save_name


            save_filename = save_name + mas_chess.CHESS_SAVE_EXT

            file_path = mas_chess.CHESS_SAVE_PATH + save_filename


            is_file_exist = os.access(
                os.path.normcase(file_path),
                os.F_OK
            )


        if is_file_exist:
            m 1eka "abbiamo già un partita salvata come '[save_name].'"

            m "Devo sovrascriverla?{nw}"
            $ _history_list.pop()
            menu:
                m "Devo sovrascriverla?{fast}"
                "Yes.":
                    pass
                "No.":
                    jump mas_chess_savegame

    python:

        with open(file_path, "w") as pgn_file:
            pgn_file.write(str(new_pgn_game))


        if new_pgn_game.headers["Result"] == "*":
            persistent._mas_chess_quicksave = str(new_pgn_game)
        else:
            persistent._mas_chess_quicksave = ""


        display_file_path = mas_chess.REL_DIR + save_filename

    m 1dsc ".{w=0.5}.{w=0.5}.{nw}"
    m 1hua "Ho salvato la nostra partita su '[display_file_path]'!"

    if not renpy.seen_label("mas_chess_pgn_explain"):

        label mas_chess_pgn_explain:
            m 1eua "E' in un formato chiamato 'Portable Game Notation'."
            m "Puoi aprire questo file come PNG."

            if game_result == "*":
                m 1lksdlb "E' anche possibile modificare il file e cambiare l' esito della partita,{w} ma sono sicura che non lo."

                m 1eka "Vero, [player]?{nw}"
                $ _history_list.pop()
                menu:
                    m "Vero, [player]?{fast}"
                    "Certo che no.":
                        m 1hua "Yay~"

    if game_result == "*":
        jump mas_chess_end

    jump mas_chess_playagain





label mas_chess_dlg_qs_lost:
    python:
        import store.mas_chess as mas_chess
        persistent._mas_chess_dlg_actions[mas_chess.QS_LOST] += 1
        qs_gone_count = persistent._mas_chess_dlg_actions[mas_chess.QS_LOST]

    call mas_chess_dlg_qs_lost_start from _mas_chess_dqsls

    if qs_gone_count == 2:
        call mas_chess_dlg_qs_lost_2 from _mas_chess_dlgqslost2

    elif qs_gone_count == 3:
        call mas_chess_dlg_qs_lost_3 from _mas_chess_dlgqslost3

    elif qs_gone_count % 5 == 0:
        call mas_chess_dlg_qs_lost_5r from _mas_chess_dlgqslost5r

    elif qs_gone_count % 7 == 0:
        call mas_chess_dlg_qs_lost_7r from _mas_chess_dlgqslost7r
    else:

        call mas_chess_dlg_qs_lost_gen from _mas_chess_dlgqslostgen

    return _return


label mas_chess_dlg_qs_lost_start:
    m 2lksdlb "Uh, [player]...{w} Sembra che sia successo qualcosa quando ho salvato la partita."
    return


label mas_chess_dlg_qs_lost_gen:
    m 1lksdlc "Mi spiace..."
    m 3eksdla "Iniziamo, invece, una nuova partita."
    return


label mas_chess_dlg_qs_lost_2:
    m 1lksdld "Sono davvero molto dispiaciuta, [player]."
    m "Cercherò di farmi perdonare."
    show monika 1ekc
    pause 1.0
    m 1dsc "E lo farò..."
    m 3eua "...creando una nuova partita!"
    return


label mas_chess_dlg_qs_lost_3:
    m 1lksdlc "Sono davvero maldestra, [player]...{w}Mi spiace."
    m 3eksdla "Cominciamo, invece, una nuova partita."
    return


label mas_chess_dlg_qs_lost_5r:
    m 2esc "E' successo [qs_gone_count] volte finora..."
    m 2tsc "Mi chiedo se sia una conseguenda del provare di {cps=*0.75}{i}qualcuno{/i}{/cps} a modificare i salvataggi.{w=1}.{w=1}."
    m 1esd "comunque..."
    m "cominciamo una nuova partita."
    show monika 1esc
    return


label mas_chess_dlg_qs_lost_7r:
    jump mas_chess_dlg_qs_lost_3



label mas_chess_dlg_qf_lost:
    python:
        import store.mas_chess as mas_chess

    call mas_chess_dlg_qf_lost_start from _mas_chess_dqfls

    m "Hai modificato i salvataggi, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Hai modificato i salvataggi, [player]?{fast}"
        "[mas_chess.DLG_QF_LOST_OFCN_CHOICE]" if mas_chess.DLG_QF_LOST_OFCN_ENABLE:
            call mas_chess_dlg_qf_lost_ofcn_start from _mas_chess_dlgqflostofcnstart

        "[mas_chess.DLG_QF_LOST_MAY_CHOICE]" if mas_chess.DLG_QF_LOST_MAY_ENABLE:
            call mas_chess_dlg_qf_lost_may_start from _mas_chess_dlgqflostmaystart

        "[mas_chess.DLG_QF_LOST_ACDNT_CHOICE]" if mas_chess.DLG_QF_LOST_ACDNT_ENABLE:
            call mas_chess_dlg_qf_lost_acdnt_start from _mas_chess_dlgqflostacdntstart

    return _return


label mas_chess_dlg_qf_lost_start:
    m 2lksdla "Beh,{w} è imbarazzante."
    m "Ricordo che dovevamo finre una partita, ma non riesco a trovare i file di salvataggio."
    return


label mas_chess_dlg_qf_lost_ofcn_start:
    python:
        import store.mas_chess as mas_chess
        persistent._mas_chess_dlg_actions[mas_chess.QF_LOST_OFCN] += 1
        qf_gone_count = persistent._mas_chess_dlg_actions[mas_chess.QF_LOST_OFCN]

    if qf_gone_count == 3:
        call mas_chess_dlg_qf_lost_ofcn_3 from _mas_chess_dlgqflostofcn3

    elif qf_gone_count == 4:
        call mas_chess_dlg_qf_lost_ofcn_4 from _mas_chess_dlgqflostofcn4

    elif qf_gone_count == 5:
        call mas_chess_dlg_qf_lost_ofcn_5 from _mas_chess_dlgqflostofcn5

    elif qf_gone_count >= 6:
        call mas_chess_dlg_qf_lost_ofcn_6 from _mas_chess_dlgqflostofcn6
    else:

        call mas_chess_dlg_qf_lost_ofcn_gen from _mas_chess_dlgqflostofcngen

    return _return


label mas_chess_dlg_qf_lost_ofcn_gen:
    m 1lksdlb "Ah, già. Non me lo faresti."
    m "Dovrei aver confuso i file."
    m 1lksdlc "Scusa, [player]."
    m "Mi farò perdonare..."
    m 1eua "Cominciando una nuova partita!"
    return


label mas_chess_dlg_qf_lost_ofcn_3:
    m 2esc "..."
    m "[player],{w} hai..."
    m 2dsc "Non importa."
    m 1esc "Cominciamo una nuova partita."
    return


label mas_chess_dlg_qf_lost_ofcn_4:
    jump mas_chess_dlg_qf_lost_ofcn_3


label mas_chess_dlg_qf_lost_ofcn_5:
    $ mas_loseAffection()
    m 2esc "..."
    m "[player],{w} Sta succedento troppe volte."
    m 2dsc "Stavolta non ti credo."
    pause 2.0
    m 2esc "Spero che non ti stia prendendo gioco di me."
    m "..."
    m 1esc "Non importa.{w} Cominciamo una nuova partita."
    return


label mas_chess_dlg_qf_lost_ofcn_6:






    $ mas_loseAffection(modifier=10)
    $ persistent.game_unlocks["chess"] = False

    $ persistent._seen_ever["unlock_chess"] = True

    m 2dfc "..."
    m 2efc "[player],{w} Non ti credo."
    m 2efd "Se fai così con tutte le nostre partite..."
    m 6wfw "Allora non voglio più giocare a scacchi con te!"
    return True


label mas_chess_dlg_qf_lost_may_start:
    python:
        import store.mas_chess as mas_chess
        persistent._mas_chess_dlg_actions[mas_chess.QF_LOST_MAYBE] += 1
        qf_gone_count = persistent._mas_chess_dlg_actions[mas_chess.QF_LOST_MAYBE]

    if qf_gone_count == 2:
        call mas_chess_dlg_qf_lost_may_2 from _mas_chess_dlgqflostmay2

    elif qf_gone_count >= 3:
        call mas_chess_dlg_qf_lost_may_3 from _mas_chess_dlgqflostmay3
    else:

        call mas_chess_dlg_qf_lost_may_gen from _mas_chess_dlgqflostmaygen

    return _return



label mas_chess_dlg_qf_lost_may_gen:
    m 2ekd "[player]!{w} Avrei dovuto capire che mi stavi prendendo in giro!"
    jump mas_chess_dlg_qf_lost_may_filechecker


label mas_chess_dlg_qf_lost_may_gen_found:
    m 2eua "Oh!"
    m 1hua "Ecco il salvataggio.{w} Grazie di averlo rimesso, [player]."
    m 1eua "Ora possiamo continuare la partita."
    return store.mas_chess.CHESS_GAME_CONT


label mas_chess_dlg_qf_lost_may_2:
    m 2ekd "[player]!{w} Smettila di prenderti gioco di me!"
    jump mas_chess_dlg_qf_lost_may_filechecker


label mas_chess_dlg_qf_lost_may_2_found:
    jump mas_chess_dlg_qf_lost_may_gen_found


label mas_chess_dlg_qf_lost_may_filechecker:
    $ import os
    $ import store.mas_chess as mas_chess
    $ game_file = mas_chess.loaded_game_filename

    if os.access(game_file, os.F_OK):
        jump mas_chess_dlg_qf_lost_may_gen_found

    m 1eka "Puoi rimettere a posto il file così che possiamo continuarea giocare?"
    if os.access(game_file, os.F_OK):
        jump mas_chess_dlg_qf_lost_may_gen_found

    show monika 1eua


    python:
        renpy.say(m, "Aspetterò un minuto...", interact=False)
        file_found = False
        seconds = 0
        while not file_found and seconds < 60:
            if os.access(game_file, os.F_OK):
                file_found = True
            else:
                renpy.pause(1.0, hard=True)
                seconds += 1

    if file_found:
        m 1hua "Yay!{w} grazie di averlo rimesso, [player]."
        m "Ora possiamo continuare la partita."
        show monika 1eua
        return mas_chess.CHESS_GAME_CONT


    m 1ekd "[player]..."
    m 1eka "Va bene. Cominciamo una nuova partita."
    return


label mas_chess_dlg_qf_lost_may_3:
    $ persistent._mas_chess_skip_file_checks = True

    m 2ekd "[player]! Questo--"
    m 2dkc "..."
    m 1esa "...non è per niente un problema."
    m "sapevo che lo avresti rifatto..."
    m 1hub "...perciò ho fatto un backup del file!"

    m 1eua "Non mi puoi più mentire, [player]."
    m "Ora continuiamo a giocare."
    return store.mas_chess.CHESS_GAME_BACKUP


label mas_chess_dlg_qf_lost_may_removed:
    $ import datetime
    $ persistent._mas_chess_timed_disable = datetime.datetime.now()
    $ mas_loseAffection(modifier=0.5)

    m 2wfw "[player]!"
    m 2wfx "Hai di nuovo cancellato il file."
    pause 0.7
    m 2rfc "Giocheremo a scacchi un'altra volta, allora."
    return True


label mas_chess_dlg_qf_lost_acdnt_start:
    python:
        import store.mas_chess as mas_chess
        persistent._mas_chess_dlg_actions[mas_chess.QF_LOST_ACDNT] += 1
        qf_gone_count = persistent._mas_chess_dlg_actions[mas_chess.QF_LOST_ACDNT]

    if qf_gone_count == 2:
        call mas_chess_dlg_qf_lost_acdnt_2 from _mas_chess_dlgqflostacdnt2

    elif qf_gone_count >= 3:
        call mas_chess_dlg_qf_lost_acdnt_3 from _mas_chess_dlgqflostacdnt3
    else:

        call mas_chess_dlg_qf_lost_acdnt_gen from _mas_chess_dlgqflostacdntgen

    return _return


label mas_chess_dlg_qf_lost_acdnt_gen:
    m 1eka "[player]..."
    m "Va bene.{w} Gli incidenti accadono a tutti."
    m 1eua "Cominciamo una nuova partita."
    return


label mas_chess_dlg_qf_lost_acdnt_2:
    m 1eka "Di nuovo? Non essere così imbranato, [player]."
    m 1hua "Non importa."
    m "Giocheremo ad una nuova partita, allora."
    show monika 1eua
    return


label mas_chess_dlg_qf_lost_acdnt_3:
    $ persistent._mas_chess_skip_file_checks = True

    m 1eka "Avevo la sensazione che sarebbe accaduto di nuovo."
    m 3hub "Perciò ho fatto un backup del file!"
    m 1eua "Ora possiamo continuare la partita."
    return store.mas_chess.CHESS_GAME_BACKUP



label mas_chess_dlg_qf_edit:
    python:
        import store.mas_chess as mas_chess

    call mas_chess_dlg_qf_edit_start from _mas_chess_dlgqfeditstart

    m 2ekc "Hai modificato i file di salvataggio?{nw}"
    $ _history_list.pop()
    menu:
        m "Hai modificato i file di salvataggio?{fast}"
        "Yes.":
            call mas_chess_dlg_qf_edit_y_start from _mas_chess_dlgqfeditystart
        "No.":
            call mas_chess_dlg_qf_edit_n_start from _mas_chess_dlgqfeditnstart

    return _return


label mas_chess_dlg_qf_edit_start:
    m 2lksdlc "[player]..."
    return


label mas_chess_dlg_qf_edit_y_start:
    python:
        import store.mas_chess as mas_chess
        persistent._mas_chess_dlg_actions[mas_chess.QF_EDIT_YES] += 1
        qf_edit_count = persistent._mas_chess_dlg_actions[mas_chess.QF_EDIT_YES]

    if qf_edit_count == 1:
        call mas_chess_dlg_qf_edit_y_1 from _mas_chess_dlgqfedity1

    elif qf_edit_count == 2:
        call mas_chess_dlg_qf_edit_y_2 from _mas_chess_dlgqfedity2
    else:

        call mas_chess_dlg_qf_edit_y_3 from _mas_chess_dlgqfedity3

    return _return


label mas_chess_dlg_qf_edit_y_1:
    m 2dsc "Sono in disaccordo con te."
    m 1euc "Ma sono felice che tu abbia risposto sinceramente."


    show screen mas_background_timed_jump(5, "mas_chess_dlg_qf_edit_y_1n")
    menu:
        "Mi spiace.":
            hide screen mas_background_timed_jump

            $ mas_gainAffection(modifier=0.5)
            m 1hua "Scuse accettate!"
            m 1eua "Fortunatamente mi ricordo ancora un po' della partita quindi possiamo."
            return store.mas_chess.CHESS_GAME_BACKUP
        "...":
            label mas_chess_dlg_qf_edit_y_1n:
                hide screen mas_background_timed_jump
                m 1lfc "Dato che l'ultima partita è stata rovinata ne cominceremo una nuova."
            return
    return


label mas_chess_dlg_qf_edit_y_2:
    python:
        import datetime
        persistent._mas_chess_timed_disable = datetime.datetime.now()
        mas_loseAffection(modifier=0.5)

    m 2dfc "Sono davvero delusa."
    m 2rfc "Ora non voglio giocare a scacchi."
    return True


label mas_chess_dlg_qf_edit_y_3:
    $ mas_loseAffection()
    $ store.mas_chess.chess_strength = (True, persistent.chess_strength)
    $ persistent.chess_strength = 20
    $ persistent._mas_chess_skip_file_checks = True

    m 2dsc "Non sono sorpresa..."
    m 2esc "Ma mi sono preparata."
    m "Ho fatto un backup della partita nel caso lo avresti rifatto."
    m 1esa "Ora finiamola."
    return store.mas_chess.CHESS_GAME_BACKUP


label mas_chess_dlg_qf_edit_n_start:
    python:
        import store.mas_chess as mas_chess
        persistent._mas_chess_dlg_actions[mas_chess.QF_EDIT_NO] += 1
        qf_edit_count = persistent._mas_chess_dlg_actions[mas_chess.QF_EDIT_NO]

    if qf_edit_count == 1:
        call mas_chess_dlg_qf_edit_n_1 from _mas_chess_dlgqfeditn1

    elif qf_edit_count == 2:
        call mas_chess_dlg_qf_edit_n_2 from _mas_chess_dlgqfeditn2
    else:

        call mas_chess_dlg_qf_edit_n_3 from _mas_chess_dlgqfeditn3

    return _return


label mas_chess_dlg_qf_edit_n_1:
    $ mas_loseAffection()
    $ store.mas_chess.chess_strength = (True, persistent.chess_strength)
    $ persistent.chess_strength = 20

    m 1ekc "Capisco."
    m "Il file sembra diverso da come lo ricordavo, ma magari la memoria mi sta ingannando."
    m 1eua "Continuiamo questa partita."
    return store.mas_chess.CHESS_GAME_FILE


label mas_chess_dlg_qf_edit_n_2:
    $ mas_loseAffection(modifier=2)
    $ store.mas_chess.chess_strength = (True, persistent.chess_strength)
    $ persistent.chess_strength = 20

    m 1ekc "Capisco."
    m "..."
    m "Finiamo questa partita."
    return store.mas_chess.CHESS_GAME_FILE


label mas_chess_dlg_qf_edit_n_3:
    $ mas_loseAffection(modifier=3)
    m 2dfc "[player]..."
    m 2dftdc "Ho fatto un backup del file.{w} Sapevo che lo avresti modificato."
    m 2dftsc "io solo-"
    $ _history_list.pop()
    m 6ektsc "Io solo{fast} non riesco a credere che tu abbia imbrogliato e mi abbia {i}mentito{/i}."
    m 6rktsc "..."


    show screen mas_background_timed_jump(3, "mas_chess_dlg_qf_edit_n_3n")
    menu:
        "Scusa.":
            hide screen mas_background_timed_jump

            $ mas_gainAffection(modifier=0.5)
            call mas_chess_dlg_qf_edit_n_3_s from _mas_chess_dlgqfeditn3s
        "...":

            label mas_chess_dlg_qf_edit_n_3n:
                hide screen mas_background_timed_jump
                call mas_chess_dlg_qf_edit_n_3_n from _mas_chess_dlgqfeditn3n

    return _return


label mas_chess_dlg_qf_edit_n_3_s:
    $ store.mas_chess.chess_strength = (True, persistent.chess_strength)
    $ persistent.chess_strength = 20
    $ persistent._mas_chess_3_edit_sorry = True
    $ persistent._mas_chess_skip_file_checks = True
    $ store.mas_chess._initQuipLists(MASQuipList)

    show monika 6ektsc
    pause 1.0
    show monika 2ektsc
    pause 1.0
    m "Ti perdono, [player], Ma non farlo di nuovo."
    m 2lktsc "..."
    return store.mas_chess.CHESS_GAME_BACKUP


label mas_chess_dlg_qf_edit_n_3_n_qs:
    python:
        import datetime
        persistent._mas_chess_timed_disable = datetime.datetime.now()
        mas_loseAffection()

    m 2dfc "[player]..."
    m 2efc "Vedo che hai di nuovo modificato i file."
    m 2lfc "Se continui a fare così, allora giocheremo un'altra volta."
    return True


label mas_chess_dlg_qf_edit_n_3_n:
    python:

        persistent._mas_chess_mangle_all = True
        persistent.autoload = "mas_chess_go_ham_and_delete_everything"












    m 6ektsc "Non posso più fidarmi di te."
    m "Addio, [player].{nw}"


label mas_chess_go_ham_and_delete_everything:
    python:
        import store.mas_chess as mas_chess
        import store._mas_root as mas_root
        import os


        gamedir = os.path.normcase(config.basedir + "/game/")


        for filename in mas_chess.del_files:
            try:
                os.remove(gamedir + filename)
            except:
                pass


        for filename in mas_chess.gt_files:
            mas_root.mangleFile(gamedir + filename)


        try:
            os.remove(
                os.path.normcase(config.basedir + "/characters/monika.chr")
            )
        except:
            pass



        mas_root.resetPlayerData()

    jump _quit



label mas_chess_dlg_chess_locked:

    $ mas_loseAffection(modifier=0.1)
    m 1efc "..."
    m 2lfc "Non me la sento ora di giocare a scacchi."
    return






label mas_chess_dlg_game_in_progress:
    if persistent._mas_chess_3_edit_sorry:

        pass
    else:

        pass
    return


label mas_chess_dlg_game_drawed:
    if persistent._mas_chess_3_edit_sorry:
        m 1wuo "Scacco?"
        m 2lfc "Hmph."
        m 2tfu "Ti batterò la prossima volta."
    else:
        m 2tkc "Scacco? Che noia..."
    return



label mas_chess_dlg_game_monika_win_pre:
    m 1sub "Ho vinto!"
    return


label mas_chess_dlg_game_monika_win:
    python:
        import store.mas_chess as mas_chess


    call mas_chess_dlg_game_monika_win_pre from _mas_chess_dlggmwpre


    if persistent._mas_chess_3_edit_sorry:


        $ t_quip, v_quip = mas_chess.monika_wins_mean_quips.quip()


        if t_quip == MASQuipList.TYPE_LABEL:

            call expression v_quip from _mas_chess_dlggmw3esl
        else:


            m 1hub "[v_quip]"
    else:

        python:

            if persistent.chess_strength < 0:
                persistent.chess_strength = 0
            elif persistent.chess_strength > 20:
                persistent.chess_strength = 20

            chess_strength_label = mas_chess.DLG_MONIKA_WIN_BASE.format(
                persistent.chess_strength
            )

        call expression chess_strength_label from _mas_chess_dlggmwcsl

    return


label mas_chess_dlg_game_monika_win_rekt:
    m 1hub "Ahaha~"
    m 1tku "Magari dovresti provare con la dama."
    m 1tfu "Dubito che riuscirai a battermi."
    return


label mas_chess_dlg_game_monika_win_0:
    jump mas_chess_dlg_game_monika_win_2


label mas_chess_dlg_game_monika_win_1:
    jump mas_chess_dlg_game_monika_win_2


label mas_chess_dlg_game_monika_win_2:
    m 1hub "E' stato davvero divertente, [player]!"
    m 3eka "Non importa l'esito finale, mi piace sempre giocare a scacchi con te~"
    if renpy.random.randint(1,15) == 1:
        m 3hua "Meglio se continui a allenarti, un giorno riuscirai a battermi!"
        if renpy.random.randint(1,20) == 1:
            m 3rfu "{cps=*2}...O almeno vincere di tanto in tanto.{/cps}{nw}"
            $ _history_list.pop()
    return


label mas_chess_dlg_game_monika_win_3:
    jump mas_chess_dlg_game_monika_win_20


label mas_chess_dlg_game_monika_win_4:
    jump mas_chess_dlg_game_monika_win_20


label mas_chess_dlg_game_monika_win_5:
    jump mas_chess_dlg_game_monika_win_20


label mas_chess_dlg_game_monika_win_6:
    jump mas_chess_dlg_game_monika_win_20


label mas_chess_dlg_game_monika_win_7:
    jump mas_chess_dlg_game_monika_win_20


label mas_chess_dlg_game_monika_win_8:
    jump mas_chess_dlg_game_monika_win_20


label mas_chess_dlg_game_monika_win_9:
    jump mas_chess_dlg_game_monika_win_20


label mas_chess_dlg_game_monika_win_10:
    jump mas_chess_dlg_game_monika_win_20


label mas_chess_dlg_game_monika_win_11:
    jump mas_chess_dlg_game_monika_win_20


label mas_chess_dlg_game_monika_win_12:
    jump mas_chess_dlg_game_monika_win_20


label mas_chess_dlg_game_monika_win_13:
    jump mas_chess_dlg_game_monika_win_20


label mas_chess_dlg_game_monika_win_14:
    jump mas_chess_dlg_game_monika_win_20


label mas_chess_dlg_game_monika_win_15:
    jump mas_chess_dlg_game_monika_win_20


label mas_chess_dlg_game_monika_win_16:
    jump mas_chess_dlg_game_monika_win_20


label mas_chess_dlg_game_monika_win_17:
    jump mas_chess_dlg_game_monika_win_20


label mas_chess_dlg_game_monika_win_18:
    jump mas_chess_dlg_game_monika_win_20


label mas_chess_dlg_game_monika_win_19:
    jump mas_chess_dlg_game_monika_win_20


label mas_chess_dlg_game_monika_win_20:
    m 1tfu "Ci andro un po' più piano con te la prossima volta."
    return



label mas_chess_dlg_game_monika_win_surr_pre:
    m 1eka "Andiamo, non arrenderti così facilmente."
    return


label mas_chess_dlg_game_monika_win_surr:
    python:
        import store.mas_chess as mas_chess


    if persistent._mas_chess_3_edit_sorry:


        $ t_quip, v_quip = mas_chess.monika_wins_surr_mean_quips.quip()


        if t_quip == MASQuipList.TYPE_LABEL:

            call expression v_quip from _mas_chess_dlggmws3esl
        else:


            m 1hub "[v_quip]"
    else:


        call mas_chess_dlg_game_monika_win_surr_pre from _mas_chess_dlggmwspre

        python:

            if persistent.chess_strength < 0:
                persistent.chess_strength = 0
            elif persistent.chess_strength > 20:
                persistent.chess_strength = 20

            chess_strength_label = mas_chess.DLG_MONIKA_WIN_SURR_BASE.format(
                persistent.chess_strength
            )

        call expression chess_strength_label from _mas_chess_dlggmwscsl

    return



label mas_chess_dlg_game_monika_win_surr_resolve:
    m 1tfc "Rinunciare è un segno di scarsa determinazione..."
    m 1lfc "Non voglio un [bf] che ha così poca determinazione."
    return


label mas_chess_dlg_game_monika_win_surr_trying:
    m 1tku "Hai considerato {i}di provarci{/i}?"
    m 1tfu "Ho sentito dire che è benefico per la salute mentale."
    return


label mas_chess_dlg_game_monika_win_surr_0:
    jump mas_chess_dlg_game_monika_win_surr_20


label mas_chess_dlg_game_monika_win_surr_1:
    jump mas_chess_dlg_game_monika_win_surr_20


label mas_chess_dlg_game_monika_win_surr_2:
    jump mas_chess_dlg_game_monika_win_surr_20


label mas_chess_dlg_game_monika_win_surr_3:
    jump mas_chess_dlg_game_monika_win_surr_20


label mas_chess_dlg_game_monika_win_surr_4:
    jump mas_chess_dlg_game_monika_win_surr_20


label mas_chess_dlg_game_monika_win_surr_5:
    jump mas_chess_dlg_game_monika_win_surr_20


label mas_chess_dlg_game_monika_win_surr_6:
    jump mas_chess_dlg_game_monika_win_surr_20


label mas_chess_dlg_game_monika_win_surr_7:
    jump mas_chess_dlg_game_monika_win_surr_20


label mas_chess_dlg_game_monika_win_surr_8:
    jump mas_chess_dlg_game_monika_win_surr_20


label mas_chess_dlg_game_monika_win_surr_9:
    jump mas_chess_dlg_game_monika_win_surr_20


label mas_chess_dlg_game_monika_win_surr_10:
    jump mas_chess_dlg_game_monika_win_surr_20


label mas_chess_dlg_game_monika_win_surr_11:
    jump mas_chess_dlg_game_monika_win_surr_20


label mas_chess_dlg_game_monika_win_surr_12:
    jump mas_chess_dlg_game_monika_win_surr_20


label mas_chess_dlg_game_monika_win_surr_13:
    jump mas_chess_dlg_game_monika_win_surr_20


label mas_chess_dlg_game_monika_win_surr_14:
    jump mas_chess_dlg_game_monika_win_surr_20


label mas_chess_dlg_game_monika_win_surr_15:
    jump mas_chess_dlg_game_monika_win_surr_20


label mas_chess_dlg_game_monika_win_surr_16:
    jump mas_chess_dlg_game_monika_win_surr_20


label mas_chess_dlg_game_monika_win_surr_17:
    jump mas_chess_dlg_game_monika_win_surr_20


label mas_chess_dlg_game_monika_win_surr_18:
    jump mas_chess_dlg_game_monika_win_surr_20


label mas_chess_dlg_game_monika_win_surr_19:
    jump mas_chess_dlg_game_monika_win_surr_20


label mas_chess_dlg_game_monika_win_surr_20:

    return



label mas_chess_dlg_game_monika_lose_pre:
    m 2hua "Hai vinto! Congratulazioni."
    return


label mas_chess_dlg_game_monika_lose:
    python:
        import store.mas_chess as mas_chess


    if persistent._mas_chess_3_edit_sorry:


        $ t_quip, v_quip = mas_chess.monika_loses_mean_quips.quip()


        if t_quip == MASQuipList.TYPE_LABEL:

            call expression v_quip from _mas_chess_dlggml3esl
        else:


            m 1dsc "[v_quip]"
    else:


        call mas_chess_dlg_game_monika_lose_pre from _mas_chess_dlggmlp

        python:

            if persistent.chess_strength < 0:
                persistent.chess_strength = 0
            elif persistent.chess_strength > 20:
                persistent.chess_strength = 20

            chess_strength_label = mas_chess.DLG_MONIKA_LOSE_BASE.format(
                persistent.chess_strength
            )

        call expression chess_strength_label from _mas_chess_dlggmlcsl

    return




label mas_chess_dlg_game_monika_lose_silly:
    m 1tku "Sicuramente non ti aspetti che io creda che tu mi abbia battuto facilmente, specialmente per qualcuno al tuo livello di abilità.."
    m 1tfu "Non essere così idiota, [player]."
    return


label mas_chess_dlg_game_monika_lose_0:
    jump mas_chess_dlg_game_monika_lose_2


label mas_chess_dlg_game_monika_lose_1:
    jump mas_chess_dlg_game_monika_lose_2


label mas_chess_dlg_game_monika_lose_2:
    m 1tku "Devo ammettere che mi sono impegnata meno di quanto avrei dovuto..."
    m 1tsb "Spero non ti spiaccia! Mi impegnerò di più per farti migliorare ancora."
    return


label mas_chess_dlg_game_monika_lose_3:
    m 1eua "La prossima volta ti battero sicuramente!"
    return


label mas_chess_dlg_game_monika_lose_4:
    m 1hua "Hai giocato abbastanza bene in questa partita."
    return


label mas_chess_dlg_game_monika_lose_5:
    jump mas_chess_dlg_game_monika_lose_6


label mas_chess_dlg_game_monika_lose_6:
    m 1hua "Questa partita è stata piuttosto stimolante!"
    return


label mas_chess_dlg_game_monika_lose_7:
    m 3hua "Giocata eccellente, [player]!"
    return


label mas_chess_dlg_game_monika_lose_8:
    jump mas_chess_dlg_game_monika_lose_10


label mas_chess_dlg_game_monika_lose_9:
    jump mas_chess_dlg_game_monika_lose_10


label mas_chess_dlg_game_monika_lose_10:
    m 1wuo "Sei un giocatore di scacchi abbastanza capace!"
    return


label mas_chess_dlg_game_monika_lose_11:
    jump mas_chess_dlg_game_monika_lose_12


label mas_chess_dlg_game_monika_lose_12:
    m 1wuo "Sei davvero un forte avversario, [player]!"
    return


label mas_chess_dlg_game_monika_lose_13:
    jump mas_chess_dlg_game_monika_lose_19


label mas_chess_dlg_game_monika_lose_14:
    jump mas_chess_dlg_game_monika_lose_19


label mas_chess_dlg_game_monika_lose_15:
    jump mas_chess_dlg_game_monika_lose_19


label mas_chess_dlg_game_monika_lose_16:

    m 2lfx "N-{w=1}Non è che ti ho fatto vincere o altro, b-{w=1}baka!"
    return


label mas_chess_dlg_game_monika_lose_17:
    jump mas_chess_dlg_game_monika_lose_19


label mas_chess_dlg_game_monika_lose_18:
    jump mas_chess_dlg_game_monika_lose_19


label mas_chess_dlg_game_monika_lose_19:
    m 1wuo "Wow! Sei fenomenale a scacchi."
    m 1sub "Potresti essere un professionista!"
    return


label mas_chess_dlg_game_monika_lose_20:
    m 1wuo "Wow!"
    m 1tku "Sicuro di non star barando?"
    return



label mas_chess_dlg_game_monika_win_end:
    m 2eua "Nonostante le regole siano semplici,gli scacchi sono un gioco piuttosto complicato."
    m 1eua "Va bene ritrovarsi sensa saper come continuare."
    m 1hua "Ricorda, la cosa importante è imparare dai propri errori."
    return


label mas_chess_dlg_game_monika_win_end_quick:
    m 1eua "Okay, [player], rigiochiamo presto."
    return


label mas_chess_dlg_game_monika_lose_end:
    m 2eub "E' fantastico quanto, anche adesso, io abbia da imparare."
    m 2eua "Non mi importerò di perdere fino a quando non smetterò di imaprare."
    m 1hua "Dopotutto, la compagnia è ottima."
    return


label mas_chess_dlg_game_monika_lose_end_quick:
    jump mas_chess_dlg_game_monika_win_end_quick


label mas_chess_dlg_game_in_progress_end:


    jump mas_chess_dlg_game_in_progress_end_quick


label mas_chess_dlg_game_in_progress_end_quick:
    m 1eua "Okay, [player], riprendiamo questa partita presto."
    return




screen mas_chess_confirm():


    modal True

    zorder 200

    style_prefix "conferma"

    add "gui/overlay/confirm.png"

    frame:

        has vbox:
            xalign .5
            yalign .5
            spacing 30

        label _("Vuoi davvero arrenderti?"):
            style "confirm_prompt"
            xalign 0.5

        hbox:
            xalign 0.5
            spacing 100

            textbutton _("Si") action Return(True)
            textbutton _("No") action Return(False)

