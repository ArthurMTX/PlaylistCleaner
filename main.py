import argparse
import base64
import os
import re
from collections import defaultdict

import requests
from colorama import init, Fore, Style
from dotenv import load_dotenv

init(autoreset=True)
load_dotenv()

AUTH_URL = 'https://accounts.spotify.com/api/token'
PLAYLIST_API_URL = 'https://api.spotify.com/v1/playlists/'
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
DEFAULT_SEPARATOR_LENGTH = 60

VARIATION_KEYWORDS = [
    'remix', 'feat', 'vip', 'bootleg', 'edit', 'mix',
    'version', 'rework', 're-edit', 'mashup', 'cover',
    'live', 'acoustic', 'instrumental', 'extended',
    'radio', 'original', 'club', 'dub', 'reprise',
    'remastered', 'session', 'vs', 'acapella',
    'versus', 'tribute', 'alt', 'alternate',
    'unplugged', 'special', 'deluxe', 'anniversary',
    'rave', 'flip', 'boot', 'exclusive', 'radio edit',
    'bonus', 'reconstruction', 'redux', 'reissue'
]

def get_access_token():
    auth_header = base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode('utf-8')).decode('utf-8')
    headers = {'Authorization': f'Basic {auth_header}'}
    data = {'grant_type': 'client_credentials'}
    response = requests.post(AUTH_URL, headers=headers, data=data)
    response_data = response.json()
    if 'access_token' in response_data:
        return response_data['access_token']
    else:
        raise Exception('Failed to get access token')

def get_playlist_info(playlist_id, access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    url = f'{PLAYLIST_API_URL}{playlist_id}'
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception('Failed to get playlist information')

    data = response.json()
    return data['name'], data['owner']['display_name']

def get_all_tracks(playlist_id, access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    url = f'{PLAYLIST_API_URL}{playlist_id}/tracks'
    params = {'limit': 100, 'offset': 0}
    tracks = []
    total = 0

    while True:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            return []

        data = response.json()
        tracks.extend(data['items'])
        total = data['total']

        print(f"{Fore.CYAN}🔄 Progress: {Fore.GREEN}{len(tracks)}/{total} {Fore.WHITE}tracks retrieved ({Fore.YELLOW}{(len(tracks) / total) * 100:.2f}%{Fore.WHITE})")

        if data['next']:
            params['offset'] += 100
        else:
            break

    tracks_info = []
    for item in tracks:
        track_name = item['track']['name']
        artist_names = [artist['name'] for artist in item['track']['artists']]
        album_name = item['track']['album']['name']
        tracks_info.append({'title': track_name, 'artists': artist_names, 'album': album_name})

    return tracks_info

def clean_title(title):
    title = re.sub(r'\(.*?\)', '', title).strip()
    for keyword in VARIATION_KEYWORDS:
        title = re.sub(rf'\b{keyword}\b', '', title, flags=re.IGNORECASE).strip()
    return title.lower()

def detect_variations(tracks):
    grouped_tracks = defaultdict(list)

    for track in tracks:
        cleaned_title = clean_title(track['title'])
        grouped_tracks[cleaned_title].append(track)

    duplicates = {title: tracks for title, tracks in grouped_tracks.items() if len(tracks) > 1}
    return duplicates

def print_separator(char='-', length=DEFAULT_SEPARATOR_LENGTH, color=Fore.WHITE):
    print(color + char * length)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="🎧 Fetch all tracks from a Spotify playlist and detect duplicates.")
    parser.add_argument('playlist_id', type=str, help='Spotify Playlist ID')
    args = parser.parse_args()

    ACCESS_TOKEN = get_access_token()
    playlist_name, playlist_owner = get_playlist_info(args.playlist_id, ACCESS_TOKEN)
    tracks = get_all_tracks(args.playlist_id, ACCESS_TOKEN)

    print_separator('=', DEFAULT_SEPARATOR_LENGTH, Fore.MAGENTA)
    print(f"{Style.BRIGHT}{Fore.YELLOW}🎶 Spotify Playlist Duplicates Detector by {Fore.CYAN}ArthurMTX")
    print(f"{Style.BRIGHT}{Fore.YELLOW}📜 Playlist Name  : {Fore.CYAN}{playlist_name}")
    print(f"{Style.BRIGHT}{Fore.YELLOW}👤 Playlist Owner : {Fore.CYAN}{playlist_owner}")
    print(f"{Style.BRIGHT}{Fore.YELLOW}🆔 Playlist ID    : {Fore.CYAN}{args.playlist_id}")
    print(f"{Style.BRIGHT}{Fore.YELLOW}💿 Total number of tracks retrieved : {Fore.GREEN}{len(tracks)}")
    print_separator('=', DEFAULT_SEPARATOR_LENGTH, Fore.MAGENTA)

    duplicates = detect_variations(tracks)

    total_duplicates = sum(len(tracks) for tracks in duplicates.values())
    duplicate_percentage = (total_duplicates / len(tracks)) * 100 if tracks else 0
    average_duplicates = total_duplicates / len(duplicates) if duplicates else 0

    print(f"{Style.BRIGHT}{Fore.YELLOW}🔁 Total duplicated tracks : {Fore.RED}{total_duplicates}")
    print(f"{Style.BRIGHT}{Fore.YELLOW}📊 Percentage of duplicated tracks : {Fore.CYAN}{duplicate_percentage:.2f}%")
    print(f"{Style.BRIGHT}{Fore.YELLOW}📈 Average number of duplicates per title : {Fore.CYAN}{average_duplicates:.2f}")
    print_separator('=', DEFAULT_SEPARATOR_LENGTH, Fore.MAGENTA)

    if duplicates:
        print(f"{Fore.GREEN}\n🎯 Duplicates found:\n")
        sorted_duplicates = sorted(duplicates.items(), key=lambda item: len(item[1]), reverse=True)
        for title, tracks in sorted_duplicates:
            print_separator('-', DEFAULT_SEPARATOR_LENGTH, Fore.BLUE)
            print(f"{Fore.YELLOW}🔍 {title.capitalize()} - {Fore.RED}{len(tracks)} occurrence(s)")
            print_separator('-', DEFAULT_SEPARATOR_LENGTH, Fore.BLUE)
            for i, track in enumerate(tracks):
                is_duplicate = any(
                    set(track['artists']) == set(other_track['artists'])
                    for j, other_track in enumerate(tracks) if i != j
                )
                if is_duplicate:
                    color = Fore.RED + Style.BRIGHT
                    emoji = "⚠️"
                else:
                    color = Fore.YELLOW + Style.BRIGHT
                    emoji = "✨"
                print(f"{color} {emoji} • {track['title']} - {', '.join(track['artists'])} - {track['album']}")
            print_separator('-', DEFAULT_SEPARATOR_LENGTH, Fore.BLUE)
            print("\n")
    else:
        print(f"{Fore.GREEN}✅ No duplicates found.")