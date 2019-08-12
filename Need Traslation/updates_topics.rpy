



define updates.version_updates = None




define updates.topics = None

init -1 python in mas_db_merging:
    import store

    def merge_db(source, dest):
        """
        Merges the given source database into the given destination db

        IN:
            source - source database to merge from
            dest - destination database to merge into
        """
        dest.update(source)


    def merge_post0810():
        """
        Runs a specific set of merges, particularly for the merge that
        happend after version 0.8.10.
        """
        
        
        if store.persistent._mas_compliments_database is not None:
            merge_db(
                store.persistent._mas_compliments_database,
                store.persistent.event_database
            )



init -1 python:
    def clearUpdateStructs():
        
        
        
        updates.topics.clear()
        updates.topics = None
        updates.version_updates.clear()
        updates.version_updates = None





init 9 python:

    if persistent.version_number != config.version:
        renpy.call_in_new_context("vv_updates_topics")



label vv_updates_topics:
    python:


        updates.version_updates = {}
        updates.topics = {}



        vv0_9_6 = "v0_9_6"
        vv0_9_5 = "v0_9_5"
        vv0_9_4 = "v0_9_4"
        vv0_9_3 = "v0_9_3"
        vv0_9_2 = "v0_9_2"
        vv0_9_1 = "v0_9_1"
        vv0_9_0 = "v0_9_0"
        vv0_8_14 = "v0_8_14"
        vv0_8_13 = "v0_8_13"
        vv0_8_12 = "v0_8_12"
        vv0_8_11 = "v0_8_11"
        vv0_8_10 = "v0_8_10"
        vv0_8_9 = "v0_8_9"
        vv0_8_8 = "v0_8_8"
        vv0_8_7 = "v0_8_7"
        vv0_8_6 = "v0_8_6"
        vv0_8_5 = "v0_8_5"
        vv0_8_4 = "v0_8_4"
        vv0_8_3 = "v0_8_3"
        vv0_8_2 = "v0_8_2"
        vv0_8_1 = "v0_8_1"
        vv0_8_0 = "v0_8_0"
        vv0_7_4 = "v0_7_4"
        vv0_7_3 = "v0_7_3"
        vv0_7_2 = "v0_7_2"
        vv0_7_1 = "v0_7_1"
        vv0_7_0 = "v0_7_0"
        vv0_6_3 = "v0_6_3"
        vv0_6_2 = "v0_6_1"
        vv0_6_1 = "v0_6_1"
        vv0_6_0 = "v0_6_0"
        vv0_5_1 = "v0_5_1"
        vv0_5_0 = "v0_5_0"
        vv0_4_0 = "v0_4_0"
        vv0_3_3 = "v0_3_3"
        vv0_3_2 = "v0_3_2"
        vv0_3_1 = "v0_3_1"
        vv0_3_0 = "v0_3_0"
        vv0_2_2 = "v0_2_2"





        updates.version_updates[vv0_9_4] = vv0_9_5
        updates.version_updates[vv0_9_3] = vv0_9_4
        updates.version_updates[vv0_9_2] = vv0_9_4
        updates.version_updates[vv0_9_1] = vv0_9_2
        updates.version_updates[vv0_9_0] = vv0_9_1
        updates.version_updates[vv0_8_14] = vv0_9_0
        updates.version_updates[vv0_8_13] = vv0_8_14
        updates.version_updates[vv0_8_12] = vv0_8_13
        updates.version_updates[vv0_8_11] = vv0_8_13
        updates.version_updates[vv0_8_10] = vv0_8_11
        updates.version_updates[vv0_8_9] = vv0_8_10
        updates.version_updates[vv0_8_8] = vv0_8_9
        updates.version_updates[vv0_8_7] = vv0_8_9
        updates.version_updates[vv0_8_6] = vv0_8_9
        updates.version_updates[vv0_8_5] = vv0_8_6
        updates.version_updates[vv0_8_4] = vv0_8_6
        updates.version_updates[vv0_8_3] = vv0_8_4
        updates.version_updates[vv0_8_2] = vv0_8_3
        updates.version_updates[vv0_8_1] = vv0_8_2
        updates.version_updates[vv0_8_0] = vv0_8_1
        updates.version_updates[vv0_7_4] = vv0_8_0
        updates.version_updates[vv0_7_3] = vv0_7_4
        updates.version_updates[vv0_7_2] = vv0_7_4
        updates.version_updates[vv0_7_1] = vv0_7_2
        updates.version_updates[vv0_7_0] = vv0_7_1
        updates.version_updates[vv0_6_3] = vv0_7_0
        updates.version_updates[vv0_6_2] = vv0_7_0
        updates.version_updates[vv0_6_1] = vv0_7_0
        updates.version_updates[vv0_6_0] = vv0_6_1
        updates.version_updates[vv0_5_1] = vv0_6_1
        updates.version_updates[vv0_5_0] = vv0_5_1
        updates.version_updates[vv0_4_0] = vv0_5_1
        updates.version_updates[vv0_3_3] = vv0_5_1
        updates.version_updates[vv0_3_2] = vv0_3_3
        updates.version_updates[vv0_3_1] = vv0_3_2
        updates.version_updates[vv0_3_0] = vv0_3_1
        updates.version_updates[vv0_2_2] = vv0_3_0
















        updates.topics[vv0_8_11] = {
            "monika_snowman": None,
            "monika_relax": None,
            "monika_hypothermia": None,
            "monika_whatiwant": None
        }


        updates.topics[vv0_8_4] = {
            "monika_bestgirl": "mas_compliment_bestgirl"
        }


        updates.topics[vv0_8_1] = {
            "monika_write": "monika_writingtip3",
            "mas_random_ask": None,
            "monika_ravel": "mas_story_ravel"
        }


        updates.topics[vv0_8_0] = {
            "monika_love2": None
        }


        updates.topics[vv0_7_4] = {
            "monika_playerhappy": None,
            "monika_bad_day": None
        }


        changedIDs = {
            "monika_deleted": None,
            "monika_whatever": None,
            "monika_games": None,
            "monika_chess": None,
            "monika_pong": None,
            "monika_vulgarity": None,
            "monika_goodbye": None,
            "monika_night": None
        }
        updates.topics[vv0_7_0] = changedIDs 


        changedIDs = {
            "monika_piano": None
        }
        updates.topics[vv0_6_1] = changedIDs


        changedIDs = dict()
        changedIDs["monika_music"] = None
        changedIDs["monika_keitai"] = None
        changedIDs["monika_subahibi"] = None
        changedIDs["monika_reddit"] = None
        changedIDs["monika_shill"] = None
        changedIDs["monika_dracula"] = None
        changedIDs["monika_undertale"] = None
        changedIDs["monika_recursion"] = None
        changedIDs["monika_lain"] = None
        changedIDs["monika_kyon"] = None
        changedIDs["monika_water"] = None
        changedIDs["monika_computer"] = None
        updates.topics[vv0_5_1] = changedIDs


        changedIDs = dict()
        changedIDs["monika_monika"] = None
        updates.topics[vv0_3_2] = changedIDs


        changedIDs = dict()
        changedIDs["monika_ghosts"] = "monika_whispers"
        updates.topics[vv0_3_1] = changedIDs




        changedIDs = None
        changedIDs = dict()
        changedIDs["ch30_1"] = "monika_god"
        changedIDs["ch30_2"] = "monika_death"
        changedIDs["ch30_3"] = "monika_bad_day"
        changedIDs["ch30_4"] = "monika_sleep"
        changedIDs["ch30_5"] = "monika_sayori"
        changedIDs["ch30_6"] = "monika_japan"
        changedIDs["ch30_7"] = "monika_high_school"
        changedIDs["ch30_8"] = "monika_nihilism"
        changedIDs["ch30_9"] = "monika_piano"
        changedIDs["ch30_10"] = "monika_twitter"
        changedIDs["ch30_11"] = "monika_portraitof"
        changedIDs["ch30_12"] = "monika_veggies"
        changedIDs["ch30_13"] = "monika_saved"
        changedIDs["ch30_14"] = "monika_secrets"
        changedIDs["ch30_15"] = "monika_color"
        changedIDs["ch30_16"] = "monika_music"
        changedIDs["ch30_17"] = "monika_listener"
        changedIDs["ch30_18"] = "monika_spicy"
        changedIDs["ch30_19"] = "monika_why"
        changedIDs["ch30_20"] = "monika_okayeveryone"
        changedIDs["ch30_21"] = "monika_ghosts"
        changedIDs["ch30_22"] = "monika_archetype"
        changedIDs["ch30_23"] = "monika_tea"
        changedIDs["ch30_24"] = "monika_favoritegame"
        changedIDs["ch30_25"] = "monika_smash"

        changedIDs["ch30_27"] = "monika_lastpoem"
        changedIDs["ch30_28"] = "monika_anxious"
        changedIDs["ch30_29"] = "monika_friends"
        changedIDs["ch30_30"] = "monika_college"
        changedIDs["ch30_31"] = "monika_middleschool"
        changedIDs["ch30_32"] = "monika_outfit"
        changedIDs["ch30_33"] = "monika_horror"
        changedIDs["ch30_34"] = "monika_rap"
        changedIDs["ch30_35"] = "monika_wine"
        changedIDs["ch30_36"] = "monika_date"
        changedIDs["ch30_37"] = "monika_kiss"
        changedIDs["ch30_38"] = "monika_yuri"
        changedIDs["ch30_39"] = "monika_writingtip"
        changedIDs["ch30_40"] = "monika_habits"
        changedIDs["ch30_41"] = "monika_creative"
        changedIDs["ch30_42"] = "monika_deleted"
        changedIDs["ch30_43"] = "monika_keitai"
        changedIDs["ch30_44"] = "monika_simulated"
        changedIDs["ch30_45"] = "monika_rain"
        changedIDs["ch30_46"] = "monika_closeness"
        changedIDs["ch30_47"] = "monika_confidence"
        changedIDs["ch30_48"] = "monika_carryme"
        changedIDs["ch30_49"] = "monika_debate"
        changedIDs["ch30_50"] = "monika_internet"
        changedIDs["ch30_51"] = "monika_lazy"
        changedIDs["ch30_52"] = "monika_mentalillness"
        changedIDs["ch30_53"] = "monika_read"
        changedIDs["ch30_54"] = "monika_festival"
        changedIDs["ch30_55"] = "monika_tsundere"
        changedIDs["ch30_56"] = "monika_introduce"
        changedIDs["ch30_57"] = "monika_cold"
        changedIDs["ch30_58"] = "monika_housewife"
        changedIDs["ch30_59"] = "monika_route"
        changedIDs["monika_literatureclub"] = "monika_ddlc"
        changedIDs["monika_religion"] = None

















































        updates.topics[vv0_3_0] = changedIDs


        changedIDs = None
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
