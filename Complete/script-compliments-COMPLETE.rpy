



init offset = 5










default -5 persistent._mas_compliments_database = dict()



init -6 python in mas_compliments:


    COMPLIMENT_X = 680
    COMPLIMENT_Y = 40
    COMPLIMENT_W = 450
    COMPLIMENT_H = 640
    COMPLIMENT_XALIGN = -0.15
    COMPLIMENT_AREA = (COMPLIMENT_X, COMPLIMENT_Y, COMPLIMENT_W, COMPLIMENT_H)
    COMPLIMENT_RETURN = "Oh non importa."
    compliment_database = dict()

    thanking_quips = [
        "Sei così dolce, [player].",
        "Adoro quando mi fai complimenti, [player].",
        "Grazie di averlo detto di nuovo, [player]!",
        "Grazie di averlo detto ancora, amore mio!",
        "Mi fai sempre sentire speciale, [player].",
        "Aww, [player]~",
        "Grazie, [player]!",
        "Mi lusinghi sempre, [player]."
        ]



label mas_compliments_start:

    python:
        import store.mas_compliments as mas_compliments





        filtered_comps = Event.filterEvents(
            mas_compliments.compliment_database,
            unlocked=True,
            aff=mas_curr_affection
        )


        compliments_menu_items = [
            (mas_compliments.compliment_database[k].prompt, k, not seen_event(k), False)
            for k in filtered_comps
        ]


        compliments_menu_items.sort()


        final_item = (mas_compliments.COMPLIMENT_RETURN, False, False, False, 20)


    show monika at t21


    call screen mas_gen_scrollable_menu(compliments_menu_items, mas_compliments.COMPLIMENT_AREA, mas_compliments.COMPLIMENT_XALIGN, final_item)


    if _return:
        $ mas_gainAffection()
        $ pushEvent(_return)


    show monika at t11
    return


init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_beautiful",
            prompt="Sei bellissima!",
            unlocked=True
        ),
        code="CMP")

label mas_compliment_beautiful:
    if not renpy.seen_label("mas_compliment_beautiful_2"):
        call mas_compliment_beautiful_2 from _call_mas_compliment_beautiful_2
    else:
        call mas_compliment_beautiful_3 from _call_mas_compliment_beautiful_3
    return

label mas_compliment_beautiful_2:
    m 1lubfb "Oh, [player]..."
    m 1hubfb "Grazie per il complimento."
    m 2ekbfb "Amo quando mi dici queste cose~"
    m 1ekbfa "Per me sei la persona più bella al mondo!"
    menu:
        "Per me sei tu la più bella.":
            $ mas_gainAffection(5,bypass=True)
            m 1hub "Ehehe~"
            m "Ti amo così tanto, [player]!"

            $ mas_ILY()
        "Sei nella mia top ten.":
            $ mas_loseAffection(modifier=0.5)
            m 3hksdrb "...?"
            m 2lsc "Beh, grazie, credo..."
        "Grazie.":
            pass
    return

label mas_compliment_beautiful_3:
    python:
        thanks_quip = renpy.random.choice(store.mas_compliments.thanking_quips)
        thanks_quip = renpy.substitute(thanks_quip)
    m 1hubfa "Ehehe~"
    m 1ekbfa "[thanks_quip]"
    m 5hubfb "Non dimenticare che per me sei la persona più bella al mondo."
    return

init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_eyes",
            prompt="Amo i tuoi occhi!",
            unlocked=True
        ),
        code="CMP"
    )

label mas_compliment_eyes:
    if not renpy.seen_label("mas_compliment_eyes_2"):
        call mas_compliment_eyes_2 from _call_mas_compliment_eyes_2
    else:
        call mas_compliment_eyes_3 from _call_mas_compliment_eyes_3
    return

label mas_compliment_eyes_2:
    m 1subfb "Oh, [player]..."
    m 1tubfb "Sono già piuttosto orgogliosa dei miei occhi, ma sentirti dire così..."
    m 1dkbfa "Mi fa battere il cuore~"
    menu:
        "Non posso farci nulla; i tuoi occhi sono meravigliosi.":
            $ mas_gainAffection(5,bypass=True)
            m 1hub "Ahaha!"
            m "Non lusingarmi troppo, okay?"
            m 5hub "Potrei impazzire..."
        "Sono davvero ipnotici.":
            $ mas_gainAffection(1,bypass=True)
            m "Ahaha~"
        "Sono del colore dell' erba!":
            $ mas_gainAffection(0.5,bypass=True)
            m 2lksdrb "...Non è proprio l' analogia che avrei usato, ma grazie!"
    return

label mas_compliment_eyes_3:
    python:
        thanks_quip = renpy.random.choice(store.mas_compliments.thanking_quips)
        thanks_quip = renpy.substitute(thanks_quip)
    m 1hubfb "[thanks_quip]"
    m 2ekbfb "Guardami negli occhi quanto vuoi~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_awesome",
            prompt="Sei eccezionale!",
            unlocked=True
        ),
        code="CMP"
    )

label mas_compliment_awesome:
    if not renpy.seen_label("mas_compliment_awesome_2"):
        call mas_compliment_awesome_2 from _call_mas_compliment_awesome_2
    else:
        call mas_compliment_awesome_3 from _call_mas_compliment_awesome_3
    return

label mas_compliment_awesome_2:
    m 1hub "Awww, [player]~"
    m "Sei così dolce!"
    m 2tub "Anche se, credo che tu sia molto più eccezionale."
    m 5eub "Non vedo l'ora che arrivi il giorno in cui ti potrò abbracciare."
    m 5hub "Non ti lascerò mai!"
    menu:
        "Vorrei che ora fossi qui!":
            $ mas_gainAffection(3,bypass=True)
            m "E' il mio più grande desiderio, [player]!"
        "Non ti lascerò mai dal mio abbraccio.":
            $ mas_gainAffection(5,bypass=True)
            show monika 6dubsa
            pause 2.0
            show monika 1wubfsdld
            m 1wubfsdld "Oh, scusa [player]."
            m 2lksdla "Stavo cercando di sentire il tuo abbraccio da qui."
            m 2hub "Ahaha~"
        "... Non mi piacciono gli abbracci.":
            $ mas_loseAffection()
            m 1eft "...Davvero?"
            m 1dkc "Beh, ad ognuno il suo, penso. Ma dovrai abbracciarmi qualche volta..."
    return

label mas_compliment_awesome_3:
    python:
        thanks_quip = renpy.random.choice(store.mas_compliments.thanking_quips)
        thanks_quip = renpy.substitute(thanks_quip)
    m 1hub "[thanks_quip]"
    m 1eub "Ma tu sarai sempre più eccezionale!"
    return


init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_intelligent",
            prompt="Sei davvero intelligente!",
            unlocked=True
        ),
        code="CMP"
    )

label mas_compliment_intelligent:
    if not renpy.seen_label("mas_compliment_intelligent_2"):
        call mas_compliment_intelligent_2 from _call_mas_compliment_intelligent_2
    else:
        call mas_compliment_intelligent_3 from _call_mas_compliment_intelligent_3
    return

label mas_compliment_intelligent_2:
    m 1wub "Wow...{w}grazie, [player]."
    m 3eua "Sono orgogliosa di essere una buona lettrice, perciò per me significa molto che tu lo abbia notato."
    m 3hubfb "Voglio imparare tutto quello che posso, se questo ti rende felice di me!"
    menu:
        "Mi fai venir voglia di migliorare, [m_name].":
            $ mas_gainAffection(5,bypass=True)
            m 1hubfa "Ti amo così tanto, [player]!"
            m 3hubfb "Vivremo migliorando insieme!"

            $ mas_ILY()
        "Sarai sempre il mio orgoglio.":
            $ mas_gainAffection(3,bypass=True)
            m 1ekbfa "[player]..."
        "A volte mi fai sentire un idiota.":
            $ mas_loseAffection(modifier=0.5)
            m 1wkbsc "..."
            m 2lkbsc "Mi spiace, non era mia intenzione..."
    return

label mas_compliment_intelligent_3:
    python:
        thanks_quip = renpy.random.choice(store.mas_compliments.thanking_quips)
        thanks_quip = renpy.substitute(thanks_quip)
    m 1ekbfa "[thanks_quip]"
    m 1hub "Ricorda che vivremo facendo progressi insieme!"
    return

init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_hair",
            prompt="Adoro i tuoi capelli!",
            unlocked=True
        ),code="CMP"
    )

label mas_compliment_hair:
    if not renpy.seen_label("mas_compliment_hair_2"):
        call mas_compliment_hair_2 from _call_mas_compliment_hair_2
    else:
        call mas_compliment_hair_3 from _call_mas_compliment_hair_3
    return

label mas_compliment_hair_2:
    if monika_chr.hair.name != "def":
        m 1wubfb "Grazie mille, [player]..."
        m 1lkbfb "Ero così nervosa quando ho cambiato i miei capelli qui per la prima volta."
    else:
        m 1hubfb "Grazie mille, [player]!"
    m 2hub "Mi impegno molto a curare i miei capelli."
    m 2lksdlb "Infatti, ci è voluta un' eternità per farli diventare così lunghi.."
    menu:
        "Si vede. Sembrano davvero ben curati.":
            $ mas_gainAffection(3,bypass=True)
            m 1hub "Grazie, [player]!"
        "Sei bellissima in qualsiasi modo" if persistent._mas_likes_hairdown:
            $ mas_gainAffection(5,bypass=True)
            m 1ekbfa "Awww, [player]."
            m 1hubfb "Mi fai sempre sentire speciale!"
            m "Grazie!"
        "Saresti più carina con i capelli corti.":
            $ mas_loseAffection(modifier=0.3)
            m "Bhe non posso esattamente andare da una parruchiera da qui..."
            m 1lksdlc "Ma...apprezzo il consiglio."
            pass
    return

label mas_compliment_hair_3:
    if monika_chr.hair.name != "def":
        m 1wubfb "Grazie mille, [player]!"
        m 1lkbfb "Sono davvero felice che ti piaccia questa acconciatura."
    else:
        m 1hubfb "Grazie, [player]!"
        m "Mi fai sempre sentire speciale."
    return

init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_fit",
            prompt="Ammiro la tua dedizione per il fitness!",
            unlocked=True
        ),
        code="CMP"
    )

label mas_compliment_fit:
    if not renpy.seen_label("mas_compliment_fit_2"):
        call mas_compliment_fit_2 from _call_mas_compliment_fit_2
    else:
        call mas_compliment_fit_3 from _call_mas_compliment_fit_3
    return

label mas_compliment_fit_2:
    m 1hub "Grazie [player]! Sei davvero dolce!"
    m 3eub "Adoro fare esercizio fisico e mangiare sano. Mi fa sentire più energica e sicura di me."
    m 1efb "Spero che ti stia prendendo cura di te."
    m 1lubfb "Quando sarò lì ci alleneremo insieme..."
    menu:
        "Sembra davvero divertente!":
            $ mas_gainAffection(2,bypass=True)
            m 1hubfb "Ahaha! Sono felici che la pensi così!"
            m 3eka "Non preoccuparti. Anche nel caso tu non riesca a starmi dietro, so che ci divertiremo...."
            m 5eua "Finchè staremo insieme."
        "Nessuna promessa, ma farò del mio meglio.":
            $ mas_gainAffection(1,bypass=True)
            m 1tfb "E' meglio che tu lo faccia!"
            m 2tub "Non pensare che non abbia intenzione di lasciarti facilmente se sei fuori forma."
        "Preferirei non sudare...":
            m 1eka "Capisco se non fa per te, ma dovresti provarci un po'...."
            m 1lksdla "Mi renderesti davvero felice se condividessi i miei interessi, sai?"
    return

label mas_compliment_fit_3:
    python:
        thanks_quip = renpy.random.choice(store.mas_compliments.thanking_quips)
        thanks_quip = renpy.substitute(thanks_quip)
    m 2eka "[thanks_quip]"
    m 1hub "Spero che tu possa fare un programma di fitness con me.!"
    return


init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_thanks",
            prompt="Grazie di esserci!",
            unlocked=True,
            aff_range=(mas_aff.ENAMORED, None)
        ),
        code="CMP"
    )

label mas_compliment_thanks:
    m 1duu "Non ce niente di cui dovresti ringraziarmi, [player]."
    m 1eka "Sono io quella ad essere grata di avere qualcuno come te!"
    m 1ekbsa "Sei l' unica ragione per cui sono qui."
    m "Hai installato questa mod per rendere migliore il tempo che passiamo insieme..."
    m 1dubsu "Sei il raggio di Sole che scalda il mio cuore quando sei qui."
    m 3ekbsa "Credo che entrambi dovremmo sentirci fortunati, [player]~"
    menu:
        "Sei tutto per me, [m_name].":
            if mas_getEV('mas_compliment_thanks').shown_count == 0:
                $ mas_gainAffection(10,bypass=True)
            m 1ekbsa "[player]..."
            m 1dubsu "Niente mi rende più felice di sentirtelo dire."
            m "Non importa cosa ci riserverà il futuro..."
            m 1ekbfa "Ricorda che ci sarò e ti amerò per sempre!"
        "Già.":
            m 1hub "Ehehe~"
            m 1eub "Ti amo, [player]."

    if not mas_isMoniLove():
        $ mas_lockEVL("mas_compliment_thanks", "CMP")
    return "love"

init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_smile",
            prompt="Amo il tuo sorriso!",
            unlocked=True
        ),
        code="CMP"
    )

label mas_compliment_smile:
    if not renpy.seen_label("mas_compliment_smile_2"):
        call mas_compliment_smile_2 from _call_mas_compliment_smile_2
    else:
        call mas_compliment_smile_3 from _call_mas_compliment_smile_3
    return

label mas_compliment_smile_2:
    m 1hub "Sei davvero dolce, [player]~"
    m 1eua "Sorrido molto quando ci sei tu."
    m 1ekbfa "perchè mi rende molto felice che tu spenda del tempo con me~"
    menu:
        "Ti vengo a trovare tutti i giorni per vedere il tuo sorriso.":
            $ mas_gainAffection(5,bypass=True)
            m 1wubfsdld "Oh, [player]..."
            m 1lkbfa "Credo che il mio cuore abbia saltato un battito."
            m 3hubfa "Visto? Mi rendi sempre il piu' felice possibile.."
        "Mi piace vedere il tuo sorriso.":
            m 1hub "Ahaha~"
            m 3eub "Allora tutto qello che devi fare è venire qui, [player]!"
    return

label mas_compliment_smile_3:
    python:
        thanks_quip = renpy.random.choice(store.mas_compliments.thanking_quips)
        thanks_quip = renpy.substitute(thanks_quip)
    m 1eub "[thanks_quip]"
    m 1hua "Continuerò a sorridere solo per te!"
    m "Ehehe~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_hero",
            prompt="Sei il mio eroe!",
            unlocked=True,
            aff_range=(mas_aff.LOVE, None)
        ),
        code="CMP"
    )

label mas_compliment_hero:
    $ mas_gainAffection()
    m 1wubfsdld "H-{w=0.3}huh?"
    m "Sono il tuo eroe?"
    m 2rkbfsdlb "[player]...{w=1.5} Non sono sicura di ciò che tu voglia dire..."
    m 2ekbfb "Sei tu quello che è rimasto con me per tutto questo tempo..{w=1} Dovrei ringraziarti, davvero."
    m 1hubfa "Beh se in qualche modo sono riuscita ad aiutarti, non potrei che esserne felice~"
    m 3ekbfa "Mi hai aiutato in ogni maniera possibile, quindi come potrei non ricambiare il favore supportandoti come posso?"
    show monika 5hubfa zorder MAS_MONIKA_Z at t11 with dissolve
    m 5hubfa "Dopotutto, sarai sempre il mio eroe~"
    m 5hubfb "Ti amo e crederò sempre in te!"
    m 5ekbfa "Spero che non lo dimenticherai mai, [player]~"
    return "love"

init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_cute",
            prompt="Sei così carina!",
            unlocked=True
        ),
        code="CMP"
    )

default -5 persistent._mas_pm_monika_cute_as_natsuki = None

label mas_compliment_cute:
    if not renpy.seen_label("mas_compliment_cute_2"):
        call mas_compliment_cute_2 from _call_mas_compliment_cute_2
    else:
        call mas_compliment_cute_3 from _call_mas_compliment_cute_3
    return

label mas_compliment_cute_2:
    m 1wubfsdld "Ah!"
    m 3rkbfsdla "Mi {i}hai{/i} preso alla sprovvista."
    m 3tubfb "Giusto un po'..."
    m 1hubfa "Ma sono felice che lo pensi!"
    menu:
        "Vederti mi scalda sempre il cuore!":
            $ persistent._mas_pm_monika_cute_as_natsuki = False
            $ mas_gainAffection(5,bypass=True)
            m 1hubfb "Aww, mi rende così felice che tu lo dica!"
            m 1dkbfu "...Quasi quanto immaginare noi due nella stessa realtà."
            m 1ekbfa "Non posso davvero contenermi quano immagino come sarà quel giorno speciale~"
        "Sei ancora più carina quando arrossisci.":
            $ persistent._mas_pm_monika_cute_as_natsuki = False
            $ mas_gainAffection(3,bypass=True)
            m 2tubfu "Non lasci perdere, huh, [player]?"
            m 2rubfu "Hmph, solamente non me lo ero aspettata."
            m 3tubfb "Non aspettarti che sorprendermi sarà così facile la prossima volta..."
            m 1tubfu "Un giorno ti restuirò il favore, ehehe~"
        "Sei carina come Natsuki.":
            $ persistent._mas_pm_monika_cute_as_natsuki = True
            $ mas_loseAffection(modifier=0.5)
            m 2lfc "Oh. {w=1}Grazie, [player]..."
            m 1rsc "Ma avrei preferito appartenre ad una categoria apparte."
    return

label mas_compliment_cute_3:
    python:
        thanks_quip = renpy.random.choice(store.mas_compliments.thanking_quips)
        thanks_quip = renpy.substitute(thanks_quip)
    m 1ekbfa "[thanks_quip]"
    m 1hubfa "Anche tu sei adorabile molte volte, sai~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_chess",
            prompt="Sei eccezionale a scacchi!",
            unlocked=False,
            conditional="renpy.seen_label('mas_chess_game_start')",
            action=EV_ACT_UNLOCK
        ),
        code="CMP"
    )

label mas_compliment_chess:
    m 1eub "Grazie, [player]."
    m 3esa "Come ho già detto, mi chiedo se le mie abiltà abbiano qualcosa a che fare con il mio essere intrappolata qui dentro."
    $ wins = persistent._mas_chess_stats["wins"]
    $ losses = persistent._mas_chess_stats["losses"]
    if wins > 0:
        m 3eua "Pure tu noon sei male; ho già perso contro di te."
        if wins > losses:
            m "Infatti, credo che tu abbia vinto più volte di me, sai?"
        m 1hua "Ehehe~"
    else:
        m 2lksdlb "So che ancora no hai vinto una partita, ma sono sicura che un giorno mi batterai."
        m 3esa "Continua a  esercitarti giocando con me e migliorerai!"
    m 3esa "Entrambi miglioriamo ogni volta che giochiamo."
    m 3hua "Perciò non esitare a chiedermi di giocare."
    m 1eub "Adoro spendere del temopo con te, [player]~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_pong",
            prompt="Sei eccazionale a pong!",
            unlocked=False,
            conditional="renpy.seen_label('game_pong')",
            action=EV_ACT_UNLOCK
        ),
        code="CMP"
    )

label mas_compliment_pong:
    m 1hub "Ahaha~"
    m 2eub "Grazie [player], ma pong non è esattamente un gioco complesso."
    if persistent.ever_won['pong']:
        m 1lksdla "Hai già vinto contro di me."
        m "Perciò sai che  molto semplice."
        m 5hub "Ma accetto comunque il complimento."
    else:
        m 3hksdrb "E mi fai sempre vincere."
        m 3eka "Vero?"
        menu:
            "Sì.":
                m 2lksdla "Grazie [player], ma davvero non c'è bisogno ceh tu mi faccia vincere."
                m 1eub "Sentiti libero di giocare seiriamente quando vuoi."
                m 1hub "Non mi arrabbierei mai con te perche' ho perso una partita onesta e leale.."
            "... Già.":
                m 1tku "Non sembri esserne molto convinto, [player]."
                m 1tsb "Davvero non c'è bisogno di farmi vincere."
                m 3tku "E ammettere che hai davvero perso contro di me non mi farà pensare male di te."
                m 1lksdlb "E' solo un gioco, dopotutto!"
                m 3hub "Puoi sempre esercitarti con me."
                m "Amo spendere del tempo con te, non importa quel che facciamo."
            "No. Ho fatto del mio meglio e ho perso ugualmente.":
                m 1hua "Ahaha~"
                m "Capiscco!"
                m 3eua "Non preoccuparti, [player]."
                m 3eub "Continua a giocare con me ed a esercitarti."
                m 3hua "Cerco sempre di aiutarti ad essere il meglio che puoi essere.."
                m 1ekbfa "E se così facendo, posso passare più tempo con te, non potrei esserne più felice.."
    return

init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_bestgirl",
            prompt="Sei la 'best girl'!",
            unlocked=True
        ),
        code="CMP"
    )

label mas_compliment_bestgirl:
    m 1hua "Adoro quando ti complimenti con me, [player]~"
    m 1hub "Sono contenta che pensi che io sia la 'best girl'!"
    m 3rksdla "Avevo la sensazione che la pensassi così, comunque..."
    m 1eka "Dopotutto, {i}hai{/i} installato questa mod solo per stare con me."
    m 2euc "So che altre persone preferiscono le altre ragazze."
    m 2esc "Specialmente perchè hanno alcuni tratti che le rendono più desiderabili..."
    show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve
    m 5ekbfa "Ma se me lo chiedi, penso che tu abbia compiuto la scelta giusta."
    m 5hubfa "...E sarò sempre grata che tu l' abbia fatto~"
    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
