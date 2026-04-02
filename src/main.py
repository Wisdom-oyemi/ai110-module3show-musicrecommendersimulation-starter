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

    # Example profiles (starter + adversarial/edge-case profiles)
    example_profiles = {
        "starter_pop": {"genre": "pop", "mood": "happy", "energy": 0.8},
        "energy_too_high": {"genre": "pop", "mood": "happy", "energy": 2.5, "likes_acoustic": False},
        "energy_negative": {"genre": "lofi", "mood": "chill", "energy": -1.0, "likes_acoustic": True},
        "unknown_tags": {"genre": "unknown_genre", "mood": "unknown_mood", "energy": 0.35, "likes_acoustic": True},
        "whitespace_case_noise": {"genre": "  POP  ", "mood": "HaPpY ", "energy": 0.82, "likes_acoustic": False},
        "string_boolean_trap": {"genre": "lofi", "mood": "chill", "energy": 0.4, "likes_acoustic": "False"},
        "ties_likely": {"genre": "", "mood": "", "energy": 0.5, "likes_acoustic": False},
    }

    # Pick any key from example_profiles to try a different scenario.
    user_prefs = example_profiles["ties_likely"]

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
