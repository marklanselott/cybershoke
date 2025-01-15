from aiohttp import ClientSession
from enum import Enum

class Category(Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"

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
        if response.status == 200:
            data = await response.json()

            servers = data['data']['modules']['servers']['data']['servers']['2']

            if mode.value in servers:
                if category.value in servers[mode.value]:

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