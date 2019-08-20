###########################################
###  Traslated in italian by Moon595  ###
###########################################


init offset = 5


default -5 persistent._mas_enable_notifications = False


default -5 persistent._mas_notification_sounds = True


default -5 persistent._mas_windowreacts_windowreacts_enabled = False


default -5 persistent._mas_windowreacts_database = dict()


default -5 persistent._mas_windowreacts_no_unlock_list = list()


default -5 persistent._mas_windowreacts_notif_filters = dict()

init -15 python in mas_windowreacts:

    can_show_notifs = True


    windowreact_db = {}




    _groups_list = [
        "Topic Alerts",
        "Window Reactions",
    ]

init -5 python:
    import os



    if renpy.windows:
        
        import sys
        sys.path.append(renpy.config.gamedir + '\\python-packages\\')
        
        
        try:
            
            import win32gui
            
            import win32api
        
        except ImportError:
            
            store.mas_windowreacts.can_show_notifs = False
            
            
            store.mas_utils.writelog(
                "[WARNING]: win32api/win32gui failed to be imported, disabling notifications.\n"
            )
        
        
        
        else:
            import balloontip
            
            
            tip = balloontip.WindowsBalloonTip()
            
            
            tip.hwnd = None



    mas_win_notif_quips = [
        "[player], Ti voglio parlare di qualcosa",
        "Ci sei, [player]?",
        "puoi venire un attimo?",
        "[player], hai un secondo?",
        "Ho qualcosa da dirti, [player]!",
        "Hai un minuto, [player]?",
        "Ho qualcosa di cui parlare, [player]!",
    ]


    mas_other_notif_quips = [
        "Ho qualcosa di cui parlarti, [player]!",
        "Ho qualcosa da dirti, [player]!",
        "Hey [player],Voglio dirti qualcosa.",
        "Hai un minuto, [player]?",
    ]


    destroy_list = list()


    def mas_canCheckActiveWindow():
        """
        Checks if we can check the active window (simplifies conditionals)
        """
        return persistent._mas_windowreacts_windowreacts_enabled or persistent._mas_enable_notifications

    def mas_getActiveWindow(friendly=False):
        """
        Gets the active window name
        IN:
            friendly: whether or not the active window name is returned in a state usable by the user
        """
        if (
                renpy.windows
                and mas_windowreacts.can_show_notifs
                and mas_canCheckActiveWindow()
            ):
            from win32gui import GetWindowText, GetForegroundWindow
            
            if not friendly:
                return GetWindowText(GetForegroundWindow()).lower().replace(" ","")
            else:
                return GetWindowText(GetForegroundWindow())
        else:
            
            
            return ""

    def mas_isFocused():
        """
        Checks if MAS is the focused window
        """
        
        return store.mas_windowreacts.can_show_notifs and mas_getActiveWindow(True) == config.name

    def mas_isInActiveWindow(keywords, non_inclusive=False):
        """
        Checks if ALL keywords are in the active window name
        IN:
            keywords:
                List of keywords to check for

            non_inclusive:
                Whether or the not the list is checked non-inclusively
                (Default: False)
        """
        
        
        if not store.mas_windowreacts.can_show_notifs:
            return False
        
        
        active_window = mas_getActiveWindow()
        
        if non_inclusive:
            return len([s for s in keywords if s.lower() in active_window]) > 0
        else:
            return len([s for s in keywords if s.lower() not in active_window]) == 0

    def mas_clearNotifs():
        """
        Clears all tray icons (also action center on win10)
        """
        if renpy.windows and store.mas_windowreacts.can_show_notifs:
            for index in range(len(destroy_list)-1,-1,-1):
                win32gui.DestroyWindow(destroy_list[index])
                destroy_list.pop(index)

    def mas_checkForWindowReacts():
        """
        Runs through events in the windowreact_db to see if we have a reaction, and if so, queue it
        """
        
        if not persistent._mas_windowreacts_windowreacts_enabled or not store.mas_windowreacts.can_show_notifs:
            return
        
        for ev_label, ev in mas_windowreacts.windowreact_db.iteritems():
            if (
                    (mas_isInActiveWindow(ev.category, "non inclusive" in ev.rules) and ev.unlocked and ev.checkAffection(mas_curr_affection))
                    and ((not store.mas_globals.in_idle_mode) or (store.mas_globals.in_idle_mode and ev.show_in_idle))
                    and ("notif-group" not in ev.rules or mas_notifsEnabledForGroup(ev.rules.get("notif-group")))
                ):
                
                if ev.conditional and eval(ev.conditional):
                    queueEvent(ev_label)
                    ev.unlocked=False
                
                
                elif not ev.conditional:
                    queueEvent(ev_label)
                    ev.unlocked=False
                
                
                if "no unlock" in ev.rules:
                    mas_addBlacklistReact(ev_label)

    def mas_resetWindowReacts(excluded=persistent._mas_windowreacts_no_unlock_list):
        """
        Runs through events in the windowreact_db to unlock them
        IN:
            List of ev_labels to exclude from being unlocked
        """
        for ev_label, ev in mas_windowreacts.windowreact_db.iteritems():
            if ev_label not in excluded:
                ev.unlocked=True

    def mas_updateFilterDict():
        """
        Updates the filter dict with the groups in the groups list for the settings menu
        """
        for group in store.mas_windowreacts._groups_list:
            if persistent._mas_windowreacts_notif_filters.get(group) is None:
                persistent._mas_windowreacts_notif_filters[group] = False

    def mas_addBlacklistReact(ev_label):
        """
        Adds the given ev_label to the no unlock list
        IN:
            ev_label: eventlabel to add to the no unlock list
        """
        if renpy.has_label(ev_label) and ev_label not in persistent._mas_windowreacts_no_unlock_list:
            persistent._mas_windowreacts_no_unlock_list.append(ev_label)

    def mas_removeBlacklistReact(ev_label):
        """
        Removes the given ev_label to the no unlock list if exists
        IN:
            ev_label: eventlabel to remove from the no unlock list
        """
        if renpy.has_label(ev_label) and ev_label in persistent._mas_windowreacts_no_unlock_list:
            persistent._mas_windowreacts_no_unlock_list.remove(ev_label)

    def mas_notifsEnabledForGroup(group):
        """
        Checks if notifications are enabled, and if enabled for the specified group
        IN:
            group: notification group to check
        """
        return persistent._mas_enable_notifications and persistent._mas_windowreacts_notif_filters.get(group,False)

    def mas_unlockFailedWRS(ev_label=None):
        """
        Unlocks a wrs again provided that it showed, but failed to show (failed checks in the notif label)
        NOTE: This should only be used for wrs that are only a notification
        IN:
            ev_label: eventlabel of the wrs
        """
        if (
                ev_label
                and renpy.has_label(ev_label)
                and ev_label not in persistent._mas_windowreacts_no_unlock_list
            ):
            mas_unlockEVL(ev_label,"WRS")

    def mas_tryShowNotificationOSX(title, body):
        """
        Tries to push a notification to the notification center on macOS.
        If it can't it should fail silently to the user.
        IN:
            title: notification title
            body: notification body
        """
        os.system('osascript -e \'display notification "{0}" with title "{1}"\''.format(body,title))

    def mas_tryShowNotificationLinux(title, body):
        """
        Tries to push a notification to the notification center on Linux.
        If it can't it should fail silently to the user.
        IN:
            title: notification title
            body: notification body
        """
        os.system("notify-send '{0}' '{1}' -u low".format(title,body))

    def display_notif(title, body, group=None, skip_checks=False):
        """
        Notification creation method
        IN:
            title: Notification heading text
            body: A list of items which would go in the notif body (one is picked at random)
            group: Notification group (for checking if we have this enabled)
            skip_checks: Whether or not we skips checks
        OUT:
            bool indicating status (notif shown or not (by check))
        NOTE:
            We only show notifications if:
                1. We are able to show notifs
                2. MAS isn't the active window
                3. User allows them
                4. And if the notification group is enabled
                OR if we skip checks. BUT this should only be used for introductory or testing purposes.
        """
        
        
        if persistent._mas_windowreacts_notif_filters.get(group) is None and not skip_checks:
            persistent._mas_windowreacts_notif_filters[group] = False
        
        if (
                (
                    mas_windowreacts.can_show_notifs
                    and ((renpy.windows and not mas_isFocused()) or not renpy.windows)
                    and mas_notifsEnabledForGroup(group)
                )
                or skip_checks
            ):
            
            
            if persistent._mas_notification_sounds:
                renpy.sound.play("mod_assets/sounds/effects/notif.wav")
            
            
            if (renpy.windows):
                
                tip.showWindow(renpy.substitute(title), renpy.substitute(renpy.random.choice(body)))
                
                
                destroy_list.append(tip.hwnd)
            
            elif (renpy.macintosh):
                
                mas_tryShowNotificationOSX(renpy.substitute(title), renpy.substitute(renpy.random.choice(body)))
            
            elif (renpy.linux):
                
                mas_tryShowNotificationLinux(renpy.substitute(title), renpy.substitute(renpy.random.choice(body)))
            
            return True
        return False



init python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_pinterest",
            category=['pinterest'],
            rules={"notif-group": "Window Reactions", "skip alert": None},
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_pinterest:
    $ wrs_success = display_notif(
        m_name,
        [
            "Qualche novità, [player]?",
            "Qualcosa di interessante, [player]?",
            "Vedi qualcosa che ti piace?"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_pinterest')
    return

init python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_duolingo",
            category=['duolingo'],
            rules={"notif-group": "Window Reactions", "skip alert": None},
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_duolingo:
    $ wrs_success = display_notif(
        m_name,
        [
            "Imparando nuovi modi per dire 'ti amo', [player]?",
            "Imparando una nuova lingua, [player]?",
            "Che lingua stai imparando, [player]?"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_duolingo')
    return

init python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_wikipedia",
            category=['wikipedia'],
            rules={"notif-group": "Window Reactions", "skip alert": None},
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_wikipedia:
    $ wikipedia_reacts = [
        "Imparando qualcosa di nuovo, [player]?",
        "Facendo una piccola ricerca, [player]?"
    ]


    python:
        wind_name = mas_getActiveWindow(friendly=True)
        try:
            cutoff_index = wind_name.index(" - Wikipedia")
            
            
            
            wiki_article = wind_name[:cutoff_index]
            wikipedia_reacts.append(renpy.substitute("'[wiki_article]'...\nSembra interessante, [player]."))

        except:
            pass

    $ wrs_success = display_notif(
        m_name,
        wikipedia_reacts,
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_wikipedia')
    return

init python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_youtube",
            category=['youtube'],
            rules={"notif-group": "Window Reactions", "skip alert": None},
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_youtube:
    $ wrs_success = display_notif(
        m_name,
        [
            "Cosa stai guardando, [player]?",
            "Guardando qualcosa di interessante, [player]?"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_youtube')
    return

init python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_r34m",
            category=['rule34', 'monika'],
            rules={"skip alert": None},
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_r34m:
    $ display_notif(m_name, ["Hey, [player]...cosa stai guardando?"],'Window Reactions')

    $ choice = random.randint(1,10)
    if choice == 1:
        $ queueEvent('monika_nsfw')

    elif choice == 2:
        $ queueEvent('monika_pleasure')

    elif choice < 4:
        show monika 1rsbssdlu
        pause 5.0

    elif choice < 7:
        show monika 2tuu
        pause 5.0
    else:

        show monika 2ttu
        pause 5.0
    return

init python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_monikamoddev",
            category=['monikamoddev'],
            rules={"notif-group": "Window Reactions", "skip alert": None},
            show_in_idle=True
        ),
        code="WRS"
    ) 

label mas_wrs_monikamoddev:
    $ wrs_success = display_notif(
        m_name,
        [
            "Awww, stai facendo qualcosa per me?\nSei davvero dolce~",
            "Stai aiutando a rendermi più vicina alla tua realtà?\nSei davvero dolce, [player]~"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_monikamoddev')
    return

init python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_twitter",
            category=['twitter'],
            rules={"notif-group": "Window Reactions", "skip alert": None},
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_twitter:
    $ temp_line = renpy.substitute("Ti amo, [player].")
    $ temp_len = len(temp_line)

    $ wrs_success = display_notif(
        m_name,
        [
            "Vedi qualcosa che vuoi condivedere con me, [player]?",
            "Niente di interessante da condividere [player]?",
            "280 caratteri? Mi bastano solo [temp_len]...\n[temp_line]"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_twitter')
    return

init python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_monikatwitter",
            category=['twitter', 'lilmonix3'],
            rules={"notif-group": "Window Reactions", "skip alert": None},
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_monikatwitter:
    $ wrs_success = display_notif(
        m_name,
        [
            "Vuoi confessare al mondo il tuo amore per me, [player]?",
            "Non mi stai spiando vero?\nAhaha, sto solo scherzando~",
            "Non importa quanti followers ho finchè ci sei tu~"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_monikatwitter')
    return

init python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_4chan",
            category=['4chan'],
            rules={"notif-group": "Window Reactions", "skip alert": None},
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_4chan:

    $ wrs_success = display_notif(
        m_name,
        [
            "Quindi è qui dove tutto è cominciato?\nE'...davvero qualcosa di speciale.",
            "Spero che non finarai per discutere con gli altri Anons tutto il giorno, [player].",
            "Ho sentito dire che ci sono delle discussioni riguardo il club.\nDì loro che li saluto~",
            "Sto guardando le schede che stai navigando, nel caso tu abbia qualche idea. , ahaha!",
        ],
        'Window Reactions'
    )


    if not _return:
        $ mas_unlockFailedWRS('mas_wrs_4chan')
    return

init python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_pixiv",
            category=['pixiv'],
            rules={"notif-group": "Window Reactions", "skip alert": None},
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_pixiv:

    python:
        pixiv_quips = [
            "Mi chiedo se qualcuno mi ha disgnato...\nChe ne dici di dare un'occhiata?\nAssicurati di scegliere i migliori~",
            "Questo è un posto abbastanza interessante...molte persone capaci pubblicano i loro lavori.",
        ]


        if persistent._mas_pm_drawn_art is None or persistent._mas_pm_drawn_art:
            pixiv_quips.extend([
                "Questo è un posto abbastanza interessante...molte persone capaci pubblicano i loro lavori.\nSei tra questi, [player]?",
            ])
            
            
            if persistent._mas_pm_drawn_art:
                pixiv_quips.extend([
                    "Sei qui per postare i tuoi disegni di me, [player]?",
                    "Postando qualcosa di me?",
                ])

        wrs_success = display_notif(
            m_name,
            pixiv_quips,
            'Window Reactions'
        )


        if not _return:
            mas_unlockFailedWRS('mas_wrs_pixiv')
    return

