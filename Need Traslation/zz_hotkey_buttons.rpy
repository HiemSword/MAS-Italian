


init python:


    def HKBHideButtons():
        
        
        
        if mas_HKBIsVisible():
            config.overlay_screens.remove("hkb_overlay")
            renpy.hide_screen("hkb_overlay")



    def HKBShowButtons():
        
        
        
        if not mas_HKBIsVisible():
            config.overlay_screens.append("hkb_overlay")


    def mas_HKBRaiseShield():
        """RUNTIME ONLY
        Disables the hotkey buttons
        """
        store.hkb_button.talk_enabled = False
        store.hkb_button.extra_enabled = False
        store.hkb_button.music_enabled = False
        store.hkb_button.play_enabled = False


    def mas_HKBDropShield():
        """RUNTIME ONLY
        Enables the hotkey buttons
        """
        store.hkb_button.talk_enabled = True
        store.hkb_button.extra_enabled = True
        store.hkb_button.music_enabled = True
        store.hkb_button.play_enabled = True


    def mas_HKBIsEnabled():
        """
        RETURNS: True if all the buttons are enabled, False otherwise
        """
        return (
            store.hkb_button.talk_enabled
            and store.hkb_button.music_enabled
            and store.hkb_button.play_enabled
            and store.hkb_button.extra_enabled
        )


    def mas_HKBIsVisible():
        """
        RETURNS: True if teh Hotkey buttons are visible, False otherwise
        """
        return "hkb_overlay" in config.overlay_screens



    def MovieOverlayHideButtons():
        
        
        
        if "movie_overlay" in config.overlay_screens:
            config.overlay_screens.remove("movie_overlay")
            renpy.hide_screen("movie_overlay")


    def MovieOverlayShowButtons():
        
        
        
        config.overlay_screens.append("movie_overlay")


init -1 python in hkb_button:


    talk_enabled = True


    extra_enabled = True


    music_enabled = True


    play_enabled = True


    movie_buttons_enabled = False







define gui.hkb_button_width = 120
define gui.hkb_button_height = None
define gui.hkb_button_tile = False

define gui.hkb_button_text_font = gui.default_font
define gui.hkb_button_text_size = gui.text_size
define gui.hkb_button_text_xalign = 0.5

define gui.hkb_button_text_idle_color = "#000"
define gui.hkb_button_text_hover_color = "#fa9"
define gui.hkb_button_text_kerning = 0.2



style hkb_vbox is vbox
style hkb_button is button
style hkb_button_text is button_text

style hkb_vbox:
    spacing 0

style hkb_button is default:
    properties gui.button_properties("hkb_button")
    idle_background "mod_assets/hkb_idle_background.png"
    hover_background "mod_assets/hkb_hover_background.png"
    ypadding 5

    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style hkb_button_text is default:
    properties gui.button_text_properties("hkb_button")
    outlines []


style hkbd_vbox is vbox
style hkbd_button is button
style hkbd_button_text is button_text

style hkbd_vbox:
    spacing 0

style hkbd_button is default:
    properties gui.button_properties("hkb_button")
    idle_background "mod_assets/hkb_disabled_background.png"
    hover_background "mod_assets/hkb_disabled_background.png"

style hkbd_button_text is default:

    font gui.default_font
    size gui.text_size
    idle_color "#000"
    hover_color "#000"
    kerning 0.2
    outlines []

style hkb_text is default:
    xalign 0.5
    size gui.text_size
    font gui.default_font
    color "#000"
    kerning 0.2
    outlines []

screen hkb_overlay():

    zorder 50

    style_prefix "hkb"

    vbox:
        xpos 0.05

        yanchor 1.0
        ypos 715


        if store.hkb_button.talk_enabled:
            textbutton _("Talk") action Function(show_dialogue_box)
        else:
            frame:
                ypadding 5
                xsize 120

                background Image("mod_assets/hkb_disabled_background.png")
                text "Talk"


        if store.hkb_button.extra_enabled:
            textbutton _("Extra") action Function(mas_open_extra_menu)
        else:
            frame:
                ypadding 5
                xsize 120

                background Image("mod_assets/hkb_disabled_background.png")
                text "Extra"


        if store.hkb_button.music_enabled:
            textbutton _("Music") action Function(select_music)
        else:
            frame:
                ypadding 5
                xsize 120

                background Image("mod_assets/hkb_disabled_background.png")
                text "Music"


        if store.hkb_button.play_enabled:
            textbutton _("Play") action Function(pick_game)
        else:
            frame:
                ypadding 5
                xsize 120

                background Image("mod_assets/hkb_disabled_background.png")
                text "Play"


screen movie_overlay():

    zorder 50

    style_prefix "hkb"

    vbox:
        xalign 0.95
        yalign 0.95

        if watchingMovie:
            textbutton _("Pause") action Jump("mm_movie_pausefilm")
        else:
            textbutton _("Pause") action NullAction() style "hkbd_button"

        if watchingMovie:
            textbutton _("Time") action Jump("mm_movie_settime")
        else:
            textbutton _("Time"):
                action NullAction()
                style "hkbd_button"

init python:
    HKBShowButtons()
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
