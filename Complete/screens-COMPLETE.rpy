init 100 python:
    layout.QUIT = store.mas_layout.QUIT
    layout.UNSTABLE = store.mas_layout.UNSTABLE
init offset = -1
init python:
    layout.QUIT_YES = "Ti prego non chiudere il gioco!"
    layout.QUIT_NO = "Grazie, [player]!\nStiamo ancora un pò insieme~"


    layout.MAS_TT_SENS_MODE = (
        "'Sensitive mode' rimuove contenuti che potrebbero essere disturbanti, offensivi,"
        " o considerato di cattivo gusto."
    )
    layout.MAS_TT_UNSTABLE = (
        "'Unstable mode' scarica gli aggiornamenti dal ramo sperimentale "
        "di sviluppo instabile. si raccomanda di fare un backup  "
        "dei file 'persistent' prima di attivare questa modalità."
        #"NOTA DAI TRADUTTORI: Questa modalità potrebbe cancellare " #DEPRECATED#These lines are used to tell the user that activating
        #"i file tradotti, si raccomanda di fare attenzione."        # the mode may delete files translated into Italian 
    )
    layout.MAS_TT_REPEAT = (
        "Attivare questo per permettere a Monika di ripetere argomenti che avete già visto."
    )
    layout.MAS_TT_NOTIF = (
        "Abilitando questa opzione Monika potrà utilizzare le notifiche del sistema e verificare se MAS è la finestra attiva. "
    )
    layout.MAS_TT_NOTIF_SOUND = (
        "Se abilitato, verrà emesso un suono di notifica personalizzato per le notifiche di Monika. "
    )
    layout.MAS_TT_G_NOTIF = (
        "Abilita le notifiche per il gruppo selezionato."
    )
    layout.MAS_TT_ACTV_WND = (
        "Abilitando questa opzione, Monika potrà vedere la tua finestra attiva "
        "e di offrire alcuni commenti in base a ciò che stai facendo."
    )




init 1 python in mas_layout:
    import store
    import store.mas_affection as aff

    QUIT_YES = store.layout.QUIT_YES
    QUIT_NO = store.layout.QUIT_NO
    QUIT = "Te ne stai andando senza salutarmi, [player]?"
    UNSTABLE = (
        "ATTENZIONE: Attivando la modalità instabile si scaricheranno gli aggiornamenti dal " +
        "ramo sperimentale instabile. Si raccomanda vivamente di fare " +
        "un backup dei file 'persistent' prima di attivare questa modalità. Si prega " +
        "di segnalare i problemi trovati qui con un tag [[UNSTABLE]."
         
    )


    QUIT_YES_BROKEN = "Potresti almeno fingere di interessarti"
    QUIT_YES_DIS = ":("
    QUIT_YES_AFF = "T_T [player]..."


    QUIT_NO_BROKEN = "{i}Ora{/i} mi ascolti?"
    QUIT_NO_UPSET = "Grazie per essere stato premuroso., [player]."
    QUIT_NO_HAPPY = ":)"
    QUIT_NO_AFF_G = "Bravo." # i think the [boy] variable is useless so i removed it from here
    QUIT_NO_AFF_GL = "Brava. :)"
    QUIT_NO_LOVE = "Ti <3"


    QUIT_BROKEN = "Vai via."
    QUIT_AFF = "Perchè sei qui?\n Clicca 'No' e usa il pulsante 'Goodbye' scemetto!" #BHO

    if store.persistent.gender == "M" or store.persistent.gender == "F":
        _usage_quit_aff = QUIT_NO_AFF_G
    else:
        _usage_quit_aff = QUIT_NO_AFF_GL







    QUIT_MAP = {
        aff.BROKEN: (QUIT_BROKEN, QUIT_YES_BROKEN, QUIT_NO_BROKEN),
        aff.DISTRESSED: (None, QUIT_YES_DIS, None),
        aff.UPSET: (None, None, QUIT_NO_UPSET),
        aff.NORMAL: (QUIT, QUIT_YES, QUIT_NO),
        aff.HAPPY: (None, None, QUIT_NO_HAPPY),
        aff.AFFECTIONATE: (QUIT_AFF, QUIT_YES_AFF, _usage_quit_aff),
        aff.ENAMORED: (None, None, None),
        aff.LOVE: (None, None, QUIT_NO_LOVE)
    }


    def findMsg(start_aff, index):
        """
        Finds first non-None quit message we need

        This uses the cascade map from affection

        IN:
            start_aff - starting affection
            index - index of the tuple we need to look at

        RETURNS:
            first non-None quit message found.
        """
        msg = QUIT_MAP[start_aff][index]
        while msg is None:
            start_aff = aff._aff_cascade_map[start_aff]
            msg = QUIT_MAP[start_aff][index]
        
        return msg


    def setupQuits():
        """
        Sets up quit message based on the current affection state
        """
        curr_aff_state = store.mas_curr_affection
        
        quit_msg, quit_yes, quit_no = QUIT_MAP[curr_aff_state]
        
        if quit_msg is None:
            quit_msg = findMsg(curr_aff_state, 0)
        
        if quit_yes is None:
            quit_yes = findMsg(curr_aff_state, 1)
        
        if quit_no is None:
            quit_no = findMsg(curr_aff_state, 2)
        
        store.layout.QUIT = quit_msg
        store.layout.QUIT_YES = quit_yes
        store.layout.QUIT_NO = quit_no


init 901 python:
    import store.mas_layout
    store.mas_layout.setupQuits()












style default:
    font gui.default_font
    size gui.text_size
    color gui.text_color
    outlines [(2, "#000000aa", 0, 0)]
    line_overlap_split 1
    line_spacing 1

style default_monika is normal:
    slow_cps 30

style edited is default:
    font "gui/font/VerilySerifMono.otf"
    kerning 8
    outlines [(10, "#000", 0, 0)]
    xpos gui.text_xpos
    xanchor gui.text_xalign
    xsize gui.text_width
    ypos gui.text_ypos
    text_align gui.text_xalign
    layout ("subtitle" if gui.text_xalign else "tex")

style normal is default:
    xpos gui.text_xpos
    xanchor gui.text_xalign
    xsize gui.text_width
    ypos gui.text_ypos

    text_align gui.text_xalign
    layout ("subtitle" if gui.text_xalign else "tex")

style input:
    color gui.accent_color

style hyperlink_text:
    color gui.accent_color
    hover_color gui.hover_color
    hover_underline True

style splash_text:
    size 24
    color "#000"
    font gui.default_font
    text_align 0.5
    outlines []

style poemgame_text:
    yalign 0.5
    font "gui/font/Halogen.ttf"
    size 30
    color "#000"
    outlines []

    hover_xoffset -3
    hover_outlines [(3, "#fef", 0, 0), (2, "#fcf", 0, 0), (1, "#faf", 0, 0)]

style gui_text:
    font gui.interface_font
    color gui.interface_text_color
    size gui.interface_text_size


style button:
    properties gui.button_properties("button")

style button_text is gui_text:
    properties gui.button_text_properties("button")
    yalign 0.5


style label_text is gui_text:
    color gui.accent_color
    size gui.label_text_size

style prompt_text is gui_text:
    color gui.text_color
    size gui.interface_text_size







style vbar:
    xsize gui.bar_size
    top_bar Frame("gui/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style bar:
    ysize 18
    base_bar Frame("gui/scrollbar/horizontal_poem_bar.png", tile=False)
    thumb Frame("gui/scrollbar/horizontal_poem_thumb.png", top=6, right=6, tile=True)

style scrollbar:
    ysize 18
    base_bar Frame("gui/scrollbar/horizontal_poem_bar.png", tile=False)
    thumb Frame("gui/scrollbar/horizontal_poem_thumb.png", top=6, right=6, tile=True)
    unscrollable "hide"
    bar_invert True


style vscrollbar:
    xsize 18
    base_bar Frame("gui/scrollbar/vertical_poem_bar.png", tile=False)
    thumb Frame("gui/scrollbar/vertical_poem_thumb.png", left=6, top=6, tile=True)
    unscrollable "hide"
    bar_invert True






style slider:
    ysize 18
    base_bar Frame("gui/scrollbar/horizontal_poem_bar.png", tile=False)
    thumb "gui/slider/horizontal_hover_thumb.png"

style vslider:
    xsize gui.slider_size
    base_bar Frame("gui/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/slider/vertical_[prefix_]thumb.png"


style frame:
    padding gui.frame_borders.padding
    background Frame("gui/frame.png", gui.frame_borders, tile=gui.frame_tile)





















screen say(who, what):
    style_prefix "say"

    window:
        id "window"

        text what id "what"

        if who is not None:

            window:
                style "namebox"
                text who id "who"



    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0

    use quick_menu


style window is default
style say_label is default
style say_dialogue is default
style say_thought is say_dialogue

style namebox is default
style namebox_label is say_label


style window:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height

    background Image("gui/textbox.png", xalign=0.5, yalign=1.0)

style window_monika is window:
    background Image("gui/textbox_monika.png", xalign=0.5, yalign=1.0)

style namebox:
    xpos gui.name_xpos
    xanchor gui.name_xalign
    xsize gui.namebox_width
    ypos gui.name_ypos
    ysize gui.namebox_height

    background Frame("gui/namebox.png", gui.namebox_borders, tile=gui.namebox_tile, xalign=gui.name_xalign)
    padding gui.namebox_borders.padding

style say_label:
    color gui.accent_color
    font gui.name_font
    size gui.name_text_size
    xalign gui.name_xalign
    yalign 0.5
    outlines [(3, "#b59", 0, 0), (1, "#b59", 1, 1)]

style say_dialogue:
    xpos gui.text_xpos
    xanchor gui.text_xalign
    xsize gui.text_width
    ypos gui.text_ypos

    text_align gui.text_xalign
    layout ("subtitle" if gui.text_xalign else "tex")

image ctc:
    xalign 0.81 yalign 0.98 xoffset -5 alpha 0.0 subpixel True
    "gui/ctc.png"
    block:
        easeout 0.75 alpha 1.0 xoffset 0
        easein 0.75 alpha 0.5 xoffset -5
        repeat











image input_caret:
    Solid("#b59")
    size (2,25) subpixel True
    block:
        linear 0.35 alpha 0
        linear 0.35 alpha 1
        repeat

screen input(prompt):
    style_prefix "input"


    window:
        has vbox:
            xalign .5
            yalign .5
            spacing 30

        text prompt style "input_prompt"
        input id "input"

style input_prompt:
    xmaximum gui.text_width
    xcenter 0.5
    text_align 0.5

style input:
    caret "input_caret"
    xmaximum gui.text_width
    xcenter 0.5
    text_align 0.5










screen choice(items):
    style_prefix "choice"

    vbox:
        for i in items:
            textbutton i.caption action i.action




define config.narrator_menu = True


style choice_vbox is vbox
style choice_button is button
style choice_button_text is button_text

style choice_vbox:
    xalign 0.5
    ypos 270
    yanchor 0.5

    spacing gui.choice_spacing

style choice_button is default:
    properties gui.button_properties("choice_button")
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style choice_button_text is default:
    properties gui.button_text_properties("choice_button")
    outlines []


init python:
    def RigMouse():
        currentpos = renpy.get_mouse_pos()
        targetpos = [640, 345]
        if currentpos[1] < targetpos[1]:
            renpy.display.draw.set_mouse_pos((currentpos[0] * 9 + targetpos[0]) / 10.0, (currentpos[1] * 9 + targetpos[1]) / 10.0)

screen rigged_choice(items):
    style_prefix "choice"

    vbox:
        for i in items:
            textbutton i.caption action i.action

    timer 1.0/30.0 repeat True action Function(RigMouse)

style talk_choice_vbox is choice_vbox:
    xcenter 960

style talk_choice_button is choice_button
style talk_choice_button_text is choice_button_text



screen talk_choice(items):
    style_prefix "talk_choice"

    vbox:
        for i in items:
            textbutton i.caption action i.action




define config.narrator_menu = True


style choice_vbox is vbox
style choice_button is button
style choice_button_text is button_text

style choice_vbox:
    xalign 0.5
    ypos 270
    yanchor 0.5

    spacing gui.choice_spacing

style choice_button is default:
    properties gui.button_properties("choice_button")
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style choice_button_text is default:
    properties gui.button_text_properties("choice_button")
    outlines []







screen quick_menu():


    zorder 100

    if quick_menu:


        hbox:
            style_prefix "quick"

            xalign 0.5
            yalign 0.995




            textbutton _("History") action Function(_mas_quick_menu_cb, "history") #BHO

            textbutton _("Salta") action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _("Auto") action Preference("auto-forward", "toggle")


            textbutton _("Salva") action Function(_mas_quick_menu_cb, "save")


            textbutton _("Carica") action Function(_mas_quick_menu_cb, "load")




            textbutton _("Impostazioni") action Function(_mas_quick_menu_cb, "preferences")







default quick_menu = True




style quick_button:
    properties gui.button_properties("quick_button")
    activate_sound gui.activate_sound

style quick_button_text:
    properties gui.button_text_properties("quick_button")
    outlines []











init python:
    def FinishEnterName():
        if not player: return
        persistent.playername = player
        renpy.hide_screen("name_input")
        renpy.jump_out_of_context("start")

screen navigation():

    vbox:
        style_prefix "navigation"

        xpos gui.navigation_xpos
        yalign 0.8

        spacing gui.navigation_spacing


        if main_menu:

            textbutton _("Just Monika") action If(persistent.playername, true=Start(), false=Show(screen="name_input", message="Inserisci il tuo nome", ok_action=Function(FinishEnterName)))

        else:

            textbutton _("History") action [ShowMenu("history"), SensitiveIf(renpy.get_screen("history") == None)]

            textbutton _("Salva") action [ShowMenu("save"), SensitiveIf(renpy.get_screen("save") == None)]

        textbutton _("Carica") action [ShowMenu("load"), SensitiveIf(renpy.get_screen("load") == None)]

        if _in_replay:

            textbutton _("End Replay") action EndReplay(confirm=True)

        elif not main_menu:
            textbutton _("Menu principale") action NullAction(), Show(screen="dialog", message="No need to go back there.\nYou'll just end up back here so don't worry.", ok_action=Hide("dialog"))

        textbutton _("Impostazioni") action [ShowMenu("preferences"), SensitiveIf(renpy.get_screen("preferences") == None)]

        if store.mas_windowreacts.can_show_notifs and not main_menu:
            textbutton _("Alerts") action [ShowMenu("notif_settings"), SensitiveIf(renpy.get_screen("notif_settings") == None)]



        if renpy.variant("pc"):


            textbutton _("Aiuto") action Help("README.html")


            textbutton _("Esci") action Quit(confirm=_confirm_quit)


style navigation_button is gui_button
style navigation_button_text is gui_button_text

style navigation_button:
    size_group "navigation"
    properties gui.button_properties("navigation_button")
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style navigation_button_text:
    properties gui.button_text_properties("navigation_button")
    font "gui/font/RifficFree-Bold.ttf"
    color "#fff"
    outlines [(4, "#b59", 0, 0), (2, "#b59", 2, 2)]
    hover_outlines [(4, "#fac", 0, 0), (2, "#fac", 2, 2)]
    insensitive_outlines [(4, "#fce", 0, 0), (2, "#fce", 2, 2)]








screen main_menu() tag menu:




    style_prefix "main_menu"








    add "menu_bg"


    frame




    use navigation

    if gui.show_name:

        vbox:
            text "[config.name!t]":
                style "main_menu_title"

            text "[config.version]":
                style "main_menu_version"


    add "menu_particles"
    add "menu_particles"
    add "menu_particles"
    add "menu_logo"








    add "menu_particles"

    add "menu_art_m"
    add "menu_fade"

    key "K_ESCAPE" action Quit(confirm=False)

style main_menu_frame is empty
style main_menu_vbox is vbox
style main_menu_text is gui_text
style main_menu_title is main_menu_text
style main_menu_version is main_menu_text:
    color "#000000"
    size 16
    outlines []

style main_menu_frame:
    xsize 310
    yfill True

    background "menu_nav"

style main_menu_vbox:
    xalign 1.0
    xoffset -20
    xmaximum 800
    yalign 1.0
    yoffset -20

style main_menu_text:
    xalign 1.0

    layout "subtitle"
    text_align 1.0
    color gui.accent_color

style main_menu_title:
    size gui.title_text_size











screen game_menu_m():
    $ persistent.menu_bg_m = True
    add "gui/menu_bg_m.png"
    timer 0.3 action Hide("game_menu_m")

screen game_menu(title, scroll=None):


    key "noshift_T" action NullAction()
    key "noshift_t" action NullAction()
    key "noshift_M" action NullAction()
    key "noshift_m" action NullAction()
    key "noshift_P" action NullAction()
    key "noshift_p" action NullAction()


    if main_menu:
        add gui.main_menu_background
    else:
        key "mouseup_3" action Return()
        add gui.game_menu_background

    style_prefix "game_menu"

    frame:
        style "game_menu_outer_frame"

        has hbox


        frame:
            style "game_menu_navigation_frame"

        frame:
            style "game_menu_content_frame"

            if scroll == "viewport":

                viewport:
                    scrollbars "vertical"
                    mousewheel True
                    draggable True
                    yinitial 1.0

                    side_yfill True

                    has vbox
                    transclude

            elif scroll == "vpgrid":

                vpgrid:
                    cols 1
                    yinitial 1.0

                    scrollbars "vertical"
                    mousewheel True
                    draggable True

                    side_yfill True

                    transclude

            else:

                transclude

    use navigation




    textbutton _("Return"):
        style "return_button"

        action Return()

    label title

    if main_menu:
        key "game_menu" action ShowMenu("main_menu")


style game_menu_outer_frame is empty
style game_menu_navigation_frame is empty
style game_menu_content_frame is empty
style game_menu_viewport is gui_viewport
style game_menu_side is gui_side
style game_menu_scrollbar is gui_vscrollbar

style game_menu_label is gui_label
style game_menu_label_text is gui_label_text

style return_button is navigation_button
style return_button_text is navigation_button_text

style game_menu_outer_frame:
    bottom_padding 30
    top_padding 120

    background "gui/overlay/game_menu.png"

style game_menu_navigation_frame:
    xsize 280
    yfill True

style game_menu_content_frame:
    left_margin 40
    right_margin 20
    top_margin 10

style game_menu_viewport:
    xsize 920

style game_menu_vscrollbar:
    unscrollable gui.unscrollable

style game_menu_side:
    spacing 10

style game_menu_label:
    xpos 50
    ysize 120

style game_menu_label_text:
    font "gui/font/RifficFree-Bold.ttf"
    size gui.title_text_size
    color "#fff"
    outlines [(6, "#b59", 0, 0), (3, "#b59", 2, 2)]
    yalign 0.5

style return_button:
    xpos gui.navigation_xpos
    yalign 1.0
    yoffset -30









screen about() tag menu:






    use game_menu(_("About"), scroll="viewport"):

        style_prefix "about"

        vbox:

            label "[config.name!t]"
            text _("Version [config.version!t]\n")


            if gui.about:
                text "[gui.about!t]\n"

            text _("Made with {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]")



define gui.about = ""


style about_label is gui_label
style about_label_text is gui_label_text
style about_text is gui_text

style about_label_text:
    size gui.label_text_size











screen save() tag menu:



    use file_slots(_("Save"))


screen load() tag menu:



    use file_slots(_("Load"))

init python:
    def FileActionMod(name, page=None, **kwargs):
        if renpy.current_screen().screen_name[0] == "save":
            return Show(screen="dialog", message="Non ha piu' senso salvare.\nNon preoccuparti, non vado da nessuna parte.", ok_action=Hide("dialog"))


screen file_slots(title):

    default page_name_value = FilePageNameInputValue()

    use game_menu(title):

        fixed:



            order_reverse True



            button:
                style "page_label"


                xalign 0.5


                input:
                    style "page_label_text"
                    value page_name_value


            grid gui.file_slot_cols gui.file_slot_rows:
                style_prefix "slot"

                xalign 0.5
                yalign 0.5

                spacing gui.slot_spacing

                for i in range(gui.file_slot_cols * gui.file_slot_rows):

                    $ slot = i + 1

                    button:
                        action FileActionMod(slot)

                        has vbox

                        add FileScreenshot(slot) xalign 0.5

                        text FileTime(slot, format=_("{#file_time}%A, %B %d %Y, %H:%M"), empty=_("empty slot")):
                            style "slot_time_text"

                        text FileSaveName(slot):
                            style "slot_name_text"

                        key "save_delete" action FileDelete(slot)


            hbox:
                style_prefix "page"

                xalign 0.5
                yalign 1.0

                spacing gui.page_spacing








                for page in range(1, 10):
                    textbutton "[page]" action FilePage(page)




style page_label is gui_label
style page_label_text is gui_label_text
style page_button is gui_button
style page_button_text is gui_button_text

style slot_button is gui_button
style slot_button_text is gui_button_text
style slot_time_text is slot_button_text
style slot_name_text is slot_button_text

style page_label:
    xpadding 50
    ypadding 3

style page_label_text:
    color "#000"
    outlines []
    text_align 0.5
    layout "subtitle"
    hover_color gui.hover_color

style page_button:
    properties gui.button_properties("page_button")

style page_button_text:
    properties gui.button_text_properties("page_button")
    outlines []

style slot_button:
    properties gui.button_properties("slot_button")

style slot_button_text:
    properties gui.button_text_properties("slot_button")
    color "#666"
    outlines []









screen preferences() tag menu:



    if renpy.mobile:
        $ cols = 2
    else:
        $ cols = 4

    default tooltip = Tooltip("")

    use game_menu(_("Settings"), scroll="viewport"):

        vbox:
            xoffset 50

            hbox:
                box_wrap True

                if renpy.variant("pc"):

                    vbox:
                        style_prefix "radio"
                        label _("Display")
                        textbutton _("Finestra") action Preference("display", "window")
                        textbutton _("Schermo Intero") action Preference("display", "fullscreen")









                vbox:
                    style_prefix "check"
                    label _("Grafica")
                    textbutton _("Disattiva Animazioni") action ToggleField(persistent, "_mas_disable_animations")
                    textbutton _("Cambia Rendering") action Function(renpy.call_in_new_context, "mas_gmenu_start")


                vbox:
                    style_prefix "check"
                    label _("Gameplay")
                    if persistent._mas_unstable_mode:
                        textbutton _("Unstable"):
                            action SetField(persistent, "_mas_unstable_mode", False)
                            selected persistent._mas_unstable_mode

                    else:
                        textbutton _("Unstable"):
                            action [Show(screen="dialog", message=layout.UNSTABLE, ok_action=Hide(screen="dialog")), SetField(persistent, "_mas_unstable_mode", True)]
                            selected persistent._mas_unstable_mode
                            hovered tooltip.Action(layout.MAS_TT_UNSTABLE)

                    textbutton _("Ripeti conversazioni"):
                        action ToggleField(persistent,"_mas_enable_random_repeats", True, False)
                        hovered tooltip.Action(layout.MAS_TT_REPEAT)



                vbox:
                    style_prefix "check"
                    label _(" ")
                    textbutton _("Sensitive Mode"):
                        action ToggleField(persistent, "_mas_sensitive_mode", True, False)
                        hovered tooltip.Action(layout.MAS_TT_SENS_MODE)

                    if renpy.windows and store.mas_windowreacts.can_show_notifs:
                        textbutton _("Window Reacts"):
                            action ToggleField(persistent, "_mas_windowreacts_windowreacts_enabled", True, False)
                            hovered tooltip.Action(layout.MAS_TT_ACTV_WND)

            null height (4 * gui.pref_spacing)

            hbox:
                style_prefix "slider"
                box_wrap True

                python:

                    if mas_randchat_prev != persistent._mas_randchat_freq:
                        
                        mas_randchat.adjustRandFreq(
                            persistent._mas_randchat_freq
                        )


                    rc_display = mas_randchat.getRandChatDisp(
                        persistent._mas_randchat_freq
                    )


                    mas_randchat_prev = persistent._mas_randchat_freq




                    if mas_suntime.change_state == mas_suntime.RISE_CHANGE:
                        
                        
                        if mas_suntime.sunrise > mas_suntime.sunset:
                            
                            mas_suntime.sunset = mas_suntime.sunrise
                        
                        if mas_sunrise_prev == mas_suntime.sunrise:
                            
                            mas_suntime.change_state = mas_suntime.NO_CHANGE
                        
                        mas_sunrise_prev = mas_suntime.sunrise

                    elif mas_suntime.change_state == mas_suntime.SET_CHANGE:
                        
                        
                        if mas_suntime.sunset < mas_suntime.sunrise:
                            
                            mas_suntime.sunrise = mas_suntime.sunset
                        
                        if mas_sunset_prev == mas_suntime.sunset:
                            
                            mas_suntime.change_state = mas_suntime.NO_CHANGE
                        
                        mas_sunset_prev = mas_suntime.sunset
                    else:
                        
                        
                        if mas_sunrise_prev != mas_suntime.sunrise:
                            mas_suntime.change_state = mas_suntime.RISE_CHANGE
                        
                        elif mas_sunset_prev != mas_suntime.sunset:
                            mas_suntime.change_state = mas_suntime.SET_CHANGE
                        
                        
                        mas_sunrise_prev = mas_suntime.sunrise
                        mas_sunset_prev = mas_suntime.sunset



                    persistent._mas_sunrise = mas_suntime.sunrise * 5
                    persistent._mas_sunset = mas_suntime.sunset * 5
                    sr_display = mas_cvToDHM(persistent._mas_sunrise)
                    ss_display = mas_cvToDHM(persistent._mas_sunset)

                vbox:

                    hbox:
                        label _("Alba   ")


                        label _("[[ " + sr_display + " ]")

                    bar value FieldValue(mas_suntime, "sunrise", range=mas_max_suntime, style="slider")


                    hbox:
                        label _("Tramonto   ")


                        label _("[[ " + ss_display + " ]")

                    bar value FieldValue(mas_suntime, "sunset", range=mas_max_suntime, style="slider")


                vbox:

                    hbox:
                        label _("Chiacchiere casuali   ")


                        label _("[[ " + rc_display + " ]")

                    bar value FieldValue(persistent, "_mas_randchat_freq",
                    range=6, style="slider")

                    hbox:
                        label _("Volume dell'ambiente")

                    bar value Preference("mixer amb volume")


                vbox:

                    label _("Velocità testo")


                    bar value FieldValue(_preferences, "text_cps", range=170, max_is_zero=False, style="slider", offset=30)

                    label _("Auto-Forward Time")

                    bar value Preference("auto-forward time")

                vbox:

                    if config.has_music:
                        label _("Volume Musica")

                        hbox:
                            bar value Preference("music volume")

                    if config.has_sound:

                        label _("Volume Suoni")

                        hbox:
                            bar value Preference("sound volume")

                            if config.sample_sound:
                                textbutton _("Test") action Play("sound", config.sample_sound)


                    if config.has_voice:
                        label _("Volume Voce")

                        hbox:
                            bar value Preference("voice volume")

                            if config.sample_voice:
                                textbutton _("Test") action Play("voice", config.sample_voice)

                    if config.has_music or config.has_sound or config.has_voice:
                        null height gui.pref_spacing

                        textbutton _("Silenzia tutto"):
                            action Preference("all mute", "toggle")
                            style "mute_all_button"


            hbox:
                textbutton _("Aggiorna"):
                    action Function(renpy.call_in_new_context, 'forced_update_now')
                    style "navigation_button"

                textbutton _("Import DDLC Save Data"):
                    action Function(renpy.call_in_new_context, 'import_ddlc_persistent_in_settings')
                    style "navigation_button"


    text tooltip.value:
        xalign 0.0 yalign 1.0
        xoffset 300 yoffset -10
        style "main_menu_version"




    text "v[config.version]":
        xalign 1.0 yalign 0.0
        xoffset -10
        style "main_menu_version"

style pref_label is gui_label
style pref_label_text is gui_label_text
style pref_vbox is vbox

style radio_label is pref_label
style radio_label_text is pref_label_text
style radio_button is gui_button
style radio_button_text is gui_button_text
style radio_vbox is pref_vbox

style check_label is pref_label
style check_label_text is pref_label_text
style check_button is gui_button
style check_button_text is gui_button_text
style check_vbox is pref_vbox

style slider_label is pref_label
style slider_label_text is pref_label_text
style slider_slider is gui_slider
style slider_button is gui_button
style slider_button_text is gui_button_text
style slider_pref_vbox is pref_vbox

style mute_all_button is check_button
style mute_all_button_text is check_button_text

style pref_label:
    top_margin gui.pref_spacing
    bottom_margin 2

style pref_label_text:
    font "gui/font/RifficFree-Bold.ttf"
    size 24
    color "#fff"
    outlines [(3, "#b59", 0, 0), (1, "#b59", 1, 1)]
    yalign 1.0

style pref_vbox:
    xsize 225

style radio_vbox:
    spacing gui.pref_button_spacing

style radio_button:
    properties gui.button_properties("radio_button")
    foreground "gui/button/check_[prefix_]foreground.png"

style radio_button_text:
    properties gui.button_text_properties("radio_button")
    font "gui/font/Halogen.ttf"
    outlines []

style check_vbox:
    spacing gui.pref_button_spacing

style check_button:
    properties gui.button_properties("check_button")
    foreground "gui/button/check_[prefix_]foreground.png"

style check_button_text:
    properties gui.button_text_properties("check_button")
    font "gui/font/Halogen.ttf"
    outlines []

style slider_slider:
    xsize 350

style slider_button:
    properties gui.button_properties("slider_button")
    yalign 0.5
    left_margin 10

style slider_button_text:
    properties gui.button_text_properties("slider_button")

style slider_vbox:
    xsize 450


screen notif_settings() tag menu:


    use game_menu(("Alerts"), scroll="viewport"):

        default tooltip = Tooltip("")

        vbox:
            style_prefix "check"
            hbox:
                spacing 25
                textbutton _("Usa le notifiche"):
                    action ToggleField(persistent, "_mas_enable_notifications")
                    selected persistent._mas_enable_notifications
                    hovered tooltip.Action(layout.MAS_TT_NOTIF)

                textbutton _("Suoni"):
                    action ToggleField(persistent, "_mas_notification_sounds")
                    selected persistent._mas_notification_sounds
                    hovered tooltip.Action(layout.MAS_TT_NOTIF_SOUND)

            label _("Alert Filtri") #BHO

        hbox:
            style_prefix "check"
            box_wrap True
            spacing 25


            for item in persistent._mas_windowreacts_notif_filters:
                if item != "Window Reactions" or persistent._mas_windowreacts_windowreacts_enabled:
                    textbutton _(item):
                        action ToggleDict(persistent._mas_windowreacts_notif_filters, item)
                        selected persistent._mas_windowreacts_notif_filters.get(item)
                        hovered tooltip.Action(layout.MAS_TT_G_NOTIF)


    text tooltip.value:
        xalign 0 yalign 1.0
        xoffset 300 yoffset -10
        style "main_menu_version"









screen history() tag menu:




    predict False

    use game_menu(_("History"), scroll=("vpgrid" if gui.history_height else "viewport")):

        style_prefix "history"

        for h in _history_list:

            window:


                has fixed:
                    yfit True

                if h.who:

                    label h.who:
                        style "history_name"



                        if "color" in h.who_args:
                            text_color h.who_args["color"]

                text h.what.replace("[","[[")

        if not _history_list:
            label _("The dialogue history is empty.")


style history_window is empty

style history_name is gui_label
style history_name_text is gui_label_text
style history_text is gui_text

style history_text is gui_text

style history_label is gui_label
style history_label_text is gui_label_text

style history_window:
    xfill True
    ysize gui.history_height

style history_name:
    xpos gui.history_name_xpos
    xanchor gui.history_name_xalign
    ypos gui.history_name_ypos
    xsize gui.history_name_width

style history_name_text:
    min_width gui.history_name_width
    text_align gui.history_name_xalign

style history_text:
    xpos gui.history_text_xpos
    ypos gui.history_text_ypos
    xanchor gui.history_text_xalign
    xsize gui.history_text_width
    min_width gui.history_text_width
    text_align gui.history_text_xalign
    layout ("subtitle" if gui.history_text_xalign else "tex")

style history_label:
    xfill True

style history_label_text:
    xalign 0.5












































































































































































screen name_input(message, ok_action):


    modal True

    zorder 200

    style_prefix "confirm"

    add "gui/overlay/confirm.png"
    key "K_RETURN" action [Play("sound", gui.activate_sound), ok_action]

    frame:

        has vbox:
            xalign .5
            yalign .5
            spacing 30

        label _(message):
            style "confirm_prompt"
            xalign 0.5

        input default "" value VariableInputValue("player") length 12 allow "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

        hbox:
            xalign 0.5
            spacing 100

            textbutton _("OK") action ok_action

screen dialog(message, ok_action):


    modal True

    zorder 200

    style_prefix "confirm"

    add "gui/overlay/confirm.png"

    frame:

        has vbox:
            xalign .5
            yalign .5
            spacing 30

        label _(message):
            style "confirm_prompt"
            xalign 0.5

        hbox:
            xalign 0.5
            spacing 100

            textbutton _("OK") action ok_action

screen quit_dialog(message, ok_action):


    modal True

    zorder 200

    style_prefix "confirm"

    add "gui/overlay/confirm.png"

    frame:

        has vbox:
            xalign .5
            yalign .5
            spacing 30

        label _(message):
            style "confirm_prompt"
            xalign 0.5

        hbox:
            xalign 0.5
            spacing 100

            textbutton _("QUIT") action ok_action

image confirm_glitch:
    "gui/overlay/confirm_glitch.png"
    pause 0.02
    "gui/overlay/confirm_glitch2.png"
    pause 0.02
    repeat

screen confirm(message, yes_action, no_action):


    modal True

    zorder 200

    style_prefix "confirm"

    add "gui/overlay/confirm.png"

    frame:

        has vbox:
            xalign .5
            yalign .5
            spacing 30

        if in_sayori_kill and message == layout.QUIT:
            add "confirm_glitch" xalign 0.5

        else:
            label _(message):
                style "confirm_prompt"
                xalign 0.5

        hbox:
            xalign 0.5
            spacing 100

            if mas_finalfarewell_mode:
                textbutton _("-") action yes_action
                textbutton _("-") action yes_action
            else:
                textbutton _("Si") action [SetField(persistent, "_mas_game_crashed", False), Show(screen="quit_dialog", message=layout.QUIT_YES, ok_action=yes_action)]
                textbutton _("No") action no_action, Show(screen="dialog", message=layout.QUIT_NO, ok_action=Hide("dialog"))







style confirm_frame is gui_frame
style confirm_prompt is gui_prompt
style confirm_prompt_text is gui_prompt_text
style confirm_button is gui_medium_button
style confirm_button_text is gui_medium_button_text

style confirm_frame:
    background Frame([ "gui/confirm_frame.png", "gui/frame.png"], gui.confirm_frame_borders, tile=gui.frame_tile)
    padding gui.confirm_frame_borders.padding
    xalign .5
    yalign .5

style confirm_prompt_text:
    color "#000"
    outlines []
    text_align 0.5
    layout "subtitle"

style confirm_button:
    properties gui.button_properties("confirm_button")
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style confirm_button_text is navigation_button_text:
    properties gui.button_text_properties("confirm_button")



screen update_check(ok_action, cancel_action, mode):


    modal True

    zorder 200

    style_prefix "update_check"

    add "gui/overlay/confirm.png"

    frame:

        has vbox:
            xalign .5
            yalign .5
            spacing 30

        if mode == 0:
            label _('Aggiornamento disponibile!'):
                style "confirm_prompt"
                xalign 0.5

        elif mode == 1:
            label _("Nessun aggiornamento trovato."):
                style "confirm_prompt"
                xalign 0.5

        elif mode == 2:
            label _('Cerco aggiornamenti...'):
                style "confirm_prompt"
                xalign 0.5
        else:

            label _('Timeout occured while checking for updates. Try again later.'):
                style "confirm_prompt"
                xalign 0.5

        hbox:
            xalign 0.5
            spacing 100

            textbutton _("Installa") action [ok_action, SensitiveIf(mode == 0)]

            textbutton _("Cancella") action cancel_action

    timer 1.0 action Return("None")





style update_check_frame is confirm_frame
style update_check_prompt is confirm_prompt
style update_check_prompt_text is confirm_prompt_text
style update_check_button is confirm_button
style update_check_button_text is confirm_button_text





screen updater:

    modal True

    style_prefix "updater"

    frame:

        has side "t c b":
            spacing gui._scale(10)

        label _("Updater")

        fixed:

            vbox:

                if u.state == u.ERROR:
                    text _("Si è verificato un errore:")
                elif u.state == u.CHECKING:
                    text _("Cerco aggiornamenti.")
                elif u.state == u.UPDATE_AVAILABLE:
                    text _("Versione [u.version] è disponibile. Vuoi installarla?")

                elif u.state == u.UPDATE_NOT_AVAILABLE:
                    text _("Monika After Story è gia aggiornato.")
                elif u.state == u.PREPARING:
                    text _("Preparazione al download.")
                elif u.state == u.DOWNLOADING:
                    text _("Scarico gli aggiornamenti. (La barra di avanzamento potrebbe non avanzare durante il download)")
                elif u.state == u.UNPACKING:
                    text _("Estraendo gli aggiornamenti.")
                elif u.state == u.FINISHING:
                    text _("Completo l'operazione.")
                elif u.state == u.DONE:
                    text _("Aggiornamento installato. Riapri Monika After Story.")
                elif u.state == u.DONE_NO_RESTART:
                    text _("Gli aggiornamenti sono stati installati.")
                elif u.state == u.CANCELLED:
                    text _("Aggiornamenti cancellati.")

                if u.message is not None:
                    null height gui._scale(10)
                    text "[u.message!q]"

                if u.progress is not None:
                    null height gui._scale(10)
                    bar value u.progress range 1.0 left_bar Solid("#cc6699") right_bar Solid("#ffffff") thumb None

        hbox:

            spacing gui._scale(25)

            if u.can_proceed:
                textbutton _("Procedi") action u.proceed

            if u.can_cancel:
                textbutton _("Cancella") action Return()


style updater_button_text is navigation_button_text
style updater_button is confirm_button
style updater_label is gui_label
style updater_label_text is game_menu_label_text
style updater_text is gui_text







screen fake_skip_indicator():
    use skip_indicator

screen skip_indicator():

    zorder 100
    style_prefix "skip"

    frame:

        has hbox:
            spacing 6

        text _("Salto")

        text "▸" at delayed_blink(0.0, 1.0) style "skip_triangle"
        text "▸" at delayed_blink(0.2, 1.0) style "skip_triangle"
        text "▸" at delayed_blink(0.4, 1.0) style "skip_triangle"



transform delayed_blink(delay, cycle):
    alpha .5

    pause delay
    block:

        linear .2 alpha 1.0
        pause .2
        linear .2 alpha 0.5
        pause (cycle - .4)
        repeat


style skip_frame is empty
style skip_text is gui_text
style skip_triangle is skip_text

style skip_frame:
    ypos gui.skip_ypos
    background Frame("gui/skip.png", gui.skip_frame_borders, tile=gui.frame_tile)
    padding gui.skip_frame_borders.padding

style skip_text:
    size gui.notify_text_size

style skip_triangle:


    font "DejaVuSans.ttf"









screen notify(message):

    zorder 100
    style_prefix "notify"

    frame at notify_appear:
        text message

    timer 3.25 action Hide('notify')


transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0


style notify_frame is empty
style notify_text is gui_text

style notify_frame:
    ypos gui.notify_ypos

    background Frame("gui/notify.png", gui.notify_frame_borders, tile=gui.frame_tile)
    padding gui.notify_frame_borders.padding

style notify_text:
    size gui.notify_text_size







init python:

    items = [(_("Introduction"),"example_chapter") #????? wtf is this shit
        ,(_("Route Part 1, How To Make A Mod"),"tutorial_route_p1")
        ,(_("Route Part 2, Music"),"tutorial_route_p2")
        ,(_("Route Part 3, Scene"),"tutorial_route_p3")
        ,(_("Route Part 4, Dialogue"),"tutorial_route_p4")
        ,(_("Route Part 5, Menu"),"tutorial_route_p5")
        ,(_("Route Part 6, Logic Statement"),"tutorial_route_p6")
        ,(_("Route Part 7, Sprite"),"tutorial_route_p7")
        ,(_("Route Part 8, Position"),"tutorial_route_p8")
        ,(_("Route Part 9, Ending"),"tutorial_route_p9")]










define prev_adj = ui.adjustment()
define main_adj = ui.adjustment()
define gui.scrollable_menu_button_width = 560
define gui.scrollable_menu_button_height = None
define gui.scrollable_menu_button_tile = False
define gui.scrollable_menu_button_borders = Borders(25, 5, 25, 5)

define gui.scrollable_menu_button_text_font = gui.default_font
define gui.scrollable_menu_button_text_size = gui.text_size
define gui.scrollable_menu_button_text_xalign = 0.0
define gui.scrollable_menu_button_text_idle_color = "#000"
define gui.scrollable_menu_button_text_hover_color = "#fa9"


define gui.twopane_scrollable_menu_button_width = 250
define gui.twopane_scrollable_menu_button_height = None
define gui.twopane_scrollable_menu_button_tile = False
define gui.twopane_scrollable_menu_button_borders = Borders(25, 5, 25, 5)

define gui.twopane_scrollable_menu_button_text_font = gui.default_font
define gui.twopane_scrollable_menu_button_text_size = gui.text_size
define gui.twopane_scrollable_menu_button_text_xalign = 0.0
define gui.twopane_scrollable_menu_button_text_idle_color = "#000"
define gui.twopane_scrollable_menu_button_text_hover_color = "#fa9"






style scrollable_menu_vbox:
    xalign 0.5
    ypos 270
    yanchor 0.5

    spacing 5

style scrollable_menu_button is choice_button:
    properties gui.button_properties("scrollable_menu_button")

style scrollable_menu_button_text is choice_button_text:
    properties gui.button_text_properties("scrollable_menu_button")

style scrollable_menu_new_button is scrollable_menu_button

style scrollable_menu_new_button_text is scrollable_menu_button_text:
    italic True

style scrollable_menu_special_button is scrollable_menu_button

style scrollable_menu_special_button_text is scrollable_menu_button_text:
    bold True

style scrollable_menu_crazy_button is scrollable_menu_button

style scrollable_menu_crazy_button_text is scrollable_menu_button_text:
    italic True
    bold True


style twopane_scrollable_menu_vbox:
    xalign 0.5
    ypos 270
    yanchor 0.5

    spacing 5

style twopane_scrollable_menu_button is choice_button:
    properties gui.button_properties("twopane_scrollable_menu_button")

style twopane_scrollable_menu_button_text is choice_button_text:
    properties gui.button_text_properties("twopane_scrollable_menu_button")

style twopane_scrollable_menu_new_button is twopane_scrollable_menu_button

style twopane_scrollable_menu_new_button_text is twopane_scrollable_menu_button_text:
    italic True

style twopane_scrollable_menu_special_button is twopane_scrollable_menu_button

style twopane_scrollable_menu_special_button_text is twopane_scrollable_menu_button_text:
    bold True




screen twopane_scrollable_menu(prev_items, main_items, left_area, left_align, right_area, right_align, cat_length):
    style_prefix "twopane_scrollable_menu"

    fixed:
        area left_area

        bar adjustment prev_adj style "vscrollbar" xalign left_align

        viewport:
            yadjustment prev_adj
            mousewheel True
            arrowkeys True

            has vbox

            for i_caption,i_label in prev_items:
                textbutton i_caption:
                    if renpy.has_label(i_label) and not seen_event(i_label):
                        style "twopane_scrollable_menu_new_button"
                    if not renpy.has_label(i_label):
                        style "twopane_scrollable_menu_special_button"

                    action Return(i_label)



            null height 20

            if cat_length == 0:
                textbutton _("Per ora basta.") action Return(False)
            elif cat_length > 1:
                textbutton _("Vai indietro") action Return(-1)


    if main_items:

        fixed:
            area right_area

            bar adjustment main_adj style "vscrollbar" xalign right_align

            viewport:
                yadjustment main_adj
                mousewheel True
                arrowkeys True

                has vbox

                for i_caption,i_label in main_items:
                    textbutton i_caption:
                        if renpy.has_label(i_label) and not seen_event(i_label):
                            style "twopane_scrollable_menu_new_button"
                        if not renpy.has_label(i_label):
                            style "twopane_scrollable_menu_special_button"

                        action Return(i_label)

                null height 20

                textbutton _("Va bene così.") action Return(False)


screen scrollable_menu(items, display_area, scroll_align, nvm_text, remove=None):
    style_prefix "scrollable_menu"

    fixed:
        area display_area

        bar adjustment prev_adj style "vscrollbar" xalign scroll_align

        viewport:
            yadjustment prev_adj
            mousewheel True

            has vbox



            for i_caption,i_label in items:
                textbutton i_caption:
                    if renpy.has_label(i_label) and not seen_event(i_label):
                        style "scrollable_menu_new_button"
                    if not renpy.has_label(i_label):
                        style "scrollable_menu_special_button"
                    action Return(i_label)



            null height 20

            if remove:

                textbutton _(remove[0]) action Return(remove[1])

            textbutton _(nvm_text) action Return(False)

























screen mas_gen_scrollable_menu(items, display_area, scroll_align, *args):
    style_prefix "scrollable_menu"

    fixed:
        area display_area

        bar adjustment prev_adj style "vscrollbar" xalign scroll_align

        viewport:
            yadjustment prev_adj
            mousewheel True

            has vbox



            for item_prompt,item_value,is_italic,is_bold in items:
                textbutton item_prompt:
                    if is_italic and is_bold:
                        style "scrollable_menu_crazy_button"
                    elif is_italic:
                        style "scrollable_menu_new_button"
                    elif is_bold:
                        style "scrollable_menu_special_button"
                    action Return(item_value)

            for final_items in args:
                if final_items[4] > 0:
                    null height final_items[4]

                textbutton _(final_items[0]):
                    if final_items[2] and final_items[3]:
                        style "scrollable_menu_crazy_button"
                    elif final_items[2]:
                        style "scrollable_menu_new_button"
                    elif final_items[3]:
                        style "scrollable_menu_special_button"
                    action Return(final_items[1])







screen mas_background_timed_jump(timeout, timeout_label):
    timer timeout action Jump(timeout_label)


screen mas_generic_restart:




    modal True

    zorder 200

    style_prefix "confirm"

    add "gui/overlay/confirm.png"

    frame:

        has vbox:
            xalign .5
            yalign .5
            spacing 30




        label _("Riavvia Monika After Story."):
            style "confirm_prompt"
            xalign 0.5

        hbox:
            xalign 0.5
            spacing 100

            textbutton _("OK") action Return(True)



init python:
    class PauseDisplayable(renpy.Displayable):
        """
        Pause until click variant of Pause
        This is because normal pause until click is broken for some reason
        """
        import pygame
        
        def __init__(self):
            super(renpy.Displayable, self).__init__()
        
        def render(self, width, height, st, at):
            
            return renpy.Render(width, height)
        
        def event(self, ev, x, y, st):
            if ev.type == pygame.MOUSEBUTTONDOWN:
                return True
            
            raise renpy.IgnoreEvent()






screen mas_generic_poem(_poem, paper="paper", _styletext="monika_text"):
    style_prefix "poem"
    vbox:
        add paper
    viewport id "vp":
        child_size (710, None)
        mousewheel True
        draggable True
        has vbox
        null height 40
        text "[_poem.title]\n\n[_poem.text]" style _styletext
        null height 100
    vbar value YScrollValue(viewport="vp") style "poem_vbar"

