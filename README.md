# ani-py

A cli to download and stream anime from [jkanime](https://jkanime.net/).

This projects is inspired by [ani-cli](https://github.com/pystardust/ani-cli). I decided to make a version that works on a website with spanish subs.

## Usage

### Basic usage
``ani-py <query> <episode>``

### Modes

#### Download anime
``ani-py -d <query>``

#### Stream anime
``ani-py -s <query>``

`ani-py` will ask you for the query, episode and mode if you run it without arguments.

The download option only works with Zippyshare.

## Main dependencies

- [typer](https://github.com/tiangolo/typer)
- [rich](https://github.com/willmcgugan/rich)
- [zippyshare-downloader](https://github.com/mansuf/zippyshare-downloader)
- [enquiries](https://gitlab.com/facingBackwards/enquiries)
