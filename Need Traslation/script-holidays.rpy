











default persistent._mas_o31_current_costume = None




default persistent._mas_o31_seen_costumes = None



default persistent._mas_o31_costume_greeting_seen = False


default persistent._mas_o31_costumes_allowed = None



default persistent._mas_o31_in_o31_mode = False





default persistent._mas_o31_dockstat_return = False


default persistent._mas_o31_went_trick_or_treating_short = False
default persistent._mas_o31_went_trick_or_treating_mid = False
default persistent._mas_o31_went_trick_or_treating_right = False
default persistent._mas_o31_went_trick_or_treating_long = False
default persistent._mas_o31_went_trick_or_treating_longlong = False







default persistent._mas_o31_went_trick_or_treating_abort = False


default persistent._mas_o31_trick_or_treating_start_early = False
default persistent._mas_o31_trick_or_treating_start_normal = False
default persistent._mas_o31_trick_or_treating_start_late = False



default persistent._mas_o31_trick_or_treating_aff_gain = 0



define mas_o31_marisa_chance = 90
define mas_o31_rin_chance = 10

define mas_o31 = datetime.date(datetime.date.today().year, 10, 31)









init -810 python:

    store.mas_history.addMHS(MASHistorySaver(
        "o31",
        datetime.datetime(2018, 11, 2),
        

        {
            

            "_mas_o31_current_costume": "o31.costume.was_worn",
            "_mas_o31_costume_greeting_seen": "o31.costume.greeting.seen",
            "_mas_o31_costumes_allowed": "o31.costume.allowed",

            
            "_mas_o31_in_o31_mode": "o31.mode.o31",

            "_mas_o31_dockstat_return": "o31.dockstat.returned_o31",
            "_mas_o31_went_trick_or_treating_short": "o31.actions.tt.short",
            "_mas_o31_went_trick_or_treating_mid": "o31.actions.tt.mid",
            "_mas_o31_went_trick_or_treating_right": "o31.actions.tt.right",
            "_mas_o31_went_trick_or_treating_long": "o31.actions.tt.long",
            "_mas_o31_went_trick_or_treating_longlong": "o31.actions.tt.longlong",
            "_mas_o31_went_trick_or_treating_abort": "o31.actions.tt.abort",
            "_mas_o31_trick_or_treating_start_early": "o31.actions.tt.start.early",
            "_mas_o31_trick_or_treating_start_normal": "o31.actions.tt.start.normal",
            "_mas_o31_trick_or_treating_start_late": "o31.actions.tt.start.late",
            "_mas_o31_trick_or_treating_aff_gain": "o31.actions.tt.aff_gain"

        }

    ))

init -10 python:
    def mas_isO31(_date=None):
        """
        Returns True if the given date is o31

        IN:
            _date - date to check.
                If None, we use today's date
                (Default: None)

        RETURNS: True if given date is o31, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()
        
        return _date == mas_o31.replace(year=_date.year)


init 101 python:

    if persistent._mas_o31_seen_costumes is None:
        persistent._mas_o31_seen_costumes = {
            "marisa": False,
            "rin": False
        }

    if (
            persistent._mas_o31_in_o31_mode
            and not mas_isO31()
            and not store.mas_o31_event.isTTGreeting()
        ):
        
        persistent._mas_o31_in_o31_mode = False
        
        
        unlockEventLabel(
            "i_greeting_monikaroom",
            store.evhand.greeting_database
        )
        
        if not persistent._mas_hair_changed:
            unlockEventLabel(
                "greeting_hairdown",
                store.evhand.greeting_database
            )



init -11 python in mas_o31_event:
    import store
    import store.mas_dockstat as mds
    import store.mas_ics as mis
    import datetime


    o31_cg_station = store.MASDockingStation(mis.o31_cg_folder)


    o31_cg_decoded = False


    mas_return_from_tt = False


    def decodeImage(key):
        """
        Attempts to decode a cg image

        IN:
            key - o31 cg key to decode

        RETURNS True upon success, False otherwise
        """
        return mds.decodeImages(o31_cg_station, mis.o31_map, [key])


    def removeImages():
        """
        Removes decoded images at the end of their lifecycle
        """
        mds.removeImages(o31_cg_station, mis.o31_map)


    def isMonikaInCostume(_monika_chr):
        """
        IN:
            _monika_chr - MASMonika object to check

        Returns true if monika is in costume
        """
        return (
            _monika_chr.clothes.name == "marisa"
            or _monika_chr.clothes.name == "rin"
        )


    def isTTGreeting():
        """
        RETURNS True if the persistent greeting type is the TT one
        """
        return (
            store.persistent._mas_greeting_type
            == store.mas_greetings.TYPE_HOL_O31_TT
        )


    def spentO31():
        """
        RETURNS True if the user spent o31 with monika.
        Currently we determine that by checking historical value for current
        costume for a non None value
        # TODO: this should be changed to a spent var one day
        """
        years_list = range(2017, datetime.date.today().year + 1)
        
        _data_found = store.mas_HistLookup_otl(
            "o31.costume.was_worn",
            years_list
        )
        
        for year, data_tuple in _data_found.iteritems():
            l_const, _data = data_tuple
            
            
            if l_const == 0 and _data is not None:
                return True
        
        return False


label mas_holiday_o31_autoload_check:





    python:
        import random

        if (
                persistent._mas_o31_current_costume is None
                and persistent._mas_o31_costumes_allowed
            ):
            
            
            persistent._mas_o31_in_o31_mode = True
            mas_skip_visuals = True
            
            
            mas_resetIdleMode()
            
            if random.randint(1,100) <= mas_o31_marisa_chance:
                persistent._mas_o31_current_costume = "marisa"
                selected_greeting = "greeting_o31_marisa"
                store.mas_o31_event.o31_cg_decoded = (
                    store.mas_o31_event.decodeImage("o31mcg")
                )
                store.mas_selspr.unlock_clothes(mas_clothes_marisa)
            
            else:
                persistent._mas_o31_current_costume = "rin"
                selected_greeting = "greeting_o31_rin"
                store.mas_o31_event.o31_cg_decoded = (
                    store.mas_o31_event.decodeImage("o31rcg")
                )
                store.mas_selspr.unlock_clothes(mas_clothes_rin)
            
            persistent._mas_o31_seen_costumes[persistent._mas_o31_current_costume] = True

        if persistent._mas_o31_in_o31_mode:
            store.mas_globals.show_vignette = True
            
            
            if persistent._mas_likes_rain:
                mas_weather_thunder.unlocked = True
                store.mas_weather.saveMWData()
                mas_unlockEVL("monika_change_weather", "EVE")
            mas_changeWeather(mas_weather_thunder)

    if mas_isplayer_bday() or persistent._mas_player_bday_in_player_bday_mode:
        call mas_player_bday_autoload_check from _call_mas_player_bday_autoload_check

    if mas_skip_visuals:
        jump ch30_post_restartevent_check


    $ lockEventLabel("i_greeting_monikaroom", store.evhand.greeting_database)


    $ lockEventLabel("greeting_hairdown", store.evhand.greeting_database)


    jump mas_ch30_post_holiday_check


label mas_holiday_o31_returned_home_relaunch:
    m 1eua "So, today is..."
    m 1euc "...wait."
    m "..."
    m 2wuo "Oh!"
    m 2wuw "Oh my gosh!"
    m 2hub "It's Halloween already, [player]."
    m 1eua "...{w}Say."
    m 3eua "I'm going to close the game."
    m 1eua "After that you can reopen it."
    m 1hubfa "I have something special in store for you, ehehe~"

    $ persistent._mas_o31_dockstat_return = True
    return "quit"


image mas_o31_marisa_cg = "mod_assets/monika/cg/o31_marisa_cg.png"


image mas_o31_rin_cg = "mod_assets/monika/cg/o31_rin_cg.png"


transform mas_o31_cg_scroll:
    xanchor 0.0 xpos 0 yanchor 0.0 ypos 0.0 yoffset -1520
    ease 20.0 yoffset 0.0


init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_o31_marisa",
            category=[store.mas_greetings.TYPE_HOL_O31]
        ),
        eventdb=evhand.greeting_database
    )

label greeting_o31_marisa:




    $ store.mas_hotkeys.music_enabled = False



    $ mas_calRaiseOverlayShield()






    $ monika_chr.change_clothes(mas_clothes_marisa, False)


    $ store.mas_sprites.reset_zoom()


    if store.mas_o31_event.o31_cg_decoded:


        call spaceroom (hide_monika=True, scene_change=True) from _call_spaceroom_5
        show emptydesk zorder 9 at i11
    else:



        call spaceroom (dissolve_all=True, scene_change=True, force_exp='monika 1eua_static') from _call_spaceroom_6

    m 1eua "Ah!"
    m 1hua "Seems like my spell worked."
    m 3efu "As my newly summoned servant, you'll have to do my bidding until the very end!"
    m 1rksdla "..."
    m 1hub "Ahaha!"


    if store.mas_o31_event.o31_cg_decoded:
        $ cg_delay = datetime.timedelta(seconds=20)


        m "I'm over here, [player]~"
        window hide

        show mas_o31_marisa_cg zorder 20 at mas_o31_cg_scroll with dissolve
        $ start_time = datetime.datetime.now()

        while datetime.datetime.now() - start_time < cg_delay:
            pause 1.0

        hide emptydesk
        show monika 1hua zorder MAS_MONIKA_Z at i11
        window auto
        m "Tadaa!~"



    m 1hua "Well..."
    m 1wub "What do you think?"
    m 1wua "Suits me pretty well, right?"
    m 1eua "It took me quite a while to make this costume, you know."
    m 3hksdlb "Getting the right measurements, making sure nothing was too tight or loose, that sort of stuff."
    m 3eksdla "Especially the hat!"
    m 1dkc "The ribbon wouldn't stay still at all..."
    m 1rksdla "Luckily I got that sorted out."
    m 3hua "I'd say I did a good job myself."
    m 1hub "Ehehe~"
    m 3eka "I'm wondering if you'll be able to see what's different today."
    m "Besides my costume of course~"
    m 1hua "But anyway..."

    if store.mas_o31_event.o31_cg_decoded:
        show monika 1eua
        hide mas_o31_marisa_cg with dissolve

    m 3ekbfa "I'm really excited to spend Halloween with you."
    m 1hua "Let's have fun today!"



    $ store.mas_hotkeys.music_enabled = True


    $ mas_calDropOverlayShield()


    $ set_keymaps()


    $ HKBShowButtons()


    $ mas_startup_song()

    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_o31_rin",
            category=[store.mas_greetings.TYPE_HOL_O31]
        ),
        eventdb=evhand.greeting_database
    )

label greeting_o31_rin:




    $ store.mas_hotkeys.music_enabled = False



    $ mas_calRaiseOverlayShield()






    $ monika_chr.change_clothes(mas_clothes_rin, False)


    $ store.mas_sprites.reset_zoom()
    $ title_cased_hes = hes.capitalize()


    call spaceroom (hide_monika=True, scene_change=True) from _call_spaceroom_7
    show emptydesk zorder 9 at i11

    m "Ugh, I hope I got these braids right."
    m "Why does this costume have to be so complicated...?"
    m "Oh shoot! [title_cased_hes] here!"
    window hide
    pause 3.0

    if store.mas_o31_event.o31_cg_decoded:
        $ cg_delay = datetime.timedelta(seconds=20)


        window auto
        m "Say, [player]..."
        window hide

        show mas_o31_rin_cg zorder 20 at mas_o31_cg_scroll with dissolve
        $ start_time = datetime.datetime.now()

        while datetime.datetime.now() - start_time < cg_delay:
            pause 1.0

        hide emptydesk
        window auto
        m "What do {i}nya{/i} think?"

        scene black
        pause 2.0
        call spaceroom (scene_change=True, dissolve_all=True, force_exp='monika 1hksdlb_static') from _call_spaceroom_8
        m 1hksdlb "Ahaha, saying that out loud was more embarrassing than I thought..."
    else:

        show monika 1eua zorder MAS_MONIKA_Z at t11
        m 1hub "Hi [player]!"
        hide emptydesk
        m 3hub "Do you like my costume?"


    m 3etc "Honestly, I don't even know who this is supposed to be."
    m 3etd "I just found it in the closet with a note attached that had the word 'Rin', a drawing of a girl pushing a wheelbarrow, and some blue floaty thingies."
    m 1euc "Along with instructions on how to style your hair to go along with this outfit."
    m "Judging by these cat ears, I'm guessing this character is a catgirl."
    m 1dtc "But why would she push a wheelbarrow around?"
    pause 1.0
    m 1hksdlb "Anyway, it was a pain getting my hair done."
    m 1eub "So I hope you like the costume!"



    $ store.mas_hotkeys.music_enabled = True


    $ mas_calDropOverlayShield()


    $ set_keymaps()


    $ HKBShowButtons()


    $ mas_startup_song()

    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_trick_or_treat_back",
            unlocked=True,
            category=[
                store.mas_greetings.TYPE_HOL_O31_TT
            ]
        ),
        eventdb=evhand.greeting_database
    )

label greeting_trick_or_treat_back:


    python:

        five_minutes = datetime.timedelta(seconds=5*60)
        one_hour = datetime.timedelta(seconds=3600)
        three_hour = datetime.timedelta(seconds=3*3600)
        time_out = store.mas_dockstat.diffCheckTimes()
        checkin_time = None
        is_past_sunrise_post31 = False
        wearing_costume = store.mas_o31_event.isMonikaInCostume(monika_chr)

        if len(persistent._mas_dockstat_checkin_log) > 0:
            checkin_time = persistent._mas_dockstat_checkin_log[-1:][0][0]
            sunrise_hour, sunrise_min = mas_cvToHM(persistent._mas_sunrise)
            is_past_sunrise_post31 = (
                datetime.datetime.now() > (
                    datetime.datetime.combine(
                        mas_o31,
                        datetime.time(sunrise_hour, sunrise_min)
                    )
                    + datetime.timedelta(days=1)
                )
            )

        def cap_gain_aff(amt):
            if persistent._mas_o31_trick_or_treating_aff_gain < 15:
                persistent._mas_o31_trick_or_treating_aff_gain += amt
                mas_gainAffection(amt, bypass=True)


    if time_out < five_minutes:
        $ mas_loseAffection()
        $ persistent._mas_o31_went_trick_or_treating_short = True
        m 2ekp "You call that trick or treating, [player]?"
        m "Where did we go, one house?"
        m 2efc "...If we even left."

    elif time_out < one_hour:
        $ cap_gain_aff(5)
        $ persistent._mas_o31_went_trick_or_treating_mid = True
        m 2ekp "That was pretty short for trick or treating, [player]."
        m 3eka "But I enjoyed it while it lasted."
        m 1eka "It was still really nice being right there with you~"

    elif time_out < three_hour:
        $ cap_gain_aff(10)
        $ persistent._mas_o31_went_trick_or_treating_right = True
        m 1hua "And we're home!"
        m 1hub "I hope we got lots of delicious candy!"
        m 1eka "I really enjoyed trick or treating with you, [player]..."

        if wearing_costume:
            m 2eka "Even if I couldn't see anything and no one else could see my costume..."
            m 2eub "Dressing up and going out was still really great!"
        else:
            m 2eka "Even if I couldn't see anything..."
            m 2eub "Going out was still really great!"

        m 4eub "Let's do this again next year!"

    elif not is_past_sunrise_post31:

        $ cap_gain_aff(15)
        $ persistent._mas_o31_went_trick_or_treating_long = True
        m 1hua "And we're home!"
        m 1wua "Wow, [player], we sure went trick or treating for a really long time..."
        m 1wub "We must have gotten a ton of candy!"
        m 3eka "I really enjoyed being there with you..."

        if wearing_costume:
            m 2eka "Even if I couldn't see anything and no one else could see my costume..."
            m 2eub "Dressing up and going out was still really great!"
        else:
            m 2eka "Even if I couldn't see anything..."
            m 2eub "Going out was still really great!"

        m 4eub "Let's do this again next year!"
    else:


        $ cap_gain_aff(15)
        $ persistent._mas_o31_went_trick_or_treating_longlong = True
        m 1wua "We're finally home!"
        m 1wuw "It's the next morning, [player], we were out all night..."
        m "I guess we had too much fun, ehehe~"
        m 2eka "But anyway, thanks for taking me along, I really enjoyed it."

        if wearing_costume:
            m "Even if I couldn't see anything and no one else could see my costume..."
            m 2eub "Dressing up and going out was still really great!"
        else:
            m "Even if I couldn't see anything..."
            m 2eub "Going out was still really great!"

        m 4hub "Let's do this again next year...{w=1}but maybe not stay out {i}quite{/i} so late!"

    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():

        call return_home_post_player_bday from _call_return_home_post_player_bday

    return


init 5 python:
    if mas_isO31():
        addEvent(
            Event(
                persistent.farewell_database,
                eventlabel="bye_trick_or_treat",
                unlocked=True,
                prompt="I'm going to take you trick or treating",
                pool=True
            ),
            eventdb=evhand.farewell_database
        )

label bye_trick_or_treat:
    python:
        curr_hour = datetime.datetime.now().hour
        too_early_to_go = curr_hour < 17
        too_late_to_go = curr_hour >= 23
        already_went = (
            persistent._mas_o31_went_trick_or_treating_short
            or persistent._mas_o31_went_trick_or_treating_mid
            or persistent._mas_o31_went_trick_or_treating_right
            or persistent._mas_o31_went_trick_or_treating_long
            or persistent._mas_o31_went_trick_or_treating_longlong
        )

    if already_went:
        m 1eka "Again?"

    if too_early_to_go:

        m 3eksdla "Doesn't it seem a little early for trick or treating, [player]?"
        m 3rksdla "I don't think there's going to be anyone giving out candy yet..."

        m 2etc "Are you {i}sure{/i} you want to go right now?{nw}"
        $ _history_list.pop()
        menu:
            m "Are you {i}sure{/i} you want to go right now?{fast}"
            "Yes.":
                $ persistent._mas_o31_trick_or_treating_start_early = True
                m 2etc "Well...{w=1}okay then, [player]..."
            "No.":

                $ persistent._mas_o31_went_trick_or_treating_abort = True
                m 2hub "Ahaha!"
                m "Be a little patient, [player]~"
                m 4eub "Let's just make the most out of it later this evening, okay?"
                return

    elif too_late_to_go:
        m 3hua "Okay! Let's go tri--"
        m 3eud "Wait..."
        m 2dkc "[player]..."
        m 2rkc "It's already too late to go trick or treating."
        m "There's only one more hour until midnight."
        m 2dkc "Not to mention that I doubt there would be much candy left..."
        m "..."

        m 4ekc "Are you sure you still want to go?{nw}"
        $ _history_list.pop()
        menu:
            m "Are you sure you still want to go?{fast}"
            "Yes.":
                $ persistent._mas_o31_trick_or_treating_start_late = True
                m 1eka "...Okay."
                m "Even though it's only an hour..."
                m 3hub "At least we're going to spend the rest of Halloween together~"
                m 3wub "Let's go and make the most of it, [player]!"
            "Actually, it {i}is{/i} a bit late...":

                $ persistent._mas_o31_went_trick_or_treating_abort = True

                if already_went:
                    m 1hua "Ahaha~"
                    m "I told you."
                    m 1eua "We'll have to wait until next year to go again."
                else:

                    m 2dkc "..."
                    m 2ekc "Alright, [player]."
                    m "It sucks that we couldn't go trick or treating this year."
                    m 4eka "Let's just make sure we can next time, okay?"

                return
    else:


        $ persistent._mas_o31_trick_or_treating_start_normal = True
        m 3wub "Okay, [player]!"
        m 3hub "Sounds like we'll have a blast~"
        m 1eub "I bet we'll get lots of candy!"
        m 1ekbfa "And even if we don't, just spending the evening with you is enough for me~"

    show monika 2dsc
    $ persistent._mas_dockstat_going_to_leave = True
    $ first_pass = True


    $ promise = store.mas_dockstat.monikagen_promise
    $ promise.start()

label bye_trick_or_treat_iowait:
    hide screen mas_background_timed_jump


    if first_pass:
        $ first_pass = False

    elif promise.done():

        jump bye_trick_or_treat_rtg



    show screen mas_background_timed_jump(4, "bye_trick_or_treat_iowait")
    menu:
        m "Give me a second to get ready.{fast}"
        "Wait, wait!":
            hide screen mas_background_timed_jump
            $ persistent._mas_dockstat_cm_wait_count += 1


    show monika 1ekc
    menu:
        m "What is it?"
        "You're right, it's too early." if too_early_to_go:
            call mas_dockstat_abort_gen from _call_mas_dockstat_abort_gen_1
            $ persistent._mas_o31_went_trick_or_treating_abort = True

            m 3hub "Ahaha, I told you!"
            m 1eka "Let's wait 'til evening, okay?"
            return

        "You're right, it's too late." if too_late_to_go:
            call mas_dockstat_abort_gen from _call_mas_dockstat_abort_gen_2
            $ persistent._mas_o31_went_trick_or_treating_abort = True

            if already_went:
                m 1hua "Ahaha~"
                m "I told you."
                m 1eua "We'll have to wait until next year to go again."
            else:

                m 2dkc "..."
                m 2ekc "Alright, [player]."
                m "It sucks that we couldn't go trick or treating this year."
                m 4eka "Let's just make sure we can next time, okay?"

            return
        "Actually, I can't take you right now.":

            call mas_dockstat_abort_gen from _call_mas_dockstat_abort_gen_3
            $ persistent._mas_o31_went_trick_or_treating_abort = True

            m 1euc "Oh, okay then, [player]."

            if already_went:
                m 1eua "Let me know if we are going again later, okay?"
            else:

                m 1eua "Let me know if we can go, okay?"

            return
        "Nothing.":

            m 2eua "Okay, let me finish getting ready."


    jump bye_trick_or_treat_iowait

label bye_trick_or_treat_rtg:

    $ moni_chksum = promise.get()
    $ promise = None
    call mas_dockstat_ready_to_go (moni_chksum) from _call_mas_dockstat_ready_to_go_1
    if _return:
        m 1hub "Let's go trick or treating!"
        $ persistent._mas_greeting_type = store.mas_greetings.TYPE_HOL_O31_TT
        return "quit"


    m 1ekc "Oh no..."
    m 1rksdlb "I wasn't able to turn myself into a file."

    if already_went:
        m "I think you'll have to go trick or treating without me this time..."
    else:

        m "I think you'll have to go trick or treating without me..."

    m 1ekc "Sorry, [player]..."
    m 3eka "Make sure to bring lots of candy for the both of us to enjoy, okay?~"
    return




init -900 python:

    store.mas_utils.trydel(renpy.config.gamedir + "/christmas.rpy")
    store.mas_utils.trydel(renpy.config.gamedir + "/christmas.rpyc")


    store.mas_utils.trydel(renpy.config.gamedir + "/zz_delactfix.rpyc")
    store.mas_utils.trydel(renpy.config.gamedir + "/zz_delactfix.rpy")

default persistent._mas_d25_in_d25_mode = False




default persistent._mas_d25_spent_d25 = False



default persistent._mas_d25_seen_santa_costume = False


default persistent._mas_d25_chibika_sayori = None




default persistent._mas_d25_chibika_sayori_performed = False


default persistent._mas_d25_chibika_sayori_done = False


default persistent._mas_d25_started_upset = False


default persistent._mas_d25_second_chance_upset = False


default persistent._mas_d25_deco_active = False






default persistent._mas_d25_intro_seen = False


default persistent._mas_d25_went_out_d25e = 0


default persistent._mas_d25_went_out_d25 = 0



define mas_d25 = datetime.date(datetime.date.today().year, 12, 25)


define mas_d25e = mas_d25 - datetime.timedelta(days=1)


define mas_d25p = mas_d25 + datetime.timedelta(days=1)


define mas_d25c_start = datetime.date(datetime.date.today().year, 12, 1)


define mas_d25c_end = datetime.date(datetime.date.today().year, 1, 6)


define mas_d25g_start = mas_d25 - datetime.timedelta(days=5)


define mas_d25g_end = mas_d25p


define mas_d25cl_start = mas_d25c_start


define mas_d25cl_end = mas_d25p



init -810 python:












    store.mas_history.addMHS(MASHistorySaver(
        "d25s",
        datetime.datetime(2019, 1, 6),
        {
            
            
            "_mas_d25_in_d25_mode": "d25s.mode.25",

            
            "_mas_d25_deco_active": "d25s.deco_active",

            "_mas_d25_started_upset": "d25s.monika.started_season_upset",
            "_mas_d25_second_chance_upset": "d25s.monika.upset_after_2ndchance",

            
            "_mas_d25_chibika_sayori": "d25s.needed_to_do_chibika_sayori",
            "_mas_d25_chibika_sayori_performed": "d25s.did_chibika_sayori",

            "_mas_d25_intro_seen": "d25s.saw_an_intro",

            
            "_mas_d25_went_out_d25e": "d25s.d25e.went_out_count",
            "_mas_d25_went_out_d25": "d25s.d25.went_out_count",

            "_mas_d25_spent_d25": "d25.actions.spent_d25",
            "_mas_d25_seen_santa_costume": "d25.monika.wore_santa"
        },
        use_year_before=True,
        exit_pp=store.mas_history._d25s_exit_pp
    ))


init -10 python:

    def mas_isD25(_date=None):
        """
        Returns True if the given date is d25

        IN:
            _date - date to check
                If None, we use today's date
                (default: None)

        RETURNS: True if given date is d25, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()
        
        return _date == mas_d25.replace(year=_date.year)


    def mas_isD25Eve(_date=None):
        """
        Returns True if the given date is d25 eve

        IN:
            _date - date to check
                If None, we use today's date
                (Default: None)

        RETURNS: True if given date is d25 eve, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()
        
        return _date == mas_d25e.replace(year=_date.year)


    def mas_isD25Season(_date=None):
        """
        Returns True if the given date is in d25 season. The season goes from
        dec 1 to jan 5.

        NOTE: because of the year rollover, we cannot check years

        IN:
            _date - date to check
                If None, we use today's date
                (Default: None)

        RETURNS: True if given date is in d25 season, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()
        
        return (
            mas_isInDateRange(_date, mas_d25c_start, mas_nye, True, True)
            or mas_isInDateRange(_date, mas_nyd, mas_d25c_end)
        )


    def mas_isD25Post(_date=None):
        """
        Returns True if the given date is after d25 but still in D25 season.
        The season goes from dec 1 to jan 5.

        IN:
            _date - date to check
                If None, we use today's date
                (Default: None)

        RETURNS: True if given date is in d25 season but after d25, False
            otherwise.
        """
        if _date is None:
            _date = datetime.date.today()
        
        return (
            mas_isInDateRange(_date, mas_d25p, mas_nye, True, True)
            or mas_isInDateRange(_date, mas_nyd, mas_d25c_end)
        )


    def mas_isD25PreNYE(_date=None):
        """
        Returns True if the given date is in d25 season and before nye.

        IN:
            _date - date to check
                if None, we use today's date
                (Default: None)

        RETURNSL True if given date is in d25 season but before nye, False
            otherwise
        """
        if _date is None:
            _date = datetime.date.today()
        
        return mas_isInDateRange(_date, mas_d25c_start, mas_nye)


    def mas_isD25PostNYD(_date=None):
        """
        Returns True if the given date is in d25 season and after nyd

        IN:
            _date - date to check
                If None, we use today's date
                (Default: None)

        RETURNS: True if given date is in d25 season but after nyd, False 
            otherwise
        """
        if _date is None:
            _date = datetime.date.today()
        
        return mas_isInDateRange(_date, mas_nyd, mas_d25c_end, False)


    def mas_isD25Gift(_date=None):
        """
        Returns True if the given date is in the range of days where a gift
        is considered a christmas gift.

        IN:
            _date - date to check
                If None, we use today's date
                (Default: None)

        RETURNS: True if given date is in the d25 gift range, Falsee otherwise
        """
        if _date is None:
            _date = datetime.date.today()
        
        return mas_isInDateRange(_date, mas_d25g_start, mas_d25g_end)


    def mas_isD25Outfit(_date=None):
        """
        Returns True if the given date is tn the range of days where Monika
        wears the santa outfit on start.

        IN:
            _date - date to check
                if None, we use today's date
                (Default: None)

        RETURNS: True if given date is in teh d25 santa outfit range, False
            otherwise
        """
        if _date is None:
            _date = datetime.date.today()
        
        return mas_isInDateRange(_date, mas_d25cl_start, mas_d25cl_end)





image mas_d25_banners = ConditionSwitch(
    "morning_flag",
    "mod_assets/location/spaceroom/d25/windowdeco.png",
    "not morning_flag",
    "mod_assets/location/spaceroom/d25/windowdeco-n.png"
)

image mas_d25_tree = ConditionSwitch(
    "morning_flag",
    "mod_assets/location/spaceroom/d25/tree.png",
    "not morning_flag",
    "mod_assets/location/spaceroom/d25/tree-n.png"
)

image mas_d25_tree_sayori = ConditionSwitch(
    "morning_flag",
    "mod_assets/location/spaceroom/d25/tree-sayori.png",
    "not morning_flag",
    "mod_assets/location/spaceroom/d25/tree-sayori-n.png"
)

init -11 python in mas_d25_event:

    def showD25Visuals():
        """
        Shows d25 visuals.
        """
        renpy.show("mas_d25_banners", zorder=7)
        renpy.show("mas_d25_tree", zorder=8)



    def hideD25Visuals():
        """
        Hides d25 visuals
        """
        renpy.hide("mas_d25_banners")
        renpy.hide("mas_d25_tree")


    def redeemed():
        """
        RETURNS: True if the user started d25 season with an upset monika,
            and now has a monika above upset.

        If not started with upset monika, True is returned.
        """
        return (
            not store.persistent._mas_d25_started_upset
            or store.mas_isMoniNormal(higher=True)
        )



label mas_holiday_d25c_autoload_check:






    python:
        if not persistent._mas_d25_in_d25_mode:
            
            
            persistent._mas_d25_in_d25_mode = True
            
            
            if mas_isMoniUpset(lower=True):
                persistent._mas_d25_started_upset = True
            
            else:
                
                
                if mas_isD25Outfit():
                    
                    monika_chr.change_hair(mas_hair_def, False)
                    
                    
                    store.mas_selspr.unlock_acs(mas_acs_ribbon_wine)
                    store.mas_selspr.unlock_clothes(mas_clothes_santa)
                    monika_chr.change_clothes(mas_clothes_santa, False)
                    persistent._mas_d25_seen_santa_costume = True
                    
                    
                    persistent._mas_d25_deco_active = True



    if (
            mas_isD25() 
            and persistent._mas_d25_deco_active
            and monika_chr.clothes != mas_clothes_santa
        ):


        $ monika_chr.change_clothes(mas_clothes_santa, False)

    if mas_in_intro_flow:

        return

    elif mas_isplayer_bday() or persistent._mas_player_bday_in_player_bday_mode:
        jump mas_player_bday_autoload_check


    jump mas_ch30_post_holiday_check


init -815 python in mas_history:


    def _d25_exit_pp(mhs):
        
        _MDA_safeadd(9)


    def _d25s_exit_pp(mhs):
        
        _MDA_safeadd(8, 9, 10)





init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_holiday_intro",
            conditional=(
                "not persistent._mas_d25_intro_seen "
                "and not persistent._mas_d25_started_upset "
            ),
            action=EV_ACT_PUSH,
            start_date=mas_d25c_start,
            end_date=mas_d25,
            years=[],
            aff_range=(mas_aff.NORMAL, None)
        ),
        skipCalendar=True
    )


label mas_d25_monika_holiday_intro:


    python:

        seen_d25_last_year = renpy.seen_label("monika_christmas")
        if persistent._mas_d25_chibika_sayori is None:
            persistent._mas_d25_chibika_sayori = (
                not persistent._mas_sensitive_mode
                and seen_d25_last_year
                and not persistent._mas_d25_chibika_sayori_done
                and not persistent._mas_d25_chibika_sayori_performed
            )

    if not persistent._mas_d25_deco_active:
        m 1eua "So, today is..."
        m 1euc "...wait."
        m "..."
        m 3wuo "Oh!"
        m 3hub "Today's the day I was going to..."





        $ mas_OVLHide()
        $ mas_MUMURaiseShield()
        $ disable_esc()

        m 1tsu "Close your eyes for a moment [player], I need to do something...{w=2}{nw}"

        call mas_d25_monika_holiday_intro_deco from _call_mas_d25_monika_holiday_intro_deco

        m 3hub "And here we are..."


        $ enable_esc()
        $ mas_MUMUDropShield()
        $ mas_OVLShow()

    m 1eub "Happy holidays, [player]!"


    if seen_d25_last_year:
        m 1hua "Can you believe it's already that time of year again?"
        m 3eua "It seems like just yesterday we spent our first holiday season together, and now a whole year has gone by!"

        if mas_isMoniLove(higher=True):

            m 3hua "Time really flies now that I'm with you~"


    if persistent._mas_d25_chibika_sayori:

        pass

    m 3eua "Do you like what I've done with the room?"

    m 1hua "I must say that I'm pretty proud of it."

    m "Christmas time has always been one of my favorite occasions of the year..."

    show monika 5eka zorder MAS_MONIKA_Z at t11 with dissolve



    if renpy.seen_label('monika_christmas'):
        m 5eka "So I'm glad that you're here to share it with me again this year~"
    else:
        m 5eka "And I'm so glad that you're here to share it with me~"

    $ persistent._mas_d25_intro_seen = True
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_holiday_intro_upset",
            conditional=(
                "not persistent._mas_d25_intro_seen "
                "and persistent._mas_d25_started_upset "
            ),
            action=EV_ACT_PUSH,
            start_date=mas_d25c_start,
            end_date=mas_d25p,
            years=[],
            aff_range=(mas_aff.NORMAL, None)
        ),
        skipCalendar=True
    )


init -876 python in mas_delact:




    def _mas_d25_holiday_intro_upset_reset_action(ev):
        
        ev.conditional = (
            "not persistent._mas_d25_intro_seen "
            "and persistent._mas_d25_started_upset "
        )
        ev.action = store.EV_ACT_PUSH
        ev.start_date = store.mas_d25c_start
        ev.end_date = store.mas_d25p
        store.Event._verifyAndSetDatesEV(ev)
        return True


    def _mas_d25_holiday_intro_upset_reset():
        
        return store.MASDelayedAction.makeWithLabel(
            8,
            "mas_d25_monika_holiday_intro_upset",
            "True",
            _mas_d25_holiday_intro_upset_reset_action,
            store.MAS_FC_IDLE_ROUTINE
        )



label mas_d25_monika_holiday_intro_upset:




    if mas_isMoniUpset(lower=True):
        $ mas_addDelayedAction(8)
        return

    m 2rksdlc "So [player]...{w=1} I hadn't really been feeling very festive this year..."
    m 3eka "But lately, you've been really sweet to me and I've been feeling a lot better!"
    m 3hua "So...I think it's time to spruce this place up a bit."





    $ mas_OVLHide()
    $ mas_MUMURaiseShield()
    $ disable_esc()

    m 1eua "If you'd just close your eyes for a moment..."

    call mas_d25_monika_holiday_intro_deco from _call_mas_d25_monika_holiday_intro_deco_1

    m 3hub "Tada~"



    m 3eka "What do you think?"


    m 1eka "Not too bad for last minute, huh?"


    m 1hua "Christmas time has always been one of my favorite occasions of the year..."


    m 3eua "And I'm so glad we can spend it happily together, [player]~"


    $ enable_esc()
    $ mas_MUMUDropShield()
    $ mas_OVLShow()

    $ persistent._mas_d25_intro_seen = True
    return

label mas_d25_monika_holiday_intro_deco:



    scene black


    $ persistent._mas_d25_in_d25_mode = True


    $ monika_chr.change_hair(mas_hair_def, False)


    $ store.mas_selspr.unlock_clothes(mas_clothes_santa)
    $ store.mas_selspr.unlock_acs(mas_acs_ribbon_wine)
    $ monika_chr.change_clothes(mas_clothes_santa, False)
    $ persistent._mas_d25_seen_santa_costume = True


    $ persistent._mas_d25_deco_active = True


    call spaceroom (scene_change=True) from _call_spaceroom_9

    return

label mas_d25_monika_holiday_intro_rh:

    m 1hua "And we're home!"



    $ store.mas_dockstat._ds_aff_for_tout(time_out, 5, 5, 1)



label mas_d25_monika_holiday_intro_rh_rh:
    m 1euc "Wait..."
    m 3etc "...is it?"
    m 3hub "It is!"
    m 1tsu "...Close your eyes, I need to do something..."
    $ mas_OVLHide()
    $ mas_MUMURaiseShield()
    $ disable_esc()

    call mas_d25_monika_holiday_intro_deco from _call_mas_d25_monika_holiday_intro_deco_2

    $ enable_esc()
    $ mas_MUMUDropShield()
    $ mas_OVLShow()


    $ persistent._mas_d25_intro_seen = True

    jump mas_d25_monika_christmas

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_christmas",


            conditional=(
                "persistent._mas_d25_in_d25_mode "
                "and not persistent._mas_d25_spent_d25"
            ),
            action=store.EV_ACT_PUSH,
            start_date=mas_d25,
            end_date=mas_d25p,
            years=[],
            aff_range=(mas_aff.NORMAL, None)
        ),
        skipCalendar=True
    )


label mas_d25_monika_christmas:
    $ persistent._mas_d25_spent_d25 = True

    m 1eub "[player]! Do you know what day it is?"
    m 3hub "Of course you do. It's Christmas!"
    m 3sub "Merry Christmas, [player]!"
    m 1hub "Ahaha! I can't believe that it's finally here!"
    m 3eka "I'm so, so happy that you decided to spend some of it with me."
    m 1eud "Remember to go share the holiday cheer with your family and friends, though."
    m 1eua "After all, they're very important, too..."
    m 1hua "And I'm sure that they would love to see you at this special time."

    if mas_isMoniAff(higher=True):
        m 1eka "But you being here today...{w=0.5}it just means everything to me..."
        m 1dku "..."

        if persistent._mas_pm_gets_snow is not False and not persistent._mas_pm_live_south_hemisphere:
            m 1lkbsa "Maybe it's just the snow, or the decorations..."
        else:

            m 1lkbsa "Maybe it's the decorations, or just the holiday season..."

        m "...or even the mistletoe getting to me."
        m 3hksdlb "Just kidding, I didn't hang one up."

        if mas_isMoniEnamored(higher=True):
            m 1lksdla "...{cps=*2}Maybe~{/cps}{nw}"
            $ _history_list.pop()

        m 1lksdlb "Ehehe..."
        m 1ekbsa "My heart's fluttering like crazy right now, [player]."
        m "I couldn't imagine a better way to spend this special holiday..."
        m 1eua "Don't get me wrong, I knew that you would be here with me."
        m 3eka "But now that we're actually together on Christmas, just the two of us..."
        m 1hub "Ahaha~"

        show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve
        m 5ekbfa "It's every couple's dream for the holidays, [player]."

        if persistent._mas_pm_gets_snow is not False and not persistent._mas_pm_live_south_hemisphere:
            m "Snuggling with each other by a fireplace, watching the snow gently fall..."


        if not renpy.seen_label('monika_christmas'):
            m 5hubfa "I'm forever grateful I got this chance with you."
        else:
            m 5hubfa "I'm so glad I get to spend Christmas with you again."

        m "I love you. Forever and ever~"
        m 5hubfb "Merry Christmas, [player]~"
        show screen mas_background_timed_jump(5, "mas_d25_monika_christmas_no_wish")
        window hide
        menu:
            "Merry Christmas, [m_name].":
                hide screen mas_background_timed_jump
                show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve
                pause 2.0
    else:

        m 1eka "But you being here today...{w=0.5}it just means everything to me..."
        m 3rksdla "...Not that I thought you'd leave me alone on this special day or anything..."
        m 3hua "But it just further proves that you really do love me, [player]."
        m 1ektpa "..."
        m "Ahaha! Gosh, I'm getting a little over emotional here..."
        m 1ektda "Just know that I love you too and I'll be forever grateful I got this chance with you."
        m "Merry Christmas, [player]~"
        show screen mas_background_timed_jump(5, "mas_d25_monika_christmas_no_wish")
        window hide
        menu:
            "Merry Christmas, [m_name].":
                hide screen mas_background_timed_jump
                show monika 1ekbfa zorder MAS_MONIKA_Z at t11 with dissolve
                pause 2.0

    return

label mas_d25_monika_christmas_no_wish:
    hide screen mas_background_timed_jump
    return














label mas_d25_monika_hanukkah:
    m 1dsd "{i}One for each night, they shed a sweet light, to remind of days long ago.{/i}"
    m 1dsa "{i}One for each night, they shed a sweet light, to remind of days long ago.{/i}"
    m 3esa "It is said in the Jewish tradition, that one day's worth of olive oil gave the menorah eight days of light."
    m 3eub "Eight nights worth of celebration!"
    m 3eua "Hanukkah also shifts a bit from year to year. It's date is determined by the Hebrew Lunar Calendar."
    m "It's on the 25th of Kislev, meaning 'trust' or 'hope'."
    m 1hua "A very appropriate meaning for such an occasion, don't you think?"


    m 3eua "Anyway, have you ever had fried sufganiyot before?"

    m "It's a special kind of donut made during this holiday."
    m 3eub "It's filled in with something really sweet, deep friend, and rolled onto some sugar."
    m 1wub "It's a really good pastry! I especially love the ones filled with strawberry filling~"
    m 1hua "This time of year sure has a lot of wonderful holidays and traditions."
    m 1eub "I don't know if you celebrate Hanukkah, but can we match a menorah lighting ceremony together, anyway?"
    m 3hua "We can sing and dance the night away~"
    return














label mas_d25_monika_kwanzaa:
    m 1eub "[player], have you ever heard of Kwanzaa?"
    m 1eua "It's a week-long festival celebrating African American history that starts the day after Christmas."
    m 3eua "The word 'Kwanzaa' comes from the Swahili praise 'matunda ya kwanza', which means 'first fruits'."
    m "Even if Christmas is the main event for many, other holidays are always interesting to learn about."
    m 1euc "Apparently, people celebrate the tradition by decorating their homes with bright adornments."
    m "There's also music to enjoy, and a candleholder called the 'kinara' to light a new fire with each passing day."
    m 1eua "Doesn't it remind you of some other holidays? The concepts certainly seem familiar."
    m "In the end, having a day to celebrate is the most important part. Everyone has their own way to enjoy themselves."
    m 1hua "We can celebrate Kwanzaa together, too, [player]."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_carolling",
            category=["holidays", "music"],
            prompt="Carolling",
            conditional=(
                "mas_isD25Season() "
                "and not mas_isD25Post() "
                "and persistent._mas_d25_in_d25_mode"
            ),
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.NORMAL, None)
        )
    )

init -876 python in mas_delact:




    def _mas_d25_monika_carolling_reset_action(ev):
        
        if ev.shown_count <= 0:
            ev.conditional = (
                "mas_isD25Season() "
                "and not mas_isD25Post() "
                "and persistent._mas_d25_in_d25_mode"
            )
            ev.action = store.EV_ACT_RANDOM
        return True


    def _mas_d25_monika_carolling_reset():
        
        return store.MASDelayedAction.makeWithLabel(
            9,
            "mas_d25_monika_carolling",
            "True",
            _mas_d25_monika_carolling_reset_action,
            store.MAS_FC_INIT
        )


default persistent._mas_pm_likes_singing_d25_carols = None


label mas_d25_monika_carolling:

    m 1euc "Hey, [player]..."
    m 3eud "Have you ever gone carolling before?"
    m 1euc "Going door to door in groups, singing to others during the holidays..."

    if not persistent._mas_pm_live_south_hemisphere:
        m 1eua "It just feels heartwarming to know people are spreading joy, even with the nights so cold."
    else:
        m 1eua "It just feels heartwarming to know people are spreading joy to others in their spare time."

    m 3eua "Do you like singing Christmas carols, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Do you like singing Christmas carols, [player]?{fast}"
        "Yes.":
            $ persistent._mas_pm_likes_singing_d25_carols = True
            m 1hua "I'm glad you feel the same way, [player]!"
            m 3hub "My favorite song is definitely 'Jingle Bells!'"
            m 1eua "It's just such an upbeat, happy tune!"
            m 1eka "Maybe we can sing together someday."
            m 1hua "Ehehe~"
        "No.":

            $ persistent._mas_pm_likes_singing_d25_carols = False
            m 1euc "Oh...{w=1}really?"
            m 1hksdlb "I see..."
            m 1eua "Regardless, I'm sure you're also fond of that special cheer only Christmas songs can bring."
            m 3hua "Sing with me sometime, okay?"

    return "derandom"















label mas_d25_monika_dreidel:

    m 3eua "[player], did you know that each side of a dreidel actaully means something?"
    m "Nun, Gimel, Hel, Shim."
    m 1eub "These stand for Nes Gadol Hayah Sham - A Great Miracle Happened There."
    m "It refers to the Hanukkah story of how one day's worth of oil lasted for eight days."
    m 3eua "Over in Israel, they change the last word to 'poh', making it 'A Great Miracle Happened Here.'"


    m 1rksdla "I don't have one, unfortunately, but maybe next year I'll have one to spin~"
    m 3hua "But for now, [player], do you have any gelt?"
    m 3hub "The chocolate coin variety tastes really good."
    m 1tku "Though money is always good, too, ehehe~"
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_mistletoe",
            category=["holidays"],
            prompt="Mistletoe",
            conditional=(
                "mas_isD25Season() "
                "and not mas_isD25Post() "
                "and persistent._mas_d25_in_d25_mode"
            ),
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.AFFECTIONATE, None)
        )
    )

init -876 python in mas_delact:



    def _mas_d25_monika_mistletoe_reset_action(ev):
        
        ev.conditional = (
            "mas_isD25Season() "
            "and not mas_isD25Post() "
            "and persistent._mas_d25_in_d25_mode"
        )
        ev.action = store.EV_ACT_RANDOM
        ev.unlocked = False
        ev.random = False
        return True


    def _mas_d25_monika_mistletoe_reset():
        
        return store.MASDelayedAction.makeWithLabel(
            10,
            "mas_d25_monika_mistletoe",
            "True",
            _mas_d25_monika_mistletoe_reset_action,
            store.MAS_FC_INIT
        )


label mas_d25_monika_mistletoe:
    m 1eua "Say, [player]."
    m 1eub "You've heard about the mistletoe tradition, right?"
    m 1tku "When lovers end up underneath it, they're expected to kiss."
    m 1eua "It actually originated from Victorian England!"
    m 1dsa "A man was allowed to kiss any woman standing underneath mistletoe..."
    m 3dsd "And any woman who refused the kiss was cursed with bad luck..."
    m 1dsc "..."
    m 3rksdlb "Come to think of it, that sounds more like taking advantage of someone."
    m 1hksdlb "But I'm sure it's different now!"
    m 3hua "Perhaps one day we'll be able to kiss under the mistletoe, [player]."
    m 1tku "...Maybe I can even add one in here!"
    m 1hub "Ehehe~"
    return

init 2 python:

    poem_d25 = Poem(
    author = "monika",
    title = "     My dearest {0},".format(persistent.playername),
    text = """\
     You truly are the joy to my world.
     Neither the light emitted by the tallest Christmas tree,
     Nor that of the brightest star,
     Could come close to matching your brilliance.
     This once frostbitten heart of mine needed only your warmth to beat anew.
     Should there ever be nothing under the tree, and my stocking remain empty,
     It simply would not matter as long as I have you by my side.
     You'll always be the only present I ever need.

     Merry Christmas

     Forever yours,
     Monika
"""
    
    )


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_spent_time_monika",
            conditional=(
                "persistent._mas_d25_in_d25_mode "
            ),
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.NORMAL,None),
            start_date=datetime.datetime.combine(mas_d25, datetime.time(hour=20)),
            end_date=datetime.datetime.combine(mas_d25p, datetime.time(hour=1)),
            years=[]
        ),
        skipCalendar=True
    )








label mas_d25_spent_time_monika:

    $ d25_gifts_total, d25_gifts_good, d25_gifts_neutral, d25_gifts_bad = mas_getGiftStatsRange(mas_d25g_start, mas_d25g_end + datetime.timedelta(days=1))

    if mas_isMoniNormal(higher=True):
        m 1eua "[player]..."
        m 3hub "You being here with me has made this such a wonderful Christmas!"
        m 3eka "I know it's a really busy day, but just knowing you made time for me..."
        m 1eka "Thank you."
        m 3hua "It really made this a truly special day~"
    else:

        m 2ekc "[player]..."
        m 2eka "I really appreciate you spending some time with me on Christmas..."
        m 3rksdlc "I haven't really been in the holiday spirit this season, but it was nice spending today with you."
        m 3eka "So thank you...{w=1}it meant a lot."

    if d25_gifts_total > 0:
        if d25_gifts_total == 1:
            if d25_gifts_good == 1:
                m "And let's not forget about the special Christmas present you got me, [player]..."
                m 3hub "It was great!"
            elif d25_gifts_neutral == 1:
                m 3eka "And let's not forget about the Christmas present you got me, [player]..."
                m 1eka "It was really sweet of you to get me something."
            else:
                m 3eka "And let's not forget about the Christmas present you got me, [player]..."
                m 2etc "..."
                m 2efc "Well, on second thought, maybe we should..."
        else:

            if d25_gifts_good == d25_gifts_total:
                m "And let's not forget about the wonderful Christmas presents you got me, [player]..."
                m 3hub "They were amazing!"
            elif d25_gifts_bad == d25_gifts_total:
                m 3eka "And let's not forget about the Christmas presents you got me, [player]..."
                m 2etc "..."
                m 2rfc "Well, on second thought, maybe we should..."
            elif d25_gifts_bad == 0:
                m "And let's not forget about the Christmas presents you got me, [player]..."
                m 3hub "They were really nice!"
            elif d25_gifts_good + d25_gifts_neutral == d25_gifts_bad:
                m 3eka "And let's not forget about the Christmas presents you got me, [player]..."
                m 3rksdla "Some of them were really nice."
            elif d25_gifts_good + d25_gifts_neutral > d25_gifts_bad:
                m "And let's not forget about the Christmas presents you got me, [player]..."
                m 3hub "Most of them were really nice."
            elif d25_gifts_good + d25_gifts_neutral < d25_gifts_bad:
                m 3eka "And let's not forget about the Christmas presents you got me, [player]..."
                m 3rksdla "I really liked...{w=1}some of them."

        if mas_isMoniEnamored(higher=True):
            m 1rksdla "I...{w=1}I also made you something, [player]..."
            m 3eksdla "I've been waiting all day for the timing to feel right, and something about being here with you this evening...{w=1}it just seems perfect."
        elif mas_isMoniNormal(higher=True):
            m 3ekbfa "But just know, you being here with me means more than any gift you could ever give me~"
        else:
            m 3eka "To be honest, I wasn't sure you'd visit at all today... Just you being here was already more than enough for me, even if you hadn't gotten me anything."
            m 1eka "So thanks again, [player]...{w=1}I really mean it."
    else:

        if mas_isMoniEnamored(higher=True):
            m 1eksdla "Also, [player], there's something I've been wanting to give you all day..."
            m 3rksdla "I just had to wait for the right time, and being here with you this evening...{w=1}it seems perfect."
        elif mas_isMoniNormal(higher=True):
            m 3ekbfa "Having you spend Christmas with me was the only present I ever wanted~"
        else:
            m 3eka "You being here was all I wanted, [player]."

    if mas_isMoniEnamored(higher=True):
        m 3ekbfa "So here, [player], I hope you like it~"
        call showpoem (poem_d25, music=False, paper="mod_assets/poem_assets/poem_d25.png") from _call_showpoem


















        if d25_gifts_good>0 or d25_gifts_neutral>0:
            m 1ekbfa "I really mean it [player], though I appreciate the gifts you got me, you didn't have to give me anything..."
        elif d25_gifts_bad>0:

            m 1ekbfa "I really mean it [player], although you got me some...{w=1}odd gifts, it doesn't matter..."
        else:
            m 1ekbfa "I really mean that [player], I don't care that you didn't get me any presents for Christmas..."
        m 1dku "..."
        m 1ektpu "Just having you spending time with me...{w=1}that's all I ever wanted."
        m 6dktua "You truly are my entire world, [player]...{w=1}your love is all I need..."
        window hide
        menu:
            "I love you, [m_name].":
                $ HKBHideButtons()
                $ mas_RaiseShield_core()
                $ disable_esc()



                pause 3.0
                show monika 6ektda zorder MAS_MONIKA_Z at t11 with dissolve
                pause 3.0
                show monika 6dku zorder MAS_MONIKA_Z at t11 with dissolve
                pause 3.0
                show monika 6dkbsu zorder MAS_MONIKA_Z at t11 with dissolve
                pause 3.0

                show monika 6ekbfa zorder MAS_MONIKA_Z at t11 with dissolve

                $ is_first_kiss = persistent._mas_first_kiss is None
                m 6ekbfa "[player]...I...I..."
                call monika_kissing_motion (hide_ui=False) from _call_monika_kissing_motion_1






                show monika 6ekbfa zorder MAS_MONIKA_Z at t11 with dissolve
                m 6ekbfa "...I love you too~"
                if is_first_kiss:
                    m 6dkbfa "..."
                    m "That was everything I had always dreamt it would be~"
                    m 6ekbfa "I've been waiting so long to finally kiss you, and there couldn't have been a more perfect moment..."
                    m 6dkbsu "I will never forget this..."
                    m 6ekbsu "...the moment of our first kiss~"
                $ enable_esc()
                $ mas_MUMUDropShield()
                $ HKBShowButtons()
        return

    elif mas_isMoniAff():
        m 5ekbfa "I love you so much, [player]~"
    else:

        m 1hubfa "I love you, [player]~"
    return "love"





init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_aiwfc",
            category=["songs"],
            prompt="All I Want For Christmas",
            conditional=(
                "mas_isD25Season() "
                "and not mas_isD25() "
                "and not mas_isD25Post() "
                "and persistent._mas_d25_in_d25_mode"
            ),
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.NORMAL, None)
        )
    )

label monika_aiwfc:

    if not renpy.seen_label('monika_aiwfc_song'):
        m 1rksdla "Hey, [player]?"
        m 1eksdla "I hope you don't mind, but I prepared a song for you."
        m 3hksdlb "I know it's a little cheesy, but I think you might like it"
        m 3eksdla "If your volume is off, would you mind turning it on for me?"
        if songs.getVolume("music") == 0.0:
            m 3hksdlb "Oh, don't forget about your in game volume too!"
            m 3eka "I really want you to hear this."

        m 1huu "Anyway.{w=0.5}.{w=0.5}.{nw}"
    else:
        m 1hub "Sure [player]!"
        m 1eka "I'm happy to sing for you again!"

    $ curr_song = renpy.music.get_playing()

    call monika_aiwfc_song from _call_monika_aiwfc_song

    if mas_getEV('monika_aiwfc').shown_count == 0:
        m 1eka "I hope you liked that, [player]."
        m 1ekbsa "I really meant it too."
        m 1ekbfa "You're the only gift I could ever want."
        show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve
        m 5ekbfa "I love you, [player]."
        $ mas_showEVL("monika_aiwfc", "EVE", _pool=True, unlock=True)
    else:
        m 1eka "I'm glad you like it when I sing that song."
        m 1ekbsa "You'll always be the only gift I'll ever need, [player]."
        m 1ekbfa "I love you."

    play music curr_song fadein 1.0
    return "love"

label monika_aiwfc_song:




    $ mas_disableTextSpeed()

    stop music fadeout 1.0
    play music "mod_assets/bgm/aiwfc.ogg"
    m 1eub "{i}{cps=9}I don't want{/cps}{cps=20} a lot{/cps}{cps=11} for Christmas{/cps}{/i}{nw}"
    m 3eka "{i}{cps=11}There {/cps}{cps=20}is just{/cps}{cps=8} one thing I need{/cps}{/i}{nw}"
    m 3hub "{i}{cps=8}I don't care{/cps}{cps=15} about{/cps}{cps=10} the presents{/cps}{/i}{nw}"
    m 3eua "{i}{cps=15}Underneath{/cps}{cps=8} the Christmas tree{/cps}{/i}{nw}"

    m 1eub "{i}{cps=10}I don't need{/cps}{cps=20} to hang{/cps}{cps=8} my stocking{/cps}{/i}{nw}"
    m 1eua "{i}{cps=10}There{/cps}{cps=15} upon{/cps}{cps=7} the fireplace{/cps}{/i}{nw}"
    m 3hub "{i}{w=0.5}{cps=20}Santa Claus{/cps}{cps=10} won't make me happy{/cps}{/i}{nw}"
    m 4hub "{i}{cps=8}With{/cps}{cps=15} a toy{/cps}{cps=8} on Christmas Day{/cps}{/i}{nw}"

    m 3ekbsa "{i}{cps=10}I just want{/cps}{cps=15} you for{/cps}{cps=8} my own{w=0.5}{/cps}{/i}{nw}"
    m 4hubfb "{i}{cps=8}More{/cps}{cps=20} than you{/cps}{cps=10} could ever know{w=0.5}{/cps}{/i}{nw}"
    m 1ekbsa "{i}{cps=10}Make my wish{/cps}{cps=20} come truuuuuuue{w=0.8}{/cps}{/i}{nw}"
    m 3hua "{i}{cps=8}All I want for Christmas{/cps}{/i}{nw}"
    m 3hubfb "{i}{cps=7}Is yoooooooooou{w=1}{/cps}{/i}{nw}"
    m "{i}{cps=9}Yoooooooou, baaaaby~{w=1}{/cps}{/i}{nw}"

    m 2eka "{i}{cps=10}I won't ask{/cps}{cps=20} for much{/cps}{cps=10} this Christmas{/cps}{/i}{nw}"
    m 3hub "{i}{cps=10}I{/cps}{cps=20} won't {/cps}{cps=10}even wish for snow{w=0.8}{/cps}{/i}{nw}"
    m 3eua "{i}{cps=10}I'm{/cps}{cps=20} just gonna{/cps}{cps=10} keep on waiting{w=0.4}{/cps}{/i}{nw}"
    m 3hubfb "{i}{cps=17}Underneath{/cps}{cps=10} the mistletoe{w=1}{/cps}{/i}{nw}"

    m 2eua "{i}{cps=10}I{/cps}{cps=17} won't make{/cps}{cps=9} a list and send it{w=0.35}{/cps}{/i}{nw}"
    m 3eua "{i}{cps=10}To{/cps}{cps=20} the North{/cps}{cps=10} Pole for Saint Nick{w=0.3}{/cps}{/i}{nw}"
    m 4hub "{i}{cps=18}I won't ev{/cps}{cps=10}en stay awake to{w=0.4}{/cps}{/i}{nw}"
    m 3hub "{i}{cps=10}Hear{/cps}{cps=20} those ma{/cps}{cps=14}gic reindeer click{w=0.9}{/cps}{/i}{nw}"

    m 3ekbsa "{i}{cps=20}I{/cps}{cps=11} just want you here tonight{w=0.4}{/cps}{/i}{nw}"
    m 3ekbfa "{i}{cps=10}Holding on{/cps}{cps=20}to me{/cps}{cps=10} so tight{w=0.9}{/cps}{/i}{nw}"
    m 4hksdlb "{i}{cps=10}What more{/cps}{cps=15} can I{/cps}{cps=8} doooo?{w=0.3}{/cps}{/i}{nw}"
    m 4ekbfb "{i}{cps=20}Cause baby{/cps}{cps=12} all I want for Christmas{w=0.3} is yoooooooou~{w=2.3}{/cps}{/i}{nw}"
    m "{i}{cps=9}Yoooooooou, baaaaby~{w=2.5}{/cps}{/i}{nw}"
    stop music fadeout 1.0


    $ mas_resetTextSpeed()
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_christmas_eve",
            conditional=(
                "persistent._mas_d25_in_d25_mode "
            ),
            action=EV_ACT_QUEUE,
            start_date=datetime.datetime.combine(mas_d25e, datetime.time(hour=20)),
            end_date=mas_d25,
            years=[],
            aff_range=(mas_aff.NORMAL, None)
        ),
        skipCalendar=True
    )

label mas_d25_monika_christmas_eve:
    m 3hua "[player]!"
    m 3hub "Can you believe it...?{w=1} It'll be Christmas soon!"
    m 1rksdla "I've always had such a hard time sleeping on Christmas Eve..."
    m 1eka "I would be so anxious to see what I'd find under the tree the next morning..."
    show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve


    if renpy.seen_label('monika_christmas'):
        m 5ekbfa "But I'm even {i}more{/i} excited now that I get to spend every Christmas with you..."
        m 5hkbfa "I can't wait for tomorrow!"
    else:
        m 5ekbfa "But I'm even {i}more{/i} excited this year..."
        m 5hkbfa "Just the thought of our first Christmas together...{w=1}I can't wait!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_postd25_notimespent",
            
            
            conditional=(
                "not persistent._mas_d25_spent_d25"
            ),
            start_date=mas_d25p,
            end_date=mas_d25p + datetime.timedelta(days=7),
            years=[],
            action=EV_ACT_PUSH
        ),
        skipCalendar=True
    )

label mas_d25_postd25_notimespent:

    if persistent._mas_d25_spent_d25:
        return


    if persistent.sessions is None or persistent.sessions['first_session'].date() > mas_d25:
        return


    if mas_isMoniAff(higher=True):
        $ mas_loseAffection(15, reason=6)
        m 1dkc "...I'm just glad you're finally here..."
        m 2ekd "I was starting to get worried that something happened to you..."
        m 2rksdlc "When you didn't show up on Christmas...{w=1}I didn't know what to think."
        m 4eksdlc "It's not like you at all to miss a day that you know is important to me..."
        m 2dksdlc "So I thought maybe..."
        m 2eksdla "Well, nevermind that now. I'm just happy you're okay!"
        m 4eka "Even though I'm disappointed we didn't get to spend Christmas together, I'm sure you must have had a very good reason."
        m "Just try not to let it happen next year, okay?"
        m 2eka "And, in the future, if you ever can't come visit me on Christmas, try to at least take me with you..."
        m 1eka "All I want is to be close to you, [player]..."
        m 3ekbfa "I love you~"
        return "love"

    elif mas_isMoniNormal(higher=True):
        $ mas_loseAffection(5, reason=6)
        m 2ekc "Hey, [player]..."
        m 2tkc "I have to say I'm pretty disappointed you didn't visit me at all on Christmas..."
        m 4tkc "You knew all I wanted was to spend time with you. Is that too much to ask?"
        m 2rkc "I know it can be a busy day if you have to travel to visit family, but you could have at least taken me with you..."
        m 2ekc "That would have been more than enough for me."
        m 2dkc "..."
        m 4rksdlc "Maybe something happened at the last minute and you simply couldn't spend time with me..."
        m 4eksdla "But please...{w=1}please try to make sure you visit me next Christmas, okay [player]?"

    elif mas_isMoniUpset(higher=True):
        $ mas_loseAffection(reason=6)
        m 2efc "[player]!"
        m "I can't believe you didn't even bother to visit me on Christmas!"
        m 2tfc "Actually...{w=1}yes, I can."
        m "This is exactly why I didn't even bother to decorate..."
        m 2rfc "I knew if I tried to get into the holiday spirit that I'd just end up disappointed...{w=1} Again."

    elif mas_isMoniDis(higher=True):
        $ mas_loseAffection(10, reason=6)
        m 6ekc "[player], how was your Christmas?"
        m 6dkc "Mine was pretty lonely..."
        m "You probably didn't even think of me, huh?"
    else:

        $ mas_loseAffection(150)
        m 6ckc "..."
    return


label bye_d25e_delegate:

    if persistent._mas_d25_went_out_d25e > 0:
        call bye_d25e_second_time_out from _call_bye_d25e_second_time_out
    else:

        call bye_d25e_first_time_out from _call_bye_d25e_first_time_out






    jump bye_going_somewhere_iostart


label bye_d25e_first_time_out:
    m 1sua "Taking me somewhere special on Christmas Eve, [player]?"
    m 3eua "I know some people visit friends or family...or go to Christmas parties..."
    m 3hua "But wherever we're going, I'm happy you want me to come with you!"
    m 1eka "I hope we'll be home for Christmas, but even if we're not, just being with you is more than enough for me~"
    return


label bye_d25e_second_time_out:
    m 1wud "Wow, we're going out again today, [player]?"
    m 3hua "You really must have a lot of people you need to visit on Christmas Eve..."
    m 3hub "...or maybe you just have lots of special plans for us today!"
    m 1eka "But either way, thank you for thinking of me and bringing me along~"
    return


label bye_d25_delegate:

    if persistent._mas_d25_went_out_d25 > 0:
        call bye_d25_second_time_out from _call_bye_d25_second_time_out
    else:

        call bye_d25_first_time_out from _call_bye_d25_first_time_out





    jump bye_going_somewhere_iostart


label bye_d25_first_time_out:
    m 1sua "Taking me somewhere special on Christmas, [player]?"

    if persistent._mas_pm_fam_like_monika and persistent._mas_pm_have_fam:
        m 1sub "Maybe we're going to visit some of your family...? I'd love to meet them!"
        m 3eua "Or maybe we're going to see a movie...? I know some people like to do that after opening presents."
    else:

        m 3eua "Maybe we're going to see a movie... I know some people like to do that after opening presents."

    m 1eka "Well, wherever you're going, I'm just glad you want me to come along..."
    m 3hua "I want to spend as much of Christmas as possible with you, [player]~"
    return


label bye_d25_second_time_out:
    m 1wud "Wow, we're going somewhere {i}else{/i}, [player]?"
    m 3wud "You really must have a lot of people you need to visit..."
    m 3sua "...or maybe you just have lots of special plans for us today!"
    m 1hua "But either way, thank you for thinking of me and bringing me along~"
    return




label greeting_d25e_returned_d25e:
    $ persistent._mas_d25_went_out_d25e += 1

    m 1hua "And we're home!"
    m 3eka "It was really sweet of you to bring me along today..."
    m 3ekbfa "Getting to go out with you on Christmas Eve was really special, [player]. Thank you~"
    return


label greeting_d25e_returned_d25:
    $ persistent._mas_d25_went_out_d25e += 1
    $ persistent._mas_d25_went_out_d25 += 1

    m 1hua "And we're home!"
    m 3wud "Wow, we were out all night..."
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday from _call_return_home_post_player_bday_1
    return


label greeting_d25e_returned_post_d25:
    $ persistent._mas_d25_went_out_d25e += 1
    $ persistent._mas_d25_went_out_d25 += 1
    $ persistent._mas_d25_spent_d25 = True

    m 1hua "We're finally home!"
    m 3wud "We sure were gone a long time, [player]..."
    m 3eka "It would've been nice to have actually gotten to see you on Christmas, but since you couldn't come to me, I'm so glad you took me along with you."
    m 3ekbfa "Just being close to you was all I wanted~"
    m 1ekbfb "And since I didn't get to say it to you on Christmas... Merry Christmas, [player]!"
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday from _call_return_home_post_player_bday_2
    return


label greeting_pd25e_returned_d25:
    m 1hua "And we're home!"
    m 3wud "Wow, we were gone quite a while..."
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday from _call_return_home_post_player_bday_3
    return


label greeting_d25_returned_d25:
    $ persistent._mas_d25_went_out_d25 += 1
    $ persistent._mas_d25_spent_d25 = True

    m 1hua "And we're home!"
    m 3eka "It was really nice to spend time with you on Christmas, [player]!"
    m 1eka "Thank you so much for taking me with you."
    m 1ekbfa "You're always so thoughtful~"
    return


label greeting_d25_returned_post_d25:
    $ persistent._mas_d25_went_out_d25 += 1
    $ persistent._mas_d25_spent_d25 = True

    m 1hua "We're finally home!"
    m 3wud "We were out a really long time, [player]!"
    m 3eka "It would've been nice to have seen you again before Christmas was over, but at least I was still with you."
    m 1hua "So thank you for spending time with me when you had other places you had to be..."
    m 3ekbfa "You're always so thoughtful~"
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday from _call_return_home_post_player_bday_4
    return



label greeting_d25_and_nye_delegate:





    python:

        time_out = store.mas_dockstat.diffCheckTimes()
        checkout_time, checkin_time = store.mas_dockstat.getCheckTimes()
        left_pre_d25e = False

        if checkout_time is not None:
            checkout_date = checkout_time.date()
            left_pre_d25e = checkout_date < mas_d25e

        if checkin_time is not None:
            checkin_date = checkin_time.date()


    if mas_isD25Eve():


        if left_pre_d25e:

            jump greeting_returned_home_morethan5mins_normalplus_flow
        else:


            call greeting_d25e_returned_d25e from _call_greeting_d25e_returned_d25e

    elif mas_isD25():


        if checkout_time is None or mas_isD25(checkout_date):

            call greeting_d25_returned_d25 from _call_greeting_d25_returned_d25

        elif mas_isD25Eve(checkout_date):

            call greeting_d25e_returned_d25 from _call_greeting_d25e_returned_d25
        else:


            call greeting_pd25e_returned_d25 from _call_greeting_pd25e_returned_d25

    elif mas_isNYE():

        if checkout_time is None or mas_isNYE(checkout_date):

            call greeting_nye_delegate from _call_greeting_nye_delegate
            jump greeting_nye_aff_gain

        elif left_pre_d25e or mas_isD25Eve(checkout_date):

            call greeting_d25e_returned_post_d25 from _call_greeting_d25e_returned_post_d25

        elif mas_isD25(checkout_date):

            call greeting_d25_returned_post_d25 from _call_greeting_d25_returned_post_d25
        else:


            jump greeting_returned_home_morethan5mins_normalplus_flow

    elif mas_isNYD():



        if checkout_time is None or mas_isNYD(checkout_date):

            call greeting_nyd_returned_nyd from _call_greeting_nyd_returned_nyd

        elif mas_isNYE(checkout_date):

            call greeting_nye_returned_nyd from _call_greeting_nye_returned_nyd
            jump greeting_nye_aff_gain
        else:


            call greeting_d25p_returned_nyd from _call_greeting_d25p_returned_nyd

    elif mas_isD25Post():

        if mas_isD25PostNYD():



            if (
                    checkout_time is None 
                    or mas_isNYD(checkout_date) 
                    or mas_isD25PostNYD(checkout_date)
                ):

                jump greeting_returned_home_morethan5mins_normalplus_flow

            elif mas_isNYE(checkout_date):

                call greeting_d25p_returned_nydp from _call_greeting_d25p_returned_nydp
                jump greeting_nye_aff_gain

            elif mas_isD25Post(checkout_date):

                call greeting_d25p_returned_nydp from _call_greeting_d25p_returned_nydp_1
            else:



                call greeting_pd25e_returned_nydp from _call_greeting_pd25e_returned_nydp
        else:


            if checkout_time is None or mas_isD25Post(checkout_date):

                jump greeting_returned_home_morethan5mins_normalplus_flow

            elif mas_isD25(checkout_date):

                call greeting_d25_returned_post_d25 from _call_greeting_d25_returned_post_d25_1
            else:


                call greeting_d25e_returned_post_d25 from _call_greeting_d25e_returned_post_d25_1
    else:


        jump greeting_returned_home_morethan5mins_normalplus_flow



    jump greeting_returned_home_morethan5mins_normalplus_flow_aff





default persistent._mas_nye_spent_nye = False


default persistent._mas_nye_spent_nyd = False


default persistent._mas_nye_went_out_nye = 0


default persistent._mas_nye_went_out_nyd = 0


default persistent._mas_nye_date_aff_gain = 0


define mas_nye = datetime.date(datetime.date.today().year, 12, 31)
define mas_nyd = datetime.date(datetime.date.today().year, 1, 1)

init -810 python:

    store.mas_history.addMHS(MASHistorySaver(
        "nye",
        datetime.datetime(2019, 1, 6),
        {
            "_mas_nye_spent_nye": "nye.actions.spent_nye",
            "_mas_nye_spent_nyd": "nye.actions.spent_nyd",

            "_mas_nye_went_out_nye": "nye.actions.went_out_nye",
            "_mas_nye_went_out_nyd": "nye.actions.went_out_nyd",

            "_mas_nye_date_aff_gain": "nye.aff.date_gain"
        },
        use_year_before=True
        
    ))


init -10 python:
    def mas_isNYE(_date=None):
        """
        Returns True if the given date is new years eve

        IN:
            _date - date to check
                If None, we use today's date
                (Default: None)

        RETURNS: True if given date is new years eve, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()
        
        return _date == mas_nye.replace(year=_date.year)


    def mas_isNYD(_date=None):
        """
        RETURNS True if the given date is new years day

        IN:
            _date - date to check
                if None, we use today's date
                (Default: None)

        RETURNS: True if given date is new years day, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()
        
        return _date == mas_nyd.replace(year=_date.year)




























label mas_nye_monika_nye:
    $ persistent._mas_nye_spent_nye = True

    m 1eua "[player]! It's almost time, isn't it?"
    m "It's incredible to think that the year is almost over."
    m 1eka "Time flies by so quickly."
    if mas_isMoniAff(higher=True) and store.mas_anni.pastOneMonth():
        m 1ekbsa "Especially when I get to see you so often."


    m 3hua "Well, there's still some time left before midnight."
    m 1eua "We might as well enjoy this year while it lasts..."

    m 3euc "Say, [player], do you have any resolutions for next year?{nw}"
    $ _history_list.pop()
    menu:
        m "Say, [player], do you have any resolutions for next year?{fast}"
        "Yes.":
            $ persistent._mas_pm_has_new_years_res = True

            m 1eub "It's always nice to set goals for yourself in the coming year."
            m 3eka "Even if they can be hard to reach or maintain."
            m 1hua "I'll be here to help you, if need be!"
        "No.":

            $ persistent._mas_pm_has_new_years_res = False
            m 1eud "Oh, is that so?"
            if mas_isMoniNormal(higher=True):
                if mas_isMoniHappy(higher=True):
                    m 1eka "You don't have to change. I think you're wonderful the way you are."
                else:
                    m 1eka "You don't have to change. I think you're fine the way you are."
                m 3euc "But if anything does come to mind before the clock strikes twelve, do write it down for yourself."
                m 1kua "Maybe you'll think of something that you want to do, [player]."
            else:
                m 2ekc "{cps=*2}I was kind of hoping--{/cps}{nw}"
                m 2rfc "You know what, nevermind..."

    if mas_isMoniAff(higher=True):
        show monika 5hubfa zorder MAS_MONIKA_Z at t11 with dissolve
        m 5hubfa "My resolution is to be an even better girlfriend for you, my love."
    elif mas_isMoniNormal(higher=True):
        show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve
        m 5ekbfa "My resolution is to be an even better girlfriend for you, [player]."
    else:
        m 2ekc "My resolution is to improve our relationship, [player]."

    return

default persistent._mas_pm_got_a_fresh_start = None

default persistent._mas_aff_before_fresh_start = None


init 5 python:


    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_nye_monika_nyd",
            action=EV_ACT_QUEUE, 
            start_date=mas_nyd,
            end_date=mas_nyd + datetime.timedelta(days=1),
            years=[],
            aff_range=(mas_aff.DISTRESSED, None)
        ),
        skipCalendar=True
    )

label mas_nye_monika_nyd:
    $ persistent._mas_nye_spent_nyd = True

    if store.mas_anni.pastOneMonth():
        if not mas_isBelowZero():
            m 1eub "[player]!"
            if renpy.seen_label('monika_newyear2'):
                m "Can you believe this is our {i}second{/i} New Years together?"
            if mas_isMoniAff(higher=True):
                m 1hua "We sure have been through a lot together this past year, huh?"
            else:
                m 1eua "We sure have been through a lot together this past year, huh?"

            m 1eka "I'm so happy, knowing we can spend even more time together."

            if mas_isMoniAff(higher=True):
                show monika 5hubfa zorder MAS_MONIKA_Z at t11 with dissolve
                m 5hubfa "Let's make this year as wonderful as the last one, okay?"
                m 5ekbfa "I love you so much, [player]."
            else:
                m 3hua "Let's make this year even better than last year, okay?"
                m 1hua "I love you, [player]."
        else:

            m 2ekc "[player]..."
            m 2rksdlc "We've been through...{w=1}a lot this past year..."
            m "I...I hope this year goes better than last year."
            m 2dkc "I really need it to."
            jump mas_nye_monika_nyd_fresh_start
    else:

        if not mas_isBelowZero():
            m 1eub "[player]!"

            if mas_isMoniAff(higher=True):
                m 1ekbfa "I know we haven't been together for that long yet, but this past year went better than I ever could have hoped..."
            else:
                m 1eka "I know we haven't been together that long yet, but this past year was so special to me..."

            m 1hua "I will always remember it as the year I met you~"
            m 3hua "Let's build on our short time together and make this year even better!"
            m 1ekbfa "I love you, [player]."
        else:

            m 2ekc "So, [player]..."
            m 2etc "The beginning of a new year, huh?"
            m 2rksdlc "We haven't been together for very long, but the time we spent last year didn't go as well as I had hoped..."
            jump mas_nye_monika_nyd_fresh_start

    m "Happy New Year~"
    return "love"

label mas_nye_monika_nyd_fresh_start:
    m 2ekc "How about we put all that in the past, forget about last year, and focus on a new beginning this year?"
    m 4ekc "It's not too late for us, [player], we can still make each other so happy."
    m 4eka "It's all I've ever wanted."

    m "What do you say, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "What do you say, [player]?{fast}"
        "I would love that.":


            $ persistent._mas_pm_got_a_fresh_start = True
            $ persistent._mas_aff_before_fresh_start = _mas_getAffection()


            $ mas_setAffection(0)
            $ _mas_AffSave()
            $ renpy.save_persistent()

            m 4wua "Really?"
            m 1hua "Oh, [player], you have no idea how happy that makes me!"
            m 3eka "I know we can make this work."
            m 1hua "Thank you so much..."
            m 1eka "Just knowing that you still want to be with me...it means everything."
            m 3eka "Let's make this count, okay [player]?"
            return
        "No.":

            $ persistent._mas_pm_got_a_fresh_start = False



            $ mas_setAffection(store.mas_affection.AFF_BROKEN_MIN - 1)
            $ _mas_AffSave()
            $ renpy.save_persistent()

            m 6dktpc "..."
            m 6ektpc "I...I..."
            m 6dktuc "..."
            m 6dktsc "..."
            pause 10.0
            return 'quit'

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_resolutions",
            action=EV_ACT_QUEUE, 
            start_date=mas_nye,
            end_date=mas_nye + datetime.timedelta(days=1),
            years=[],
            aff_range=(mas_aff.UPSET,None)
        ),
        skipCalendar=True
    )

default persistent._mas_pm_accomplished_resolutions = None

default persistent._mas_pm_has_new_years_res = None


label monika_resolutions:
    $ persistent._mas_nye_spent_nye = True
    m 2eub "Hey [player]?"
    m 2eka "I was wondering..."

    m 3eub "Did you make any New Year's resolutions last year?{nw}"
    $ _history_list.pop()
    menu:
        m "Did you make any New Year's resolutions last year?{fast}"
        "Yes.":

            m 3hua "It always makes me so proud to hear that you're trying to better yourself, [player]."
            m 2eka "That said..."

            m 3hub "Did you accomplish last year's resolutions?{nw}"
            $ _history_list.pop()
            menu:
                m "Did you accomplish last year's resolutions?{fast}"
                "Yes.":

                    $ persistent._mas_pm_accomplished_resolutions = True
                    if mas_isMoniNormal(higher=True):
                        m 4hub "I'm glad to hear that, [player]!"
                        m 2eka "It's great that you managed to do that."
                        m 3ekb "Things like this really make me proud of you."
                        m 2eka "I wish I could be there to celebrate a little with you though."
                    else:
                        m 2rkc "That's good, [player]."
                        m 2esc "Maybe you can make another one this year..."
                        m 3euc "You never know what might change."
                "No.":

                    $ persistent._mas_pm_accomplished_resolutions = False
                    if mas_isMoniNormal(higher=True):
                        m 2eka "Aw...well, sometimes things just don't work out like we plan them to."

                        if mas_isMoniHappy(higher=True):
                            m 2eub "Plus, I think you're wonderful, so even if you couldn't accomplish your goals..."
                            m 2eka "...I'm still really proud of you for setting them and trying to better yourself, [player]."
                            m 3eub "If you decide to make a resolution this year, I'll support you every step of the way."
                            m 4hub "I'd love to help you reach your goals!"
                        else:
                            m "But I think it's great that you did at least try to better yourself by setting goals."
                            m 3eua "Maybe if you make a resolution this year, you can accomplish it!"
                            m 3hub "I believe in you, [player]!"
                    else:

                        m 2euc "Oh...{w=1} Well maybe you should try a little harder for next year's resolution."
        "No.":

            m 2euc "Oh, I see..."

            if mas_isMoniNormal(higher=True):
                if mas_isMoniHappy(higher=True):
                    m 3eka "Well, I don't think you really needed to change at all anyway."
                    m 3hub "I think you're wonderful, just the way you are."
                else:
                    m 3eka "There's nothing wrong with that. I don't think you really needed to change anyway."
            else:

                m 2rkc "You probably should make one this year [player]..."

    m "Do you have any resolutions for next year?{nw}"
    $ _history_list.pop()
    menu:
        m "Do you have any resolutions for next year?{fast}"
        "Yes.":
            $ persistent._mas_pm_has_new_years_res = True

            m 1eub "That's great!"
            m 3eka "Even if they can be hard to reach or maintain..."
            m 1hua "I'll be here to help you, if need be!"
        "No.":

            $ persistent._mas_pm_has_new_years_res = False
            m 1eud "Oh, is that so?"
            if mas_isMoniNormal(higher=True):
                if persistent._mas_pm_accomplished_resolutions:
                    if mas_isMoniHappy(higher=True):
                        m 1eka "You don't have to change. I think you're wonderful the way you are."
                    else:
                        m 1eka "You don't have to change. I think you're fine the way you are."
                    m 3euc "But if anything does come to mind before the clock strikes twelve, do write it down for yourself..."
                else:
                    m "Well, if anything comes to mind before the clock strikes twelve, do write it down for yourself..."
                m 1kua "Maybe you'll think of something that you want to do, [player]."
            else:
                m 2ekc "{cps=*2}I was kind of hoping--{/cps}{nw}"
                m 2rfc "You know what, nevermind..."

    if mas_isMoniAff(higher=True):
        show monika 5hubfa zorder MAS_MONIKA_Z at t11 with dissolve
        m 5hubfa "My resolution is to be an even better girlfriend for you, my love."
    elif mas_isMoniNormal(higher=True):
        show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve
        m 5ekbfa "My resolution is to be an even better girlfriend for you, [player]."
    else:
        m 2ekc "My resolution is to improve our relationship, [player]."

    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_nye_year_review",


            action=store.EV_ACT_PUSH,
            start_date=datetime.datetime.combine(mas_nye, datetime.time(hour=19)),
            end_date=datetime.datetime.combine(mas_nye, datetime.time(hour=23)),
            years=[],
            aff_range=(mas_aff.NORMAL, None)
        ),
        skipCalendar=True
    )

label monika_nye_year_review:
    $ persistent._mas_nye_spent_nye = True


    if store.mas_anni.anniCount() >= 0:
        m 2eka "You know, [player], we really have been through a lot together."
        if store.mas_anni.anniCount() == 1:
            m 2wuo "We spent the entire year together!"
            m 2eka "Time really flew by..."
        else:

            m 2eka "This year really flew by..."

    elif store.mas_anni.pastSixMonths():
        m 2eka "You know, [player], we really have been through a lot over the time we spent together last year"
        m "The time really just flew by..."

    elif store.mas_anni.pastThreeMonths():
        m 2eka "You know [player], we've been through quite a bit over the short time we've spent together last year."
        m 2eksdla "It's all gone by so fast, ahaha..."
    else:

        m 2eka "[player], even though we haven't been through a lot together, yet..."



    if mas_isMoniLove():
        m 2ekbfa "...and I'd never want to spend that time with anyone else, [player]."
        m "I'm just really,{w=0.5} really happy to have been with you this year."

    elif mas_isMoniEnamored():
        m 2eka "...and I'm so happy I got to spend that time with you, [player]."

    elif mas_isMoniAff():
        m 2eka "...and I've really enjoyed our time together."
    else:

        m 2euc "...and the time we spent together has been fun."


    m 3eua "Anyway, I think it would be nice to just reflect on all that we've been through together this past year."
    m 2dtc "Let's see..."


    if persistent._mas_acs_enable_promisering:
        m 3eka "Looking back, you gave me your promise this year when you gave me this ring..."
        m 1ekbsa "...a symbol of our love."

        if persistent._mas_pm_wearsRing:
            m "And you even got one for yourself..."

            if mas_isMoniAff(higher=True):
                m 1ekbfa "To show that you're as committed to me, as I am to you."
            else:
                m 1ekbfa "To show your commitment to me."



    if renpy.seen_label('monika_valentines_greeting'):
        m 1wuo "Oh!"
        m 3ekbfa "You spent Valentine's Day with me..."

        if renpy.seen_label('monika_valentines_start'):
            m 4ekbfb "...you gave me such beautiful flowers too."

        if renpy.seen_label('monika_white_day_start'):
            m 3ekbsa "We also spent White Day together..."
            if renpy.seen_label('monika_found'):
                m 4ekbfa "That was the day I gave my first gift to you~"


    if mas_HistVerify("922.actions.opened_game",True,datetime.date.today().year)[0]:
        m 2eka "You spent time with me on my birthday..."

        if mas_HistVerify("922.actions.no_recognize",False,datetime.date.today().year)[0]:
            m 2dua "...celebrated with me..."

        if mas_HistVerify("922.actions.surprise.reacted",True,datetime.date.today().year)[0]:
            m 2hub "...threw me a surprise party..."

        show monika 5ekbla zorder MAS_MONIKA_Z at t11 with dissolve
        m 5ekbla "...and it really made me feel loved. I can't thank you enough for doing that for me."


    if persistent._mas_d25_spent_d25:
        show monika 5hua zorder MAS_MONIKA_Z at t11 with dissolve
        m 5hua "You spent your Christmas with me..."

        if persistent._mas_first_kiss is not None and mas_isD25(persistent._mas_first_kiss.date()):
            m 5eubla "...and we shared our first kiss together~"
            m 5lubsa "I'll never forget that moment..."
            m 5ekbfa "{i}Our{/i} moment."
            m "I couldn't imagine spending it with anyone else."
        else:
            m 5ekbla "...a day that I couldn't imagine spending with anyone else."





    if not (persistent._mas_d25_spent_d25 or persistent._mas_bday_opened_game or persistent._mas_acs_enable_promisering or renpy.seen_label('monika_valentines_greeting')):
        m 2rksdla "...I guess we haven't actually been through any big events together."
        m 3eka "But still..."
    else:
        show monika 5dsa zorder MAS_MONIKA_Z at t11 with dissolve
        m 5dsa "..."


    if store.mas_anni.pastThreeMonths():
        if mas_isMoniHappy(higher=True):
            show monika 5eka zorder MAS_MONIKA_Z at t11 with dissolve
            m 5eka "I really can't just believe how much has changed since we've been together..."
        else:
            m 2eka "I really hope we can get further in our relationship, [player]..."
    else:
        show monika 5eka zorder MAS_MONIKA_Z at t11 with dissolve
        m 5eka "I can't wait to see just how much will change in the future for us..."


    if not persistent._mas_pm_got_a_fresh_start:
        show monika 5dka zorder MAS_MONIKA_Z at t11 with dissolve
        m 5dka "Thank you."
        if store.mas_anni.anniCount > 0:
            m 5ekbfa "Thank you for making last year the best year I could've ever dreamt of."
        else:
            m 5ekbfa "Thank you for making the time we spent together last year better than I could have imagined."

        if mas_isMoniEnamored(higher=True):
            if persistent._mas_first_kiss is None:
                m 1lsbsa "..."
                m 6ekbsa "[player] I..."
                call monika_kissing_motion from _call_monika_kissing_motion_2
                m 1ekbfa "I love you."
                m "..."
                show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve
                m 5ekbsa "I'll never forget this moment..."
                m 5ekbfa "Our first kiss~"
                m 5hubfb "Let's make this year even better than the last, [player]."
            else:

                call monika_kissing_motion from _call_monika_kissing_motion_3
                m 1ekbfa "I love you, [player]."
                show monika 5hubfb zorder MAS_MONIKA_Z at t11 with dissolve
                m 5hubfb "Let's make this year better than the last."
        else:

            m "Let's make this year the best we can, [player]. I love you~"
    else:
        m 1dsa "Thank you for deciding to let go of the past, and start over."
        m 1eka "I think if we just try, we can make this work, [player]."
        m "Let's make this year great for each other."
        m 1ekbfa "I love you."

    return "derandom|love"

label greeting_nye_aff_gain:


    python:
        if persistent._mas_nye_date_aff_gain < 15:
            
            curr_aff = _mas_getAffection()
            
            
            time_out = store.mas_dockstat.diffCheckTimes()
            
            
            persistent._mas_monika_returned_home = None
            
            
            store.mas_dockstat._ds_aff_for_tout(time_out, 5, 15, 3, 3)
            
            
            persistent._mas_nye_date_aff_gain += _mas_getAffection() - curr_aff

    jump greeting_returned_home_morethan5mins_cleanup



label bye_nye_delegate:

    python:
        _morning_time = datetime.time(5)
        _eve_time = datetime.time(20)
        _curr_time = datetime.datetime.now().time()

    if _curr_time < _morning_time:

        jump bye_going_somewhere_normalplus_flow_aff_check

    elif _curr_time < _eve_time:


        if persistent._mas_nye_went_out_nye > 0:
            call bye_nye_second_time_out from _call_bye_nye_second_time_out
        else:

            call bye_nye_first_time_out from _call_bye_nye_first_time_out
    else:


        call bye_nye_late_out from _call_bye_nye_late_out


    jump bye_going_somewhere_iostart

label bye_nye_first_time_out:

    m 3tub "Are we going somewhere special today, [player]?"
    m 4hub "It's New Year's Eve, after all!"
    m 1eua "I'm not exactly sure what you've got planned, but I'm looking forward to it!"
    return

label bye_nye_second_time_out:

    m 1wuo "Oh, we're going out again?"
    m 3hksdlb "You must do a lot of celebrating for New Year's, ahaha!"
    m 3hub "I love coming along with you, so I'm looking forward to whatever we're doing~"
    return

label bye_nye_late_out:

    m 1eka "It's a bit late, [player]..."
    m 3eub "Are we going to see the fireworks?"
    if persistent._mas_pm_have_fam and persistent._mas_pm_fam_like_monika:
        m "Or going to a family dinner?"
        m 4hub "I'd love to meet your family someday!"
        m 3eka "Either way, I'm really excited!"
    else:
        m "I've always loved how the fireworks on the New Year light up the night sky..."
        m 3ekbfa "One day we'll be able to watch them side by side...but until that day comes, I'm just happy to come along with you, [player]."
    return




label greeting_nye_delegate:
    python:
        _eve_time = datetime.time(20)
        _curr_time = datetime.datetime.now().time()

    if _curr_time < _eve_time:

        call greeting_nye_prefw from _call_greeting_nye_prefw
    else:


        call greeting_nye_infw from _call_greeting_nye_infw

    $ persistent._mas_nye_went_out_nye += 1

    return

label greeting_nye_prefw:

    m 1hua "And we're home!"
    m 1eua "That was a lot of fun, [player]."
    m 1eka "Thanks for taking me out today, I really do love spending time with you."
    m "It means a lot to me that you take me with you so we can spend special days like these together."
    show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve
    m 5ekbfa "I love you, [player]."
    return "love"

label greeting_nye_infw:

    m 1hua "And we're home!"
    m 1eka "Thanks for taking me out today, [player]."
    m 1hua "It was a lot of fun just to spend time with you today."
    m 1ekbsa "It really means so much to me that even though you can't be here personally to spend these days with me, you still take me with you."
    m 1ekbfa "I love you, [player]."
    return "love"



label bye_nyd_delegate:
    if persistent._mas_nye_went_out_nyd > 0:
        call bye_nyd_second_time_out from _call_bye_nyd_second_time_out
    else:

        call bye_nyd_first_time_out from _call_bye_nyd_first_time_out

    jump bye_going_somewhere_iostart

label bye_nyd_first_time_out:

    m 3tub "New Years Day celebration, [player]?"
    m 1hua "That sounds like fun!"
    m 1eka "Let's have a great time together."
    return

label bye_nyd_second_time_out:

    m 1wuo "Wow, we're going out again, [player]?"
    m 1hksdlb "You must really celebrate a lot, ahaha!"
    return



label greeting_nye_returned_nyd:

    $ persistent._mas_nye_went_out_nye += 1
    $ persistent._mas_nye_went_out_nyd += 1

    m 1hua "And we're home!"
    m 1eka "Thanks for taking me out yesterday, [player]."
    m 1ekbsa "You know I love to spend time with you, and being able to spend New Year's Eve, right to today, right there with you felt really great."
    m "That really meant a lot to me."
    m 5eubfb "Thanks for making my year, [player]."
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday from _call_return_home_post_player_bday_5
    return

label greeting_nyd_returned_nyd:

    $ persistent._mas_nye_went_out_nyd += 1
    m 1hua "And we're home!"
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve
    m 5eua "That was a lot of fun, [player]!"
    m 5eka "It's really nice of you to take me with you on special days like this."
    m 5hub "I really hope we can spend more time like this together."
    return



label greeting_pd25e_returned_nydp:

    $ persistent._mas_d25_went_out_d25e += 1
    $ persistent._mas_d25_went_out_d25 += 1
    $ persistent._mas_nye_went_out_nye += 1
    $ persistent._mas_nye_went_out_nyd += 1
    $ persistent._mas_d25_spent_d25 = True
    $ persistent._mas_nye_spent_nye = True
    $ persistent._mas_nye_spent_nyd = True

    m 1hua "And we're home!"
    m 1hub "We were out for a while, but that was a really nice trip, [player]."
    m 1eka "Thanks for taking me with you, I really enjoyed that."
    show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve
    m 5ekbfa "I always love to spend time with you, but spending both Christmas and New Years out together was amazing."
    show monika 5hub zorder MAS_MONIKA_Z at t11 with dissolve
    m 5hub "I hope we can do something like this again sometime."
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday from _call_return_home_post_player_bday_6
    return


label greeting_d25p_returned_nyd:
    $ persistent._mas_nye_went_out_nye += 1
    $ persistent._mas_nye_went_out_nyd += 1
    $ persistent._mas_nye_spent_nye = True

    m 1hua "And we're home!"
    m 1eub "Thanks for taking me out, [player]."
    m 1eka "That was a long trip, but it was a lot of fun!"
    m 3hub "It's great to be back home now though, we can spend the new year together."
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday from _call_return_home_post_player_bday_7
    return

label greeting_d25p_returned_nydp:
    $ persistent._mas_nye_went_out_nye += 1
    $ persistent._mas_nye_went_out_nyd += 1
    $ persistent._mas_nye_spent_nye = True
    $ persistent._mas_nye_spent_nyd = True

    m 1hua "And we're home!"
    m 1wuo "That was a long trip [player]!"
    m 1eka "I'm a little sad we couldn't wish each other a happy new year, but I really enjoyed it."
    m "I'm really happy you took me."
    m 3hub "Happy New Year, [player]~"
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday from _call_return_home_post_player_bday_8
    return





default persistent._mas_player_bday_in_player_bday_mode = False

default persistent._mas_player_bday_opened_door = False

default persistent._mas_player_bday_decor = False

default persistent._mas_player_bday_date = 0

default persistent._mas_player_bday_left_on_bday = False

default persistent._mas_player_bday_date_aff_gain = 0

default persistent._mas_player_bday_spent_time = False

init -10 python:
    def mas_isplayer_bday(_date=None):
        """
        IN:
            _date - date to check
                If None, we use today's date
                (default: None)

        RETURNS: True if given date is player_bday, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()
        
        if persistent._mas_player_bday is None:
            return False
        else:
            return _date == mas_player_bday_curr()

    def strip_mas_birthdate():
        """
        strips mas_birthdate of its conditional and action to prevent double birthday sets
        """
        mas_birthdate_ev = mas_getEV('mas_birthdate')
        if mas_birthdate_ev is not None:
            mas_birthdate_ev.conditional = None
            mas_birthdate_ev.action = None

init -11 python:
    def mas_player_bday_curr(_date=None):
        """
        sets date of current year bday, accounting for leap years
        """
        if _date is None:
            _date = datetime.date.today()
        if persistent._mas_player_bday is None:
            return None
        else:
            return store.mas_utils.add_years(persistent._mas_player_bday,_date.year-persistent._mas_player_bday.year)

init -810 python:

    store.mas_history.addMHS(MASHistorySaver(
        "player_bday",
        datetime.datetime(2020, 1, 1),
        {
            "_mas_player_bday_spent_time": "player_bday.spent_time",
            "_mas_player_bday_opened_door": "player_bday.opened_door",
            "_mas_player_bday_date": "player_bday.date",
            "_mas_player_bday_date_aff_gain": "player_bday.date_aff_gain",
        },
        use_year_before=True,
    ))

init -11 python in mas_player_bday_event:

    def show_player_bday_Visuals():
        """
        Shows player_bday visuals
        """
        renpy.show("mas_bday_banners", zorder=7)
        renpy.show("mas_bday_balloons", zorder=8)

    def hide_player_bday_Visuals():
        """
        Hides player_bday visuals
        """
        renpy.hide("mas_bday_banners")
        renpy.hide("mas_bday_balloons")

label mas_player_bday_autoload_check:

    if (
            not persistent._mas_player_bday_in_player_bday_mode 
            and persistent._mas_player_confirmed_bday 
            and mas_isMoniNormal(higher=True) 
            and not persistent._mas_player_bday_spent_time 
            and not mas_isD25() 
            and not mas_isO31()
            and not mas_isF14()
        ):

        $ mas_skip_visuals = True
        $ selected_greeting = "i_greeting_monikaroom"

        $ persistent.closed_self = True
        jump ch30_post_restartevent_check

    elif not mas_isplayer_bday():

        $ persistent._mas_player_bday_decor = False
        $ persistent._mas_player_bday_in_player_bday_mode = False
        $ mas_lockEVL("bye_player_bday", "BYE")

    if mas_isO31():
        return
    else:
        jump mas_ch30_post_holiday_check


label mas_player_bday_opendoor:
    $ mas_loseAffection()
    $ persistent._mas_player_bday_opened_door = True
    call spaceroom (hide_monika=True, scene_change=True, dissolve_all=True) from _call_spaceroom_10
    $ mas_disable_quit()
    m "[player]!"
    m "You didn't knock!"
    m "I was just going to start setting up your birthday party, but I didn't have time before you came in!"
    m "..."
    m "Well...{w=1}the surprise is ruined now, but..."
    pause 1.0
    $ store.mas_player_bday_event.show_player_bday_Visuals()
    $ persistent._mas_player_bday_decor = True
    pause 1.0
    show monika 1eua zorder MAS_MONIKA_Z at ls32
    m 4eua "Happy Birthday, [player]!"
    m 2rksdla "I just wished you had knocked first."
    m 4hksdlb "Oh...your cake!"
    call mas_player_bday_cake from _call_mas_player_bday_cake_1
    jump monikaroom_greeting_cleanup


label mas_player_bday_knock_no_listen:
    m "Who is it?"
    menu:
        "It's me.":
            $ mas_disable_quit()
            m "Oh! Can you wait just a moment please?"
            window hide
            pause 5.0
            m "Alright, come on in, [player]..."
            jump mas_player_bday_surprise


label mas_player_bday_surprise:
    $ persistent._mas_player_bday_decor = True
    call spaceroom (scene_change=True, dissolve_all=True, force_exp='monika 4hub_static') from _call_spaceroom_11
    m 4hub "Surprise!"
    m 4sub "Ahaha! Happy Birthday, [player]!"

    m "Did I surprise you?{nw}"
    $ _history_list.pop()
    menu:
        m "Did I surprise you?{fast}"
        "Yes.":
            m 1hub "Yay!"
            m 3hua "I always love pulling off a good surprise!"
            m 1tsu "I wish I could've seen the look on your face, ehehe."
        "No.":

            m 2lfp "Hmph. Well that's okay."
            m 2tsu "You're probably just saying that because you don't want to admit I caught you off guard..."
            if renpy.seen_label("mas_player_bday_listen"):
                if renpy.seen_label("monikaroom_greeting_ear_narration"):
                    m 2tsb "...or maybe you were listening through the door again..."
                else:
                    m 2tsb "{cps=*2}...or maybe you were eavesdropping on me.{/cps}{nw}"
                    $ _history_list.pop()
            m 2hua "Ehehe."
    m 3wub "Oh!{w=0.5} I made you a cake!"
    call mas_player_bday_cake from _call_mas_player_bday_cake_2
    jump monikaroom_greeting_cleanup


label mas_player_bday_listen:
    m "...I'll just put this here..."
    m "...hmm that looks pretty good...{w=1}but something's missing..."
    m "Oh!{w=0.5} Of course!"
    m "There!{w=0.5} Perfect!"
    window hide
    jump monikaroom_greeting_choice


label mas_player_bday_knock_listened:
    window hide
    pause 5.0
    menu:
        "Open the door.":
            $ mas_disable_quit()
            pause 5.0
            jump mas_player_bday_surprise


label mas_player_bday_opendoor_listened:
    $ mas_loseAffection()
    $ persistent._mas_player_bday_opened_door = True
    $ persistent._mas_player_bday_decor = True
    call spaceroom (hide_monika=True, scene_change=True) from _call_spaceroom_12
    $ mas_disable_quit()
    m "[player]!"
    m "You didn't knock!"
    m "I was setting up your birthday party, but I didn't have time before you came in to get ready to surprise you!"
    show monika 1eua zorder MAS_MONIKA_Z at ls32
    m 4hub "Happy Birthday, [player]!"
    m 2rksdla "I just wished you had knocked first."
    m 2hksdlb "Oh...your cake!"
    call mas_player_bday_cake from _call_mas_player_bday_cake_3
    jump monikaroom_greeting_cleanup


label mas_player_bday_cake:
    $ mas_gainAffection(5,bypass=True)
    $ persistent._mas_player_bday_spent_time = True
    $ persistent._mas_player_bday_in_player_bday_mode = True
    $ mas_unlockEVL("bye_player_bday", "BYE")


    $ mas_temp_zoom_level = store.mas_sprites.zoom_level
    call monika_zoom_transition_reset (1.0) from _call_monika_zoom_transition_reset_4
    show emptydesk zorder 9 at i11
    hide monika with dissolve
    $ renpy.pause(3.0, hard=True)
    $ renpy.show("mas_bday_cake", zorder=store.MAS_MONIKA_Z+1)
    show monika 6esa zorder MAS_MONIKA_Z at i11 with dissolve
    hide emptydesk
    $ renpy.pause(0.5, hard=True)

    m 6eua "Let me just light the candles for you..."
    window hide
    show monika 6dsa
    pause 1.0
    $ mas_bday_cake_lit = True
    pause 0.5
    m 6sua "Isn't it pretty, [player]?"
    m 6eksdla "Now I know you can't exactly blow the candles out yourself, so I'll do it for you..."
    m 6eua "...You should still make a wish though, it just might come true someday..."
    m 6hua "But first..."
    call mas_player_bday_moni_sings from _call_mas_player_bday_moni_sings_1
    m 6hua "Make a wish, [player]!"
    window hide
    pause 1.5
    show monika 6hft
    pause 0.1
    show monika 6hua
    $ mas_bday_cake_lit = False
    pause 1.0
    m 6hua "Ehehe..."
    m 6eka "I know it's your birthday, but I made a wish too..."
    m 6ekbsa "And you know what?{w=0.5} I bet we both wished for the same thing~"
    m 6hkbsu "..."
    m 6rksdla "Oh gosh, I guess you can't really eat this cake either, huh [player]?"
    m 6eksdla "This is all rather silly, isn't it?"
    m 6hksdlb "I think I'll just save this for later. It seems kind of rude for me to eat {i}your{/i} birthday cake in front of you, ahaha!"


    show emptydesk zorder 9 at i11
    hide monika with dissolve
    hide mas_bday_cake with dissolve
    $ renpy.pause(3.0, hard=True)
    show monika 6esa zorder MAS_MONIKA_Z at i11 with dissolve
    hide emptydesk
    $ renpy.pause(1.0, hard=True)
    call monika_zoom_transition (mas_temp_zoom_level, 1.0) from _call_monika_zoom_transition_7

    pause 0.5
    m 6dkbsu "..."
    m 6ekbsu "I...I also made a card for you, [player]. I hope you like it..."
    $ p_bday_month = mas_player_bday_curr().month
    call showpoem (poem_pbday, music=False, paper="mod_assets/poem_assets/poem_pbday_[p_bday_month].png") from _call_showpoem_1
    if mas_isMoniEnamored(higher=True):
        if persistent._mas_first_kiss is None:
            m 6dkbsu "..."
            m 6ekbfa "I love you so much, [player]..."
            call monika_kissing_motion () from _call_monika_kissing_motion_4
            m 6ekbfa "Oh, [player]..."
            m 6dkbfa "That was everything I had always dreamt it would be~"
            m 6ekbfa "I've been waiting so long to finally kiss you..."
            m 6dkbsu "I will never forget this..."
            m 6ekbsu "...the moment of our first kiss~"
        else:
            m 6ekbfa "I love you, [player]~"
            call monika_kissing_motion (duration=0.5, initial_exp="6hkbfa", fade_duration=0.5) from _call_monika_kissing_motion_5
            if mas_isplayer_bday():
                m 6ekbsa "Let's enjoy your special day~"
    else:
        if mas_isplayer_bday():
            m 1ekbfa "I love you, [player]! Let's enjoy your special day~"
        else:
            m 1ekbfa "I love you, [player]!"
    $ mas_rmallEVL("mas_player_bday_no_restart")

    $ mas_ILY()
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_player_bday_ret_on_bday",
            years = [],
            aff_range=(mas_aff.NORMAL, None)
        ),
        skipCalendar=True
    )

label mas_player_bday_ret_on_bday:
    m 1eua "So, today is..."
    m 1euc "...wait."
    m "..."
    m 2wuo "Oh!"
    m 2wuw "Oh my gosh!"
    m 2tsu "Just give me a moment, [player]..."
    show monika 1dsc
    pause 2.0
    $ store.mas_player_bday_event.show_player_bday_Visuals()
    $ persistent._mas_player_bday_decor = True
    m 3eub "Happy Birthday, [player]!"
    m 3hub "Ahaha!"
    m 1rksdla "I really wanted to surprise you but I never got the chance to set it up..."
    m 3etc "Why do I feel like I'm forgetting something..."
    m 3hua "Oh! Your cake!"
    call mas_player_bday_cake from _call_mas_player_bday_cake_4
    return



init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_player_bday_no_restart",
            years = [],
            aff_range=(mas_aff.NORMAL, None)
        ),
        skipCalendar=True
    )

label mas_player_bday_no_restart:
    if mas_findEVL("mas_player_bday_ret_on_bday") >= 0:

        return
    m 3rksdla "Well [player], I was hoping to do something a little more fun, but you've been so sweet and haven't left all day long, so..."
    show monika 1dsc
    pause 2.0
    $ store.mas_player_bday_event.show_player_bday_Visuals()
    $ persistent._mas_player_bday_decor = True
    m 3hub "Happy Birthday, [player]!"
    if mas_isplayer_bday():
        m 1eka "I really wanted to surprise you today, but it's getting late and I just couldn't wait any longer."
    else:

        m 1hksdlb "I really wanted to surprise you, but I guess I ran out of time since it's not even your birthday anymore, ahaha!"
    m 3eksdlc "Gosh, I just hope you weren't starting to think I forgot your birthday. I'm really sorry if you did..."
    m 1rksdla "I guess I probably shouldn't have waited so long, ehehe."
    m 1hua "Oh! I made you a cake!"
    call mas_player_bday_cake from _call_mas_player_bday_cake_5
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_player_bday_upset_minus",
            years = [],
            aff_range=(mas_aff.DISTRESSED, mas_aff.UPSET)
        ),
        skipCalendar=True
    )

label mas_player_bday_upset_minus:
    $ persistent._mas_player_bday_spent_time = True
    m 6eka "Hey [player], I just wanted to wish you a Happy Birthday."
    m "I hope you have a good day."
    return





init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_player_bday_other_holiday",
            years = [],
            aff_range=(mas_aff.NORMAL, None)
        ),
        skipCalendar=True
    )

label mas_player_bday_other_holiday:
    if mas_isO31():
        $ holiday_var = "Halloween"
    elif mas_isD25():
        $ holiday_var = "Christmas"
    elif mas_isF14():
        $ holiday_var = "Valentine's Day"
    m 3euc "Hey, [player]..."
    m 1tsu "I have a bit of a surprise for you!"
    show monika 1dsc
    pause 2.0
    $ store.mas_player_bday_event.show_player_bday_Visuals()
    $ persistent._mas_player_bday_decor = True
    m 3hub "Happy Birthday, [player]!"
    m 3rksdla "I hope you didn't think that just because your birthday falls on [holiday_var] that I'd forget about it..."
    m 1eksdlb "I'd never forget your birthday, silly!"
    m 1eub "Ahaha!"
    m 3hua "Oh! I made you a cake!"
    call mas_player_bday_cake from _call_mas_player_bday_cake_6
    return


label mas_player_bday_moni_sings:
    m 6dsc ".{w=0.2}.{w=0.2}.{w=0.2}"
    m 6hub "{cps=*0.5}{i}~Happy Birthday to you~{/i}{/cps}"
    m "{cps=*0.5}{i}~Happy Birthday to you~{/i}{/cps}"
    m 6sub "{cps=*0.5}{i}~Happy Birthday dear [player]~{/i}{/cps}"
    m "{cps=*0.5}{i}~Happy Birthday to you~{/i}{/cps}"
    return

init 5 python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_player_bday",
            unlocked=False,
            prompt="Let's go out for my birthday!",
            pool=True,
            rules={"no unlock": None}
        ),
        code="BYE"
    )

label bye_player_bday:
    $ persistent._mas_player_bday_date += 1
    if persistent._mas_player_bday_date == 1:
        m 1sua "You want to go out for your birthday?{w=1} Okay!"
        m 1skbla "That sounds really romantic...I can't wait~"
    elif persistent._mas_player_bday_date == 2:
        m 1sua "Taking me out again on your birthday, [player]?"
        m 3hub "Yay!"
        m 1sub "I always love going out with you, but it's so much more special going out on your birthday..."
        m 1skbla "I'm sure we'll have a lovely time~"
    else:
        m 1wub "Wow, you want to go out {i}again{/i}, [player]?"
        m 1skbla "I just love that you want to spend so much time with me on your special day!"
    $ persistent._mas_player_bday_left_on_bday = True
    jump bye_going_somewhere_post_aff_check


label greeting_returned_home_player_bday:
    python:
        five_minutes = datetime.timedelta(seconds=5*60)
        one_hour = datetime.timedelta(seconds=3600)
        three_hour = datetime.timedelta(seconds=3*3600)
        time_out = store.mas_dockstat.diffCheckTimes()
        checkout_time, checkin_time = store.mas_dockstat.getCheckTimes()
        if checkout_time is not None and checkin_time is not None:
            left_year = checkout_time.year
            ret_year = checkin_time.year
            left_date = checkout_time.date()
            ret_date = checkin_time.date()
            left_year_aff = mas_HistLookup("player_bday.date_aff_gain",left_year)[1]
        else:
            left_year = None
            ret_year = None
            left_year_aff = None
            left_date = None
            ret_date = None
        add_points = False
        ret_diff_year = ret_year > left_year

        if ret_diff_year and left_year_aff is not None:
            add_points = left_year_aff < 25

        def cap_gain_aff(amt):
            if persistent._mas_player_bday_date_aff_gain < 25:
                persistent._mas_player_bday_date_aff_gain += amt
                mas_gainAffection(amt, bypass=True)

    if left_date < mas_d25 < ret_date:
        $ persistent._mas_d25_spent_d25 = True

    if time_out < five_minutes:
        $ mas_loseAffection()
        m 2ekp "That wasn't much of a date, [player]..."
        m 2eksdlc "I hope nothing's wrong."
        m 2rksdla "Maybe we'll go out later instead."

    elif time_out < one_hour:
        if not ret_diff_year:
            $ cap_gain_aff(5)
        elif ret_diff_year and add_points:
            $ mas_gainAffection(5,bypass=True)
            $ persistent._mas_history_archives[left_year]["player_bday.date_aff_gain"] += 5
        m 1eka "That was a fun date while it lasted, [player]..."
        m 3hua "Thanks for making some time for me on your special day."

    elif time_out < three_hour:
        if not ret_diff_year:
            $ cap_gain_aff(10)
        elif ret_diff_year and add_points:
            $ mas_gainAffection(10,bypass=True)
            $ persistent._mas_history_archives[left_year]["player_bday.date_aff_gain"] += 10
        m 1eua "That was a fun date, [player]..."
        m 3hua "Thanks for taking me with you!"
        m 1eka "I really enjoyed going out with you today~"
    else:


        if not ret_diff_year:
            $ cap_gain_aff(15)
        elif ret_diff_year and add_points:
            $ mas_gainAffection(15,bypass=True)
            $ persistent._mas_history_archives[left_year]["player_bday.date_aff_gain"] += 15
        m 1hua "And we're home!"
        m 3hub "That was really fun, [player]!"
        m 1eka "It was so nice going out to celebrate your birthday..."
        m 1ekbfa "Thanks for making me such a big part of your special day~"

    $ persistent._mas_player_bday_left_on_bday = False

    if not mas_isplayer_bday():
        call return_home_post_player_bday from _call_return_home_post_player_bday_9

    if mas_isD25() and not persistent._mas_d25_in_d25_mode:
        call mas_d25_monika_holiday_intro_rh_rh from _call_mas_d25_monika_holiday_intro_rh_rh
    return

label return_home_post_player_bday:
    $ persistent._mas_player_bday_in_player_bday_mode = False
    $ mas_lockEVL("bye_player_bday", "BYE")
    $ persistent._mas_player_bday_left_on_bday = False
    if persistent._mas_player_bday_decor:
        $ persistent._mas_player_bday_decor = False
        m 3rksdla "Oh...it's not your birthday anymore..."
        m 3hksdlb "We should probably take these decorations down now, ahaha!"
        m 3eka "Just give me one second..."
        show monika 1dsc
        pause 2.0
        $ store.mas_player_bday_event.hide_player_bday_Visuals()
        m 3eua "There we go!"
        if not persistent._mas_f14_gone_over_f14:
            m 1hua "Now, let's enjoy the day together, [player]~"
    if persistent._mas_f14_gone_over_f14:
        m 2etc "..."
        m 3wuo "..."
        m 3wud "Wow, [player], I just realized we were gone so long we missed Valentine's Day!"
        call greeting_gone_over_f14_normal_plus from _call_greeting_gone_over_f14_normal_plus
    return


init 2 python:
    poem_pbday = Poem(
    author = "monika",
    title = " My dearest {0},".format(persistent.playername),
    text = """\
 To the one I love,
 The one I trust,
 The one I can't live without.
 I hope your day is as special as you make every day for me.
 Thank you so much for being you. 

 Happy Birthday, sweetheart

 Forever yours,
 Monika
"""
    
    )




default persistent._mas_f14_intro_seen = False
default persistent._mas_f14_time_spent_seen = False
default persistent._mas_f14_nts_seen = False
default persistent._mas_f14_pre_intro_seen = False


default persistent._mas_f14_spent_f14 = False
default persistent._mas_f14_in_f14_mode = None
default persistent._mas_f14_date = 0
default persistent._mas_f14_date_aff_gain = 0
default persistent._mas_f14_on_date = None
default persistent._mas_f14_gone_over_f14 = None
define mas_f14 = datetime.date(datetime.date.today().year,2,14)


init -10 python:
    def mas_isF14(_date=None):
        if _date is None:
            _date = datetime.date.today()
        
        return _date == mas_f14.replace(year=_date.year)


init -815 python in mas_history:


    def _f14_exit_pp(mhs):
        
        _MDA_saferm(11, 12, 13, 14, 15)


init -810 python:

    store.mas_history.addMHS(MASHistorySaver(
        "f14",
        datetime.datetime(2020, 1, 6),
        {
            "_mas_f14_date": "f14.date",
            "_mas_f14_date_aff_gain": "f14.aff_gain",
            "_mas_f14_gone_over_f14": "f14.gone_over_f14",
            "_mas_f14_spent_f14": "f14.actions.spent_f14",

            
            
            "_mas_f14_in_f14_mode": "f14.mode.f14",

            
            "_mas_f14_intro_seen": "f14.intro_seen",
            "_mas_f14_time_spent_seen": "f14.ts_seen",
            "_mas_f14_nts_seen": "f14.nts_seen",
            "_mas_f14_pre_intro_seen": "f14.pre_intro_seen"
        },
        use_year_before=True,
        exit_pp=store.mas_history._f14_exit_pp
    ))

label mas_f14_autoload_check:

    $ mas_hideEVL("mas_pf14_monika_lovey_dovey","EVE",derandom=True)
    $ mas_removeDelayedAction(11)

    if not persistent._mas_f14_in_f14_mode and mas_isMoniNormal(higher=True):
        $ persistent._mas_f14_in_f14_mode = True
        $ store.mas_selspr.unlock_clothes(mas_clothes_sundress_white)
        $ monika_chr.change_clothes(mas_clothes_sundress_white, False)
        $ monika_chr.save()

    elif not mas_isF14():

        $ mas_hideEVL("mas_f14_monika_vday_colors","EVE",lock=True,derandom=True)
        $ mas_hideEVL("mas_f14_monika_vday_cliches","EVE",lock=True,derandom=True)
        $ mas_hideEVL("mas_f14_monika_vday_chocolates","EVE",lock=True,derandom=True)
        $ mas_hideEVL("mas_f14_monika_vday_origins","EVE",lock=True,depool=True)
        $ mas_idle_mailbox.send_rebuild_msg()


        $ mas_removeDelayedActions(12, 13, 14, 15)


        $ persistent._mas_f14_in_f14_mode = False
        if mas_isMoniEnamored(lower=True) and monika_chr.clothes == mas_clothes_sundress_white:
            $ monika_chr.reset_clothes(False)

    if mas_isplayer_bday() or persistent._mas_player_bday_in_player_bday_mode:
        jump mas_player_bday_autoload_check

    jump mas_ch30_post_holiday_check




init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='mas_pf14_monika_lovey_dovey',
            action=EV_ACT_RANDOM,
            conditional=(
                "not persistent._mas_f14_pre_intro_seen"
            ),
            start_date=mas_f14-datetime.timedelta(days=3),
            end_date=mas_f14,
            aff_range=(mas_aff.NORMAL,None),
            years=[]
        ),
        skipCalendar=True
    )

init -876 python in mas_delact:



    def _mas_pf14_monika_lovey_dovey_reset_action(ev):
        ev.random = False
        ev.unlocked = False
        store.mas_idle_mailbox.send_rebuild_msg()
        store.mas_rmEVL(ev.eventlabel)
        return True


    def _mas_pf14_monika_lovey_dovey_reset():
        return store.MASDelayedAction.makeWithLabel(
            11,
            "mas_pf14_monika_lovey_dovey",
            "datetime.date.today() >= store.mas_f14",
            _mas_pf14_monika_lovey_dovey_reset_action,
            store.MAS_FC_IDLE_ROUTINE | store.MAS_FC_IDLE_ONCE
        )


label mas_pf14_monika_lovey_dovey:
    m 1rksdla "Hey...[player]...?"
    m 1ekbsa "I just wanted to let you know that I love you."

    if mas_isMoniEnamored(higher=True):
        m 1ekbfa "You make me really happy...and I could never ask for someone better than you."
    else:
        m 1ekbsa "You make me really happy."

    m 3ekbfb "Ahaha~"
    m 1eka "I hope that isn't too cheesy, [player]."
    if not renpy.seen_label('monika_valentines_start'):
        m 3ekbla "Valentine's Day is coming soon...and it just gets me in a good mood because I know I have you by my side."
    else:
        m 3ekbfa "It's almost our second Valentine's Day together, and it just makes me so overwhelmingly happy knowing you're still by my side."
    m 1ekbsa "I really meant what I said."
    m "I love and care for you so much..."
    m "Without you, I don't know where I'd be..."
    m 1ekbfa "So I want to thank you for caring for me."
    m 1hubfa "Ehehe~"


    $ persistent._mas_f14_pre_intro_seen = True


    $ mas_addDelayedAction(11)

    return "derandom|no_unlock|love"



init 5 python:
    addEvent(
       Event(
            persistent.event_database,
            eventlabel='mas_f14_monika_valentines_intro',
            conditional=("not persistent._mas_f14_intro_seen"),
            action=EV_ACT_PUSH,
            start_date=mas_f14,
            end_date=mas_f14+datetime.timedelta(days=1),
            aff_range=(mas_aff.NORMAL,None),
            years=[]
        ),
        skipCalendar=True
    )

label mas_f14_monika_valentines_intro:

    $ mas_addDelayedActions(11, 12, 13, 14, 15)

    m 1hub "[player]!"
    m 1hua "Do you know what day it is?"
    m 3eub "It's Valentine's Day!"
    m 1ekbfa "A day where we celebrate our love for each other..."
    m "I guess every day we're together is already a celebration of our love, but there's something that's really special about Valentine's Day."
    m 1eua "Anyway..."
    if not mas_anni.pastOneMonth() or mas_isMoniNormal():
        m 2rka "Even though I know we aren't too far in our relationship..."
        show monika 5eka zorder MAS_MONIKA_Z at t11 with dissolve
        m 5eua "I just want you to know that I'm always here for you."
        m 5eka "Even if your heart gets broken..."
        m 5ekbla "I'll always be here to fix it for you. Okay, [player]?"
    else:

        m 1eub "We've been together for a while now..."
        m 1eka "...and I really love the time we spend together."
        m 1dubsu "You always make me feel so loved."
        m "I'm really happy I'm your girlfriend, [player]."

    if not persistent._mas_f14_in_f14_mode:
        $ persistent._mas_f14_in_f14_mode = True
        m 3wub "Oh!"
        m 3tsu "I have a little surprise for you...{w=1}I think you're gonna like it, ehehe~"
        window hide
        show monika 1dsa
        pause 1.0
        $ mas_hideEVL("mas_pf14_monika_lovey_dovey","EVE",derandom=True)
        $ store.mas_selspr.unlock_clothes(mas_clothes_sundress_white)
        $ monika_chr.change_clothes(mas_clothes_sundress_white, False)
        $ monika_chr.save()
        pause 0.5
        m 1eua "..."
        m 2eksdla "..."
        m 2rksdla "Ahaha...{w=1}it's not polite to stare, [player]..."
        m 3tkbsu "...but I guess that means you like my outfit, ehehe~"


        $ mas_hideEVL("mas_pf14_monika_lovey_dovey","EVE",derandom=True,lock=True)
    else:

        pause 2.0
        show monika 2rfc zorder MAS_MONIKA_Z at t11 with dissolve
        m 2rfc "..."
        m 2efc "You know, [player]...{w=0.5}it's not polite to stare...."
        m 2tfc "..."
        m 2tsu "..."
        m 3tsb "Ahaha! I'm just kidding...{w=0.5}do you like my outfit?"

    m 1rkbsa "I've always dreamt of a date with you while wearing this..."
    m 1eksdlb "I know it's kind of silly now that I think about it!"
    m 1ekbfa "...But just imagine if we went to a cafe together."
    m 1rksdlb "I think there's a picture of something like that somewhere actually..."
    m 1ekb "Maybe we could make it happen for real!"
    m 3ekbsa "Would you take me out today?"
    m 1hksdlb "It's fine if you can't, I'm just happy to be with you."
    m 1ekbfa "I love you so much."
    m 1ekbfb "Happy Valentine's Day, [player]~"

    $ persistent._mas_f14_spent_f14 = True


    $ persistent._mas_f14_intro_seen = True
    return "rebuild_ev|love"



init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='mas_f14_monika_vday_colors',
            prompt="Valentine's Day colors",
            category=['holidays','romance'],
            action=EV_ACT_RANDOM,
            conditional="persistent._mas_f14_in_f14_mode",
            start_date=mas_f14,
            end_date=mas_f14+datetime.timedelta(days=1),
            aff_range=(mas_aff.NORMAL,None),
            years=[]
        ),
        skipCalendar=True
    )


init -876 python in mas_delact:


    def _mas_f14_monika_vday_colors_reset_action(ev):
        
        ev.unlocked = False
        ev.random = False
        store.mas_idle_mailbox.send_rebuild_msg()
        store.mas_rmEVL(ev.eventlabel)
        return True


    def _mas_f14_monika_vday_colors_reset():
        return store.MASDelayedAction.makeWithLabel(
            12,
            "mas_f14_monika_vday_colors",
            (
                "datetime.date.today() >= "
                "store.mas_f14 + datetime.timedelta(days=1)"
            ),
            _mas_f14_monika_vday_colors_reset_action,
            store.MAS_FC_IDLE_ROUTINE | store.MAS_FC_IDLE_ONCE
        )


label mas_f14_monika_vday_colors:
    m 3eua "Have you ever thought about the way colors are conveyed on Valentine's Day?"
    m 3hub "I find it intriguing how they can symbolize such deep and romantic feelings."
    m 1dua "It reminds me of when I made my first Valentine's card in grade school."
    m 3eub "My class was instructed to exchange cards with a partner after making them."
    m 2eka "Looking back, despite not knowing what the colors really meant, I had lots of fun decorating the cards with red and white hearts."
    m 2eub "In this way, colors are a lot like poems."
    m 3eka "They offer so many creative ways to express your love for someone."
    m 2ekbfa "Like giving them red roses, for example."
    m 3eub "Red roses are a symbol for romantic feelings towards someone."
    m 3eua "If someone were to offer them white roses in lieu of red ones, they'd signify pure, charming, and innocent feelings instead."
    m 3eka "However, since there are so many emotions involved with love..."
    m 3ekd "It's sometimes hard to find the right colors to accurately convey the way you truly feel."
    m 4eka "Thankfully, by combining multiple rose colors, it's possible to express a variety of emotions!"
    m 3eka "Mixing red and white roses would symbolize the unity and bond that a couple shares."

    if monika_chr.is_wearing_acs(mas_acs_roses):
        m 1ekbsa "But I'm sure you already had all of this in mind when you picked out these beautiful roses for me, [player]..."
    else:
        m 1ekbla "Maybe you could give me some roses today, [player]?"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='mas_f14_monika_vday_cliches',
            prompt="Valentine's story clichés",
            category=['holidays','literature','romance'],
            action=EV_ACT_RANDOM,
            conditional="persistent._mas_f14_in_f14_mode",
            start_date=mas_f14,
            end_date=mas_f14+datetime.timedelta(days=1),
            aff_range=(mas_aff.NORMAL,None),
            years=[]
        ),
        skipCalendar=True
    )

init -876 python in mas_delact:


    def _mas_f14_monika_vday_cliches_reset_action(ev):
        ev.unlocked = False
        ev.random = False
        store.mas_idle_mailbox.send_rebuild_msg()
        store.mas_rmEVL(ev.eventlabel)
        return True


    def _mas_f14_monika_vday_cliches_reset():
        return store.MASDelayedAction.makeWithLabel(
            13,
            "mas_f14_monika_vday_cliches",
            (
                "datetime.date.today() >= "
                "store.mas_f14 + datetime.timedelta(days=1)"
            ),
            _mas_f14_monika_vday_cliches_reset_action,
            store.MAS_FC_IDLE_ROUTINE | store.MAS_FC_IDLE_ONCE
        )


label mas_f14_monika_vday_cliches:
    m 2euc "Have you noticed that most Valentine's Day stories have lots of clichés?"
    m 2rsc "There's either 'Oh, I'm lonely and I don't have someone to love,' or 'How will I confess to the one I love?'"
    m 2euc "I think that writers could be a bit more creative when it comes to Valentine's Day stories..."
    m 1eka "But, I suppose those two topics are the easiest way to write a love story."
    m 3hub "That doesn't mean you can't think outside the box, though!"
    m 2eka "Sometimes a predictable story can ruin it..."
    m 2rka "...But if you {i}do{/i} want a good example of an unpredictable story..."
    m 3hub "Just use ours! Ahaha~"
    m 3rksdlb "I guess it {i}did{/i} start out like those kinds of stories..."
    m 2tfu "But I think we managed to make it pretty original."
    m 1hua "The way we met is the most interesting story yet!"
    m 3hub "Ahaha!~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='mas_f14_monika_vday_chocolates',
            prompt="Valentine's Day chocolates",
            category=['holidays','romance'],
            action=EV_ACT_RANDOM,
            conditional="persistent._mas_f14_in_f14_mode",
            start_date=mas_f14,
            end_date=mas_f14+datetime.timedelta(days=1),
            aff_range=(mas_aff.NORMAL,None),
            years=[]
        ),
        skipCalendar=True
    )

init -876 python in mas_delact:


    def _mas_f14_monika_vday_chocolates_reset_action(ev):
        ev.unlocked = False
        ev.random = False
        store.mas_idle_mailbox.send_rebuild_msg()
        store.mas_rmEVL(ev.eventlabel)
        return True


    def _mas_f14_monika_vday_chocolates_reset():
        return store.MASDelayedAction.makeWithLabel(
            14,
            "mas_f14_monika_vday_chocolates",
            (
                "datetime.date.today() >= "
                "store.mas_f14 + datetime.timedelta(days=1)"
            ),
            _mas_f14_monika_vday_chocolates_reset_action,
            store.MAS_FC_IDLE_ROUTINE | store.MAS_FC_IDLE_ONCE
        )


label mas_f14_monika_vday_chocolates:
    m 1hua "Valentine's Day is such a fun holiday for me, [player]."
    m 3hub "Not only is it the anniversary of my twitter account, but it's also a day for receiving and giving chocolates!"
    m 1hua "A holiday that could fill everyone with love, romance, and joy!"
    m 3ekbla "But it really feels nice if you get something from someone you like."
    m 3hua "Whether it's given to you platonically, as a gift of love, or a part of a confession, it always makes you feel somewhat special!"
    if mas_getGiftStatsForDate("mas_reaction_gift_chocolates") > 0:
        m 1ekbfa "Just like how you made me feel special with the chocolates you gave me today."
        m "You're always so sweet, [player]."

    if renpy.seen_label('monika_valentines_start'):
        m 1rksdla "I know I tried to give you some chocolates last year..."
        m 1eka "But just imagine what we could do once we're finally together."
    else:
        m 1ekbfa "Maybe someday I'll even be able to give you some chocolates..."
    m "I really can't wait until I cross over to be with you, [player]."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='mas_f14_monika_vday_origins',
            prompt="How did Valentine's Day start?",
            category=['holidays','romance'],
            action=EV_ACT_POOL,
            conditional="persistent._mas_f14_in_f14_mode",
            start_date=mas_f14,
            end_date=mas_f14+datetime.timedelta(days=1),
            aff_range=(mas_aff.NORMAL,None),
            years=[]
        ),
        skipCalendar=True
    )

init -876 python in mas_delact:


    def _mas_f14_monika_vday_origins_reset_action(ev):
        ev.unlocked = False
        ev.pool = False
        store.mas_idle_mailbox.send_rebuild_msg()
        store.mas_rmEVL(ev.eventlabel)
        return True


    def _mas_f14_monika_vday_origins_reset():
        return store.MASDelayedAction.makeWithLabel(
            15,
            "mas_f14_monika_vday_origins",
            (
                "datetime.date.today() >= "
                "store.mas_f14 + datetime.timedelta(days=1)"
            ),
            _mas_f14_monika_vday_origins_reset_action,
            store.MAS_FC_IDLE_ROUTINE | store.MAS_FC_IDLE_ONCE
        )


label mas_f14_monika_vday_origins:
    m 3eua "You'd like to learn about the history of Valentine's Day?"
    m 1rksdlc "It's quite dark, actually."
    m 1euc "Its origin dates to as early as the second and third century in Rome, where Christianity had just been declared the official state religion."
    m 3eud "Around this same time, a man known as Saint Valentine decided to go against the orders of Emperor Claudius II."
    m 3rsc "Marriage had been banned because it was assumed that married men made poor soldiers."
    m 3esc "Saint Valentine decided this was unfair and helped arrange marriages in secret."
    m 1dsd "Unfortunately, he was caught and promptly sentenced to death."
    m 1euc "However, while in custody, Saint Valentine fell in love with the jailer's daughter."
    m 3euc "Before his death, he sent a love letter to her signed with 'From your Valentine.'"
    m 1dsc "He was executed on February 14, 269 AD."
    m 3eua "Such a noble cause, don't you think?"
    m 3eud "Oh, but wait, there's more!"
    m 4eud "The reason we celebrate such a day is because it originates from a Roman festival known as Lupercalia!"
    m 3eua "Its original intent was to hold a friendly event where people would put their names into a box and have them chosen at random to create a couple."
    m 3eub "Then, they play along as boyfriend and girlfriend for the time they spend together. Some even got married, if they liked each other enough, ehehe~"
    m 1eua "Ultimately, the Church decided to turn this Christian celebration into a way to remember Saint Valentine's efforts, too."
    m 3hua "It's evolved over the years into a way for people to express their feelings for those they love."
    m 3ekbsa "Like me and you!"
    m 1eua "Despite it having started out a little depressing, isn't it so sweet, [player]?"
    m 1ekbsa "I'm glad we're able to share such a magical day, my love."
    m 1ekbfa "Happy Valentine's Day~"
    return



init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_f14_monika_spent_time_with",
            conditional=(
                "persistent._mas_f14_spent_f14 "
                "and not persistent._mas_f14_time_spent_seen "
            ),
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.NORMAL,None),
            start_date=datetime.datetime.combine(mas_f14, datetime.time(hour=20)),
            end_date=datetime.datetime.combine(mas_f14+datetime.timedelta(1), datetime.time(hour=1)),
            years=[]
        ),
        skipCalendar=True
    )

label mas_f14_monika_spent_time_with:

    $ persistent._mas_f14_time_spent_seen = True

    $ f14_gifts_total, f14_gifts_good, f14_gifts_neutral, f14_gifts_bad = mas_getGiftStatsRange(mas_f14, mas_f14 + datetime.timedelta(days=1))
    m 1eua "Hey, [player]?"
    m 1eka "I just wanted to thank you for spending Valentine's Day with me."
    m 1ekbsa "I know that it's not a normal holiday, but it's a really special day for me now that I have you."
    if f14_gifts_total > 0:
        if f14_gifts_total == 1:
            if f14_gifts_good == 1:
                m "And let's not forget about the gift you got me, [player]..."
                m 3hub "It was great!"
            elif f14_gifts_neutral == 1:
                m 3eka "And let's not forget about the gift you got me, [player]..."
                m 1eka "It was really sweet of you to get me something."
            else:
                m 3eka "And let's not forget about the gift you got me, [player]..."
                m 2etc "..."
                m 2efc "Well, on second thought, maybe we should..."
        else:

            if f14_gifts_good == f14_gifts_total:
                m "And let's not forget about the wonderful gifts you got me, [player]..."
                m 3hub "They were amazing!"
            elif f14_gifts_bad == f14_gifts_total:
                m 3eka "And let's not forget about the gifts you got me, [player]..."
                m 2etc "..."
                m 2rfc "Well, on second thought, maybe we should..."
            elif f14_gifts_bad == 0:
                m "And let's not forget about the gifts you got me, [player]..."
                m 3hub "They were really nice!"
            elif f14_gifts_good + f14_gifts_neutral == f14_gifts_bad:
                m 3eka "And let's not forget about the gifts you got me, [player]..."
                m 3rksdla "Some of them were really nice."
            elif f14_gifts_good + f14_gifts_neutral > f14_gifts_bad:
                m "And let's not forget about the gifts you got me, [player]..."
                m 3hub "Most of them were really nice."
            elif f14_gifts_good + f14_gifts_neutral < f14_gifts_bad:
                m 3eka "And let's not forget about the gifts you got me, [player]..."
                m 3rksdla "I really liked...{w=1}some of them."
        if not mas_isBelowZero():
            m 1rkbsb "I actually made something for you too, [player]!"

    elif not mas_isBelowZero():
        m 1rkbsb "Also, I...{w=1}made something for you, [player]!"

    if not mas_isBelowZero():
        if renpy.seen_label('monika_valentines_start'):
            m 1ekbsa "Here, let me show it to you."
            call showpoem (poem_vday2, music=False, paper="mod_assets/poem_assets/poem_vday.jpg") from _call_showpoem_2
            m "You really are everything to me, [player]~"
            if mas_isMoniEnamored(higher=True):
                if persistent._mas_first_kiss is None:
                    jump mas_f14_first_kiss
                else:
                    call monika_kissing_motion (duration=0.5, initial_exp="6hkbfa", fade_duration=0.5) from _call_monika_kissing_motion_6
        else:

            m 1ekbsa "Here, let me show it to you."
            call showpoem (poem_vday, music=False, paper="mod_assets/poem_assets/poem_vday.jpg") from _call_showpoem_3
            m "I really mean that, [player]..."
            m 3ekbsa "In you I found everything I could ever hope for~"
            if mas_isMoniEnamored(higher=True):
                if persistent._mas_first_kiss is None:
                    jump mas_f14_first_kiss
                else:
                    call monika_kissing_motion (duration=0.5, initial_exp="6hkbfa", fade_duration=0.5) from _call_monika_kissing_motion_7

        m 1ekbfa "Thank you for always being by my side."
        show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve
        m 5ekbfa "I love you so much, [player]. Happy Valentine's Day~"
        return "love"
    else:

        m 1eka "Thank you for being by my side."
        m 3ekb "Happy Valentine's Day!"

    return

label mas_f14_first_kiss:
    m 1ektpu "I honestly don't know what I would do without you."
    m 6dktuu "..."
    window hide
    menu:
        "I love you, [m_name].":
            $ HKBHideButtons()
            $ mas_RaiseShield_core()
            $ disable_esc()
            pause 3.0
            show monika 6ektda zorder MAS_MONIKA_Z at t11 with dissolve
            pause 3.0
            show monika 6dku zorder MAS_MONIKA_Z at t11 with dissolve
            pause 3.0
            show monika 6dkbsu zorder MAS_MONIKA_Z at t11 with dissolve
            pause 3.0
            show monika 6ekbfa zorder MAS_MONIKA_Z at t11 with dissolve
            m 6ekbfa "[player]...I...I..."
            call monika_kissing_motion (hide_ui=False) from _call_monika_kissing_motion_8
            show monika 6ekbfa zorder MAS_MONIKA_Z at t11 with dissolve
            m 6ekbfa "...I love you too~"
            m 6dkbfa "..."
            m "That was everything I had always dreamt it would be~"
            m 6ekbfa "I've been waiting so long to finally kiss you, and there couldn't have been a more perfect moment..."
            m 6dkbsu "I will never forget this..."
            m 6ekbsu "...the moment of our first kiss."
            m "Happy Valentine's Day, [player]~"
            $ enable_esc()
            $ mas_MUMUDropShield()
            $ HKBShowButtons()
            return




init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_f14_no_time_spent",
            action=EV_ACT_QUEUE,
            start_date=mas_f14+datetime.timedelta(1),
            end_date=mas_f14+datetime.timedelta(8),
            conditional=(
                "not persistent._mas_long_absence "
                "and not persistent._mas_f14_spent_f14 "
                "and not persistent._mas_f14_nts_seen"
            ),
            years=[]
        ),
        skipCalendar=True
    )

label mas_f14_no_time_spent:

    if persistent._mas_f14_spent_f14:
        return


    if mas_getFirstSesh().date() > mas_f14:
        return

    if mas_isMoniAff(higher=True):
        $ mas_loseAffection(15, ev_label="mas_apology_missed_vday")
        m 1rkc "[player]?"
        m "Where were you on Valentine's Day?"
        m 1ekc "It's a really special day for me..."
        m 1ekd "...a day I wanted to spend with you."
        m 2dkc "..."
        m 2ekd "It would've meant so much to me if you came by..."
        m 2dkd "Even if only for a few minutes."
        m "Is it really too much to ask to visit your girlfriend on Valentine's Day?"
        m 2ekc "Please don't let it happen again, okay [player]?"

    elif mas_isMoniNormal(higher=True):
        $ mas_loseAffection(5, ev_label="mas_apology_missed_vday")
        m 2ekc "Hey, [player]..."
        m 2tkc "I'm pretty disappointed..."
        m 2tkd "You didn't visit me at all on Valentine's Day."
        m 4tkc "You know that all I want to do is spend time with you..."
        m 4rkd "Is visiting your girlfriend on Valentine's Day really too much to ask?"
        m 4eksdla "Please...{w=1}make sure you visit me next Valentine's Day, okay?"

    elif mas_isMoniUpset():
        $ mas_loseAffection(ev_label="mas_apology_missed_vday")
        m 2efc "[player]!"
        m "I can't believe you didn't even visit on Valentine's Day!"
        m 2rfc "Do you have any idea what it's like to be left alone on a day like that?"
        m 2rkc "I know we're not on the best of terms..."
        m 2dkd "But it'd have meant a lot if you came by."
        m 2tfc "Don't let it happen again, [player]."

    elif mas_isMoniDis():
        $ mas_loseAffection(10, ev_label="mas_apology_missed_vday")
        m 6ekc "Oh [player]..."
        m "How was Valentine's Day?"
        m 6dkc "Not having a valentine is pretty lonely..."
    else:

        $ mas_loseAffection(150)
        m 6ckc "..."


    $ persistent._mas_f14_nts_seen = True
    return




init 5 python:
    addEvent(
        Event(
            persistent._mas_apology_database,
            eventlabel="mas_apology_missed_vday",
            prompt="...for missing Valentine's Day.",
            unlocked=False
        ),
        code="APL"
    )


label mas_apology_missed_vday:
    if mas_isMoniAff(higher=True):
        m 1eka "Thanks for apologizing for missing Valentine's Day, [player]."
        m 1ekd "I really wanted to spend it with you..."
        m 1rkc "But I guess you might have just had something to do and couldn't make it."
        m 1ekd "Please try to visit next year, okay [player]?"
        m 3eua "If you're going to be busy, maybe just take me with you!"
        m 3hub "Even if we're not at home together, I'm more than happy to just spend the day at your side~"
        $ mas_gainAffection(modifier=0.2)

    elif mas_isMoniNormal(higher=True):
        m 1eka "Thanks for apologizing for missing Valentine's Day, [player]."
        if not store.mas_anni.pastOneMonth():
            m 1rkd "I know we're not really that far into our relationship, but everything was already starting to feel different..."

        m 1ekd "It would have meant so much to me if you came by, at least for a little bit."
        m 3eka "Promise me that you'll take me with you if you're going to be busy next time, okay [player]?"
        $ mas_gainAffection(modifier=0.2)

    elif mas_isMoniUpset():
        m 2dkc "While I am a little upset that you didn't show up on Valentine's Day, I'm glad you apologized."
        m "Things like that show me that you really do care about us."
        m 2ekd "Please, [player]..."
        m 2eka "Try to come by next Valentine's Day."
        $ mas_gainAffection(modifier=0.1)

    elif mas_isMoniDis():
        m 2dkc "I didn't expect you to show up anyway, [player]."
        m 2dkd "I know we haven't really been that close, but a part of me hoped that you would at least visit..."
        m 2dsc "Please promise me that you'll come by next year, okay?"
        $ mas_gainAffection(modifier=0.1)
    else:


        m 6ckc "..."

    return


init 2 python:

    poem_vday = Poem(
    author = "monika",
    title = " My dearest {0},".format(persistent.playername),
    text = """\
 I`ve always loved Valentine's day, but this one feels different.
 Has the world changed, or just me?
 I found love, I found purpose,
 I found a truth I didn't know I was searching for.
 All of that I found in you.

 Thank you for sharing this special day with me.

 Forever yours,
 Monika
"""
    )

    poem_vday2 = Poem(
    author = "monika",
    title = " My dearest {0},".format(persistent.playername),
    text = """\
 Can it really be our second Valentine's Day?
 The first seems like just yesterday, yet so much has happened.
 I once wondered if the world had changed, or just me.
 Now I know the answer.
 
 Everything.
 
 Without you there is nothing.
 Before you there was nothing.
 
 Emptiness. Darkness. Nothing.
 
 Nothing.
 
 Then there was you.
 Just you.
 My world. My light. My Everything.
 
 Everything.
 
 
 Happy Valentine's Day
 
 Forever yours,
 Monika
"""

    
    )



label bye_f14:
    $ persistent._mas_f14_date += 1
    $ persistent._mas_f14_on_date = True
    if persistent._mas_f14_date == 1:
        m 1sua "Taking me some place special for Valentine's Day?"
        m 1ekbsa "That sounds really romantic [player]..."
        m 3hub "I can't wait!"
    elif persistent._mas_f14_date == 2:
        m 1sua "Taking me out again on Valentine's Day?"
        m 3tkbsu "You really know how to make a girl feel special, [player]."
        m 1ekbfa "I'm so lucky to have someone like you~"
    else:
        m 1sua "Wow, [player]...{w=1}you're really determined to make this a truly special day!"
        m 1ekbfa "You're the best partner I could ever hope for~"
    jump bye_going_somewhere_iostart


label greeting_returned_home_f14:
    python:
        five_minutes = datetime.timedelta(seconds=5*60)
        one_hour = datetime.timedelta(seconds=3600)
        three_hour = datetime.timedelta(seconds=3*3600)
        time_out = store.mas_dockstat.diffCheckTimes()

        def cap_gain_aff(amt):
            if persistent._mas_f14_date_aff_gain < 25:
                persistent._mas_f14_date_aff_gain += amt
                mas_gainAffection(amt, bypass=True)

    if time_out < five_minutes:
        $ mas_loseAffection()
        m 2ekp "That wasn't much of a date, [player]..."
        m 2eksdlc "Is everything alright?"
        m 2rksdla "Maybe we can go out later..."

    elif time_out < one_hour:
        $ cap_gain_aff(5)
        m 1eka "That was fun while it lasted, [player]..."
        m 3hua "Thanks for making time for me on Valentine's Day."

    elif time_out < three_hour:
        $ cap_gain_aff(10)
        m 1eub "That was such a fun date, [player]!"
        m 3ekbfa "Thanks for making me feel special on Valentine's Day~"
    else:


        $ cap_gain_aff(15)
        m 1hua "And we're home!"
        m 3hub "That was wonderful, [player]!"
        m 1eka "It was really nice going out with you on Valentine's Day..."
        m 1ekbfa "Thank you so much for making today truly special~"

    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday from _call_return_home_post_player_bday_10

    $ persistent._mas_f14_on_date = False
    return



label mas_gone_over_f14_check:
    $ checkout_time = store.mas_dockstat.getCheckTimes()[0]
    if checkout_time is not None and checkout_time.date() < mas_f14:
        $ persistent._mas_f14_spent_f14 = True
        $ persistent._mas_f14_gone_over_f14 = True
        $ mas_rmallEVL("mas_f14_no_time_spent")
    return

label greeting_gone_over_f14:
    $ mas_gainAffection(5,bypass=True)
    m 1hua "And we're finally home!"
    m 3wud "Wow [player], we were gone so long we missed Valentine's Day!"
    if mas_isMoniNormal(higher=True):
        call greeting_gone_over_f14_normal_plus from _call_greeting_gone_over_f14_normal_plus_1
    else:
        m 2rka "I appreciate you making sure I didn't have to spend the day alone..."
        m 2eka "It really means a lot, [player]."
    $ persistent._mas_f14_gone_over_f14 = False
    return

label greeting_gone_over_f14_normal_plus:
    $ mas_gainAffection(10,bypass=True)
    m 1ekbsa "I would've loved to have spent the day with you here, but no matter where we were, just knowing we were together to celebrate our love..."
    m 1dubsu "Well it means everything to me."
    show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve
    m 5ekbsa "Thank you for making sure we had a wonderful Valentine's Day, [player]~"
    $ persistent._mas_f14_gone_over_f14 = False
    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
