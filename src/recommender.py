from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

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
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs ranked by score against the user's profile."""
        user_prefs = {
            "genre": user.favorite_genre,
            "mood":  user.favorite_mood,
            "energy": user.target_energy,
        }
        ranked = sorted(
            self.songs,
            key=lambda song: score_song(user_prefs, vars(song))[0],
            reverse=True,
        )
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable string explaining why a song was recommended."""
        user_prefs = {
            "genre": user.favorite_genre,
            "mood":  user.favorite_mood,
            "energy": user.target_energy,
        }
        _, reasons = score_song(user_prefs, vars(song))
        return ", ".join(reasons) if reasons else "no strong matches found"

def load_songs(csv_path: str) -> List[Dict]:
    """Read a CSV file and return each row as a typed dictionary."""
    import csv
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a song out of 90 pts (genre 20, mood 30, energy 40) and return reasons.

    EXPERIMENTAL — Weight Shift:
      Genre weight halved  : 40 → 20 pts  (binary match)
      Mood weight unchanged:      30 pts  (binary match)
      Energy weight doubled: 20 → 40 pts  (continuous 0–1 proximity)
    Total max is still 90 pts so scores remain directly comparable to baseline.
    """
    score = 0.0
    reasons = []

    # Step 1 — Genre match (20 pts, halved from 40)
    if song["genre"] == user_prefs.get("genre"):
        score += 20.0
        reasons.append(f"genre match (+20.0)")

    # Step 2 — Mood match (30 pts, unchanged)
    if song["mood"] == user_prefs.get("mood"):
        score += 30.0
        reasons.append(f"mood match (+30.0)")

    # Step 3 — Energy proximity (0–40 pts, doubled from 0–20)
    if "energy" in user_prefs:
        energy_score = (1 - abs(song["energy"] - user_prefs["energy"])) * 40
        score += energy_score
        reasons.append(f"energy match (+{energy_score:.1f})")

    return (score, reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort by score descending, and return the top k with explanations."""
    scored = sorted(
        [
            (song, score, ", ".join(reasons))
            for song in songs
            for score, reasons in [score_song(user_prefs, song)]
        ],
        key=lambda item: item[1],
        reverse=True,
    )
    return scored[:k]
