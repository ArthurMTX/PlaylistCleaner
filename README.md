# Spotify Playlist Duplicate Finder 🎧

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Spotify API](https://img.shields.io/badge/Spotify%20API-v1-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Overview 📜

**Spotify Playlist Duplicate Finder** is a Python script that helps you identify and manage duplicate tracks in your Spotify playlists. It detects tracks that have variations like remixes, covers, or live versions and helps you clean up your playlists by identifying redundant entries.

## Features ✨

- **Fetch all tracks** from a Spotify playlist.
- **Detect duplicate tracks** based on variations (e.g., remix, live, cover).
- **Color-coded output** with emojis for easy readability.
- **Progress tracking** during data retrieval.
- **Summarized statistics** about duplicates found.

## Requirements 📦

- Python 3.8+
- Spotify Developer Account (for API access)
- Spotify Client ID and Client Secret

## Installation 🚀

1. **Clone the repository**:
    ```bash
    git clone https://github.com/ArthurMTX/PlaylistCleaner.git
    cd PlaylistCleaner
    ```

2. **Create a virtual environment (optional but recommended)**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
    - Create a `.env` file in the project root directory:
    ```bash
    touch .env
    ```
    - Add your Spotify API credentials to the `.env` file:
    ```env
    SPOTIFY_CLIENT_ID=your_spotify_client_id
    SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
    ```

## Usage 🛠️

To use the script, simply run the following command:

```bash
python main.py <your_playlist_id>
```

## Output 🎯

The script provides detailed information about duplicates:

    Red entries indicate exact duplicates (same title and artist).
    Yellow entries indicate variations (e.g., different versions of the same track).
    Overall statistics like the total number of duplicates and percentage of duplicates.

Example output:

```markdown

==================================================
📜 Playlist Name : My Awesome Playlist
🆔 Playlist ID   : 5IsfvDlyiZFbYQ5jwzNWxm
🎵 Total number of tracks retrieved : 293
==================================================
🔁 Total duplicated tracks : 48
📊 Percentage of duplicated tracks : 16.38%
📈 Average number of duplicates per title : 3.00
==================================================

🎯 Duplicates found:

--------------------------------------------------
🔍 Allstars Mic - 6 occurrence(s)
--------------------------------------------------
 ⚠️ • Allstars Mic (feat. DnB Allstars) - Eksman, Amplify, DnB Allstars - Album 1
 ✨ • Allstars Mic (feat. DnB Allstars) - Natty D, R3IDY, DnB Allstars - Album 2
--------------------------------------------------
```

## Contributing 🤝

Contributions are welcome! If you'd like to improve the script or add new features, feel free to fork the repository and submit a pull request.