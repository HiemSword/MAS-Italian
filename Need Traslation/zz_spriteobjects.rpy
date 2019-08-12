














init -2 python in mas_sprites:



    import store

    temp_storage = dict()








    _hair__testing_entry = False
    _hair__testing_exit = False
    _clothes__testing_entry = False
    _clothes__testing_exit = False
    _acs__testing_entry = False
    _acs__testing_exit = False





    def _acs_wear_if_in_tempstorage(_moni_chr, key):
        """
        Wears the acs in tempstorage at the given key, if any.

        IN:
            _moni_chr - MASMonika object
            key - key in tempstorage 
        """
        acs_items = temp_storage.get(key, None)
        if acs_items is not None:
            for acs_item in acs_items:
                _moni_chr.wear_acs(acs_item)


    def _acs_wear_if_in_tempstorage_s(_moni_chr, key):
        """
        Wears a single acs in tempstorage at the given key, if any.

        IN:
            _moni_chr - MASMonika object
            key - key in tempstorage
        """
        acs_item = temp_storage.get(key, None)
        if acs_item is not None:
            _moni_chr.wear_acs(acs_item)


    def _acs_wear_if_wearing_acs(_moni_chr, acs, acs_to_wear):
        """
        Wears the given acs if wearing another acs.

        IN:
            _moni_chr - MASMonika object
            acs - acs to check if wearing
            acs_to_wear - acs to wear if wearing acs
        """
        if _moni_chr.is_wearing_acs(acs):
            _moni_chr.wear_acs(acs_to_wear)


    def _acs_wear_if_wearing_type(_moni_chr, acs_type, acs_to_wear):
        """
        Wears the given acs if wearing an acs of the given type.

        IN:
            _moni_chr - MASMonika object
            acs_type - acs type to check if wearing
            acs_to_wear - acs to wear if wearing acs type
        """
        if _moni_chr.is_wearing_acs_type(acs_type):
            _moni_chr.wear_acs(acs_to_wear)


    def _acs_wear_if_not_wearing_type(_moni_chr, acs_type, acs_to_wear):
        """
        Wears the given acs if NOT wearing an acs of the given type.

        IN:
            _moni_chr - MASMonika object
            acs_type - asc type to check if not wearing
            acs_to_wear - acs to wear if not wearing acs type
        """
        if not _moni_chr.is_wearing_acs_type(acs_type):
            _moni_chr.wear_acs(acs_to_wear)


    def _acs_ribbon_save_and_remove(_moni_chr):
        """
        Removes ribbon acs and aves them to temp storage.

        IN:
            _moni_chr - MASMonika object
        """
        prev_ribbon = _moni_chr.get_acs_of_type("ribbon")
        
        
        if prev_ribbon != store.mas_acs_ribbon_blank:
            temp_storage["hair.ribbon"] = prev_ribbon
        
        if prev_ribbon is not None:
            _moni_chr.remove_acs(prev_ribbon)
        
        
        store.mas_lockEVL("monika_ribbon_select", "EVE")


    def _acs_save_and_remove_exprop(_moni_chr, exprop, key, lock_topics):
        """
        Removes acs with given exprop, saving them to temp storage with
        given key.
        Also locks topics with the exprop if desired

        IN:
            _moni_chr - MASMonika object
            exprop - exprop to remove and save acs
            key - key to use for temp storage
            lock_topics - True will lock topics associated with this exprop
                False will not
        """
        acs_items = _moni_chr.get_acs_of_exprop(exprop, get_all=True)
        if len(acs_items) > 0:
            temp_storage[key] = acs_items
            _moni_chr.remove_acs_exprop(exprop)
        
        if lock_topics:
            lock_exprop_topics(exprop)


    def _hair_unlock_select_if_needed():
        """
        Unlocks the hairdown selector if enough hair is unlocked.
        """
        if len(store.mas_selspr.filter_hair(True)) > 1:
            store.mas_unlockEVL("monika_hair_select", "EVE")









    def _hair_def_entry(_moni_chr, **kwargs):
        """
        Entry programming point for ponytail
        """
        pass


    def _hair_def_exit(_moni_chr, **kwargs):
        """
        Exit programming point for ponytail
        """
        pass


    def _hair_down_entry(_moni_chr, **kwargs):
        """
        Entry programming point for hair down
        """
        pass


    def _hair_down_exit(_moni_chr, **kwargs):
        """
        Exit programming point for hair down
        """
        pass


    def _hair_bun_entry(_moni_chr, **kwargs):
        """
        Entry programming point for hair bun
        """
        pass









    def _clothes_def_entry(_moni_chr, **kwargs):
        """
        Entry programming point for def clothes
        """
        pass



    def _clothes_rin_entry(_moni_chr, **kwargs):
        """
        Entry programming point for rin clothes
        """
        
        temp_storage["clothes.rin"] = store.mas_acs_promisering.pose_map
        store.mas_acs_promisering.pose_map = store.MASPoseMap(
            p1=None,
            p2=None,
            p3="1",
            p4=None,
            p5="5old",
            p6=None
        )
        
        
        store.mas_lockEVL("monika_hair_select", "EVE")
        
        
        
        
        
        
        
        _acs_ribbon_save_and_remove(_moni_chr)
        
        
        
        
        
        
        
        
        
        
        _moni_chr.lock_hair = True
        
        
        store.mas_lockEVL("monika_ribbon_select", "EVE")
        
        
        
        
        _acs_save_and_remove_exprop(
            _moni_chr,
            "left-hair-strand-eye-level",
            "acs.left-hair-strand-eye-level",
            True
        )
        
        
        
        
        _moni_chr.remove_acs(store.mas_acs_ear_rose)





    def _clothes_rin_exit(_moni_chr, **kwargs):
        """
        Exit programming point for rin clothes
        """
        rin_map = temp_storage.get("clothes.rin", None)
        if rin_map is not None:
            store.mas_acs_promisering.pose_map = rin_map
        
        
        _hair_unlock_select_if_needed()
        
        
        
        
        
        
        _acs_wear_if_in_tempstorage_s(_moni_chr, "hair.ribbon")
        
        
        
        
        
        
        
        
        
        
        
        
        
        _moni_chr.lock_hair = False
        
        
        if _moni_chr.is_wearing_hair_with_exprop("ribbon"):
            store.mas_filterUnlockGroup(SP_ACS, "ribbon")
        
        
        
        
        _acs_wear_if_in_tempstorage(
            _moni_chr,
            "acs.left-hair-strand-eye-level"
        )
        store.mas_filterUnlockGroup(SP_ACS, "left-hair-clip")


    def _clothes_marisa_entry(_moni_chr, **kwargs):
        """
        Entry programming point for marisa clothes
        """
        
        temp_storage["clothes.marisa"] = store.mas_acs_promisering.pose_map
        store.mas_acs_promisering.pose_map = store.MASPoseMap(
            p1=None,
            p2="6",
            p3="1",
            p4=None,
            p5=None,
            p6=None
        )
        
        
        store.mas_lockEVL("monika_hair_select", "EVE")
        
        
        
        
        
        
        _acs_ribbon_save_and_remove(_moni_chr)
        
        
        
        
        
        
        
        
        
        
        _moni_chr.lock_hair = True
        
        
        store.mas_lockEVL("monika_ribbon_select", "EVE")
        
        
        _acs_save_and_remove_exprop(
            _moni_chr,
            "left-hair-strand-eye-level",
            "acs.left-hair-strand-eye-level",
            True
        )
        
        
        
        
        _moni_chr.remove_acs(store.mas_acs_ear_rose)





    def _clothes_marisa_exit(_moni_chr, **kwargs):
        """
        Exit programming point for marisa clothes
        """
        marisa_map = temp_storage.get("clothes.marisa", None)
        if marisa_map is not None:
            store.mas_acs_promisering.pose_map = marisa_map
        
        
        _hair_unlock_select_if_needed()
        
        
        
        
        
        
        _acs_wear_if_in_tempstorage_s(_moni_chr, "hair.ribbon")
        
        
        
        
        
        
        
        _moni_chr.lock_hair = False
        
        
        
        
        if _moni_chr.is_wearing_hair_with_exprop("ribbon"):
            store.mas_filterUnlockGroup(SP_ACS, "ribbon")
        
        
        
        
        _acs_wear_if_in_tempstorage(
            _moni_chr,
            "acs.left-hair-strand-eye-level"
        )
        store.mas_filterUnlockGroup(SP_ACS, "left-hair-clip")


    def _clothes_santa_entry(_moni_chr, **kwargs):
        """
        Entry programming point for santa clothes
        """
        
        temp_storage["clothes.santa"] = store.mas_acs_promisering.pose_map
        store.mas_acs_promisering.pose_map = store.MASPoseMap(
            p1=None,
            p2="7",
            p3="1",
            p4=None,
            p5=None,
            p6=None
        )
        
        
        
        _moni_chr.remove_acs(store.mas_acs_ear_rose)


    def _clothes_santa_exit(_moni_chr, **kwargs):
        """
        Exit programming point for santa clothes
        """
        santa_map = temp_storage.get("clothes.santa", None)
        if santa_map is not None:
            store.mas_acs_promisering.pose_map = santa_map





    def _clothes_sundress_white_entry(_moni_chr, **kwargs):
        """
        Entry programming point for sundress white
        """
        _moni_chr.wear_acs(store.mas_acs_hairties_bracelet_brown)
        _moni_chr.wear_acs(store.mas_acs_musicnote_necklace_gold)


    def _clothes_sundress_white_exit(_moni_chr, **kwargs):
        """
        Exit programming point for sundress white
        """
        
        
        _moni_chr.remove_acs(store.mas_acs_hairties_bracelet_brown)
        _moni_chr.remove_acs(store.mas_acs_musicnote_necklace_gold)






    def _acs_quetzalplushie_entry(_moni_chr, **kwargs):
        """
        Entry programming point for quetzal plushie acs
        """
        
        store.mas_showEVL('monika_plushie','EVE',_random=True)


    def _acs_quetzalplushie_exit(_moni_chr, **kwargs):
        """
        Exit programming point for quetzal plushie acs
        """
        
        _moni_chr.remove_acs(store.mas_acs_quetzalplushie_santahat)
        
        
        _moni_chr.remove_acs(store.mas_acs_quetzalplushie_antlers)
        
        
        store.mas_hideEVL('monika_plushie','EVE',derandom=True)


    def _acs_quetzalplushie_santahat_entry(_moni_chr, **kwargs):
        """
        Entry programming point for quetzal plushie santa hat acs
        """
        
        _moni_chr.wear_acs(store.mas_acs_quetzalplushie)


    def _acs_quetzalplushie_antlers_entry(_moni_chr, **kwargs):
        """
        Entry programming point for quetzal plushie antlers acs
        """
        
        _moni_chr.wear_acs(store.mas_acs_quetzalplushie)


    def _acs_heartchoc_entry(_moni_chr, **kwargs):
        """
        Entry programming point for heartchoc acs
        """
        
        
        
        
        
        
        if not (store.mas_isF14() or store.mas_isD25Season()):
            if _moni_chr.is_wearing_acs(store.mas_acs_quetzalplushie):
                _moni_chr.wear_acs(store.mas_acs_center_quetzalplushie)
        
        else:
            _moni_chr.remove_acs(store.mas_acs_quetzalplushie)


    def _acs_heartchoc_exit(_moni_chr, **kwargs):
        """
        Exit programming point for heartchoc acs
        """
        if _moni_chr.is_wearing_acs(store.mas_acs_center_quetzalplushie):
            _moni_chr.wear_acs(store.mas_acs_quetzalplushie)



init -1 python:








































    mas_hair_def = MASHair(
        "def",
        "def",
        MASPoseMap(
            default=True,
            use_reg_for_l=True
        ),


        ex_props={
            "ribbon": True,
            "ribbon-restore": True
        }
    )
    store.mas_sprites.init_hair(mas_hair_def)
    store.mas_selspr.init_selectable_hair(
        mas_hair_def,
        "Ponytail",
        "def",
        "hair",
        select_dlg=[
            "Do you like my ponytail, [player]?"
        ]
    )
    store.mas_selspr.unlock_hair(mas_hair_def)





    mas_hair_down = MASHair(
        "down",
        "down",
        MASPoseMap(
            default=True,
            use_reg_for_l=True
        ),



    )
    store.mas_sprites.init_hair(mas_hair_down)
    store.mas_selspr.init_selectable_hair(
        mas_hair_down,
        "Down",
        "down",
        "hair",
        select_dlg=[
            "Feels nice to let my hair down..."
        ]
    )





    mas_hair_ponytail = MASHair(
        "ponytail",
        "def",  
        MASPoseMap(
            default = True,
            use_reg_for_l=True,
        ),

        ex_props={
            "ribbon": True,
            "ribbon-off": True,
        }
    )



































    mas_hair_custom = MASHair(
        "custom",
        "custom",
        MASPoseMap(),

        
        split=MASPoseMap(
            default=False,
            use_reg_for_l=True
        ),
    )
    store.mas_sprites.init_hair(mas_hair_custom)


init -1 python:




























    mas_clothes_def = MASClothes(
        "def",
        "def",
        MASPoseMap(
            default=True,
            use_reg_for_l=True
        ),
        stay_on_start=True,
        entry_pp=store.mas_sprites._clothes_def_entry,
    )
    store.mas_sprites.init_clothes(mas_clothes_def)
    store.mas_selspr.init_selectable_clothes(
        mas_clothes_def,
        "School Uniform",
        "schooluniform",
        "clothes",
        visible_when_locked=True,
        hover_dlg=None,
        select_dlg=[
            "Ready for school!"
        ]
    )
    store.mas_selspr.unlock_clothes(mas_clothes_def)





    mas_clothes_marisa = MASClothes(
        "marisa",
        "marisa",
        MASPoseMap(
            p1="steepling",
            p2="crossed",
            p3="restleftpointright",
            p4="pointright",
            p6="down"
        ),
        fallback=True,
        hair_map={
            "all": "custom"
        },
        stay_on_start=True,
        entry_pp=store.mas_sprites._clothes_marisa_entry,
        exit_pp=store.mas_sprites._clothes_marisa_exit,
        ex_props={
            "forced hair": True,
            "baked outfit": True,
        }
    )
    store.mas_sprites.init_clothes(mas_clothes_marisa)
    store.mas_selspr.init_selectable_clothes(
        mas_clothes_marisa,
        "Witch Costume",
        "marisa",
        "clothes",
        visible_when_locked=False,
        hover_dlg=None,
        select_dlg=[
            "Just an ordinary costume, ~ze."
        ]
    )






    mas_clothes_rin = MASClothes(
        "rin",
        "rin",
        MASPoseMap(
            p1="steepling",
            p2="crossed",
            p3="restleftpointright",
            p4="pointright",
            p6="down"
        ),
        fallback=True,
        hair_map={
            "all": "custom"
        },
        stay_on_start=True,
        entry_pp=store.mas_sprites._clothes_rin_entry,
        exit_pp=store.mas_sprites._clothes_rin_exit,
        ex_props={
            "forced hair": True,
            "baked outfit": True,
        }
    )
    store.mas_sprites.init_clothes(mas_clothes_rin)
    store.mas_selspr.init_selectable_clothes(
        mas_clothes_rin,
        "Neko Costume",
        "rin",
        "clothes",
        visible_when_locked=False,
        hover_dlg=[
            "~nya?",
            "n-nya..."
        ],
        select_dlg=[
            "Nya!"
        ]
    )





    mas_clothes_santa = MASClothes(
        "santa",
        "santa",
        




        MASPoseMap(
            p1="steepling",
            p2="crossed",
            p3="restleftpointright",
            p4="pointright",
            p6="down"
        ),
        fallback=True,
        hair_map={
            "bun": "def"
        },
        stay_on_start=True,
        entry_pp=store.mas_sprites._clothes_santa_entry,
        exit_pp=store.mas_sprites._clothes_santa_exit,
        ex_props={
            "desired-ribbon": "ribbon_wine",
        },
    )
    store.mas_sprites.init_clothes(mas_clothes_santa)
    store.mas_selspr.init_selectable_clothes(
        mas_clothes_santa,
        "Santa Costume",
        "santa",
        "clothes",
        visible_when_locked=False,
        hover_dlg=None,
        select_dlg=[
            "Merry Christmas!",
            "What kind of {i}presents{/i} do you want?",
            "Happy holidays!"
        ]
    )





    mas_clothes_sundress_white = MASClothes(
        "sundress_white",
        "sundress_white",
        MASPoseMap(
            default=True,
            use_reg_for_l=True,
        ),
        stay_on_start=True,
        entry_pp=store.mas_sprites._clothes_sundress_white_entry,
        exit_pp=store.mas_sprites._clothes_sundress_white_exit,
    )
    store.mas_sprites.init_clothes(mas_clothes_sundress_white)
    store.mas_selspr.init_selectable_clothes(
        mas_clothes_sundress_white,
        "Sundress (White)",
        "sundress_white",
        "clothes",
        visible_when_locked=False,
        hover_dlg=None,
        select_dlg=[
            "Are we going anywhere special today, [player]?",
            "I've always loved this outfit...",
        ],
    )


init -1 python:





























    mas_acs_mug = MASAccessory(
        "mug",
        "mug",
        MASPoseMap(
            default="0",
            use_reg_for_l=True
        ),
        stay_on_start=True,
        acs_type="mug",
        mux_type=["mug"]
    )
    store.mas_sprites.init_acs(mas_acs_mug)





    mas_acs_ear_rose = MASAccessory(
        "ear_rose",
        "ear_rose",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=False,
        rec_layer=MASMonika.PST_ACS,
    )
    store.mas_sprites.init_acs(mas_acs_ear_rose)





    mas_acs_hairties_bracelet_brown = MASAccessory(
        "hairties_bracelet_brown",
        "hairties_bracelet_brown",
        MASPoseMap(
            p1="1",
            p2="2",
            p3="1",
            p4="4",
            p5="5",
            p6=None
        ),
        stay_on_start=True,
        acs_type="wrist-bracelet",
        mux_type=["wrist-bracelet"],
        ex_props={
            "bare wrist": True,
        }
    )
    store.mas_sprites.init_acs(mas_acs_hairties_bracelet_brown)





    mas_acs_heartchoc = MASAccessory(
        "heartchoc",
        "heartchoc",
        MASPoseMap(
            default="0",
            use_reg_for_l=True
        ),
        stay_on_start=False,
        acs_type="chocs",
        
        entry_pp=store.mas_sprites._acs_heartchoc_entry,
        exit_pp=store.mas_sprites._acs_heartchoc_exit
    )
    store.mas_sprites.init_acs(mas_acs_heartchoc)





    mas_acs_hotchoc_mug = MASAccessory(
        "hotchoc_mug",
        "hotchoc_mug",
        MASPoseMap(
            default="0",
            use_reg_for_l=True
        ),
        stay_on_start=True,
        acs_type="mug",
        mux_type=["mug"]
    )
    store.mas_sprites.init_acs(mas_acs_hotchoc_mug)





    mas_acs_musicnote_necklace_gold = MASAccessory(
        "musicnote_necklace_gold",
        "musicnote_necklace_gold",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="necklace",
        mux_type=["necklace"],
        ex_props={
            "bare collar": True,
        },
        rec_layer=MASMonika.BFH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_musicnote_necklace_gold)




    mas_acs_promisering = MASAccessory(
        "promisering",
        "promisering",
        MASPoseMap(
            p1=None,
            p2="4",
            p3="1",
            p4=None,
            p5="5",
            p6=None
        ),
        stay_on_start=True,
        acs_type="ring",
        ex_props={
            "bare hands": True
        }
    )
    store.mas_sprites.init_acs(mas_acs_promisering)





    mas_acs_quetzalplushie = MASAccessory(
        "quetzalplushie",
        "quetzalplushie",
        MASPoseMap(
            default="0",
            use_reg_for_l=True
        ),
        stay_on_start=False,
        acs_type="plush_q",

        
        
        mux_type=["plush_mid"],
        entry_pp=store.mas_sprites._acs_quetzalplushie_entry,
        exit_pp=store.mas_sprites._acs_quetzalplushie_exit
    )
    store.mas_sprites.init_acs(mas_acs_quetzalplushie)





    mas_acs_quetzalplushie_antlers = MASAccessory(
        "quetzalplushie_antlers",
        "quetzalplushie_antlers",
        MASPoseMap(
            default="0",
            use_reg_for_l=True
        ),
        priority=12,
        stay_on_start=False,
        entry_pp=store.mas_sprites._acs_quetzalplushie_antlers_entry
    )




    mas_acs_center_quetzalplushie = MASAccessory(
        "quetzalplushie_mid",
        "quetzalplushie_mid",
        MASPoseMap(
            default="0",
            use_reg_for_l=True
        ),
        stay_on_start=False,
        acs_type="plush_mid",
        mux_type=["plush_q"],
    )
    store.mas_sprites.init_acs(mas_acs_center_quetzalplushie)





    mas_acs_quetzalplushie_santahat = MASAccessory(
        "quetzalplushie_santahat",
        "quetzalplushie_santahat",
        MASPoseMap(
            default="0",
            use_reg_for_l=True
        ),
        priority=11,
        stay_on_start=False,
        entry_pp=store.mas_sprites._acs_quetzalplushie_santahat_entry
    )
    store.mas_sprites.init_acs(mas_acs_quetzalplushie_santahat)





    mas_acs_ribbon_black = MASAccessory(
        "ribbon_black",
        "ribbon_black",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_black)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_black,
        "Ribbon (Black)",
        "ribbon_black",
        "ribbon",
        hover_dlg=[
            "That's pretty formal, [player]."
        ],
        select_dlg=[
            "Are we going somewhere special, [player]?"
        ]
    )




    mas_acs_ribbon_blank = MASAccessory(
        "ribbon_blank",
        "ribbon_blank",
        MASPoseMap(
            default="0",
            use_reg_for_l=True
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_blank)





    mas_acs_ribbon_blue = MASAccessory(
        "ribbon_blue",
        "ribbon_blue",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_blue)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_blue,
        "Ribbon (Blue)",
        "ribbon_blue",
        "ribbon",
        hover_dlg=[
            "Like the ocean..."
        ],
        select_dlg=[
            "Great choice, [player]!"
        ]
    )





    mas_acs_ribbon_darkpurple = MASAccessory(
        "ribbon_dark_purple",
        "ribbon_dark_purple",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_darkpurple)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_darkpurple,
        "Ribbon (Dark Purple)",
        "ribbon_dark_purple",
        "ribbon",
        hover_dlg=[
            "I love that color!"
        ],
        select_dlg=[
            "Lavender is a nice change of pace."
        ]
    )





    mas_acs_ribbon_emerald = MASAccessory(
        "ribbon_emerald",
        "ribbon_emerald",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_emerald)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_emerald,
        "Ribbon (Emerald)",
        "ribbon_emerald",
        "ribbon",
        hover_dlg=[
            "I've always loved this color...",
        ],
        select_dlg=[
            "It's just like my eyes!"
        ]
    )




    mas_acs_ribbon_def = MASAccessory(
        "ribbon_def",
        "ribbon_def",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_def)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_def,
        "Ribbon (White)",
        "ribbon_def",
        "ribbon",
        hover_dlg=[
            "Do you miss my old ribbon, [player]?"
        ],
        select_dlg=[
            "Back to the classics!"
        ]
    )





    mas_acs_ribbon_gray = MASAccessory(
        "ribbon_gray",
        "ribbon_gray",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_gray)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_gray,
        "Ribbon (Gray)",
        "ribbon_gray",
        "ribbon",
        hover_dlg=[
            "Like a warm, rainy day..."
        ],
        select_dlg=[
            "That's a really unique color, [player]."
        ]
    )





    mas_acs_ribbon_green = MASAccessory(
        "ribbon_green",
        "ribbon_green",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_green)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_green,
        "Ribbon (Green)",
        "ribbon_green",
        "ribbon",
        hover_dlg=[
            "That's a lovely color!"
        ],
        select_dlg=[
            "Green, just like my eyes!"
        ]
    )





    mas_acs_ribbon_lightpurple = MASAccessory(
        "ribbon_light_purple",
        "ribbon_light_purple",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_lightpurple)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_lightpurple,
        "Ribbon (Light Purple)",
        "ribbon_light_purple",
        "ribbon",
        hover_dlg=[
            "This purple looks pretty nice, right [player]?"
        ],
        select_dlg=[
            "Really has a spring feel to it."
        ]
    )





    mas_acs_ribbon_peach = MASAccessory(
        "ribbon_peach",
        "ribbon_peach",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_peach)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_peach,
        "Ribbon (Peach)",
        "ribbon_peach",
        "ribbon",
        hover_dlg=[
            "That's beautiful!"
        ],
        select_dlg=[
            "Just like autumn leaves..."
        ]
    )





    mas_acs_ribbon_pink = MASAccessory(
        "ribbon_pink",
        "ribbon_pink",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_pink)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_pink,
        "Ribbon (Pink)",
        "ribbon_pink",
        "ribbon",
        hover_dlg=[
            "Looks cute, right?"
        ],
        select_dlg=[
            "Good choice!"
        ]
    )





    mas_acs_ribbon_platinum = MASAccessory(
        "ribbon_platinum",
        "ribbon_platinum",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_platinum)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_platinum,
        "Ribbon (Platinum)",
        "ribbon_platinum",
        "ribbon",
        hover_dlg=[
            "That's an interesting color, [player].",
        ],
        select_dlg=[
            "I'm quite fond of it, actually."
        ]
    )





    mas_acs_ribbon_red = MASAccessory(
        "ribbon_red",
        "ribbon_red",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_red)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_red,
        "Ribbon (Red)",
        "ribbon_red",
        "ribbon",
        hover_dlg=[
            "Red is a beautiful color!"
        ],
        select_dlg=[
            "Just like roses~"
        ]
    )





    mas_acs_ribbon_ruby = MASAccessory(
        "ribbon_ruby",
        "ribbon_ruby",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_ruby)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_ruby,
        "Ribbon (Ruby)",
        "ribbon_ruby",
        "ribbon",
        hover_dlg=[
            "That's a beautiful shade of red."
        ],
        select_dlg=[
            "Doesn't it look pretty?"
        ]
    )





    mas_acs_ribbon_sapphire = MASAccessory(
        "ribbon_sapphire",
        "ribbon_sapphire",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_sapphire)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_sapphire,
        "Ribbon (Sapphire)",
        "ribbon_sapphire",
        "ribbon",
        hover_dlg=[
            "Like a clear summer sky..."
        ],
        select_dlg=[
            "Nice choice, [player]!"
        ]
    )





    mas_acs_ribbon_silver = MASAccessory(
        "ribbon_silver",
        "ribbon_silver",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_silver)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_silver,
        "Ribbon (Silver)",
        "ribbon_silver",
        "ribbon",
        hover_dlg=[
            "I like the look of this one.",
            "I've always loved silver."
        ],
        select_dlg=[
            "Nice choice, [player]."
        ]
    )





    mas_acs_ribbon_teal = MASAccessory(
        "ribbon_teal",
        "ribbon_teal",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_teal)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_teal,
        "Ribbon (Teal)",
        "ribbon_teal",
        "ribbon",
        hover_dlg=[
            "Looks really summer-y, right?"
        ],
        select_dlg=[
            "Just like a summer sky."
        ]
    )





    mas_acs_ribbon_wine = MASAccessory(
        "ribbon_wine",
        "ribbon_wine",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_wine)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_wine,
        "Ribbon (Wine)",
        "ribbon_wine",
        "ribbon",
        hover_dlg=[
            "That's a great color!"
        ],
        select_dlg=[
            "Formal! Are you taking me somewhere special, [player]?"
        ]
    )





    mas_acs_ribbon_yellow = MASAccessory(
        "ribbon_yellow",
        "ribbon_yellow",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_yellow)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_yellow,
        "Ribbon (Yellow)",
        "ribbon_yellow",
        "ribbon",
        hover_dlg=[
            "This color reminds me of a nice summer day!"
        ],
        select_dlg=[
            "Great choice, [player]!"
        ]
    )





    mas_acs_roses = MASAccessory(
        "roses",
        "roses",
        MASPoseMap(
            default="0",
            use_reg_for_l=True
        ),
        priority=11,
        stay_on_start=False,
        acs_type="flowers",
    )
    store.mas_sprites.init_acs(mas_acs_roses)














default persistent._mas_acs_enable_coffee = False


default persistent._mas_coffee_been_given = False


default persistent._mas_coffee_brew_time = None


default persistent._mas_coffee_cup_done = None


default persistent._mas_coffee_cups_drank = 0


define mas_coffee.BREW_LOW = 2*60


define mas_coffee.BREW_HIGH = 4*60


define mas_coffee.DRINK_LOW = 10 * 60


define mas_coffee.DRINK_HIGH = 2 * 3600


define mas_coffee.BREW_CHANCE = 80



define mas_coffee.DRINK_CHANCE = 80



define mas_coffee.COFFEE_TIME_START = 5


define mas_coffee.COFFEE_TIME_END = 12


define mas_coffee.BREW_DRINK_SPLIT = 9











default persistent._mas_acs_enable_hotchoc = False


default persistent._mas_c_hotchoc_been_given = False


default persistent._mas_c_hotchoc_brew_time = None


default persistent._mas_c_hotchoc_cup_done = None


default persistent._mas_c_hotchoc_cups_drank = 0


define mas_coffee.HOTCHOC_TIME_START = 19


define mas_coffee.HOTCHOC_TIME_END = 22


define mas_coffee.HOTCHOC_BREW_DRINK_SPLIT = 21



default persistent._mas_acs_enable_quetzalplushie = False



default persistent._mas_acs_enable_promisering = False
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
