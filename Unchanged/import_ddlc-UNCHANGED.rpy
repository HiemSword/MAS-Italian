


init python:
    def dumpPersistentToFile(dumped_persistent,dumppath):
        
        
        
        
        
        
        
        dumped_persistent=vars(dumped_persistent)
        
        fo = open(dumppath, "w")
        
        for key in sorted(dumped_persistent.iterkeys()):
            fo.write(str(key) + ' - ' + str(type(dumped_persistent[key])) + ' >>> '+ str(dumped_persistent[key]) + '\n\n')
        
        fo.close()

label import_ddlc_persistent_in_settings:

    $ mas_RaiseShield_core()

    call import_ddlc_persistent from _call_import_ddlc_persistent_1

    if store.mas_globals.dlg_workflow:


        $ enable_esc()
        $ mas_MUMUDropShield()
    else:


        $ mas_DropShield_core()

    return

label import_ddlc_persistent:
    python:
        from renpy.loadsave import dump, loads

        import glob


        if renpy.macintosh:
            rv = "~/Library/RenPy/"
            check_path = os.path.expanduser(rv)

        elif renpy.windows:
            if 'APPDATA' in os.environ:
                check_path =  os.environ['APPDATA'] + "/RenPy/"
            else:
                rv = "~/RenPy/"
                check_path = os.path.expanduser(rv)

        else:
            rv = "~/.renpy/"
            check_path = os.path.expanduser(rv)

        save_path=glob.glob(check_path + 'DDLC/persistent')
        if not save_path:
            save_path=glob.glob(check_path + 'DDLC-*/persistent')

    $ quick_menu = False
    scene black
    with Dissolve(1.0)

    if save_path:
        $ save_path=save_path[0]
        "Save data for Doki Doki Literature Club was found at [save_path]."
        menu:
            "Would you like to import Doki Doki Literature Club save data into [config.name]?\n(DDLC will not be affected)"
            "Yes, import DDLC save data.":
                pause 0.3
                pass
            "No, do not import.":
                pause 0.3
                return
    else:

        $ quick_menu = False
        "Save data from Doki Doki Literature Club could not be found."
        menu:
            "Save data will not be imported at this time."
            "Okay":
                pause 0.3
                pass
        return


    python:
        from renpy.loadsave import dump, loads


        f=file(save_path,"rb")
        s=f.read().decode("zlib")
        f.close()

        old_persistent=loads(s)


        renpy.call_in_new_context("vv_updates_topics") 
        old_persistent = updateTopicIDs("v030",old_persistent)
        old_persistent = updateTopicIDs("v031",old_persistent)
        old_persistent = updateTopicIDs("v032",old_persistent)
        old_persistent = updateTopicIDs("v033",old_persistent)
        clearUpdateStructs()




    default merge_previous = False
    if persistent.first_run:
        label import_ddlc_persistent.save_merge_or_replace:
        menu:
            "Previous Monika After Story save data has also been found.\nReplace or merge with DDLC save data?"
            "Merge save data.":
                $ merge_previous=True
            "Delete After Story data.":

                menu:
                    "Monika After Story data will be deleted. This cannot be undone. Are you sure?"
                    "Yes":
                        m "You really haven't changed. Have you?"
                    "No":
                        jump import_ddlc_persistent.save_merge_or_replace
            "Cancel.":
                "DDLC data can be imported later in the Settings menu."
                return


    python:



















































        if merge_previous is True and old_persistent._chosen is not None and persistent._chosen is not None:
            persistent._chosen.update(old_persistent._chosen)
        elif old_persistent._chosen is not None:
            persistent._chosen=old_persistent._chosen




        if merge_previous is True and old_persistent._seen_audio is not None and persistent._seen_audio is not None:
            persistent._seen_audio.update(old_persistent._seen_audio)
        elif old_persistent._seen_audio is not None:
            persistent._seen_audio=old_persistent._seen_audio





        if merge_previous is True and old_persistent._seen_ever is not None and persistent._seen_ever is not None:
            persistent._seen_ever.update(old_persistent._seen_ever)
        elif old_persistent._seen_ever is not None:
            persistent._seen_ever=old_persistent._seen_ever




        if merge_previous is True and old_persistent._chosen is not None and persistent._chosen is not None:
            persistent._seen_images.update(old_persistent._seen_images)
        elif old_persistent._chosen is not None:
            persistent._seen_images=old_persistent._seen_images




        if merge_previous is True and old_persistent._seen_translates is not None and persistent._seen_translates is not None:
            persistent._seen_translates.update(old_persistent._seen_translates)
        elif old_persistent._seen_translates is not None:
            persistent._seen_translates=old_persistent._seen_translates




        if merge_previous is True and old_persistent.clear is not None and persistent.clear is not None:
            for flag in persistent.clear:
                persistent.clear[flag] = persistent.clear[flag] or old_persistent.clear[flag]
        elif old_persistent.clear is not None:
            persistent.clear=old_persistent.clear



        if merge_previous is True and old_persistent.clearall is not None and persistent.clearall is not None:
            persistent.clearall = persistent.clearall or old_persistent.clearall
        elif old_persistent.clearall is not None:
            persistent.clearall=old_persistent.clearall







        if merge_previous is True and old_persistent.ghost_menu is not None and persistent.ghost_menu is not None:
            persistent.ghost_menu=persistent.ghost_menu or old_persistent.ghost_menu
            persistent.seen_ghost_menu=persistent.seen_ghost_menu or old_persistent.seen_ghost_menu
        elif old_persistent.ghost_menu is not None:
            persistent.ghost_menu=old_persistent.ghost_menu
            persistent.seen_ghost_menu = old_persistent.seen_ghost_menu



        if merge_previous is True and old_persistent.monika_kill is not None and persistent.monika_kill is not None:
            persistent.monika_kill = persistent.monika_kill or old_persistent.monika_kill
        elif old_persistent.monika_kill is not None:
            persistent.monika_kill=old_persistent.monika_kill



        if merge_previous is True and old_persistent.monika_reload is not None and persistent.monika_reload is not None:
            persistent.monika_reload = persistent.monika_reload + old_persistent.monika_reload
        elif old_persistent.monika_reload is not None:
            persistent.monika_reload=old_persistent.monika_reload








        if merge_previous is True and persistent.playername is not "" and old_persistent.playername is not None and persistent.playername is not None:
            if persistent.playername == old_persistent.playername:
                persistent.playername
            else:
                renpy.call_in_new_context('merge_unmatched_names')
        elif old_persistent.playername is not None:
            persistent.playername=old_persistent.playername
        player=persistent.playername




        if merge_previous is True and old_persistent.playthrough is not None and persistent.playthrough is not None:
            if persistent.playthrough >= old_persistent.playthrough:
                persistent.playthrough
            else:
                persistent.playthrough = old_persistent.playthrough
        elif old_persistent.playthrough is not None:
            persistent.playthrough = old_persistent.playthrough



        if merge_previous is True and old_persistent.seen_eyes is not None and persistent.seen_eyes is not None:
            persistent.seen_eyes = persistent.seen_eyes or old_persistent.seen_eyes
        elif old_persistent.seen_eyes is not None:
            persistent.seen_eyes=old_persistent.seen_eyes



        if merge_previous is True and old_persistent.seen_sticker is not None and persistent.seen_sticker is not None:
            persistent.seen_sticker = persistent.seen_sticker or old_persistent.seen_sticker
        elif old_persistent.seen_sticker is not None:
            persistent.seen_sticker=old_persistent.seen_sticker



        if merge_previous is True and old_persistent.special_poems is not None and persistent.special_poems is not None:
            persistent.special_poems = persistent.special_poems + old_persistent.special_poems
        elif old_persistent.special_poems is not None:
            persistent.special_poems=old_persistent.special_poems









        if merge_previous is True and old_persistent.tried_skip is not None and persistent.tried_skip is not None:
            persistent.tried_skip = persistent.tried_skip or old_persistent.tried_skip
        elif old_persistent.tried_skip is not None:
            persistent.tried_skip=old_persistent.tried_skip



        if merge_previous is True and old_persistent.yuri_kill is not None and persistent.yuri_kill is not None:
            persistent.yuri_kill = persistent.yuri_kill or old_persistent.yuri_kill
        elif old_persistent.yuri_kill is not None:
            persistent.yuri_kill=old_persistent.yuri_kill


        persistent.has_merged = True

    return

label merge_unmatched_names:
    menu:
        "Save file names do not match. Which would you like to keep?"
        "[old_persistent.playername]":
            $ persistent.playername=old_persistent.playername
        "[persistent.playername]":
            $ persistent.playername

    return

