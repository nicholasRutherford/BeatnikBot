"""
Queries the Beatnik API for resuls

Sample query
'https://www.beatnikapp.com/api/convert?q=https://open.spotify.com/track/3nGWzFBJ5tMzHWAgs16fK6?si=dXVxz7D2RIya96S1jf-7VQ'
=>
{'album': 'The Glorious Dead',
 'album_art': 'https://i.scdn.co/image/ab67616d0000b273ffa262e79ca11e55114f7fd6',
 'apple': 'https://music.apple.com/us/album/what-makes-a-good-man-original-version/519013512?i=519013514',
 'artist': 'The Heavy',
 'errors': [],
 'gpm': 'https://music.google.com/music/m/Tkx2jsxtdwyfnvdjfcocktlcese',
 'id': 1118,
 'soundcloud': 'https://soundcloud.com/theheavyyy/kenny-remix',
 'spotify': 'https://open.spotify.com/track/3nGWzFBJ5tMzHWAgs16fK6?si=dXVxz7D2RIya96S1jf-7VQ',
 'title': 'What Makes A Good Man?',
 'type': 'track'}
"""
import requests
BEATNIK_QUERY_API = "https://www.beatnikapp.com/api/convert?q="


def get_beatnik_data(query):
    r = requests.get(BEATNIK_QUERY_API + query)
    json_result = r.json()

    return {'album': json_result.get('album'),
            'album_art': json_result.get('album_art'),
            'apple': json_result.get('apple'),
            'artist': json_result.get('artist'),
            'errors': json_result.get('errors'),
            'gpm': json_result.get('gpm'),
            'soundcloud': json_result.get('soundcloud'),
            'spotify': json_result.get('spotify'),
            'title': json_result.get('title'),
            'tidal': json_result.get('tidal')
            }
