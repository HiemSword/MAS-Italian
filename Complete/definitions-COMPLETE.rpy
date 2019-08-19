define persistent.demo = False
define persistent.steam = False
define config.developer = False

init 1 python:
    persistent.steam = "steamapps" in config.basedir.lower()

python early:
    import singleton
    me = singleton.SingleInstance()

    MAS_MONIKA_Z = 10
    MAS_BACKGROUND_Z =5


    import datetime


    import traceback
    _dev_tb_list = []






    EV_ACT_PUSH = "push"
    EV_ACT_QUEUE = "queue"
    EV_ACT_UNLOCK = "unlock"
    EV_ACT_RANDOM = "random"
    EV_ACT_POOL = "pool"


    EV_ACTIONS = [
        EV_ACT_PUSH,
        EV_ACT_QUEUE,
        EV_ACT_UNLOCK,
        EV_ACT_RANDOM,
        EV_ACT_POOL
    ]


    class EventException(Exception):
        def __init__(self, _msg):
            self.msg = _msg
        def __str__(self):
            return "EventError: " + self.msg

















































































    class Event(object):
        
        
        T_EVENT_NAMES = {
            "eventlabel":0,
            "prompt":1,
            "label":2,
            "category":3,
            "unlocked":4,
            "random":5,
            "pool":6,
            "conditional":7,
            "action":8,
            "start_date":9,
            "end_date":10,
            "unlock_date":11,
            "shown_count":12,
            "diary_entry":13,
            "last_seen":14,
            "years":15,
            "sensitive":16,
            "aff_range":17,
            "show_in_idle":18,
        }
        
        
        N_EVENT_NAMES = ("per_eventdb", "eventlabel", "locks", "rules")
        
        
        DIARY_LIMIT = 500
        
        
        
        
        
        
        
        INIT_LOCKDB = None
        
        
        
        
        
        
        ACTION_MAP = dict()
        
        
        
        def __init__(self,
                per_eventdb,
                eventlabel,
                prompt=None,
                label=None,
                category=None,
                unlocked=False,
                random=False,
                pool=False,
                conditional=None,
                action=None,
                start_date=None,
                end_date=None,
                unlock_date=None,
                diary_entry=None,
                rules=dict(),
                last_seen=None,
                years=None,
                sensitive=False,
                aff_range=None,
                show_in_idle=False
            ):
            
            
            if not eventlabel:
                raise EventException("'_eventlabel' cannot be None")
            if per_eventdb is None:
                raise EventException("'per_eventdb' cannot be None")
            if action is not None and action not in EV_ACTIONS:
                raise EventException("'" + action + "' is not a valid action")
            if diary_entry is not None and len(diary_entry) > self.DIARY_LIMIT:
                raise Exception(
                    (
                        "diary entry for {0} is longer than {1} characters"
                    ).format(eventlabel, self.DIARY_LIMIT)
                )
            if rules is None:
                raise Exception(
                    "'{0}' - rules property cannot be None".format(eventlabel)
                )
            if (
                    start_date is not None
                    and type(start_date) is not datetime.datetime
                    and type(start_date) is not datetime.date
                ):
                raise Exception(
                    "'{0}' - invalid start date.".format(eventlabel)
                )
            if (
                    end_date is not None
                    and type(end_date) is not datetime.datetime
                    and type(end_date) is not datetime.date
                ):
                raise Exception(
                    "'{0}' - invalid end date.".format(eventlabel)
                )
            if years is not None and type(years) is not list:
                raise Exception(
                    "'{0}' - invalid years.".format(eventlabel)
                )
            
            
            
            if aff_range is not None:
                low, high = aff_range
                if low is None and high is None:
                    aff_range = None
            
            
            
            if not store.mas_affection._isValidAffRange(aff_range):
                raise Exception("{0} | bad aff range: {1}".format(
                    eventlabel, str(aff_range)
                ))
            
            self.eventlabel = eventlabel
            self.per_eventdb = per_eventdb
            
            
            if not prompt:
                prompt = self.eventlabel
            
            
            if not label:
                label = prompt
            
            
            if type(start_date) is datetime.date:
                start_date = datetime.datetime.combine(
                    start_date,
                    datetime.time.min
                )
            if type(end_date) is datetime.date:
                end_date = datetime.datetime.combine(
                    end_date,
                    datetime.time.min
                )
            
            self.rules = rules
            
            
            
            
            data_row = (
                self.eventlabel,
                prompt,
                label,
                category,
                unlocked,
                random,
                pool,
                conditional,
                action,
                start_date,
                end_date,
                unlock_date,
                0, 
                diary_entry,
                last_seen,
                years,
                sensitive,
                aff_range,
                show_in_idle
            )
            
            stored_data_row = self.per_eventdb.get(eventlabel, None)
            
            
            
            if stored_data_row:
                
                stored_data_list = list(stored_data_row)
                
                
                lock_entry = Event.INIT_LOCKDB.get(eventlabel, None)
                
                if lock_entry:
                    
                    if len(stored_data_row) < len(data_row):
                        
                        
                        
                        stored_data_list.extend(
                            data_row[len(stored_data_row):]
                        )
                    
                    
                    
                    for name,index in Event.T_EVENT_NAMES.iteritems():
                        
                        if not lock_entry[index]:
                            stored_data_list[index] = data_row[index]
                    
                    self.per_eventdb[eventlabel] = tuple(stored_data_list)
                
                else:
                    
                    
                    if len(stored_data_row) < len(data_row):
                        
                        data_row = list(data_row)
                        data_row[0:len(stored_data_list)] = stored_data_list
                        self.per_eventdb[self.eventlabel] = tuple(data_row)
                    
                    
                    self.prompt = prompt
                    self.category = category
                    self.diary_entry = diary_entry
                    
                    self.years = years
                    self.sensitive = sensitive
                    self.aff_range = aff_range
                    self.show_in_idle = show_in_idle
            
            
            else:
                
                self.per_eventdb[self.eventlabel] = data_row
            
            
            Event.INIT_LOCKDB.setdefault(eventlabel, mas_init_lockdb_template)
        
        
        
        def __eq__(self, other):
            if isinstance(self, other.__class__):
                return self.eventlabel == other.eventlabel
            return False
        
        
        def __ne__(self, other):
            return not self.__eq__(other)
        
        
        def __setattr__(self, name, value):
            
            
            
            if name in self.N_EVENT_NAMES:
                super(Event, self).__setattr__(name, value)
            
            
            
            
            else:
                attr_loc = self.T_EVENT_NAMES.get(name, None)
                
                if attr_loc:
                    
                    data_row = self.per_eventdb.get(self.eventlabel, None)
                    
                    if not data_row:
                        
                        raise EventException(
                            self.eventlabel + " not found in eventdb"
                        )
                    
                    
                    
                    if name == "start_date" or name == "end_date":
                        if type(value) is datetime.date:
                            value = datetime.datetime.combine(
                                value,
                                datetime.time.min
                            )
                        
                        
                        if type(value) is not datetime.datetime:
                            value = None
                    
                    
                    data_row = list(data_row)
                    data_row[attr_loc] = value
                    data_row = tuple(data_row)
                    
                    
                    self.per_eventdb[self.eventlabel] = data_row
                
                else:
                    raise EventException(
                        "'{0}' is not a valid attribute for Event".format(name)
                    )
        
        
        def __getattr__(self, name):
            attr_loc = self.T_EVENT_NAMES.get(name, None)
            
            if attr_loc:
                
                data_row = self.per_eventdb.get(self.eventlabel, None)
                
                if not data_row:
                    
                    raise EventException(
                        self.eventlabel + " not found in db"
                    )
                
                
                return data_row[attr_loc]
            
            else:
                return super(Event, self).__getattribute__(name)
        
        
        def monikaWantsThisFirst(self):
            """
            Checks if a special instant key is in this Event's rule dict

            RETURNS: True if the this key is here, false otherwise
            """
            return (
                self.rules is not None
                and "monika wants this first" in self.rules
            )
        
        
        def checkAffection(self, aff_level):
            """
            Checks if the given aff_level is within range of this event's
            aff_range.

            IN:
                aff_level - aff_level to check

            RETURNS: True if aff_level is within range of event's aff_range,
                False otherwise
            """
            if self.aff_range is None:
                return True
            
            
            low, high = self.aff_range
            return store.mas_affection._betweenAff(low, aff_level, high)
        
        
        def canRepeat(self):
            """
            Checks if this event has the vars to enable repeat

            RETURNS: True if this event can repeat, False if not
            """
            return (
                self.start_date is not None
                and self.end_date is not None
                and self.years is not None
            )
        
        
        def prepareRepeat(self, force=False):
            """
            Prepres this event's dates for a repeat.

            NOTE: does not check if the event hasnt been reached this year.

            IN:
                force - If True, we force the years to change
                    (Default: False)

            RETURNS: True if this event can repeat, False if not
            """
            
            if not self.canRepeat():
                return False
            
            new_start, new_end, was_changed = Event._yearAdjustEV(self, force)
            
            if was_changed:
                self.start_date = new_start
                self.end_date = new_end
            
            return True
        
        
        @staticmethod
        def getSortPrompt(ev):
            
            
            
            return renpy.substitute(ev.prompt).lower()
        
        
        @staticmethod
        def getSortShownCount(ev):
            """
            Function used for sorting by shown counts

            RETURNS: the shown_count property of an event
            """
            return ev.shown_count
        
        @staticmethod
        def lockInit(name, ev=None, ev_label=None):
            """
            Locks the property for a given event object or eventlabel.
            This will prevent the property from being overwritten on object
            creation.

            IN:
                name - name of property to lock
                ev - Event object to property lock
                    (Default: None)
                ev_label - event label of Event to property lock
                    (Default: None)
            """
            Event._modifyInitLock(name, True, ev=ev, ev_label=ev_label)
        
        
        @staticmethod
        def unlockInit(name, ev=None, ev_label=None):
            """
            Unlocks the property for a given event object or event label.
            This will allow the property to be overwritten on object creation.

            IN:
                name - name of property to lock
                ev - Event object to property lock
                    (Default: None)
                ev_label - event label of Event to property lock
                    (Default: None)
            """
            Event._modifyInitLock(name, False, ev=ev, ev_label=ev_label)
        
        
        @staticmethod
        def _modifyInitLock(name, value, ev=None, ev_label=None):
            """
            Modifies the init lock for a given event/eventlabel

            IN:
                name - name of property to modify
                value - value to set the property
                ev - Eveng object to property lock
                    (Default: None)
                ev_label - event label of Event to property lock
                    (Default: None)
            """
            
            if ev is None and ev_label is None:
                return
            
            
            property_dex = Event.T_EVENT_NAMES.get(name, None)
            if property_dex is None:
                return
            
            
            if ev:
                ev_label = ev.eventlabel
            
            
            lock_entry = list(Event.INIT_LOCKDB[ev_label])
            lock_entry[property_dex] = value
            Event.INIT_LOCKDB[ev_label] = tuple(lock_entry)
        
        
        @staticmethod
        def _verifyAndSetDatesEV(ev):
            """
            Runs _verifyDatesEV and sets the event properties if change
            happens

            IN:
                ev - event object to verify and set
            """
            new_start, new_end, was_changed = Event._verifyDatesEV(ev)
            if was_changed:
                ev.start_date = new_start
                ev.end_date = new_end
        
        
        @staticmethod
        def _verifyDatesEV(ev):
            """
            _verifyDates, but for an Event object.

            IN:
                ev - event object to verify dates

            RETURNS: See _verifyDates
            """
            return Event._verifyDates(ev.start_date, ev.end_date, ev.years)
        
        
        @staticmethod
        def _yearAdjustEV(ev, force=False):
            """
            _yearAdjust, but for an Event object

            IN:
                ev - evnet object to adjust years
                force - if True, we force years to update
                    (Default: False)

            RETURNS: See _verifyDates
            """
            return Event._yearAdjust(
                ev.start_date,
                ev.end_date,
                ev.years,
                force
            )
        
        
        @staticmethod
        def _verifyDates(_start, _end, _years):
            """
            Given start/end/_yeras, figure out the appropriate start and end
            dates. We use current datetime to figure this out.

            NOTE: this is meant for Event use ONLY
            NOTE: this is NOT meant to be used with an Event object.
                See _verifyDatesEV

            IN:
                _start - start datetime
                _end - end datetime (exclusive)
                _years - years list

            RETURNS tuple of the following format:
                [0]: start datetime to use
                [1]: end datetime to use
                [2]: True if there was and adjustment, False if not
            """
            
            if _start is None or _end is None or _years is None:
                
                return (_start, _end, False)
            
            
            return Event._yearAdjust(_start, _end, _years)
        
        
        @staticmethod
        def _yearAdjust(_start, _end, _years, force=False):
            """
            Performs the year adjustment algorithm.

            IN:
                force - If True, we force year to update
                    (Default: False)

            RETURNS: see _verifyDates
            """
            _now = datetime.datetime.now()
            
            
            if (_start <= _now < _end) and not force:
                return (_start, _end, False)
            
            
            add_yr_fun = store.mas_utils.add_years
            
            if len(_years) == 0:
                
                
                if force:
                    
                    return (add_yr_fun(_start, 1), add_yr_fun(_end, 1), True)
                
                
                
                diff = _now.year - _start.year
                new_end = add_yr_fun(_end, diff)
                
                if new_end <= _now:
                    
                    diff += 1
                    new_end = add_yr_fun(_end, diff)
                
                
                return (add_yr_fun(_start, diff), new_end, True)
            
            
            if force:
                
                
                new_years = [
                    year
                    for year in _years
                    if year > _now.year
                ]
            
            else:
                new_years = [
                    year
                    for year in _years
                    if year >= _now.year
                ]
            
            if len(new_years) == 0:
                
                return (_start, _end, False)
            
            new_years.sort()
            
            
            diff = _now.year - new_years[0]
            new_end = add_yr_fun(_end, diff)
            
            if force:
                
                return (add_yr_fun(_start, diff), new_end, True)
            
            if new_end <= _now:
                if len(new_years) <= 1:
                    
                    return (_start, _end, False)
                
                
                diff = _now.year - new_years[1]
                new_end = add_yr_fun(_end, diff)
            
            return (add_yr_fun(_start, diff), new_end, True)
        
        
        @staticmethod
        def _getNextYear(_years, year_comp):
            """
            Retreieves the next possible year into the future from the given
            years list.

            NOTE: if empty list, we return current year.

            IN:
                _years - list of years
                year_comp - year to start search from.

            RETURNS next possible year into the future from the given years
                list. If _years is empty, current year is returned.
                If unable to find a next year, we return None.
            """
            
            if len(_years) == 0:
                return datetime.date.today().year
            
            
            new_years = [
                year
                for year in _years
                if year > year_comp
            ]
            
            
            if len(new_years) == 0:
                return None
            
            
            return sorted(new_years)[0]
        
        
        @staticmethod
        def _filterEvent(
                event,
                category=None,
                unlocked=None,
                random=None,
                pool=None,
                action=None,
                seen=None,
                excl_cat=None,
                moni_wants=None,
                sensitive=None,
                aff=None,
            ):
            
            
            
            
            
            
            
            
            
            
            
            from collections import Counter
            
            
            if unlocked is not None and event.unlocked != unlocked:
                return False
            
            if random is not None and event.random != random:
                return False
            
            if pool is not None and event.pool != pool:
                return False
            
            if aff is not None and not event.checkAffection(aff):
                return False
            
            if seen is not None and renpy.seen_label(event.eventlabel) != seen:
                return False
            
            if category is not None:
                
                if category[0]:
                    if not event.category or len(set(category[1]).intersection(set(event.category))) == 0:
                        return False
                
                
                elif not event.category or len(set(category[1]).intersection(set(event.category))) != len(category[1]):
                    return False
            
            if action is not None and event.action not in action:
                return False
            
            if excl_cat is not None:
                
                if not excl_cat and event.category:
                    return False
                
                
                if event.category and len(set(excl_cat).intersection(set(event.category))) > 0:
                    return False
            
            
            if sensitive is not None and event.sensitive != sensitive:
                return False
            
            
            if moni_wants is not None and event.monikaWantsThisFirst() != moni_wants:
                return False
            
            
            return True
        
        @staticmethod
        def filterEvents(
                events,

                category=None,
                unlocked=None,
                random=None,
                pool=None,
                action=None,
                seen=None,
                excl_cat=None,
                moni_wants=None,
                sensitive=None,
                aff=None
            ):
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            if (not events or len(events) == 0 or (
                    category is None
                    and unlocked is None
                    and random is None
                    and pool is None
                    and action is None
                    and seen is None
                    and excl_cat is None
                    and moni_wants is None
                    and sensitive is None
                    and aff is None)):
                return events
            
            
            
            
            
            
            if (category and (
                    len(category) < 2
                    or category[0] is None
                    or category[1] is None
                    or len(category[1]) == 0)):
                category = None
            if action and len(action) == 0:
                action = None
            if sensitive is None:
                try:
                    
                    if persistent._mas_sensitive_mode:
                        sensitive = False
                except:
                    pass
            
            filt_ev_dict = dict()
            
            
            for k,v in events.iteritems():
                
                if Event._filterEvent(v,category=category, unlocked=unlocked,
                        random=random, pool=pool, action=action, seen=seen,
                        excl_cat=excl_cat,moni_wants=moni_wants,
                        sensitive=sensitive, aff=aff):
                    
                    filt_ev_dict[k] = v
            
            return filt_ev_dict
        
        @staticmethod
        def getSortedKeys(events, include_none=False):
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            if not events or len(events) == 0:
                return []
            
            
            ev_list = events.values() 
            
            
            if include_none:
                none_labels = list()
            
            
            eventlabels = list()
            for ev in ev_list:
                
                if ev.unlock_date is not None:
                    index = 0
                    
                    while (index < len(eventlabels)
                            and ev.unlock_date < events[
                                eventlabels[index]
                            ].unlock_date):
                        index += 1
                    eventlabels.insert(index, ev.eventlabel)
                
                elif include_none: 
                    none_labels.append(ev.eventlabel)
            
            if include_none:
                eventlabels.extend(none_labels)
            
            
            if len(eventlabels) == 0:
                return []
            
            return eventlabels
        
        @staticmethod
        def checkConditionals(events, rebuild_ev=False):
            
            
            
            
            
            
            
            
            
            import datetime
            
            
            if not events or len(events) == 0:
                return None
            
            _now = datetime.datetime.now()
            
            for ev_label,ev in events.iteritems():
                
                
                
                
                
                
                
                
                
                if (
                        
                        ev.conditional is not None

                        
                        and ev.checkAffection(mas_curr_affection)

                        
                        and ev.start_date is None
                        and ev.end_date is None

                        
                        and ev.action in Event.ACTION_MAP

                        
                        and eval(ev.conditional)
                    ):
                    
                    
                    Event._performAction(
                        ev,
                        unlock_time=_now,
                        rebuild_ev=rebuild_ev
                    )
                    
                    
                    ev.conditional = None
            
            
            return events
        
        @staticmethod
        def checkCalendar(events):
            
            
            
            
            
            import datetime
            
            
            if not events or len(events) == 0:
                return None
            
            
            ev_list = events.keys() 
            
            current_time = datetime.datetime.now()
            
            for ev in ev_list:
                
                e = events[ev]
                
                
                if (e.start_date is None) and (e.end_date is None):
                    continue
                
                
                if e.start_date is not None:
                    if e.start_date > current_time:
                        continue
                
                if e.end_date is not None:
                    if e.end_date <= current_time:
                        continue
                
                if e.conditional is not None:
                    if not eval(e.conditional):
                        continue
                
                
                if e.action in Event.ACTION_MAP:
                    
                    Event._performAction(e, unlock_time=current_time)
                    
                    
                    if e.years is not None:
                        
                        
                        if len(e.years) == 0:
                            
                            
                            e.start_date = store.mas_utils.add_years(e.start_date, 1)
                            e.end_date = store.mas_utils.add_years(e.end_date, 1)
                            continue
                        
                        
                        new_years = [year for year in e.years if year > e.start_date.year]
                        
                        
                        if len(new_years) > 0:
                            
                            new_years.sort()
                            
                            
                            new_year = new_years[0]
                            
                            
                            diff = new_year - e.start_date.year
                            
                            
                            e.start_date = store.mas_utils.add_years(e.start_date, diff)
                            e.end_date = store.mas_utils.add_years(e.end_date, diff)
                            continue
                    
                    
                    events[ev].conditional = "False"
            
            return events
        
        
        @staticmethod
        def _checkEvent(ev, curr_time):
            """
            Singular filter function for checkEvents

            RETURNS: True if passes filter, False if not
            """
            
            if ev.start_date is None and ev.conditional is None:
                return False
            
            
            if not ev.checkAffection(mas_curr_affection):
                return False
            
            
            if ev.start_date is not None and ev.start_date > curr_time:
                return False
            
            if ev.end_date is not None and ev.end_date <= curr_time:
                return False
            
            
            if ev.conditional is not None and not eval(ev.conditional):
                return False
            
            
            if ev.action not in Event.ACTION_MAP:
                return False
            
            
            return True
        
        
        @staticmethod
        def checkEvents(ev_dict, rebuild_ev=True):
            """
            This acts as a combination of both checkConditoinal and
            checkCalendar

            does NOT return dict
            """
            if not ev_dict or len(ev_dict) == 0:
                return
            
            _now = datetime.datetime.now()
            
            for ev_label,ev in ev_dict.iteritems():
                
                
                
                if Event._checkEvent(ev, _now):
                    
                    Event._performAction(
                        ev,
                        unlock_time=_now,
                        rebuild_ev=rebuild_ev
                    )
                    
                    
                    if not ev.prepareRepeat(True):
                        
                        ev.conditional = None
                        ev.action = None
            
            return
        
        
        @staticmethod
        def _checkRepeatRule(ev, check_time, defval=True):
            """
            DEPRECATED (remove when farewells is updated)

            Checks a single event against its repeat rules, which are evaled
            to a time.
            NOTE: no sanity checks

            IN:
                ev - single event to check
                check_time - datetime used to check time rules
                defval - defval to pass into the rules
                    (Default: True)

            RETURNS:
                True if this event passes its repeat rule, False otherwise
            """
            
            
            if MASSelectiveRepeatRule.evaluate_rule(
                    check_time, ev, defval=defval
                ):
                return True
            
            
            
            if MASNumericalRepeatRule.evaluate_rule(
                    check_time, ev, defval=defval
                ):
                return True
            
            return False
        
        
        @staticmethod
        def checkRepeatRules(events, check_time=None):
            """
            DEPRECATED (remove when farewells is updated)

            checks the event dict against repeat rules, which are evaluated
            to a time.

            IN:
                events - dict of events of the following format:
                    eventlabel: event object
                check_time - the datetime object that will be used to check the
                    timed rules, if none is passed we check against the current time

            RETURNS:
                A filtered dict containing the events that passed their own rules
                for the given check_time
            """
            
            if not events or len(events) == 0:
                return None
            
            
            if check_time is None:
                check_time = datetime.datetime.now()
            
            
            available_events = dict()
            
            
            for label, event in events.iteritems():
                if Event._checkRepeatRule(event, check_time, defval=False):
                    
                    if event.monikaWantsThisFirst():
                        return {event.eventlabel: event}
                    
                    available_events[event.eventlabel] = event
            
            
            return available_events
        
        
        @staticmethod
        def _checkFarewellRule(ev):
            """
            Checks the given event against its own farewell specific rule.

            IN:
                ev - event to check

            RETURNS:
                True if this event passes its repeat rule, False otherwise
            """
            return MASFarewellRule.evaluate_rule(ev)
        
        
        @staticmethod
        def checkFarewellRules(events):
            """
            Checks the event dict (farewells) against their own farewell specific
            rules, filters out those Events whose rule check return true. As for
            now the only rule specific is their specific special random chance

            IN:
                events - dict of events of the following format:
                    eventlabel: event object

            RETURNS:
                A filtered dict containing the events that passed their own rules

            """
            
            if not events or len(events) == 0:
                return None
            
            
            available_events = dict()
            
            
            for label, event in events.iteritems():
                
                
                if Event._checkFarewellRule(event):
                    
                    if event.monikaWantsThisFirst():
                        return {event.eventlabel: event}
                    
                    
                    available_events[label] = event
            
            
            return available_events
        
        @staticmethod
        def _checkAffectionRule(ev,keepNoRule=False):
            """
            Checks the given event against its own affection specific rule.

            IN:
                ev - event to check

            RETURNS:
                True if this event passes its repeat rule, False otherwise
            """
            return MASAffectionRule.evaluate_rule(ev,noRuleReturn=keepNoRule)
        
        
        @staticmethod
        def checkAffectionRules(events,keepNoRule=False):
            """
            Checks the event dict against their own affection specific rules,
            filters out those Events whose rule check return true. This rule
            checks if current affection is inside the specified range contained
            on the rule

            IN:
                events - dict of events of the following format:
                    eventlabel: event object
                keepNoRule - Boolean indicating wheter if it should keep
                    events that don't have an affection rule defined

            RETURNS:
                A filtered dict containing the events that passed their own rules

            """
            
            if not events or len(events) == 0:
                return None
            
            
            available_events = dict()
            
            
            for label, event in events.iteritems():
                
                
                if Event._checkAffectionRule(event,keepNoRule=keepNoRule):
                    
                    if event.monikaWantsThisFirst():
                        return {event.eventlabel: event}
                    
                    
                    available_events[label] = event
            
            
            return available_events
        
        
        @staticmethod
        def _performAction(ev, **kwargs):
            """
            Efficient / no checking action performing

            NOTE: does NOT check ev.action for nonNone

            IN:
                ev - event we are performing action on
                **kwargs - keyword args to pass to action
            """
            Event.ACTION_MAP[ev.action](ev, **kwargs)
        
        
        @staticmethod
        def performAction(ev, **kwargs):
            """
            Performs the action of the given event

            IN:
                ev - event we are perfrming action on
            """
            if ev.action in Event.ACTION_MAP:
                Event._performAction(ev, **kwargs)




    class MASButtonDisplayable(renpy.Displayable):
        """
        Special button type that represents a usable button for custom
        displayables.

        PROPERTIES:
            xpos - x position of this button (relative to container)
            ypos - y position of this button (relative to container)
            width - width of this button
            height - height of this button
            hover_sound - sound played when being hovered (this is played only
                once per hover. IF None, no sound is played)
            activate_sound - sound played when activated (this is played only
                once per activation. If None, no sound is played)
            enable_when_disabled - True means that the button is active even
                if shown disabled. False if otherwise
            sound_when_disabled - True means that sound is active even when the
                button is shown disabled, False if not.
                NOTE: only works if enable_when_disabled is True
            return_value - Value returned when button is activated
            disabled - True means to disable this button, False not
            hovered - True if we are being hovered, False if not
            _button_click - integer value to match a mouse click:
                1 - left (Default)
                2 - middle
                3 - right
                4 - scroll up
                5 - scroll down
            _button_down - pygame mouse button event type to activate button
                MOUSEBUTTONUP (Default)
                MOUSEBUTTONDOWN
        """
        import pygame
        
        
        _STATE_IDLE = 0
        _STATE_HOVER = 1
        _STATE_DISABLED = 2
        
        
        _INDEX_TEXT = 0
        _INDEX_BUTTON = 1
        
        def __init__(self,
                idle_text,
                hover_text,
                disable_text,
                idle_back,
                hover_back,
                disable_back,
                xpos,
                ypos,
                width,
                height,
                hover_sound=None,
                activate_sound=None,
                enable_when_disabled=False,
                sound_when_disabled=False,
                return_value=True
            ):
            """
            Constructor for the custom displayable

            IN:
                idle_text - Text object to show when button is idle
                hover_text - Text object to show when button is being hovered
                disable_text - Text object to show when button is disabled
                idle_back - Image object for background when button is idle
                hover_back - Image object for background when button is being
                    hovered
                disable_back - Image object for background when button is
                    disabled
                xpos - x position of this button (relative to container)
                ypos - y position of this button (relative to container)
                with - with of this button
                height - height of this button
                hover_sound - sound to play when hovering. If None, no sound
                    is played
                    (Default: None)
                activate_sound - sound to play when activated. If None, no
                    sound is played
                    (Default: None)
                enable_when_disabled - True will enable the button even if
                    it is visibly disabled. FAlse will not
                    (Default: False)
                sound_when_disabled - True will enable sound even if the
                    button is visibly disabled. False will not. Only works if
                    enable_when_disabled is True.
                    (Default: False)
                return_value - Value to return when the button is activated
                    (Default: True)
            """
            
            
            
            
            
            
            
            
            self.xpos = xpos
            self.ypos = ypos
            self.width = width
            self.height = height
            self.hover_sound = hover_sound
            self.activate_sound = activate_sound
            self.enable_when_disabled = enable_when_disabled
            self.sound_when_disabled = sound_when_disabled
            self.return_value = return_value
            self.disabled = False
            self.hovered = False
            self._button_click = 1
            self._button_down = pygame.MOUSEBUTTONUP
            
            
            self._button_states = {
                self._STATE_IDLE: (idle_text, idle_back),
                self._STATE_HOVER: (hover_text, hover_back),
                self._STATE_DISABLED: (disable_text, disable_back)
            }
            
            
            self._state = self._STATE_IDLE
        
        
        def _isOverMe(self, x, y):
            """
            Checks if the given x and y coodrinates are over this button.

            RETURNS: True if the given x, y is over this button, False if not
            """
            return (
                0 <= (x - self.xpos) <= self.width
                and 0 <= (y - self.ypos) <= self.height
            )
        
        
        def _playActivateSound(self):
            """
            Plays the activate sound if we are allowed to.
            """
            if not self.disabled or self.sound_when_disabled:
                renpy.play(self.activate_sound, channel="sound")
        
        
        def _playHoverSound(self):
            """
            Plays the hover soudn if we are allowed to.
            """
            if not self.disabled or self.sound_when_disabled:
                renpy.play(self.hover_sound, channel="sound")
        
        
        def disable(self):
            """
            Disables this button. This changes the internal state, so its
            preferable to use this over setting the disabled property
            directly
            """
            self.disabled = True
            self._state = self._STATE_DISABLED
        
        
        def enable(self):
            """
            Enables this button. This changes the internal state, so its
            preferable to use this over setting the disabled property
            directly
            """
            self.disabled = False
            self._state = self._STATE_IDLE
        
        
        def getSize(self):
            """
            Returns the size of this button

            RETURNS:
                tuple of the following format:
                    [0]: width
                    [1]: height
            """
            return (self.width, self.height)
        
        
        def ground(self):
            """
            Grounds (unhovers) this button. This changes the internal state,
            so its preferable to use this over setting the hovered property
            directly

            NOTE: If this button is disabled (and not enable_when_disabled),
            this will do NOTHING
            """
            if not self.disabled or self.enable_when_disabled:
                self.hovered = False
                
                if self.disabled:
                    self._state = self._STATE_DISABLED
                else:
                    self._state = self._STATE_IDLE
        
        
        def hover(self):
            """
            Hovers this button. This changes the internal state, so its
            preferable to use this over setting the hovered property directly

            NOTE: IF this button is disabled (and not enable_when_disabled),
            this will do NOTHING
            """
            if not self.disabled or self.enable_when_disabled:
                self.hovered = True
                self._state = self._STATE_HOVER
        
        
        def render(self, width, height, st, at):
            
            
            render_text, render_back = self._button_states[self._state]
            render_text = renpy.render(render_text, width, height, st, at)
            render_back = renpy.render(render_back, width, height, st, at)
            
            
            rt_w, rt_h = render_text.get_size()
            
            
            r = renpy.Render(self.width, self.height)
            
            
            r.blit(render_back, (0, 0))
            r.blit(
                render_text,
                (int((self.width - rt_w) / 2), int((self.height - rt_h) / 2))
            )
            
            
            return r
        
        
        def event(self, ev, x, y, st):
            
            
            
            if self._state != self._STATE_DISABLED or self.enable_when_disabled:
                
                
                if ev.type == pygame.MOUSEMOTION:
                    is_over_me = self._isOverMe(x, y)
                    if self.hovered:
                        if not is_over_me:
                            self.hovered = False
                            self._state = self._STATE_IDLE
                    
                    
                    
                    elif is_over_me:
                        self.hovered = True
                        self._state = self._STATE_HOVER
                        
                        if self.hover_sound:
                            self._playHoverSound()
                
                elif (
                        ev.type == self._button_down
                        and ev.button == self._button_click
                    ):
                    if self.hovered:
                        if self.activate_sound:
                            self._playActivateSound()
                        return self.return_value
            
            
            return None



    class MASQuipList(object):
        import random
        """
        Class that manages a list of quips. Quips have types which helps us
        when deciding how to execute quips. Also we have some properties that
        make it easy to customize a quiplist.

        I suggest that you only use this if you need to have multipe types
        of quips in a list. If you're only doing one-liners, a regular list
        will suffice.

        Currently 3 types of quips:
            glitchtext - special type for a glitchtext generated quip.
            label - this quip is actually the label for the actual quip
                (assumed the label has a return and is designed to be called)
            line - this quip is the actual line we want to display.
            other - other types of quips

        CONSTANTS:
            TYPE_GLITCH - glitch text type quip
            TYPE_LABEL - label type quip
            TYPE_LINE - line type quip
            TYPE_OTHER - other, custom types of quips

        PROPERTIES:
            allow_glitch - True means glitch quips can be added to this list
            allow_label - True means label quips can be added to this list
            allow_line - True means line quips can be added to this list
            raise_issues - True will raise exceptions if bad things occur:
                - if a quip that was not allowed was added
                - if a label that does not exist was added
                - etc...
        """
        
        TYPE_GLITCH = 0
        TYPE_LABEL = 1
        TYPE_LINE = 2
        TYPE_OTHER = 50
        
        TYPES = (
            TYPE_GLITCH,
            TYPE_LABEL,
            TYPE_LINE,
            TYPE_OTHER
        )
        
        def __init__(self,
                allow_glitch=True,
                allow_label=True,
                allow_line=True,
                raise_issues=True
            ):
            """
            Constructor for MASQuipList

            IN:
                allow_glitch - True means glitch quips can be added to this
                    list, False means no
                    (Default: True)
                allow_label - True means label quips can be added to this list,
                    False means no
                    (Default: True)
                allow_line - True means line quips can be added to ths list,
                    False means no
                    (Default: True)
                raise_issues - True means we will raise exceptions if bad
                    things occour. False means we stay quiet
                    (Default: True)
            """
            
            
            self.allow_glitch = allow_glitch
            self.allow_label = allow_label
            self.allow_line = allow_line
            self.raise_issues = raise_issues
            
            
            self._m1_definitions__quiplist = list()
        
        
        def addGlitchQuip(self,
                length,
                cps_speed=0,
                wait_time=None,
                no_wait=False
            ):
            """
            Adds a glitch quip based upon the given params.

            IN:
                length - length of the glitch text
                cps_speed - integer value to use as glitchtext speed multiplier
                    If 0 or 1, no cps speed change is done.
                    (Default: 0)
                wait_time - integer value to use as wait time. If None, no
                    wait tag is used
                    (Default: None)
                no_wait - If True, a no wait tag is added to the glitchtext.
                    otherwise, no no-wait tag is added.
                    (Default: False)

            RETURNS:
                index location of the added quip, or -1 if we werent allowed to
            """
            if self.allow_glitch:
                
                
                quip = glitchtext(length)
                
                
                if cps_speed > 0 and cps_speed != 1:
                    cps_speedtxt = "cps=*{0}".format(cps_speed)
                    quip = "{" + cps_speedtxt + "}" + quip + "{/cps}"
                
                
                if wait_time is not None:
                    wait_text = "w={0}".format(wait_time)
                    quip += "{" + wait_text + "}"
                
                
                if no_wait:
                    quip += "{nw}"
                
                
                self._m1_definitions__quiplist.append((self.TYPE_GLITCH, quip))
                
                return len(self._m1_definitions__quiplist) - 1
            
            else:
                self._m1_definitions__throwError(
                    "Glitchtext cannot be added to this MASQuipList"
                )
                return -1
        
        
        def addLabelQuip(self, label_name):
            """
            Adds a label quip.

            IN:
                label_name - label name of this quip

            RETURNS:
                index location of the added quip, or -1 if we werent allowed to
                or the label didnt exist
            """
            if self.allow_label:
                
                
                if not renpy.has_label(label_name):
                    
                    self._m1_definitions__throwError(
                        "Label '{0}' does not exist".format(label_name)
                    )
                    return -1
                
                
                self._m1_definitions__quiplist.append((self.TYPE_LABEL, label_name))
                
                return len(self._m1_definitions__quiplist) - 1
            
            else:
                self._m1_definitions__throwError(
                    "Labels cannot be added to this MASQuipList"
                )
                return -1
        
        
        def addLabelQuips(self, label_list):
            """
            Adds multiple label quips.

            IN:
                label_list - list of label names to add
            """
            for _label in label_list:
                self.addLabelQuip(_label)
        
        
        def addLineQuip(self, line, custom_type=None):
            """
            Adds a line quip. A custom type can be given if the caller wants
            this line quip to be differentable from other line quips.

            IN:
                line - line quip
                custom_type - the type to use for this line quip instead of
                    TYPE_LINE. If None, TYPE_LINE is used.
                    (Default: None)

            RETURNS:
                index location of the added quip, or -1 if we werent allowed to
                or the given custom_type is conflicting exisiting types.
            """
            if self.allow_line:
                
                
                if custom_type is None:
                    custom_type = self.TYPE_LINE
                
                elif custom_type in self.TYPES:
                    
                    self._m1_definitions__throwError(
                        (
                            "Custom type for '{0}' conflicts with default " +
                            "types."
                        ).format(line)
                    )
                    return -1
                
                
                self._m1_definitions__quiplist.append((custom_type, line))
                
                return len(self._m1_definitions__quiplist) -1
            
            else:
                self._m1_definitions__throwError(
                    "Lines cannot be added to this MASQuipList"
                )
                return -1
        
        
        def quip(self, remove=False):
            """
            Randomly picks a quip and returns the result.

            Line quips are automatically cleaned and prepared ([player],
            gender pronouns are all replaced appropraitely). If the caller
            wants additional variable replacements, they must do that
            themselves.

            IN:
                remove - True means we remove the quip we select. False means
                    keep it in the internal list.

            RETURNS:
                tuple of the following format:
                    [0]: type of this quip
                    [1]: value of this quip
            """
            if remove:
                
                sel_index = random.randint(0, len(self._m1_definitions__quiplist) - 1)
                quip_type, quip_value = self._m1_definitions__quiplist.pop(sel_index)
            
            else:
                
                
                quip_type, quip_value = random.choice(self._m1_definitions__quiplist)
            
            
            if quip_type == self.TYPE_GLITCH:
                quip_value = self._quipGlitch(quip_value)
            
            elif quip_type == self.TYPE_LABEL:
                quip_value = self._quipLabel(quip_value)
            
            elif quip_type == self.TYPE_LINE:
                quip_value = self._quipLine(quip_value)
            
            return (quip_type, quip_value)
        
        
        def _getQuip(self, index):
            """
            Retrieves the quip at the given index.

            IN:
                index - the index the wanted quip is at

            RETURNS:
                tuple of the following format:
                    [0]: type of this quip
                    [1]: value of this quip
            """
            return self._m1_definitions__quiplist[index]
        
        
        def _getQuipList(self):
            """
            Retrieves the internal quip list. This is a direct reference to
            the internal list, so be careful.

            RETURNS:
                the internal quiplist
            """
            return self._m1_definitions__quiplist
        
        
        def _quipGlitch(self, gt_quip):
            """
            Processes the given glitch text quip for usage.

            IN:
                gt_quip - the glitchtext quip (value) to process

            RETURNS:
                glitchtext quip ready for display.
            """
            
            return gt_quip
        
        
        def _quipLabel(self, la_quip):
            """
            Processes the given label quip for usage.

            IN:
                la_quip - the label quip (value) to process

            RETURNS:
                label quip ready for call
            """
            
            return la_quip
        
        
        def _quipLine(self, li_quip):
            """
            Processes the given line quip for usage.

            IN:
                li_quip - the line quip (value) to process

            RETURNS:
                line quip ready for display
            """
            
            
            
            
            
            
            
            
            
            return renpy.substitute(li_quip)
        
        
        def _removeQuip(self, index):
            """
            Removes the quip at the given index. (and returns it back)

            IN:
                index - the index of the quip to remove.

            RETURNS:
                tuple of the following format:
                    [0]: type of the removed quip
                    [1]: value of the removed quip
            """
            quip_tup = self._m1_definitions__quiplist.pop(index)
            return quip_tup
        
        
        def _m1_definitions__generateLineQuipReplacements(self):
            """
            Generates line quip replacement list for easy string replacement.

            RETURNS: a list for line quip variable replacements

            ASSUMES:
                player
                currentuser
                mcname
                <all gender prounouns>
            """
            return [
                ("[player]", player),
                ("[currentuser]", currentuser),
                ("[mcname]", mcname),
                ("[his]", his),
                ("[he]", he),
                ("[hes]", hes),
                ("[heis]", heis),
                ("[bf]", bf),
                ("[man]", man),
                ("[boy]", boy),
                ("[guy]", guy)
            ]
        
        
        def _m1_definitions__throwError(self, msg):
            """
            Internal function that throws an error if we are allowed to raise
            issues.

            IN:
                msg - message to display
            """
            if self.raise_issues:
                raise Exception(msg)





    class MASMailbox(object):
        """
        Async communication between different objects.

        NOTE: even though this is usable on its own, its highly recommended
        that you extend this class to encapsulate message constants.

        NOTE: this is NOT like notify, objects can only respond to messages
            when they are active.

        PROPERTIES:
            box - the actual mailbox that contains messages
        """
        RETURN_KEY = "__mas_return"
        
        
        def __init__(self):
            """
            Constructor
            """
            self.box = {}
        
        
        def get(self, headline):
            """
            Removes a message from the box, and returns it.

            IN:
                headline - identifier for the message

            RETURNS:
                the message data stored, None if no message data or if the
                message was actually None.
            """
            if headline in self.box:
                return self.box.pop(headline)
            
            return None
        
        
        def mas_get_return(self):
            """
            Removes and returns a MAS_RETURN message.

            RETURNS:
                the returned message, or None if no message data or if the
                emssage was wasctually none
            """
            return self.get(self.RETURN_KEY)
        
        
        def mas_send_return(self, msg):
            """
            Adds a MAS_RETURN message to the box.

            IN:
                msg - message to return
            """
            self.send(self.RETURN_KEY, msg)
        
        
        def read(self, headline):
            """
            Reads a message from the box.

            NOTE: does NOT remove the message.

            IN:
                headline - identifier for the message

            RETURNS:
                the message data stored, None if no message data or if the
                message was actually None
            """
            return self.box.get(headline, None)
        
        
        def send(self, headline, msg):
            """
            Adds a message to the box.

            IN:
                headline - identifier for this message.
                msg - message to send
            """
            self.box[headline] = msg




init -1 python in _mas_root:
    import store
    import datetime



    nonunicode = (
        "¡¢£¤¥¦§¨©ª«¬®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝ" +
        "Þßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿĀāĂăĄąĆćĈĉĊċČčĎďĐđĒēĔĕĖėĘę" +
        "ĚěĜĝĞğĠġĢģĤĥĦħĨĩĪīĬĭĮįİıĲĳĴĵĶķĸĹĺĻļĽľĿŀŁłŃńŅņŇňŉŊŋŌōŎŏŐőŒœŔŕŖ" +
        "ŗŘřŚśŜŝŞşŠšŢţŤťŦŧŨũŪūŬŭŮůŰűŲųŴŵŶŷŸŹźŻżŽž"
    )

    def glitchtext(length):
        import random
        output = ""
        for x in range(length):
            output += random.choice(nonunicode)
        return output

    def mangleFile(filepath, mangle_length=1000):
        """
        Mangles the file at the given filepath. Will create the file if it
        doesnt exists

        IN:
            filepath - path of the file to mangle
            mangle_length - how many characters to use to mangle
                (Default: 1000)
        """
        import struct
        bad_text = glitchtext(mangle_length)
        bad_text = [ord(x) for x in bad_text]
        bad_text = struct.pack("{0}i".format(mangle_length), *bad_text)
        with open(filepath, "wb") as m_file:
            m_file.write(bad_text)


    def resetPlayerData():
        """
        Completely resets player data in persistents.

        NOTE: Not all player-related persistent values may be reset by this
        function. If there are more player-related data in persistent that is
        not reset by this function, PLEASE LET US KNOW

        ASSUMES: a ton of persistent stuff
        """
        import datetime
        
        
        renpy.game.persistent._seen_ever = dict()
        
        
        renpy.game.persistent.playername = ""
        renpy.game.persistent.playthrough = 0
        renpy.game.persistent.yuri_kill = 0
        renpy.game.persistent.clear = [False] * 10
        renpy.game.persistent.special_poems = None
        renpy.game.persistent.clearall = None
        renpy.game.persistent.first_load = None
        
        
        renpy.game.persistent.event_database = dict()
        renpy.game.persistent.farewell_database = dict()
        renpy.game.persistent.closed_self = False
        renpy.game.persistent.seen_monika_in_room = False
        renpy.game.persistent.ever_won = {
            'pong':False,
            'chess':False,
            'hangman':False,
            'piano':False
        }
        renpy.game.persistent.game_unlocks = {
            'pong':True,
            'chess':False,
            'hangman':False,
            'piano':False
        }
        renpy.game.persistent.sessions={
            'last_session_end':datetime.datetime.now(),
            'current_session_start':datetime.datetime.now(),
            'total_playtime':datetime.timedelta(seconds=0),
            'total_sessions':0,
            'first_session':datetime.datetime.now()
        }
        renpy.game.persistent.playerxp = 0
        renpy.game.persistent.idlexp_total = 0
        renpy.game.persistent.rejected_monika = True
        renpy.game.persistent.current_track = None
        
        
        renpy.game.persistent._mas_chess_stats = {
            "wins": 0,
            "losses": 0,
            "draws": 0
        }
        renpy.game.persistent._mas_chess_quicksave = ""
        renpy.game.persistent.chess_strength = 20
        renpy.game.persistent._mas_chess_dlg_actions = dict()
        renpy.game.persistent._mas_chess_timed_disable = None
        renpy.game.persistent._mas_chess_3_edit_sorry = False
        
        
        renpy.game.persistent._mas_you_chr = False
        renpy.game.persistent.opendoor_opencount = 0
        renpy.game.persistent.opendoor_knockyes = False
        renpy.game.persistent._mas_greeting_type = None
        
        
        renpy.game.persistent._mas_hangman_playername = False
        
        
        renpy.game.persistent._mas_pnml_data = list()
        renpy.game.persistent._mas_piano_keymaps = dict()
        
        
        renpy.game.persistent._mas_affection["affection"] = 0


    def initialSessionData():
        """
        Completely resets session data to usable initial values.
        NOTE: these are not the defaults, but rather what they would be set to
        on a first load.
        """
        store.persistent.sessions = {
            "last_session_end": None,
            "current_session_start": datetime.datetime.now(),
            "total_playtime": datetime.timedelta(seconds=0),
            "total_sessions": 1,
            "first_session": datetime.datetime.now()
        }


init -999 python:
    import os


    renpy.not_infinite_loop(120)


    if not os.access(os.path.normcase(renpy.config.basedir + "/log"), os.F_OK):
        try:
            os.mkdir(os.path.normcase(renpy.config.basedir + "/log"))
        except:
            pass


init -990 python in mas_utils:
    import store
    import os
    import shutil
    import datetime
    import codecs
    import platform
    import time

    from os.path import expanduser
    from renpy.log import LogFile


    _mas__failrm = "[ERROR] Failed remove: '{0}' | {1}\n"
    _mas__failcp = "[ERROR] Failed copy: '{0}' -> '{1}' | {2}\n"


    BAD_TEXT = {
        "{": "{{",
        "[": "[["
    }



    def clean_gui_text(text):
        """
        Cleans the given text so its suitable for GUI usage

        IN:
            text - text to clean

        RETURNS:
            cleaned text
        """
        for bad in BAD_TEXT:
            text = text.replace(bad, BAD_TEXT[bad])
        
        return text


    def tryparseint(value, default=0):
        """
        Attempts to parse the given value into an int. Returns the default if
        that parse failed.

        IN:
            value - value to parse
            default - value to return if parse fails
            (Default: 0)

        RETURNS: an integer representation of the given value, or default if
            the given value could not be parsed into an int
        """
        try:
            return int(value)
        except:
            return default


    def copyfile(oldpath, newpath):
        """
        Copies the file at oldpath into a file at newpath
        Paths assumed to include the filename (like an mv command)

        NOTE:
            if a copy fails, the error is logged

        IN:
            oldpath - path to old file, including filename
            newpath - path to new file, including filename

        RETURNS:
            True if copy succeeded, False otherwise
        """
        try:
            shutil.copyfile(oldpath, newpath)
            return True
        except Exception as e:
            writelog(_mas__failcp.format(oldpath, newpath, str(e)))
        return False


    def writelog(msg):
        """
        Writes to the mas log if it is open

        IN:
            msg - message to write to log
        """
        if mas_log_open:
            mas_log.write(msg)


    def trydel(f_path, log=False):
        """
        Attempts to delete something at the given path

        NOTE: completely hides exceptions, unless log is True
        """
        try:
            os.remove(f_path)
        except Exception as e:
            if log:
                writelog("[exp] {0}\n".format(repr(e)))


    def trywrite(f_path, msg, log=False, mode="w"):
        """
        Attempts to write out a file at the given path

        Exceptions are hidden

        IN:
            f_path - path to write file
            msg - text to write
            log - True means we log exceptions
                (Default: False)
            mode - write mode to use
                (Defaut: w)
        """
        outfile = None
        try:
            outfile = open(f_path, mode)
            outfile.write(msg)
        except Exception as e:
            if log:
                writelog("[exp] {0}\n".format(repr(e)))
        finally:
            if outfile is not None:
                outfile.close()


    def logrotate(logpath, filename):
        """
        Does a log rotation. Log rotations contstantly increase. We defualt
        to about 2 decimal places, but let the limit go past that

        NOTE: exceptions are logged

        IN:
            logpath - path to the folder containing logs
                NOTE: this is assumed to have the trailing slash
            filename - filename of the log to rotate
        """
        try:
            filelist = os.listdir(logpath)
        except Exception as e:
            writelog("[ERROR] " + str(e) + "\n")
            return
        
        
        _m1_definitions__numformat = "{:02d}"
        _m1_definitions__numdelim = "."
        
        
        
        filelist = sorted([
            x
            for x in filelist
            if x.startswith(filename)
        ])
        
        
        
        if len(filelist) > 1:
            fname, dot, largest_num = filelist.pop().rpartition(_m1_definitions__numdelim)
            largest_num = tryparseint(largest_num, -1)
        
        else:
            
            largest_num = -1
        
        
        largest_num += 1
        
        
        new_path = os.path.normcase("".join([
            logpath,
            filename,
            _m1_definitions__numdelim,
            _m1_definitions__numformat.format(largest_num)
        ]))
        trydel(new_path)
        
        
        old_path = os.path.normcase(logpath + filename)
        copyfile(old_path, new_path)
        
        
        trydel(old_path)

    def tryparsedt(_datetime, default=None, sep=" "):
        """
        Trys to parse a datetime isoformat string into a datetime object

        IN:
            _datetime - datetime iso format string to parse
            default - default value to return if parsing fails
            sep - separator used when converting to isoformat

        RETURNS:
            datetime object, or default if parsing failed
        """
        if len(_datetime) == 0:
            return default
        
        try:
            
            _date, _sep, _time = _datetime.partition(sep)
            
            
            year, month, day = _date.split("-")
            
            
            hour, minute, second = _time.split(":", 2)
            
            
            second, _sep, ms = second.partition(".")
            
            
            ms = ms[:6]
            
            
            year = tryparseint(year, -1)
            month = tryparseint(month, -1)
            day = tryparseint(day, -1)
            hour = tryparseint(hour, -1)
            minute = tryparseint(minute, -1)
            second = tryparseint(second, -1)
            ms = tryparseint(ms, 0) 
            
            
            return datetime.datetime(year, month, day, hour, minute, second, ms)
        
        except:
            return default

    log_error = None


    class MASMacLog(LogFile):
        
        def __init__(self, name, append=False, developer=False, flush=True):
            """
            `name`
                The name of the logfile, without the .txt extension.
            `append`
                If true, we will append to the logfile. If false, we will truncate
                it to an empty file the first time we write to it.
            `developer`
                If true, nothing happens if config.developer is not set to True.
            `flush`
                Determines if the file is flushed after each write.
            """
            LogFile.__init__(self, name, append=append, developer=developer, flush=flush)
        
        
        def open(self):  
            
            if self.file:
                return True
            
            if self.file is False:
                return False
            
            if self.developer and not renpy.config.developer:
                return False
            
            if not renpy.config.log_enable:
                return False
            
            try:
                
                home = expanduser("~")
                base = os.path.join(home,".MonikaAfterStory/" )
                
                if base is None:
                    return False
                
                fn = os.path.join(base, self.name + ".txt")
                
                path, filename = os.path.split(fn)
                if not os.path.exists(path):
                    os.makedirs(path)
                
                if self.append:
                    mode = "a"
                else:
                    mode = "w"
                
                if renpy.config.log_to_stdout:
                    self.file = real_stdout
                
                else:
                    
                    try:
                        self.file = codecs.open(fn, mode, "utf-8")
                    except:
                        pass
                
                if self.append:
                    self.write('')
                    self.write('=' * 78)
                    self.write('')
                
                self.write("%s", time.ctime())
                try:
                    self.write("%s", platform.platform())
                except:
                    self.write("Unknown platform.")
                self.write("%s", renpy.version)
                self.write("%s %s", renpy.config.name, renpy.config.version)
                self.write("")
                
                return True
            
            except:
                self.file = False
                return False



    mas_mac_log_cache = { }

    def macLogOpen(name, append=False, developer=False, flush=False):  
        rv = mas_mac_log_cache.get(name, None)
        
        if rv is None:
            rv = MASMacLog(name, append=append, developer=developer, flush=flush)
            mas_mac_log_cache[name] = rv
        
        return rv

    def getMASLog(name, append=False, developer=False, flush=False):
        if renpy.macapp or renpy.macintosh:
            return macLogOpen(name, append=append, developer=developer, flush=flush)
        return renpy.renpy.log.open(name, append=append, developer=developer, flush=flush)



    if store.persistent._mas_unstable_mode:
        mas_log = getMASLog("log/mas_log", append=True, flush=True)
    else:
        mas_log = getMASLog("log/mas_log")

    mas_log_open = mas_log.open()
    mas_log.raw_write = True


init -100 python in mas_utils:

    import datetime
    import ctypes
    import random
    import os
    from cStringIO import StringIO as fastIO

    _m1_definitions__FLIMIT = 1000000

    def tryparsefloat(value, default=0):
        """
        Attempts to parse the given value into a float. Returns the default if
        that parse failed.

        IN:
            value - value to parse
            default - value to return if parse fails
            (Default: 0)

        RETURNS: a float representation of the given value, or default if
            the given value could not be parsed into an float
        """
        try:
            return float(value)
        except:
            return default


    def bullet_list(_list, bullet="  -"):
        """
        Converts a list of items into a bulleted list of strings.

        IN:
            _list - list to convert into bulleted list
            bullet - the bullet to use. A space is added between the bullet and
                the item.
                (Default: 2 spaces and a dash)

        RETURNS: a list of strings where each string is an item with a bullet.
        """
        return [bullet + " " + str(item) for item in _list]



    def add_years(initial_date, years):
        """
        ASSUMES:
            initial_date as datetime
            years as an int

        IN:
            initial_date: the date to add years to
            years : the number of years to add

        RETURNS:
            the date with the years added, if it's feb 29th it goes to mar 1st,
            if feb 29 doesn't exists in the new year
        """
        try:
            
            
            return initial_date.replace(year=initial_date.year + years)
        except ValueError:
            
            
            return  initial_date + (datetime.date(initial_date.year + years, 1, 1)
                                - datetime.date(initial_date.year, 1, 1))




    def add_months(starting_date,months):
        old_month=starting_date.month
        old_year=starting_date.year
        old_day=starting_date.day
        
        
        total_months = old_month + months
        
        
        new_month = total_months % 12
        
        
        new_month = 12 if new_month == 0 else new_month
        
        
        new_year = old_year + int(total_months / 12)
        if new_month == 12:
            new_year -= 1
        
        
        
        date_worked=False
        reduce_days=0
        while reduce_days<=3 and not date_worked:
            try:
                new_date = starting_date.replace(year=new_year,month=new_month,day=old_day-reduce_days)
                date_worked = True
            except ValueError:
                reduce_days+=1
        
        if not date_worked:
            raise ValueError('Adding months failed')
        
        return new_date




    def sod(starting_date):
        return am3(starting_date)


    def mdnt(starting_date):
        """
        Takes a datetime object and returns a new datetime with the same date
        at midnight

        IN:
            starting_date - date to change

        RETURNS:
            starting_date but at midnight
        """
        return starting_date.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )


    def am3(_datetime):
        """
        Takes a datetime object and returns a new datetime with the same date
        at 3 am.

        IN:
            _datetime - datetime to change

        RETURNS:
            _datetime but at 3am
        """
        return _datetime.replace(
            hour=3,
            minute=0,
            second=0,
            microsecond=0
        )


    def _EVgenY(_start, _end, current, for_start):
        """
        Generates/decides if a given start/end datetime/date should have its
        year incremented or not.

        NOTE: specialized for Event creation datetime selection
        NOTE: this only modifies year.

        IN:
            _start - datetime/date that begins this period
            _end - datetime/date that ends this period
            current - datetime/date to compare with (should be either today
                or now)
            for_start - True if we want the next valid start, False for end

        RETURNS either next valid _start or next valid _end.
        """
        
        if for_start:
            _focus = _start
        else:
            _focus = _end
        
        if current < _end:
            
            
            return _focus
        
        
        return _focus.replace(year=current.year + 1)


    def randomblob(size, seed=None):
        """
        Generates a blob of StringIO data with the given size

        NOTE: if seed is given, the current random state will be restored
            after this function ends

        NOTE: generated bytes are in range of 0-255

        IN:
            size - size in bytes of the blob to make
            seed - seed to use
                if None, curent time is used (as per random documentation)
                (Default: None)

        RETURNS:
            a cStringIO buffer of the random blob
        """
        data = fastIO()
        _byte_count = 0
        curr_state = None
        
        
        curr_state = random.getstate()
        random.seed(seed)
        
        
        while _byte_count < size:
            data.write(chr(random.randint(0, 255)))
            _byte_count += 1
        
        
        random.setstate(curr_state)
        
        return data


    def randomblob_fast(size):
        """
        Generates a randomb blob of stringIO data more efficientally and with
        true random using urandom

        NOTE: to prevent errors, we only generate bytes at 4M per iteration

        IN:
            size - size in bytes of the blob to make

        RETURNS:
            a cStringIO buffer of the random blob
        """
        data = fastIO()
        _byte_limit = 4 * (1024**2) 
        
        while size > 0:
            make_bytes = _byte_limit
            if (size - _byte_limit) <= 0:
                make_bytes = size
                size = 0
            
            else:
                size -= make_bytes
            
            data.write(os.urandom(make_bytes))
        
        return data


    def intersperse(_list, _sep):
        """
        Intersperses a list with the given separator
        """
        result_list = [_sep] * (len(_list) * 2 - 1)
        result_list[0::2] = _list
        return result_list


    def log_entry(entry_log, value):
        """
        Generic entry add to the given log.
        Stores both time and given value as a tuple:
            [0]: datetime.now()
            [1]: value

        IN:
            entry_log - list to log entry to
            value - value to log in this entry
        """
        entry_log.append((datetime.datetime.now(), value))


    class ISCRAM(ctypes.BigEndianStructure):
        _iscramfieldbuilder = [
            3, 3, 2, 1, 3, 2, 2, 1, 3, 3, 1, 3, 1
        ] 
        _iscramfieldorder = [
            12, 11, 0, 4, 2, 9, 5, 3, 8, 7, 6, 1, 10
        ] 
        _iscramfieldlist = [
            ("sign", ctypes.c_ubyte, 1)
        ]
        for x in range(0, len(_iscramfieldorder)):
            _iscramfieldlist.append((
                "b" + str(x),
                ctypes.c_ubyte,
                _iscramfieldbuilder[_iscramfieldorder.index(x)]
            ))
        _pack_ = 1
        _fields_ = list(_iscramfieldlist)


    class FSCRAM(ctypes.BigEndianStructure):
        _pack_ = 1
        _fields_ = [
            ("sign", ctypes.c_ubyte, 1),
            ("inum", ISCRAM),
            ("fnum", ISCRAM),
            ("dnum", ISCRAM)
        ]


    def _ntoub(num, bsize):
        """
        Partial packing.
        """
        st = 1
        val = 0
        for i in range(0,bsize):
            if (num & st) > 0:
                val += st
            st *= 2
        
        return val


    def _itoIS(num):
        """
        integer packing
        """
        packednum = ISCRAM()
        if num < 0:
            packednum.sign = 1
            num *= -1
        
        for i in range(0, len(ISCRAM._iscramfieldbuilder)):
            bsize = ISCRAM._iscramfieldbuilder[i]
            savepoint = _ntoub(num, bsize)
            exec("".join([
                "packednum.b",
                str(ISCRAM._iscramfieldorder[i]),
                " = ",
                str(savepoint)
            ]))
            num = num >> bsize
        
        
        
        return packednum


    def _IStoi(packednum):
        """
        integer unpacking
        """
        num = 0
        for i in range(len(ISCRAM._iscramfieldbuilder)-1, -1, -1):
            num = num << ISCRAM._iscramfieldbuilder[i]
            num = num | eval("".join([
                "packednum.b",
                str(ISCRAM._iscramfieldorder[i])
            ]))
        
        if packednum.sign > 0:
            return num * -1
        
        return num


    def _ftoFS(num):
        """
        Float packing
        """
        packednum = FSCRAM()
        if num < 0:
            packednum.sign = 1
            num *= -1
        
        ival = int(num)
        packednum.inum = _itoIS(ival)
        packednum.fnum = _itoIS(int((num - ival) * _m1_definitions__FLIMIT))
        packednum.dnum = _itoIS(_m1_definitions__FLIMIT)
        
        return packednum


    def _FStof(packednum):
        """
        Float unpacking
        """
        ival = _IStoi(packednum.inum)
        fnum = _IStoi(packednum.fnum)
        dnum = float(_IStoi(packednum.dnum))
        
        fval = ival + (fnum / dnum)
        
        if packednum.sign > 0:
            return fval * -1
        
        return fval


    def _splitfloat(num):
        """
        Splits a float into integer parts:

        [0]: integer
        [1]: numerator
        [2]: denominator
        """
        ival = int(num)
        cleanival = ival
        if num < 0:
            num *= -1
            cleanival *= -1
        return (ival, int((num - cleanival) * _m1_definitions__FLIMIT), _m1_definitions__FLIMIT)


init -1 python:
    import datetime 
    import os
    if "mouseup_3" in config.keymap['game_menu']:
        config.keymap['game_menu'].remove('mouseup_3')
    if "mouseup_3" not in config.keymap["hide_windows"]:
        config.keymap['hide_windows'].append('mouseup_3')
    config.keymap['self_voicing'] = []
    config.keymap['clipboard_voicing'] = []
    config.keymap['toggle_skip'] = []
    renpy.music.register_channel("music_poem", mixer="music", tight=True)



    monika_topics = {}

    def get_procs():
        """
        Retrieves list of processes running right now!

        Only works for windows atm

        RETURNS: list of running processes, or an empty list if
        we couldn't do that
        """
        if renpy.windows:
            import subprocess
            try:
                return subprocess.check_output(
                    "wmic process get Description",
                    shell=True
                ).lower().replace("\r", "").replace(" ", "").split("\n")
            except:
                pass
        return []


    def is_running(proc_list):
        """
        Checks if a process in the given list is currently running.

        RETURNS: True if a proccess in proc_list is running, False otherwise
        """
        running_procs = get_procs()
        if len(running_procs) == 0:
            return False
        
        for proc in proc_list:
            if proc in running_procs:
                return True
        
        
        return False

    def is_file_present(filename):
        if not filename.startswith("/"):
            filename = "/" + filename
        
        filepath = renpy.config.basedir + filename
        
        try:
            return os.access(os.path.normcase(filepath), os.F_OK)
        except:
            return False


    def is_apology_present():
        return is_file_present('/imsorry') or is_file_present('/imsorry.txt')


    def mas_cvToHM(mins):
        """
        Converts the given minutes into hour / minutes

        IN:
            mins - number of minutes

        RETURNS:
            tuple of the following format:
                [0] - hours
                [1] - minutes
        """
        return (int(mins / 60), int(mins % 60))


    def mas_isSTtoAny(_time, _suntime, _hour, _min):
        """
        Checks if the given time is within this range:
        _suntime <= _time < (_hour, _min)

        NOTE: upper bound is limited to midnight

        IN:
            _time - current time to check
                NOTE: datetime.time object
            _suntime - suntime to use for lower bound
                NOTE: suntimes are given in minutes
            _hour - hour to use for upper bound
            _min - minute to use for upper bound

        RETURNS:
            True if the given time is within bounds of the given suntime and
                given hour / mins, False otherwise
        """
        _curr_minutes = (_time.hour * 60) + _time.minute
        _upper_minutes = (_hour * 60) + _min
        return _suntime <= _curr_minutes < _upper_minutes


    def mas_isSRtoAny(_time, _hour, _min=0):
        """
        Checks if the given time is within Sunrise time to the given _hour
        and _minute

        NOTE: upper bound is limited to midnight

        IN:
            _time - current time to check
                NOTE: datetime.time object
            _hour - hour to use for upper bound
            _min - minute to use for upper bound
                (Default: 0)

        RETURNS:
            True if the given time is whithin bounds of sunrise and the given
            hour / mins, False otherwise
        """
        return mas_isSTtoAny(_time, persistent._mas_sunrise, _hour, _min)


    def mas_isSStoAny(_time, _hour, _min=0):
        """
        Checks if the given time is within sunset to the given _hour and minute

        NOTE: upper bound is limited to midnight

        IN:
            _time - current time to check
                NOTE: datetime.time object
            _hour - hour to use for upper bound
            _min - minute to use for upper bound
                (Default: 0)

        RETURNS:
            True if the given time is within bounds of sunset and the given
            hour/min, False otherwise
        """
        return mas_isSTtoAny(_time, persistent._mas_sunset, _hour, _min)


    def mas_isMNtoAny(_time, _hour, _min=0):
        """
        Checks if the given time is within midnight to the given hour/min.

        NOTE: upper bound is 24 midnight
        NOTE: lower bound is 0 midnight

        IN:
            _time - current time to check
                NOTE: datetime.time object
            _hour - hour to use for upper bound
            _min - minute to use for upper bound
                (Default: 0)

        RETURNS:
            True if the given time is within bounds of midnight and the given
            hour/min, False otherwise
        """
        return mas_isSTtoAny(_time, 0, _hour, _min)


    def mas_isNtoAny(_time, _hour, _min=0):
        """
        Checks if the given time is within noon to the given hour/min.

        NOTE: upper bound is 24 midnight

        IN:
            _time - current time to check
                NOTE: datetime.time object
            _hour - hour to use for upper bound
            _min - minute to use for upper bound
                (Default: 0)

        RETURNS:
            True if the given time is within bounds of noon and the given hour
            /min, False otherwise
        """
        return mas_isSTtoAny(_time, 12*60, _hour, _min)


    def mas_isAnytoST(_time, _hour, _min, _suntime):
        """
        Checks if the given time is within this range:
        (_hour, _min) <= _time < _suntime

        NOTE: lower bound is limited to midnight

        IN:
            _time - current time to check
                NOTE: datetime.time object
            _hour - hour to use for lower bound
            _min - minute to use for lower bound
            _suntime - suntime to use for upper bound
                NOTE: suntimes are given in minutes

        RETURNS:
            True if the given time is within bounds of the given hour / mins
            and the given suntime, false Otherwise
        """
        _curr_minutes = (_time.hour * 60) + _time.minute
        _lower_minutes = (_hour * 60) + _min
        return _lower_minutes <= _curr_minutes < _suntime


    def mas_isAnytoSR(_time, _hour, _min=0):
        """
        Checks if the given time is within a given hour and minute to sunrise
        time

        NOTE: lower bound is limited to midnight

        IN:
            _time - current time to check
                NOTE: datetime.time object
            _hour - hour to use for lower bound
            _min - minute to use for lower bound
                (Default: 0)

        RETURNS:
            True if the given time is within the bounds of the given hour/min
            and sunrise, False otherwise
        """
        return mas_isAnytoST(_time, _hour, _min, persistent._mas_sunrise)


    def mas_isAnytoSS(_time, _hour, _min=0):
        """
        Checks if the given time is within a given hour/min to sunset time

        NOTE: lower bound is limited to midnight

        IN:
            _time - current time to check
                NOTE: datetime.time object
            _hour - hour to use for lower bound
            _min - minute to use for lower bound
                (Default: 0)

        RETURNS:
            True if the given time is within the bounds of the given hour/min
            and sunset, False otherwise
        """
        return mas_isAnytoST(_time, _hour, _min, persistent._mas_sunset)


    def mas_isAnytoMN(_time, _hour, _min=0):
        """
        Checks if the given time is within a given hour/min to midnight (next
        day)

        NOTE: lower bound is limited to midnight
        NOTE: upper bound is 24 - midnight

        IN:
            _time - current time to check
                NOTE: datetime.time object
            _hour - hour to use for lower bound
            _min - mintue to use for lower bound
                (DEfault: 0)

        RETURNS:
            True if the given time is within the bounds of the given hour/min
            and midnight, False otherwise
        """
        return mas_isAnytoST(_time, _hour, _min, 24*60)


    def mas_isAnytoN(_time, _hour, _min=0):
        """
        Checks if the given time is within a given hour/min to noon.

        NOTE: lower bound is limited to midnight

        IN:
            _time - current time to check
                NOTE: datetime.time object
            _hour - hour to use for lower bound
            _min - minute to use for lower bound
                (Default: 0)

        RETURNS:
            True if the given tim eis within the bounds of the given hour/min
            and Noon, False otherwise
        """
        return mas_isAnytoST(_time, _hour, _min, 12*60)


    def mas_isMNtoSR(_time):
        """
        Checks if the given time is within midnight to sunrise

        IN:
            _time - current time to check
                NOTE: datetime.time object

        RETURNS: True if the given time is within midnight to sunrise
        """
        return mas_isAnytoSR(_time, 0)


    def mas_isSRtoN(_time):
        """
        Checks if the given time is within sunrise to noon

        IN:
            _time - current time to check
                NOTE: datetime.time object

        RETURNS: True if the given time is witin sunrise to noon
        """
        return mas_isSRtoAny(_time, 12)


    def mas_isNtoSS(_time):
        """
        Checks if the given time is within noon to sunset

        IN:
            _time - current time to check
                NOTE: datetime.time object

        RETURNS: True if the given time is within noon to sunset
        """
        return mas_isAnytoSS(_time, 12)


    def mas_isSStoMN(_time):
        """
        Checks if the given time is within sunset to midnight

        IN:
            _time - current time to check
                NOTE: datetime.time object

        RETURNS: True if the given time is within sunset to midnight
        """
        return mas_isSStoAny(_time, 24)


    def mas_isSunny(_time):
        """
        Checks if the sun is up during the given time

        IN:
            _time - current time to check
                NOTE: datetime.time object

        RETURNS: True if it is sunny during the given time
        """
        _curr_minutes = (_time.hour * 60) + _time.minute
        return persistent._mas_sunrise <= _curr_minutes < persistent._mas_sunset


    def mas_isNight(_time):
        """
        Checks if the sun is down during the given time

        IN:
            _time - current time to check
                NOTE: datetime.time object

        RETURNS: True if it the sun is down during the given time
        """
        return not mas_isSunny(_time)


    def mas_cvToDHM(mins):
        """
        Converts the given minutes into a displayable hour / minutes
        HH:MM
        NOTE: 24 hour format only

        IN:
            mins - number of minutes

        RETURNS:
            string time perfect for displaying
        """
        s_hour, s_min = mas_cvToHM(mins)
        return "{0:0>2d}:{1:0>2d}".format(s_hour, s_min)



    def mas_getSessionLength():
        return datetime.datetime.now() - persistent.sessions['current_session_start']



    def mas_getAbsenceLength():
        return persistent.sessions.get('current_session_start', datetime.datetime.today()) - persistent.sessions.get('last_session_end', datetime.datetime.today())


    def mas_genDateRange(_start, _end):
        """
        Generates a list of datetime.date objects with the given range.

        NOTE: exclusive:

        IN:
            _start - starting date of range
            _end - ending date of range

        RETURNS: list of datetime.date objects between the _start and _end,
            exclusive. May be empty if invalid start and end dates are given
        """
        
        if _start >= _end:
            return []
        
        _date_range = []
        one_day = datetime.timedelta(days=1)
        curr_date = _start
        
        while curr_date < _end:
            _date_range.append(curr_date)
            curr_date += one_day
        
        return _date_range


    def mas_EVgenYDT(_start, _end, for_start):
        """
        Creates a valid start or end datetime for Event creation, given the
        start and end datetimes.

        NOTE: this only modifies year. Build a custom function for something
        more precise.

        IN:
            _start - datetime that begins this period
            _end - datetime that ends this period
            for_start - True if we want the next valid starting datetime
                False if we want the next valid ending datetime

        RETURNS: valid datetime for Event creation
        """
        return store.mas_utils._EVgenY(
            _start,
            _end,
            datetime.datetime.now(),
            for_start
        )


    def mas_EVgenYD(
            _start,
            _end,
            for_start,
            _time=datetime.time.min
        ):
        """
        Variation of mas_EVgenYDT that accepts datetime.dates. This still
        returns datetimes though.

        IN:
            _start - date that begins this period
            _end - date that ends this period
            for_start - True if we want the next valid starting datetime
                False if we want the next valid ending datetime
            _time - time to use with the dates.
                (Default: datetime.time.min)

        RETURNS: valid datetime for Event creation
        """
        return datetime.datetime.combine(
            store.mas_utils._EVgenY(
                _start,
                _end,
                datetime.date.today(),
                for_start
            ),
            _time
        )


    def mas_isMonikaBirthday():
        return datetime.date.today() == mas_monika_birthday


    def mas_isSpecialDay():
        """
        Checks if today is a special day(birthday, anniversary or holiday)

        RETURNS:
            boolean indicating if today is a special day.
        """
        
        return (
            mas_isMonikaBirthday()
            or mas_isO31()
            or mas_isD25()
            or (mas_anni.isAnniAny() and not mas_anni.isAnniWeek())
            or mas_isNYE()
            or mas_isF14()
        )

    def mas_getNextMonikaBirthday():
        today = datetime.date.today()
        if mas_monika_birthday < today:
            return datetime.date(
                today.year + 1,
                mas_monika_birthday.month,
                mas_monika_birthday.day
            )
        return mas_monika_birthday


    def mas_recognizedBday(_date=None):
        """
        Checks if the user recognized monika's birthday at all.

        TODO: this is one-shot. we need to make this generic to future bdays

        RETURNS:
            True if the user recoginzed monika's birthday, False otherwise
        """
        if _date is None:
            _date = mas_monika_birthday
        
        return (
            mas_generateGiftsReport(_date)[0] > 0
            or persistent._mas_bday_date_count > 0
            or persistent._mas_bday_sbp_reacted
            or persistent._mas_bday_said_happybday
        )


    def mas_maxPlaytime():
        return datetime.datetime.now() - datetime.datetime(2017, 9, 22)


    def mas_isInDateRange(
            subject,
            _start,
            _end,
            start_inclusive=True,
            end_inclusive=False
        ):
        """
        Checks if the given subject date is within  range of the given start
        end dates.

        NOTE: this does year normalization, so we only compare months and days
        NOTE: we do NOT compare years

        IN:
            subject - subject date to compare
            _start - starting date of the range
            _end - ending date of the range
            start_inclusive - True if start date should be inclusive
                (Derfault: True)
            end_inclusive - True if end date should be inclusive
                (Default: False)

        RETURNS: True if the given subject is within date range, False if not
        """
        real_start = _start.replace(year=subject.year)
        real_end = _end.replace(year=subject.year)
        
        if start_inclusive:
            if real_start > subject:
                return False
        
        else:
            if real_start >= subject:
                return False
        
        if end_inclusive:
            if subject > real_end:
                return False
        
        else:
            if subject >= real_end:
                return False
        
        
        return True


    def mas_getFirstSesh():
        """
        Returns the first session datetime.

        If we could not get it, datetime.datetime.now() is returnd
        """
        if (
                persistent.sessions is not None
                and "first_session" in persistent.sessions
                and type(persistent.sessions["first_session"])
                    == datetime.datetime
            ):
            return persistent.sessions["first_session"]
        
        return datetime.datetime.now()


    def get_pos(channel='music'):
        pos = renpy.music.get_pos(channel=channel)
        if pos: return pos
        return 0
    def delete_all_saves():
        for savegame in renpy.list_saved_games(fast=True):
            renpy.unlink_save(savegame)
    def delete_character(name):
        if persistent.do_not_delete: return
        import os
        try: os.remove(config.basedir + "/characters/" + name + ".chr")
        except: pass
    def pause(time=None):
        if not time:
            renpy.ui.saybehavior(afm=" ")
            renpy.ui.interact(mouse='pause', type='pause', roll_forward=None)
            return
        if time <= 0: return
        renpy.pause(time)


    def enumerate_steam():
        installPath=""
        if renpy.windows:
            import _winreg    
            
            
            aReg = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
            try:
                
                keyVal = _winreg.OpenKey(aReg, r"SOFTWARE\Valve\Steam")
            except:
                
                try:
                    keyVal = _winreg.OpenKey(aReg, r"SOFTWARE\Wow6432Node\Valve\Steam")
                except:
                    
                    return None
            for i in range(4):
                
                n,installPath,t = _winreg.EnumValue(keyVal, i)
                if n=="InstallPath": break
            installPath+="/steamapps"
        elif renpy.mac:
            installPath=os.environ.get("HOME") + "/Library/Application Support/Steam/SteamApps"
        elif renpy.linux:
            installPath=os.environ.get("HOME") + "/.steam/Steam/steamapps" \
            
        else:
            return None
        try:
            appIds = [file[12:-4] for file in os.listdir(installPath) if file.startswith("appmanifest")]
        except:
            appIds = None
        return appIds

init 2 python:


    def mas_isCoffeeTime(_time=None):
        """
        Checks if its coffee time for monika

        IN:
            _time - time to check
                If None, we use current time
                (Defualt: None)

        RETURNS:
            true if its coffee time, false if not
        """
        if _time is None:
            _time = datetime.datetime.now()
        
        
        return (
            store.mas_coffee.COFFEE_TIME_START
            <= _time.hour <
            store.mas_coffee.COFFEE_TIME_END
        )


    def mas_brewCoffee(_start_time=None):
        """
        Starts brewing coffee aka sets up the coffee finished brewing event

        IN:
            _start_time - time to start brewing the coffee
                If None, we assume now
                (Default: None)
        """
        if _start_time is None:
            _start_time = datetime.datetime.now()
        
        
        persistent._mas_coffee_brew_time = _start_time
        
        
        end_brew = random.randint(
            store.mas_coffee.BREW_LOW,
            store.mas_coffee.BREW_HIGH
        )
        
        
        brew_ev = mas_getEV("mas_coffee_finished_brewing")
        brew_ev.conditional = (
            "persistent._mas_coffee_brew_time is not None "
            "and (datetime.datetime.now() - persistent._mas_coffee_brew_time) "
            "> datetime.timedelta(0, {0})"
        ).format(end_brew)
        brew_ev.action = EV_ACT_QUEUE


    def mas_drinkCoffee(_start_time=None):
        """
        Lets monika drink coffee aka sets the time she should stop drinking
        coffee (coffee finished drinking event)

        IN:
            _start_time - time to start dirnking coffee
                If None, we use now
                (Defualt: now)
        """
        if _start_time is None:
            _start_time = datetime.datetime.now()
        
        
        
        drinking_time = datetime.timedelta(
            0,
            random.randint(
                store.mas_coffee.DRINK_LOW,
                store.mas_coffee.DRINK_HIGH
            )
        )
        
        
        persistent._mas_coffee_cup_done = _start_time + drinking_time
        
        
        drink_ev = mas_getEV("mas_coffee_finished_drinking")
        drink_ev.conditional = (
            "persistent._mas_coffee_cup_done is not None "
            "and datetime.datetime.now() > persistent._mas_coffee_cup_done"
        )
        drink_ev.action = EV_ACT_QUEUE
        
        
        persistent._mas_coffee_cups_drank += 1


    def mas_resetCoffee():
        """
        Completely resets all coffee vars
        NOTE: this only resets the coffee drinking vars, not the history
        """
        brew_ev = mas_getEV("mas_coffee_finished_brewing")
        drink_ev = mas_getEV("mas_coffee_finished_drinking")
        monika_chr.remove_acs(mas_acs_mug)
        brew_ev.conditional = None
        brew_ev.action = None
        drink_ev.conditional = None
        drink_ev.action = None
        persistent._mas_coffee_brew_time = None
        persistent._mas_coffee_cup_done = None
        mas_rmEVL(brew_ev.eventlabel)
        mas_rmEVL(drink_ev.eventlabel)


    def _mas_startupCoffeeLogic():
        """
        Runs startup logic regarding coffee stuff.

        It is assumed that this run prior to conditional checking.
        """
        
        if not persistent._mas_acs_enable_coffee:
            return
        
        
        brew_ev = mas_getEV("mas_coffee_finished_brewing")
        drink_ev = mas_getEV("mas_coffee_finished_drinking")
        _now = datetime.datetime.now()
        _chance = random.randint(1, 100)
        time_for_coffee = mas_isCoffeeTime(_now)
        
        
        def still_brew(_time):
            return (
                _time is not None
                and _time.date() == _now.date()
                and mas_isCoffeeTime(_time)
            )
        
        def still_drink(_time):
            return _time is not None and _now < _time
        
        
        
        if not time_for_coffee:
            
            
            
            
            
            if still_brew(persistent._mas_coffee_brew_time):
                
                
                
                
                if brew_ev.conditional is not None and eval(brew_ev.conditional):
                    
                    
                    mas_rmEVL(brew_ev.eventlabel)
                    mas_drinkCoffee(persistent._mas_coffee_brew_time)
                    
                    if not still_drink(persistent._mas_coffee_cup_done):
                        
                        mas_resetCoffee()
                    
                    else:
                        
                        brew_ev.conditional = None
                        brew_ev.action = None
                        persistent._mas_coffee_brew_time = None
                        monika_chr.wear_acs_pst(mas_acs_mug)
            
            elif still_drink(persistent._mas_coffee_cup_done):
                
                
                brew_ev.conditional = None
                brew_ev.action = None
                persistent._mas_coffee_brew_time = None
                mas_rmEVL(brew_ev.eventlabel)
                
                
                if not monika_chr.is_wearing_acs(mas_acs_mug):
                    monika_chr.wear_acs_pst(mas_acs_mug)
            
            else:
                
                mas_resetCoffee()
        
        else:
            
            
            
            if (
                    still_brew(persistent._mas_coffee_brew_time)
                    or still_drink(persistent._mas_coffee_cup_done)
                ):
                return
            
            
            
            
            
            mas_resetCoffee()
            
            if (
                    _now.hour < store.mas_coffee.BREW_DRINK_SPLIT
                    and _chance <= store.mas_coffee.BREW_CHANCE
                ):
                
                mas_brewCoffee()
            
            elif _chance <= store.mas_coffee.DRINK_CHANCE:
                
                mas_drinkCoffee()
                monika_chr.wear_acs_pst(mas_acs_mug)
        
        return





    def mas_isHotChocTime(_time=None):
        """
        Checks if its hot chocolate time for monika

        IN:
            _time - time to check
                If None, we use current time
                (Defualt: None)

        RETURNS:
            true if its hot chocolate time, false if not
        """
        if _time is None:
            _time = datetime.datetime.now()
        
        
        return (
            store.mas_coffee.HOTCHOC_TIME_START
            <= _time.hour <
            store.mas_coffee.HOTCHOC_TIME_END
        )


    def mas_brewHotChoc(_start_time=None):
        """
        Starts brewing hot chocolate aka sets up the hot chocolate finished
        brewing event

        IN:
            _start_time - time to start brewing the hotchoc
                If None, we assume now
                (Default: None)
        """
        if _start_time is None:
            _start_time = datetime.datetime.now()
        
        
        persistent._mas_c_hotchoc_brew_time = _start_time
        
        
        end_brew = random.randint(
            store.mas_coffee.BREW_LOW,
            store.mas_coffee.BREW_HIGH
        )
        
        
        brew_ev = mas_getEV("mas_c_hotchoc_finished_brewing")
        brew_ev.conditional = (
            "persistent._mas_c_hotchoc_brew_time is not None "
            "and (datetime.datetime.now() - "
            "persistent._mas_c_hotchoc_brew_time) "
            "> datetime.timedelta(0, {0})"
        ).format(end_brew)
        brew_ev.action = EV_ACT_QUEUE


    def mas_drinkHotChoc(_start_time=None):
        """
        Lets monika drink hot chocolate aka sets the time she should stop
        drinking hot chocolate (hot chocolate finished drinking event)

        IN:
            _start_time - time to start dirnking hot chocolate
                If None, we use now
                (Defualt: now)
        """
        if _start_time is None:
            _start_time = datetime.datetime.now()
        
        
        
        drinking_time = datetime.timedelta(
            0,
            random.randint(
                store.mas_coffee.DRINK_LOW,
                store.mas_coffee.DRINK_HIGH
            )
        )
        
        
        persistent._mas_c_hotchoc_cup_done = _start_time + drinking_time
        
        
        drink_ev = mas_getEV("mas_c_hotchoc_finished_drinking")
        drink_ev.conditional = (
            "persistent._mas_c_hotchoc_cup_done is not None "
            "and datetime.datetime.now() > persistent._mas_c_hotchoc_cup_done"
        )
        drink_ev.action = EV_ACT_QUEUE
        
        
        persistent._mas_c_hotchoc_cups_drank += 1


    def mas_resetHotChoc():
        """
        Completely resets all hot chocolate vars
        NOTE: this only resets the hotchoc drinking vars, not the history
        """
        brew_ev = mas_getEV("mas_c_hotchoc_finished_brewing")
        drink_ev = mas_getEV("mas_c_hotchoc_finished_drinking")
        monika_chr.remove_acs(mas_acs_hotchoc_mug)
        brew_ev.conditional = None
        brew_ev.action = None
        drink_ev.conditional = None
        drink_ev.action = None
        persistent._mas_c_hotchoc_brew_time = None
        persistent._mas_c_hotchoc_cup_done = None
        mas_rmEVL(brew_ev.eventlabel)
        mas_rmEVL(drink_ev.eventlabel)


    def _mas_startupHotChocLogic():
        """
        Runs startup logic regarding hotchocolate stuff.

        It is assumed that this run prior to conditional checking.
        """
        
        if not persistent._mas_acs_enable_hotchoc:
            return
        
        
        brew_ev = mas_getEV("mas_c_hotchoc_finished_brewing")
        drink_ev = mas_getEV("mas_c_hotchoc_finished_drinking")
        _now = datetime.datetime.now()
        _chance = random.randint(1, 100)
        time_for_coffee = mas_isHotChocTime(_now)
        
        
        def still_brew(_time):
            return (
                _time is not None
                and _time.date() == _now.date()
                and mas_isHotChocTime(_time)
            )
        
        def still_drink(_time):
            return _time is not None and _now < _time
        
        
        
        
        if not time_for_coffee:
            
            
            
            
            
            if still_brew(persistent._mas_c_hotchoc_brew_time):
                
                
                
                
                if brew_ev.conditional is not None and eval(brew_ev.conditional):
                    
                    
                    mas_rmEVL(brew_ev.eventlabel)
                    mas_drinkHotChoc(persistent._mas_c_hotchoc_brew_time)
                    
                    if not still_drink(persistent._mas_c_hotchoc_cup_done):
                        
                        mas_resetHotChoc()
                    
                    else:
                        
                        brew_ev.conditional = None
                        brew_ev.action = None
                        persistent._mas_c_hotchoc_brew_time = None
                        monika_chr.wear_acs_pst(mas_acs_hotchoc_mug)
            
            elif still_drink(persistent._mas_c_hotchoc_cup_done):
                
                
                brew_ev.conditional = None
                brew_ev.action = None
                persistent._mas_c_hotchoc_brew_time = None
                mas_rmEVL(brew_ev.eventlabel)
                
                
                if not monika_chr.is_wearing_acs(mas_acs_hotchoc_mug):
                    monika_chr.wear_acs_pst(mas_acs_hotchoc_mug)
            
            else:
                
                mas_resetHotChoc()
        
        else:
            
            
            
            if (
                    still_brew(persistent._mas_c_hotchoc_brew_time)
                    or still_drink(persistent._mas_c_hotchoc_cup_done)
                ):
                return
            
            
            
            
            
            mas_resetHotChoc()
            
            if (
                    _now.hour < store.mas_coffee.HOTCHOC_BREW_DRINK_SPLIT
                    and _chance <= store.mas_coffee.BREW_CHANCE
                ):
                
                mas_brewHotChoc()
            
            elif _chance <= store.mas_coffee.DRINK_CHANCE:
                
                mas_drinkHotChoc()
                monika_chr.wear_acs_pst(mas_acs_hotchoc_mug)
        
        return


    def mas_startupPlushieLogic(chance=4):
        """
        Runs a simple random check for the quetzal plushie.

        IN:
            chance - value that determines the chance of that
                determines if the plushie will appear
                Defualts to 4
        """
        
        if not persistent._mas_acs_enable_quetzalplushie or mas_isF14():
            
            mas_acs_quetzalplushie.exit(monika_chr)
            return
        
        
        if renpy.random.randint(1,chance) == 1:
            if persistent._mas_d25_deco_active:
                
                monika_chr.wear_acs_pst(mas_acs_quetzalplushie_santahat)
            
            else:
                monika_chr.wear_acs_pst(mas_acs_quetzalplushie)
        
        else:
            
            mas_acs_quetzalplushie.exit(monika_chr)
        
        return


    def mas_incMoniReload():
        """
        Increments the monika reload counter unless its at max
        """
        if persistent.monika_reload < 4:
            persistent.monika_reload += 1




define audio.t1 = "<loop 22.073>bgm/1.ogg"
define audio.t2 = "<loop 4.499>bgm/2.ogg"
define audio.t2g = "bgm/2g.ogg"
define audio.t2g2 = "<from 4.499 loop 4.499>bgm/2.ogg"
define audio.t2g3 = "<loop 4.492>bgm/2g2.ogg"
define audio.t3 = "<loop 4.618>bgm/3.ogg"
define audio.t3g = "<to 15.255>bgm/3g.ogg"
define audio.t3g2 = "<from 15.255 loop 4.618>bgm/3.ogg"
define audio.t3g3 = "<loop 4.618>bgm/3g2.ogg"
define audio.t3m = "<loop 4.618>bgm/3.ogg"
define audio.t4 = "<loop 19.451>bgm/4.ogg"
define audio.t4g = "<loop 1.000>bgm/4g.ogg"
define audio.t5 = "<loop 4.444>bgm/5.ogg"
define audio.t5b = "<loop 4.444>bgm/5.ogg"
define audio.t5c = "<loop 4.444>bgm/5.ogg"
define audio.t6 = "<loop 10.893>bgm/6.ogg"
define audio.t6g = "<loop 10.893>bgm/6g.ogg"
define audio.t6r = "<to 39.817 loop 0>bgm/6r.ogg"
define audio.t6s = "<loop 43.572>bgm/6s.ogg"
define audio.t7 = "<loop 2.291>bgm/7.ogg"
define audio.t7a = "<loop 4.316 to 12.453>bgm/7.ogg"
define audio.t7g = "<loop 31.880>bgm/7g.ogg"
define audio.t8 = "<loop 9.938>bgm/8.ogg"
define audio.t9 = "<loop 3.172>bgm/9.ogg"
define audio.t9g = "<loop 1.532>bgm/9g.ogg"
define audio.t10 = "<loop 5.861>bgm/10.ogg"
define audio.t10y = "<loop 0>bgm/10-yuri.ogg"
define audio.td = "<loop 36.782>bgm/d.ogg"

define audio.m1 = "bgm/m1.ogg"
define audio.mend = "<loop 6.424>bgm/monika-end.ogg"

define audio.ghostmenu = "<loop 0>bgm/ghostmenu.ogg"
define audio.g1 = "<loop 0>bgm/g1.ogg"
define audio.g2 = "<loop 0>bgm/g2.ogg"
define audio.hb = "<loop 0>bgm/heartbeat.ogg"

define audio.closet_open = "sfx/closet-open.ogg"
define audio.closet_close = "sfx/closet-close.ogg"
define audio.page_turn = "sfx/pageflip.ogg"
define audio.fall = "sfx/fall.ogg"



define audio.rain = "mod_assets/sounds/amb/rain_2.ogg"


image black = "#000000"
image dark = "#000000e4"
image darkred = "#110000c8"
image white = "#ffffff"
image splash = "bg/splash.png"
image end:
    truecenter
    "gui/end.png"
image bg residential_day = "bg/residential.png"
image bg class_day = "bg/class.png"
image bg corridor = "bg/corridor.png"
image bg club_day = "bg/club.png"
image bg club_day2:
    choice:
        "bg club_day"
    choice:
        "bg club_day"
    choice:
        "bg club_day"
    choice:
        "bg club_day"
    choice:
        "bg club_day"
    choice:
        "bg/club-skill.png"
image bg closet = "bg/closet.png"
image bg bedroom = "bg/bedroom.png"
image bg sayori_bedroom = "bg/sayori_bedroom.png"
image bg house = "bg/house.png"
image bg kitchen = "bg/kitchen.png"

image bg notebook = "bg/notebook.png"
image bg notebook-glitch = "bg/notebook-glitch.png"

image bg glitch = LiveTile("bg/glitch.jpg")

image glitch_color:
    ytile 3
    zoom 2.5
    parallel:
        "bg/glitch-red.png"
        0.1
        "bg/glitch-green.png"
        0.1
        "bg/glitch-blue.png"
        0.1
        repeat
    parallel:
        yoffset 720
        linear 0.5 yoffset 0
        repeat
    parallel:
        choice:
            xoffset 0
        choice:
            xoffset 10
        choice:
            xoffset 20
        choice:
            xoffset 35
        choice:
            xoffset -10
        choice:
            xoffset -20
        choice:
            xoffset -30
        0.01
        repeat
    parallel:
        alpha 0.6
        linear 0.15 alpha 0.1
        0.2
        alpha 0.6
        linear 0.15 alpha 0.1
        0.2
        alpha 0.7
        linear 0.45 alpha 0



image glitch_color2:
    ytile 3
    zoom 2.5
    parallel:
        "bg/glitch-red.png"
        0.1
        "bg/glitch-green.png"
        0.1
        "bg/glitch-blue.png"
        0.1
        repeat
    parallel:
        yoffset 720
        linear 0.5 yoffset 0
        repeat
    parallel:
        choice:
            xoffset 0
        choice:
            xoffset 10
        choice:
            xoffset 20
        choice:
            xoffset 35
        choice:
            xoffset -10
        choice:
            xoffset -20
        choice:
            xoffset -30
        0.01
        repeat
    parallel:
        alpha 0.7
        linear 0.45 alpha 0




image sayori 1 = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/a.png")
image sayori 1a = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/a.png")
image sayori 1b = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/b.png")
image sayori 1c = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/c.png")
image sayori 1d = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/d.png")
image sayori 1e = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/e.png")
image sayori 1f = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/f.png")
image sayori 1g = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/g.png")
image sayori 1h = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/h.png")
image sayori 1i = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/i.png")
image sayori 1j = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/j.png")
image sayori 1k = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/k.png")
image sayori 1l = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/l.png")
image sayori 1m = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/m.png")
image sayori 1n = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/n.png")
image sayori 1o = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/o.png")
image sayori 1p = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/p.png")
image sayori 1q = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/q.png")
image sayori 1r = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/r.png")
image sayori 1s = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/s.png")
image sayori 1t = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/t.png")
image sayori 1u = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/u.png")
image sayori 1v = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/v.png")
image sayori 1w = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/w.png")
image sayori 1x = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/x.png")
image sayori 1y = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/y.png")

image sayori 2 = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/a.png")
image sayori 2a = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/a.png")
image sayori 2b = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/b.png")
image sayori 2c = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/c.png")
image sayori 2d = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/d.png")
image sayori 2e = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/e.png")
image sayori 2f = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/f.png")
image sayori 2g = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/g.png")
image sayori 2h = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/h.png")
image sayori 2i = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/i.png")
image sayori 2j = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/j.png")
image sayori 2k = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/k.png")
image sayori 2l = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/l.png")
image sayori 2m = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/m.png")
image sayori 2n = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/n.png")
image sayori 2o = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/o.png")
image sayori 2p = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/p.png")
image sayori 2q = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/q.png")
image sayori 2r = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/r.png")
image sayori 2s = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/s.png")
image sayori 2t = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/t.png")
image sayori 2u = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/u.png")
image sayori 2v = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/v.png")
image sayori 2w = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/w.png")
image sayori 2x = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/x.png")
image sayori 2y = im.Composite((960, 960), (0, 0), "sayori/1l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/y.png")

image sayori 3 = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/a.png")
image sayori 3a = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/a.png")
image sayori 3b = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/b.png")
image sayori 3c = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/c.png")
image sayori 3d = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/d.png")
image sayori 3e = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/e.png")
image sayori 3f = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/f.png")
image sayori 3g = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/g.png")
image sayori 3h = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/h.png")
image sayori 3i = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/i.png")
image sayori 3j = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/j.png")
image sayori 3k = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/k.png")
image sayori 3l = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/l.png")
image sayori 3m = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/m.png")
image sayori 3n = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/n.png")
image sayori 3o = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/o.png")
image sayori 3p = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/p.png")
image sayori 3q = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/q.png")
image sayori 3r = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/r.png")
image sayori 3s = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/s.png")
image sayori 3t = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/t.png")
image sayori 3u = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/u.png")
image sayori 3v = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/v.png")
image sayori 3w = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/w.png")
image sayori 3x = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/x.png")
image sayori 3y = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/1r.png", (0, 0), "sayori/y.png")

image sayori 4 = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/a.png")
image sayori 4a = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/a.png")
image sayori 4b = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/b.png")
image sayori 4c = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/c.png")
image sayori 4d = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/d.png")
image sayori 4e = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/e.png")
image sayori 4f = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/f.png")
image sayori 4g = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/g.png")
image sayori 4h = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/h.png")
image sayori 4i = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/i.png")
image sayori 4j = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/j.png")
image sayori 4k = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/k.png")
image sayori 4l = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/l.png")
image sayori 4m = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/m.png")
image sayori 4n = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/n.png")
image sayori 4o = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/o.png")
image sayori 4p = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/p.png")
image sayori 4q = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/q.png")
image sayori 4r = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/r.png")
image sayori 4s = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/s.png")
image sayori 4t = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/t.png")
image sayori 4u = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/u.png")
image sayori 4v = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/v.png")
image sayori 4w = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/w.png")
image sayori 4x = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/x.png")
image sayori 4y = im.Composite((960, 960), (0, 0), "sayori/2l.png", (0, 0), "sayori/2r.png", (0, 0), "sayori/y.png")

image sayori 5 = im.Composite((960, 960), (0, 0), "sayori/3a.png")
image sayori 5a = im.Composite((960, 960), (0, 0), "sayori/3a.png")
image sayori 5b = im.Composite((960, 960), (0, 0), "sayori/3b.png")
image sayori 5c = im.Composite((960, 960), (0, 0), "sayori/3c.png")
image sayori 5d = im.Composite((960, 960), (0, 0), "sayori/3d.png")

image sayori 1ba = im.Composite((960, 960), (0, 0), "sayori/1bl.png", (0, 0), "sayori/1br.png", (0, 0), "sayori/a.png")
image sayori 1bb = im.Composite((960, 960), (0, 0), "sayori/1bl.png", (0, 0), "sayori/1br.png", (0, 0), "sayori/b.png")
image sayori 1bc = im.Composite((960, 960), (0, 0), "sayori/1bl.png", (0, 0), "sayori/1br.png", (0, 0), "sayori/c.png")
image sayori 1bd = im.Composite((960, 960), (0, 0), "sayori/1bl.png", (0, 0), "sayori/1br.png", (0, 0), "sayori/d.png")
image sayori 1be = im.Composite((960, 960), (0, 0), "sayori/1bl.png", (0, 0), "sayori/1br.png", (0, 0), "sayori/e.png")
image sayori 1bf = im.Composite((960, 960), (0, 0), "sayori/1bl.png", (0, 0), "sayori/1br.png", (0, 0), "sayori/f.png")
image sayori 1bg = im.Composite((960, 960), (0, 0), "sayori/1bl.png", (0, 0), "sayori/1br.png", (0, 0), "sayori/g.png")
image sayori 1bh = im.Composite((960, 960), (0, 0), "sayori/1bl.png", (0, 0), "sayori/1br.png", (0, 0), "sayori/h.png")
image sayori 1bi = im.Composite((960, 960), (0, 0), "sayori/1bl.png", (0, 0), "sayori/1br.png", (0, 0), "sayori/i.png")
image sayori 1bj = im.Composite((960, 960), (0, 0), "sayori/1bl.png", (0, 0), "sayori/1br.png", (0, 0), "sayori/j.png")
image sayori 1bk = im.Composite((960, 960), (0, 0), "sayori/1bl.png", (0, 0), "sayori/1br.png", (0, 0), "sayori/k.png")
image sayori 1bl = im.Composite((960, 960), (0, 0), "sayori/1bl.png", (0, 0), "sayori/1br.png", (0, 0), "sayori/l.png")
image sayori 1bm = im.Composite((960, 960), (0, 0), "sayori/1bl.png", (0, 0), "sayori/1br.png", (0, 0), "sayori/m.png")
image sayori 1bn = im.Composite((960, 960), (0, 0), "sayori/1bl.png", (0, 0), "sayori/1br.png", (0, 0), "sayori/n.png")
image sayori 1bo = im.Composite((960, 960), (0, 0), "sayori/1bl.png", (0, 0), "sayori/1br.png", (0, 0), "sayori/o.png")
image sayori 1bp = im.Composite((960, 960), (0, 0), "sayori/1bl.png", (0, 0), "sayori/1br.png", (0, 0), "sayori/p.png")
image sayori 1bq = im.Composite((960, 960), (0, 0), "sayori/1bl.png", (0, 0), "sayori/1br.png", (0, 0), "sayori/q.png")
image sayori 1br = im.Composite((960, 960), (0, 0), "sayori/1bl.png", (0, 0), "sayori/1br.png", (0, 0), "sayori/r.png")
image sayori 1bs = im.Composite((960, 960), (0, 0), "sayori/1bl.png", (0, 0), "sayori/1br.png", (0, 0), "sayori/s.png")
image sayori 1bt = im.Composite((960, 960), (0, 0), "sayori/1bl.png", (0, 0), "sayori/1br.png", (0, 0), "sayori/t.png")
image sayori 1bu = im.Composite((960, 960), (0, 0), "sayori/1bl.png", (0, 0), "sayori/1br.png", (0, 0), "sayori/u.png")
image sayori 1bv = im.Composite((960, 960), (0, 0), "sayori/1bl.png", (0, 0), "sayori/1br.png", (0, 0), "sayori/v.png")
image sayori 1bw = im.Composite((960, 960), (0, 0), "sayori/1bl.png", (0, 0), "sayori/1br.png", (0, 0), "sayori/w.png")
image sayori 1bx = im.Composite((960, 960), (0, 0), "sayori/1bl.png", (0, 0), "sayori/1br.png", (0, 0), "sayori/x.png")
image sayori 1by = im.Composite((960, 960), (0, 0), "sayori/1bl.png", (0, 0), "sayori/1br.png", (0, 0), "sayori/y.png")

image sayori 2ba = im.Composite((960, 960), (0, 0), "sayori/1bl.png", (0, 0), "sayori/2br.png", (0, 0), "sayori/a.png")
image sayori 2bb = im.Composite((960, 960), (0, 0), "sayori/1bl.png", (0, 0), "sayori/2br.png", (0, 0), "sayori/b.png")
image sayori 2bc = im.Composite((960, 960), (0, 0), "sayori/1bl.png", (0, 0), "sayori/2br.png", (0, 0), "sayori/c.png")
image sayori 2bd = im.Composite((960, 960), (0, 0), "sayori/1bl.png", (0, 0), "sayori/2br.png", (0, 0), "sayori/d.png")
image sayori 2be = im.Composite((960, 960), (0, 0), "sayori/1bl.png", (0, 0), "sayori/2br.png", (0, 0), "sayori/e.png")
image sayori 2bf = im.Composite((960, 960), (0, 0), "sayori/1bl.png", (0, 0), "sayori/2br.png", (0, 0), "sayori/f.png")
image sayori 2bg = im.Composite((960, 960), (0, 0), "sayori/1bl.png", (0, 0), "sayori/2br.png", (0, 0), "sayori/g.png")
image sayori 2bh = im.Composite((960, 960), (0, 0), "sayori/1bl.png", (0, 0), "sayori/2br.png", (0, 0), "sayori/h.png")
image sayori 2bi = im.Composite((960, 960), (0, 0), "sayori/1bl.png", (0, 0), "sayori/2br.png", (0, 0), "sayori/i.png")
image sayori 2bj = im.Composite((960, 960), (0, 0), "sayori/1bl.png", (0, 0), "sayori/2br.png", (0, 0), "sayori/j.png")
image sayori 2bk = im.Composite((960, 960), (0, 0), "sayori/1bl.png", (0, 0), "sayori/2br.png", (0, 0), "sayori/k.png")
image sayori 2bl = im.Composite((960, 960), (0, 0), "sayori/1bl.png", (0, 0), "sayori/2br.png", (0, 0), "sayori/l.png")
image sayori 2bm = im.Composite((960, 960), (0, 0), "sayori/1bl.png", (0, 0), "sayori/2br.png", (0, 0), "sayori/m.png")
image sayori 2bn = im.Composite((960, 960), (0, 0), "sayori/1bl.png", (0, 0), "sayori/2br.png", (0, 0), "sayori/n.png")
image sayori 2bo = im.Composite((960, 960), (0, 0), "sayori/1bl.png", (0, 0), "sayori/2br.png", (0, 0), "sayori/o.png")
image sayori 2bp = im.Composite((960, 960), (0, 0), "sayori/1bl.png", (0, 0), "sayori/2br.png", (0, 0), "sayori/p.png")
image sayori 2bq = im.Composite((960, 960), (0, 0), "sayori/1bl.png", (0, 0), "sayori/2br.png", (0, 0), "sayori/q.png")
image sayori 2br = im.Composite((960, 960), (0, 0), "sayori/1bl.png", (0, 0), "sayori/2br.png", (0, 0), "sayori/r.png")
image sayori 2bs = im.Composite((960, 960), (0, 0), "sayori/1bl.png", (0, 0), "sayori/2br.png", (0, 0), "sayori/s.png")
image sayori 2bt = im.Composite((960, 960), (0, 0), "sayori/1bl.png", (0, 0), "sayori/2br.png", (0, 0), "sayori/t.png")
image sayori 2bu = im.Composite((960, 960), (0, 0), "sayori/1bl.png", (0, 0), "sayori/2br.png", (0, 0), "sayori/u.png")
image sayori 2bv = im.Composite((960, 960), (0, 0), "sayori/1bl.png", (0, 0), "sayori/2br.png", (0, 0), "sayori/v.png")
image sayori 2bw = im.Composite((960, 960), (0, 0), "sayori/1bl.png", (0, 0), "sayori/2br.png", (0, 0), "sayori/w.png")
image sayori 2bx = im.Composite((960, 960), (0, 0), "sayori/1bl.png", (0, 0), "sayori/2br.png", (0, 0), "sayori/x.png")
image sayori 2by = im.Composite((960, 960), (0, 0), "sayori/1bl.png", (0, 0), "sayori/2br.png", (0, 0), "sayori/y.png")

image sayori 3ba = im.Composite((960, 960), (0, 0), "sayori/2bl.png", (0, 0), "sayori/1br.png", (0, 0), "sayori/a.png")
image sayori 3bb = im.Composite((960, 960), (0, 0), "sayori/2bl.png", (0, 0), "sayori/1br.png", (0, 0), "sayori/b.png")
image sayori 3bc = im.Composite((960, 960), (0, 0), "sayori/2bl.png", (0, 0), "sayori/1br.png", (0, 0), "sayori/c.png")
image sayori 3bd = im.Composite((960, 960), (0, 0), "sayori/2bl.png", (0, 0), "sayori/1br.png", (0, 0), "sayori/d.png")
image sayori 3be = im.Composite((960, 960), (0, 0), "sayori/2bl.png", (0, 0), "sayori/1br.png", (0, 0), "sayori/e.png")
image sayori 3bf = im.Composite((960, 960), (0, 0), "sayori/2bl.png", (0, 0), "sayori/1br.png", (0, 0), "sayori/f.png")
image sayori 3bg = im.Composite((960, 960), (0, 0), "sayori/2bl.png", (0, 0), "sayori/1br.png", (0, 0), "sayori/g.png")
image sayori 3bh = im.Composite((960, 960), (0, 0), "sayori/2bl.png", (0, 0), "sayori/1br.png", (0, 0), "sayori/h.png")
image sayori 3bi = im.Composite((960, 960), (0, 0), "sayori/2bl.png", (0, 0), "sayori/1br.png", (0, 0), "sayori/i.png")
image sayori 3bj = im.Composite((960, 960), (0, 0), "sayori/2bl.png", (0, 0), "sayori/1br.png", (0, 0), "sayori/j.png")
image sayori 3bk = im.Composite((960, 960), (0, 0), "sayori/2bl.png", (0, 0), "sayori/1br.png", (0, 0), "sayori/k.png")
image sayori 3bl = im.Composite((960, 960), (0, 0), "sayori/2bl.png", (0, 0), "sayori/1br.png", (0, 0), "sayori/l.png")
image sayori 3bm = im.Composite((960, 960), (0, 0), "sayori/2bl.png", (0, 0), "sayori/1br.png", (0, 0), "sayori/m.png")
image sayori 3bn = im.Composite((960, 960), (0, 0), "sayori/2bl.png", (0, 0), "sayori/1br.png", (0, 0), "sayori/n.png")
image sayori 3bo = im.Composite((960, 960), (0, 0), "sayori/2bl.png", (0, 0), "sayori/1br.png", (0, 0), "sayori/o.png")
image sayori 3bp = im.Composite((960, 960), (0, 0), "sayori/2bl.png", (0, 0), "sayori/1br.png", (0, 0), "sayori/p.png")
image sayori 3bq = im.Composite((960, 960), (0, 0), "sayori/2bl.png", (0, 0), "sayori/1br.png", (0, 0), "sayori/q.png")
image sayori 3br = im.Composite((960, 960), (0, 0), "sayori/2bl.png", (0, 0), "sayori/1br.png", (0, 0), "sayori/r.png")
image sayori 3bs = im.Composite((960, 960), (0, 0), "sayori/2bl.png", (0, 0), "sayori/1br.png", (0, 0), "sayori/s.png")
image sayori 3bt = im.Composite((960, 960), (0, 0), "sayori/2bl.png", (0, 0), "sayori/1br.png", (0, 0), "sayori/t.png")
image sayori 3bu = im.Composite((960, 960), (0, 0), "sayori/2bl.png", (0, 0), "sayori/1br.png", (0, 0), "sayori/u.png")
image sayori 3bv = im.Composite((960, 960), (0, 0), "sayori/2bl.png", (0, 0), "sayori/1br.png", (0, 0), "sayori/v.png")
image sayori 3bw = im.Composite((960, 960), (0, 0), "sayori/2bl.png", (0, 0), "sayori/1br.png", (0, 0), "sayori/w.png")
image sayori 3bx = im.Composite((960, 960), (0, 0), "sayori/2bl.png", (0, 0), "sayori/1br.png", (0, 0), "sayori/x.png")
image sayori 3by = im.Composite((960, 960), (0, 0), "sayori/2bl.png", (0, 0), "sayori/1br.png", (0, 0), "sayori/y.png")

image sayori 4ba = im.Composite((960, 960), (0, 0), "sayori/2bl.png", (0, 0), "sayori/2br.png", (0, 0), "sayori/a.png")
image sayori 4bb = im.Composite((960, 960), (0, 0), "sayori/2bl.png", (0, 0), "sayori/2br.png", (0, 0), "sayori/b.png")
image sayori 4bc = im.Composite((960, 960), (0, 0), "sayori/2bl.png", (0, 0), "sayori/2br.png", (0, 0), "sayori/c.png")
image sayori 4bd = im.Composite((960, 960), (0, 0), "sayori/2bl.png", (0, 0), "sayori/2br.png", (0, 0), "sayori/d.png")
image sayori 4be = im.Composite((960, 960), (0, 0), "sayori/2bl.png", (0, 0), "sayori/2br.png", (0, 0), "sayori/e.png")
image sayori 4bf = im.Composite((960, 960), (0, 0), "sayori/2bl.png", (0, 0), "sayori/2br.png", (0, 0), "sayori/f.png")
image sayori 4bg = im.Composite((960, 960), (0, 0), "sayori/2bl.png", (0, 0), "sayori/2br.png", (0, 0), "sayori/g.png")
image sayori 4bh = im.Composite((960, 960), (0, 0), "sayori/2bl.png", (0, 0), "sayori/2br.png", (0, 0), "sayori/h.png")
image sayori 4bi = im.Composite((960, 960), (0, 0), "sayori/2bl.png", (0, 0), "sayori/2br.png", (0, 0), "sayori/i.png")
image sayori 4bj = im.Composite((960, 960), (0, 0), "sayori/2bl.png", (0, 0), "sayori/2br.png", (0, 0), "sayori/j.png")
image sayori 4bk = im.Composite((960, 960), (0, 0), "sayori/2bl.png", (0, 0), "sayori/2br.png", (0, 0), "sayori/k.png")
image sayori 4bl = im.Composite((960, 960), (0, 0), "sayori/2bl.png", (0, 0), "sayori/2br.png", (0, 0), "sayori/l.png")
image sayori 4bm = im.Composite((960, 960), (0, 0), "sayori/2bl.png", (0, 0), "sayori/2br.png", (0, 0), "sayori/m.png")
image sayori 4bn = im.Composite((960, 960), (0, 0), "sayori/2bl.png", (0, 0), "sayori/2br.png", (0, 0), "sayori/n.png")
image sayori 4bo = im.Composite((960, 960), (0, 0), "sayori/2bl.png", (0, 0), "sayori/2br.png", (0, 0), "sayori/o.png")
image sayori 4bp = im.Composite((960, 960), (0, 0), "sayori/2bl.png", (0, 0), "sayori/2br.png", (0, 0), "sayori/p.png")
image sayori 4bq = im.Composite((960, 960), (0, 0), "sayori/2bl.png", (0, 0), "sayori/2br.png", (0, 0), "sayori/q.png")
image sayori 4br = im.Composite((960, 960), (0, 0), "sayori/2bl.png", (0, 0), "sayori/2br.png", (0, 0), "sayori/r.png")
image sayori 4bs = im.Composite((960, 960), (0, 0), "sayori/2bl.png", (0, 0), "sayori/2br.png", (0, 0), "sayori/s.png")
image sayori 4bt = im.Composite((960, 960), (0, 0), "sayori/2bl.png", (0, 0), "sayori/2br.png", (0, 0), "sayori/t.png")
image sayori 4bu = im.Composite((960, 960), (0, 0), "sayori/2bl.png", (0, 0), "sayori/2br.png", (0, 0), "sayori/u.png")
image sayori 4bv = im.Composite((960, 960), (0, 0), "sayori/2bl.png", (0, 0), "sayori/2br.png", (0, 0), "sayori/v.png")
image sayori 4bw = im.Composite((960, 960), (0, 0), "sayori/2bl.png", (0, 0), "sayori/2br.png", (0, 0), "sayori/w.png")
image sayori 4bx = im.Composite((960, 960), (0, 0), "sayori/2bl.png", (0, 0), "sayori/2br.png", (0, 0), "sayori/x.png")
image sayori 4by = im.Composite((960, 960), (0, 0), "sayori/2bl.png", (0, 0), "sayori/2br.png", (0, 0), "sayori/y.png")

image sayori glitch:
    "sayori/glitch1.png"
    pause 0.01666
    "sayori/glitch2.png"
    pause 0.01666
    repeat


image natsuki 11 = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/1t.png")
image natsuki 1a = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/a.png")
image natsuki 1b = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/b.png")
image natsuki 1c = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/c.png")
image natsuki 1d = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/d.png")
image natsuki 1e = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/e.png")
image natsuki 1f = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/f.png")
image natsuki 1g = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/g.png")
image natsuki 1h = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/h.png")
image natsuki 1i = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/i.png")
image natsuki 1j = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/j.png")
image natsuki 1k = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/k.png")
image natsuki 1l = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/l.png")
image natsuki 1m = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/m.png")
image natsuki 1n = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/n.png")
image natsuki 1o = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/o.png")
image natsuki 1p = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/p.png")
image natsuki 1q = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/q.png")
image natsuki 1r = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/r.png")
image natsuki 1s = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/s.png")
image natsuki 1t = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/t.png")
image natsuki 1u = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/u.png")
image natsuki 1v = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/v.png")
image natsuki 1w = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/w.png")
image natsuki 1x = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/x.png")
image natsuki 1y = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/y.png")
image natsuki 1z = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/z.png")

image natsuki 21 = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/1t.png")
image natsuki 2a = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/a.png")
image natsuki 2b = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/b.png")
image natsuki 2c = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/c.png")
image natsuki 2d = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/d.png")
image natsuki 2e = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/e.png")
image natsuki 2f = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/f.png")
image natsuki 2g = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/g.png")
image natsuki 2h = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/h.png")
image natsuki 2i = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/i.png")
image natsuki 2j = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/j.png")
image natsuki 2k = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/k.png")
image natsuki 2l = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/l.png")
image natsuki 2m = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/m.png")
image natsuki 2n = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/n.png")
image natsuki 2o = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/o.png")
image natsuki 2p = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/p.png")
image natsuki 2q = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/q.png")
image natsuki 2r = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/r.png")
image natsuki 2s = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/s.png")
image natsuki 2t = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/t.png")
image natsuki 2u = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/u.png")
image natsuki 2v = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/v.png")
image natsuki 2w = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/w.png")
image natsuki 2x = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/x.png")
image natsuki 2y = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/y.png")
image natsuki 2z = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/z.png")

image natsuki 31 = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/1t.png")
image natsuki 3a = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/a.png")
image natsuki 3b = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/b.png")
image natsuki 3c = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/c.png")
image natsuki 3d = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/d.png")
image natsuki 3e = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/e.png")
image natsuki 3f = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/f.png")
image natsuki 3g = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/g.png")
image natsuki 3h = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/h.png")
image natsuki 3i = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/i.png")
image natsuki 3j = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/j.png")
image natsuki 3k = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/k.png")
image natsuki 3l = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/l.png")
image natsuki 3m = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/m.png")
image natsuki 3n = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/n.png")
image natsuki 3o = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/o.png")
image natsuki 3p = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/p.png")
image natsuki 3q = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/q.png")
image natsuki 3r = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/r.png")
image natsuki 3s = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/s.png")
image natsuki 3t = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/t.png")
image natsuki 3u = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/u.png")
image natsuki 3v = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/v.png")
image natsuki 3w = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/w.png")
image natsuki 3x = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/x.png")
image natsuki 3y = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/y.png")
image natsuki 3z = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/z.png")

image natsuki 41 = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/1t.png")
image natsuki 4a = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/a.png")
image natsuki 4b = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/b.png")
image natsuki 4c = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/c.png")
image natsuki 4d = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/d.png")
image natsuki 4e = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/e.png")
image natsuki 4f = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/f.png")
image natsuki 4g = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/g.png")
image natsuki 4h = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/h.png")
image natsuki 4i = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/i.png")
image natsuki 4j = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/j.png")
image natsuki 4k = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/k.png")
image natsuki 4l = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/l.png")
image natsuki 4m = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/m.png")
image natsuki 4n = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/n.png")
image natsuki 4o = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/o.png")
image natsuki 4p = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/p.png")
image natsuki 4q = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/q.png")
image natsuki 4r = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/r.png")
image natsuki 4s = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/s.png")
image natsuki 4t = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/t.png")
image natsuki 4u = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/u.png")
image natsuki 4v = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/v.png")
image natsuki 4w = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/w.png")
image natsuki 4x = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/x.png")
image natsuki 4y = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/y.png")
image natsuki 4z = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/z.png")

image natsuki 12 = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/2t.png")
image natsuki 12a = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/2ta.png")
image natsuki 12b = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/2tb.png")
image natsuki 12c = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/2tc.png")
image natsuki 12d = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/2td.png")
image natsuki 12e = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/2te.png")
image natsuki 12f = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/2tf.png")
image natsuki 12g = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/2tg.png")
image natsuki 12h = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/2th.png")
image natsuki 12i = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/2ti.png")

image natsuki 42 = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/2t.png")
image natsuki 42a = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/2ta.png")
image natsuki 42b = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/2tb.png")
image natsuki 42c = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/2tc.png")
image natsuki 42d = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/2td.png")
image natsuki 42e = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/2te.png")
image natsuki 42f = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/2tf.png")
image natsuki 42g = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/2tg.png")
image natsuki 42h = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/2th.png")
image natsuki 42i = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/2ti.png")

image natsuki 51 = im.Composite((960, 960), (18, 22), "natsuki/1t.png", (0, 0), "natsuki/3.png")
image natsuki 5a = im.Composite((960, 960), (18, 22), "natsuki/a.png", (0, 0), "natsuki/3.png")
image natsuki 5b = im.Composite((960, 960), (18, 22), "natsuki/b.png", (0, 0), "natsuki/3.png")
image natsuki 5c = im.Composite((960, 960), (18, 22), "natsuki/c.png", (0, 0), "natsuki/3.png")
image natsuki 5d = im.Composite((960, 960), (18, 22), "natsuki/d.png", (0, 0), "natsuki/3.png")
image natsuki 5e = im.Composite((960, 960), (18, 22), "natsuki/e.png", (0, 0), "natsuki/3.png")
image natsuki 5f = im.Composite((960, 960), (18, 22), "natsuki/f.png", (0, 0), "natsuki/3.png")
image natsuki 5g = im.Composite((960, 960), (18, 22), "natsuki/g.png", (0, 0), "natsuki/3.png")
image natsuki 5h = im.Composite((960, 960), (18, 22), "natsuki/h.png", (0, 0), "natsuki/3.png")
image natsuki 5i = im.Composite((960, 960), (18, 22), "natsuki/i.png", (0, 0), "natsuki/3.png")
image natsuki 5j = im.Composite((960, 960), (18, 22), "natsuki/j.png", (0, 0), "natsuki/3.png")
image natsuki 5k = im.Composite((960, 960), (18, 22), "natsuki/k.png", (0, 0), "natsuki/3.png")
image natsuki 5l = im.Composite((960, 960), (18, 22), "natsuki/l.png", (0, 0), "natsuki/3.png")
image natsuki 5m = im.Composite((960, 960), (18, 22), "natsuki/m.png", (0, 0), "natsuki/3.png")
image natsuki 5n = im.Composite((960, 960), (18, 22), "natsuki/n.png", (0, 0), "natsuki/3.png")
image natsuki 5o = im.Composite((960, 960), (18, 22), "natsuki/o.png", (0, 0), "natsuki/3.png")
image natsuki 5p = im.Composite((960, 960), (18, 22), "natsuki/p.png", (0, 0), "natsuki/3.png")
image natsuki 5q = im.Composite((960, 960), (18, 22), "natsuki/q.png", (0, 0), "natsuki/3.png")
image natsuki 5r = im.Composite((960, 960), (18, 22), "natsuki/r.png", (0, 0), "natsuki/3.png")
image natsuki 5s = im.Composite((960, 960), (18, 22), "natsuki/s.png", (0, 0), "natsuki/3.png")
image natsuki 5t = im.Composite((960, 960), (18, 22), "natsuki/t.png", (0, 0), "natsuki/3.png")
image natsuki 5u = im.Composite((960, 960), (18, 22), "natsuki/u.png", (0, 0), "natsuki/3.png")
image natsuki 5v = im.Composite((960, 960), (18, 22), "natsuki/v.png", (0, 0), "natsuki/3.png")
image natsuki 5w = im.Composite((960, 960), (18, 22), "natsuki/w.png", (0, 0), "natsuki/3.png")
image natsuki 5x = im.Composite((960, 960), (18, 22), "natsuki/x.png", (0, 0), "natsuki/3.png")
image natsuki 5y = im.Composite((960, 960), (18, 22), "natsuki/y.png", (0, 0), "natsuki/3.png")
image natsuki 5z = im.Composite((960, 960), (18, 22), "natsuki/z.png", (0, 0), "natsuki/3.png")



image natsuki 1ba = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/a.png")
image natsuki 1bb = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/b.png")
image natsuki 1bc = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/c.png")
image natsuki 1bd = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/d.png")
image natsuki 1be = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/e.png")
image natsuki 1bf = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/f.png")
image natsuki 1bg = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/g.png")
image natsuki 1bh = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/h.png")
image natsuki 1bi = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/i.png")
image natsuki 1bj = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/j.png")
image natsuki 1bk = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/k.png")
image natsuki 1bl = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/l.png")
image natsuki 1bm = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/m.png")
image natsuki 1bn = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/n.png")
image natsuki 1bo = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/o.png")
image natsuki 1bp = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/p.png")
image natsuki 1bq = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/q.png")
image natsuki 1br = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/r.png")
image natsuki 1bs = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/s.png")
image natsuki 1bt = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/t.png")
image natsuki 1bu = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/u.png")
image natsuki 1bv = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/v.png")
image natsuki 1bw = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/w.png")
image natsuki 1bx = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/x.png")
image natsuki 1by = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/y.png")
image natsuki 1bz = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/z.png")

image natsuki 2ba = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/a.png")
image natsuki 2bb = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/b.png")
image natsuki 2bc = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/c.png")
image natsuki 2bd = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/d.png")
image natsuki 2be = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/e.png")
image natsuki 2bf = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/f.png")
image natsuki 2bg = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/g.png")
image natsuki 2bh = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/h.png")
image natsuki 2bi = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/i.png")
image natsuki 2bj = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/j.png")
image natsuki 2bk = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/k.png")
image natsuki 2bl = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/l.png")
image natsuki 2bm = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/m.png")
image natsuki 2bn = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/n.png")
image natsuki 2bo = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/o.png")
image natsuki 2bp = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/p.png")
image natsuki 2bq = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/q.png")
image natsuki 2br = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/r.png")
image natsuki 2bs = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/s.png")
image natsuki 2bt = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/t.png")
image natsuki 2bu = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/u.png")
image natsuki 2bv = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/v.png")
image natsuki 2bw = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/w.png")
image natsuki 2bx = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/x.png")
image natsuki 2by = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/y.png")
image natsuki 2bz = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/z.png")

image natsuki 3ba = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/a.png")
image natsuki 3bb = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/b.png")
image natsuki 3bc = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/c.png")
image natsuki 3bd = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/d.png")
image natsuki 3be = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/e.png")
image natsuki 3bf = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/f.png")
image natsuki 3bg = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/g.png")
image natsuki 3bh = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/h.png")
image natsuki 3bi = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/i.png")
image natsuki 3bj = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/j.png")
image natsuki 3bk = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/k.png")
image natsuki 3bl = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/l.png")
image natsuki 3bm = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/m.png")
image natsuki 3bn = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/n.png")
image natsuki 3bo = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/o.png")
image natsuki 3bp = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/p.png")
image natsuki 3bq = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/q.png")
image natsuki 3br = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/r.png")
image natsuki 3bs = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/s.png")
image natsuki 3bt = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/t.png")
image natsuki 3bu = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/u.png")
image natsuki 3bv = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/v.png")
image natsuki 3bw = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/w.png")
image natsuki 3bx = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/x.png")
image natsuki 3by = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/y.png")
image natsuki 3bz = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/z.png")

image natsuki 4ba = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/a.png")
image natsuki 4bb = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/b.png")
image natsuki 4bc = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/c.png")
image natsuki 4bd = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/d.png")
image natsuki 4be = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/e.png")
image natsuki 4bf = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/f.png")
image natsuki 4bg = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/g.png")
image natsuki 4bh = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/h.png")
image natsuki 4bi = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/i.png")
image natsuki 4bj = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/j.png")
image natsuki 4bk = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/k.png")
image natsuki 4bl = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/l.png")
image natsuki 4bm = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/m.png")
image natsuki 4bn = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/n.png")
image natsuki 4bo = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/o.png")
image natsuki 4bp = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/p.png")
image natsuki 4bq = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/q.png")
image natsuki 4br = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/r.png")
image natsuki 4bs = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/s.png")
image natsuki 4bt = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/t.png")
image natsuki 4bu = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/u.png")
image natsuki 4bv = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/v.png")
image natsuki 4bw = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/w.png")
image natsuki 4bx = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/x.png")
image natsuki 4by = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/y.png")
image natsuki 4bz = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/z.png")

image natsuki 12ba = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/2bta.png")
image natsuki 12bb = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/2btb.png")
image natsuki 12bc = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/2btc.png")
image natsuki 12bd = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/2btd.png")
image natsuki 12be = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/2bte.png")
image natsuki 12bf = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/2btf.png")
image natsuki 12bg = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/2btg.png")
image natsuki 12bh = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/2bth.png")
image natsuki 12bi = im.Composite((960, 960), (0, 0), "natsuki/1bl.png", (0, 0), "natsuki/1br.png", (0, 0), "natsuki/2bti.png")

image natsuki 42ba = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/2bta.png")
image natsuki 42bb = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/2btb.png")
image natsuki 42bc = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/2btc.png")
image natsuki 42bd = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/2btd.png")
image natsuki 42be = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/2bte.png")
image natsuki 42bf = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/2btf.png")
image natsuki 42bg = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/2btg.png")
image natsuki 42bh = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/2bth.png")
image natsuki 42bi = im.Composite((960, 960), (0, 0), "natsuki/2bl.png", (0, 0), "natsuki/2br.png", (0, 0), "natsuki/2bti.png")

image natsuki 5ba = im.Composite((960, 960), (18, 22), "natsuki/a.png", (0, 0), "natsuki/3b.png")
image natsuki 5bb = im.Composite((960, 960), (18, 22), "natsuki/b.png", (0, 0), "natsuki/3b.png")
image natsuki 5bc = im.Composite((960, 960), (18, 22), "natsuki/c.png", (0, 0), "natsuki/3b.png")
image natsuki 5bd = im.Composite((960, 960), (18, 22), "natsuki/d.png", (0, 0), "natsuki/3b.png")
image natsuki 5be = im.Composite((960, 960), (18, 22), "natsuki/e.png", (0, 0), "natsuki/3b.png")
image natsuki 5bf = im.Composite((960, 960), (18, 22), "natsuki/f.png", (0, 0), "natsuki/3b.png")
image natsuki 5bg = im.Composite((960, 960), (18, 22), "natsuki/g.png", (0, 0), "natsuki/3b.png")
image natsuki 5bh = im.Composite((960, 960), (18, 22), "natsuki/h.png", (0, 0), "natsuki/3b.png")
image natsuki 5bi = im.Composite((960, 960), (18, 22), "natsuki/i.png", (0, 0), "natsuki/3b.png")
image natsuki 5bj = im.Composite((960, 960), (18, 22), "natsuki/j.png", (0, 0), "natsuki/3b.png")
image natsuki 5bk = im.Composite((960, 960), (18, 22), "natsuki/k.png", (0, 0), "natsuki/3b.png")
image natsuki 5bl = im.Composite((960, 960), (18, 22), "natsuki/l.png", (0, 0), "natsuki/3b.png")
image natsuki 5bm = im.Composite((960, 960), (18, 22), "natsuki/m.png", (0, 0), "natsuki/3b.png")
image natsuki 5bn = im.Composite((960, 960), (18, 22), "natsuki/n.png", (0, 0), "natsuki/3b.png")
image natsuki 5bo = im.Composite((960, 960), (18, 22), "natsuki/o.png", (0, 0), "natsuki/3b.png")
image natsuki 5bp = im.Composite((960, 960), (18, 22), "natsuki/p.png", (0, 0), "natsuki/3b.png")
image natsuki 5bq = im.Composite((960, 960), (18, 22), "natsuki/q.png", (0, 0), "natsuki/3b.png")
image natsuki 5br = im.Composite((960, 960), (18, 22), "natsuki/r.png", (0, 0), "natsuki/3b.png")
image natsuki 5bs = im.Composite((960, 960), (18, 22), "natsuki/s.png", (0, 0), "natsuki/3b.png")
image natsuki 5bt = im.Composite((960, 960), (18, 22), "natsuki/t.png", (0, 0), "natsuki/3b.png")
image natsuki 5bu = im.Composite((960, 960), (18, 22), "natsuki/u.png", (0, 0), "natsuki/3b.png")
image natsuki 5bv = im.Composite((960, 960), (18, 22), "natsuki/v.png", (0, 0), "natsuki/3b.png")
image natsuki 5bw = im.Composite((960, 960), (18, 22), "natsuki/w.png", (0, 0), "natsuki/3b.png")
image natsuki 5bx = im.Composite((960, 960), (18, 22), "natsuki/x.png", (0, 0), "natsuki/3b.png")
image natsuki 5by = im.Composite((960, 960), (18, 22), "natsuki/y.png", (0, 0), "natsuki/3b.png")
image natsuki 5bz = im.Composite((960, 960), (18, 22), "natsuki/z.png", (0, 0), "natsuki/3b.png")


image natsuki 1 = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/1t.png")
image natsuki 2 = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/1t.png")
image natsuki 3 = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/1t.png")
image natsuki 4 = im.Composite((960, 960), (0, 0), "natsuki/2l.png", (0, 0), "natsuki/2r.png", (0, 0), "natsuki/1t.png")
image natsuki 5 = im.Composite((960, 960), (18, 22), "natsuki/1t.png", (0, 0), "natsuki/3.png")

image natsuki mouth = LiveComposite((960, 960), (0, 0), "natsuki/0.png", (390, 340), "n_rects_mouth", (480, 334), "n_rects_mouth")

image n_rects_mouth:
    RectCluster(Solid("#000"), 4, 15, 5).sm
    size (20, 25)

image n_moving_mouth:
    "images/natsuki/mouth.png"
    pos (615, 305)
    xanchor 0.5 yanchor 0.5
    parallel:
        choice:
            ease 0.10 yzoom 0.2
        choice:
            ease 0.05 yzoom 0.2
        choice:
            ease 0.075 yzoom 0.2
        pass
        choice:
            0.02
        choice:
            0.04
        choice:
            0.06
        choice:
            0.08
        pass
        choice:
            ease 0.10 yzoom 1
        choice:
            ease 0.05 yzoom 1
        choice:
            ease 0.075 yzoom 1
        pass
        choice:
            0.02
        choice:
            0.04
        choice:
            0.06
        choice:
            0.08
        repeat
    parallel:
        choice:
            0.2
        choice:
            0.4
        choice:
            0.6
        ease 0.2 xzoom 0.4
        ease 0.2 xzoom 0.8
        repeat

image natsuki_ghost_blood:
    "#00000000"
    "natsuki/ghost_blood.png" with ImageDissolve("images/menu/wipedown.png", 80.0, ramplen=4, alpha=True)
    pos (620,320) zoom 0.80

image natsuki ghost_base:
    "natsuki/ghost1.png"
image natsuki ghost1:
    "natsuki 11"
    "natsuki ghost_base" with Dissolve(20.0, alpha=True)
image natsuki ghost2 = Image("natsuki/ghost2.png")
image natsuki ghost3 = Image("natsuki/ghost3.png")
image natsuki ghost4:
    "natsuki ghost3"
    parallel:
        easeout 0.25 zoom 4.5 yoffset 1200
    parallel:
        ease 0.025 xoffset -20
        ease 0.025 xoffset 20
        repeat
    0.25
    "black"
image natsuki glitch1:
    "natsuki/glitch1.png"
    zoom 1.25
    block:
        yoffset 300 xoffset 100 ytile 2
        linear 0.15 yoffset 200
        repeat
    time 0.75
    yoffset 0 zoom 1 xoffset 0 ytile 1
    "natsuki 4e"

image natsuki scream = im.Composite((960, 960), (0, 0), "natsuki/1l.png", (0, 0), "natsuki/1r.png", (0, 0), "natsuki/scream.png")
image natsuki vomit = "natsuki/vomit.png"

image n_blackeyes = "images/natsuki/blackeyes.png"
image n_eye = "images/natsuki/eye.png"


image yuri 1 = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/1r.png", (0, 0), "yuri/a.png")
image yuri 2 = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/a.png")
image yuri 3 = im.Composite((960, 960), (0, 0), "yuri/2l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/a.png")
image yuri 4 = im.Composite((960, 960), (0, 0), "yuri/3.png", (0, 0), "yuri/a2.png")

image yuri 1a = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/1r.png", (0, 0), "yuri/a.png")
image yuri 1b = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/1r.png", (0, 0), "yuri/b.png")
image yuri 1c = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/1r.png", (0, 0), "yuri/c.png")
image yuri 1d = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/1r.png", (0, 0), "yuri/d.png")
image yuri 1e = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/1r.png", (0, 0), "yuri/e.png")
image yuri 1f = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/1r.png", (0, 0), "yuri/f.png")
image yuri 1g = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/1r.png", (0, 0), "yuri/g.png")
image yuri 1h = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/1r.png", (0, 0), "yuri/h.png")
image yuri 1i = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/1r.png", (0, 0), "yuri/i.png")
image yuri 1j = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/1r.png", (0, 0), "yuri/j.png")
image yuri 1k = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/1r.png", (0, 0), "yuri/k.png")
image yuri 1l = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/1r.png", (0, 0), "yuri/l.png")
image yuri 1m = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/1r.png", (0, 0), "yuri/m.png")
image yuri 1n = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/1r.png", (0, 0), "yuri/n.png")
image yuri 1o = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/1r.png", (0, 0), "yuri/o.png")
image yuri 1p = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/1r.png", (0, 0), "yuri/p.png")
image yuri 1q = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/1r.png", (0, 0), "yuri/q.png")
image yuri 1r = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/1r.png", (0, 0), "yuri/r.png")
image yuri 1s = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/1r.png", (0, 0), "yuri/s.png")
image yuri 1t = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/1r.png", (0, 0), "yuri/t.png")
image yuri 1u = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/1r.png", (0, 0), "yuri/u.png")
image yuri 1v = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/1r.png", (0, 0), "yuri/v.png")
image yuri 1w = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/1r.png", (0, 0), "yuri/w.png")

image yuri 1y1 = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/1r.png", (0, 0), "yuri/y1.png")
image yuri 1y2 = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/1r.png", (0, 0), "yuri/y2.png")
image yuri 1y3 = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/1r.png", (0, 0), "yuri/y3.png")
image yuri 1y4 = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/1r.png", (0, 0), "yuri/y4.png")
image yuri 1y5 = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/1r.png", (0, 0), "yuri/y5.png")
image yuri 1y6 = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/1r.png", (0, 0), "yuri/y6.png")
image yuri 1y7 = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/1r.png", (0, 0), "yuri/y7.png")

image yuri 2a = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/a.png")
image yuri 2b = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/b.png")
image yuri 2c = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/c.png")
image yuri 2d = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/d.png")
image yuri 2e = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/e.png")
image yuri 2f = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/f.png")
image yuri 2g = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/g.png")
image yuri 2h = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/h.png")
image yuri 2i = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/i.png")
image yuri 2j = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/j.png")
image yuri 2k = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/k.png")
image yuri 2l = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/l.png")
image yuri 2m = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/m.png")
image yuri 2n = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/n.png")
image yuri 2o = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/o.png")
image yuri 2p = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/p.png")
image yuri 2q = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/q.png")
image yuri 2r = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/r.png")
image yuri 2s = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/s.png")
image yuri 2t = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/t.png")
image yuri 2u = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/u.png")
image yuri 2v = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/v.png")
image yuri 2w = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/w.png")

image yuri 2y1 = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/y1.png")
image yuri 2y2 = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/y2.png")
image yuri 2y3 = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/y3.png")
image yuri 2y4 = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/y4.png")
image yuri 2y5 = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/y5.png")
image yuri 2y6 = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/y6.png")
image yuri 2y7 = im.Composite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/y7.png")

image yuri 3a = im.Composite((960, 960), (0, 0), "yuri/2l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/a.png")
image yuri 3b = im.Composite((960, 960), (0, 0), "yuri/2l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/b.png")
image yuri 3c = im.Composite((960, 960), (0, 0), "yuri/2l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/c.png")
image yuri 3d = im.Composite((960, 960), (0, 0), "yuri/2l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/d.png")
image yuri 3e = im.Composite((960, 960), (0, 0), "yuri/2l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/e.png")
image yuri 3f = im.Composite((960, 960), (0, 0), "yuri/2l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/f.png")
image yuri 3g = im.Composite((960, 960), (0, 0), "yuri/2l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/g.png")
image yuri 3h = im.Composite((960, 960), (0, 0), "yuri/2l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/h.png")
image yuri 3i = im.Composite((960, 960), (0, 0), "yuri/2l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/i.png")
image yuri 3j = im.Composite((960, 960), (0, 0), "yuri/2l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/j.png")
image yuri 3k = im.Composite((960, 960), (0, 0), "yuri/2l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/k.png")
image yuri 3l = im.Composite((960, 960), (0, 0), "yuri/2l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/l.png")
image yuri 3m = im.Composite((960, 960), (0, 0), "yuri/2l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/m.png")
image yuri 3n = im.Composite((960, 960), (0, 0), "yuri/2l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/n.png")
image yuri 3o = im.Composite((960, 960), (0, 0), "yuri/2l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/o.png")
image yuri 3p = im.Composite((960, 960), (0, 0), "yuri/2l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/p.png")
image yuri 3q = im.Composite((960, 960), (0, 0), "yuri/2l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/q.png")
image yuri 3r = im.Composite((960, 960), (0, 0), "yuri/2l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/r.png")
image yuri 3s = im.Composite((960, 960), (0, 0), "yuri/2l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/s.png")
image yuri 3t = im.Composite((960, 960), (0, 0), "yuri/2l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/t.png")
image yuri 3u = im.Composite((960, 960), (0, 0), "yuri/2l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/u.png")
image yuri 3v = im.Composite((960, 960), (0, 0), "yuri/2l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/v.png")
image yuri 3w = im.Composite((960, 960), (0, 0), "yuri/2l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/w.png")

image yuri 3y1 = im.Composite((960, 960), (0, 0), "yuri/2l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/y1.png")
image yuri 3y2 = im.Composite((960, 960), (0, 0), "yuri/2l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/y2.png")
image yuri 3y3 = im.Composite((960, 960), (0, 0), "yuri/2l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/y3.png")
image yuri 3y4 = im.Composite((960, 960), (0, 0), "yuri/2l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/y4.png")
image yuri 3y5 = im.Composite((960, 960), (0, 0), "yuri/2l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/y5.png")
image yuri 3y6 = im.Composite((960, 960), (0, 0), "yuri/2l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/y6.png")
image yuri 3y7 = im.Composite((960, 960), (0, 0), "yuri/2l.png", (0, 0), "yuri/2r.png", (0, 0), "yuri/y7.png")

image yuri 4a = im.Composite((960, 960), (0, 0), "yuri/3.png", (0, 0), "yuri/a2.png")
image yuri 4b = im.Composite((960, 960), (0, 0), "yuri/3.png", (0, 0), "yuri/b2.png")
image yuri 4c = im.Composite((960, 960), (0, 0), "yuri/3.png", (0, 0), "yuri/c2.png")
image yuri 4d = im.Composite((960, 960), (0, 0), "yuri/3.png", (0, 0), "yuri/d2.png")
image yuri 4e = im.Composite((960, 960), (0, 0), "yuri/3.png", (0, 0), "yuri/e2.png")

image yuri 1ba = im.Composite((960, 960), (0, 0), "yuri/a.png", (0, 0), "yuri/1bl.png", (0, 0), "yuri/1br.png")
image yuri 1bb = im.Composite((960, 960), (0, 0), "yuri/b.png", (0, 0), "yuri/1bl.png", (0, 0), "yuri/1br.png")
image yuri 1bc = im.Composite((960, 960), (0, 0), "yuri/c.png", (0, 0), "yuri/1bl.png", (0, 0), "yuri/1br.png")
image yuri 1bd = im.Composite((960, 960), (0, 0), "yuri/d.png", (0, 0), "yuri/1bl.png", (0, 0), "yuri/1br.png")
image yuri 1be = im.Composite((960, 960), (0, 0), "yuri/e.png", (0, 0), "yuri/1bl.png", (0, 0), "yuri/1br.png")
image yuri 1bf = im.Composite((960, 960), (0, 0), "yuri/f.png", (0, 0), "yuri/1bl.png", (0, 0), "yuri/1br.png")
image yuri 1bg = im.Composite((960, 960), (0, 0), "yuri/g.png", (0, 0), "yuri/1bl.png", (0, 0), "yuri/1br.png")
image yuri 1bh = im.Composite((960, 960), (0, 0), "yuri/h.png", (0, 0), "yuri/1bl.png", (0, 0), "yuri/1br.png")
image yuri 1bi = im.Composite((960, 960), (0, 0), "yuri/i.png", (0, 0), "yuri/1bl.png", (0, 0), "yuri/1br.png")
image yuri 1bj = im.Composite((960, 960), (0, 0), "yuri/j.png", (0, 0), "yuri/1bl.png", (0, 0), "yuri/1br.png")
image yuri 1bk = im.Composite((960, 960), (0, 0), "yuri/k.png", (0, 0), "yuri/1bl.png", (0, 0), "yuri/1br.png")
image yuri 1bl = im.Composite((960, 960), (0, 0), "yuri/l.png", (0, 0), "yuri/1bl.png", (0, 0), "yuri/1br.png")
image yuri 1bm = im.Composite((960, 960), (0, 0), "yuri/m.png", (0, 0), "yuri/1bl.png", (0, 0), "yuri/1br.png")
image yuri 1bn = im.Composite((960, 960), (0, 0), "yuri/n.png", (0, 0), "yuri/1bl.png", (0, 0), "yuri/1br.png")
image yuri 1bo = im.Composite((960, 960), (0, 0), "yuri/o.png", (0, 0), "yuri/1bl.png", (0, 0), "yuri/1br.png")
image yuri 1bp = im.Composite((960, 960), (0, 0), "yuri/p.png", (0, 0), "yuri/1bl.png", (0, 0), "yuri/1br.png")
image yuri 1bq = im.Composite((960, 960), (0, 0), "yuri/q.png", (0, 0), "yuri/1bl.png", (0, 0), "yuri/1br.png")
image yuri 1br = im.Composite((960, 960), (0, 0), "yuri/r.png", (0, 0), "yuri/1bl.png", (0, 0), "yuri/1br.png")
image yuri 1bs = im.Composite((960, 960), (0, 0), "yuri/s.png", (0, 0), "yuri/1bl.png", (0, 0), "yuri/1br.png")
image yuri 1bt = im.Composite((960, 960), (0, 0), "yuri/t.png", (0, 0), "yuri/1bl.png", (0, 0), "yuri/1br.png")
image yuri 1bu = im.Composite((960, 960), (0, 0), "yuri/u.png", (0, 0), "yuri/1bl.png", (0, 0), "yuri/1br.png")
image yuri 1bv = im.Composite((960, 960), (0, 0), "yuri/v.png", (0, 0), "yuri/1bl.png", (0, 0), "yuri/1br.png")
image yuri 1bw = im.Composite((960, 960), (0, 0), "yuri/w.png", (0, 0), "yuri/1bl.png", (0, 0), "yuri/1br.png")

image yuri 2ba = im.Composite((960, 960), (0, 0), "yuri/a.png", (0, 0), "yuri/1bl.png", (0, 0), "yuri/2br.png")
image yuri 2bb = im.Composite((960, 960), (0, 0), "yuri/b.png", (0, 0), "yuri/1bl.png", (0, 0), "yuri/2br.png")
image yuri 2bc = im.Composite((960, 960), (0, 0), "yuri/c.png", (0, 0), "yuri/1bl.png", (0, 0), "yuri/2br.png")
image yuri 2bd = im.Composite((960, 960), (0, 0), "yuri/d.png", (0, 0), "yuri/1bl.png", (0, 0), "yuri/2br.png")
image yuri 2be = im.Composite((960, 960), (0, 0), "yuri/e.png", (0, 0), "yuri/1bl.png", (0, 0), "yuri/2br.png")
image yuri 2bf = im.Composite((960, 960), (0, 0), "yuri/f.png", (0, 0), "yuri/1bl.png", (0, 0), "yuri/2br.png")
image yuri 2bg = im.Composite((960, 960), (0, 0), "yuri/g.png", (0, 0), "yuri/1bl.png", (0, 0), "yuri/2br.png")
image yuri 2bh = im.Composite((960, 960), (0, 0), "yuri/h.png", (0, 0), "yuri/1bl.png", (0, 0), "yuri/2br.png")
image yuri 2bi = im.Composite((960, 960), (0, 0), "yuri/i.png", (0, 0), "yuri/1bl.png", (0, 0), "yuri/2br.png")
image yuri 2bj = im.Composite((960, 960), (0, 0), "yuri/j.png", (0, 0), "yuri/1bl.png", (0, 0), "yuri/2br.png")
image yuri 2bk = im.Composite((960, 960), (0, 0), "yuri/k.png", (0, 0), "yuri/1bl.png", (0, 0), "yuri/2br.png")
image yuri 2bl = im.Composite((960, 960), (0, 0), "yuri/l.png", (0, 0), "yuri/1bl.png", (0, 0), "yuri/2br.png")
image yuri 2bm = im.Composite((960, 960), (0, 0), "yuri/m.png", (0, 0), "yuri/1bl.png", (0, 0), "yuri/2br.png")
image yuri 2bn = im.Composite((960, 960), (0, 0), "yuri/n.png", (0, 0), "yuri/1bl.png", (0, 0), "yuri/2br.png")
image yuri 2bo = im.Composite((960, 960), (0, 0), "yuri/o.png", (0, 0), "yuri/1bl.png", (0, 0), "yuri/2br.png")
image yuri 2bp = im.Composite((960, 960), (0, 0), "yuri/p.png", (0, 0), "yuri/1bl.png", (0, 0), "yuri/2br.png")
image yuri 2bq = im.Composite((960, 960), (0, 0), "yuri/q.png", (0, 0), "yuri/1bl.png", (0, 0), "yuri/2br.png")
image yuri 2br = im.Composite((960, 960), (0, 0), "yuri/r.png", (0, 0), "yuri/1bl.png", (0, 0), "yuri/2br.png")
image yuri 2bs = im.Composite((960, 960), (0, 0), "yuri/s.png", (0, 0), "yuri/1bl.png", (0, 0), "yuri/2br.png")
image yuri 2bt = im.Composite((960, 960), (0, 0), "yuri/t.png", (0, 0), "yuri/1bl.png", (0, 0), "yuri/2br.png")
image yuri 2bu = im.Composite((960, 960), (0, 0), "yuri/u.png", (0, 0), "yuri/1bl.png", (0, 0), "yuri/2br.png")
image yuri 2bv = im.Composite((960, 960), (0, 0), "yuri/v.png", (0, 0), "yuri/1bl.png", (0, 0), "yuri/2br.png")
image yuri 2bw = im.Composite((960, 960), (0, 0), "yuri/w.png", (0, 0), "yuri/1bl.png", (0, 0), "yuri/2br.png")

image yuri 3ba = im.Composite((960, 960), (0, 0), "yuri/a.png", (0, 0), "yuri/2bl.png", (0, 0), "yuri/2br.png")
image yuri 3bb = im.Composite((960, 960), (0, 0), "yuri/b.png", (0, 0), "yuri/2bl.png", (0, 0), "yuri/2br.png")
image yuri 3bc = im.Composite((960, 960), (0, 0), "yuri/c.png", (0, 0), "yuri/2bl.png", (0, 0), "yuri/2br.png")
image yuri 3bd = im.Composite((960, 960), (0, 0), "yuri/d.png", (0, 0), "yuri/2bl.png", (0, 0), "yuri/2br.png")
image yuri 3be = im.Composite((960, 960), (0, 0), "yuri/e.png", (0, 0), "yuri/2bl.png", (0, 0), "yuri/2br.png")
image yuri 3bf = im.Composite((960, 960), (0, 0), "yuri/f.png", (0, 0), "yuri/2bl.png", (0, 0), "yuri/2br.png")
image yuri 3bg = im.Composite((960, 960), (0, 0), "yuri/g.png", (0, 0), "yuri/2bl.png", (0, 0), "yuri/2br.png")
image yuri 3bh = im.Composite((960, 960), (0, 0), "yuri/h.png", (0, 0), "yuri/2bl.png", (0, 0), "yuri/2br.png")
image yuri 3bi = im.Composite((960, 960), (0, 0), "yuri/i.png", (0, 0), "yuri/2bl.png", (0, 0), "yuri/2br.png")
image yuri 3bj = im.Composite((960, 960), (0, 0), "yuri/j.png", (0, 0), "yuri/2bl.png", (0, 0), "yuri/2br.png")
image yuri 3bk = im.Composite((960, 960), (0, 0), "yuri/k.png", (0, 0), "yuri/2bl.png", (0, 0), "yuri/2br.png")
image yuri 3bl = im.Composite((960, 960), (0, 0), "yuri/l.png", (0, 0), "yuri/2bl.png", (0, 0), "yuri/2br.png")
image yuri 3bm = im.Composite((960, 960), (0, 0), "yuri/m.png", (0, 0), "yuri/2bl.png", (0, 0), "yuri/2br.png")
image yuri 3bn = im.Composite((960, 960), (0, 0), "yuri/n.png", (0, 0), "yuri/2bl.png", (0, 0), "yuri/2br.png")
image yuri 3bo = im.Composite((960, 960), (0, 0), "yuri/o.png", (0, 0), "yuri/2bl.png", (0, 0), "yuri/2br.png")
image yuri 3bp = im.Composite((960, 960), (0, 0), "yuri/p.png", (0, 0), "yuri/2bl.png", (0, 0), "yuri/2br.png")
image yuri 3bq = im.Composite((960, 960), (0, 0), "yuri/q.png", (0, 0), "yuri/2bl.png", (0, 0), "yuri/2br.png")
image yuri 3br = im.Composite((960, 960), (0, 0), "yuri/r.png", (0, 0), "yuri/2bl.png", (0, 0), "yuri/2br.png")
image yuri 3bs = im.Composite((960, 960), (0, 0), "yuri/s.png", (0, 0), "yuri/2bl.png", (0, 0), "yuri/2br.png")
image yuri 3bt = im.Composite((960, 960), (0, 0), "yuri/t.png", (0, 0), "yuri/2bl.png", (0, 0), "yuri/2br.png")
image yuri 3bu = im.Composite((960, 960), (0, 0), "yuri/u.png", (0, 0), "yuri/2bl.png", (0, 0), "yuri/2br.png")
image yuri 3bv = im.Composite((960, 960), (0, 0), "yuri/v.png", (0, 0), "yuri/2bl.png", (0, 0), "yuri/2br.png")
image yuri 3bw = im.Composite((960, 960), (0, 0), "yuri/w.png", (0, 0), "yuri/2bl.png", (0, 0), "yuri/2br.png")

image yuri 4ba = im.Composite((960, 960), (0, 0), "yuri/a2.png", (0, 0), "yuri/3b.png")
image yuri 4bb = im.Composite((960, 960), (0, 0), "yuri/b2.png", (0, 0), "yuri/3b.png")
image yuri 4bc = im.Composite((960, 960), (0, 0), "yuri/c2.png", (0, 0), "yuri/3b.png")
image yuri 4bd = im.Composite((960, 960), (0, 0), "yuri/d2.png", (0, 0), "yuri/3b.png")
image yuri 4be = im.Composite((960, 960), (0, 0), "yuri/e2.png", (0, 0), "yuri/3b.png")

image y_glitch_head:
    "images/yuri/za.png"
    0.15
    "images/yuri/zb.png"
    0.15
    "images/yuri/zc.png"
    0.15
    "images/yuri/zd.png"
    0.15
    repeat

image yuri stab_1 = "yuri/stab/1.png"
image yuri stab_2 = "yuri/stab/2.png"
image yuri stab_3 = "yuri/stab/3.png"
image yuri stab_4 = "yuri/stab/4.png"
image yuri stab_5 = "yuri/stab/5.png"
image yuri stab_6 = LiveComposite((960,960), (0, 0), "yuri/stab/6-mask.png", (0, 0), "yuri stab_6_eyes", (0, 0), "yuri/stab/6.png")

image yuri stab_6_eyes:
    "yuri/stab/6-eyes.png"
    subpixel True
    parallel:
        choice:
            xoffset 0.5
        choice:
            xoffset 0
        choice:
            xoffset -0.5
        0.2
        repeat
    parallel:
        choice:
            yoffset 0.5
        choice:
            yoffset 0
        choice:
            yoffset -0.5
        0.2
        repeat
    parallel:
        2.05
        easeout 1.0 yoffset -15
        linear 10 yoffset -15


image yuri oneeye = LiveComposite((960, 960), (0, 0), "yuri/1l.png", (0, 0), "yuri/1r.png", (0, 0), "yuri/oneeye.png", (0, 0), "yuri oneeye2")
image yuri oneeye2:
    "yuri/oneeye2.png"
    subpixel True
    pause 5.0
    linear 60 xoffset -50 yoffset 20

image yuri glitch:
    "yuri/glitch1.png"
    pause 0.1
    "yuri/glitch2.png"
    pause 0.1
    "yuri/glitch3.png"
    pause 0.1
    "yuri/glitch4.png"
    pause 0.1
    "yuri/glitch5.png"
    pause 0.1
    repeat
image yuri glitch2:
    "yuri/0a.png"
    pause 0.1
    "yuri/0b.png"
    pause 0.5
    "yuri/0a.png"
    pause 0.3
    "yuri/0b.png"
    pause 0.3
    "yuri 1"

image yuri eyes = LiveComposite((1280, 720), (0, 0), "yuri/eyes1.png", (0, 0), "yuripupils")

image yuri eyes_base = "yuri/eyes1.png"

image yuripupils:
    "yuri/eyes2.png"
    yuripupils_move

image yuri cuts = "yuri/cuts.png"

image yuri dragon:
    "yuri 3"
    0.25
    parallel:
        "yuri/dragon1.png"
        0.01
        "yuri/dragon2.png"
        0.01
        repeat
    parallel:
        0.01
        choice:
            xoffset -1
            xoffset -2
            xoffset -5
            xoffset -6
            xoffset -9
            xoffset -10
        0.01
        xoffset 0
        repeat
    time 0.55
    xoffset 0
    "yuri 3"


define narrator = Character(ctc="ctc", ctc_position="fixed")
define mc = DynamicCharacter('player', what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")
define s = DynamicCharacter('s_name', image='sayori', what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")
define n = DynamicCharacter('n_name', image='natsuki', what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")
define y = DynamicCharacter('y_name', image='yuri', what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")
define ny = Character('Nat & Yuri', what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")

define _dismiss_pause = config.developer

default persistent.playername = ""
default player = persistent.playername



default persistent.playthrough = 0
default persistent.yuri_kill = 0
default persistent.seen_eyes = None
default persistent.seen_sticker = None
default persistent.ghost_menu = None
default persistent.seen_ghost_menu = None
default seen_eyes_this_chapter = False
default persistent.anticheat = 0
default persistent.clear = [False, False, False, False, False, False, False, False, False, False]
default persistent.special_poems = None
default persistent.clearall = None
default persistent.menu_bg_m = None
default persistent.first_load = None
default persistent.has_merged = False
default persistent._mas_monika_nickname = "Monika"
default in_sayori_kill = None
default in_yuri_kill = None
default anticheat = 0
define config.mouse = None
default allow_skipping = True
default basedir = config.basedir
default chapter = 0
default currentpos = 0
default faint_effect = None


default s_name = "Sayori"
default m_name = persistent._mas_monika_nickname
default n_name = "Natsuki"
default y_name = "Yuri"



default n_poemappeal = [0, 0, 0]
default s_poemappeal = [0, 0, 0]
default y_poemappeal = [0, 0, 0]
default m_poemappeal = [0, 0, 0]


default poemwinner = ['sayori', 'sayori', 'sayori']


default s_readpoem = False
default n_readpoem = False
default y_readpoem = False
default m_readpoem = False


default poemsread = 0



default n_appeal = 0
default s_appeal = 0
default y_appeal = 0
default m_appeal = 0



default n_exclusivewatched = False
default y_exclusivewatched = False


default y_gave = False
default y_ranaway = False


default ch1_choice = "sayori"


default help_sayori = None
default help_monika = None


default ch4_scene = "yuri"
default ch4_name = "Yuri"
default sayori_confess = True


default natsuki_23 = None


default persistent.monika_topic = ""
default player_dialogue = persistent.monika_topic
default persistent.monika_said_topics = []
default persistent.event_list = []
default persistent.event_database = dict()
default persistent.farewell_database = dict()
default persistent.greeting_database = dict()
default persistent._mas_apology_database = dict()
default persistent.gender = "M"
default persistent.chess_strength = 3
default persistent.closed_self = False
default persistent._mas_game_crashed = False
default persistent.seen_monika_in_room = False
default persistent.ever_won = {'pong':False,'chess':False,'hangman':False,'piano':False}
default persistent.game_unlocks = {'pong':True,'chess':False,'hangman':False,'piano':False}
default persistent.sessions = {'last_session_end':None,'current_session_start':None,'total_playtime':datetime.timedelta(seconds=0),'total_sessions':0,'first_session':datetime.datetime.now()}
default persistent.playerxp = 0
default persistent.idlexp_total = 0
default persistent.random_seen = 0
default persistent._mas_affection = {"affection":0,"goodexp":1,"badexp":1,"apologyflag":False, "freeze_date": None, "today_exp":0}
default seen_random_limit = False
default persistent._mas_enable_random_repeats = False

default persistent._mas_first_calendar_check = False


define mas_is_raining = False


define MAS_RAIN_UPSET = 25
define MAS_RAIN_DIS = 40
define MAS_RAIN_BROKEN = 70


define mas_is_snowing = False


default persistent._mas_in_idle_mode = False
default persistent._mas_idle_data = {}





default persistent._mas_monika_clothes = "def"
default persistent._mas_monika_hair = "def"
default persistent._mas_likes_hairdown = False
default persistent._mas_hair_changed = False



default persistent._mas_sunrise = 6 * 60
default persistent._mas_sunset = 18 * 60


define mas_max_suntime = int((24 * 60) / 5) - 1
define mas_sunrise_prev = persistent._mas_sunrise
define mas_sunset_prev = persistent._mas_sunset
define mas_suntime.NO_CHANGE = 0
define mas_suntime.RISE_CHANGE = 1
define mas_suntime.SET_CHANGE = 2
define mas_suntime.change_state = mas_suntime.NO_CHANGE
define mas_suntime.modifier = 5



define mas_suntime.sunrise = int(persistent._mas_sunrise / 5)
define mas_suntime.sunset = int(persistent._mas_sunset / 5)

define mas_checked_update = False

define random_seen_limit = 30
define times.REST_TIME = 6*3600
define times.FULL_XP_AWAY_TIME = 24*3600
define times.HALF_XP_AWAY_TIME = 72*3600
define xp.NEW_GAME = 30
define xp.WIN_GAME = 30
define xp.AWAY_PER_HOUR = 10
define xp.IDLE_PER_MINUTE = 1
define xp.IDLE_XP_MAX = 120
define xp.NEW_EVENT = 15
define mas_skip_visuals = False
define mas_monika_twitter_handle = "lilmonix3"
define mas_monika_birthday = datetime.date(datetime.date.today().year, 9, 22)


default persistent._mas_sensitive_mode = False

init python:
    startup_check = False
    try:
        persistent.ever_won['hangman']
    except:
        persistent.ever_won['hangman']=False
    try:
        persistent.ever_won['piano']
    except:
        persistent.ever_won['piano']=False
#NOTA: NON HO LA MINIMA IDEA SE QUESTI DEVONO ESSERE TRADOTTI O NO #BHO
default his = "his"
default he = "he"
default hes = "he's"
default heis = "he is"
default bf = "boyfriend"
default man = "man"
default boy = "boy"
default guy = "guy"
default him = "him"
default himself = "himself"



default persistent._mas_randchat_freq = 0
define mas_randchat_prev = persistent._mas_randchat_freq
init 1 python in mas_randchat:




    OFTEN         = 5 
    NORMAL        = 15 
    LESS_OFTEN    = 40 
    OCCASIONALLY  = 2*60 
    RARELY        = 390 
    VERY_RARELY   = 20*60 
    NEVER         = 0


    SPAN_MULTIPLIER = 3




    SLIDER_MAP = {
        0: OFTEN,
        1: NORMAL,
        2: LESS_OFTEN,
        3: OCCASIONALLY,
        4: RARELY,
        5: VERY_RARELY,
        6: NEVER
    }

#E NEANCHE QUESTA
    SLIDER_MAP_DISP = {
        0: "Often",
        1: "Normal",
        2: "Less Often",
        3: "Occasionally",
        4: "Rarely",
        5: "Very Rarely",
        6: "Never"
    }



    rand_low = NORMAL
    rand_high = NORMAL * SPAN_MULTIPLIER
    rand_chat_waittime_left = 0

    def adjustRandFreq(slider_value):
        """
        Properly adjusts the random limits given the slider value

        IN:
            slider_value - slider value given from the slider
                Should be between 0 - 5
        """
        slider_setting = SLIDER_MAP.get(slider_value, 1)
        
        
        
        global rand_low
        global rand_high
        
        rand_low = slider_setting
        rand_high = slider_setting * SPAN_MULTIPLIER
        renpy.game.persistent._mas_randchat_freq = slider_value
        
        setWaitingTime()


    def getRandChatDisp(slider_value):
        """
        Retrieves the random chatter display string using the given slider
        value

        IN:
            slider_value - slider value given from the slider

        RETURNS:
            displayable string that reprsents the current random chatter
            setting
        """
        randchat_disp = SLIDER_MAP_DISP.get(slider_value, None)
        
        if slider_value is None:
            return "Never"
        
        return randchat_disp


    def setWaitingTime():
        """
        Sets up the waiting time for the next random chat, depending on the current random chatter selection.
        """
        global rand_chat_waittime_left
        
        rand_chat_waittime_left = renpy.random.randint(rand_low, rand_high)


    def wait():
        """
        Pauses renpy for a small amount of seconds.
        This helps adapting fast to a new random chatter selection.
        All events before a random chat can also be handled rather than to keep waiting the whole time at once.
        """
        global rand_chat_waittime_left
        
        WAITING_TIME = 5
        
        if rand_chat_waittime_left > WAITING_TIME:
            rand_chat_waittime_left -= WAITING_TIME
            renpy.pause(WAITING_TIME, hard=True)
        
        elif rand_chat_waittime_left > 0:
            waitFor = rand_chat_waittime_left
            rand_chat_waittime_left = 0
            renpy.pause(waitFor, hard=True)
        
        else:
            rand_chat_waittime_left = 0
            renpy.pause(WAITING_TIME, hard=True)


    def waitedLongEnough():
        """
        Checks whether the waiting time is up yet.

        RETURNS:
            boolean to determine whether the wait is over
        """
        global rand_chat_waittime_left
        
        return rand_chat_waittime_left == 0 and rand_low != 0




init 4 python:
    import store.mas_randchat as mas_randchat

return







# E NEANCHE QUESTO
label set_gender:
    if persistent.gender == "M":
        $ his = "his"
        $ he = "he"
        $ hes = "he's"
        $ heis = "he is"
        $ bf = "boyfriend"
        $ man = "man"
        $ boy = "boy"
        $ guy = "guy"
        $ him = "him"
        $ himself = "himself"
    elif persistent.gender == "F":
        $ his = "her"
        $ he = "she"
        $ hes = "she's"
        $ heis = "she is"
        $ bf = "girlfriend"
        $ man = "woman"
        $ boy = "girl"
        $ guy = "girl"
        $ him = "her"
        $ himself = "herself"
    else:
        $ his = "their"
        $ he = "they"
        $ hes = "they're"
        $ heis = "they are"
        $ bf = "partner"
        $ man = "person"
        $ boy = "person"
        $ guy = "person"
        $ him = "them"
        $ himself = "themselves"
    return

style jpn_text:
    font "mod_assets/font/mplus-2p-regular.ttf"


init python:
    def mas_passedILY(pass_time, check_time=None):
        '''
        Checks whether we are within the appropriate time since the last time
        Monika told the player 'ily' which is stored in persistent._mas_last_monika_ily
        IN:
            pass_time - a timedelta corresponding to the time limit we want to check against
            check_time - the time at which we want to check, will typically be datetime.datetime.now()
                which is the default

        RETURNS:
            boolean indicating if we are within the time limit
        '''
        if check_time is None:
            check_time = datetime.datetime.now()
        return persistent._mas_last_monika_ily is not None and (check_time - persistent._mas_last_monika_ily) <= pass_time

    def mas_ILY(set_time=None):
        '''
        Sets persistent._mas_last_monika_ily (the last time Monika said ily) to a given time
        IN:
            set_time - the time we want to set persistent._mas_last_monika_ily to
                defaults to datetime.datetime.now()
        '''
        if set_time is None:
            set_time = datetime.datetime.now()
        persistent._mas_last_monika_ily = set_time
