import aiohttp
import asyncio
import time
import math
import re

from sqlite_db import load_one_people, sql_start

SWAPI_PEOPLE_URL = 'https://swapi.dev/api/people/'


async def call_url(url, param=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=param) as response:
            return await response.json()


async def load_all_people():
    one_page = await call_url(SWAPI_PEOPLE_URL)
    list_corutina = []
    count_pages = math.ceil(one_page['count'] / len(one_page['results']))
    for page in range(1, count_pages + 1):
        corutina = call_url(f'{SWAPI_PEOPLE_URL}/', f'page={page}')
        list_corutina.append(corutina)
    api_responses = await asyncio.gather(*list_corutina)
    return api_responses


async def load_additional_data_people(one_page):
    data = ['films', 'species', 'starships', 'vehicles']
    people_list = []
    for people in one_page['results']:
        people_id = re.search(fr"https://swapi.dev/api/people/(\w*)/", people['url'])
        people['id'] = int(people_id.group(1))
        for i in data:
            if len(people[i]) > 0:
                corutina_film = []
                for url_film in people[i]:
                    corutina = call_url(url_film)
                    corutina_film.append(corutina)
                api_responses = await asyncio.gather(*corutina_film)
                people[i] = ''
                for resp in api_responses:
                    if i == 'films':
                        people[i] += resp['title'] + ', '
                    else:
                        people[i] += resp['name'] + ', '
            else:
                people[i] = 'Null'

        people_list.append(people)
    return people_list


async def loading_additional_data(people_list):
    corutina_list = []
    for people in people_list:
        corutina = load_additional_data_people(people)
        corutina_list.append(corutina)
    responses = await asyncio.gather(*corutina_list)
    return responses


async def load_data_in_db(list_data):
    count = 0
    corutina_list = []
    for page in list_data:
        for people in page:
            count += 1
            corutina = await load_one_people(people)

    return count


async def main():
    list_people = await load_all_people()
    print('Получен список всех персонажей')
    data = await loading_additional_data(list_people)
    print('Загружены дополнительные данные  ')
    db = await load_data_in_db(data)
    print(f'сохранено в базу данных:{db} ')


if __name__ == '__main__':
    start = time.time()
    sql_start()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
    finish = time.time() - start
    print(finish)
