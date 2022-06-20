import typing as tp

import requests
import aiohttp
import asyncio

API_URL = 'https://pokeapi.co/api/v2/{api_name}?limit=100000&offset=0'


def log_print(msg: str) -> None:
    print(msg)


def check_count(api_name: str) -> int:
    response = requests.get(API_URL.format(api_name=api_name))
    return response.json().get('count', -1)


def get_urls(api_name: str) -> tp.List[str]:
    response = requests.get(API_URL.format(api_name=api_name))
    return [item['url'] for item in response.json().get('results', [])]


async def get_item(session: aiohttp.ClientSession, url: str, extract: tp.Callable[[tp.Dict], tp.Dict]) -> tp.Dict:
    async with session.get(url) as resp:
        data = await resp.json()
        return extract(data)


async def get_them_all(urls: tp.List[str], extract: tp.Callable[[tp.Dict], tp.Dict]) -> tp.List[tp.Dict]:
    connector = aiohttp.TCPConnector(limit=2)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [asyncio.ensure_future(get_item(session, url, extract)) for url in urls]
        items = await asyncio.gather(*tasks)
        return list(items)


def main(api_name: str, extract: tp.Callable[[tp.Dict], tp.Dict]) -> tp.List[tp.Dict]:
    return asyncio.run(get_them_all(get_urls(api_name), extract))


if __name__ == '__main__':
    print(check_count('generation'))
