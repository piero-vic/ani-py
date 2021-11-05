#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import re


class Jkanime():
    """Jkanime site"""

    base_url = 'https://jkanime.net/'
    ajax_search_url = base_url + 'ajax/ajax_search/?q={0}'
    anime_url = base_url + '{0}/'
    episode_url = anime_url + '{1}/'

    session = requests.Session()
    headers = {'user-agent': 'Mozilla/5.0'}

    def session_get(self, *args, **kwargs):
        """
        Execute request
        """
        try:
            return self.session.get(*args, **kwargs)
        except Exception:
            print('No hay conección a internet')
            exit()

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

        return {anime['title']: anime for anime in query_result}

    def get_download_links(self, anime_slug, ep):
        """
        Returns download link of an specific episode.
        """
        r = self.session_get(
            self.episode_url.format(anime_slug, ep),
            headers=self.headers
        )
        links = BeautifulSoup(r.content, 'html.parser').findAll('a')
        return [link["href"] for link in links if link.parent.name == 'td']

    def get_embedded_video_links(self, anime_slug, ep):
        r = self.session_get(
            self.episode_url.format(anime_slug, ep),
            headers=self.headers
        )
        return re.findall('https://jkanime.net/(?:jk|um).+?(?=")', r.text)

    def get_video_link(self, links):
        for link in links:
            r = self.session_get(link, headers=self.headers)
            if r.status_code == 200:
                break
        return re.findall("https://cloud1.+?(?=')", r.text)[0]
