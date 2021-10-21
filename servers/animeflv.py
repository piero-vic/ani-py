#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests

from pprint import pprint


class Animeflv():
    """AnimeFLV site"""

    id = 'animeflv'
    name = 'AnimeFLV'
    lang = 'es'

    base_url = 'https://www3.animeflv.net/'
    post_search_url = base_url + 'api/animes/search'
    search_url = base_url + 'browse?q='
    anime_url = base_url + '/anime/{0}/'
    episode_url = base_url + 'ver/{0}-{1}/'

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

    def session_post(self, *args, **kwargs):
        """
        Initialize requests session
        """
        try:
            r = self.session.post(*args, **kwargs)
        except Exception:
            raise

        return r

    def search_anime(self, query):
        """
        Returns the first 5 matches on a list of dictionaries.
        """

        r = self.session_post(self.post_search_url, data = {'value': query}, headers=self.headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        pprint(soup)
