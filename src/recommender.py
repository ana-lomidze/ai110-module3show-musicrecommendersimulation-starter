import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field, asdict

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genres: List[str]
    favorite_moods: List[str]
    target_energy: float
    favorite_artists: List[str] = field(default_factory=list)
    target_acousticness: Optional[float] = None
    target_valence: Optional[float] = None
    target_danceability: Optional[float] = None
    target_tempo_bpm: Optional[float] = None

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        ranked = recommend_songs(asdict(user), [asdict(s) for s in self.songs], k=k)
        return [Song(**song_dict) for song_dict, _, _ in ranked]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        score, reasons = score_song(asdict(user), asdict(song))
        if not reasons:
            return f"Score {score:.2f}: no matching preferences"
        return f"Score {score:.2f}: " + "; ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    int_fields = ("id",)
    float_fields = ("energy", "tempo_bpm", "valence", "danceability", "acousticness")

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for field in int_fields:
                row[field] = int(row[field])
            for field in float_fields:
                row[field] = float(row[field])
            songs.append(row)
    return songs

WEIGHTS = {
    "genre": 8, "mood": 7, "energy": 6, "artist": 5,
    "acousticness": 4, "valence": 3, "danceability": 2, "tempo_bpm": 1,
}

# feature -> user pref key (the song's value is checked against the user's list)
CATEGORICAL = {
    "genre": "favorite_genres",
    "mood": "favorite_moods",
    "artist": "favorite_artists",
}

# feature -> (user pref key, largest possible gap R)
NUMERIC = {
    "energy": ("target_energy", 1.0),
    "acousticness": ("target_acousticness", 1.0),
    "valence": ("target_valence", 1.0),
    "danceability": ("target_danceability", 1.0),
    "tempo_bpm": ("target_tempo_bpm", 120.0),  # normalized over 60-180 BPM
}

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    weighted_sum = 0.0
    total_weight = 0.0
    reasons: List[str] = []

    for feature, weight in WEIGHTS.items():
        if feature in CATEGORICAL:
            liked = user_prefs.get(CATEGORICAL[feature])
            if not liked:
                continue  # no preference: skip, don't count as a mismatch
            sim = 1.0 if song[feature] in liked else 0.0
            if sim:
                reasons.append(f"{feature} match: {song[feature]} (+{weight})")
        else:
            pref_key, value_range = NUMERIC[feature]
            target = user_prefs.get(pref_key)
            if target is None:
                continue
            sim = max(0.0, 1 - abs(song[feature] - target) / value_range)
            reasons.append(f"{feature} {song[feature]} vs target {target} (sim {sim:.2f})")

        weighted_sum += weight * sim
        total_weight += weight

    if total_weight == 0:
        return 0.0, []
    return weighted_sum / total_weight, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    target_energy = user_prefs.get("target_energy")

    def rank_key(item: Tuple[Dict, float, str]) -> Tuple[float, float]:
        song, score, _ = item
        # Ties on score are broken by closeness to the target energy.
        gap = abs(song["energy"] - target_energy) if target_energy is not None else 0.0
        return (score, -gap)

    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, "; ".join(reasons)))

    return sorted(scored, key=rank_key, reverse=True)[:k]
