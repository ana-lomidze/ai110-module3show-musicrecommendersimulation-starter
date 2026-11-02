# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  
## Scoring Approach

Think of the recommender like a friend who knows your taste and rates every song in the catalog from 0 to 100% on how well it fits you. Then they hand you the best few.

### What the model knows about each song

Each song has a genre (like lofi or pop), a mood (chill, happy, intense) and an artist. It also has a few numbers that describe how the song feels: energy, how acoustic it sounds, how upbeat it is (valence), how danceable it is, and its tempo.

### What the model knows about you

You can list favorite genres, moods and artists. You can also say how much energy you want and how acoustic you like your music. Valence, danceability and tempo are optional. If you don't say anything about one of these, the model ignores it and doesn't count it against a song.

### How it turns that into a score

The model checks each thing you care about, one at a time, and gives the song a mark from 0 to 1.

- **Genre, mood and artist** are a yes or no. If the song's genre is on your list, it gets full marks, and if not, zero.
- **The numbers** reward being *close* to what you asked for. If you want medium energy, a song with slightly lower or slightly higher energy still scores well, and one that is far off scores poorly. More isn't automatically better.

Not every feature matters equally. Genre counts the most, then mood, then energy, then artist, then acousticness, and the rest count a little. The final score is an average of all those marks, with the more important ones counting for more.

### How songs are ranked

The model sorts the songs from best to worst score. If two songs tie, the one whose energy is closer to your target wins. It shows you the top few, each with a short note on why it was picked.

### What I changed from the starter

The starter only knew a single favorite genre, a single favorite mood, a target energy and a yes/no "likes acoustic." I replaced that with lists of favorites, a target for how acoustic you want things, and an optional favorite-artist list. The starter code also did nothing yet. I built the part that reads the song catalog, the scoring, the ranking and the plain-English explanations. The output now shows each song's score and the reasons it matched.


---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 


Based on our experiments with the 22-song catalog:

- **Filter bubble**: Genre, mood and artist make up about 55% of the score (20 of 36 points), so users mostly get back the labels they already named, with little cross-genre discovery.
- **Exact match penalty**: Genre, mood and artist are scored 1 or 0, so near-misses get nothing. "Wistful" earns no credit for a "melancholy" fan, and "Willow Letters" scored only 0.30 for the classics user despite a very similar sound.
- **Thin catalog**: 18 genres and 18 moods across 22 songs means most genres have a single song. Users who like reggae, latin or country get one on-genre result and then loosely related filler.
- **Lofi and classical advantage**: Genres with several songs (lofi has 3, classical and pop have 2 each) give those users fuller, better-matched lists than users of one-song genres.
- **Energy overreach**: Energy is both weighted at 6 and the tiebreaker, so high-energy songs with no genre or mood match, like EDM and punk, filled the bottom of the rock user's top 5.
- **Single target per feature**: Each numeric preference is one value, so users who like both calm and intense music get averaged into the middle.
- **No diversity**: Pure score ranking let LoRoom take two of the top spots for the chill user.

---

## 7. Evaluation  

#### Profiles used for testing:
```
user_prefs_chill = {
    "favorite_genres": ["lofi", "jazz"],
    "favorite_moods": ["chill", "relaxed"],
    "target_energy": 0.40,
    "favorite_artists": ["LoRoom"],
    "target_acousticness": 0.80,
}

user_prefs_rock = {
    "favorite_genres": ["rock", "metal"],
    "favorite_moods": ["intense"],
    "target_energy": 1.0,
    "favorite_artists": ["Voltline"],
}

user_prefs_classic = {
    "favorite_genres": ["classical"],
    "favorite_moods": ["melancholy"],
    "target_energy": 0.20,
    "favorite_artists": ["Clara Whitfield"],
    "target_acousticness": 0.99,
}
```

The chill user was my first test. This user was created while implementing the logic behind the recommendations. It was added to the code during the testing phase to see if the results were as expected.

With the rock user, I wanted to see how much the genres would effect the recommendation.

When looking through the recommendations for the classics user, I wanted to see how much of an effect would favorite artist have. I was really happy with the result becuase it didn't prioritize the favorite artist. I took this mainly from my own experience with song recommendation platforms. I don't like it when I get the same artists recommended over and over. I like having my favorite artist as a suggestion for the system to take as a "here's the vibes I like."


---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
