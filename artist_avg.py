import argparse
import json
import statistics
import sys

import musicbrainzngs as mb
import requests

mb.set_useragent('altest', '0.1', 'https://github.com/jamesnunn')
BROWSE_LIMIT = 100


class ArtistNotFoundError(Exception):
    pass


def get_artist_id(artist):
    '''Get the musicbrainz artist id for feeding into `musicbrainzngs.browse_releases`'''
    possible_ids = mb.search_artists(artist=artist, strict=True)['artist-list']
    try:
        artist = [res['id'] for res in possible_ids if int(res['ext:score']) == 100][0]
    except IndexError:
        raise ArtistNotFoundError(f'Artist {artist} not found')
    return artist


def get_all_artist_songs(artist):
    '''Get a list of songs for a given artist'''
    artist_id = get_artist_id(artist)
    offset = 0
    songs = []
    result_len = BROWSE_LIMIT

    while result_len == BROWSE_LIMIT:
        result = mb.browse_releases(artist=artist_id, release_type=['single'], limit=BROWSE_LIMIT, offset=offset)['release-list']
        result_len = len(result)
        offset += result_len
        songs.extend([s['title'] for s in result])

    return list(set(songs))


def get_song_lyric_count(artist, title):
    '''Get the count of lyrics in a song, given the artist and title'''
    r = requests.get(f'https://api.lyrics.ovh/v1/{artist}/{title}')
    try:
        data = r.json()
    except json.decoder.JSONDecodeError:
        count = 0
    else:
        lyrics = data.get('lyrics', '')
        count = len(lyrics.split())
    return count


def get_artist_avg_lyrics(artist):
    '''Calculate the mean lyric length for an artist'''
    songs = get_all_artist_songs(artist)
    counts = filter(None, [get_song_lyric_count(artist, song) for song in songs])
    return statistics.mean(counts)


def main():

    parser = argparse.ArgumentParser('Artist Lyric Stats')
    parser.add_argument('artists', nargs='+')

    args = parser.parse_args()

    for artist in args.artists:
        try:
            avg = get_artist_avg_lyrics(artist)
            print(f'{artist} average word count in lyrics: {avg}')
        except ArtistNotFoundError as e:
            print(e)


if __name__ == '__main__':
    main()