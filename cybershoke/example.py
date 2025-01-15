import aiohttp, asyncio, config, json
from cybershoke import Category, Location, get_servers

with open(config.cookies_path, 'r', encoding='utf-8') as file:
    cookies_json = json.load(file)

COOKIE = {cookie['name']: cookie['value'] for cookie in cookies_json}

HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "uk-UA,uk;q=0.9",
    "Origin": "https://cybershoke.net",
    "Referer": "https://cybershoke.net/",
    "Sec-CH-UA": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
}

async def main():
    async with aiohttp.ClientSession(
        headers=HEADERS, 
        cookies=COOKIE
    ) as session:

        servers = await get_servers(
            session,
            category=Category.MEDIUM,
            location=Location.Germany
        )

        for server in servers:
            if server['players'] < server['maxplayers']:
                players = f"{server['players']}/{server['maxplayers']}"
                print(players, server['map'], f"connect {server['ip']}:{server['port']}")



asyncio.run(main())

"""
aiohttp 3.11.11
Brotli 1.1.0
"""