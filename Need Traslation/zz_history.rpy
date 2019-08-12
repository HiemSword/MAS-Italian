init offset = -816














































































init -44 python in mas_history:
    import store
    import datetime


    if store.persistent._mas_history_archives is None:
        store.persistent._mas_history_archives = dict()


    for year in range(2017, datetime.date.today().year + 1):
        if year not in store.persistent._mas_history_archives:
            store.persistent._mas_history_archives[year] = dict()



    if store.persistent._mas_history_mhs_data is None:
        store.persistent._mas_history_mhs_data = dict()


    mhs_db = dict()


    mhs_sorted_list = list()





    L_FOUND = 0


    L_NO_YEAR = 1


    L_NO_KEY = 2



    def lookup(key, year):
        """
        Looks up data in the historical archives.

        IN:
            key - data key to lookup
            year - year to look up data

        RETURNS: a tuple of the following format:
            [0]: Lookup constant 
            [1]: retrieved data (which may be None). This is always None if
                we could not find year or key
        """
        archives = store.persistent._mas_history_archives
        
        
        data_file = archives.get(year, None)
        if data_file is None:
            return (L_NO_YEAR, None)
        
        
        if key not in data_file:
            return (L_NO_KEY, None)
        
        
        return (L_FOUND, data_file[key])


    def lookup_ot(key, *years):
        """
        Looks up data overtime in the historical archives.

        IN:
            key - data key to lookup
            years - years to look up data

        RETURNS: SEE lookup_ot_l
        """
        return lookup_ot_l(key, years)


    def lookup_otl(key, years_list):
        """
        Looks up data overtime in the historical archives.

        IN:
            key - data key to look up
            years_list - list of years to lookup data

        RETURNS: dict of the following format:
            year: tuple (SEE lookup)
        """
        found_data = dict()
        
        for year in years_list:
            found_data[year] = lookup(key, year)
        
        return found_data


    def verify(key, _verify, years_list):
        """
        Internali version of mas_HistVerify
        """
        if len(years_list) == 0:
            years_list = range(2017, datetime.date.today().year+1)
        
        found_data = lookup_otl(key, years_list)
        years_found = []
        
        for year, data_tuple in found_data.iteritems():
            status, _data = data_tuple
            
            if status == L_FOUND and _data == _verify:
                years_found.append(year)
        
        return (len(years_found) > 0, years_found)



    def _store(value, key, year):
        """
        Stores data in the historical archives.

        NOTE: will OVERWRITE data that already exists.

        IN:
            value - value to store
            key - data key to store value
            year - year to store value
        """
        store.persistent._mas_history_archives[year][key] = value



    def loadMHSData():
        """
        Loads persistent MASHistorySaver data into the mhs_db

        Also adds MHS to the sorted list and sorts it.

        ASSUMES: the mhs database is already filled
        """
        for mhs_id, mhs_data in store.persistent._mas_history_mhs_data.iteritems():
            mhs = mhs_db.get(mhs_id, None)
            if mhs is not None:
                mhs.fromTuple(mhs_data)
                mhs_sorted_list.append(mhs)
        
        mhs_sorted_list.sort(key=store.MASHistorySaver.getSortKey)


    def saveMHSData():
        """
        Saves MASHistorySaver data from mhs_db into persistent
        """
        for mhs_id, mhs in mhs_db.iteritems():
            store.persistent._mas_history_mhs_data[mhs_id] = mhs.toTuple()



    def addMHS(mhs):
        """
        Adds the given mhs to the database.

        IN:
            mhs - MASHistorySaver object to add
        
        ASSUMES that the given mhs does not conflict with existing
        """
        mhs_db[mhs.id] = mhs


    def getMHS(mhs_id):
        """
        Gets the MASHistorySaver object with the given id

        IN:
            mhs_id - id of the MASHistorySaver object to get

        RETURNS: MASHistorySaver object, or None if not found
        """
        return mhs_db.get(mhs_id, None)


init -34 python:


    def mas_HistLookup(key, year):
        """
        Looks up data in the historical archives.

        IN:
            key - data key to look up
            year - year to look up data

        RETURNS: a tuple of the following format:
            [0]: mas_history lookup constant
            [1]: retrieved data (which may be None). This is always None if
                we could not find year or key
        """
        return store.mas_history.lookup(key, year)


    def mas_HistLookup_k(year, *keys):
        """
        Looks up data in the historical archives
        NOTE: this accepts keys as string pieces that are put together

        IN:
            year - year to look up data
            keys - string pieces of a key to search for

        RETURNS: same as mas_HistLookup
        """
        return store.mas_history.lookup(".".join(keys), year)


    def mas_HistLookup_ot(key, *years):
        """
        Looks up data overtime in the historical archives.

        IN:
            key - data key to look up
            years - years to look updata

        RETURNS: dict of the following format:
            year: data tuple from mas_HistLookup
        """
        return store.mas_history.lookup_otl(key, years)


    def mas_HistLookup_otl(key, years_list):
        """
        Looks up data overtime in the historical archives.

        IN:
            key - data key to look up
            years_list - list of years to lookup data

        RETURNS: dict of the following format:
            year: data tuple from mas_HistLookup
        """
        return store.mas_history.lookup_otl(key, years_list)


    def mas_HistLookup_otl_k(years_list, *keys):
        """
        Looks up data overtime in the historical archives

        IN:
            years_list - list of years to lookup data
            *keys - string pieces of a key to search for

        RETURNS: See mas_HistLookup_otl
        """
        return store.mas_history.lookup_otl(".".join(keys), years_list)


    def mas_HistVerify(key, _verify, *years):
        """
        Verifies if data at the given key matches the verification value.

        IN:
            key - data key to lookup
            _verify - the data we want to match to
            years - years to look up data (as args)
                Dont pass in anything if you want to lookup all years since
                2017

        RETURNS: tuple of the following format:
            [0]: true/False if we found data that matched the verification
            [1]: list of years that matched the verification
        """
        return store.mas_history.verify(key, _verify, years)


    def mas_HistVerify_k(years_list, _verify, *keys):
        """
        Verifies if data at the given key matches the verification value.

        IN:
            years_list - list of years to look up data (as args)
                Pass an empty list if you want to lookup all years since
                2017.
            _verify - the data we want to match to
            *keys - string pieces of a key to search for

        RETURNS: see mas_HistVerify
        """
        return store.mas_history.verify(".".join(keys), _verify, years_list)




    class MASHistorySaver(object):
        """
        Class designed to represent mapping of historial data that we need to
        save over certain intervals.

        PROPERTIES:
            id - identifier of this MASHistorySaver object
                NOTE: Must be unique
            trigger - datetime to trigger the saving
                NOTE: this is changed automatically when saving is done
                NOTE: the trigger's year is what we use to determine where to
                    save the historical data
            mapping - mapping of persistent variable names to historical data
                keys
            use_year_before - True means that when saving data, we should use
                trigger.year - 1 as the year to determine where to save
                historical data. This is mainly for year-end events like 
                d31 and new years
            dont_reset - True means we do NOT reset the persistent var
                when doing the save.
            entry_pp - programming point called before saving data
                self is passed to this
            exitpp - programming point called after saving data
                self is passed to this
            trigger_pp - programming point called to update trigger with
                instead of the default year+1
        """
        import store.mas_history as mas_history
        
        
        first_sesh = -1
        
        def __init__(self, 
                mhs_id,
                trigger,
                mapping,
                use_year_before=False,
                dont_reset=False,
                entry_pp=None,
                exit_pp=None,
                trigger_pp=None
            ):
            """
            Constructor

            Throws exception if mhs_id is NOT unique

            IN:
                mhs_id - identifier of this MASHistorySaver object
                    NOTE: Must be unique
                trigger - datetime of when to trigger data saving for this
                    NOTE: if the year of this datetime is 2 years ahead of the
                        current year, we reset this to 1 year ahead of the
                        current year.
                    NOTE: this is changed every time we execute the saveing
                        routine
                    NOTE: trigger.year is used when saving historical data
                mapping - mapping of the persistent variable names to 
                    historical data keys
                use_year_before - True will use trigger.year-1 when saving
                    historical data instead of trigger.year. 
                    (Default: False)
                dont_reset - True will NOT reset the persistent var after
                    saving.
                    (Default: False)
                entry_pp - programming point called before saving data
                    self is passed to this
                    (Default: None)
                exit_pp - programming point called after saving data
                    self is passed to this
                    (Default: None)
                trigger_pp - if not None, this pp is called with the current
                    trigger when updating trigger, and the returned datetime 
                    is used as the new trigger.
                    (Default: None)
            """
            
            if mhs_id in self.mas_history.mhs_db:
                raise Exception(
                    "History object '{0}' already exists".format(mhs_id)
                )
            
            if MASHistorySaver.first_sesh == -1:
                if persistent.sessions is not None:
                    MASHistorySaver.first_sesh = persistent.sessions.get(
                        "first_session",
                        None
                    )
                
                else:
                    MASHistorySaver.first_sesh = None
            
            self.id = mhs_id
            self.setTrigger(trigger)  
            self.use_year_before = use_year_before
            self.mapping = mapping
            self.dont_reset = dont_reset
            self.entry_pp = entry_pp
            self.exit_pp = exit_pp
            self.trigger_pp = trigger_pp
        
        
        @staticmethod
        def getSortKey(_mhs):
            """
            Gets the sort key for this MASHistorySaver

            IN: 
                _mhs - MASHistorSaver to get sort key

            RETURNS the sort key, which is trigger datetime
            """
            return _mhs.trigger
        
        
        @staticmethod
        def correctTriggerYear(_trigger):
            """
            Determines the correct year to set trigger to.

            A triggers with a correct year are basically triggers that have not
            passed yet. It's not as simple as increasing year since we have to
            account for triggers that have yet to execute this year.

            IN:
                _trigger - trigger we are trying to change

            RETURNS: _trigger with the correct year
            """
            _now = datetime.datetime.now()
            _temp_trigger = _trigger.replace(year=_now.year)
            
            if _now > _temp_trigger:
                
                return _trigger.replace(year=_now.year + 1)
            
            
            return _temp_trigger
        
        
        def fromTuple(self, data_tuple):
            """
            Loads data from the data tuple

            IN:
                data_tuple - tuple of the following format:
                    [0]: datetime to set the trigger property
                    [1]: use_year_before 
                        - check for existence before loading
            """
            self.setTrigger(data_tuple[0])
            
            if len(data_tuple) > 1:
                self.use_year_before = data_tuple[1]
        
        
        def setTrigger(self, _trigger):
            """
            Sets the trigger of this object. This function does cleansing of
            bad trigger dates.

            IN:
                _trigger - trigger to change to
            """
            _now = datetime.datetime.now()
            
            
            
            
            first_sesh = MASHistorySaver.first_sesh
            if first_sesh is None:
                first_sesh = _now
            
            if (
                    _trigger.year > (_now.year + 1)
                    or _trigger <= first_sesh
                ):
                
                
                
                
                
                
                
                
                
                self.trigger = MASHistorySaver.correctTriggerYear(_trigger)
            
            else:
                
                self.trigger = _trigger
        
        
        def save(self):
            """
            Runs the saving routine

            NOTE: does NOT check trigger.

            NOTE: will CHANGE trigger
            """
            if self.entry_pp is not None:
                self.entry_pp(self)
            
            
            source = persistent.__dict__
            dest = self.mas_history
            save_year = self.trigger.year
            
            if self.use_year_before:
                save_year -= 1
            
            
            for p_key, data_key in self.mapping.iteritems():
                
                
                dest._store(source.get(p_key, None), data_key, save_year)
                
                
                if not self.dont_reset:
                    source[p_key] = None
            
            
            if self.trigger_pp is not None:
                self.trigger = self.trigger_pp(self.trigger)
            
            else:
                self.trigger = MASHistorySaver.correctTriggerYear(self.trigger)
            
            if self.exit_pp is not None:
                self.exit_pp(self)
        
        
        def toTuple(self):
            """
            Converts this MASHistorySaver object into a tuple

            RETURNS tuple of the following format:
                [0]: trigger - the trigger property of this object
                [1]: use_year_before - the use_year_before property of this obj
                    NOTE: needed for ease of migrations
            """
            return (self.trigger, self.use_year_before)


init 16 python in mas_history:


    def _runMHSAlg():
        """
        Runs the historical data saving algorithm

        ASSUMES:
            - mhs_db is filled with MASHistorySaver objects 
        """
        
        
        _now = datetime.datetime.now()
        index = 0
        
        
        for mhs in mhs_sorted_list:
            
            
            if mhs.trigger <= _now:
                mhs.save()


    loadMHSData()


    _runMHSAlg()


    saveMHSData()


init python in mas_delact:

    nothing = "temp"

init python in mas_history:
    from store.mas_delact import _MDA_safeadd, _MDA_saferm


init 1 python in mas_history:



    def _bday_exit_pp(mhs):
        
        
        
        
        pass



    def _pm_holdme_adj_times(elapsed):
        """
        Sets the appropraite persistent vars according to the elasped time 
        for the hold me topic
        """
        
        if store.persistent._mas_pm_longest_held_monika is None:
            store.persistent._mas_pm_longest_held_monika = elapsed
            store.persistent._mas_pm_total_held_monika = elapsed
            return
        
        
        if elapsed > store.persistent._mas_pm_longest_held_monika:
            store.persistent._mas_pm_longest_held_monika = elapsed
        
        
        store.persistent._mas_pm_total_held_monika += elapsed


init 6 python:

























    store.mas_history.addMHS(MASHistorySaver(
        "pm",
        datetime.datetime(2019, 1, 1),
        {
            
            "_mas_pm_religious": "pm.lifestyle.religious",
            "_mas_pm_like_playing_sports": "pm.lifestyle.plays_sports",
            "_mas_pm_like_playing_tennis": "pm.lifestyle.plays_tennis",
            "_mas_pm_meditates": "pm.lifestyle.meditates",
            "_mas_pm_see_therapist": "pm.lifestyle.sees_therapist",
            "_mas_pm_driving_can_drive": "pm.lifestyle.can_drive",
            "_mas_pm_driving_learning": "pm.lifestyle.learning_to_drive",
            "_mas_pm_driving_post_accident": "pm.lifestyle.driving_post_accident",
            "_mas_pm_is_fast_reader": "pm.lifestyle.reads_fast",

            
            "_mas_pm_wearsRing": "pm.lifestyle.ring.wears_one",

            
            "_mas_pm_play_jazz": "pm.lifestyle.music.play_jazz",

            
            "_mas_pm_do_smoke": "pm.lifestyle.smoking.smokes",
            "_mas_pm_do_smoke_quit": "pm.lifestyle.smoking.trying_to_quit",

            
            "_mas_pm_eat_fast_food": "pm.lifestyle.food.eats_fast_food",
            "_mas_pm_drinks_soda": "pm.lifestyle.food.drinks_soda",

            
            "_mas_pm_love_yourself": "pm.emotions.love_self",

            
            "_mas_pm_have_fam": "pm.family.have_family",
            "_mas_pm_have_fam_sibs": "pm.family.have_siblings",
            "_mas_pm_no_fam_bother": "pm.family.bothers_you",
            "_mas_pm_have_fam_mess": "pm.family.is_mess",
            "_mas_pm_have_fam_mess_better": "pm.family.will_get_better",
            "_mas_pm_no_talk_fam": "pm.family.no_talk_about",
            "_mas_pm_fam_like_monika": "pm.family.likes_monika",

            
            "_mas_pm_drawn_art": "pm.actions.drawn_art",
            "_mas_pm_has_new_years_res": "pm.actions.made_new_years_resolutions",
            "_mas_pm_accomplished_resolutions": "pm.actions.did_new_years_resolutions",
            "_mas_pm_has_bullied_people": "pm.actions.bullied_people",

            
            "_mas_pm_gamed_late": "pm.actions.games.gamed_late",

            
            "_mas_pm_ate_breakfast_times": "pm.actions.food.breakfast_times",
            "_mas_pm_ate_lunch_times": "pm.actions.food.lunch_times",
            "_mas_pm_ate_dinner_times": "pm.actions.food.dinner_times",
            "_mas_pm_ate_snack_times": "pm.actions.food.snack_times",
            "_mas_pm_ate_late_times": "pm.actions.food.late_times",

            
            "_mas_pm_d25_mistletoe_kiss": "pm.actions.monika.mistletoe_kiss",
            "_mas_pm_taken_monika_out": "pm.actions.monika.taken_out_of_sp",
            "_mas_pm_longest_held_monika": "pm.actions.monika.longest_held_time",
            "_mas_pm_total_held_monika": "pm.actions.monika.total_held_time",
            "_mas_pm_listened_to_grad_speech": "pm.actions.monika.listened_to_grad_speech",

            
            "_mas_pm_gone_to_prom": "pm.actions.prom.went",
            "_mas_pm_prom_good": "pm.actions.prom.good",
            "_mas_pm_had_prom_date": "pm.actions.prom.had_date",
            "_mas_pm_prom_monika": "pm.actions.prom.wanted_monika",
            "_mas_pm_prom_not_interested": "pm.actions.prom.no_interest",
            "_mas_pm_prom_shy": "pm.actions.prom.too_shy",
            "_mas_pm_no_prom": "pm.actions.prom.no_prom",

            
            "_mas_pm_read_yellow_wp": "pm.actions.books.read_yellow_wp",

            
            "_mas_pm_donate_charity": "pm.actions.charity.donated",
            "_mas_pm_donate_volunteer_charity": "pm.actions.charity.volunteered",

            
            "_mas_pm_added_custom_bgm": "pm.actions.mas.music.added_custom_bgm",

            
            "_mas_pm_zoomed_out": "pm.actions.mas.zoom.out",
            "_mas_pm_zoomed_in": "pm.actions.mas.zoom.in",
            "_mas_pm_zoomed_in_max": "pm.actions.mas.zoom.in_max",

            
            "_mas_pm_will_change": "pm.actions.mas.opendoor.will_change",

            
            "_mas_pm_has_rpy": "pm.actions.mas.dev.has_rpy",
            "_mas_pm_has_contributed_to_mas": "pm.actions.mas.dev.has_contributed",
            "_mas_pm_wants_to_contribute_to_mas": "pm.actions.mas.dev.wants_to_contribute",

            
            "_mas_pm_live_in_city": "pm.location.live_in_city",
            "_mas_pm_live_near_beach": "pm.location.live_near_beach",
            "_mas_pm_live_south_hemisphere": "pm.location.south_hemi",
            "_mas_pm_gets_snow": "pm.location.snows",

            
            "_mas_pm_likes_horror": "pm.likes.horror",
            "_mas_pm_likes_spoops": "pm.likes.spooks",
            "_mas_pm_watch_mangime": "pm.likes.manga_and_anime",
            "_mas_pm_would_like_mt_peak": "pm.likes.reach_mt_peak",

            
            "_mas_pm_likes_singing_d25_carols": "pm.likes.d25.singing_carols",

            
            "_mas_pm_a_hater": "pm.likes.monika.not",
            "_mas_pm_liked_grad_speech": "pm.likes.monika.grad_speech",

            
            "_mas_pm_like_rap": "pm.likes.music.rap",
            "_mas_pm_like_vocaloids": "pm.likes.music.vocaloids",
            "_mas_pm_like_rock_n_roll": "pm.likes.music.rock_n_roll",
            "_mas_pm_like_orchestral_music": "pm.likes.music.orchestral",
            "_mas_pm_like_jazz": "pm.likes.music.jazz",
            "_mas_pm_like_other_music": "pm.likes.music.other",

            
            "_mas_pm_like_mint_ice_cream": "pm.likes.food.mint_ice_cream",

            
            "_mas_pm_likes_panties": "pm.likes.clothes.panties",
            "_mas_pm_no_talk_panties": "pm.likes.clothes.panties.no_talk",

            
            "_mas_pm_cares_about_dokis": "pm.likes.dokis.cares_about_them",

            
            
            "_mas_pm_lang_other": "pm.know.lang.other",
            "_mas_pm_lang_jpn": "pm.know.lang.jpn",

            
            "_mas_pm_given_false_justice": "pm.exp.given_false_justice",
            "_mas_pm_driving_been_in_accident": "pm.exp.been_in_car_accident",
            "_mas_pm_is_bullying_victim": "pm.exp.victim_of_bullying",
            "_mas_pm_currently_bullied": "pm.exp.currently_being_bullied",

            
            
            "_mas_pm_monika_deletion_justice": "pm.op.monika.delmoni_justified",
            "_mas_pm_monika_evil": "pm.op.monika.is_evil",
            "_mas_pm_monika_evil_but_ok": "pm.op.monika.is_evil_but_it_ok",
            "_mas_pm_monika_cute_as_natsuki": "pm.op.monika.is_cute_as_natsuki",

            
            "_mas_pm_shared_appearance": "pm.looks.shared_looks",

            
            "_mas_pm_eye_color": "pm.looks.eyes.color",

            
            "_mas_pm_hair_color": "pm.looks.hair.color",
            "_mas_pm_hair_length": "pm.looks.hair.length",
            "_mas_pm_shaved_hair": "pm.looks.hair.shaved",
            "_mas_pm_no_hair_no_talk": "pm.looks.hair.no_talk",

            
            "_mas_pm_skin_tone": "pm.looks.skin.tone",

            
            "_mas_pm_height": "pm.looks.dims.height",
            "_mas_pm_units_height_metric": "pm.looks.dims.height_is_metric",

            
            "_mas_pm_would_come_to_spaceroom": "pm.future.goto_spaceroom",

            
            "_mas_pm_owns_car": "pm.owns.car",
            "_mas_pm_owns_car_type": "pm.owns.car_type",

        },
        use_year_before=True,
        dont_reset=True
    ))




    store.mas_history.addMHS(MASHistorySaver(
        "922",
        datetime.datetime(2018, 9, 30),
        

        {
            "_mas_bday_opened_game": "922.actions.opened_game",
            "_mas_bday_no_time_spent": "922.actions.no_time_spent",
            "_mas_bday_no_recognize": "922.actions.no_recognize",
            "_mas_bday_said_happybday": "922.actions.said_happybday",
            "_mas_bday_date_count": "922.actions.date.count",
            "_mas_bday_date_affection_lost": "922.actions.date.aff_lost",
            "_mas_bday_date_affection_gained": "922.actions.date.aff_gained",
            "_mas_bday_sbp_aff_given": "922.actions.surprise.aff_given",
            "_mas_bday_sbp_reacted": "922.actions.surprise.reacted",
            "_mas_bday_sbp_found_cake": "922.actions.surprise.found_cake",
            "_mas_bday_sbp_found_banners": "922.actions.surprise.found_banners",
            "_mas_bday_sbp_found_balloons": "922.actions.surprise.found_balloons"
        },
        exit_pp=store.mas_history._bday_exit_pp
    ))


    store.mas_history.addMHS(MASHistorySaver(
        "aff",
        datetime.datetime(2019, 1, 2),
        {
            "_mas_aff_before_fresh_start": "aff.before_fresh_start"
        },
        use_year_before=True
    ))
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
