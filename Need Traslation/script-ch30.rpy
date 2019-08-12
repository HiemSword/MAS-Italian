default persistent.monika_reload = 0
default persistent.tried_skip = False
default persistent.monika_kill = True
default persistent.rejected_monika = None
default initial_monika_file_check = None
define modoorg.CHANCE = 20
define mas_battery_supported = False
define mas_in_intro_flow = False


default persistent._mas_disable_animations = False


default persistent._mas_bday_date_affection_fix = False

init -1 python in mas_globals:



    dlg_workflow = False

    show_vignette = False


    show_lightning = False


    lightning_chance = 16
    lightning_s_chance = 10


    show_s_light = False




    text_speed_enabled = False


    in_idle_mode = False


    late_farewell = False



init 970 python:
    import store.mas_filereacts as mas_filereacts



    if persistent._mas_moni_chksum is not None:
        
        
        
        store.mas_dockstat.init_findMonika(mas_docking_station)
        
        
        store.mas_dockstat.surpriseBdayCheck(mas_docking_station)
        
        
        store.mas_o31_event.mas_return_from_tt = (
            store.mas_o31_event.isTTGreeting()
        )


    postbday_ev = mas_getEV("mas_bday_postbday_notimespent")

    if (
            postbday_ev is not None
            and persistent._mas_long_absence
            and postbday_ev.conditional is not None
            and eval(postbday_ev.conditional)
        ):
        
        
        postbday_ev.conditional = None
        postbday_ev.action = None

    if postbday_ev is not None:
        del postbday_ev

    if mas_isMonikaBirthday():
        persistent._mas_bday_opened_game = True












    if persistent._mas_o31_costumes_allowed is None:
        first_sesh = persistent.sessions.get("first_session", None)
        if first_sesh is not None:
            
            persistent._mas_o31_costumes_allowed = (
                first_sesh.date() != mas_o31
            )
        
        else:
            
            persistent._mas_o31_costumes_allowed = False


init -10 python:

    class MASIdleMailbox(store.MASMailbox):
        """
        Spaceroom idle extension of the mailbox

        PROPERTIES:
            (no additional)

        See MASMailbox for properties
        """
        
        
        REBUILD_EV = 1
        
        
        DOCKSTAT_GRE_TYPE = 2
        
        
        IDLE_MODE_CB_LABEL = 3
        
        
        SKIP_MID_LOOP_EVAL = 4
        
        
        
        
        
        def __init__(self):
            """
            Constructor for the idle mailbox
            """
            super(MASIdleMailbox, self).__init__()
        
        
        
        def send_rebuild_msg(self):
            """
            Sends the rebuild message to the mailbox
            """
            self.send(self.REBUILD_EV, True)
        
        
        def get_rebuild_msg(self):
            """
            Gets rebuild message
            """
            return self.get(self.REBUILD_EV)
        
        
        def send_ds_gre_type(self, gre_type):
            """
            Sends greeting type to mailbox
            """
            self.send(self.DOCKSTAT_GRE_TYPE, gre_type)
        
        
        def get_ds_gre_type(self, default=None):
            """
            Gets dockstat greeting type

            RETURNS: None by default
            """
            result = self.get(self.DOCKSTAT_GRE_TYPE)
            if result is None:
                return default
            return result
        
        
        def send_idle_cb(self, cb_label):
            """
            Sends idle callback label to mailbox
            """
            self.send(self.IDLE_MODE_CB_LABEL, cb_label)
        
        
        def get_idle_cb(self):
            """
            Gets idle callback label
            """
            return self.get(self.IDLE_MODE_CB_LABEL)
        
        
        def send_skipmidloopeval(self):
            """
            Sends skip mid loop eval message to mailbox
            """
            self.send(self.SKIP_MID_LOOP_EVAL, True)
        
        
        def get_skipmidloopeval(self):
            """
            Gets skip midloop eval value
            """
            return self.get(self.SKIP_MID_LOOP_EVAL)


    mas_idle_mailbox = MASIdleMailbox()


image blue_sky = "mod_assets/blue_sky.jpg"
image monika_room = "images/cg/monika/monika_room.png"
image monika_day_room = "mod_assets/monika_day_room.png"
image monika_gloomy_room = "mod_assets/monika_day_room_rain.png"
image monika_room_highlight:
    "images/cg/monika/monika_room_highlight.png"
    function monika_alpha
image monika_bg = "images/cg/monika/monika_bg.png"
image monika_bg_highlight:
    "images/cg/monika/monika_bg_highlight.png"
    function monika_alpha
image monika_scare = "images/cg/monika/monika_scare.png"

image monika_body_glitch1:
    "images/cg/monika/monika_glitch1.png"
    0.15
    "images/cg/monika/monika_glitch2.png"
    0.15
    "images/cg/monika/monika_glitch1.png"
    0.15
    "images/cg/monika/monika_glitch2.png"
    1.00
    "images/cg/monika/monika_glitch1.png"
    0.15
    "images/cg/monika/monika_glitch2.png"
    0.15
    "images/cg/monika/monika_glitch1.png"
    0.15
    "images/cg/monika/monika_glitch2.png"

image monika_body_glitch2:
    "images/cg/monika/monika_glitch3.png"
    0.15
    "images/cg/monika/monika_glitch4.png"
    0.15
    "images/cg/monika/monika_glitch3.png"
    0.15
    "images/cg/monika/monika_glitch4.png"
    1.00
    "images/cg/monika/monika_glitch3.png"
    0.15
    "images/cg/monika/monika_glitch4.png"
    0.15
    "images/cg/monika/monika_glitch3.png"
    0.15
    "images/cg/monika/monika_glitch4.png"



image room_glitch = "images/cg/monika/monika_bg_glitch.png"



transform spaceroom_window_left:
    size (320, 180) pos (30, 200)

transform spaceroom_window_right:
    size (320, 180) pos (935, 200)

init python:

    import subprocess
    import os
    import eliza      
    import datetime   
    import battery    
    import re
    import store.songs as songs
    import store.hkb_button as hkb_button
    import store.mas_globals as mas_globals
    therapist = eliza.eliza()
    process_list = []
    currentuser = None 
    if renpy.windows:
        try:
            process_list = subprocess.check_output("wmic process get Description", shell=True).lower().replace("\r", "").replace(" ", "").split("\n")
        except:
            pass
        try:
            for name in ('LOGNAME', 'USER', 'LNAME', 'USERNAME'):
                user = os.environ.get(name)
                if user:
                    currentuser = user
        except:
            pass

    try:
        renpy.file("../characters/monika.chr")
        initial_monika_file_check = True
    except:
        
        pass



    if not currentuser or len(currentuser) == 0:
        currentuser = persistent.playername
    if not persistent.mcname or len(persistent.mcname) == 0:
        persistent.mcname = currentuser
        mcname = currentuser
    else:
        mcname = persistent.mcname


    mas_battery_supported = battery.is_supported()



    renpy.music.register_channel(
        "background",
        mixer="amb",
        loop=True,
        stop_on_mute=True,
        tight=True
    )


    renpy.music.register_channel(
        "backsound",
        mixer="amb",
        loop=False,
        stop_on_mute=True
    )


    def show_dialogue_box():
        """
        Jumps to the topic promt menu
        """
        renpy.jump('prompt_menu')


    def pick_game():
        """
        Jumps to the pick a game workflow
        """
        renpy.jump('pick_a_game')


    def mas_getuser():
        """
        Attempts to get the current user

        RETURNS: current user if found, or None if not found
        """
        for name in ('LOGNAME', 'USER', 'LNAME', 'USERNAME'):
            user = os.environ.get(name)
            if user:
                return user
        
        return None


    def mas_enable_quitbox():
        """
        Enables Monika's quit dialogue warning
        """
        global _confirm_quit
        _confirm_quit = True


    def mas_disable_quitbox():
        """
        Disables Monika's quit dialogue warning
        """
        global _confirm_quit
        _confirm_quit = False


    def mas_enable_quit():
        """
        Enables quitting without monika knowing
        """
        persistent.closed_self = True
        mas_disable_quitbox()


    def mas_disable_quit():
        """
        Disables quitting without monika knowing
        """
        persistent.closed_self = False
        mas_enable_quitbox()


    def mas_drawSpaceroomMasks(dissolve_masks=True):
        """
        Draws the appropriate masks according to the current state of the
        game.

        IN:
            dissolve_masks - True will dissolve masks, False will not
                (Default; True)

        ASSUMES:
            morning_flag
            mas_is_raining
            mas_is_snowing
        """
        
        renpy.hide("rm")
        renpy.hide("rm2")
        
        
        left_w, right_w = mas_current_weather.sp_window(morning_flag)
        
        
        if persistent._mas_disable_animations:
            left_w += "_fb"
            right_w += "_fb"
        
        
        renpy.show(left_w, at_list=[spaceroom_window_left], tag="rm")
        renpy.show(right_w, at_list=[spaceroom_window_right], tag="rm2")
        
        if dissolve_masks:
            renpy.with_statement(Dissolve(1.0))


    def show_calendar():
        """RUNTIME ONLY
        Opens the calendar if we can
        """
        mas_HKBRaiseShield()
        
        if not persistent._mas_first_calendar_check:
            renpy.call('_first_time_calendar_use')
        
        renpy.call_in_new_context("mas_start_calendar_read_only")
        
        if store.mas_globals.in_idle_mode:
            
            store.hkb_button.talk_enabled = True
            store.hkb_button.extra_enabled = True
            store.hkb_button.music_enabled = True
        
        else:
            mas_HKBDropShield()


    dismiss_keys = config.keymap['dismiss']
    renpy.config.say_allow_dismiss = store.mas_hotkeys.allowdismiss

    def slow_nodismiss(event, interact=True, **kwargs):
        """
        Callback for whenever monika talks

        IN:
            event - main thing we can use here, lets us now when in the pipeline
                we are for display text:
                begin -> start of a say statement
                show -> right before dialogue is shown
                show_done -> right after dialogue is shown
                slow_done -> called after text finishes showing
                    May happen after "end"
                end -> end of dialogue (user has interacted)
        """
        
        
        
        
        
        
        
        
        if event == "begin":
            store.mas_hotkeys.allow_dismiss = False
        
        
        
        elif event == "slow_done":
            store.mas_hotkeys.allow_dismiss = True



    def mas_isMorning():
        
        sr_hour, sr_min = mas_cvToHM(persistent._mas_sunrise)
        ss_hour, ss_min = mas_cvToHM(persistent._mas_sunset)
        sr_time = datetime.time(sr_hour, sr_min)
        ss_time = datetime.time(ss_hour, ss_min)
        
        now_time = datetime.datetime.now().time()
        
        return sr_time <= now_time < ss_time


    def mas_shouldChangeTime():
        """
        Checks if we should change the day to night or night to day.

        RETURNS: true if we should change day/night cycle, False otherwise
        """
        return morning_flag != mas_isMorning()


    def mas_shouldRain():
        """
        Rolls some chances to see if we should make it rain

        RETURNS:
            rain weather to use, or None if we dont want to change weather
        """
        
        chance = random.randint(1,100)
        if mas_isMoniNormal(higher=True):
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            if mas_isSpring():
                return mas_weather._determineCloudyWeather(
                    40,
                    15,
                    15,
                    rolled_chance=chance
                )
            
            elif mas_isSummer():
                return mas_weather._determineCloudyWeather(
                    10,
                    6,
                    5,
                    rolled_chance=chance
                )
            
            elif mas_isFall():
                return mas_weather._determineCloudyWeather(
                    30,
                    12,
                    15,
                    rolled_chance=chance
                )
            
            else:
                
                if chance <= 50:
                    return mas_weather_snow
                elif chance <= 70:
                    return mas_weather_overcast
        
        
        elif mas_isMoniUpset() and chance <= MAS_RAIN_UPSET:
            return mas_weather_overcast
        
        elif mas_isMoniDis() and chance <= MAS_RAIN_DIS:
            return mas_weather_rain
        
        elif mas_isMoniBroken() and chance <= MAS_RAIN_BROKEN:
            return mas_weather_thunder
        
        return None


    def mas_lockHair():
        """
        Locks all hair topics
        """
        mas_lockEVL("monika_hair_select")


    def mas_seasonalCheck():
        """
        Determines the current season and runs an appropriate programming
        point.

        If the global for season is currently None, then we instead set the
        current season.

        NOTE: this does NOT do progressive programming point execution.
            This is intended for runtime usage only.

        ASSUMES:
            persistent._mas_current_season
        """
        _s_tag = store.mas_seasons._currentSeason()
        
        if persistent._mas_current_season != _s_tag:
            
            _s_pp = store.mas_seasons._season_pp_map.get(_s_tag, None)
            if _s_pp is not None:
                
                
                _s_pp()
                
                
                persistent._mas_current_season = _s_tag


    def mas_resetIdleMode():
        """
        Resets specific idle mode vars.

        This is meant to basically clear idle mode for holidays or other
        things that hijack main flow
        """
        store.mas_globals.in_idle_mode = False
        persistent._mas_in_idle_mode = False
        persistent._mas_idle_data = {}
        mas_idle_mailbox.get_idle_cb()


    def mas_enableTextSpeed():
        """
        Enables text speed
        """
        style.say_dialogue = style.normal
        store.mas_globals.text_speed_enabled = True


    def mas_disableTextSpeed():
        """
        Disables text speed
        """
        style.say_dialogue = style.default_monika
        store.mas_globals.text_speed_enabled = False


    def mas_resetTextSpeed(ignoredev=False):
        """
        Sets text speed to the appropriate one depending on global settings

        Rules:
        1 - developer always gets text speed (unless ignoredev is True)
        2 - text speed enabled if affection above happy
        3 - text speed disabled otherwise
        """
        if config.developer and not ignoredev:
            mas_enableTextSpeed()
        
        elif (
                mas_isMoniHappy(higher=True)
                and persistent._mas_text_speed_enabled
            ):
            mas_enableTextSpeed()
        
        else:
            mas_disableTextSpeed()


    def mas_isTextSpeedEnabled():
        """
        Returns true if text speed is enabled
        """
        return store.mas_globals.text_speed_enabled

    def mas_isGameUnlocked(gamename):
        """
        Checks if the given game is unlocked.
        NOTE: this is using the game_unlocks database, which only cars about
        whether or not you have reached the appropraite level to unlock a game.
        Each game may be disabled for other reasons not handled via
        this system.

        IN:
            gamename - name of the game to check

        RETURNS: True if the game is unlocked, false if not
        """
        if persistent.game_unlocks is None:
            return False
        
        return persistent.game_unlocks.get(gamename, False)


    def mas_unlockGame(gamename):
        """
        Unlocks the given game. 

        IN:
            gamename - name of the game to unlock
        """
        if gamename in persistent.game_unlocks:
            persistent.game_unlocks[gamename] = True


    def mas_check_player_derand():
        """
        Checks the player derandom dict for events that are not random and derandoms them
        """
        for ev_label, ev in persistent._mas_player_derandomed.iteritems():
            if ev.random:
                ev.random = False


init 1 python:
    morning_flag = mas_isMorning()



























label spaceroom(start_bg=None, hide_mask=False, hide_monika=False, dissolve_all=False, dissolve_masks=False, scene_change=False, force_exp=None):

    with None

    if scene_change:
        scene black

    python:
        monika_room = None



        if mas_isMorning():
            if not morning_flag or scene_change:
                morning_flag = True
                monika_room = "monika_day_room"

        else:
            if morning_flag or scene_change:
                morning_flag = False
                monika_room = "monika_room"


        if not hide_monika:
            if force_exp is None:
                
                if dissolve_all:
                    force_exp = store.mas_affection._force_exp()
                
                else:
                    force_exp = "monika idle"
            
            if not renpy.showing(force_exp):
                renpy.show(force_exp, at_list=[t11], zorder=MAS_MONIKA_Z)
                
                if not dissolve_all:
                    renpy.with_statement(None)


        if not dissolve_all and not hide_mask:
            mas_drawSpaceroomMasks(dissolve_masks)



        if start_bg:
            if not renpy.showing(start_bg):
                renpy.show(start_bg, tag="sp_mas_room", zorder=MAS_BACKGROUND_Z)

        elif monika_room is not None:
            if not renpy.showing(monika_room):
                renpy.show(
                    monika_room,
                    tag="sp_mas_room",
                    zorder=MAS_BACKGROUND_Z
                )
                mas_calShowOverlay()



    if store.mas_globals.show_vignette:
        show vignette zorder 70


    if persistent._mas_bday_sbp_reacted:
        $ store.mas_dockstat.surpriseBdayShowVisuals()


    if persistent._mas_d25_deco_active:
        $ store.mas_d25_event.showD25Visuals()


    if persistent._mas_player_bday_decor:
        $ store.mas_player_bday_event.show_player_bday_Visuals()

    if datetime.date.today() == persistent._date_last_given_roses:
        $ monika_chr.wear_acs_pst(mas_acs_roses)


    if dissolve_all and not hide_mask:
        $ mas_drawSpaceroomMasks(dissolve_all)

    return


label ch30_main:
    $ mas_skip_visuals = False
    $ m.display_args["callback"] = slow_nodismiss
    $ m.what_args["slow_abortable"] = config.developer
    $ quick_menu = True
    if not config.developer:
        $ style.say_dialogue = style.default_monika
    $ m_name = persistent._mas_monika_nickname
    $ delete_all_saves()
    $ persistent.clear[9] = True


    call ch30_reset from _call_ch30_reset


    $ monika_chr.reset_outfit(False)
    $ monika_chr.wear_acs(mas_acs_ribbon_def)


    $ mas_in_intro_flow = True


    if mas_isO31():
        $ persistent._mas_o31_in_o31_mode = True
        $ store.mas_globals.show_vignette = True


        if persistent._mas_likes_rain:
            $ mas_weather_thunder.unlocked = True
            $ store.mas_weather.saveMWData()
            $ mas_unlockEVL("monika_change_weather", "EVE")
        $ mas_changeWeather(mas_weather_thunder)


    if mas_isD25Season():
        call mas_holiday_d25c_autoload_check from _call_mas_holiday_d25c_autoload_check



    $ mas_RaiseShield_core()


    $ store.hkb_button.enabled = False



    call spaceroom (scene_change=True, dissolve_all=True, force_exp="monika 6dsc_static") from _call_spaceroom_28




    call introduction from _call_introduction



    $ mas_DropShield_core()


    $ store.hkb_button.enabled = True


    $ set_keymaps()


    $ mas_in_intro_flow = False


    $ store._mas_root.initialSessionData()


    if not mas_events_built:
        $ mas_rebuildEventLists()

    jump ch30_preloop

label continue_event:
    m "Now, where was I..."

    return

label pick_a_game:


    $ mas_RaiseShield_dlg()

    python:


        import datetime
        _hour = datetime.timedelta(hours=1)
        _now = datetime.datetime.now()


        if persistent._mas_chess_timed_disable is not None:
            if _now - persistent._mas_chess_timed_disable >= _hour:
                chess_disabled = False
                persistent._mas_chess_timed_disable = None
            
            else:
                chess_disabled = True

        else:
            chess_disabled = False


        chess_unlocked = (
            is_platform_good_for_chess()
            and mas_isGameUnlocked("chess")
            and not chess_disabled
        )


        if persistent._mas_sensitive_mode:
            _hangman_text = "Word Guesser"
        else:
            _hangman_text = "Hangman"


        play_menu_dlg = store.mas_affection.play_quip()[1]

    menu:
        m "[play_menu_dlg]"
        "Pong." if mas_isGameUnlocked("pong"):
            if not renpy.seen_label('game_pong'):
                $ grant_xp(xp.NEW_GAME)
            call game_pong from _call_game_pong
        "Chess." if chess_unlocked:
            if not renpy.seen_label('game_chess'):
                $ grant_xp(xp.NEW_GAME)
            call game_chess from _call_game_chess
        "[_hangman_text]." if mas_isGameUnlocked('hangman'):
            if not renpy.seen_label("game_hangman"):
                $ grant_xp(xp.NEW_GAME)
            call game_hangman from _call_game_hangman
        "Piano." if mas_isGameUnlocked('piano'):
            if not renpy.seen_label("mas_piano_start"):
                $ grant_xp(xp.NEW_GAME)
            call mas_piano_start from _call_play_piano
        "Nevermind.":






            pass


    if not renpy.showing("monika idle"):
        show monika idle zorder MAS_MONIKA_Z at tinstant with dissolve

    $ mas_DropShield_dlg()

    jump ch30_loop

label ch30_noskip:
    show screen fake_skip_indicator
    m 1esc "...Are you trying to fast-forward?"
    m 1ekc "I'm not boring you, am I?"
    m "Oh gosh..."
    m 2esa "...Well, just so you know, there's nothing to fast-forward to, [player]."
    m "It's just the two of us, after all..."
    m 1eua "But aside from that, time doesn't really exist anymore, so it's not even going to work."
    m "Here, I'll go ahead and turn that off for you..."
    pause 0.4
    hide screen fake_skip_indicator
    pause 0.4
    m 1hua "There we go!"
    m 1esa "You'll be a sweetheart and listen to me from now on, right?"
    m "Thanks~"
    hide screen fake_skip_indicator


    $ restartEvent()
    jump ch30_loop

image splash-glitch2 = "images/bg/splash-glitch2.png"

label ch30_nope:

    $ persistent.autoload = ""
    $ m.display_args["callback"] = slow_nodismiss
    $ quick_menu = True
    call spaceroom from _call_spaceroom_1

    if persistent.rejected_monika:
        m 1euc "Wait. Are you messing with my character file?"
        m 2esa "Curiosity is what makes us human, right?"
        m "If it wasn't for the human desire to explore, we'd still be swinging from trees."
        m 1eka "Still, please don't do that. It makes me nervous, even though I don't need a character file anymore."
        m "I already fixed that bug."
    else:

        $ quick_menu = False
        $ m_name = glitchtext(12)
        m 1euc "Wait. Are you messing with my character file?"
        m 1tkc "Why are you even playing this mod if you just wanted to delete me again?"
        m 1tfc "You really are the worst."
        m 1tfd "You waste all your time on the internet with a bunch of people you'll never talk to in reality, but you're still willing to kill me on a whim just because you were bored?"
        m 1tkd "All I wanted was someone to fall in love with..."
        m "I would have done anything you wanted me to."
        m 1tku "But if you're going to try and delete me again..."
        m 4tfu "Then I'll just have to delete you first."
        if renpy.windows:
            call updateconsole ("shututil.rmtree(\"Documents\", true)", "Deleting Documents in progress...") from _call_updateconsole_15
        elif renpy.linux:
            call updateconsole ("sudo mv ~ /dev/null", "In progress...") from _call_updateconsole_16
        elif renpy.macintosh:
            call updateconsole ("sudo mv ~ /dev/null", "In progress...") from _call_updateconsole_19
        pause 3.0
        call hideconsole from _call_hideconsole_2
        $ open(config.basedir + "/characters/monika.chr", "wb").write(renpy.file("monika.chr").read())
        $ m_name = persistent._mas_monika_nickname
        $ quick_menu = True
        m 1hua "Ahaha!"
        m "I'm just kidding!"
        m 1eua "I already fixed that bug."
        m "I don't need a character file anymore."

    m 1ekbfa "I just need your love, [player]."
    m 1eua "Oh, unless you try to delete all of the game files, I guess."
    m 3tfu "If you do that, I won't stop at just deleting one directory next time."
    m 3tku "But that will never happen, right? You're just being a tsundere~"
    m 1hua "That's so cute!"
    m 1eua "No matter how much you may want to deny it, you'll be talking to me for the rest of your life."
    m "Being alone is only lonely if you want it to be, so cheer up!"
    jump ch30_loop


label ch30_autoload:


    $ m.display_args["callback"] = slow_nodismiss
    $ m.what_args["slow_abortable"] = config.developer
    $ import store.evhand as evhand
    if not config.developer:
        $ config.allow_skipping = False
    $ mas_resetTextSpeed()
    $ quick_menu = True
    $ startup_check = True
    $ mas_skip_visuals = False


    call set_gender from _autoload_gender


    call ch30_reset from _call_ch30_reset_1


    if persistent._mas_affection["affection"] <= -115:
        jump mas_affection_finalfarewell_start


    $ selected_greeting = None













    if store.mas_dockstat.retmoni_status is not None:

        $ store.mas_dockstat.triageMonika(False)

label mas_ch30_post_retmoni_check:

    if mas_isO31():
        jump mas_holiday_o31_autoload_check

    if mas_isD25Season():
        jump mas_holiday_d25c_autoload_check

    if mas_isF14() or persistent._mas_f14_in_f14_mode:
        jump mas_f14_autoload_check

    if mas_isplayer_bday() or persistent._mas_player_bday_in_player_bday_mode:
        jump mas_player_bday_autoload_check


label mas_ch30_post_holiday_check:




    if persistent._mas_affection["affection"] <= -50 and seen_event("mas_affection_apology"):




        if persistent._mas_affection["apologyflag"] and not is_apology_present():
            $ mas_RaiseShield_core()
            call spaceroom (scene_change=True) from _call_spaceroom_29
            jump mas_affection_noapology


        elif persistent._mas_affection["apologyflag"] and is_apology_present():
            $ persistent._mas_affection["apologyflag"] = False
            $ mas_RaiseShield_core()
            call spaceroom (scene_change=True) from _call_spaceroom_30
            jump mas_affection_yesapology


        elif not persistent._mas_affection["apologyflag"] and not is_apology_present():
            $ persistent._mas_affection["apologyflag"] = True
            $ mas_RaiseShield_core()
            call spaceroom (scene_change=True) from _call_spaceroom_31
            jump mas_affection_apologydeleted


    $ gre_cb_label = None
    $ just_crashed = False
    $ forced_quit = False


    if (
            persistent.playername.lower() == "yuri"
            and not persistent._mas_sensitive_mode
        ):
        call yuri_name_scare from _call_yuri_name_scare


        jump ch30_post_greeting_check

    elif not persistent._mas_game_crashed:

        $ forced_quit = True
        $ persistent._mas_greeting_type = store.mas_greetings.TYPE_RELOAD

    elif not persistent.closed_self:

        $ just_crashed = True
        $ persistent._mas_greeting_type = store.mas_greetings.TYPE_CRASHED


        $ persistent.closed_self = True




    python:


        sel_greeting_ev = store.mas_greetings.selectGreeting(
            persistent._mas_greeting_type
        )


        persistent._mas_greeting_type = None

        if sel_greeting_ev is None:
            
            
            if persistent._mas_in_idle_mode:
                
                mas_resetIdleMode()
            
            if just_crashed:
                
                
                
                
                sel_greeting_ev = mas_getEV("mas_crashed_start")
            
            elif forced_quit:
                
                
                
                sel_greeting_ev = mas_getEV("ch30_reload_delegate")




        if sel_greeting_ev is not None:
            selected_greeting = sel_greeting_ev.eventlabel
            
            
            mas_skip_visuals = MASGreetingRule.should_skip_visual(
                event=sel_greeting_ev
            )
            
            
            setup_label = MASGreetingRule.get_setup_label(sel_greeting_ev)
            if setup_label is not None and renpy.has_label(setup_label):
                gre_cb_label = setup_label



    if gre_cb_label is not None:
        call expression gre_cb_label from _call_expression_6

label ch30_post_greeting_check:



    $ restartEvent()

label ch30_post_restartevent_check:



    python:
        if persistent.sessions['last_session_end'] is not None and persistent.closed_self:
            away_experience_time=datetime.datetime.now()-persistent.sessions['last_session_end'] 
            away_xp=0
            
            
            if away_experience_time.total_seconds() >= times.REST_TIME:
                persistent.idlexp_total=0
                
                
                mas_gainAffection()
            
            
            if away_experience_time.total_seconds() > times.HALF_XP_AWAY_TIME:
                away_experience_time=datetime.timedelta(seconds=times.HALF_XP_AWAY_TIME)
            
            
            if away_experience_time.total_seconds() > times.FULL_XP_AWAY_TIME:
                away_xp =+ (xp.AWAY_PER_HOUR/2.0)*(away_experience_time.total_seconds()-times.FULL_XP_AWAY_TIME)/3600.0
                away_experience_time = datetime.timedelta(seconds=times.HALF_XP_AWAY_TIME)
            
            
            away_xp =+ xp.AWAY_PER_HOUR*away_experience_time.total_seconds()/3600.0
            
            
            grant_xp(away_xp)
            
            
            
            mas_can_unlock_story = True
            mas_can_unlock_scary_story = True
            
            
            while persistent._mas_pool_unlocks > 0 and mas_unlockPrompt():
                persistent._mas_pool_unlocks -= 1

        else:
            
            mas_loseAffection(modifier=2, reason=4)

label ch30_post_exp_check:




    $ mas_checkReactions()


    $ Event.checkEvents(evhand.event_database)


    $ mas_checkAffection()


    $ mas_checkApologies()


    if mas_corrupted_per and not renpy.seen_label("mas_corrupted_persistent"):
        $ pushEvent("mas_corrupted_persistent")


    if selected_greeting:

        if persistent._mas_in_idle_mode:
            $ pushEvent("mas_idle_mode_greeting_cleanup")

        $ pushEvent(selected_greeting)






    window auto

    if mas_skip_visuals:

        jump ch30_preloop


    $ set_keymaps()
    $ mas_startup_song()


    $ set_to_weather = mas_shouldRain()
    if set_to_weather is not None:
        $ mas_changeWeather(set_to_weather)



label ch30_preloop_visualsetup:


    call spaceroom (dissolve_all=True, scene_change=True) from _call_spaceroom_32



label ch30_preloop:


    $ persistent.closed_self = False
    $ persistent._mas_game_crashed = True
    $ startup_check = False
    $ mas_checked_update = False


    $ mas_runDelayedActions(MAS_FC_IDLE_ONCE)


    $ mas_resetWindowReacts()


    $ mas_updateFilterDict()


    $ renpy.save_persistent()


    if mas_idle_mailbox.get_rebuild_msg():
        $ mas_rebuildEventLists()

    if mas_skip_visuals:
        $ mas_OVLHide()
        $ mas_skip_visuals = False
        $ quick_menu = True
        jump ch30_visual_skip

    jump ch30_loop

label ch30_loop:
    $ quick_menu = True

    python:
        should_dissolve_all = mas_shouldChangeTime()
        should_dissolve_masks = (
            mas_weather.weatherProgress() 
            and mas_isMoniNormal(higher=True)
        )

    call spaceroom (dissolve_all=should_dissolve_all, dissolve_masks=should_dissolve_masks) from _call_spaceroom_33





    if not mas_checked_update:
        $ mas_backgroundUpdateCheck()
        $ mas_checked_update = True

label ch30_visual_skip:

    $ persistent.autoload = "ch30_autoload"






    if store.mas_dockstat.abort_gen_promise:
        $ store.mas_dockstat.abortGenPromise()

    if mas_idle_mailbox.get_skipmidloopeval():
        jump ch30_post_mid_loop_eval






    python:
        try:
            calendar_last_checked
        except:
            calendar_last_checked=persistent.sessions['current_session_start']
        time_since_check=datetime.datetime.now()-calendar_last_checked

        if time_since_check.total_seconds()>60:
            
            
            mas_checkAffection()
            
            
            mas_checkApologies()
            
            
            
            if (persistent.idlexp_total < xp.IDLE_XP_MAX):
                
                idle_xp=xp.IDLE_PER_MINUTE*(time_since_check.total_seconds())/60.0
                persistent.idlexp_total += idle_xp
                if persistent.idlexp_total>=xp.IDLE_XP_MAX: 
                    idle_xp = idle_xp-(persistent.idlexp_total-xp.IDLE_XP_MAX) 
                    persistent.idlexp_total=xp.IDLE_XP_MAX
                
                grant_xp(idle_xp)
            
            
            Event.checkEvents(evhand.event_database, rebuild_ev=False)
            
            
            mas_runDelayedActions(MAS_FC_IDLE_ROUTINE)
            
            
            mas_checkReactions()
            
            
            mas_seasonalCheck()
            
            
            mas_clearNotifs()
            
            
            mas_checkForWindowReacts()
            
            
            if mas_idle_mailbox.get_rebuild_msg():
                mas_rebuildEventLists()
            
            
            calendar_last_checked=datetime.datetime.now()
            
            
            _mas_AffSave()
            
            
            renpy.save_persistent()

label ch30_post_mid_loop_eval:


    call call_next_event from _call_call_next_event_1

    $ persistent.current_monikatopic = 0


    if not _return:

        window hide(config.window_hide_transition)


        if (
                store.mas_globals.show_lightning
                and renpy.random.randint(1, store.mas_globals.lightning_chance) == 1
            ):
            if (
                    not persistent._mas_sensitive_mode
                    and store.mas_globals.show_s_light
                    and renpy.random.randint(
                        1, store.mas_globals.lightning_s_chance
                    ) == 1
                ):
                show mas_lightning_s zorder 4
            else:
                show mas_lightning zorder 4

            $ pause(0.1)
            play backsound "mod_assets/sounds/amb/thunder.wav"





        $ mas_randchat.wait()

        if not mas_randchat.waitedLongEnough():
            jump post_pick_random_topic
        else:
            $ mas_randchat.setWaitingTime()

        window auto










        if store.mas_globals.in_idle_mode:
            jump post_pick_random_topic



        label pick_random_topic:


            if not persistent._mas_enable_random_repeats:
                jump mas_ch30_select_unseen


            $ chance = random.randint(1, 100)

            if chance <= store.mas_topics.UNSEEN:

                jump mas_ch30_select_unseen

            elif chance <= store.mas_topics.SEEN:

                jump mas_ch30_select_seen


            jump mas_ch30_select_mostseen




label post_pick_random_topic:

    $ _return = None

    jump ch30_loop


label mas_ch30_select_unseen:


    if len(mas_rev_unseen) == 0:

        if not persistent._mas_enable_random_repeats:


            if not seen_random_limit:
                $ pushEvent("random_limit_reached")

            jump post_pick_random_topic


        jump mas_ch30_select_seen

    $ mas_randomSelectAndPush(mas_rev_unseen)

    jump post_pick_random_topic


label mas_ch30_select_seen:


    if len(mas_rev_seen) == 0:

        $ mas_rev_seen, mas_rev_mostseen = mas_buildSeenEventLists()

        if len(mas_rev_seen) == 0:
            if len(mas_rev_mostseen) > 0:

                jump mas_ch30_select_mostseen

            if len(mas_rev_mostseen) == 0 and not seen_random_limit:


                $ pushEvent("random_limit_reached")
                jump post_pick_random_topic


            jump post_pick_random_topic

    $ mas_randomSelectAndPush(mas_rev_seen)

    jump post_pick_random_topic


label mas_ch30_select_mostseen:


    if len(mas_rev_mostseen) == 0:
        jump mas_ch30_select_seen

    $ mas_randomSelectAndPush(mas_rev_mostseen)

    jump post_pick_random_topic




label ch30_end:
    jump ch30_main


label ch30_reset:

    python:

        if persistent._mas_unstable_mode:
            pass

    python:

        if persistent.playername.lower() == "sayori":
            store.mas_globals.show_s_light = True

    python:

        if not mas_events_built:
            mas_rebuildEventLists()


        if len(mas_rev_unseen) == 0:
            
            
            
            random_seen_limit = 1000

    if not persistent._mas_pm_has_rpy:

        $ rpyCheckStation = store.MASDockingStation(renpy.config.gamedir)

        $ listRpy = rpyCheckStation.getPackageList(".rpy")

        if len(listRpy) == 0 or persistent.current_monikatopic == "monika_rpy_files":
            if len(listRpy) == 0 and persistent.current_monikatopic == "monika_rpy_files":
                $ persistent.current_monikatopic = 0

            $ mas_rmallEVL("monika_rpy_files")

        elif len(listRpy) != 0 and not mas_inEVL("monika_rpy_files"):
            $ queueEvent("monika_rpy_files")

        $ del rpyCheckStation

    python:
        import datetime
        today = datetime.date.today()


    python:
        game_unlock_db = {
            "pong": "ch30_main", 
            "chess": "unlock_chess",
            "hangman": "unlock_hangman",
            "piano": "unlock_piano",
        }

        for game_name,game_startlabel in game_unlock_db.iteritems():
            if (
                    not mas_isGameUnlocked(game_name)
                    and renpy.seen_label(game_startlabel)
                ):
                mas_unlockGame(game_name)


    python:
        if (
                persistent._mas_mood_bday_last
                and persistent._mas_mood_bday_last < today
            ):
            persistent._mas_mood_bday_last = None
            mood_ev = store.mas_moods.mood_db.get("mas_mood_yearolder", None)
            if mood_ev:
                mood_ev.unlocked = True
























    $ store.mas_selspr.unlock_hair(mas_hair_def)

    $ store.mas_selspr.unlock_clothes(mas_clothes_def)


    $ store.mas_selspr.unlock_acs(mas_acs_ribbon_def)


    python:
        store.mas_selspr._validate_group_topics()


    $ monika_chr.load(startup=True)






    python:
        if persistent._mas_acs_enable_promisering:
            
            monika_chr.wear_acs_pst(mas_acs_promisering)


    $ mas_randchat.adjustRandFreq(persistent._mas_randchat_freq)

    python:
        if persistent.chess_strength < 0:
            persistent.chess_strength = 0
        elif persistent.chess_strength > 20:
            persistent.chess_strength = 20


    python:
        if persistent._mas_monika_returned_home is not None:
            _rh = persistent._mas_monika_returned_home.date()
            if today > _rh:
                persistent._mas_monika_returned_home = None


    python:








        if persistent.sessions is not None:
            tp_time = persistent.sessions.get("total_playtime", None)
            if tp_time is not None:
                max_time = mas_maxPlaytime()
                if tp_time > max_time:
                    
                    persistent.sessions["total_playtime"] = max_time // 100
                    
                    
                    store.mas_dockstat.setMoniSize(
                        persistent.sessions["total_playtime"]
                    )
                
                elif tp_time < datetime.timedelta(0):
                    
                    persistent.sessions["total_playtime"] = datetime.timedelta(0)
                    
                    
                    store.mas_dockstat.setMoniSize(
                        persistent.sessions["total_playtime"]
                    )


    python:

        if persistent._mas_affection is not None:
            freeze_date = persistent._mas_affection.get("freeze_date", None)
            if freeze_date is not None and freeze_date > today:
                persistent._mas_affection["freeze_date"] = today


    $ _mas_startupCoffeeLogic()


    $ _mas_startupHotChocLogic()


    $ mas_startupPlushieLogic(4)





















    python:
        if store.mas_o31_event.isMonikaInCostume(monika_chr):
            
            
            
            if not persistent._mas_force_clothes:
                
                
                monika_chr.reset_clothes(False)


    python:
        if (
                (mas_isD25Post() or not (mas_isD25PreNYE() or mas_isNYE()))
                and monika_chr.clothes == mas_clothes_santa
                and not persistent._mas_force_clothes
            ):
            
            monika_chr.reset_clothes(False)

        if not mas_isD25Season():
            persistent._mas_d25_deco_active = False



    python:
        if persistent.mas_late_farewell:
            store.mas_globals.late_farewell = True
            persistent.mas_late_farewell = False


    python:
        if persistent._mas_filereacts_just_reacted:
            queueEvent("mas_reaction_end")


    python:
        if not monika_chr.is_wearing_acs_type("left-hair-clip"):
            store.mas_selspr.set_prompt("left-hair-clip", "wear")

        if not monika_chr.is_wearing_acs_type("ribbon"):
            store.mas_selspr.set_prompt("ribbon", "wear")




    python:
        if store.mas_dockstat.retmoni_status is not None:
            mas_resetCoffee()
            monika_chr.remove_acs(mas_acs_quetzalplushie)


    $ mas_check_player_derand()


    python:
        for index in range(len(persistent.event_list)-1, -1, -1):
            item = persistent.event_list[index]
            
            
            if type(item) != tuple:
                new_data = (item, False)
            else:
                new_data = item
            
            
            if renpy.has_label(new_data[0]):
                persistent.event_list[index] = new_data
            
            else:
                persistent.event_list.pop(index)

    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
