

























































































































































































































default persistent._mas_sprites_json_gifted_sprites = {}










init -21 python in mas_sprites_json:
    import __builtin__
    import json
    import store
    import store.mas_utils as mas_utils


    from store.mas_ev_data_ver import _verify_bool, _verify_str, \
        _verify_int, _verify_list

    log = mas_utils.getMASLog("log/spj")
    log_open = log.open()
    log.raw_write = True

    py_list = __builtin__.list
    py_dict = __builtin__.dict

    sprite_station = store.MASDockingStation(
        renpy.config.basedir + "/game/mod_assets/monika/j/"
    )





    hm_key_delayed_veri = {}


    hm_val_delayed_veri = {}




    def _add_hair_to_verify(hairname, verimap, name):
        
        if hairname not in verimap:
            verimap[hairname] = []
        
        verimap[hairname].append(name)





    giftname_map = {
        "__testing": (0, "__testing"),
    }











    namegift_map = {
        (0, "__testing"): "__testing",
    }





    def writelog(msg):
        
        if log_open:
            log.write(msg)


    def writelogs(msgs):
        
        if log_open:
            for msg in msgs:
                log.write(msg)
        
        
        msgs[:] = []




    READING_FILE = "reading JSON at '{0}'..."
    SP_LOADING = "loading {0} sprite object '{1}'..."
    SP_SUCCESS = "{0} sprite object '{1}' loaded successfully!"
    SP_SUCCESS_DRY = "{0} sprite object '{1}' loaded successfully! DRY RUN"

    BAD_TYPE = "property '{0}' - expected type {1}, got {2}"
    EXTRA_PROP = "extra property '{0}' found"
    REQ_MISS = "required property '{0}' not found"
    BAD_SPR_TYPE = "invalid sprite type '{0}'"
    BAD_ACS_LAYER = "invalid ACS layer '{0}'"
    BAD_LIST_TYPE = "property '{0}' index '{1}' - expected type {2}, got {3}"
    EMPTY_LIST = "property '{0}' cannot be an empty list"

    DUPE_GIFTNAME = "giftname '{0}' already exists"
    MATCH_GIFT = (
        "cannot associate giftname '{0}' with sprite object type {1} name "
        "'{2}' - sprite object already associated with giftname '{3}'"
    )
    NO_GIFT = "without 'giftname', this cannot be natively unlocked"


    MPM_LOADING = "loading MASPoseMap in '{0}'..."
    MPM_SUCCESS = "MASPoseMap '{0}' loaded successfully!"
    MPM_BAD_POSE = "property '{0}' - invalid pose '{1}'"
    MPM_FB_DEF = "in fallback mode but default not set"
    MPM_FB_DEF_L = "in fallback mode but leaning default not set"
    MPM_ACS_DEF = "acs default pose not set"
    MPM_ACS_DEF_L = "acs leaning default pose not set"
    MPM_ACS_BAD_POSE_TYPE = "property '{0}' - expected type {1}, got {2}"


    HM_LOADING = "loading hair_map..."
    HM_SUCCESS = "hair_map loaded successfully!"
    HM_BAD_K_TYPE = "key '{0}' - expected type {1}, got {2}"
    HM_BAD_V_TYPE = "value for key '{0}' - expected type {1}, got {2}"
    HM_MISS_ALL = "hair_map does not have key 'all' set. Using default for 'all'."
    HM_FOUND_CUST = (
        "'custom' hair cannot be used in JSON hair maps. "
        "Outfits using 'custom' hair must be created manually."
    )
    HM_VER_ALL = "verifying hair maps..."
    HM_VER_SUCCESS = "hair map verification complete!"
    HM_NO_KEY = (
        "hair '{0}' does not exist - found in hair_map keys of these "
        "sprites: {1}"
    )
    HM_NO_VAL = (
        "hair '{0}' does not exist - found in hair_map values of these "
        "sprites: {1}. replacing with defaults."
    )


    EP_LOADING = "loading ex_props..."
    EP_SUCCESS = "ex_props loaded successfully!"
    EP_BAD_K_TYPE = "key '{0}' - expected type {1}, got {2}"
    EP_BAD_V_TYPE = "value for key '{0}' - expected type int/str/bool, got {1}"


    SI_LOADING = "loading select_info..."
    SI_SUCCESS = "sel_info loaded successfully!"


    PP_MISS = "'{0}' progpoint not found"
    PP_NOTFUN = "'{0}' progpoint not callable"


    IL_NOTLOAD = "image at '{0}' is not loadable"


    GR_LOADING = "creating reactions for gifts..."
    GR_SUCCESS = "gift reactions created successfully!"
    GR_FOUND = "reaction label found for {0} sprite '{1}', giftname '{2}'"
    GR_GEN = "using generic reaction for {0} sprite '{1}', giftname '{2}'"



    SP_ACS = 0
    SP_HAIR = 1
    SP_CLOTHES = 2

    SP_CONSTS = (
        SP_ACS,
        SP_HAIR,
        SP_CLOTHES,
    )

    SP_STR = {
        SP_ACS: "ACS",
        SP_HAIR: "HAIR",
        SP_CLOTHES: "CLOTHES",
    }

    SP_UF_STR = {
        SP_ACS: "accessory",
        SP_HAIR: "hairstyle",
        SP_CLOTHES: "outfit",
    }

    SP_PP = {
        SP_ACS: "store.mas_sprites._acs_{0}_{1}",
        SP_HAIR: "store.mas_sprites._hair_{0}_{1}",
        SP_CLOTHES: "store.mas_sprites._clothes_{0}_{1}",
    }

    SP_RL = {
        SP_ACS: "mas_reaction_gift_acs_{0}",
        SP_HAIR: "mas_reaction_gift_hair_{0}",
        SP_CLOTHES: "mas_reaction_gift_clothes_{0}",
    }

    SP_RL_GEN = "{0}|{1}|{2}"

    def _verify_sptype(val, allow_none=True):
        if val is None:
            return allow_none
        return val in SP_CONSTS






    REQ_SHARED_PARAM_NAMES = {
        

        "name": (str, _verify_str),
        "img_sit": (str, _verify_str),
        

    }

    OPT_SHARED_PARAM_NAMES = {
        "stay_on_start": (bool, _verify_bool),

        



    }

    OPT_AC_SHARED_PARAM_NAMES = {
        "giftname": (str, _verify_str),
    }

    OPT_ACS_PARAM_NAMES = {
        



        "priority": (int, _verify_int),
        "acs_type": (str, _verify_str),
    }
    OPT_ACS_PARAM_NAMES.update(OPT_AC_SHARED_PARAM_NAMES)

    OPT_HC_SHARED_PARAM_NAMES = {
        "fallback": (bool, _verify_bool),
    }

    OPT_HAIR_PARAM_NAMES = {
        

        "unlock": (bool, _verify_bool),
    }

    OPT_CLOTH_PARAM_NAMES = {
        

    }
    OPT_CLOTH_PARAM_NAMES.update(OPT_AC_SHARED_PARAM_NAMES)


    OBJ_BASED_PARAM_NAMES = (
        "pose_map",
        "ex_props",
        "select_info",
        "split",
        "hair_map",
    )


    SEL_INFO_REQ_PARAM_NAMES = {
        "display_name": (str, _verify_str),
        "thumb": (str, _verify_str),
        "group": (str, _verify_str),
    }

    SEL_INFO_OPT_PARAM_NAMES = {
        "visible_when_locked": (bool, _verify_bool),
    }



    DRY_RUN = "dryrun"


init 189 python in mas_sprites_json:
    from store.mas_sprites import _verify_pose, HAIR_MAP, CLOTH_MAP, ACS_MAP
    from store.mas_piano_keys import MSG_INFO, MSG_WARN, MSG_ERR, \
        JSON_LOAD_FAILED, FILE_LOAD_FAILED, \
        MSG_INFO_ID, MSG_WARN_ID, MSG_ERR_ID, \
        LOAD_TRY, LOAD_SUCC, LOAD_FAILED, \
        NAME_BAD


    import store.mas_sprites as sms
    import store.mas_selspr as sml



    MSG_INFO_IDD = "        [info]: {0}\n"
    MSG_WARN_IDD = "        [Warning!]: {0}\n"
    MSG_ERR_IDD = "        [!ERROR!]: {0}\n"


    def _replace_hair_map(sp_name, hair_to_replace):
        """
        Replaces the hair vals of the given sprite object with the given name
        of the given hair with defaults.

        IN:
            sp_name - name of the clothing sprite object to replace hair
                map values in
            hair_to_replace - hair name to replace with defaults
        """
        
        sp_obj = CLOTH_MAP.get(sp_name, None)
        if sp_obj is None or sp_obj.hair_map is None:
            return
        
        
        for hair_key in sp_obj.hair_map:
            if sp_obj.hair_map[hair_key] == hair_to_replace:
                sp_obj.hair_map[hair_key] = store.mas_hair_def.name


    def _remove_sel_list(name, sel_list):
        """
        Removes selectable from selectbale list

        Only intended for json usage. DO not use elsewhere. In general, you
        should NEVER need to remove a selectable from the selectable list.
        """
        for index in range(len(sel_list)-1, -1, -1):
            if sel_list[index].name == name:
                sel_list.pop(index)


    def _reset_sp_obj(sp_obj):
        """
        Uninits the given sprite object. This is meant only for json
        sprite usage if we need to back out.

        IN:
            sp_obj - sprite object to remove
        """
        sp_type = sp_obj.gettype()
        sp_name = sp_obj.name
        
        
        if sp_type not in SP_CONSTS:
            return
        
        if sp_type == SP_ACS:
            _item_map = sms.ACS_MAP
            _sel_map = sml.ACS_SEL_MAP
            _sel_list = sml.ACS_SEL_SL
        
        elif sp_type == SP_HAIR:
            _item_map = sms.HAIR_MAP
            _sel_map = sml.HAIR_SEL_MAP
            _sel_list = sml.HAIR_SEL_SL
        
        else:
            
            _item_map = sms.CLOTH_MAP
            _sel_map = sml.CLOTH_SEL_MAP
            _sel_list = sml.CLOTH_SEL_SL
        
        
        if sp_name in _item_map:
            _item_map.pop(sp_name)
        
        if sml.get_sel(sp_obj) is not None:
            
            if sp_name in _sel_map:
                _sel_map.pop(sp_name)
            
            
            _remove_sel_list(sp_name, _sel_list)


    def _build_loadstrs(sp_obj, sel_obj=None):
        """
        Builds list of strings that need to be verified via loadable.

        IN:
            sp_obj - sprite object to build strings from
            sel_obj - selectable to build thumb string from. 
                Ignored if None
                (Default: None)

        RETURNS: list of strings that would need to be loadable verified
        """
        
        to_verify = []
        
        
        
        
        
        
        
        
        
        
        
        
        to_verify.extend(sp_obj._build_loadstrs())
        
        
        if sel_obj is not None:
            to_verify.append(sel_obj._build_thumbstr())
        
        return to_verify


    def _check_giftname(giftname, sp_type, sp_name, errs, err_base):
        """
        Initializes the giftname with the sprite info

        IN:
            giftname - giftname we want to use
            sp_type - sprite type we want to init
            sp_name - name of the sprite object to associated with this gift
                (use the sprite's name property == ID)
            err_base - base to use for the error messages

        OUT:
            errs - list to save error messages to
        """
        
        if giftname in giftname_map:
            errs.append(err_base.format(DUPE_GIFTNAME.format(giftname)))
            return
        
        
        sp_value = (sp_type, sp_name)
        if sp_value in namegift_map:
            errs.append(err_base.format(MATCH_GIFT.format(
                giftname,
                SP_STR[sp_type],
                sp_name,
                namegift_map[sp_value]
            )))
            return


    def _init_giftname(giftname, sp_type, sp_name):
        """
        Initializes the giftname with the sprite info
        does not check for valid giftname.

        IN:
            giftname - giftname we want to use
            sp_type - sprite type we want to init
            sp_name - name of the sprite object to associate with this gift
        """
        
        giftname_map[giftname] = (sp_type, sp_name)
        namegift_map[(sp_type, sp_name)] = giftname


    def _process_giftname():
        """
        Process the gift maps by cleaning the persistent vars
        """
        
        for fr_sp_gn in store.persistent._mas_filereacts_sprite_gifts:
            if fr_sp_gn not in giftname_map:
                store.persistent._mas_filereacts_sprite_gifts.pop(fr_sp_gn)
        
        
        for j_sp_data in store.persistent._mas_sprites_json_gifted_sprites:
            if j_sp_data not in namegift_map:
                store.persistent._mas_sprites_json_gifted_sprites.pop(j_sp_data)


    def _process_progpoint(
            sp_type,
            name,
            save_obj,
            warns,
            infos,
            progname
        ):
        """
        Attempts to find a prop point for a sprite object with the given
        sp_type and name

        IN:
            sp_type - sprite object type
            name - name of sprite object
            progname - name of progpoint (do not include suffix)
        
        OUT:
            save_obj - dict to save progpoint to
            warns - list to save warning messages to
            infos - list to save info messages to
        """
        
        e_pp_str = SP_PP[sp_type].format(name, progname)
        
        
        try:
            e_pp = eval(e_pp_str)
        
        except:
            
            e_pp = None
        
        
        if e_pp is None:
            infos.append(MSG_INFO_ID.format(PP_MISS.format(progname)))
        
        elif not callable(e_pp):
            infos.append(MSG_WARN_ID.format(PP_NOTFUN.format(progname)))
        
        else:
            
            save_obj[progname + "_pp"] = e_pp


    def _test_loadables(sp_obj, errs):
        """
        Tests loadable images and errs if an image is not loadable.

        IN:
            sp_obj - sprite object to test

        OUT:
            errs - list to save error messages to
        """
        
        sel_obj = sml.get_sel(sp_obj)
        
        
        to_verify = _build_loadstrs(sp_obj, sel_obj)
        
        
        for imgpath in to_verify:
            if not renpy.loadable(imgpath):
                errs.append(MSG_ERR_ID.format(IL_NOTLOAD.format(imgpath)))


    def _validate_type(json_obj):
        """
        Validates the type of this json object.

        Logs errors. Also pops type off

        IN:
            json_obj - json object to validate

        RETURNS: SP constant if valid type, None otherwise
        """
        
        if "type" not in json_obj:
            writelog(MSG_ERR_ID.format(REQ_MISS.format("type")))
            return None
        
        
        type_val = json_obj.pop("type")
        if not _verify_sptype(type_val, False):
            writelog(MSG_ERR_ID.format(BAD_SPR_TYPE.format(type(type_val))))
            return None
        
        
        return type_val


    def _validate_mux_type(json_obj, errs):
        """
        Validates mux_type of this json object

        IN:
            json_obj - json object to validate
        
        OUT:
            errs - list to save error messages to
                if nothing was addeed to this list, the mux_type is valid

        RETURNS: mux_type found. May be None
        """
        if "mux_type" not in json_obj:
            return None
        
        
        mux_type = json_obj.pop("mux_type")
        
        if not _verify_list(mux_type):
            
            errs.append(MSG_ERR_ID.format(BAD_TYPE.format(
                "mux_type",
                py_list,
                type(mux_type)
            )))
            return None
        
        
        for index in range(len(mux_type)):
            acs_type = mux_type[index]
            if not _verify_str(acs_type):
                errs.append(MSG_ERR_ID.format(BAD_LIST_TYPE.format(
                    "mux_type",
                    index,
                    str,
                    type(acs_type)
                )))
        
        
        
        
        return mux_type


    def _validate_iterstr(
            jobj,
            save_obj,
            propname,
            required,
            allow_none,
            errs,
            err_base
        ):
        """
        Validates an iterable if it consists solely of strings

        an empty list is considered bad.

        IN:
            jobj - json object to parse
            propname - property name for error messages
            required - True if this property is required, False if not
            allow_none - True if None is valid value, False if not
            err_base - error base to use for error messages

        OUT:
            save_obj - dict to save to
            errs - list to svae error message to
        """
        
        if propname not in jobj:
            if required:
                errs.append(err_base.format(REQ_MISS.format(propname)))
            return
        
        
        iterval = jobj.pop(propname)
        
        
        if iterval is None:
            if not allow_none:
                errs.append(err_base.format(BAD_TYPE.format(
                    propname,
                    py_list,
                    type(iterval)
                )))
            return
        
        
        if len(iterval) <= 0:
            errs.append(err_base.format(EMPTY_LIST.format(propname)))
            return
        
        
        for index in range(len(iterval)):
            item = iterval[index]
            
            if not _verify_str(item):
                errs.append(err_base.format(BAD_LIST_TYPE.format(
                    propname,
                    index,
                    str,
                    type(item)
                )))
        
        
        if len(errs) <= 0:
            save_obj[propname] = iterval


    def _validate_params(
            jobj, 
            save_obj, 
            param_dict,
            required,
            errs,
            err_base
        ):
        """
        Validates a list of parameters, while also saving said params into
        given save object.

        Errors/Warnings are logged to given lists

        IN:
            jobj - json object to parse
            param_dict - dict of params + verification functiosn
            required - True if the given params are required, False otherwise.
            err_base - base format string to use for errors

        OUT:
            save_obj - dict to save data to
            errs - list to save error messages to
        """
        
        allow_none = not required
        
        for param_name, verifier_info in param_dict.iteritems():
            if param_name in jobj:
                param_val = jobj.pop(param_name)
                desired_type, verifier = verifier_info
                
                if not verifier(param_val, allow_none):
                    
                    errs.append(err_base.format(BAD_TYPE.format(
                        param_name,
                        desired_type,
                        type(param_val)
                    )))
                
                else:
                    
                    
                    save_obj[param_name] = param_val
            
            elif required:
                
                errs.append(err_base.format(REQ_MISS.format(param_name)))


    def _validate_acs(jobj, save_obj, obj_based, errs, warns, infos):
        """
        Validates ACS-specific properties, as well as acs pose map

        Props validated:
            - rec_layer
            - priority
            - acs_type
            - mux_type
            - pose_map
            - giftname

        IN:
            jobj - json object to pasrse
            obj_based - dict of object-based items
                (contains pose_map)

        OUT:
            save_obj - dict to save data to
            errs - list to save error messages to
                NOTE: does NOT write errs
            warns - list to save warning messages to
                NOTE: MAY WRITE WARNS
            infos - list to save info messages to
        """
        
        
        
        _validate_params(
            jobj,
            save_obj,
            OPT_ACS_PARAM_NAMES,
            False,
            errs,
            MSG_ERR_ID
        )
        if len(errs) > 0:
            return
        
        
        if "rec_layer" in jobj:
            rec_layer = jobj.pop("rec_layer")
            
            if not store.MASMonika._verify_rec_layer(rec_layer):
                errs.append(MSG_ERR_ID.format(BAD_ACS_LAYER.format(rec_layer)))
                return
            
            
            save_obj["rec_layer"] = rec_layer
        
        
        mux_type = _validate_mux_type(jobj, errs)
        if len(errs) > 0:
            return
        
        
        save_obj["mux_type"] = mux_type
        
        
        writelog(MSG_INFO_ID.format(MPM_LOADING.format("pose_map")))
        
        
        pose_map = store.MASPoseMap.fromJSON(
            obj_based.pop("pose_map"),
            True,
            False,
            errs,
            warns
        )
        if pose_map is None or len(errs) > 0:
            writelogs(warns)
            return
        
        
        
        writelogs(warns)
        
        
        writelog(MSG_INFO_ID.format(MPM_SUCCESS.format("pose_map")))
        save_obj["pose_map"] = pose_map


    def _validate_fallbacks(jobj, save_obj, obj_based, errs, warns, infos):
        """
        Validates fallback related properties and pose map

        Props validated:
            - fallback
            - pose_map

        IN:
            jobj - json object to parse
            obj_based - dict of object-based items
                (contains pose_map)

        OUT:
            save_obj - dict to save data to
            errs - list to save error messages to
            warns - list to save warning messages to
            infos - list to save info messages to
        """
        
        _validate_params(
            jobj,
            save_obj,
            OPT_HC_SHARED_PARAM_NAMES,
            False,
            errs,
            MSG_ERR_ID
        )
        if len(errs) > 0:
            return
        
        
        fallback = save_obj.get("fallback", False)
        
        
        writelog(MSG_INFO_ID.format(MPM_LOADING.format("pose_map")))
        pose_map = store.MASPoseMap.fromJSON(
            obj_based.pop("pose_map"),
            False,
            fallback,
            errs,
            warns
        )
        if pose_map is None or len(errs) > 0:
            writelogs(warns)
            return
        
        
        
        writelogs(warns)
        
        
        writelog(MSG_INFO_ID.format(MPM_SUCCESS.format("pose_map")))
        save_obj["pose_map"] = pose_map


    def _validate_hair(jobj, save_obj, obj_based, errs, warns, infos):
        """
        Validates HAIR related properties

        Props validated:
            - unlock
        
        IN:
            jobj - json object to parse
            obj_based - dict of object-based items
                (contains split)

        OUT:
            save_obj - dict to save data to
            errs - list to save error messages to
            warns - list ot save warning messages to
            infos - list to save info messages to
        """
        _validate_params(
            jobj,
            save_obj,
            OPT_HAIR_PARAM_NAMES,
            False,
            errs,
            MSG_ERR_ID
        )
        if len(errs) > 0:
            return
        
        writelogs(warns)





























    def _validate_clothes(
            jobj,
            save_obj,
            obj_based,
            sp_name,
            dry_run,
            errs,
            warns,
            infos
        ):
        """
        Validates CLOTHES related properties

        Props validated:
            - hair_map
            - giftname

        IN:
            jobj - json object to parse
            obj_based - dict of objected-baesd items
                (contains split)
            sp_name - name of the clothes we are validating
            dry_run - true if we are dry running, False if not

        OUT:
            save_obj - dict to save data to
            errs - list to save error messages to
            warns - list to save warning messages to
            infos - list to save info messages to
        """
        
        _validate_params(
            jobj,
            save_obj,
            OPT_CLOTH_PARAM_NAMES,
            False,
            errs,
            MSG_ERR_ID
        )
        if len(errs) > 0:
            return
        
        
        if "hair_map" not in obj_based:
            
            return
        
        
        writelog(MSG_INFO_ID.format(HM_LOADING))
        hair_map = obj_based.pop("hair_map")
        
        for hair_key,hair_value in hair_map.iteritems():
            
            
            
            if _verify_str(hair_key):
                if (
                        not dry_run 
                        and hair_key != "all"
                        and hair_key not in HAIR_MAP
                    ):
                    _add_hair_to_verify(hair_key, hm_key_delayed_veri, sp_name)
            else:
                errs.append(MSG_ERR_IDD.format(HM_BAD_K_TYPE.format(
                    hair_key,
                    str,
                    type(hair_key)
                )))
            
            
            if _verify_str(hair_value):
                if hair_value == "custom":
                    errs.append(MSG_ERR_IDD.format(HM_FOUND_CUST))
                
                elif not dry_run and hair_value not in HAIR_MAP:
                    _add_hair_to_verify(
                        hair_value,
                        hm_val_delayed_veri,
                        sp_name
                    )
            
            else:
                errs.append(MSG_ERR_IDD.format(HM_BAD_V_TYPE.format(
                    hair_key,
                    str,
                    type(hair_value)
                )))
        
        
        if "all" not in hair_map:
            writelog(MSG_WARN_IDD.format(HM_MISS_ALL))
            hair_map["all"] = "def"
        
        
        if len(errs) > 0:
            return
        
        
        writelog(MSG_INFO_ID.format(HM_SUCCESS))
        save_obj["hair_map"] = hair_map


    def _validate_ex_props(jobj, save_obj, obj_based, errs, warns, infos):
        """
        Validates ex_props proprety

        Props validated:
            - ex_props

        IN:
            jobj - json object to parse
            obj_based - dict of object-based items
                (contains ex_props)

        OUT:
            save_obj - dict to save data to
            errs - list to save error messages to
            warns - list to save warning messages to
            infos - list to save info messages to
        """
        
        if "ex_props" not in obj_based:
            return
        
        
        writelog(MSG_INFO_ID.format(EP_LOADING))
        ex_props = obj_based.pop("ex_props")
        
        for ep_key,ep_val in ex_props.iteritems():
            if not _verify_str(ep_key):
                errs.append(MSG_ERR_IDD.format(EP_BAD_K_TYPE.format(
                    ep_key,
                    str,
                    type(ep_key)
                )))
            
            if not (
                    _verify_str(ep_val)
                    or _verify_bool(ep_val)
                    or _verify_int(ep_val)
                ):
                errs.append(MSG_ERR_IDD.format(EP_BAD_V_TYPE.format(
                    ep_key,
                    type(ep_val)
                )))
        
        
        if len(errs) > 0:
            return
        
        
        writelog(MSG_INFO_ID.format(EP_SUCCESS))
        save_obj["ex_props"] = ex_props


    def _validate_selectable(jobj, save_obj, obj_based, errs, warns, infos):
        """
        Validates selectable 

        Props validated:
            - select_info

        IN:
            jobj - json object to parse
            obj_based - dict of object-based items
                (contains select_info)

        OUT:
            save_obj - dict to save data to
            errs - list to save error messages to
            warns - list to save warning messages to
            infos - list to save info messages to

        RETURNS: dict of saved select info data
        """
        
        if "select_info" not in obj_based:
            return
        
        
        writelog(MSG_INFO_ID.format(SI_LOADING))
        select_info = obj_based.pop("select_info")
        
        
        _validate_params(
            select_info,
            save_obj,
            SEL_INFO_REQ_PARAM_NAMES,
            True,
            errs,
            MSG_ERR_IDD
        )
        if len(errs) > 0:
            return
        
        
        _validate_params(
            select_info,
            save_obj,
            SEL_INFO_OPT_PARAM_NAMES,
            False,
            errs,
            MSG_ERR_IDD
        )
        if len(errs) > 0:
            return
        
        
        if "hover_dlg" in select_info:
            
            _validate_iterstr(
                select_info,
                save_obj,
                "hover_dlg",
                False,
                True,
                errs,
                MSG_ERR_IDD
            )
            if len(errs) > 0:
                return
        
        if "select_dlg" in select_info:
            
            _validate_iterstr(
                select_info,
                save_obj,
                "select_dlg",
                False,
                True,
                errs,
                MSG_ERR_IDD
            )
            if len(errs) > 0:
                return
        
        
        for extra_prop in select_info:
            writelog(MSG_WARN_IDD.format(EXTRA_PROP.format(extra_prop)))
        
        
        writelog(MSG_INFO_ID.format(SI_SUCCESS))




    def addSpriteObject(filepath):
        """
        Adds a sprite object, given its json filepath

        NOTE: most exceptions logged
        NOTE: may raise exceptions

        IN:
            filepath - filepath to the JSON we want to load
        """
        dry_run = False
        jobj = None
        msgs_err = []
        msgs_warn = []
        msgs_info = []
        msgs_exprop = []
        obj_based_params = {}
        sp_obj_params = {}
        sel_params = {}
        unlock_hair = True
        giftname = None
        
        writelog("\n" + MSG_INFO.format(READING_FILE.format(filepath)))
        
        
        with open(filepath, "r") as jsonfile:
            jobj = json.load(jsonfile)
        
        
        if jobj is None:
            writelog(MSG_ERR.format(JSON_LOAD_FAILED.format(filepath)))
            return
        
        if DRY_RUN in jobj:
            jobj.pop(DRY_RUN)
            dry_run = True
        
        
        for jkey in jobj.keys():
            if jkey.startswith("__"):
                jobj.pop(jkey)
        
        
        
        
        
        
        
        
        
        
        
        
        sp_type = _validate_type(jobj)
        if sp_type is None:
            return
        
        
        _validate_params(
            jobj,
            sp_obj_params,
            REQ_SHARED_PARAM_NAMES,
            True,
            msgs_err,
            MSG_ERR_ID
        )
        if len(msgs_err) > 0:
            writelogs(msgs_err)
            return
        
        
        sp_name = sp_obj_params["name"]
        
        
        writelog(MSG_INFO.format(SP_LOADING.format(
            SP_STR.get(sp_type),
            sp_name
        )))
        
        
        
        if "pose_map" not in jobj:
            writelog(MSG_ERR_ID.format(REQ_MISS.format("pose_map")))
            return
        
        
        for param_name in OBJ_BASED_PARAM_NAMES:
            if param_name in jobj:
                obj_based_params[param_name] = jobj.pop(param_name)
        
        
        _validate_params(
            jobj,
            sp_obj_params,
            OPT_SHARED_PARAM_NAMES,
            False,
            msgs_err,
            MSG_ERR_ID
        )
        if len(msgs_err) > 0:
            writelogs(msgs_err)
            return
        
        
        if sp_type == SP_ACS:
            
            _validate_acs(
                jobj,
                sp_obj_params,
                obj_based_params,
                msgs_err,
                msgs_warn,
                msgs_info
            )
            if len(msgs_err) > 0:
                writelogs(msgs_err)
                return
        
        else:
            
            _validate_fallbacks(
                jobj,
                sp_obj_params,
                obj_based_params,
                msgs_err,
                msgs_warn,
                msgs_info
            )
            if len(msgs_err) > 0:
                writelogs(msgs_warn)
                writelogs(msgs_err)
                return
            
            if sp_type == SP_HAIR:
                _validate_hair(
                    jobj,
                    sp_obj_params,
                    obj_based_params,
                    msgs_err,
                    msgs_warn,
                    msgs_info
                )
                if len(msgs_err) > 0:
                    writelogs(msgs_warn)
                    writelogs(msgs_err)
                    return
            
            else:
                
                _validate_clothes(
                    jobj,
                    sp_obj_params,
                    obj_based_params,
                    sp_name,
                    dry_run,
                    msgs_err,
                    msgs_warn,
                    msgs_info
                )
                if len(msgs_err) > 0:
                    writelogs(msgs_warn)
                    writelogs(msgs_err)
                    return
        
        
        _validate_ex_props(
            jobj,
            sp_obj_params,
            obj_based_params,
            msgs_err,
            msgs_warn,
            msgs_info
        )
        if len(msgs_err) > 0:
            writelogs(msgs_warn)
            writelogs(msgs_err)
            return
        
        
        _validate_selectable(
            jobj,
            sel_params,
            obj_based_params,
            msgs_err,
            msgs_warn,
            msgs_info
        )
        if len(msgs_err) > 0:
            writelogs(msgs_warn)
            writelogs(msgs_err)
            return
        
        
        
        
        for extra_prop in jobj:
            writelog(MSG_WARN_ID.format(EXTRA_PROP.format(extra_prop)))
        
        
        if "unlock" in sp_obj_params:
            unlock_hair = sp_obj_params.pop("unlock")
            giftname = None
        
        elif "giftname" in sp_obj_params:
            giftname = sp_obj_params.pop("giftname")
            
            
            _check_giftname(giftname, sp_type, sp_name, msgs_err, MSG_ERR_ID)
            if len(msgs_err) > 0:
                writelogs(msgs_err)
                return
        
        elif sp_type != SP_HAIR:
            writelog(MSG_WARN_ID.format(NO_GIFT))
            giftname = None
        
        
        _process_progpoint(
            sp_type,
            sp_name,
            sp_obj_params,
            msgs_warn,
            msgs_info,
            "entry"
        )
        _process_progpoint(
            sp_type,
            sp_name,
            sp_obj_params,
            msgs_warn,
            msgs_info,
            "exit"
        )
        writelogs(msgs_info)
        writelogs(msgs_warn)
        
        
        try:
            if sp_type == SP_ACS:
                sp_obj = store.MASAccessory(**sp_obj_params)
                sms.init_acs(sp_obj)
                sel_obj_name = "acs"
            
            elif sp_type == SP_HAIR:
                sp_obj = store.MASHair(**sp_obj_params)
                sms.init_hair(sp_obj)
                sel_obj_name = "hair"
            
            else:
                
                sp_obj = store.MASClothes(**sp_obj_params)
                sms.init_clothes(sp_obj)
                sel_obj_name = "clothes"
        
        except Exception as e:
            
            writelog(MSG_ERR.format(e.message))
            return
        
        
        _test_loadables(sp_obj, msgs_err)
        if len(msgs_err) > 0:
            writelogs(msgs_err)
            _reset_sp_obj(sp_obj)
            return
        
        
        
        if len(sel_params) > 0:
            sel_params[sel_obj_name] = sp_obj
            
            try:
                if sp_type == SP_ACS:
                    sml.init_selectable_acs(**sel_params)
                
                elif sp_type == SP_HAIR:
                    sml.init_selectable_hair(**sel_params)
                    if unlock_hair:
                        sml.unlock_hair(sp_obj)
                
                else:
                    
                    sml.init_selectable_clothes(**sel_params)
            
            except Exception as e:
                
                writelog(MSG_ERR.format(e.message))
                
                
                _reset_sp_obj(sp_obj)
                return
        
        
        if giftname is not None and not dry_run:
            _init_giftname(giftname, sp_type, sp_name)
        
        
        if dry_run:
            _reset_sp_obj(sp_obj)
            writelog(MSG_INFO.format(SP_SUCCESS_DRY.format(
                SP_STR.get(sp_type),
                sp_name
            )))
        
        else:
            sp_obj.is_custom = True
            writelog(MSG_INFO.format(SP_SUCCESS.format(
                SP_STR.get(sp_type),
                sp_name
            )))


    def addSpriteObjects():
        """
        Adds sprite objects if we find any

        Also does delayed validation rules:
            - hair
        """
        json_files = sprite_station.getPackageList(".json")
        
        if len(json_files) < 1:
            return
        
        
        for j_obj in json_files:
            j_path = sprite_station.station + j_obj
            try:
                addSpriteObject(j_path)
            except Exception as e:
                writelog(MSG_ERR.format(
                    FILE_LOAD_FAILED.format(j_path, repr(e))
                ))


    def verifyHairs():
        """
        Verifies all hair items that we encountered
        """
        writelog("\n" + MSG_INFO.format(HM_VER_ALL))
        
        
        for hkey in hm_key_delayed_veri:
            if hkey not in HAIR_MAP:
                writelog(MSG_WARN_ID.format(HM_NO_KEY.format(
                    hkey,
                    hm_key_delayed_veri[hkey]
                )))
        
        
        for hval in hm_val_delayed_veri:
            if hval not in HAIR_MAP:
                sp_name_list = hm_val_delayed_veri[hval]
                writelog(MSG_WARN_ID.format(HM_NO_VAL.format(
                    hval,
                    sp_name_list
                )))
                
                
                for sp_name in sp_name_list:
                    _replace_hair_map(sp_name, hval)
        
        writelog(MSG_INFO.format(HM_VER_SUCCESS))


    def _addGift(giftname):
        """
        Adds the reaction for this gift, using the correct label depending on
        gift label existence.

        IN:
            giftname - giftname to add reaction for
        """
        namegift = giftname_map.get(giftname, None)
        if namegift is None:
            return
        
        gifttype, spname = namegift
        rlstr = SP_RL.get(gifttype,  None)
        if rlstr is None:
            return
        
        
        reaction_label = rlstr.format(spname)
        if renpy.has_label(reaction_label):
            store.addReaction(reaction_label, giftname, is_good=True)
            writelog(MSG_INFO_ID.format(GR_FOUND.format(
                SP_STR.get(gifttype),
                spname,
                giftname
            )))
        
        else:
            writelog(MSG_INFO_ID.format(GR_GEN.format(
                SP_STR.get(gifttype),
                spname,
                giftname
            )))


    def processGifts():
        """
        Processes giftnames that were loaded, adding/removing them from
        certain dicts.
        """
        writelog("\n" + MSG_INFO.format(GR_LOADING))
        
        frs_gifts = store.persistent._mas_filereacts_sprite_gifts
        msj_gifts = store.persistent._mas_sprites_json_gifted_sprites
        
        for giftname in frs_gifts.keys():
            if giftname in giftname_map:
                
                frs_gifts[giftname] = giftname_map[giftname]
            
            else:
                
                frs_gifts.pop(giftname)
        
        
        
        for giftname in giftname_map:
            if not giftname.startswith("__"):
                sp_data = giftname_map[giftname]
                
                
                if sp_data in msj_gifts:
                    
                    msj_gifts[sp_data] = giftname
                
                
                frs_gifts[giftname] = sp_data
                
                
                _addGift(giftname)
        
        writelog(MSG_INFO.format(GR_SUCCESS))


init 190 python in mas_sprites_json:



    addSpriteObjects()
    verifyHairs()


    processGifts()
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
