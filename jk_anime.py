#!/usr/bin/env python3

from zippyshare_downloader import extract_info, extract_info_coro
from bs4 import BeautifulSoup
import requests
from pprint import pprint


SESSION = requests.Session()
HEADERS = {'user-agent': 'Mozilla/5.0'}


def search_anime(query):
    """
    Returns the first 5 dictionaries on a list of matches.
    """
    query_url = f'https://jkanime.net/ajax/ajax_search/?q={query}'
    response = SESSION.get(query_url, headers=HEADERS)
    if response.status_code == 200:
        query_result = response.json()['animes']
    else:
        print('Connection Error')
        return 1
    return query_result


def select_anime(anime_list):
    """
    Prints list of anime names and ask you to select one.
    """
    for i in range(len(anime_list)):
        print(f'{i+1}. {anime_list[i]["title"]}')

    number = input(f'Elige un anime[1/{len(anime_list)}]: ')
    number = int(number)
    return anime_list[number-1]


def get_ep_num(anime_slug):
    """
    Returns the number of episodes of an anime.
    """
    anime_url = f'https://jkanime.net/{anime_slug}'
    response = SESSION.get(anime_url, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')

    details_container = soup.find('div', {'class': 'anime__details__widget'})
    details = details_container.findChildren('li')
    return details[3].contents[1].strip()


def select_ep(anime):
    ep_num = get_ep_num(anime['slug'])
    print(f'\n{anime["title"]} ({ep_num})')
    while True:
        try:
            ep = int(input('Elige un episodio: '))
        except Exception as e:
            print("Tienes que escribir un number")
            continue
        else:
            break
    print()
    return ep


def get_link(anime_slug, ep):
    """
    Returns the Zippyshare download link of an specific episode.
    """
    url = f'https://jkanime.net/{anime_slug}/{ep}/'
    response = SESSION.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    for link in soup.findAll('a'):
        if link.parent.name == 'td':
            return link["href"]


def main():
    # Search for anime
    query = input('Buscar Anime: ')
    anime_list = search_anime(query)
    anime = select_anime(anime_list)
    # Select episode
    ep = select_ep(anime)
    # Print link
    link = get_link(anime['slug'], ep)
    if link is None:
        print('Enlace de descarga no disponible')
    elif 'zippyshare' in link:
        extract_info(link)
    else:
        print('El enlace no es de Zippyshare')


if __name__ == '__main__':
    main()
