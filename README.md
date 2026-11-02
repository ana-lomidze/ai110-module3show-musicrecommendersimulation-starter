# 🎵 Music Recommender Simulation

## Project Summary

This project is a content-based music recommender that suggests songs to a user by comparing song attributes (genre, mood, artist, energy, acousticness and more) against a user "taste profile," instead of using other listeners' behavior. Each song gets a weighted score from 0 to 1 and a short explanation of why it was picked.

---

## How The System Works

Real-world song recommendation platforms like YouTube and Spotify use a combination of methods to recommend songs.

### YouTube
Uses Content-based filtering and collaborative filtering.

**Content-based filtering** describes items by analyzing the content itself. YouTube's system processes signals like audio, visuals, video titles, descriptions, and tags to understand how each video compares to others.

**Collaborative filtering** is a technique used in recommendation systems that analyzes user behavior to find commonalities between users. In the context of YouTube, it identifies relationships between videos based on user behavior. So two videos become more similar as more of the same viewers watch them.

In addition, YouTube models the user as a complex and evolving "vector" built with the following types of data:
- Long-term watch history: captures a user's historic interests and preference.
- Short-term sessions behavior: reflects on the current user behavior and preference.
- Demographic and environment: adds context based on current device, location, time of day, etc. to the user's profile.


### Spotify
Combines collaborative filtering, NLP on text about music, and raw audio analysis.

For each song, Spotify collects two main data types: artist-provided metadata and raw audio analysis.
- Metadata: Tagged onto each song by the artist. Contains information like artist, song title, album, and genre.
- Raw Audio Analysis: Includes detailed information about the track itself. Things like bpm, loudness, and key. With this information and complex knowledge of music theory, Spotify's algorithm assigns values to every song in three categories: danceability, energy, and valence.

Along with this kind of data collection and categorization, Spotify uses natural language processing (NLP) models to gather information about the music in a more text-based context. For example, analyzing the lyrics or user-created playlist titles.

Spotify also uses collaborative filtering. As explained in the YouTube section, this technique involves analyzing user behavior and finding commonalities between users.


### My Music Recommendation System
My recommender is **content-based**: it compares each song's attributes to a user's taste profile and ranks songs by how closely they match. It doesn't use other users' behavior, because the dataset has no listening history.

#### Features

**Song** (from `data/songs.csv`): genre, mood, energy, artist, acousticness, valence, danceability, tempo_bpm.

**UserProfile** stores the user's preferences for those same features: favorite genres, favorite moods, target energy, favorite artists, target acousticness, and optional targets for valence, danceability and tempo.

Example profile (a chill lofi listener):

​```python
user_prefs = {
    "favorite_genres": ["lofi", "jazz"],
    "favorite_moods": ["chill", "relaxed"],
    "target_energy": 0.40,
    "favorite_artists": ["LoRoom"],
    "target_acousticness": 0.80,
}
​```

#### Scoring Rule (one song)

Each feature produces a similarity between 0 and 1, and the song's score is a weighted average of those similarities:

$$\text{score}(u, s) = \frac{\sum_{i \in A} w_i \cdot \text{sim}_i(u, s)}{\sum_{i \in A} w_i}$$

$A$ is the set of features the user gave a preference for. Features without a preference are skipped and the remaining weights are renormalized, so a missing preference never counts as a mismatch.

**Weights** follow my ranking of how much each feature matters:

| Rank | Feature | Weight |
|---|---|---|
| 1 | genre | 8 |
| 2 | mood | 7 |
| 3 | energy | 6 |
| 4 | artist | 5 |
| 5 | acousticness | 4 |
| 6 | valence | 3 |
| 7 | danceability | 2 |
| 8 | tempo_bpm | 1 |

**Categorical features** (genre, mood, artist): the user gives a short list for each (e.g. `favorite_genres`). Similarity is 1 if the song's value is in the list, otherwise 0.

**Numeric features** (energy, acousticness, valence, danceability, tempo): similarity rewards songs that are *close* to the user's target, not songs with higher or lower values:

$$\text{sim}(x, t) = 1 - \frac{|x - t|}{R}$$

$x$ is the song's value, $t$ is the user's target, and $R$ is the largest possible gap. $R = 1$ for the 0–1 features. Tempo is normalized over 60–180 BPM, so $R = 120$. For acousticness, $t$ is the user's `target_acousticness`.

#### Ranking Rule (list of songs)

1. Score every song with the scoring rule.
2. Sort by score, highest first.
3. Break ties by closeness on energy.
4. Return the top *k* songs, each with an explanation of which features matched.

The scoring rule says how good one song is for one user. The ranking rule decides which songs to show and in what order. Keeping them separate means list-level concerns like ties, top-k cutoffs and diversity don't have to be built into the per-song score, and each can be tested and changed independently.

#### Known Limitations

- Genre and mood still require exact matches against the user's lists, so near-matches outside them, such as "pop" and "indie pop", get no partial credit. Long lists make every song match, so lists should stay short (2–3 items).
- Energy, tempo and acousticness are correlated in this data, so they partly count the same signal.

#### Potential Biases
- **Labels dominate.** Genre and mood together make up roughly half of the score (15 of 30 points when five features are active). A song that fits the user's energy and acousticness almost perfectly can still rank low if its genre and mood labels aren't in the user's lists.
- **The artist bonus favors the familiar.** Favorite-artist matches get a bonus, which works against discovering new artists.
- **Mood labels are subjective.** Moods like "chill," "relaxed" and "focused" feel close but score as total mismatches unless the user lists all of them.

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
```
============================================================
 TOP 5 RECOMMENDATIONS
 Profile: genres=pop | moods=happy | energy=0.80
============================================================

#1  Sunrise City - Neon Echo
    Score: 0.99
    Why:
      - genre match: pop (+8)
      - mood match: happy (+7)
      - energy 0.82 vs target 0.8 (sim 0.98)
------------------------------------------------------------

#2  Gym Hero - Max Pulse
    Score: 0.63
    Why:
      - genre match: pop (+8)
      - energy 0.93 vs target 0.8 (sim 0.87)
------------------------------------------------------------

#3  Rooftop Lights - Indigo Parade
    Score: 0.61
    Why:
      - mood match: happy (+7)
      - energy 0.76 vs target 0.8 (sim 0.96)
------------------------------------------------------------

#4  Concrete Crown - Kid Meridian
    Score: 0.28
    Why:
      - energy 0.78 vs target 0.8 (sim 0.98)
------------------------------------------------------------

#5  Calle Sol - Los Faroles
    Score: 0.27
    Why:
      - energy 0.84 vs target 0.8 (sim 0.96)
------------------------------------------------------------
```


### Other User Prefrence Outputs

```
============================================================
 TOP 5 RECOMMENDATIONS
 Profile: genres=lofi, jazz | moods=chill, relaxed | energy=0.40
============================================================

#1  Midnight Coding - LoRoom
    Score: 0.98
    Why:
      - genre match: lofi (+8)
      - mood match: chill (+7)
      - energy 0.42 vs target 0.4 (sim 0.98)
      - artist match: LoRoom (+5)
      - acousticness 0.71 vs target 0.8 (sim 0.91)
------------------------------------------------------------

#2  Coffee Shop Stories - Slow Stereo
    Score: 0.82
    Why:
      - genre match: jazz (+8)
      - mood match: relaxed (+7)
      - energy 0.37 vs target 0.4 (sim 0.97)
      - acousticness 0.89 vs target 0.8 (sim 0.91)
------------------------------------------------------------

#3  Library Rain - Paper Lanterns
    Score: 0.82
    Why:
      - genre match: lofi (+8)
      - mood match: chill (+7)
      - energy 0.35 vs target 0.4 (sim 0.95)
      - acousticness 0.86 vs target 0.8 (sim 0.94)
------------------------------------------------------------

#4  Focus Flow - LoRoom
    Score: 0.76
    Why:
      - genre match: lofi (+8)
      - energy 0.4 vs target 0.4 (sim 1.00)
      - artist match: LoRoom (+5)
      - acousticness 0.78 vs target 0.8 (sim 0.98)
------------------------------------------------------------

#5  Spacewalk Thoughts - Orbit Bloom
    Score: 0.53
    Why:
      - mood match: chill (+7)
      - energy 0.28 vs target 0.4 (sim 0.88)
      - acousticness 0.92 vs target 0.8 (sim 0.88)
------------------------------------------------------------
============================================================
 TOP 5 RECOMMENDATIONS
 Profile: genres=rock, metal | moods=intense | energy=1.00
============================================================

#1  Storm Runner - Voltline
    Score: 0.98
    Why:
      - genre match: rock (+8)
      - mood match: intense (+7)
      - energy 0.91 vs target 1.0 (sim 0.91)
      - artist match: Voltline (+5)
------------------------------------------------------------

#2  Ironclad Fury - Black Ember
    Score: 0.53
    Why:
      - genre match: metal (+8)
      - energy 0.97 vs target 1.0 (sim 0.97)
------------------------------------------------------------

#3  Gym Hero - Max Pulse
    Score: 0.48
    Why:
      - mood match: intense (+7)
      - energy 0.93 vs target 1.0 (sim 0.93)
------------------------------------------------------------

#4  Strobe Cathedral - Pulse Theory
    Score: 0.22
    Why:
      - energy 0.95 vs target 1.0 (sim 0.95)
------------------------------------------------------------

#5  Parking Lot Anthem - Rusty Halo
    Score: 0.22
    Why:
      - energy 0.94 vs target 1.0 (sim 0.94)
------------------------------------------------------------
============================================================
 TOP 5 RECOMMENDATIONS
 Profile: genres=classical | moods=melancholy | energy=0.20
============================================================

#1  Nocturne for Rain - Elena Voss
    Score: 0.83
    Why:
      - genre match: classical (+8)
      - mood match: melancholy (+7)
      - energy 0.18 vs target 0.2 (sim 0.98)
      - acousticness 0.97 vs target 0.99 (sim 0.98)
------------------------------------------------------------

#2  Morning Sonata - Clara Whitfield
    Score: 0.71
    Why:
      - genre match: classical (+8)
      - energy 0.45 vs target 0.2 (sim 0.75)
      - artist match: Clara Whitfield (+5)
      - acousticness 0.96 vs target 0.99 (sim 0.97)
------------------------------------------------------------

#3  Spacewalk Thoughts - Orbit Bloom
    Score: 0.31
    Why:
      - energy 0.28 vs target 0.2 (sim 0.92)
      - acousticness 0.92 vs target 0.99 (sim 0.93)
------------------------------------------------------------

#4  Willow Letters - Juniper & Moth
    Score: 0.31
    Why:
      - energy 0.3 vs target 0.2 (sim 0.90)
      - acousticness 0.93 vs target 0.99 (sim 0.94)
------------------------------------------------------------

#5  Library Rain - Paper Lanterns
    Score: 0.29
    Why:
      - energy 0.35 vs target 0.2 (sim 0.85)
      - acousticness 0.86 vs target 0.99 (sim 0.87)
------------------------------------------------------------

```


**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

**Different types of users**

I ran three profiles against the 22-song catalog:

- **Chill (lofi/jazz, chill/relaxed, energy 0.40, artist LoRoom)**: The top result was "Midnight Coding" (0.98), matching on genre, mood, energy and artist. The rest of the list was sensible low-energy, acoustic songs.
- **Rock (rock/metal, intense, energy 1.0, artist Voltline)**: "Storm Runner" scored 0.98 and the next result dropped to 0.53. Ranks #4 and #5 (EDM and punk) scored 0.22 on energy similarity alone.
- **Classical (classical, melancholy, energy 0.20, acousticness 0.99, artist Clara Whitfield)**: "Nocturne for Rain" by Elena Voss ranked #1 (0.83) over the favorite-artist song "Morning Sonata" (0.71), because Morning Sonata is uplifting and higher-energy.

**Raising the artist weight**

I temporarily changed the weights from genre 8, mood 7, artist 5 to genre 7, mood 6, artist 8, then reverted them.

- **Classical**: The top two swapped. "Morning Sonata" took #1 (0.75) over "Nocturne for Rain" (0.74), so a 0.01 gap put an upbeat song first for a user who asked for melancholy.
- **Chill**: "Focus Flow" (LoRoom) moved from #4 to #2 (0.80), ahead of two songs that matched the user's genre and mood but not the artist.
- **Rock**: The order stayed the same. The #1 song already matched the artist, and it rose to 0.98.

I kept the original weights because the higher artist weight let a name match override the user's stated mood. It also gave an advantage to artists with several songs in the catalog.

---

## Limitations and Risks

- **Tiny catalog**: With 22 songs, 15 of the 18 genres and 15 of the 18 moods have only one song, so users of those genres get one on-genre result and then filler.
- **Exact-match labels**: Genre, mood and artist score 1 or 0, so near-misses like "wistful" vs. "melancholy" get no credit. These three features are also about 55% of the score, which creates a filter bubble.
- **Limited features**: It doesn't use lyrics, language, popularity or listening history, and each numeric preference is a single target value, so users with varied taste get averaged into the middle.
- **Energy overreach**: Energy is both weighted at 6 and the tiebreaker, so high-energy songs with no genre or mood match can still fill the bottom of a top 5.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Building this showed me that a recommender is really a set of choices about what counts. Each song and user is turned into a few numbers and labels, and a weighted score decides the ranking. Small choices mattered a lot: raising the artist weight from 5 to 8 changed one score by only 0.01, but it flipped the classics user's top pick to an upbeat song they hadn't asked for. The explanations I attached to each result made this easy to see, since I could tell exactly which feature pushed a song up or down.

