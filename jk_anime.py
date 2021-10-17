#!/usr/bin/env python3

from zippyshare_downloader import extract_info, extract_info_coro
from bs4 import BeautifulSoup
import requests
from pprint import pprint
import enquiries


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
    anime_dict = {}
    for anime in query_result:
        anime_dict[anime['title']] = {
            'title': anime['title'],
            'image': anime['image'],
            'type': anime['type'],
            'link': f"https://jkanime.net/{anime['slug']}/",
            'ep': get_ep_num(f"https://jkanime.net/{anime['slug']}/")
        }
    return anime_dict


def select_anime(anime_dict):
    """
    Prints list of anime names and ask you to select one.
    """
    choice = enquiries.choose('Selecciona un anime: ', anime_dict.keys())
    return anime_dict[choice]


def get_ep_num(anime_url):
    """
    Returns the number of episodes of an anime.
    """
    response = SESSION.get(anime_url, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')

    details_container = soup.find('div', {'class': 'anime__details__widget'})
    details = details_container.findChildren('li')
    return details[3].contents[1].strip()


def select_ep(anime):
    """
    Asks you to select one episode
    """
    ep_num = get_ep_num(anime['link'])
    print(f'\n{anime["title"]} ({anime["ep"]})')
    while True:
        try:
            ep = int(input('Elige un episodio: '))
        except Exception as e:
            print("Tienes que escribir un número")
            continue
        else:
            break
    return str(ep)


def get_link(url):
    """
    Returns the Zippyshare download link of an specific episode.
    """
    response = SESSION.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    for link in soup.findAll('a'):
        if link.parent.name == 'td':
            return link["href"]


def main():
    # Search for anime
    query = input('Buscar Anime: ')
    anime_dict = search_anime(query)
    anime = select_anime(anime_dict)

    # Select episode
    ep = select_ep(anime)

    # Get download link
    url = anime['link'] + ep
    link = get_link(url)
    if link is None:
        print('Noy hay un enlace de descarga no disponible')
    elif 'zippyshare' in link:
        extract_info(link)
    else:
        print('El enlace no es de Zippyshare. Descargalo en tu navegador')
        print(link)


if __name__ == '__main__':
    main()
