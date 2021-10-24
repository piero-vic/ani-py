#!/usr/bin/env python3

import typer
from zippyshare_downloader import extract_info
import enquiries
import subprocess
from rich.console import Console
from rich.theme import Theme

from servers import Jkanime


custom_theme = Theme({
    'good': 'bold green',
    'bad': 'bold red',
    'warning': 'bold yellow'
})

console = Console(theme=custom_theme)


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
    while True:
        try:
            ep = int(input(f'Elige un episodio ({anime["ep"]}): '))
        except Exception as e:
            # Delete previous line
            CURSOR_UP_ONE = '\x1b[1A'
            ERASE_LINE = '\x1b[2K'
            print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
            continue
        else:
            break
    return ep


def select_link(links):
    """
    Prints links and ask you to select one.
    """
    if not links:
        console.print('No hay un enlace de descarga disponible', style="bad")
        exit()
    elif len(links) == 1:
        return links[0]
    elif len(links) > 1:
        console.print('[bold]Selecciona un enlace |[/] [warning]Solo Zippyshare esta disponible para descarga[/]')
        return enquiries.choose('', links)


def download(link):
    """
    Download the links. Print link if not available.
    """
    if 'zippyshare' not in link:
        console.print(f'Descargalo en tu navegador => {link}', style="good")
    else:
        if enquiries.confirm('¿Quieres descargar el episodio?'):
            try:
                extract_info(link)
            except Exception as e:
                raise

def open_video_player(url):
    option = f"--http-header-fields='Referer: {Jkanime().base_url}'"
    subprocess.run(['mpv', option, url])


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

    if len(anime_dict) == 1:
        anime_info = list(anime_dict.values())[0]
    else:
        anime_info = select_anime(anime_dict)

    # Print anime title
    console.print(f'{anime_info["title"]}', style="good")

    # Select episode
    if anime_info['type'] == 'Movie':
        episode = 'pelicula'
    elif episode is None:
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
        open_video_player(link)


if __name__ == '__main__':
    app.command()(main)
    app()
