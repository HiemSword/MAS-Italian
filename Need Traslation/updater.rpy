
default persistent._mas_unstable_mode = False
default persistent._mas_can_update = True


default persistent._mas_just_updated = False






define mas_updater.regular = "http://d2vycydjjutzqv.cloudfront.net/updates.json"
define mas_updater.unstable = "http://dzfsgufpiee38.cloudfront.net/updates.json"

define mas_updater.force = False
define mas_updater.timeout = 10


transform mas_updater_slide:
    xpos 641 xanchor 0 ypos -35 yanchor 0
    linear 1.0 ypos 0 yanchor 0
    time 10.0
    linear 1.0 ypos -35 yanchor 0

image mas_update_available = "mod_assets/updateavailable.png"

init -1 python:


    class MASUpdaterDisplayable(renpy.Displayable):
        
        
        
        
        
        
        
        
        import pygame 
        import time 
        import threading
        
        
        BUTTON_WIDTH = 120
        BUTTON_HEIGHT = 35
        BUTTON_BOT_SPACE = 50
        BUTTON_SPACING = 10
        
        FRAME_WIDTH = 500
        FRAME_HEIGHT = 250
        
        VIEW_WIDTH = 1280
        VIEW_HEIGHT = 720
        
        TEXT_YOFFSET = -15
        
        MOUSE_EVENTS = (
            pygame.MOUSEMOTION,
            pygame.MOUSEBUTTONUP,
            pygame.MOUSEBUTTONDOWN
        )
        
        TIMEOUT = 10 
        
        
        
        
        
        STATE_PRECHECK = -1
        
        
        
        STATE_CHECKING = 0
        
        
        
        
        STATE_BEHIND = 1
        
        
        
        
        STATE_UPDATED = 2
        
        
        
        
        STATE_TIMEOUT = 3
        
        
        
        
        STATE_NO_OK = 4
        
        
        
        
        STATE_BAD_JSON = 5
        
        
        def __init__(self, update_link):
            """
            Constructor
            """
            super(renpy.Displayable, self).__init__()
            
            self.update_link = update_link
            
            
            
            self.background = Solid(
                "#FFE6F47F",
                xsize=self.VIEW_WIDTH,
                ysize=self.VIEW_HEIGHT
            )
            
            
            self.confirm = Solid(
                "#000000B2",
                xsize=self.FRAME_WIDTH,
                ysize=self.FRAME_HEIGHT
            )
            
            
            button_idle = Image("mod_assets/hkb_idle_background.png")
            button_hover = Image("mod_assets/hkb_hover_background.png")
            button_disabled = Image("mod_assets/hkb_disabled_background.png")
            
            
            button_text_ok_idle = Text(
                "Ok",
                font=gui.default_font,
                size=gui.text_size,
                color="#000",
                outlines=[]
            )
            button_text_ok_hover = Text(
                "Ok",
                font=gui.default_font,
                size=gui.text_size,
                color="#fa9",
                outlines=[]
            )
            
            
            button_text_cancel_idle = Text(
                "Cancel",
                font=gui.default_font,
                size=gui.text_size,
                color="#000",
                outlines=[]
            )
            button_text_cancel_hover = Text(
                "Cancel",
                font=gui.default_font,
                size=gui.text_size,
                color="#fa9",
                outlines=[]
            )
            
            
            button_text_update_idle = Text(
                "Update",
                font=gui.default_font,
                size=gui.text_size,
                color="#000",
                outlines=[]
            )
            button_text_update_hover = Text(
                "Update",
                font=gui.default_font,
                size=gui.text_size,
                color="#fa9",
                outlines=[]
            )
            
            
            button_text_retry_idle = Text(
                "Retry",
                font=gui.default_font,
                size=gui.text_size,
                color="#000",
                outlines=[]
            )
            button_text_retry_hover = Text(
                "Retry",
                font=gui.default_font,
                size=gui.text_size,
                color="#fa9",
                outlines=[]
            )
            
            
            
            self._confirm_x = int((self.VIEW_WIDTH - self.FRAME_WIDTH) / 2)
            self._confirm_y = int((self.VIEW_HEIGHT - self.FRAME_HEIGHT) / 2)
            
            
            button_center_x = (
                int((self.FRAME_WIDTH - self.BUTTON_WIDTH) / 2) +
                self._confirm_x
            )
            button_center_y = (
                (self._confirm_y + self.FRAME_HEIGHT) -
                self.BUTTON_BOT_SPACE
            )
            
            
            button_left_x = (
                int(
                    (
                        self.FRAME_WIDTH -
                        (
                            (2 * self.BUTTON_WIDTH) +
                            self.BUTTON_SPACING
                        )
                    ) / 2
                ) +
                self._confirm_x
            )
            button_left_y = button_center_y
            
            
            self._button_ok = MASButtonDisplayable(
                button_text_ok_idle,
                button_text_ok_hover,
                button_text_ok_idle,
                button_idle,
                button_hover,
                button_idle,
                button_center_x,
                button_center_y,
                self.BUTTON_WIDTH,
                self.BUTTON_HEIGHT,
                hover_sound=gui.hover_sound,
                activate_sound=gui.activate_sound
            )
            
            self._button_cancel = MASButtonDisplayable(
                button_text_cancel_idle,
                button_text_cancel_hover,
                button_text_cancel_idle,
                button_idle,
                button_hover,
                button_idle,
                button_left_x + self.BUTTON_WIDTH + self.BUTTON_SPACING,
                button_left_y,
                self.BUTTON_WIDTH,
                self.BUTTON_HEIGHT,
                hover_sound=gui.hover_sound,
                activate_sound=gui.activate_sound
            )
            
            self._button_update = MASButtonDisplayable(
                button_text_update_idle,
                button_text_update_hover,
                button_text_update_idle,
                button_idle,
                button_hover,
                button_disabled,
                button_left_x,
                button_left_y,
                self.BUTTON_WIDTH,
                self.BUTTON_HEIGHT,
                hover_sound=gui.hover_sound,
                activate_sound=gui.activate_sound
            )
            
            self._button_retry = MASButtonDisplayable(
                button_text_retry_idle,
                button_text_retry_hover,
                button_text_retry_idle,
                button_idle,
                button_hover,
                button_disabled,
                button_left_x,
                button_left_y,
                self.BUTTON_WIDTH,
                self.BUTTON_HEIGHT,
                hover_sound=gui.hover_sound,
                activate_sound=gui.activate_sound
            )
            
            
            self._text_checking = Text(
                "Checking for updates...",
                font=gui.default_font,
                size=gui.text_size,
                color="#ffe6f4",
                outlines=[]
            )
            self._text_update = Text(
                "New update available!",
                font=gui.default_font,
                size=gui.text_size,
                color="#ffe6f4",
                outlines=[]
            )
            self._text_noupdate = Text(
                "No update found.",
                font=gui.default_font,
                size=gui.text_size,
                color="#ffe6f4",
                outlines=[]
            )
            self._text_timeout = Text(
                "Connection timed out.",
                font=gui.default_font,
                size=gui.text_size,
                color="#ffe6f4",
                outlines=[]
            )
            self._text_badresponse = Text(
                "Server returned bad response.",
                font=gui.default_font,
                size=gui.text_size,
                color="#ffe6f4",
                outlines=[]
            )
            self._text_badjson = Text(
                "Server returned bad JSON.",
                font=gui.default_font,
                size=gui.text_size,
                color="#ffe6f4",
                outlines=[]
            )
            
            
            self._checking_buttons = [
                self._button_update,
                self._button_cancel
            ]
            self._behind_buttons = self._checking_buttons
            self._updated_buttons = [self._button_ok]
            self._timeout_buttons = [
                self._button_retry,
                self._button_cancel
            ]
            
            
            self._state = self.STATE_PRECHECK
            
            
            self._button_update.disable()
            
            
            self._prev_time = time.time()
            
            
            self._check_thread = None
            self._thread_result = list()
        
        
        def _checkUpdate(self):
            """
            Does the purely logical update checking
            This will set the appropriate states
            """
            
            if self._state == self.STATE_CHECKING:
                
                
                
                if len(self._thread_result) > 0:
                    self._state = self._thread_result.pop()
                    
                    
                    if self._state == self.STATE_BEHIND:
                        
                        self._button_update.enable()
                
                elif time.time() - self._prev_time > self.TIMEOUT:
                    
                    self._state = self.STATE_TIMEOUT
            
            elif self._state == self.STATE_PRECHECK:
                
                
                
                self._thread_result = list()
                self._check_thread = threading.Thread(
                    target=MASUpdaterDisplayable._sendRequest,
                    args=(self.update_link, self._thread_result)
                )
                self._check_thread.start()
                self._state = self.STATE_CHECKING
        
        
        @staticmethod
        def _handleRedirect(new_url):
            """
            Attempts to connect to the redircted url

            IN:
                new_url - the redirect we want to connect to

            Returns read_json if we got a connection, Nnone otherwise
            """
            import httplib
            
            _http, double_slash, url = new_url.partition("//")
            url, single_slash, req_uri = url.partition("/")
            read_json = None
            h_conn = httplib.HTTPConnection(
                url
            )
            
            try:
                
                h_conn.connect()
                
                
                h_conn.request("GET", single_slash + req_uri)
                server_response = h_conn.getresponse()
                
                if server_response.status != 200:
                    
                    return None
                
                read_json = server_response.read()
            
            except httplib.HTTPException:
                
                return None
            
            finally:
                h_conn.close()
            
            return read_json
        
        
        
        @staticmethod
        def _sendRequest(update_link, thread_result):
            """
            Sends out the http request and returns a response and stuff
            NOTE: designed to be called as a background thread

            ASSUMES:
                _thread_result
                    appends appropriate state for use
            """
            import httplib
            import json
            
            
            
            _http, double_slash, url = update_link.partition("//")
            url, single_slash, json_file = url.partition("/")
            read_json = None
            h_conn = httplib.HTTPConnection(
                url
            )
            
            try:
                
                h_conn.connect()
                
                
                h_conn.request("GET", "/" + json_file)
                server_response = h_conn.getresponse()
                
                
                if server_response.status == 301:
                    
                    new_url = server_response.getheader("location", None)
                    
                    if new_url is None:
                        
                        thread_result.append(MASUpdaterDisplayable.STATE_NO_OK)
                        return
                    
                    
                    h_conn.close()
                    read_json = MASUpdaterDisplayable._handleRedirect(new_url)
                    
                    if read_json is None:
                        
                        thread_result.append(MASUpdaterDisplayable.STATE_NO_OK)
                        return
                
                elif server_response.status != 200:
                    
                    thread_result.append(MASUpdaterDisplayable.STATE_NO_OK)
                    return
                
                else:
                    
                    read_json = server_response.read()
            
            except httplib.HTTPException:
                
                thread_result.append(MASUpdaterDisplayable.STATE_TIMEOUT)
                return
            
            finally:
                h_conn.close()
            
            
            try:
                read_json = json.loads(read_json)
            
            except ValueError:
                
                thread_result.append(MASUpdaterDisplayable.STATE_BAD_JSON)
                return
            
            
            try:
                _mod = read_json.get("Mod", None)
            
            except:
                
                thread_result.append(MASUpdaterDisplayable.STATE_BAD_JSON)
                return
            
            if _mod is None:
                
                thread_result.append(MASUpdaterDisplayable.STATE_BAD_JSON)
                return
            
            latest_version = _mod.get("pretty_version", None)
            
            if latest_version is None:
                
                thread_result.append(MASUpdaterDisplayable.STATE_BAD_JSON)
                return
            
            
            if latest_version == config.version:
                
                thread_result.append(MASUpdaterDisplayable.STATE_UPDATED)
            
            else:
                
                thread_result.append(MASUpdaterDisplayable.STATE_BEHIND)
            
            return
        
        
        def render(self, width, height, st, at):
            """
            RENDER
            """
            
            
            self._checkUpdate()
            
            
            r = renpy.Render(width, height)
            
            
            back = renpy.render(self.background, width, height, st, at)
            confirm = renpy.render(self.confirm, width, height, st, at)
            
            if (
                    self._state == self.STATE_CHECKING
                    or self._state == self.STATE_PRECHECK
                ):
                
                display_text = renpy.render(
                    self._text_checking,
                    width,
                    height,
                    st,
                    at
                )
                display_buttons = self._checking_buttons
            
            elif self._state == self.STATE_UPDATED:
                
                display_text = renpy.render(
                    self._text_noupdate,
                    width,
                    height,
                    st,
                    at
                )
                display_buttons = self._updated_buttons
            
            elif self._state == self.STATE_BEHIND:
                
                display_text = renpy.render(
                    self._text_update,
                    width,
                    height,
                    st,
                    at
                )
                display_buttons = self._behind_buttons
            
            else:
                
                
                
                
                if self._state == self.STATE_TIMEOUT:
                    
                    display_text = renpy.render(
                        self._text_timeout,
                        width,
                        height,
                        st,
                        at
                    )
                
                elif self._state == self.STATE_NO_OK:
                    
                    display_text = renpy.render(
                        self._text_badresponse,
                        width,
                        height,
                        st,
                        at
                    )
                
                else:
                    
                    display_text = renpy.render(
                        self._text_badjson,
                        width,
                        height,
                        st,
                        at
                    )
                
                display_buttons = self._timeout_buttons
            
            
            rendered_buttons = [
                (
                    x.render(width, height, st, at),
                    (x.xpos, x.ypos)
                )
                for x in display_buttons
            ]
            
            
            pw, ph = display_text.get_size()
            
            
            r.blit(back, (0, 0))
            r.blit(confirm, (self._confirm_x, self._confirm_y))
            r.blit(
                display_text,
                (
                    int((width - pw) / 2),
                    int((height - ph) / 2) + self.TEXT_YOFFSET
                )
            )
            for vis_b, xy in rendered_buttons:
                r.blit(vis_b, xy)
            
            
            renpy.redraw(self, 1.0)
            
            return r
        
        
        def event(self, ev, x, y, st):
            """
            EVENT
            """
            if ev.type in self.MOUSE_EVENTS:
                
                if (
                        self._state == self.STATE_CHECKING
                        or self._state == self.STATE_PRECHECK
                    ):
                    
                    
                    if self._button_cancel.event(ev, x, y, st):
                        
                        return -1
                
                elif self._state == self.STATE_UPDATED:
                    
                    
                    if self._button_ok.event(ev, x, y, st):
                        
                        return -1
                
                elif self._state == self.STATE_BEHIND:
                    
                    
                    if self._button_update.event(ev, x, y, st):
                        
                        return 1
                    
                    if self._button_cancel.event(ev, x, y, st):
                        
                        return -1
                
                else:
                    
                    
                    
                    
                    if self._button_cancel.event(ev, x, y, st):
                        
                        return -1
                    
                    if self._button_retry.event(ev, x, y, st):
                        
                        self._button_update.disable()
                        self._prev_time = time.time()
                        self._state = self.STATE_PRECHECK
                
                renpy.redraw(self, 0)
            
            raise renpy.IgnoreEvent()


init python in mas_updater:


    def checkUpdate():
        """
        RETURNS:
            update_link if theres update available
            None if no update avaiable, or no need to update rn
        """
        import time
        import os
        import shutil
        
        curr_time = time.time()
        
        if renpy.game.persistent._mas_unstable_mode:
            update_link = unstable
        
        else:
            update_link = regular
        
        last_updated = renpy.game.persistent._update_last_checked.get(update_link, 0)
        
        if last_updated > curr_time:
            last_updated = 0
        
        
        game_update = os.path.normcase(renpy.config.basedir + "/game/update")
        ddlc_update = os.path.normcase(renpy.config.basedir + "/update")
        base_update = os.path.normcase(renpy.config.basedir)
        if os.access(game_update, os.F_OK):
            try:
                if os.access(ddlc_update, os.F_OK):
                    shutil.rmtree(ddlc_update)
                
                shutil.move(game_update, base_update)
                can_update = renpy.store.updater.can_update()
            
            except:
                can_update = False
        
        else:
            can_update = renpy.store.updater.can_update()
        
        
        renpy.game.persistent._mas_can_update = can_update
        
        if force:
            check_wait = 0
        else:
            
            check_wait = 3600 * 24
        
        if curr_time-last_updated > check_wait and can_update:
            return update_link
        
        return None


init 10 python:

    def _mas_backgroundUpdateCheck():
        """
        THIS IS A PRIVATE FUNCTION
        Background update check
        """
        import time
        import store.mas_updater as mas_updater
        
        update_link = mas_updater.checkUpdate()
        
        if not update_link:
            return
        
        
        thread_result = list()
        MASUpdaterDisplayable._sendRequest(update_link, thread_result)
        
        if len(thread_result) > 0:
            
            state = thread_result.pop()
            
            if state == MASUpdaterDisplayable.STATE_BEHIND:
                
                renpy.show(
                    "mas_update_available",
                    at_list=[mas_updater_slide],
                    layer="front",
                    zorder=18,
                    tag="masupdateroverlay"
                )
        
        return


    def mas_backgroundUpdateCheck():
        """
        This launches the background update thread
        """
        import threading
        
        
        the_thread = threading.Thread(
            target=_mas_backgroundUpdateCheck
        )
        the_thread.start()


init -894 python:

    def _mas_getBadFiles():
        """
        Searches through the entire mod_assets folder for any file
        with the '.new' extension and returns their paths
        RETURNS:
            a list containing the file names, list will be empty if
            there was no 'bad' files
        """
        import os
        
        return [
            os.path.join(root, file)
            for root, dirs, files in os.walk(os.path.join(config.gamedir,'mod_assets'))
                for file in files
                    if file.endswith(".new")
            ]

    def mas_cleanBadUpdateFiles():
        """
        Moves any file with the '.new' extension to the correct file
        """
        import shutil
        files = _mas_getBadFiles()
        for file in files:
            shutil.move(file, file[:-4])


    if renpy.game.persistent._mas_just_updated:
        
        mas_cleanBadUpdateFiles()
        
        renpy.game.persistent._mas_just_updated = False



label mas_updater_steam_issue:

    m 1eub "[player]!{w} I see you're using Steam."
    m 1eksdlb "Unfortunately..."
    m 1efp "I can't run the updater because Steam is a meanie!"
    m 1eksdla "You'll have to manually install the update from the releases page on the mod's website.{w} {a=http://www.monikaafterstory.com/releases.html}Click here to go to releases page{/a}."
    m 1hua "Make sure to say goodbye to me first before installing the update."
    return


label forced_update_now:
    $ mas_updater.force = True


    if persistent.steam and not persistent._mas_unstable_mode:

        $ mas_RaiseShield_core()

        call mas_updater_steam_issue from _call_mas_updater_steam_issue

        if store.mas_globals.dlg_workflow:


            $ enable_esc()
            $ mas_MUMUDropShield()
        else:


            $ mas_DropShield_core()

        return


label update_now:
    $ import time


    if persistent.steam and not persistent._mas_unstable_mode:
        return


    if renpy.showing("masupdateroverlay", layer="overlay"):
        hide masupdateroverlay

    $ update_link = store.mas_updater.checkUpdate()

    if not persistent._mas_can_update:

        python:
            no_update_dialog = (
                "Error: Failed to move 'update/' folder. Please manually " +
                "move the update folder from 'game/' to the base 'ddlc/' " +
                "directory and try again."
            )
        call screen dialog(message=no_update_dialog, ok_action=Return())

    elif update_link:


        python:
            ui.add(MASUpdaterDisplayable(update_link))
            updater_selection = ui.interact()



        if updater_selection > 0:

            $ persistent.closed_self = True
            $ persistent._mas_just_updated = True


            stop background
            stop music


            call quit from _call_quit
            $ renpy.save_persistent()
            $ updater.update(update_link, restart=True)


            $ mas_clearNotifs()


            jump _quit
        else:


            $ persistent._update_last_checked[update_link] = time.time()
    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
