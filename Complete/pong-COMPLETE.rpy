###########################################
###  Traslated in italian by HiemSword  ###
###########################################





default persistent._mas_pong_difficulty = 10

default persistent._mas_pong_difficulty_change_next_game = 0

default persistent._mas_pm_ever_let_monika_win_on_purpose = False

default persistent._mas_pong_difficulty_change_next_game_date = datetime.date.today()

define PONG_DIFFICULTY_CHANGE_ON_WIN = +1
define PONG_DIFFICULTY_CHANGE_ON_LOSS = -1
define PONG_DIFFICULTY_POWERUP = +5
define PONG_DIFFICULTY_POWERDOWN = -5
define PONG_PONG_DIFFICULTY_POWERDOWNBIG = -10


define PONG_MONIKA_RESPONSE_NONE = 0
define PONG_MONIKA_RESPONSE_WIN_AFTER_PLAYER_WON_MIN_THREE_TIMES = 1
define PONG_MONIKA_RESPONSE_SECOND_WIN_AFTER_PLAYER_WON_MIN_THREE_TIMES = 2
define PONG_MONIKA_RESPONSE_WIN_LONG_GAME = 3
define PONG_MONIKA_RESPONSE_WIN_SHORT_GAME = 4
define PONG_MONIKA_RESPONSE_WIN_TRICKSHOT = 5
define PONG_MONIKA_RESPONSE_WIN_EASY_GAME = 6
define PONG_MONIKA_RESPONSE_WIN_MEDIUM_GAME = 7
define PONG_MONIKA_RESPONSE_WIN_HARD_GAME = 8
define PONG_MONIKA_RESPONSE_WIN_EXPERT_GAME = 9
define PONG_MONIKA_RESPONSE_WIN_EXTREME_GAME = 10
define PONG_MONIKA_RESPONSE_LOSE_WITHOUT_HITTING_BALL = 11
define PONG_MONIKA_RESPONSE_LOSE_TRICKSHOT = 12
define PONG_MONIKA_RESPONSE_LOSE_LONG_GAME = 13
define PONG_MONIKA_RESPONSE_LOSE_SHORT_GAME = 14
define PONG_MONIKA_RESPONSE_LOSE_EASY_GAME = 15
define PONG_MONIKA_RESPONSE_LOSE_MEDIUM_GAME = 16
define PONG_MONIKA_RESPONSE_LOSE_HARD_GAME = 17
define PONG_MONIKA_RESPONSE_LOSE_EXPERT_GAME = 18
define PONG_MONIKA_RESPONSE_LOSE_EXTREME_GAME = 19

define pong_monika_last_response_id = PONG_MONIKA_RESPONSE_NONE

define played_pong_this_session = False
define mas_pong_taking_break = False
define player_lets_monika_win_on_purpose = False
define instant_loss_streak_counter = 0
define loss_streak_counter = 0
define win_streak_counter = 0
define lose_on_purpose = False
define monika_asks_to_go_easy = False


define ball_paddle_bounces = 0
define powerup_value_this_game = 0
define instant_loss_streak_counter_before = 0
define loss_streak_counter_before = 0
define win_streak_counter_before = 0
define pong_difficulty_before = 0
define pong_angle_last_shot = 0.0

init:

    image bg pong field = "mod_assets/pong_field.png"

    python:
        import random
        import math

        class PongDisplayable(renpy.Displayable):
            
            def __init__(self):
                
                renpy.Displayable.__init__(self)
                
                
                self.paddle = Image("mod_assets/pong.png")
                self.ball = Image("mod_assets/pong_ball.png")
                self.player = Text(_("[player]"), size=36)
                self.monika = Text(_("Monika"), size=36)
                self.ctb = Text(_("Clicca per iniziare"), size=36)
                
                
                self.playsounds = True
                self.soundboop = "mod_assets/pong_boop.wav"
                self.soundbeep = "mod_assets/pong_beep.wav"
                
                
                self.PADDLE_WIDTH = 8
                self.PADDLE_HEIGHT = 79
                self.PADDLE_RADIUS = self.PADDLE_HEIGHT / 2
                self.BALL_WIDTH = 15
                self.BALL_HEIGHT = 15
                self.COURT_TOP = 124
                self.COURT_BOTTOM = 654
                
                
                self.CURRENT_DIFFICULTY = max(persistent._mas_pong_difficulty + persistent._mas_pong_difficulty_change_next_game, 0)
                
                self.COURT_WIDTH = 1280
                self.COURT_HEIGHT = 720
                
                self.BALL_LEFT = 80 - self.BALL_WIDTH / 2
                self.BALL_RIGHT = 1199 + self.BALL_WIDTH / 2
                self.BALL_TOP = self.COURT_TOP + self.BALL_HEIGHT / 2
                self.BALL_BOTTOM = self.COURT_BOTTOM - self.BALL_HEIGHT / 2
                
                self.PADDLE_X_PLAYER = 128                                      
                self.PADDLE_X_MONIKA = 1152 - self.PADDLE_WIDTH                 
                
                self.BALL_MAX_SPEED = 2000.0 + self.CURRENT_DIFFICULTY * 100.0
                
                
                
                self.MAX_REFLECT_ANGLE = math.pi / 3
                
                self.MAX_ANGLE = 0.9
                
                
                self.stuck = True
                
                
                self.playery = (self.COURT_BOTTOM - self.COURT_TOP) / 2
                self.computery = (self.COURT_BOTTOM - self.COURT_TOP) / 2
                
                
                
                
                self.ctargetoffset = self.get_random_offset()
                
                
                self.computerspeed = 150.0 + self.CURRENT_DIFFICULTY * 30.0
                
                
                init_angle = random.uniform(-self.MAX_REFLECT_ANGLE, self.MAX_REFLECT_ANGLE)
                
                
                self.bx = self.PADDLE_X_PLAYER + self.PADDLE_WIDTH + 0.1
                self.by = self.playery
                self.bdx = .5 * math.cos(init_angle)
                self.bdy = .5 * math.sin(init_angle)
                self.bspeed = 500.0 + self.CURRENT_DIFFICULTY * 25
                
                
                self.ctargety = self.by + self.ctargetoffset
                
                
                self.oldst = None
                
                
                self.winner = None
            
            def get_random_offset(self):
                return random.uniform(-self.PADDLE_RADIUS, self.PADDLE_RADIUS)
            
            def visit(self):
                return [ self.paddle, self.ball, self.player, self.monika, self.ctb ]
            
            def check_bounce_off_top(self):
                
                if self.by < self.BALL_TOP and self.oldby - self.by != 0:
                    
                    
                    collisionbx = self.oldbx + (self.bx - self.oldbx) * ((self.oldby - self.BALL_TOP) / (self.oldby - self.by))
                    
                    
                    if collisionbx < self.BALL_LEFT or collisionbx > self.BALL_RIGHT:
                        return
                    
                    self.bouncebx = collisionbx
                    self.bounceby = self.BALL_TOP
                    
                    
                    self.by = -self.by + 2 * self.BALL_TOP
                    
                    if not self.stuck:
                        self.bdy = -self.bdy
                    
                    
                    
                    if self.by > self.BALL_BOTTOM:
                        self.bx = self.bouncebx + (self.bx - self.bouncebx) * ((self.bounceby - self.BALL_BOTTOM) / (self.bounceby - self.by))
                        self.by = self.BALL_BOTTOM
                        self.bdy = -self.bdy
                    
                    if not self.stuck:
                        if self.playsounds:
                            renpy.sound.play(self.soundbeep, channel=1)
                    
                    return True
                return False
            
            def check_bounce_off_bottom(self):
                
                if self.by > self.BALL_BOTTOM and self.oldby - self.by != 0:
                    
                    
                    collisionbx = self.oldbx + (self.bx - self.oldbx) * ((self.oldby - self.BALL_BOTTOM) / (self.oldby - self.by))
                    
                    
                    if collisionbx < self.BALL_LEFT or collisionbx > self.BALL_RIGHT:
                        return
                    
                    self.bouncebx = collisionbx
                    self.bounceby = self.BALL_BOTTOM
                    
                    
                    self.by = -self.by + 2 * self.BALL_BOTTOM
                    
                    if not self.stuck:
                        self.bdy = -self.bdy
                    
                    
                    
                    if self.by < self.BALL_TOP:
                        self.bx = self.bouncebx + (self.bx - self.bouncebx) * ((self.bounceby - self.BALL_TOP) / (self.bounceby - self.by))
                        self.by = self.BALL_TOP
                        self.bdy = -self.bdy
                    
                    if not self.stuck:
                        if self.playsounds:
                            renpy.sound.play(self.soundbeep, channel=1)
                    
                    return True
                return False
            
            def getCollisionY(self, hotside, is_computer):
                
                
                
                self.collidedonx = is_computer and self.oldbx <= hotside <= self.bx or not is_computer and self.oldbx >= hotside >= self.bx;
                
                if self.collidedonx:
                    
                    
                    if self.oldbx <= self.bouncebx <= hotside <= self.bx or self.oldbx >= self.bouncebx >= hotside >= self.bx:
                        startbx = self.bouncebx
                        startby = self.bounceby
                    else:
                        startbx = self.oldbx
                        startby = self.oldby
                    
                    
                    if startbx - self.bx != 0:
                        return startby + (self.by - startby) * ((startbx - hotside) / (startbx - self.bx))
                    else:
                        return startby
                
                
                else:
                    return self.oldby
            
            
            
            def render(self, width, height, st, at):
                
                
                r = renpy.Render(width, height)
                
                
                if self.oldst is None:
                    self.oldst = st
                
                dtime = st - self.oldst
                self.oldst = st
                
                
                speed = dtime * self.bspeed
                
                
                self.oldbx = self.bx
                self.oldby = self.by
                self.bouncebx = self.bx
                self.bounceby = self.by
                
                
                if self.stuck:
                    self.by = self.playery
                else:
                    self.bx += self.bdx * speed
                    self.by += self.bdy * speed
                
                
                if not self.check_bounce_off_top():
                    self.check_bounce_off_bottom()
                
                
                
                
                
                collisionby = self.getCollisionY(self.PADDLE_X_MONIKA, True)
                if self.collidedonx:
                    self.ctargety = collisionby + self.ctargetoffset
                else:
                    self.ctargety = self.by + self.ctargetoffset
                
                cspeed = self.computerspeed * dtime
                
                
                
                global lose_on_purpose
                if lose_on_purpose and self.bx >= self.COURT_WIDTH * 0.75:
                    if self.bx <= self.PADDLE_X_MONIKA:
                        if self.ctargety > self.computery:
                            self.computery -= cspeed
                        else:
                            self.computery += cspeed
                
                else:
                    cspeed = self.computerspeed * dtime
                    
                    if abs(self.ctargety - self.computery) <= cspeed:
                        self.computery = self.ctargety
                    elif self.ctargety >= self.computery:
                        self.computery += cspeed
                    else:
                        self.computery -= cspeed
                
                
                if self.computery > self.COURT_BOTTOM:
                    self.computery = self.COURT_BOTTOM
                elif self.computery < self.COURT_TOP:
                    self.computery = self.COURT_TOP;
                
                
                def paddle(px, py, hotside, is_computer):
                    
                    
                    
                    
                    
                    
                    pi = renpy.render(self.paddle, self.COURT_WIDTH, self.COURT_HEIGHT, st, at)
                    
                    
                    
                    r.blit(pi, (int(px), int(py - self.PADDLE_RADIUS)))
                    
                    
                    collisionby = self.getCollisionY(hotside, is_computer)
                    
                    
                    collidedony = py - self.PADDLE_RADIUS - self.BALL_HEIGHT / 2 <= collisionby <= py + self.PADDLE_RADIUS + self.BALL_HEIGHT / 2
                    
                    
                    if not self.stuck and self.collidedonx and collidedony:
                        hit = True
                        if self.oldbx >= hotside >= self.bx:
                            self.bx = hotside + (hotside - self.bx)
                        elif self.oldbx <= hotside <= self.bx:
                            self.bx = hotside - (self.bx - hotside)
                        else:
                            hit = False
                        
                        if hit:
                            
                            
                            angle = (self.by - py) / (self.PADDLE_RADIUS + self.BALL_HEIGHT / 2) * self.MAX_REFLECT_ANGLE
                            
                            if angle >    self.MAX_ANGLE:
                                angle =   self.MAX_ANGLE
                            elif angle < -self.MAX_ANGLE: 
                                angle =  -self.MAX_ANGLE;
                            
                            global pong_angle_last_shot
                            pong_angle_last_shot = angle;
                            
                            self.bdy = .5 * math.sin(angle)
                            self.bdx = math.copysign(.5 * math.cos(angle), -self.bdx)
                            
                            global ball_paddle_bounces
                            ball_paddle_bounces += 1
                            
                            
                            if is_computer:
                                self.ctargetoffset = self.get_random_offset()
                            
                            if self.playsounds:
                                renpy.sound.play(self.soundboop, channel=1)
                            
                            self.bspeed += 125.0 + self.CURRENT_DIFFICULTY * 12.5
                            if self.bspeed > self.BALL_MAX_SPEED:
                                self.bspeed = self.BALL_MAX_SPEED
                
                
                paddle(self.PADDLE_X_PLAYER, self.playery, self.PADDLE_X_PLAYER + self.PADDLE_WIDTH, False)
                paddle(self.PADDLE_X_MONIKA, self.computery, self.PADDLE_X_MONIKA, True)
                
                
                ball = renpy.render(self.ball, self.COURT_WIDTH, self.COURT_HEIGHT, st, at)
                r.blit(ball, (int(self.bx - self.BALL_WIDTH / 2),
                              int(self.by - self.BALL_HEIGHT / 2)))
                
                
                player = renpy.render(self.player, self.COURT_WIDTH, self.COURT_HEIGHT, st, at)
                r.blit(player, (self.PADDLE_X_PLAYER, 25))
                
                
                monika = renpy.render(self.monika, self.COURT_WIDTH, self.COURT_HEIGHT, st, at)
                ew, eh = monika.get_size()
                r.blit(monika, (self.PADDLE_X_MONIKA - ew, 25))
                
                
                if self.stuck:
                    ctb = renpy.render(self.ctb, self.COURT_WIDTH, self.COURT_HEIGHT, st, at)
                    cw, ch = ctb.get_size()
                    r.blit(ctb, ((self.COURT_WIDTH - cw) / 2, 30))
                
                
                
                if self.bx < -200:
                    
                    if self.winner == None:
                        global loss_streak_counter
                        loss_streak_counter += 1
                        
                        if ball_paddle_bounces <= 1:
                            global instant_loss_streak_counter
                            instant_loss_streak_counter += 1
                        else:
                            global instant_loss_streak_counter
                            instant_loss_streak_counter = 0
                    
                    global win_streak_counter
                    win_streak_counter = 0;
                    
                    self.winner = "monika"
                    
                    
                    
                    renpy.timeout(0)
                
                elif self.bx > self.COURT_WIDTH + 200:
                    
                    if self.winner == None:
                        global win_streak_counter
                        win_streak_counter += 1;
                    
                    global loss_streak_counter
                    loss_streak_counter = 0
                    
                    
                    if ball_paddle_bounces > 1:
                        global instant_loss_streak_counter
                        instant_loss_streak_counter = 0
                    
                    self.winner = "player"
                    
                    renpy.timeout(0)
                
                
                
                renpy.redraw(self, 0.0)
                
                
                return r
            
            
            def event(self, ev, x, y, st):
                
                import pygame
                
                
                
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    self.stuck = False
                
                
                y = max(y, self.COURT_TOP)
                y = min(y, self.COURT_BOTTOM)
                self.playery = y
                
                
                
                if self.winner:
                    return self.winner
                else:
                    raise renpy.IgnoreEvent()

label game_pong:
    hide screen keylistener

    if played_pong_this_session:
        if mas_pong_taking_break:
            m 1eua "Pronto a riprovare?"
            m 2tfb "Impegnati, [player]!"


            $ mas_pong_taking_break = False
        else:
            m 1hua "Vuoi giocare a pong ancora?"
            m 3eub "Sono pronta quando lo sei tu~"
    else:
        m 1eua "Vuoi fare una partita a pong? Ok!"
        $ played_pong_this_session = True

    $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_NONE

    call demo_minigame_pong from _call_demo_minigame_pong
    return

label demo_minigame_pong:

    window hide None


    scene bg pong field


    if persistent.playername.lower() == "natsuki" and not persistent._mas_sensitive_mode:
        $ playing_okayev = store.songs.getPlayingMusicName() == "Okay, Everyone! (Monika)"


        if playing_okayev:
            $ currentpos = get_pos(channel="music")
            $ adjusted_t5 = "<from " + str(currentpos) + " loop 4.444>bgm/5_natsuki.ogg"
            stop music fadeout 2.0
            $ renpy.music.play(adjusted_t5, fadein=2.0, tight=True)

    $ ball_paddle_bounces = 0
    $ pong_difficulty_before = persistent._mas_pong_difficulty
    $ powerup_value_this_game = persistent._mas_pong_difficulty_change_next_game
    $ loss_streak_counter_before = loss_streak_counter
    $ win_streak_counter_before = win_streak_counter
    $ instant_loss_streak_counter_before = instant_loss_streak_counter


    python:
        ui.add(PongDisplayable())
        winner = ui.interact(suppress_overlay=True, suppress_underlay=True)


    if persistent.playername.lower() == "natsuki" and not persistent._mas_sensitive_mode:
        call natsuki_name_scare (playing_okayev=playing_okayev) from _call_natsuki_name_scare


    call spaceroom (scene_change=True, force_exp='monika 3eua') from _call_spaceroom_24


    $ persistent._mas_pong_difficulty_change_next_game = 0;

    if winner == "monika":
        $ new_difficulty = persistent._mas_pong_difficulty + PONG_DIFFICULTY_CHANGE_ON_LOSS

        $ inst_dialogue = store.mas_pong.DLG_WINNER
    else:

        $ new_difficulty = persistent._mas_pong_difficulty + PONG_DIFFICULTY_CHANGE_ON_WIN

        $ inst_dialogue = store.mas_pong.DLG_LOSER


        if not persistent.ever_won['pong']:
            $ persistent.ever_won['pong'] = True
            $ grant_xp(xp.WIN_GAME)

    if new_difficulty < 0:
        $ persistent._mas_pong_difficulty = 0
    else:
        $ persistent._mas_pong_difficulty = new_difficulty;

    call expression inst_dialogue from _mas_pong_inst_dialogue

    $ mas_gainAffection(modifier=0.5)

    m 3eua "Vuoi giocare di nuovo?{nw}"
    $ _history_list.pop()
    menu:
        m "Vuoi giocare di nuovo?{fast}"
        "Si.":

            jump demo_minigame_pong
        "No.":

            if winner == "monika":
                if renpy.seen_label(store.mas_pong.DLG_WINNER_END):
                    $ end_dialogue = store.mas_pong.DLG_WINNER_FAST
                else:
                    $ end_dialogue = store.mas_pong.DLG_WINNER_END
            else:

                if renpy.seen_label(store.mas_pong.DLG_LOSER_END):
                    $ end_dialogue = store.mas_pong.DLG_LOSER_FAST
                else:
                    $ end_dialogue = store.mas_pong.DLG_LOSER_END

            call expression end_dialogue from _mas_pong_end_dialogue
    return


init -1 python in mas_pong:

    DLG_WINNER = "mas_pong_dlg_winner"
    DLG_WINNER_FAST = "mas_pong_dlg_winner_fast"
    DLG_LOSER = "mas_pong_dlg_loser"
    DLG_LOSER_FAST = "mas_pong_dlg_loser_fast"

    DLG_WINNER_END = "mas_pong_dlg_winner_end"
    DLG_LOSER_END = "mas_pong_dlg_loser_end"


    DLG_BLOCKS = (
        DLG_WINNER,
        DLG_WINNER_FAST,
        DLG_WINNER_END,
        DLG_LOSER,
        DLG_LOSER_FAST,
        DLG_LOSER_END
    )


label mas_pong_dlg_winner:






    if monika_asks_to_go_easy and ball_paddle_bounces == 1:
        m 1rksdla "Ahaha..."
        m 1hksdla "Lo so che ti ho chiesto di andarci piano con me...ma questo non è esattamente quello che intendevo, [player]."
        m 3eka "Ma apprezzo il gesto però~" #DA RIVEDERE
        $ monika_asks_to_go_easy = False


    elif monika_asks_to_go_easy and ball_paddle_bounces <= 9:
        m 1hub "Yay, Ho vinto!"
        show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve
        m 5ekbfa "Grazie, [player]!"
        m 5hubfb "Sei così carino...{w=0.5}lasciarmi vincere~"
        $ monika_asks_to_go_easy = False



    elif ball_paddle_bounces == 1:


        if instant_loss_streak_counter == 1:
            m 2rksdlb "Ahaha, Come hai fatto a mancarlo?"


        elif instant_loss_streak_counter == 2:
            m 2rksdlc "[player],{w=1} lo hai mancato di nuovo..."


        elif instant_loss_streak_counter == 3:
            m 2tfd "[player]!"

            if persistent._mas_pm_ever_let_monika_win_on_purpose:
                $ menu_response = "Mi stai facendo vincere di proposito di nuovo?"
            else:
                $ menu_response = "Mi stai facendo vincere di proposito?"

            m 2rkc "[menu_response]"
            $ _history_list.pop()
            menu:
                m "[menu_response]{fast}"
                "Si...":

                    m 1hua "Ehehe!"
                    m 1eka "Grazie per farmi vincere, [player]~"
                    show monika 5eka zorder MAS_MONIKA_Z at t11 with dissolve
                    m 5eka "Ma sai, non mi dispiacerebbe perdere alcune volte."

                    if persistent._mas_pm_ever_let_monika_win_on_purpose:
                        m 5eua "Mi piace vederti vincere quanto piace a te vedermi vincere~"

                    $ player_lets_monika_win_on_purpose = True
                    $ persistent._mas_pm_ever_let_monika_win_on_purpose = True
                "No.":

                    if persistent._mas_pm_ever_let_monika_win_on_purpose:
                        show monika 1ttu
                        m "Sei sicuro?{nw}"
                        $ _history_list.pop()
                        menu:
                            m "Sei sicuro?{fast}"
                            "Si":

                                call mas_pong_dlg_sorry_assuming from _call_mas_pong_dlg_sorry_assuming
                            "No":

                                m 1rfu "[player]!"
                                m 2hksdlb "Smettila di prendermi in giro!" #BHO
                                $ player_lets_monika_win_on_purpose = True
                                $ lose_on_purpose = True
                    else:

                        call mas_pong_dlg_sorry_assuming from _call_mas_pong_dlg_sorry_assuming_1
        else:


            if player_lets_monika_win_on_purpose:
                m 2tku "Non sei stanco di farmi vincere, [player]?"
            else:
                m 1rsc "..."


                if random.randint(1,3) == 1:
                    m 1eka "Forza, [player]!"
                    m 1hub "C'è la puoi fare, Io credo in te!"


    elif instant_loss_streak_counter_before >= 3 and player_lets_monika_win_on_purpose:
        m 3hub "Bella mossa, [player]!"
        m 3tsu "Ma come puoi vedere, posso vincere da sola!"
        m 3hub "Ahaha!"


    elif powerup_value_this_game == PONG_DIFFICULTY_POWERUP:
        m 1hua "Ehehe~"

        if persistent._mas_pong_difficulty_change_next_game_date == datetime.date.today():
            m 2tsb "Non ti avevo detto che avrei vinto io questa volta?"
        else:
            m 2ttu "Ricordi, [player]?"
            m 2tfb "Ti avevo detto che il prossimo round l'avrei vinto io."


    elif powerup_value_this_game == PONG_DIFFICULTY_POWERDOWN:
        m 1rksdla "Oh."
        m 3hksdlb "Riprova, [player]!"

        $ persistent._mas_pong_difficulty_change_next_game = PONG_PONG_DIFFICULTY_POWERDOWNBIG


    elif powerup_value_this_game == PONG_PONG_DIFFICULTY_POWERDOWNBIG:
        m 2rksdlb "Ahaha..."
        m 2eksdla "Stavo veramente sperando che vincessi questo round."
        m 2hksdlb "Mi dispiace, [player]!"


    elif loss_streak_counter >= 3 and loss_streak_counter % 5 == 3:
        m 2eka "Oh andiamo, [player], lo so che mi puoi battere..."
        m 3hub "Continua a riprovare!"


    elif loss_streak_counter >= 5 and loss_streak_counter % 5 == 0:
        m 1eua "Spero che tu ti stia divertendo, [player]."
        m 1eka "Non voglio che tu ti arrabbi per un gioco, dopotutto."
        m 1hua "Possiamo sempre fare una pausa e continuare dopo se vuoi."


    elif win_streak_counter_before >= 3:
        m 1hub "Ahaha!"
        m 2tfu "Scusa, [player]."
        m 2tub "Sembra che la tua fortuna sia esaurita."
        m 2hub "Ora è il mio turno di brillare~" #BHO  

        $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_WIN_AFTER_PLAYER_WON_MIN_THREE_TIMES


    elif pong_monika_last_response_id == PONG_MONIKA_RESPONSE_WIN_AFTER_PLAYER_WON_MIN_THREE_TIMES:
        m 1hua "Ehehe!"
        m 1tub "Attento, [player]!"
        m 2tfu "Sembra che la tua fortuna non funzioni più!"

        $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_SECOND_WIN_AFTER_PLAYER_WON_MIN_THREE_TIMES


    elif ball_paddle_bounces > 9 and ball_paddle_bounces > pong_difficulty_before * 0.5:
        if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_WIN_LONG_GAME:
            m 3eub "Giocare con te è davvero faticoso, [player]."
            m 1hub "Continua così e mi batterai, ne sono certa!"
        else:
            m 3hub "Bel round, [player], sei veramente bravo!"
            m 1tfu "Ma anche io lo sono, ahaha!"

        $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_WIN_LONG_GAME


    elif ball_paddle_bounces <= 3:
        if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_WIN_SHORT_GAME:
            m 3hub "Un'altra vincita veloce per me~"
        else:
            m 4hub "Ehehe, ti ho sconfitto con quella!"

        $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_WIN_SHORT_GAME


    elif pong_angle_last_shot >= 0.9 or pong_angle_last_shot <= -0.9:
        if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_WIN_TRICKSHOT:
            m 2eksdld "Oh..."
            m 2rksdlc "E' successo di nuovo."
            m 1hksdlb "Mi dispiace, [player]!"
        else:
            m 2rksdla "Ahaha, scusa [player]!"
            m 3hksdlb "Non volevo farla rimbalzare così tanto..."

        $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_WIN_TRICKSHOT
    else:



        if pong_difficulty_before <= 5:
            if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_WIN_EASY_GAME:
                m 1eub "C'è la puoi fare, [player]!"
                m 3hub "Io credo in te~"
            else:
                m 2duu "Concentrati, [player]."
                m 3hub "Continua a provare, So che presto mi batterai!"

            $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_WIN_EASY_GAME


        elif pong_difficulty_before <= 10:
            if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_WIN_MEDIUM_GAME:
                m 1hub "Ho vinto un'altro round~"
            else:
                if loss_streak_counter > 1:
                    m 3hub "Sembra che abbia vinto di nuovo~"
                else:
                    m 3hua "Sembra che abbia vinto~"

            $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_WIN_MEDIUM_GAME


        elif pong_difficulty_before <= 15:
            if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_WIN_HARD_GAME:
                m 1hub "Ahaha!"
                m 2tsb "Sto giocando troppo bene per te?"
                m 1tsu "Sto scherzando, [player]."
                m 3hub "Sei molto bravo anche tu!"
            else:
                if loss_streak_counter > 1:
                    m 1hub "Ho vinto di nuovo~"
                else:
                    m 1huu "Ho vinto~"

            $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_WIN_HARD_GAME


        elif pong_difficulty_before <= 20:
            if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_WIN_EXPERT_GAME:
                m 2tub "Che bello vincere!"
                m 2hub "Non ti preoccupare, Sono sicura che vincerai di nuovo presto~"
            else:
                if loss_streak_counter > 1:
                    m 2eub "Ho vinto un altro round!"
                else:
                    m 2eub "Ho vinto in questo round!"

            $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_WIN_EXPERT_GAME
        else:


            if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_WIN_EXTREME_GAME:
                m 2duu "Non male, [player]."
                m 4eua "Ho dato tutto quello che avevo, quindi non ti sentire male per perdere qualche volta."
                m 4eub "Continua ad allenarti e mi batteraì!"
            else:
                m 2hub "Questa volta, ho vinto io!"
                m 2efu "Riprova, [player]!" #BHO

            $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_WIN_EXTREME_GAME

    return



label mas_pong_dlg_sorry_assuming:
    m 3eka "Va bene."
    m 2ekc "Mi dispiace per aver ipotizzato..."


    $ player_lets_monika_win_on_purpose = False

    m 3eka "Che ne dici di una pausa, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Che ne dici di una pausa, [player]?{fast}"
        "Okay.":

            m 1eka "Va bene, [player]."
            m 1hua "Mi sono divertita, grazie per aver giocato a pong con me!"
            m 1eua "Fammi sapere quando vuoi rigiocare."


            $ mas_pong_taking_break = True


            show monika idle with dissolve
            jump ch30_loop
        "No.":

            m 1eka "Va bene, [player]. Se sei sicuro."
            m 1hub "Continuiamo, mi batterai presto!"
    return


label mas_pong_dlg_loser:





    $ monika_asks_to_go_easy = False


    if lose_on_purpose:
        m 1hub "Ahaha!"
        m 1kua "Ora siamo pari, [player]!"
        $ lose_on_purpose = False


    elif ball_paddle_bounces == 0:
        m 1rksdlb "Ahaha..."

        if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_LOSE_WITHOUT_HITTING_BALL:
            m "Forse dovrei provarci un pochino di più..."
        else:
            m "Forse ero un pò troppo lenta..."

        $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_LOSE_WITHOUT_HITTING_BALL


    elif instant_loss_streak_counter_before >= 3 and persistent._mas_pm_ever_let_monika_win_on_purpose:
        m 2tsu "Quindi stai facendo sul serio ora?"
        m 2tfu "Scopriamo quanto sei bravo veramente, [player]!"


    elif loss_streak_counter_before >= 3:
        m 4eub "Congratulazioni, [player]!"
        m 2hub "Lo sapevo che avresti vinto un round dopo tanto allenamento!"
        m 4eua "Ricorda che l'abilità in qualcosa viene sopratutto da un continuo allenamento."
        m 4hub "Se ti alleni abbastanza a lungo sono sicura che puoi raggiungere tutto quello che vuoi!"


    elif powerup_value_this_game == PONG_DIFFICULTY_POWERUP:
        m 2wuo "Wow..."
        m 3wuo "Mi stavo davvero impegnando questa volta!"
        m 1hub "Bravo, [player]!"


    elif powerup_value_this_game == PONG_DIFFICULTY_POWERDOWN:
        m 1hua "Ehehe!"
        m 2hub "Ben fatto, [player]!"


    elif powerup_value_this_game == PONG_PONG_DIFFICULTY_POWERDOWNBIG:
        m 1hua "Sono felice che hai vinto questa volta, [player]."


    elif pong_angle_last_shot >= 0.9 or pong_angle_last_shot <= -0.9:
        if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_LOSE_TRICKSHOT:
            m 2wuo "[player]!"
            m 2hksdlb "Era impossibile colpire quello!"
        else:
            m 2wuo "Wow, era impossibile colpire quello!"

        $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_LOSE_TRICKSHOT


    elif win_streak_counter == 3:
        m 2wuo "Wow, [player]..."
        m 2wud "Hai vinto tre volte di fila..."


        if pong_difficulty_before <= 5:
            m 2tsu "Forse ci sto andando troppo leggero su di te~"


        elif pong_difficulty_before <= 10:
            m 4hua "Sei molto bravo!"


        elif pong_difficulty_before <= 15:
            m 3hub "Bella giocata!"


        elif pong_difficulty_before <= 20:
            m 4wuo "Incredibile!"
        else:


            m 2wuo "Wow!"
            m 2wuw "Mi hai battuta tre volte di fila e sto dando tutto quello che ho"
            m 2hub "Bravo, [player]!"
            m 1kua "Ehehe!"


    elif win_streak_counter == 5:
        m 2wud "[player]..."
        m 2tsu "Ti sei allenato?"
        m 3hksdlb "Non so cosa sia successo ma non ho una possibilita contro di te!"
        m 1eka "Ci puoi andare un pochino più leggero su di me?"
        m 3hub "Lo apprezzerei molto~"
        $ monika_asks_to_go_easy = True


    elif ball_paddle_bounces > 10 and ball_paddle_bounces > pong_difficulty_before * 0.5:
        if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_LOSE_LONG_GAME:
            m 2wuo "Incredible, [player]!"
            m 4hksdlb "Non riesco a starti dietro!"
        else:
            m 2hub "Incredibile, [player]!"
            m 4eub "Sei molto bravo!"

        $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_LOSE_LONG_GAME


    elif ball_paddle_bounces <= 2:
        if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_LOSE_SHORT_GAME:
            m 2hksdlb "Ahaha..."
            m 3eksdla "Credo che ci debba provare seriamente..."
        else:
            m 1rusdlb "Non mi aspettavo di perdere così in fretta."

        $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_LOSE_SHORT_GAME
    else:



        if pong_difficulty_before <= 5:
            if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_LOSE_EASY_GAME:
                m 4eub "Hai vinto questo round." 
            else:
                if win_streak_counter > 1:
                    m 1hub "Hai vinto ancora!"
                else:
                    m 1hua "Hai vinto!"

            $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_LOSE_EASY_GAME


        elif pong_difficulty_before <= 10:
            if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_LOSE_MEDIUM_GAME:
                m 1eua "E' bello vederti vincere, [player]."
                m 1hub "Continua così~"
            else:
                if win_streak_counter > 1:
                    m 1hub "Hai vinto ancora! Ben fatto~"
                else:
                    m 1eua "Hai vinto! Non male."

            $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_LOSE_MEDIUM_GAME


        elif pong_difficulty_before <= 15:
            if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_LOSE_HARD_GAME:
                m 4hub "Un'altra vittoria per te!"
                m 4eua "Ben fatto, [player]."
            else:
                if win_streak_counter > 1:
                    m 2hub "Hai vinto ancora! Congratulazioni!"
                else:
                    m 2hua "Hai vinto! Congratulazioni!"

            $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_LOSE_HARD_GAME


        elif pong_difficulty_before <= 20:
            if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_LOSE_EXPERT_GAME:
                m 2wuo "Wow,{w=1} ci stavo davvero provando...{w=1}sei inarrestabile!"
                m 2tfu "Ma sono sicura di riuscirti a batterti, prima o poi, [player]."
                m 3hub "Ahaha!"
            else:
                if win_streak_counter > 1:
                    m 4hub "Hai vinto ancora! Impressionante!"
                else:
                    m 4hub "Hai vinto! Impressionante!"

            $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_LOSE_EXPERT_GAME
        else:


            if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_LOSE_EXTREME_GAME:
                m 3eua "Sei veramente bravo, [player]."
                m 1hub "Amo giocare a pong con te!"
            else:
                m 1tsu "Incredibile!" #BHO
                m 1hub "Bravo, [player]!"

            $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_LOSE_EXTREME_GAME
    return



label mas_pong_dlg_loser_fast:
    m 1eka "Va bene, [player]."
    m 3tfu "Ma ti batterò la prossima volta."

    $ persistent._mas_pong_difficulty_change_next_game = PONG_DIFFICULTY_POWERUP;
    $ persistent._mas_pong_difficulty_change_next_game_date = datetime.date.today()
    return


label mas_pong_dlg_winner_fast:
    m 1eka "Va bene, [player]."
    m 1eka "Grazie per aver giocato a pong con me e avermi fatto vincere."
    m 1hua "Mi sono divertita molto! Giochiamoci ancora qualche volta, ok?"

    $ persistent._mas_pong_difficulty_change_next_game = PONG_DIFFICULTY_POWERDOWN;
    return


label mas_pong_dlg_loser_end:
    m 1wuo "Wow, Ci stavo davvero mettendo tutta me stessa questa volta."
    m 1eua "Devi aver fatto molta pratica per diventare cosi' bravo."
    m 2tuu "Immagino che tu volessi far colpo su di me, [player]."
    m 1hua "Sei così dolce~"
    return


label mas_pong_dlg_winner_end:
    m 4tku "Non riesco ad essere davvero emozionata per un gioco così semplice..."
    m 1eua "Ma almeno è divertente giocarci."
    m 1ekbsa "Especialmente con te, [player]."
    m 1hubfb "Ahaha!"
    m 1ekbfa "Grazie per avermi fatto vincere."
    m 1tku "Solo gli studenti delle elementari perdono seriamente a Pong, giusto?"
    m 1hua "Ehehe~"
    return

