"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")

    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print()
    print("=" * 44)
    print(f"  User Profile")
    print(f"  Genre: {user_prefs['genre']}  |  Mood: {user_prefs['mood']}  |  Energy: {user_prefs['energy']}")
    print("=" * 44)
    print()

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"  #{rank}  {song['title']} — {song['artist']}")
        print(f"       Score : {score:.1f} / 90.0")
        print(f"       Why   : {explanation}")
        print(f"       Genre : {song['genre']}  |  Mood : {song['mood']}  |  Energy : {song['energy']}")
        print()

    print("=" * 44)


if __name__ == "__main__":
    main()
