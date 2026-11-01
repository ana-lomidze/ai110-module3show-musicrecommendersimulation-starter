# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world song recommendation platforms like YouTube and Spotify use a combination of methods to recommend songs.

### YouTube
Uses Content-based filtering and collaborative filtering.

**Content-based filtering** describes times by analyszing the content itself. YouTube's system processes signals like audio, visuals, video titles, descriptions, and tags to understand how each video compare to others.

**Collaborative filtering** is a technique used in recommendation systems that analyzes user behvior to find commonalities between users. In the context of YouTube, it identifies relationships between videos based on user behvior. So two videos become more similar as more of the same viewers watch them.

In addition, YouTube models the user as a complex and evolving "vector" built with the following types of data:
- Long-term watch history: captures a user's historic interests and preference.
- Short-term sessions behavior: refeclts on the current user behvior and prefernce.
- Demographic and environment: adds context based on current device, location, time of day, etc. to the user's profile.


### Spotify
Combines collaborative filtering, NLP on text about music, and raw audio analysis.

For each song, Spotify colllects two main data types: artisit-provided metadata and raw audio analysis.
- Metadata: Tagged onto each song by the artist. Contains information like artist, song title, album, and genre.
- Raw Audio Analysis: Includes detailed information about the track itself. Things like bpm, loudness, and key. With this information and complex knowlege of music theory, Spotify's algorithm assigns values to every song in three categories: danceability, energy, and valence.

Along with this kind of data collection and categorization, Spotify uses natural language processing (NLP) modetls to gather information about the music in a more text-based context. For example, analyzing the lyrics or user-created playlist titles.

Spotify also uses collaborative filtering. As explained in the YouTube section, this technique involves analzying user behavior and finding commonalities between users.


### My Music Recommenation System
My recommender is **content-based**: it compares each song's attributes to a user's taste profile and ranks songs by how closely they match. It doesn't use other users' behavior, because the dataset has no listening history.

#### Features

**Song** (from `data/songs.csv`): genre, mood, energy, artist, acousticness, valence, danceability, tempo_bpm.

**UserProfile** stores the user's preferences for those same features: favorite genre, favorite mood, target energy, favorite artists, whether they like acoustic music, and optional targets for valence, danceability and tempo.

#### Scoring Rule (one song)

Each feature produces a similarity between 0 and 1, and the song's score is a weighted average of those similarities:

$$\text{score}(u, s) = \frac{\sum_{i \in A} w_i \cdot \text{sim}_i(u, s)}{\sum_{i \in A} w_i}$$

$A$ is the set of features the user gave a preference for. Features without a preference are skipped and the remaining weights are renormalized, so a missing preference never counts as a mismatch.

**Weights** follow my ranking of how much each feature matters:

| Rank | Feature | Weight |
|---|---|---|
| 1 | energy | 8 |
| 2 | genre | 7 |
| 3 | mood | 6 |
| 4 | artist | 5 |
| 5 | acousticness | 4 |
| 6 | valence | 3 |
| 7 | danceability | 2 |
| 8 | tempo_bpm | 1 |

**Categorical features** (genre, mood, artist): similarity is 1 if the song matches the preference, otherwise 0.

**Numeric features** (energy, acousticness, valence, danceability, tempo): similarity rewards songs that are *close* to the user's target, not songs with higher or lower values:

$$\text{sim}(x, t) = 1 - \frac{|x - t|}{R}$$

$x$ is the song's value, $t$ is the user's target, and $R$ is the largest possible gap. $R = 1$ for the 0–1 features. Tempo is normalized over 60–180 BPM, so $R = 120$. For acousticness, "likes acoustic" sets the target to 1 and otherwise to 0.

#### Ranking Rule (list of songs)

1. Score every song with the scoring rule.
2. Sort by score, highest first.
3. Break ties by closeness on energy.
4. Return the top *k* songs, each with an explanation of which features matched.

The scoring rule says how good one song is for one user. The ranking rule decides which songs to show and in what order. Keeping them separate means list-level concerns like ties, top-k cutoffs and diversity don't have to be built into the per-song score, and each can be tested and changed independently.

#### Known Limitations

- Genre and mood require exact matches, so near-matches such as "pop" and "indie pop" get no partial credit.
- Energy, tempo and acousticness are correlated in this data, so they partly count the same signal.


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

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



