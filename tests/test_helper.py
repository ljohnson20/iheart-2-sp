# Tests for station_listener.py
import pytest
import helper


def test_song_clean_string():
    assert helper.clean_string('Beautiful People (feat. Khalid)') == 'beautiful people khalid'


def test_artist_clean_string():
    assert helper.clean_string('Panic! At The Disco') == "panic at disco"


def test_less_clean_string():
    assert helper.clean_string('A$AP Rocky & Kid Cudi', False) == "a$ap rocky & kid cudi"


def test_find_api_url():
    assert helper.api_url_find('https://www.iheart.com/live/z100-1469/') == \
           "https://us.api.iheart.com/api/v3/live-meta/stream/1469/currentTrackMeta"


def test_fail_api_url():
    assert not helper.api_url_find("https://www.iheart.com/lpn02")
