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

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n🎵 Top recommendations:\n")
    for idx, rec in enumerate(recommendations, 1):
        song, score, reasons = rec
        print(f"{idx}. {song['title']}")
        print(f"   Score: {score:.2f}")
        print(f"   Why:")
        for reason in reasons:
            print(f"     • {reason}")
        print()


if __name__ == "__main__":
    main()
