#!/usr/bin/env python3

from zippyshare_downloader import extract_info
import enquiries

from servers import Jkanime


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


def main():
    try:
        # Search for anime
        query = input('Buscar Anime: ')
        anime_dict = Jkanime().search_anime(query)
        anime = select_anime(anime_dict)

        # Select episode
        ep = select_ep(anime)

        mode = enquiries.choose('', ['Download', 'Stream'])

        if mode == 'Download':
            # Get download link
            links = Jkanime().get_download_links(anime['slug'], ep)

            # Select and download link
            link = select_link(links)
            download(link)
        else:
            # Get embedded video link
            links = Jkanime().get_embedded_video_links(anime['slug'], ep)
            link = Jkanime().get_video_link(links)
            Jkanime().open_video_player(link)

    except KeyboardInterrupt:
        return 1


if __name__ == '__main__':
    main()
