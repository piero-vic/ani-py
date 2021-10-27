#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import re


class Jkanime():
    """Jkanime site"""

    id = 'jkanime'
    name = 'JKanime'
    lang = 'es'

    base_url = 'https://jkanime.net/'
    ajax_search_url = 'https://jkanime.net/ajax/ajax_search/?q={0}'
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
        r = self.session_get(self.ajax_search_url.format(query),
                             headers=self.headers)

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
                'type': anime['type'],
                'slug': anime['slug'],
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

    def get_embedded_video_links(self, anime_slug, ep):
        r = self.session_get(
            self.episode_url.format(anime_slug, ep),
            headers=self.headers
        )

        embedded_links = re.findall('https://jkanime.net/(?:jk|um).+?(?=")', r.text)
        return embedded_links

    def select_embeded_link(self, links):
        for link in links:
            r = self.session_get(link, headers=self.headers)
            if r.status_code == 200:
                return r

    def get_video_link(self, links):
        r = self.select_embeded_link(links)
        embedded_links = re.findall("https://cloud1.+?(?=')", r.text)
        return embedded_links[0]
