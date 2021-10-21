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
