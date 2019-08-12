






define persistent._mas_zz_lupd_ex_v = []


init -10 python:
    found_monika_ani = persistent.monika_anniversary is not None
    no_topics_list = persistent.monika_random_topics is None








init 4 python:


    if persistent.version_number != config.version:
        
        persistent.monika_topic = None
        
        
        persistent._mas_unsee_unseen = False





















init python:

    def removeTopicID(topicID):
        
        
        
        
        
        
        
        
        
        
        
        if renpy.seen_label(topicID):
            persistent._seen_ever.pop(topicID)


    def mas_eraseTopic(topicID, per_eventDB):
        """
        Erases an event from both lockdb and Event database
        This should also handle lockdb data as well.
        TopicIDs that are not in the given eventDB are silently ignored.
        (LockDB data will be erased if found)

        IN:
            topicID - topic ID / label
            per_eventDB - persistent database this topic is in
        """
        if topicID in per_eventDB:
            per_eventDB.pop(topicID)
        
        if topicID in Event.INIT_LOCKDB:
            Event.INIT_LOCKDB.pop(topicID)


    def mas_transferTopic(old_topicID, new_topicID, per_eventDB):
        """DEPREACTED
        NOTE: This can cause data corruption. DO NOT USE.

        Transfers a topic's data from the old topic ID to the new one int he
        given database as well as the lock database.

        NOTE: If the new topic ID already exists in the given databases,
        the data is OVERWRITTEN

        IN:
            old_topicID - old topic ID to transfer
            new_topicID - new topic ID to receieve
            per_eventDB - persistent databse this topic is in
        """
        if old_topicID in per_eventDB:
            
            
            
            old_data = list(per_eventDB.pop(old_topicID))
            old_data[0] = new_topicID
            per_eventDB[new_topicID] = tuple(old_data)
        
        if old_topicID in Event.INIT_LOCKDB:
            Event.INIT_LOCKDB[new_topicID] = Event.INIT_LOCKDB.pop(old_topicID)


    def mas_transferTopicSeen(old_topicID, new_topicID):
        """
        Tranfers persistent seen ever data. This is separate because of complex
        topic adjustments

        IN:
            old_topicID - old topic ID to tranfer
            new_topicID - new topic ID to receieve
        """
        if old_topicID in persistent._seen_ever:
            persistent._seen_ever.pop(old_topicID)
            persistent._seen_ever[new_topicID] = True


    def adjustTopicIDs(changedIDs,updating_persistent=persistent):
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        for oldTopic in changedIDs:
            if updating_persistent._seen_ever.pop(oldTopic,False):
                updating_persistent._seen_ever[changedIDs[oldTopic]] = True
        
        return updating_persistent



    def updateTopicIDs(version_number,updating_persistent=persistent):
        
        
        
        
        
        
        
        
        
        
        
        
        
        if version_number in updates.topics:
            changedIDs = updates.topics[version_number]
            
            
            if changedIDs is not None:
                adjustTopicIDs(changedIDs, updating_persistent)
        
        return updating_persistent


    def updateGameFrom(startVers):
        
        
        
        
        
        
        
        
        
        
        while startVers in updates.version_updates:
            
            updateTo = updates.version_updates[startVers]
            
            
            if renpy.has_label(updateTo) and not renpy.seen_label(updateTo):
                renpy.call_in_new_context(updateTo, updateTo)
            startVers = updates.version_updates[startVers]





init 10 python:


    if persistent.version_number is None:
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        persistent.version_number = config.version
        
        
        clearUpdateStructs()

    elif persistent.version_number != config.version:
        
        t_version = persistent.version_number
        if "-" in t_version:
            t_version = t_version[:t_version.index("-")]
        vvvv_version = "v"+"_".join(t_version.split("."))
        
        updateGameFrom(vvvv_version)
        
        
        persistent.version_number = config.version
        
        
        clearUpdateStructs()



    def _mas_resetVersionUpdates():
        """
        Resets all version update script's seen status
        """
        late_updates = [
            "v0_8_3",
            "v0_8_4",
            "v0_8_10"
        ]
        
        renpy.call_in_new_context("vv_updates_topics")
        ver_list = store.updates.version_updates.keys()
        
        if "-" in config.version:
            working_version = config.version[:config.version.index("-")]
        else:
            working_version = config.version
        
        ver_list.extend(["mas_lupd_" + x for x in late_updates])
        ver_list.append("v" + "_".join(
            working_version.split(".")
        ))
        
        for _version in ver_list:
            if _version in persistent._seen_ever:
                persistent._seen_ever.pop(_version)













label vgenericupdate(version="v0_2_2"):
label v0_6_1(version=version):
label v0_5_1(version=version):
label v0_3_3(version=version):
label v0_3_2(version=version):
label v0_3_1(version=version):
    python:

        updateTopicIDs(version)

    return




label v0_9_6(version="v0_9_6"):
    python:
        ev_label_list = [
            ("monika_whatwatching","mas_wrs_youtube"),
            ("monika_lookingat","mas_wrs_r34m"),
            ("monika_monikamoddev","mas_wrs_monikamoddev")
        ]


        for old_ev_label, new_ev_label in ev_label_list:
            ev = mas_getEV(new_ev_label)
            if old_ev_label in persistent._mas_windowreacts_database:
                old_ev = Event(
                    persistent._mas_windowreacts_database,
                    old_ev_label
                )
            else:
                old_ev = None
            
            if ev is not None and old_ev is not None:
                ev.shown_count += old_ev.shown_count
                
                if ev.last_seen is None or ev.last_seen <= old_ev.last_seen:
                    ev.last_seen = old_ev.last_seen
                
                mas_transferTopicSeen(old_ev_label, new_ev_label)
                
                
                mas_eraseTopic(old_ev_label, persistent.event_database)


        if not renpy.seen_label("greeting_tears"):
            mas_unlockEVL("greeting_tears", "GRE")


        family_ev = mas_getEV("monika_family")
        if family_ev is not None:
            family_ev.pool = True
    return


label v0_9_5(version="v0_9_5"):
    python:

        if persistent._mas_likes_rain:
            mas_unlockEVL("monika_rain_holdme", "EVE")


        why_ev = mas_getEV('monika_why')
        if why_ev is not None:
            why_ev.pool = False
            if not renpy.seen_label('monika_why') or not mas_anni.pastOneMonth():
                why_ev.random = True
    return


label v0_9_4(version="v0_9_4"):
    python:

        if persistent._mas_greeting_type != store.mas_greetings.TYPE_LONG_ABSENCE:
            
            persistent._mas_long_absence = False


        if mas_getEV('monika_ptod_tip001').unlocked:
            
            mas_hideEVL("monika_ptod_tip000", "EVE", lock=True)


        outfit_ev = mas_getEV("monika_outfit")
        if outfit_ev is not None and renpy.seen_label(outfit_ev.eventlabel):
            outfit_ev.unlocked = True

    return


label v0_9_2(version="v0_9_2"):
    python:


        mas_eraseTopic("monika_szs", persistent.event_database)


        if persistent._mas_pm_have_fam is False:
            mas_hideEVL("monika_familygathering", "EVE", derandom=True)







        sleigh_ev = mas_getEV("monika_sleigh")
        if "mas_d25_monika_sleigh" in persistent.event_database:
            old_sleigh_ev = Event(
                persistent.event_database,
                "mas_d25_monika_sleigh"
            )
        else:
            old_sleigh_ev = None
        if sleigh_ev is not None and old_sleigh_ev is not None:
            sleigh_ev.unlock_date = old_sleigh_ev.unlock_date
            sleigh_ev.shown_count = old_sleigh_ev.shown_count
            sleigh_ev.last_seen = old_sleigh_ev.last_seen
            mas_transferTopicSeen("mas_d25_monika_sleigh", "monika_sleigh")
            
            
            mas_eraseTopic("mas_d25_monika_sleigh", persistent.event_database)


        mas_lockEVL("mas_pf14_monika_lovey_dovey","EVE")


        def fix_tip(tip_ev, prev_tip_ev):
            
            tip_ev.random = False
            
            if renpy.seen_label(tip_ev.eventlabel):
                
                tip_ev.unlocked = True
                tip_ev.conditional = None
                tip_ev.pool = True
                tip_ev.action = None
                
                if tip_ev.shown_count <= 0:
                    tip_ev.shown_count = 1
                
                if tip_ev.unlock_date is None:
                    tip_ev.unlock_date = datetime.datetime.now()
                
                
                if prev_tip_ev is not None:
                    persistent._seen_ever[prev_tip_ev.eventlabel] = True
            
            else:
                
                tip_ev.unlocked = False
                tip_ev.shown_count = 0
                
                if prev_tip_ev is None:
                    
                    tip_ev.pool = True
                    tip_ev.conditional = None
                    tip_ev.action = None
                    tip_ev.unlock_date = datetime.datetime.now()
                
                else:
                    
                    tip_ev.conditional = (
                        "seen_event('" + prev_tip_ev.eventlabel + "')"
                    )
                    tip_ev.pool = False
                    tip_ev.action = EV_ACT_POOL
                    tip_ev.unlock_date = None


        wt_5 = mas_getEV("monika_writingtip5")
        wt_4 = mas_getEV("monika_writingtip4")
        wt_3 = mas_getEV("monika_writingtip3")
        wt_2 = mas_getEV("monika_writingtip2")
        wt_1 = mas_getEV("monika_writingtip1")
        if wt_5 is not None:
            fix_tip(wt_5, wt_4)

        if wt_4 is not None:
            fix_tip(wt_4, wt_3)

        if wt_3 is not None:
            fix_tip(wt_3, wt_2)

        if wt_2 is not None:
            fix_tip(wt_2, wt_1)

        if wt_1 is not None:
            fix_tip(wt_1, None)


    return


label v0_9_1(version="v0_9_1"):
    python:

        if (
                persistent._mas_pm_likes_spoops
                and not renpy.seen_label("greeting_ghost")
            ):
            mas_unlockEVL("greeting_ghost", "GRE")


        plush_ev = mas_getEV("monika_plushie")
        if plush_ev is not None:
            plush_ev.unlocked = False
            plush_ev.category = None
            plush_ev.prompt = "monika_plushie"

        if renpy.seen_label("monika_driving"):
            mas_unlockEVL("monika_vehicle","EVE")

    return


label v0_9_0(version="v0_9_0"):
    python:

        if persistent._mas_called_moni_a_bad_name:
            nickname_ev = mas_getEV("monika_affection_nickname")
            if nickname_ev is not None:
                nickname_ev.unlocked = True





        d25e_ev = mas_getEV("mas_d25_monika_christmas_eve")
        if d25e_ev is not None:
            d25e_ev.conditional = (
                "persistent._mas_d25_in_d25_mode "
            )
            d25e_ev.action = EV_ACT_QUEUE

        d25_hi_ev = mas_getEV("mas_d25_monika_holiday_intro")
        if d25_hi_ev is not None:
            d25_hi_ev.conditional = (
                "not persistent._mas_d25_intro_seen "
                "and not persistent._mas_d25_started_upset "
            )
            d25_hi_ev.action = EV_ACT_PUSH

        d25_ev = mas_getEV("mas_d25_monika_christmas")
        if d25_ev is not None:
            d25_ev.conditional = (
                "persistent._mas_d25_in_d25_mode "
                "and not persistent._mas_d25_spent_d25"
            )
            d25_ev.action = EV_ACT_PUSH

        d25p_nts = mas_getEV("mas_d25_postd25_notimespent")
        if d25p_nts is not None:
            d25p_nts.conditional = (
                "not persistent._mas_d25_spent_d25"
            )
            d25p_nts.action = EV_ACT_PUSH

        d25_hiu_ev = mas_getEV("mas_d25_monika_holiday_intro_upset")
        if d25_hiu_ev is not None:
            d25_hiu_ev.conditional = (
                "not persistent._mas_d25_intro_seen "
                "and persistent._mas_d25_started_upset "
            )
            d25_hiu_ev.action = EV_ACT_PUSH

        d25_stm_ev = mas_getEV("mas_d25_spent_time_monika")
        if d25_stm_ev is not None:
            d25_stm_ev.conditional = (
                "persistent._mas_d25_in_d25_mode "
            )
            d25_stm_ev.action = EV_ACT_QUEUE
            d25_stm_ev.start_date = datetime.datetime.combine(
                mas_d25,
                datetime.time(hour=20)
            )
            d25_stm_ev.end_date = datetime.datetime.combine(
                mas_d25p,
                datetime.time(hour=1)
            )
            d25_stm_ev.years = []
            Event._verifyAndSetDatesEV(d25_stm_ev)


        nye_yr_ev = mas_getEV("monika_nye_year_review")
        if nye_yr_ev is not None:
            nye_yr_ev.action = EV_ACT_PUSH

        nyd_ev = mas_getEV("mas_nye_monika_nyd")
        if nyd_ev is not None:
            nyd_ev.action = EV_ACT_QUEUE

        res_ev = mas_getEV("monika_resolutions")
        if res_ev is not None:
            res_ev.action = EV_ACT_QUEUE


        if (
                persistent._mas_player_bday is not None
                and not persistent._mas_player_confirmed_bday
            ):
            mas_bd_ev = mas_getEV("mas_birthdate")
            if mas_bd_ev is not None:
                mas_bd_ev.conditional = "True"
                mas_bd_ev.action = EV_ACT_QUEUE


        for gre_label, gre_ev in store.evhand.greeting_database.iteritems():
            
            gre_ev.random = False


        if renpy.seen_label("monika_rain"):
            mas_unlockEVL("monika_rain", "EVE")


        if not renpy.seen_label("greeting_ourreality"):
            mas_unlockEVL("greeting_ourreality", "GRE")


        if persistent._mas_acs_enable_quetzalplushie:
            mas_hideEVL("monika_pets", "EVE", derandom=True)


        d25_mis_ev = mas_getEV("mas_d25_monika_mistletoe")
        if d25_mis_ev is not None:
            
            mas_addDelayedAction(10)

    return


label v0_8_14(version="v0_8_14"):
    python:

        rain_ev = mas_getEV("monika_rain")
        if rain_ev is not None and not rain_ev.random:
            rain_ev.unlocked = True


        if store.mas_o31_event.spentO31():
            mas_weather_thunder.unlocked = True
            store.mas_weather.saveMWData()

    return


label v0_8_13(version="v0_8_13"):
    python:


        d25_sp_tm = mas_getEV("mas_d25_spent_time_monika")
        if d25_sp_tm is not None:
            if (
                    d25_sp_tm.start_date.hour != 20
                    or d25_sp_tm.end_date.hour != 1
                ):
                d25_sp_tm.start_date = datetime.datetime.combine(
                    mas_d25,
                    datetime.time(hour=20)
                )
                
                d25_sp_tim.end_date = datetime.datetime.combine(
                    mas_d25p,
                    datetime.time(hour=1)
                )
                
                Event._verifyAndSetDatesEV(d25_sp_tm)

        d25_ce = mas_getEV("mas_d25_monika_christmas_eve")
        if d25_ce is not None:
            if d25_ce.start_date.hour != 20:
                d25_ce.start_date = datetime.datetime.combine(
                    mas_d25e,
                    datetime.time(hour=20)
                )
                
                d25_ce.end_date = mas_d25
                
                Event._verifyAndSetDatesEV(d25_ce)

        nye_re = mas_getEV("monika_nye_year_review")
        if nye_re is not None:
            if (
                    nye_re.start_date.hour != 19
                    or nye_re.end_date.hour != 23
                ):
                nye_re.start_date = datetime.datetime.combine(
                    mas_nye,
                    datetime.time(hour=19)
                )
                
                nye_re.end_date = datetime.datetime.combine(
                    mas_nye,
                    datetime.time(hour=23)
                )
                
                Event._verifyAndSetDatesEV(nye_re)


        bday_sp = mas_getEV("mas_bday_spent_time_with")
        if bday_sp is not None:
            if (
                    bday_sp.start_date.hour != 22
                    or bday_sp.end_date.hour != 23
                ):
                bday_sp.start_date = datetime.datetime.combine(
                    mas_monika_birthday,
                    datetime.time(hour=22)
                )
                
                bday_sp.end_date = datetime.datetime.combine(
                    mas_monika_birthday,
                    datetime.time(hour=23, minute=59)
                )
                
                Event._verifyAndSetDatesEV(bday_sp)

    return


label v0_8_11(version="v0_8_11"):
    python:
        import store.mas_compliments as mas_comp
        import store.evhand as evhand


        thanks_ev = mas_comp.compliment_database.get(
            "mas_compliment_thanks",
            None
        )
        if thanks_ev:
            
            thanks_ev.conditional = None
            thanks_ev.action = None
            
            
            if not renpy.seen_label(thanks_ev.eventlabel):
                thanks_ev.unlocked = True


        if not persistent._mas_called_moni_a_bad_name:
            mas_unlockEventLabel("monika_affection_nickname")

        if (
                not persistent._mas_pm_taken_monika_out
                and len(persistent._mas_dockstat_checkin_log) > 0
            ):
            persistent._mas_pm_taken_monika_out = True

    return


label v0_8_10(version="v0_8_10"):
    python:
        import store.evhand as evhand
        import store.mas_history as mas_history


        if persistent.sessions is not None:
            first_sesh = persistent.sessions.get("first_session", None)
            if first_sesh:
                store.mas_anni.reset_annis(first_sesh)
                store.mas_anni.unlock_past_annis()


        if (
                persistent._mas_bday_sbd_aff_given is not None
                and persistent._mas_bday_sbd_aff_given > 0
            ):
            persistent._mas_history_archives[2018][
                "922.actions.surprise.aff_given"
            ] = persistent._mas_bday_sbd_aff_given


        unlockEventLabel(
            "i_greeting_monikaroom",
            store.evhand.greeting_database
        )
        if not persistent._mas_hair_changed:
            unlockEventLabel(
                "greeting_hairdown",
                store.evhand.greeting_database
            )


        changename_ev = evhand.event_database.get("monika_changename", None)
        if changename_ev and renpy.seen_label("preferredname"):
            changename_ev.unlocked = True
            changename_ev.pool = True
            persistent._seen_ever["monika_changename"] = True


        family_ev = evhand.event_database.get("monika_family", None)
        if family_ev:
            family_ev.random = False


        persistent._mas_zz_lupd_ex_v.append(version)

    return


label v0_8_9(version="v0_8_9"):
    python:
        import store.evhand as evhand


        mas_eraseTopic("monika_weddingring", persistent.event_database)



        horror_ev = evhand.event_database.get("monika_horror", None)
        if horror_ev:
            horror_ev.conditional = (
                "datetime.date(2018, 10, 26) <= datetime.date.today() "
                "<= datetime.date(2018, 10, 30)"
            )
            horror_ev.action = EV_ACT_QUEUE

    return



label v0_8_6(version="v0_8_6"):
    python:
        import store.evhand as evhand
        import datetime


        genderredo_ev = evhand.event_database.get("gender_redo", None)
        if genderredo_ev and renpy.seen_label("gender"):
            genderredo_ev.unlocked = True
            genderredo_ev.pool = True
            
            
            persistent._seen_ever["gender_redo"] = True


        new_char_ev = evhand.event_database.get("mas_new_character_file", None)
        if new_char_ev and not renpy.seen_label("mas_new_character_file"):
            new_char_ev.conditional = "True"
            new_char_ev.action = EV_ACT_PUSH

    return


label v0_8_4(version="v0_8_4"):
    python:

        import store.evhand as evhand
        import store.mas_stories as mas_stories


        updateTopicIDs(version)









        best_evlabel = "monika_bestgirl"
        best_comlabel = "mas_compliment_bestgirl"
        best_ev = Event(persistent.event_database, eventlabel=best_evlabel)
        best_compliment = mas_compliments.compliment_database.get(best_comlabel, None)
        best_lockdata = None


        if best_evlabel in Event.INIT_LOCKDB:
            best_lockdata = Event.INIT_LOCKDB.pop(best_evlabel)

        if best_compliment:
            
            best_compliment.shown_count = best_ev.shown_count
            best_compliment.last_seen = best_ev.last_seen
            
            if best_lockdata:
                
                Event.INIT_LOCKDB[best_comlabel] = best_lockdata


        if best_evlabel in persistent.event_database:
            persistent.event_database.pop(best_evlabel)


        persistent._mas_zz_lupd_ex_v.append(version)


    return


label v0_8_3(version="v0_8_3"):
    python:
        import datetime
        import store.evhand as evhand


        ex_ev = evhand.event_database.get("monika_explain", None)
        if ex_ev is not None:
            ex_ev.random = False
            ex_ev.pool = True


        kiz_ev = evhand.event_database.get("monika_kizuna", None)
        if kiz_ev is not None and not renpy.seen_label(kiz_ev.eventlabel):
            kiz_ev.action = EV_ACT_POOL
            kiz_ev.unlocked = False
            kiz_ev.pool = False
            kiz_ev.conditional = "seen_event('greeting_hai_domo')"


        curr_level = get_level()
        if curr_level > 25:
            persistent._mas_pool_unlocks = int(curr_level / 2)


        derandomable = [
            "monika_natsuki_letter",
            "monika_prom",
            "monika_beach",
            "monika_asks_family",
            "monika_smoking",
            "monika_otaku",
            "monika_jazz",
            "monika_orchestra",
            "monika_meditation",
            "monika_sports",
            "monika_weddingring",
            "monika_icecream",
            "monika_japanese",
            "monika_haterReaction",
            "monika_cities",
            "monika_images",
            "monika_rain",
            "monika_selfesteem",
            "monika_yellowwp",
            "monika_familygathering"
        ]
        for topic in derandomable:
            ev = evhand.event_database.get(topic, None)
            if renpy.seen_label(topic) and ev:
                ev.unlocked = True
                ev.unlock_date = datetime.datetime.now()



        persistent._mas_zz_lupd_ex_v.append(version)

    return


label v0_8_2(version="v0_8_2"):
    python:
        import store.mas_anni as mas_anni


        mas_anni.reset_annis(persistent.sessions["first_session"])

    return


label v0_8_1(version="v0_8_1"):
    python:
        import store.evhand as evhand
        import store.mas_stories as mas_stories



        m_ff = evhand.event_database.get("monika_fastfood", None)
        if m_ff:
            hideEvent(m_ff, derandom=True)
            m_ff.pool = True


        updateTopicIDs(version)




        writ_5 = evhand.event_database.get("monika_writingtip5", None)
        if writ_5 and not renpy.seen_label(writ_5.eventlabel):
            writ_5.pool = False
            writ_5.conditional = "seen_event('monika_writingtip4')"
            writ_5.action = EV_ACT_POOL


        writ_4 = evhand.event_database.get("monika_writingtip4", None)
        if writ_4 and not renpy.seen_label(writ_4.eventlabel):
            writ_4.pool = False
            writ_4.conditional = "seen_event('monika_writingtip3')"
            writ_4.action = EV_ACT_POOL



        writ_3_old = persistent.event_database.get("monika_write", None)

        if writ_3_old is not None:
            persistent.event_database.pop("monika_write")

        writ_3 = evhand.event_database.get("monika_writingtip3", None)

        if writ_3_old is not None and writ_3 is not None:
            writ_3.unlocked = writ_3_old[Event.T_EVENT_NAMES["unlocked"]]
            writ_3.unlock_date = writ_3_old[Event.T_EVENT_NAMES["unlock_date"]]

        if writ_3 and not renpy.seen_label(writ_3.eventlabel):
            writ_3.pool = False
            writ_3.conditional = "seen_event('monika_writingtip2')"
            writ_3.action = EV_ACT_POOL


        zero_t = "monika_writingtip"
        old_t = "monika_writingtip1"
        new_t = "monika_writingtip2"
        if zero_t in persistent.event_database:
            
            
            
            mas_transferTopicSeen(old_t, new_t)
            old_t_ev = mas_getEV(old_t)
            new_t_ev = mas_getEV(new_t)
            
            if old_t_ev is not None and new_t_ev is not None:
                new_t_ev.unlocked = old_t_ev.unlocked
                new_t_ev.unlock_date = old_t_ev.unlock_date
            
            if new_t_ev and not renpy.seen_label(new_t):
                new_t_ev.conditional = "seen_event('monika_writingtip1')"
                new_t_ev.pool = False
                new_t_ev.action = EV_ACT_POOL
            
            
            zero_t_d = persistent.event_database.pop(zero_t)
            mas_transferTopicSeen(zero_t, old_t)
            if old_t_ev is not None:
                old_t_ev.unlocked = zero_t_d[Event.T_EVENT_NAMES["unlocked"]]
                old_t_ev.unlock_date = zero_t_d[
                    Event.T_EVENT_NAMES["unlock_date"]
                ]


        persistent._mas_enable_random_repeats = None
        persistent._mas_monika_repeated_herself = None


        annis = (
            "anni_1week",
            "anni_1month",
            "anni_3month",
            "anni_6month"
        ) 
        for anni in annis:
            anni_ev = evhand.event_database.get(anni, None)
            
            if anni_ev and isPast(anni_ev):
                
                persistent._seen_ever[anni] = True
                anni_ev.unlocked = True


        music_ev = Event(persistent.event_database, eventlabel="monika_music2")
        music_ev.unlocked = False
        music_ev.random = False









        ravel_evlabel = "monika_ravel"
        ravel_stlabel = "mas_story_ravel"
        ravel_ev = Event(persistent.event_database, eventlabel=ravel_evlabel)
        ravel_story = mas_stories.story_database.get(ravel_stlabel, None)
        ravel_lockdata = None


        if ravel_evlabel in Event.INIT_LOCKDB:
            ravel_lockdata = Event.INIT_LOCKDB.pop(ravel_evlabel)

        if ravel_story:
            
            ravel_story.shown_count = ravel_ev.shown_count
            ravel_story.last_seen = ravel_ev.last_seen
            
            if ravel_lockdata:
                
                Event.INIT_LOCKDB[ravel_stlabel] = ravel_lockdata


        if ravel_evlabel in persistent.event_database:
            persistent.event_database.pop(ravel_evlabel)


    return


label v0_8_0(version="v0_8_0"):
    python:
        import store.evhand as evhand


        if (
                renpy.seen_label("monika_changename")
                or renpy.seen_label("preferredname")
            ):
            evhand.event_database["monika_changename"].unlocked = True

        annis = (
            "anni_1week",
            "anni_1month",
            "anni_3month",
            "anni_6month"
        ) 
        for anni in annis:
            if isPast(evhand.event_database[anni]):
                persistent._seen_ever[anni] = True

        persistent = updateTopicIDs(version)


        for k in updates.topics["v0_8_0"]:
            mas_eraseTopic(k, persistent.event_database)



        for k in updates.topics["v0_7_4"]:
            mas_eraseTopic(k, persistent.event_database)


        m_ff = evhand.event_database.get("monika_fastfood", None)
        if m_ff:
            hideEvent(m_ff, derandom=True)
            m_ff.pool = True

    return



label v0_7_4(version="v0_7_4"):
    python:



        import os
        try: os.remove(config.basedir + "/game/valentines.rpyc")
        except: pass


        try: os.remove(config.basedir + "/game/white-day.rpyc")
        except: pass



        import store.evhand as evhand
        import store.mas_utils as mas_utils
        import datetime
        fullday = datetime.timedelta(days=1)
        threeday = datetime.timedelta(days=3)
        week = datetime.timedelta(days=7)
        month = datetime.timedelta(days=30)
        year = datetime.timedelta(days=365)
        def _month_adjuster(key, months, span):
            new_anni_date = mas_utils.add_months(
                mas_utils.sod(persistent.sessions["first_session"]),
                months
            )
            evhand.event_database[key].start_date = new_anni_date
            evhand.event_database[key].end_date = new_anni_date + span


        _month_adjuster("anni_1month", 1, fullday)
        _month_adjuster("anni_3month", 3, fullday)
        _month_adjuster("anni_6month", 6, fullday)
        _month_adjuster("anni_1", 12, fullday)
        _month_adjuster("anni_2", 24, fullday)
        _month_adjuster("anni_3", 36, threeday)
        _month_adjuster("anni_4", 48, week)
        _month_adjuster("anni_5", 60, week)
        _month_adjuster("anni_10", 120, month)
        _month_adjuster("anni_20", 240, year)
        evhand.event_database["anni_100"].start_date = mas_utils.add_months(
            mas_utils.sod(persistent.sessions["first_session"]),
            1200
        )



        for k in evhand.farewell_database:
            
            evhand.farewell_database[k].unlocked = True

        updateTopicIDs(version)



        for k in updates.topics["v0_7_4"]:
            mas_eraseTopic(k, persistent.event_database)

    return


label v0_7_2(version="v0_7_2"):
    python:
        import store.evhand as evhand


        for k in evhand.event_database:
            event = evhand.event_database[k]
            if (renpy.seen_label(event.eventlabel)
                and (event.random or event.action == EV_ACT_RANDOM)):
                event.unlocked = True
                event.conditional = None




    return


label v0_7_1(version="v0_7_1"):
    python:

        if persistent.you is not None:
            persistent._mas_you_chr = persistent.you

        if persistent.pnml_data is not None:
            persistent._mas_pnml_data = persistent.pnml_data

        if renpy.seen_label("zz_play_piano"):
            removeTopicID("zz_play_piano")
            persistent._seen_ever["mas_piano_start"] = True

    return


label v0_7_0(version="v0_7_0"):
    python:

        import os
        try: os.remove(config.basedir + "/game/christmas.rpyc")
        except: pass


        updateTopicIDs(version)

        temp_event_list = list(persistent.event_list)

        import store.evhand as evhand
        for k in evhand.event_database:
            event = evhand.event_database[k]
            if (renpy.seen_label(event.eventlabel)
                and (event.pool
                    or event.random
                    or event.action == EV_ACT_POOL
                    or event.action == EV_ACT_RANDOM
                )):
                event.unlocked = True
                event.conditional = None
                
                
                grant_xp(xp.NEW_EVENT)


        persistent.event_list = temp_event_list


        if seen_event('game_chess'):
            persistent.game_unlocks['chess']=True


        if seen_event('preferredname'):
            evhand.event_database["monika_changename"].unlocked = True

    return


label v0_4_0(version="v0_4_0"):
    python:

        persistent.monika_random_topics = None




    return


label v0_3_0(version="v0_3_0"):
    python:

        removeTopicID("monika_piano")
        removeTopicID("monika_college")


        updateTopicIDs(version)
    return



























































label mas_lupd_v0_8_10:
    python:
        import store.mas_selspr as mas_selspr


        if persistent._mas_hair_changed:
            mas_selspr.unlock_hair(mas_hair_down)
            unlockEventLabel("monika_hair_select")


        if persistent._mas_o31_seen_costumes is not None:
            if persistent._mas_o31_seen_costumes.get("marisa", False):
                mas_selspr.unlock_clothes(mas_clothes_marisa)
            if persistent._mas_o31_seen_costumes.get("rin", False):
                mas_selspr.unlock_clothes(mas_clothes_rin)


        mas_selspr.save_selectables()

    return

label mas_lupd_v0_8_4:
    python:

        import store.evhand as evhand
        import datetime

        aff_to_grant = 0

        if renpy.seen_label('monika_christmas'):
            aff_to_grant += 10

        if renpy.seen_label('monika_newyear1'):
            aff_to_grant += 5

        if renpy.seen_label('monika_valentines_chocolates'):
            aff_to_grant += 15

        if renpy.seen_label('monika_found'):
            aff_to_grant += 10

        moni_love = evhand.event_database.get("monika_love", None)

        if moni_love is not None:
            aff_to_grant += (moni_love.shown_count * 7) / 100

        aff_to_grant += (datetime.datetime.now() - persistent.sessions["first_session"]).days / 3

        if aff_to_grant > 200:
            aff_to_grant = 200

        _mas_AffLoad()
        store.mas_gainAffection(aff_to_grant,bypass=True)
        _mas_AffSave()

    return

label mas_lupd_v0_8_3:
    python:

        if persistent.sessions:
            first_sesh = persistent.sessions.get("first_session", None)
            if first_sesh:
                store.mas_anni.reset_annis(first_sesh)

    return


init 999 python:
    for _m1_updates__temp_version in persistent._mas_zz_lupd_ex_v:
        _m1_updates__lupd_v = "mas_lupd_" + _m1_updates__temp_version
        if renpy.has_label(_m1_updates__lupd_v) and not renpy.seen_label(_m1_updates__lupd_v):
            renpy.call_in_new_context(_m1_updates__lupd_v)

    persistent._mas_zz_lupd_ex_v = list()
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
