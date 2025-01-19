from aiohttp import ClientSession
from enum import Enum

class Location(Enum):
    Kyiv ="kiev"
    Warsaw = "warsaw"
    Germany = "germany"
    Finland = "finland"
    Sweden = "sweden"
    France = "france"
    Lithuania = "lithuania"
    London = "gb"
    Moscow = "moscow"
    Turkey = "turkey"
    Georgia = "georgia"

class Mode(Enum):
    _2X2 = "2X2"
    _5X5 = "5X5"
    AIMDM = "AIMDM"
    ARENA = "ARENA"
    AWP = "AWP"
    AWPDM = "AWPDM"
    BHOP = "BHOP"
    CLUTCH = "CLUTCH"
    DEATHRUN = "DEATHRUN"
    DM = "DM"
    DUELS = "DUELS"
    DUELS_TWO_X_TWO = "DUELS2X2"
    EXECUTE = "EXECUTE"
    HNS = "HNS"
    HSDM = "HSDM"
    KZ = "KZ"
    MANIAC = "MANIAC"
    MINIGAMES = "MINIGAMES"
    MULTICFGDM = "MULTICFGDM"
    PISTOLDM = "PISTOLDM"
    PISTOLRETAKE = "PISTOLRETAKE"
    PUBLIC = "PUBLIC"
    RETAKE = "RETAKE"
    RETAKECARDS = "RETAKECARDS"
    SURF = "SURF"
    SURFCOMBAT = "SURFCOMBAT"

class Category(Enum):
    # DM | DEATHRUN
    EASY = "EASY" # yes MANIAC
    MEDIUM = "MEDIUM" # not DEATHRUN | yes PISTOLDM

    # DUELS | DUELS2X2 | PUBLIC
    ARENA_MAPS = "ARENA MAPS" # not DUELS2X2, PUBLIC
    ONLY_DUST2 = "ONLY DUST2"
    ONLY_MIRAGE = "ONLY MIRAGE"
    ALL_MAPS = "ALL MAPS"

    # AWP
    AWP_CANNONS = "AWP CANNONS"
    ONLY_AWP_LEGO_2 = "ONLY AWP LEGO 2"

    # BHOP
    TIER_1_2_EASY = "TIER 1-2 - EASY" # yes SURF
    TIER_3_4_MEDIUM = "TIER 3-4 - MEDIUM"

    # CLUTCH
    _2VS5 = "2VS5"
    _1VS3 = "1VS3"

    # EXECUTE | RETAKE | RETAKECARDS
    _9_SLOTS = "9 SLOTS" # not RETAKECARDS
    _7_SLOTS = "7 SLOTS" 

    # HNS
    RULES = "RULES"
    TRAINING = "TRAINING"

    # KZ
    TIER_1_2 = "TIER 1-2"
    TIER_3_4 = "TIER 3-4"
    TIER_5_6 = "TIER 5-6"

    # MANIAC
    CLASSIC = "CLASSIC"

    # MINIGAMES
    FUN_MAPS = "FUN MAPS"

    # PISTOLDM
    HSDM = "HSDM"

    # SURF
    TIER_1_BEGINNER = "TIER 1 - BEGINNER"
    TIER_3_5_HARD = "TIER 3-5 - HARD"

    mode_withot_category = [
        Mode._2X2,  Mode._5X5, Mode.AIMDM, Mode.ARENA,
        Mode.AWPDM, Mode.HSDM, Mode.MULTICFGDM, 
        Mode.PISTOLRETAKE, Mode.SURFCOMBAT
    ]

class Map(Enum):
    DE_MIRAGE_FPS = "de_mirage_fps"
    DE_MIRAGE = "de_mirage"
    DE_DUST2 = "de_dust2"
    DE_ANUBIS = "de_anubis"
    DE_INFERNO = "de_inferno"
    DE_ANCIENT = "de_ancient"

async def get_servers(
        session: ClientSession, 
        category: Category=Category.EASY, 
        location: Location=None, 
        mode: Mode=Mode.DM,
        map: Map=Map.DE_MIRAGE,
        people_now: list[int] = None,
        max_people_on_server: int = None
    ):
    url = f"https://api.cybershoke.net/api/v2/main/data"

    async with session.get(url) as response:
        data = await response.json()

        servers = data['data']['modules']['servers']['data']['servers']['2']

        if mode.value in servers:

            if category.value in servers[mode.value] or mode in Category.mode_withot_category:

                if mode in Category.mode_withot_category: category.value = ""
                    
                servers = servers[mode.value][category.value]
                ok_servers = []

                for server in servers:

                    if location:
                        if server['location'] != location.value: continue

                    if map:
                        if server['map'] != map.value: continue

                    if people_now and len(people_now)==2:
                        if \
                            server['players'] >= people_now[0] \
                            and\
                            server['players'] <= people_now[1]: pass
                        else: continue

                    if max_people_on_server:
                        if server['maxplayers'] < max_people_on_server: continue
                                
                    ok_servers.append(server)

                return ok_servers
            return "This mode does not have such a category"
        return "such mode not found"