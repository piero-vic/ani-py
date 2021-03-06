#!/usr/bin/env python3

import typer
from zippyshare_downloader import extract_info
import enquiries
import subprocess
from rich.console import Console
from rich.theme import Theme
from .servers import Jkanime


CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

console = Console(theme=Theme({
    'good': 'bold green',
    'bad': 'bold red',
    'warning': 'bold yellow'
}))


def select_anime(anime_dict):
    """
    Prints list of anime names and ask you to select one.
    """
    if len(anime_dict) == 1:
        return list(anime_dict.values())[0]
    else:
        choice = enquiries.choose('', anime_dict.keys())
        return anime_dict[choice]


def select_ep(anime):
    """
    Asks you to select one episode
    """
    while True:
        try:
            ep = int(input(f'Elige un episodio: '))
            break
        except Exception:
            print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
            continue
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
        try:
            extract_info(link)
        except Exception:
            print('Error de conección')
            exit()


def open_video_player(url):
    """
    Opens media player.
    """
    option = f"--http-header-fields='Referer: {Jkanime().base_url}'"
    subprocess.Popen(['mpv', '--no-terminal', option, url, '&'])


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
        print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
    with console.status("[bold green]Buscando...") as status:
        anime_dict = Jkanime().search_anime(anime)
    anime_info = select_anime(anime_dict)

    # Select episode
    console.print(f'{anime_info["title"]}', style="good")
    if anime_info['type'] == 'Movie':
        episode = 'pelicula'
    elif episode is None:
        episode = select_ep(anime_info)
        print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)

    # Select mode
    if mode is None:
        mode = enquiries.choose('', ['Download', 'Stream'])

    # Download
    if mode == 'Download' or mode is True:
        links = Jkanime().get_download_links(anime_info['slug'], episode)
        link = select_link(links)
        print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
        download(link)
    # Stream
    else:
        with console.status("[bold green]Obteniendo enlaces...") as status:
            links = Jkanime().get_embedded_video_links(anime_info['slug'], episode)
            link = Jkanime().get_video_link(links)
        console.print("Abriendo video", style="bold green")
        open_video_player(link)

    console.print('Gracias por usar ani-py :cherry_blossom:', style="bold")


app = typer.Typer(add_completion=False)
app.command()(main)
