import pytest

import artist_avg


def test_get_artist_id():
    assert artist_avg.get_artist_id('Coldplay') == 'cc197bad-dc9c-440d-a5b5-d52ba2e14234'


def test_get_song_lyric_count():
    assert artist_avg.get_song_lyric_count('Coldplay', 'Adventure of a Lifetime') == 286


def test_get_all_artist_songs():
    assert len(artist_avg.get_all_artist_songs('Coldplay')) == 101
