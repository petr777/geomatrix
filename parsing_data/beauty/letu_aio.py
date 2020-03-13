import aiohttp
import asyncio
import re

async def fetch(url, session, id_city):
    async with session.get(url) as resp:
        assert resp.status == 200
        JSON = await resp.json()
        print(JSON)


        return await resp.text()


async def bound_fetch(sem, url, session, id_city):
    async with sem:
        await fetch(url, session, id_city)


async def main():
    tasks = []
    sem = asyncio.Semaphore(5)
    async with aiohttp.ClientSession() as session:
        resp = await session.get('https://www.letu.ru/stores?')
        resp_text = await resp.text()
        id_session = re.findall(r"sessionStorage.setItem\('_dynSessConf',(.*)\);", resp_text)[0]
        id_session = id_session.replace("'", "").strip()
        for id_city in range(0, 80000):
            url = f"https://www.letu.ru/rest/model/atg/rest/geolocation/actor/GeolocationActor/setGeolocationInfo?pushSite=storeMobileRU&locale=ru_RU&cityId={id_city}&pushSite=storeMobileRU&_dynSessConf={id_session}"
            task = asyncio.ensure_future(bound_fetch(sem, url, session, id_city))
            tasks.append(task)
        responses = asyncio.gather(*tasks)
        await responses


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
