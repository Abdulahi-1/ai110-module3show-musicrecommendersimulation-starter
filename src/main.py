"""
Command line runner for the Music Recommender Simulation.

Runs six user profiles through the recommender:
  - Three "normal" taste profiles
  - Three adversarial / edge-case profiles designed to probe scoring edge cases
"""

from typing import Optional
from recommender import load_songs, recommend_songs


# ---------------------------------------------------------------------------
# Profile definitions
# ---------------------------------------------------------------------------

PROFILES = [
    # --- Normal profiles ---------------------------------------------------
    {
        "label": "High-Energy Pop",
        "prefs": {"genre": "pop", "mood": "happy", "energy": 0.9},
        "note": None,
    },
    {
        "label": "Chill Lofi",
        "prefs": {"genre": "lofi", "mood": "chill", "energy": 0.3},
        "note": None,
    },
    {
        "label": "Deep Intense Rock",
        "prefs": {"genre": "rock", "mood": "intense", "energy": 0.95},
        "note": None,
    },

    # --- Adversarial / edge-case profiles ----------------------------------
    {
        "label": "Adversarial: High Energy + Non-existent Mood",
        "prefs": {"genre": "pop", "mood": "sad", "energy": 0.9},
        "note": (
            "'sad' does not exist in the dataset — mood branch never fires. "
            "Expect genre match to dominate; energy proximity breaks ties."
        ),
    },
    {
        "label": "Adversarial: Lofi Lover at Max Energy",
        "prefs": {"genre": "lofi", "mood": "chill", "energy": 1.0},
        "note": (
            "Lofi songs cluster around energy 0.3–0.4. "
            "Requesting energy=1.0 maximally penalises every lofi track's "
            "energy component even though genre+mood match perfectly."
        ),
    },
    {
        "label": "Adversarial: Unknown Genre + Zero Energy",
        "prefs": {"genre": "classical", "mood": "intense", "energy": 0.0},
        "note": (
            "'classical' is absent from the catalogue — genre never matches (+40). "
            "Energy=0.0 heavily penalises high-energy songs. "
            "Only mood and energy shape the ranking."
        ),
    },
]


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def print_profile_results(label: str, prefs: dict, note: Optional[str], songs: list) -> None:
    width = 60
    print()
    print("=" * width)
    print(f"  Profile : {label}")
    print(f"  Genre   : {prefs['genre']}")
    print(f"  Mood    : {prefs['mood']}")
    print(f"  Energy  : {prefs['energy']}")
    if note:
        # Word-wrap the note at ~55 chars
        import textwrap
        wrapped = textwrap.fill(note, width=55)
        for i, line in enumerate(wrapped.splitlines()):
            prefix = "  Note    : " if i == 0 else "           "
            print(f"{prefix}{line}")
    print("-" * width)

    recommendations = recommend_songs(prefs, songs, k=5)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"  #{rank}  {song['title']} — {song['artist']}")
        print(f"       Score : {score:.1f} / 90.0  [genre:20 mood:30 energy:40]")
        print(f"       Why   : {explanation}")
        print(f"       Genre : {song['genre']}  |  Mood : {song['mood']}  |  Energy : {song['energy']}")
        print()
    print("=" * width)


def main() -> None:
    songs = load_songs("data/songs.csv")

    for profile in PROFILES:
        print_profile_results(
            label=profile["label"],
            prefs=profile["prefs"],
            note=profile["note"],
            songs=songs,
        )


if __name__ == "__main__":
    main()
