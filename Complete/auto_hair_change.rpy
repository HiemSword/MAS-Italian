

init 999 python:
    #Reset force hair, so we can have Moni set her own hair next sesh
    renpy.game.persistent._mas_force_hair = False

    #Override this label so we always end up here when taking Monika somewhere
    config.label_overrides["bye_going_somewhere_post_aff_check"] = "bye_going_somewhere_post_aff_check_override"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sethair_ponytail",
            conditional=(
                "mas_isMorning() "
                "and monika_chr.hair != store.mas_hair_def "
                "and (monika_chr.clothes != store.mas_clothes_marisa and monika_chr.clothes != store.mas_clothes_rin) "
                "and not store.persistent._mas_force_hair "
            ),
            action=EV_ACT_QUEUE,
            show_in_idle=True,
            rules={"skip alert": None}
        )
    )

label monika_sethair_ponytail:
    if store.mas_globals.in_idle_mode or (mas_canCheckActiveWindow() and not mas_isFocused()):
        m 3eua "Mi sto preparando per la giornata.{w=0.5}.{w=0.5}.{w=2}{nw}"

    else:
        m 1eua "Aspetta un attimo, [player]."
        m 2dsa "Mi sto preparando per la giornata che ci aspetta.{w=0.5}.{w=0.5}.{nw}"

    # this should auto lock/unlock stuff
    $ monika_chr.change_hair(mas_hair_def,by_user=False)

    if store.mas_globals.in_idle_mode or (mas_canCheckActiveWindow() and not mas_isFocused()):
        m 3hub "Fatto!{w=1}{nw}"

    else:
        m 3hub "Fatto!"
        m 1eua "Se vuoi che mi rimetta come prima, basta chiedere, okay?" #DA SISTEMARE

    #Need to recondition/action this
    python:
        hairup_ev = mas_getEV("monika_sethair_ponytail")

        hairup_ev.conditional=(
                "mas_isMorning() "
                "and monika_chr.hair != store.mas_hair_def "
                "and (monika_chr.clothes != store.mas_clothes_marisa and monika_chr.clothes != store.mas_clothes_rin) "
                "and not store.persistent._mas_force_hair "
            )
        hairup_ev.action = EV_ACT_QUEUE
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sethair_down",
            conditional=(
                "not mas_isMorning() "
                "and monika_chr.hair != store.mas_hair_down "
                "and (monika_chr.clothes != store.mas_clothes_marisa and monika_chr.clothes != store.mas_clothes_rin) "
                "and not store.persistent._mas_force_hair "
            ),
            action=EV_ACT_QUEUE,
            show_in_idle=True,
            rules={"skip alert": None}
        )
    )

label monika_sethair_down:
    if store.mas_globals.in_idle_mode or (mas_canCheckActiveWindow() and not mas_isFocused()):
        m 2dsa "Mi sto sistemandoper la giornata.{w=0.5}.{w=0.5}.{w=2}{nw}"
    else:
        m 2dsa "Un secondo [player], Mi sto sistemando.{w=0.5}.{w=0.5}.{nw}"

    $ monika_chr.change_hair(mas_hair_down,by_user=False)

    if store.mas_globals.in_idle_mode or (mas_canCheckActiveWindow() and not mas_isFocused()):
        m "Molto meglio.{w=1}{nw}"

    else:
        m 1eua "Molto meglio."
        if not renpy.has_label('monika_welcome_home'):
            show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve
            m 5eua "Possiamo continuare la nostra serata insieme, [player]." #da sistemare

        else:
            show monika 5hua at t11 zorder MAS_MONIKA_Z with dissolve

        m 5hua "Se desideri che cambi acconciatura, basta chiedere~"


    #Need to recondition/action this
    python:
        hairdown_ev = mas_getEV("monika_sethair_down")

        hairdown_ev.conditional=(
                "not mas_isMorning() "
                "and monika_chr.hair != store.mas_hair_down "
                "and (monika_chr.clothes != store.mas_clothes_marisa and monika_chr.clothes != store.mas_clothes_rin) "
                "and not store.persistent._mas_force_hair "
            )
        hairdown_ev.action = EV_ACT_QUEUE
    return

#START: Overridden labels
#NOTE: We only override the post_aff_check because it falls through to the rest rather than jumps/calls
label bye_going_somewhere_post_aff_check_override:

    # event based
    if mas_isMonikaBirthday():
        m 1hua "Ehehe. E' un pò romantico, vero?"
        m 1eua "Forse potresti chiamarlo a da-{nw}"
        $ _history_list.pop()
        $ _history_list.pop()
        m 1hua "Oh! Scusa, ho detto qualcosa?"

    if mas_isO31():
        m 1wub "Oh! Andiamo a fare dolcetto-o-scherzetto, [player]?{nw}" #da sistemare
        $ _history_list.pop()
        menu:
            m "Oh! Andiamo a fare dolcetto-o-scherzetto, [player]?{fast}"
            "Si.":
                jump bye_trick_or_treat

            "No.":
                m 2ekp "Oh, okay."


label bye_going_somewhere_iostart_override:
    # NOTE: jump back to this label to begin io generation

    show monika 2dsc
    $ persistent._mas_dockstat_going_to_leave = True
    $ first_pass = True

    # launch I/O thread
    $ promise = store.mas_dockstat.monikagen_promise
    $ promise.start()

label bye_going_somewhere_iowait_override:
    hide screen mas_background_timed_jump

    # we want to display the menu first to give users a chance to quit
    if first_pass:
        $ first_pass = False

    elif promise.done():
        # i/o thread is done!

        #Make sure hair is up for when we leave
        $ monika_chr.change_hair(mas_hair_def, by_user=False)

        #We'll wear a ribbon if it's a special day
        if mas_isSpecialDay():
            $ monika_chr.wear_acs(mas_acs_ribbon_def)
        jump bye_going_somewhere_rtg
    else:
        #clean up the history list so only one "give me a second..." should show up
        $ _history_list.pop()

    # display menu options
    # 4 seconds seems decent enough for waiting.
    show screen mas_background_timed_jump(4, "bye_going_somewhere_iowait_override")
    menu:
        m "Dammi un secondo per prepararmi.{fast}"
        "Aspetta, aspetta!":
            hide screen mas_background_timed_jump
            $ persistent._mas_dockstat_cm_wait_count += 1

    # fall thru to the wait wait flow
    show monika 1ekc
    menu:
        m "Cosa c'è?"
        "Non posso portarti in questo momento.":
            call mas_dockstat_abort_gen
            jump bye_going_somewhere_leavemenu

        "Niente.":
            # if we get here, we should jump back to the top so we can
            # continue waiting
            m 2hub "Oh, perfetto! Finisco di prepararmi."

    # by default, continue looping
    jump bye_going_somewhere_iowait_override
