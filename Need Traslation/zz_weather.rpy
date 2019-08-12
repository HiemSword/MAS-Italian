




image room_mask = Movie(
    channel="window_1",
    play="mod_assets/window/spaceroom/window_1.webm",
    mask=None
)
image room_mask_fb = "mod_assets/window/spaceroom/window_1_fallback.png"

image room_mask2 = Movie(
    channel="window_2",
    play="mod_assets/window/spaceroom/window_2.webm",
    mask=None
)
image room_mask2_fb = "mod_assets/window/spaceroom/window_2_fallback.png"

image room_mask3 = Movie(
    channel="window_3",
    play="mod_assets/window/spaceroom/window_3.webm",
    mask=None
)
image room_mask3_fb = "mod_assets/window/spaceroom/window_3_fallback.png"

image room_mask4 = Movie(
    channel="window_4",
    play="mod_assets/window/spaceroom/window_4.webm",
    mask=None
)
image room_mask4_fb = "mod_assets/window/spaceroom/window_4_fallback.png"


image rain_mask_left = Movie(
    channel="window_5",
    play="mod_assets/window/spaceroom/window_5.webm",
    mask=None
)
image rain_mask_left_fb = "mod_assets/window/spaceroom/window_5_fallback.png"

image rain_mask_right = Movie(
    channel="window_6",
    play="mod_assets/window/spaceroom/window_6.webm",
    mask=None
)
image rain_mask_right_fb = "mod_assets/window/spaceroom/window_6_fallback.png"

image night_rain_mask_left = Movie(
    channel="window_5",
    play="mod_assets/window/spaceroom/window_5_night_rain.mp4",
    mask=None
)
image night_rain_mask_left_fb = "mod_assets/window/spaceroom/window_5_night_rain_fb.png"

image night_rain_mask_right = Movie(
    channel="window_6",
    play="mod_assets/window/spaceroom/window_6_night_rain.mp4",
    mask=None
)
image night_rain_mask_right_fb = "mod_assets/window/spaceroom/window_6_night_rain_fb.png"


image snow_mask_night_left = Movie(
    channel="window_7",
    play="mod_assets/window/spaceroom/window_7.webm",
    mask=None
)
image snow_mask_night_left_fb = "mod_assets/window/spaceroom/window_7_fallback.png"

image snow_mask_night_right = Movie(
    channel="window_8",
    play="mod_assets/window/spaceroom/window_8.webm",
    mask=None
)
image snow_mask_night_right_fb = "mod_assets/window/spaceroom/window_8_fallback.png"

image snow_mask_day_left = Movie(
    channel="window_9",
    play="mod_assets/window/spaceroom/window_9.webm",
    mask=None
)
image snow_mask_day_left_fb = "mod_assets/window/spaceroom/window_9_fallback.png"

image snow_mask_day_right = Movie(
    channel="window_10",
    play="mod_assets/window/spaceroom/window_10.webm",
    mask=None
)
image snow_mask_day_right_fb = "mod_assets/window/spaceroom/window_10_fallback.png"


image overcast_mask_left = Movie(
    channel="window_5",
    play="mod_assets/window/spaceroom/overcast_mask_left.mp4",
    mask=None
)
image overcast_mask_left_fb = "mod_assets/window/spaceroom/overcast_mask_left_fb.png"

image overcast_mask_right = Movie(
    channel="window_6",
    play="mod_assets/window/spaceroom/overcast_mask_right.mp4",
    mask=None
)
image overcast_mask_right_fb = "mod_assets/window/spaceroom/overcast_mask_right_fb.png"

image overcast_mask_left_night = Movie(
    channel="window_5",
    play="mod_assets/window/spaceroom/overcast_mask_left_night.mp4",
    mask=None
)
image overcast_mask_left_night_fb = "mod_assets/window/spaceroom/overcast_mask_left_night_fb.png"

image overcast_mask_right_night = Movie(
    channel="window_6",
    play="mod_assets/window/spaceroom/overcast_mask_right_night.mp4",
    mask=None
)
image overcast_mask_right_night_fb = "mod_assets/window/spaceroom/overcast_mask_right_night_fb.png"









image mas_island_frame_day = "mod_assets/location/special/with_frame.png"
image mas_island_day = "mod_assets/location/special/without_frame.png"
image mas_island_frame_night = "mod_assets/location/special/night_with_frame.png"
image mas_island_night = "mod_assets/location/special/night_without_frame.png"









default persistent._mas_weather_MWdata = {}



default persistent._mas_date_last_checked_rain = None


default persistent._mas_should_rain_today = None


init python in mas_weather:

    def shouldRainToday():
        
        
        if not store.persistent._mas_date_last_checked_rain or store.persistent._mas_date_last_checked_rain < datetime.date.today():
            store.persistent._mas_date_last_checked_rain = datetime.date.today()
            
            
            chance = random.randint(1,100)
            
            
            
            
            
            
            
            
            
            
            if store.mas_isSpring():
                store.persistent._mas_should_rain_today = chance >= 30
            elif store.mas_isSummer():
                store.persistent._mas_should_rain_today = chance >= 85
            elif store.mas_isFall():
                store.persistent._mas_should_rain_today = chance >= 40
            else:
                store.persistent._mas_should_rain_today = False
        
        return store.persistent._mas_should_rain_today


    def _determineCloudyWeather(
            rain_chance,
            thunder_chance,
            overcast_chance,
            rolled_chance=None
        ):
        """
        Determines if weather should be rainiy/thunder/overcase, or none of 
        those.

        IN:
            rain_chance - chance of rain out of 100
            thunder_chance - chance of thunder out of 100
                NOTE: this should be percentage based on rain chance, i.e.:
                thunder_chance * (rain_chance as %)
            overcast_chance - chance of overcast out of 100
            rolled_chance - if passed, then we use that chance instead of
                generating a random chance. None means we generate our
                own chance.
                (Default: None)

        RETURNS:
            appropriate weather type, or None if neither of these weathers.
        """
        if rolled_chance is None:
            rolled_chance = random.randint(1,100)
        
        if shouldRainToday():
            
            
            if rolled_chance <= rain_chance:
                
                
                if rolled_chance <= thunder_chance:
                    return store.mas_weather_thunder
                
                
                return store.mas_weather_rain
            
            
            
            rolled_chance -= rain_chance
        
        if rolled_chance <= overcast_chance:
            return store.mas_weather_overcast
        
        
        return None


init -20 python in mas_weather:
    import random
    import datetime
    import store


    force_weather = False


    WEATHER_MAP = {}



    WEAT_RETURN = "Nevermind"

    weather_change_time = None













    def weatherProgress():
        """
        Runs a roll on mas_shouldRain() to pick a new weather to change to after a time between half an hour - one and a half hour

        RETURNS:
            - True or false on whether or not to call spaceroom
        """
        
        
        if force_weather:
            return False
        
        
        global weather_change_time
        
        if not weather_change_time:
            weather_change_time = datetime.datetime.now() + datetime.timedelta(0,random.randint(1800,5400))
        
        elif weather_change_time < datetime.datetime.now():
            
            weather_change_time = datetime.datetime.now() + datetime.timedelta(0,random.randint(1800,5400))
            
            
            new_weather = store.mas_shouldRain()
            if new_weather is not None and new_weather != store.mas_current_weather:
                store.mas_changeWeather(new_weather)
                
                if new_weather == store.mas_weather_thunder:
                    renpy.play("mod_assets/sounds/amb/thunder_1.wav",channel="backsound")
                return True
            
            elif store.mas_current_weather != store.mas_weather_def:
                store.mas_changeWeather(store.mas_weather_def)
                return True
        
        return False


    def loadMWData():
        """
        Loads persistent MASWeather data into the weather map

        ASSUMES: weather map is already filled
        """
        if store.persistent._mas_weather_MWdata is None:
            return
        
        for mw_id, mw_data in store.persistent._mas_weather_MWdata.iteritems():
            mw_obj = WEATHER_MAP.get(mw_id, None)
            if mw_obj is not None:
                mw_obj.fromTuple(mw_data)


    def saveMWData():
        """
        Saves MASWeather data from weather map into persistent
        """
        for mw_id, mw_obj in WEATHER_MAP.iteritems():
            store.persistent._mas_weather_MWdata[mw_id] = mw_obj.toTuple()


    def unlockedWeathers():
        """
        Returns number of unlocked weather items
        """
        count = 0
        for mw_id, mw_obj in WEATHER_MAP.iteritems():
            if mw_obj.unlocked:
                count += 1
        
        return count






    def _weather_rain_entry(_old):
        """
        Rain start programming point
        """
        
        
        if _old != store.mas_weather_thunder:
            
            
            store.mas_is_raining = True
            
            
            renpy.music.play(
                store.audio.rain,
                channel="background",
                loop=True,
                fadein=1.0
            )
            
            
            store.mas_lockEVL("mas_monika_islands", "EVE") 


    def _weather_rain_exit(_new):
        """
        RAIN stop programming point
        """
        
        
        if _new != store.mas_weather_thunder:
            
            store.mas_is_raining = False
            
            
            renpy.music.stop(channel="background", fadeout=1.0)
            
            
            
            
            
            islands_ev = store.mas_getEV("mas_monika_islands")
            if (
                    islands_ev is not None
                    and islands_ev.shown_count > 0
                    and islands_ev.checkAffection(store.mas_curr_affection)
                ):
                store.mas_unlockEVL("mas_monika_islands", "EVE")







    def _weather_snow_entry(_old):
        """
        Snow entry programming point
        """
        
        store.mas_is_snowing = True
        
        
        store.mas_lockEVL("mas_monika_islands", "EVE")
        
        
        if not store.mas_weather_snow.unlocked:
            store.mas_weather_snow.unlocked = True
            saveMWData()




    def _weather_snow_exit(_new):
        """
        Snow exit programming point
        """
        
        store.mas_is_snowing = False
        
        
        islands_ev = store.mas_getEV("mas_monika_islands")
        if (
                islands_ev is not None
                and islands_ev.shown_count > 0
                and islands_ev.checkAffection(store.mas_curr_affection)
            ):
            store.mas_unlockEVL("mas_monika_islands", "EVE")




    def _weather_thunder_entry(_old):
        """
        Thunder entry programming point
        """
        
        
        
        if _old != store.mas_weather_rain:
            _weather_rain_entry(_old)
        
        
        store.mas_globals.show_lightning = True


    def _weather_thunder_exit(_new):
        """
        Thunder exit programming point
        """
        
        store.mas_globals.show_lightning = False
        
        
        
        if _new != store.mas_weather_rain:
            _weather_rain_exit(_new)


    def _weather_overcast_entry(_old):
        
        store.mas_lockEVL("mas_monika_islands", "EVE") 


    def _weather_overcast_exit(_new):
        
        islands_ev = store.mas_getEV("mas_monika_islands")
        if (
                islands_ev is not None
                and islands_ev.shown_count > 0
                and islands_ev.checkAffection(store.mas_curr_affection)
            ):
            store.mas_unlockEVL("mas_monika_islands", "EVE")


init -10 python:


    class MASWeather(object):
        """
        Weather class to determine some props for weather

        PROPERTIES:
            weather_id - Id that defines this weather object
            prompt - button label for this weater
            unlocked - determines if this weather is unlocked/selectable
            sp_left_day - image tag for spaceroom's left window in day time
            sp_right_day - image tag for spaceroom's right window in day time
            sp_left_night - image tag for spaceroom's left window in nighttime
            sp_right_night - image tag for spaceroom's right window in night
            isbg_wf_day - image PATH for islands bg daytime with frame
            isbg_wof_day = image PATH for islands bg daytime without frame
            isbg_wf_night - image PATH for island bg nighttime with frame
            isbg_wof_night - image PATH for island bg nighttime without framme

            entry_pp - programming point to execute when switching to this 
                weather
            exit_pp - programming point to execute when leaving this weather

        NOTE: for all image tags, `_fb` is appeneded for fallbacks
        """
        import store.mas_weather as mas_weather
        
        def __init__(
                self, 
                weather_id,
                prompt,
                sp_left_day,
                sp_right_day,
                sp_left_night=None,
                sp_right_night=None,
                isbg_wf_day=None,
                isbg_wof_day=None,
                isbg_wf_night=None,
                isbg_wof_night=None,
                entry_pp=None,
                exit_pp=None,
                unlocked=False
            ):
            """
            Constructor for a MASWeather object

            IN:
                weather_id - id that defines this weather object
                    NOTE: must be unique
                prompt - button label for this weathe robject
                sp_left_day - image tag for spaceroom's left window in daytime
                sp_right_day - image tag for spaceroom's right window in daytime
                unlocked - True if this weather object starts unlocked,
                    False otherwise
                    (Default: False)
                sp_left_night - image tag for spaceroom's left window in night
                    If None, we use left_day for this
                    (Default: None)
                sp_right_night - image tag ofr spaceroom's right window in
                    night
                    If None, we use right_day for this
                    (Default: None)
                isbg_wf_day - image PATH for islands bg daytime with frame
                    (Default: None)
                isbg_wof_day = image PATH for islands bg daytime without frame
                    (Default: None)
                isbg_wf_night - image PATH for island bg nighttime with frame
                    If None, we use isbg_wf_day
                    (Default: None)
                isbg_wof_night - image PATH for island bg nighttime without 
                    framme
                    If None, we use isbg_wof_day
                    (Default: None)
                entry_pp - programming point to execute after switching to 
                    this weather
                    (Default: None)
                exit_pp - programming point to execute before leaving this
                    weather
                    (Default: None)
            """
            if weather_id in self.mas_weather.WEATHER_MAP:
                raise Exception("duplicate weather ID")
            
            self.weather_id = weather_id
            self.prompt = prompt
            self.sp_left_day = sp_left_day
            self.sp_right_day = sp_right_day
            self.sp_left_night = sp_left_night
            self.sp_right_night = sp_right_night
            self.isbg_wf_day = isbg_wf_day
            self.isbg_wof_day = isbg_wof_day
            self.isbg_wf_night = isbg_wf_night
            self.isbg_wof_night = isbg_wof_night
            self.unlocked = unlocked
            self.entry_pp = entry_pp
            self.exit_pp = exit_pp
            
            
            if sp_left_night is None:
                self.sp_left_night = sp_left_day
            
            if sp_right_night is None:
                self.sp_right_night = sp_right_day
            
            
            if isbg_wf_night is None:
                self.isbg_wf_night = isbg_wf_day
            
            if isbg_wof_night is None:
                self.isbg_wof_night = isbg_wof_day
            
            
            self.mas_weather.WEATHER_MAP[weather_id] = self
        
        
        def __eq__(self, other):
            if isinstance(other, MASWeather):
                return self.weather_id == other.weather_id
            return NotImplemented
        
        
        def __ne__(self, other):
            result = self.__eq__(other)
            if result is NotImplemented:
                return result
            return not result
        
        
        def entry(self, old_weather):
            """
            Runs entry programming point
            """
            if self.entry_pp is not None:
                self.entry_pp(old_weather)
        
        
        def exit(self, new_weather):
            """
            Runs exit programming point
            """
            if self.exit_pp is not None:
                self.exit_pp(new_weather)
        
        
        def fromTuple(self, data_tuple):
            """
            Loads data from tuple

            IN:
                data_tuple - tuple of the following format:
                    [0]: unlocked property
            """
            self.unlocked = data_tuple[0]
        
        
        def sp_window(self, day):
            """
            Returns spaceroom masks for window

            IN:
                day - True if we want day time masks

            RETURNS tuple of following format:
                [0]: left window mask
                [1]: right window mask
            """
            if day:
                return (self.sp_left_day, self.sp_right_day)
            
            return (self.sp_left_night, self.sp_right_night)
        
        
        def isbg_window(self, day, no_frame):
            """
            Returns islands bg PATH for window

            IN:
                day - True if we want daytime bg
                no_frame - True if we want no frame
            """
            if day:
                if no_frame:
                    return self.isbg_wof_day
                
                return self.isbg_wf_day
            
            
            if no_frame:
                return self.isbg_wof_night
            
            return self.isbg_wf_night
        
        
        def toTuple(self):
            """
            Converts this MASWeather object into a tuple

            RETURNS: tuple of the following format:
                [0]: unlocked property
            """
            return (self.unlocked,)




init -1 python:


    mas_weather_def = MASWeather(
        "def",
        "Default",

        
        "room_mask3",
        "room_mask4",

        
        "room_mask",
        "room_mask2",

        
        "mod_assets/location/special/with_frame.png",
        "mod_assets/location/special/without_frame.png",

        
        "mod_assets/location/special/night_with_frame.png",
        "mod_assets/location/special/night_without_frame.png",

        unlocked=True
    )


    mas_weather_rain = MASWeather(
        "rain",
        "Rain",

        
        "rain_mask_left",
        "rain_mask_right",

        
        "night_rain_mask_left",
        "night_rain_mask_right",

        
        isbg_wf_day="mod_assets/location/special/rain_with_frame.png",
        isbg_wof_day="mod_assets/location/special/rain_without_frame.png",

        entry_pp=store.mas_weather._weather_rain_entry,
        exit_pp=store.mas_weather._weather_rain_exit,
        unlocked=True,
    )


    mas_weather_snow = MASWeather(
        "snow",
        "Snow",

        
        "snow_mask_day_left",
        "snow_mask_day_right",

        
        "snow_mask_night_left",
        "snow_mask_night_right",

        entry_pp=store.mas_weather._weather_snow_entry,
        exit_pp=store.mas_weather._weather_snow_exit
    )


    mas_weather_thunder = MASWeather(
        "thunder",
        "Thunder/Lightning",

        
        "rain_mask_left",
        "rain_mask_right",

        
        "night_rain_mask_left",
        "night_rain_mask_right",

        
        isbg_wf_day="mod_assets/location/special/rain_with_frame.png",
        isbg_wof_day="mod_assets/location/special/rain_without_frame.png",

        entry_pp=store.mas_weather._weather_thunder_entry,
        exit_pp=store.mas_weather._weather_thunder_exit
    )


    mas_weather_overcast = MASWeather(
        "overcast",
        "Overcast",

        
        "overcast_mask_left",
        "overcast_mask_right",

        
        "overcast_mask_left_night",
        "overcast_mask_right_night",

        
        isbg_wf_day="mod_assets/location/special/rain_with_frame.png",
        isbg_wof_day="mod_assets/location/special/rain_without_frame.png",

        entry_pp=store.mas_weather._weather_overcast_entry,
        exit_pp=store.mas_weather._weather_overcast_exit,
        unlocked=True
    )




    store.mas_weather.loadMWData()


init 800 python:

    def mas_setWeather(_weather):
        """
        Sets the initial weather.
        This is meant for startup/ch30_reset

        NOTE: this does NOt call exit programming points

        IN:
            _weather - weather to set to. 
        """
        global mas_current_weather
        old_weather = mas_current_weather
        mas_current_weather = _weather
        mas_current_weather.entry(old_weather)


    def mas_changeWeather(new_weather, by_user=None):
        """
        Changes weather without doing scene changes

        NOTE: this does NOT do scene change/spaceroom

        IN:
            new_weather - weather to change to
            by_user - flag for if user changes weather or not
        """
        
        if by_user is not None:
            mas_weather.force_weather = bool(by_user)
        
        mas_current_weather.exit(new_weather)
        mas_setWeather(new_weather)



    mas_current_weather = None
    mas_setWeather(mas_weather_def)










label mas_change_weather(new_weather, by_user=None):

    if by_user is not None:
        $ mas_weather.force_weather = bool(by_user)


    $ mas_current_weather.exit(new_weather)


    $ old_weather = mas_current_weather
    $ mas_current_weather = new_weather
    call spaceroom (dissolve_masks=True, force_exp="monika 1dsc_static") from _call_spaceroom


    $ mas_current_weather.entry(old_weather)

    return

init 5 python:

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_change_weather",
            category=["weather"],
            prompt="Can you change the weather?",
            pool=True,
            unlocked=True,
            rules={"no unlock": None},
            aff_range=(mas_aff.AFFECTIONATE, None)
        )
    )

label monika_change_weather:

    m 1hua "Sure!"

label monika_change_weather_loop:

    show monika 1eua at t21

    $ renpy.say(m, "What kind of weather would you like?", interact=False)

    python:

        import store.mas_weather as mas_weather
        import store.mas_moods as mas_moods



        weathers = [(mas_weather_def.prompt, mas_weather_def, False, False)]


        other_weathers = [
            (mw_obj.prompt, mw_obj, False, False)
            for mw_id, mw_obj in mas_weather.WEATHER_MAP.iteritems()
            if mw_id != "def" and mw_obj.unlocked
        ]


        other_weathers.sort()


        weathers.extend(other_weathers)


        weathers.append(("Progressive","auto",False,False))


        final_item = (mas_weather.WEAT_RETURN, False, False, False, 20)


    call screen mas_gen_scrollable_menu(weathers, mas_moods.MOOD_AREA, mas_moods.MOOD_XALIGN, final_item)

    $ sel_weather = _return

    show monika at t11


    if sel_weather is False:
        m 1eka "Oh, alright."
        m "If you want to change the weather, just ask, okay?"
        return

    elif sel_weather == "auto":
        if mas_weather.force_weather:
            m 1hub "Sure!"
            m 1dsc "Just give me a second.{w=0.5}.{w=0.5}.{nw}"


            $ mas_weather.force_weather = False
            m 1eua "There we go!"
            m 1eka "If you want me to change the weather, just ask. Okay?"
        else:
            m 1hua "That's the current weather, silly."
            m "Try again~"
            jump monika_change_weather_loop
        return

    if sel_weather == mas_current_weather and mas_weather.force_weather:
        m 1hua "That's the current weather, silly."
        m "Try again~"
        jump monika_change_weather_loop

    $ skip_outro = False
    $ skip_leadin = False



    if sel_weather == mas_weather_rain or sel_weather == mas_weather_thunder:
        if not renpy.seen_label("monika_rain"):
            $ pushEvent("monika_rain")
            $ skip_outro = True

        elif persistent._mas_likes_rain is False:
            m 1eka "I thought you didn't like rain."
            m 2etc "Maybe you changed your mind?"
            m 1dsc "..."
            $ skip_leadin = True



    if not skip_leadin:
        m 1eua "Alright!"
        m 1dsc "Just give me a second.{w=0.5}.{w=0.5}.{nw}"


    call mas_change_weather (sel_weather, by_user=True) from _call_mas_change_weather_1

    if not skip_outro:
        m 1eua "There we go!"
        m "If you want to change the weather again, just ask me, okay?"

    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
