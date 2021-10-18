#!/usr/bin/env python3

from zippyshare_downloader import extract_info
from bs4 import BeautifulSoup
import requests
import enquiries


SESSION = requests.Session()
HEADERS = {'user-agent': 'Mozilla/5.0'}


def search_anime(query):
    """
    Returns the first 5 dictionaries on a list of matches.
    """
    query_url = f'https://jkanime.net/ajax/ajax_search/?q={query}'
    try:
        response = SESSION.get(query_url, headers=HEADERS)
    except Exception as e:
        print('Error de conección')
        exit()

    if response.status_code == 200:
        query_result = response.json()['animes']
        if not query_result:
            print('No se encuentraron resultados')
            exit()
    else:
        print('Error de conección')
        exit()

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
    print(f'{anime["title"]} ({anime["ep"]})')
    while True:
        try:
            ep = int(input('Elige un episodio: '))
        except Exception as e:
            print("Tienes que escribir un número")
            continue
        else:
            break
    return str(ep)


def get_links(url):
    """
    Returns the Zippyshare download link of an specific episode.
    """
    response = SESSION.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = []
    for link in soup.findAll('a'):
        if link.parent.name == 'td':
            links.append(link["href"])
    return links


def main():
    # Search for anime
    query = input('Buscar Anime: ')
    anime_dict = search_anime(query)
    anime = select_anime(anime_dict)

    # Select episode
    ep = select_ep(anime)

    # Get download link
    url = anime['link'] + ep
    links = get_links(url)

    if not links:
        print('Noy hay un enlace de descarga no disponible')
        exit()
    elif len(links) > 1:
        print('Nota: Solo Zippyshare esta disponible para descarga.')
        link = enquiries.choose('Selecciona un enlace', links)
    elif len(links) == 1:
        link = links[0]

    if 'zippyshare' not in link:
        print('El enlace no es de Zippyshare. Descargalo en tu navegador')
        print(link)

    else:
        if enquiries.confirm('¿Quieres descargar el episodio?'):
            try:
                extract_info(link)
            except Exception as e:
                raise


if __name__ == '__main__':
    main()
