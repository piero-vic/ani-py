#!/usr/bin/env python3

import typer
from zippyshare_downloader import extract_info
import enquiries

from servers import Jkanime


def select_anime(anime_dict):
    """
    Prints list of anime names and ask you to select one.
    """
    choice = enquiries.choose('', anime_dict.keys())
    return anime_dict[choice]


def select_ep(anime):
    """
    Asks you to select one episode
    """
    ep_num = Jkanime().get_ep_num(anime['slug'])
    print(f'{anime["title"]}')
    while True:
        try:
            ep = int(input(f'Elige un episodio ({anime["ep"]}): '))
        except Exception as e:
            continue
        else:
            break
    return ep


def select_link(links):
    """
    Prints links and ask you to select one.
    """
    if not links:
        print('No hay un enlace de descarga disponible')
        exit()
    elif len(links) == 1:
        return links[0]
    elif len(links) > 1:
        return enquiries.choose(
            ('Selecciona un enlace ' +
             '(Solo Zippyshare esta disponible para descarga)'),
            links
        )


def download(link):
    """
    Download the links. Print link if not available.
    """
    if 'zippyshare' not in link:
        print('El enlace no es de Zippyshare. Descargalo en tu navegador')
        print(link)
    else:
        if enquiries.confirm('¿Quieres descargar el episodio?'):
            try:
                extract_info(link)
            except Exception as e:
                raise


app = typer.Typer(add_completion=False)


def main(
    anime: str = typer.Argument(None),
    episode: int = typer.Argument(None),
    mode: bool = typer.Option(None,
                              "--download/--stream", '-d/-s',
                              help="Choose to download or stream.")
):
    # Search for anime
    if anime is None:
        anime = input('Buscar Anime: ')

    anime_dict = Jkanime().search_anime(anime)
    anime_info = select_anime(anime_dict)

    # Select episode
    if episode is None:
        episode = select_ep(anime_info)

    # Select mode
    if mode is None:
        mode = enquiries.choose('', ['Download', 'Stream'])

    # Download
    if mode == 'Download' or mode is True:
        # Get download link
        links = Jkanime().get_download_links(anime_info['slug'], episode)
        # Select and download link
        link = select_link(links)
        download(link)
    # Stream
    else:
        # Get embedded video link
        links = Jkanime().get_embedded_video_links(anime_info['slug'], episode)
        link = Jkanime().get_video_link(links)
        Jkanime().open_video_player(link)


if __name__ == '__main__':
    app.command()(main)
    app()
