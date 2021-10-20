#!/usr/bin/env python3

from zippyshare_downloader import extract_info
from bs4 import BeautifulSoup
import requests
import enquiries


SESSION = requests.Session()
HEADERS = {'user-agent': 'Mozilla/5.0'}


class Jkanime():
    """Jkanime site"""

    id = 'jkanime'
    name = 'JKanime'
    lang = 'es'

    base_url = 'https://jkanime.net/'
    ajax_search_url = 'https://jkanime.net/ajax/ajax_search/?q='
    search_url = base_url + 'buscar/'
    anime_url = base_url + '{0}/'
    episode_url = anime_url + '{1}/'

    session = requests.Session()
    headers = {'user-agent': 'Mozilla/5.0'}

    def session_get(self, *args, **kwargs):
        """
        Initialize requests session
        """
        try:
            r = self.session.get(*args, **kwargs)
        except Exception:
            raise

        return r

    def search_anime(self, query):
        """
        Returns the first 5 matches on a list of dictionaries.
        """
        self.query_url = self.ajax_search_url + query

        r = self.session_get(self.query_url, headers=self.headers)

        if r.status_code != 200:
            print('Error de conección')
            exit()

        query_result = r.json()['animes']

        if not query_result:
            print('No se encuentraron resultados')
            exit()

        anime_dict = {}
        for anime in query_result:
            anime_dict[anime['title']] = {
                'title': anime['title'],
                'image': anime['image'],
                'type': anime['type'],
                'slug': anime['slug'],
                'link': self.anime_url.format(anime['slug']),
                'ep': self.get_ep_num(anime['slug'])
            }
        return anime_dict

    def get_ep_num(self, anime_slug):
        """
        Returns the number of episodes of an anime.
        """
        r = self.session_get(
            self.anime_url.format(anime_slug), headers=self.headers
        )

        soup = BeautifulSoup(r.content, 'html.parser')
        details_container = soup.find(
            'div', {'class': 'anime__details__widget'}
        )
        details = details_container.findChildren('li')
        return details[3].contents[1].strip()

    def get_download_links(self, anime_slug, ep):
        """
        Returns download link of an specific episode.
        """
        r = self.session_get(
            self.episode_url.format(anime_slug, ep),
            headers=self.headers
        )
        soup = BeautifulSoup(r.content, 'html.parser')
        links = []
        for link in soup.findAll('a'):
            if link.parent.name == 'td':
                links.append(link["href"])
        return links


def select_anime(anime_dict):
    """
    Prints list of anime names and ask you to select one.
    """
    choice = enquiries.choose('Selecciona un anime: ', anime_dict.keys())
    return anime_dict[choice]


def select_ep(anime):
    """
    Asks you to select one episode
    """
    ep_num = Jkanime().get_ep_num(anime['slug'])
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


def main():
    # Search for anime
    query = input('Buscar Anime: ')
    anime_dict = Jkanime().search_anime(query)
    anime = select_anime(anime_dict)

    # Select episode
    ep = select_ep(anime)

    # Get download link
    links = Jkanime().get_download_links(anime['slug'], ep)

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
