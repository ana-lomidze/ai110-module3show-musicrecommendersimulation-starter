"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from typing import Dict, List, Tuple
from src.recommender import load_songs, recommend_songs

WIDTH = 60


def profile_summary(user_prefs: Dict) -> str:
    parts = []
    if user_prefs.get("favorite_genres"):
        parts.append("genres=" + ", ".join(user_prefs["favorite_genres"]))
    if user_prefs.get("favorite_moods"):
        parts.append("moods=" + ", ".join(user_prefs["favorite_moods"]))
    if user_prefs.get("target_energy") is not None:
        parts.append(f"energy={user_prefs['target_energy']:.2f}")
    return " | ".join(parts)


def print_recommendations(user_prefs: Dict, recommendations: List[Tuple[Dict, float, str]]) -> None:
    print("=" * WIDTH)
    print(f" TOP {len(recommendations)} RECOMMENDATIONS")
    print(f" Profile: {profile_summary(user_prefs)}")
    print("=" * WIDTH)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{rank}  {song['title']} - {song['artist']}")
        print(f"    Score: {score:.2f}")
        print("    Why:")
        for reason in explanation.split("; "):
            print(f"      - {reason}")
        print("-" * WIDTH)


def main() -> None:
    songs = load_songs("data/songs.csv")

    user_prefs_happy = {
        "favorite_genres": ["pop"],
        "favorite_moods": ["happy"],
        "target_energy": 0.8,
    }

    user_prefs_chill = {
        "favorite_genres": ["lofi", "jazz"],
        "favorite_moods": ["chill", "relaxed"],
        "target_energy": 0.40,
        "favorite_artists": ["LoRoom"],
        "target_acousticness": 0.80,
    }

    user_prefs_rock = {
        "favorite_genres": ["rock", "metal"],
        "favorite_moods": ["intense"],
        "target_energy": 1.0,
        "favorite_artists": ["Voltline"],
    }

    user_prefs_classic = {
        "favorite_genres": ["classical"],
        "favorite_moods": ["melancholy"],
        "target_energy": 0.20,
        "favorite_artists": ["Clara Whitfield"],
        "target_acousticness": 0.99,
    }

    # recommendations = recommend_songs(user_prefs, songs, k=5)
    # print_recommendations(user_prefs, recommendations)

    recommendations = recommend_songs(user_prefs_chill, songs, k=5)
    print_recommendations(user_prefs_chill, recommendations)


    recommendations = recommend_songs(user_prefs_rock, songs, k=5)
    print_recommendations(user_prefs_rock, recommendations)

    recommendations = recommend_songs(user_prefs_classic, songs, k=5)
    print_recommendations(user_prefs_classic, recommendations)


if __name__ == "__main__":
    main()
