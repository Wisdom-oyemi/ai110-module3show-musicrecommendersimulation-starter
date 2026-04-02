from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

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
        ranked_songs = sorted(self.songs, key=lambda song: _score_song_object(user, song)[0], reverse=True)
        return ranked_songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        return _score_song_object(user, song)[1]

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    int_fields = {"id"}
    float_fields = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}

    songs: List[Dict] = []
    with open(csv_path, mode="r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            song = dict(row)

            for field in int_fields:
                if field in song and song[field] != "":
                    song[field] = int(song[field])

            for field in float_fields:
                if field in song and song[field] != "":
                    song[field] = float(song[field])

            songs.append(song)
    return songs


def _normalize_user_prefs(user_prefs: Dict) -> Dict[str, object]:
    """
    Normalize user preferences to a consistent format.
    
    Converts user preference dictionary keys (genre/favorite_genre, mood/favorite_mood, etc.)
    to a standard format with lowercase genre and mood for case-insensitive matching.
    
    Args:
        user_prefs: Dictionary with keys like 'genre', 'mood', 'energy', 'likes_acoustic'
                   or 'favorite_genre', 'favorite_mood', 'target_energy', 'likes_acoustic'
    
    Returns:
        Dictionary with normalized keys: 'genre' (str, lowercase), 'mood' (str, lowercase),
        'energy' (float), 'likes_acoustic' (bool)
    """
    return {
        "genre": str(user_prefs.get("genre", user_prefs.get("favorite_genre", ""))).lower(),
        "mood": str(user_prefs.get("mood", user_prefs.get("favorite_mood", ""))).lower(),
        "energy": float(user_prefs.get("energy", user_prefs.get("target_energy", 0.0))),
        "likes_acoustic": bool(user_prefs.get("likes_acoustic", False)),
    }


def _score_components(user_genre: str, user_mood: str, target_energy: float, likes_acoustic: bool, song_genre: str, song_mood: str, song_energy: float, song_acousticness: float) -> Tuple[float, List[str]]:
    """
    Calculate a recommendation score and reasons based on the Algorithm Recipe.
    
    Scoring breakdown:
    - Genre match: +35 points
    - Mood match: +30 points
    - Energy closeness: up to +20 points (inversely proportional to absolute difference)
    - Acoustic preference: +15 points if user preference matches song acousticness
    
    Args:
        user_genre: User's preferred genre (lowercase)
        user_mood: User's preferred mood (lowercase)
        target_energy: User's target energy level (0.0-1.0)
        likes_acoustic: Whether user likes acoustic music
        song_genre: Song's genre
        song_mood: Song's mood
        song_energy: Song's energy level (0.0-1.0)
        song_acousticness: Song's acousticness level (0.0-1.0)
    
    Returns:
        Tuple of (score: float, reasons: List[str]) where reasons are human-readable
        explanations for why the song scored the way it did
    """
    score = 0.0
    reasons: List[str] = []

    if song_genre.lower() == user_genre:
        score += 35.0
        reasons.append(f"genre matches your preference ({song_genre})")

    if song_mood.lower() == user_mood:
        score += 30.0
        reasons.append(f"mood matches your preference ({song_mood})")

    energy_score = max(0.0, 20.0 * (1.0 - abs(float(song_energy) - target_energy)))
    score += energy_score
    reasons.append(f"energy is close to your target (+{energy_score:.1f})")

    acoustic_bonus = 0.0
    if likes_acoustic and song_acousticness >= 0.6:
        acoustic_bonus = 15.0
        reasons.append("it is acoustic enough for your taste")
    elif not likes_acoustic and song_acousticness <= 0.4:
        acoustic_bonus = 15.0
        reasons.append("it is not very acoustic, which fits your taste")

    score += acoustic_bonus

    if not reasons:
        reasons.append("it is a reasonable overall fit based on the scoring rules")

    return score, reasons


def _format_explanation(song: Dict, score: float, reasons: List[str]) -> str:
    """
    Format a scored song and its reasons into a single explanation string.
    
    Args:
        song: Song dictionary with at least a 'title' key
        score: The calculated recommendation score
        reasons: List of reason strings from _score_components
    
    Returns:
        A formatted string like: "Song Title scored 85.0 because reason1; reason2; reason3."
    """
    title = song.get("title", "This song")
    return f"{title} scored {score:.1f} because " + "; ".join(reasons) + "."


def _score_song_dict(user_prefs: Dict, song: Dict) -> Tuple[float, str]:
    """
    Score a song dictionary against user preferences.
    
    Combines normalization, component scoring, and explanation formatting.
    Used by the functional recommend_songs API.
    
    Args:
        user_prefs: User preference dictionary
        song: Song dictionary with audio features and metadata
    
    Returns:
        Tuple of (score: float, explanation: str)
    """
    normalized = _normalize_user_prefs(user_prefs)
    score, reasons = _score_components(
        normalized["genre"],
        normalized["mood"],
        float(normalized["energy"]),
        bool(normalized["likes_acoustic"]),
        str(song.get("genre", "")),
        str(song.get("mood", "")),
        float(song.get("energy", 0.0)),
        float(song.get("acousticness", 0.0)),
    )
    return score, _format_explanation(song, score, reasons)


def _score_song_object(user: UserProfile, song: Song) -> Tuple[float, str]:
    """
    Score a Song object against a UserProfile.
    
    Calculates components and formats explanation. Used by the OOP Recommender class.
    
    Args:
        user: UserProfile object with taste preferences
        song: Song object with audio features and metadata
    
    Returns:
        Tuple of (score: float, explanation: str)
    """
    score, reasons = _score_components(
        user.favorite_genre.lower(),
        user.favorite_mood.lower(),
        float(user.target_energy),
        bool(user.likes_acoustic),
        song.genre,
        song.mood,
        float(song.energy),
        float(song.acousticness),
    )
    return score, f"{song.title} scored {score:.1f} because " + "; ".join(reasons) + "."

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, List[str]]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    
    Returns:
        List of tuples: (song_dict, score, reasons_list)
        where reasons_list contains human-readable explanations for the score
    """
    ranked_results = []

    for song in songs:
        normalized = _normalize_user_prefs(user_prefs)
        score, reasons = _score_components(
            normalized["genre"],
            normalized["mood"],
            float(normalized["energy"]),
            bool(normalized["likes_acoustic"]),
            str(song.get("genre", "")),
            str(song.get("mood", "")),
            float(song.get("energy", 0.0)),
            float(song.get("acousticness", 0.0)),
        )
        ranked_results.append((song, score, reasons))

    ranked_results.sort(key=lambda item: item[1], reverse=True)
    return ranked_results[:k]
