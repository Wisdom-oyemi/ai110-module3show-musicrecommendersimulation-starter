# 🎵 Music Recommender Simulation

## Project Summary

This project aims to create a recommendation system of songs for a user based on their preferences and past song choices.

---

## How The System Works

Real-world song recommendations are driven by algorithm paths that analyze user-system interactions and build a sort of "profile." That profile is made up of aggregated actions (like play, like, skip, repeat, etc.) which are used to rank songs and assign similar songs based on other profiles' similar attributes. My particular version of this model will prioritize a content-based approach to assigning similar songs, using certain qualities of a given song to "score" and "rank" them by order of compatibility, greatest to least.

The Song object will contain features that are attributes of the song itself (for ranking and scoring purposes), and the UserProfile object will contain data on the amount and type of interactions the user has with the system, as well as their preferred music taste.

Algorithm Recipe:
Genre: +35 if match, otherwise 0
Mood: +30 if match, otherwise 0
Energy: up to +20 using closeness
Energy score = 20 × (1 - abs(song.energy - user.target_energy))
Hard minimum at 0
Acoustic:
If user likes acoustic and song.acousticness >= 0.6: +15
If user does not like acoustic and song.acousticness <= 0.4: +15
Otherwise 0

Brief Note: above system may prioritize exact matches over songs in a slightly lower but acceptable range

Sample terminal recommendation:
![alt text](<Screenshot 2026-04-01 215603.png>)

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

---

## Experiments Tried

Included here are a few screenshots resulting from edge-case testing in main.py:
![alt text](<Screenshot 2026-04-01 222702.png>) ![alt text](<Screenshot 2026-04-01 222743.png>) ![alt text](<Screenshot 2026-04-01 222843.png>) ![alt text](<Screenshot 2026-04-01 222924.png>) ![alt text](<Screenshot 2026-04-01 223003.png>) ![alt text](<Screenshot 2026-04-01 223104.png>)

---

## Limitations and Risks


- It works best on a small dataset (e.g. a semi-short song playlist)
- It might over favor one genre or mood over another

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

Data from any source is converted into recommendations via mathematical/algorithmic processes that judge input based on a predefined scoring metric. That is to say, any given data input will be assigned (or totaled up to) a particular score based on how much its attributes line up to the ideal attributes defined by the user/programmer. As a result, the data with the best total scores are "recommended" in collusion to the previously-made choice. Biases and inconsistency can slip unnoticed into these scoring methods based on the training dataset given to the algorithm or even just the stipulations of the scoring system itself. For instance, if training data is heavily skewed toward a specific genre of music, and the scoring metrics favor genre association over mood or danceability association, pop music will be more recommended to the user.


---

## 7. `Model Card`


```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

> VibeCheck v1

---

## 2. Intended Use

> This model suggests 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for exploration and testing only, not for real users.

---

## 3. How It Works (Short Explanation)

The recommender is based on a semi-strict preference match algorithm. It bases its recommendations on a song's particular genre, mood, energy, and acoustic-ness. Each of these factors are assigned a score based on how close the queued song is to the current song the user is listening to (and the overall preferences of the user), and the total f all those scores is the final likelihood that the song is a close match.

---

## 4. Data

Describe your dataset.
18 songs are in the primary dataset of `data/songs.csv`. The last 8 songs were added as extra data for testing and function implementation. This data file represents a variety of genres and moods, from pop and lo-fi to classical and country; it represents a diverse music taste very similar to my own.

---

## 5. Strengths

The recommender model works well at its basic computation of similar songs to a given input/sample profile. It also has a streamlined CLI/terminal output with explanations for the evaluation.

---

## 6. Limitations and Bias

The recommender tends to be biased toward pop or pop-adjacent song genres due to the initial dataset being mostly populated with pop music, and it is also potentially unable to differentiate different factors that could tip the favor of one song against another.

---

## 7. Evaluation

The system was evaluated in the following ways:
- Used multiple user profiles (including edge cases) and jotted down the results
- Compared my simulation to my Spotify recommendations playlists (like On Repeat or Liked Songs)
- Created testsuite for the  scoring logic

---

## 8. Future Work

If more time was given to develop this program, I would try to:
- Include a diversity of song recommendations instead of formulating the closest match
- Potentially include more features for scoring/ranking, like tempo ranges or lyric themes

---

## 9. Personal Reflection

I learned a lot about the mechanisms that work behind recommender systems, in particular the kind of math that's done behind-the-scenes to ensure that the song/video being recommended matches the already played song/video. I was surprised by the simplicity of the logic (at a smaller scale, obviously), and it's inspiring to know that with a few extra components it would function rather well. Human judgement or review is still vastly important in the process, because the model may seem "smart" but actually just be a little more precise than advertised, NOT perfect.

