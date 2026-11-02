# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeFinder 1.0**  

---

## 2. Intended Use  

This recommender suggests the top 5 songs from a small 22-song catalog, based on a user's stated preferences. Each song gets a score from 0 to 1 and a short explanation of why it was picked (for example, "genre match: classical (+8)"). Users can give favorite genres, moods and artists, plus target values for energy, acousticness, valence, danceability and tempo.

**Assumptions about the user**
- The user knows their taste and can state it up front. There is no listening history or feedback.
- Their taste can be described as a short list of liked labels plus one target value per numeric feature.
- Every preference they give matters. Features they leave out are ignored, not treated as neutral.

**Intended use**
This is for classroom exploration only. It is not meant for real users or a real product.
 

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

There are 22 total songs - originally 10; I added 12 songs - in the catalog with 18 distinct genres and moods:
**Genres**
- lofi (3)
- pop (2)
- classical (2)
- rock, ambient, jazz, synthwave, indie pop, hip hop, country, reggae, metal, r&b, edm, folk, shoegaze, latin and punk

**Moods**
- chill (3)
- happy (2)
- intense(2)
- relaxed, moody, focused, confident, melancholy, nostalgic, carefree, angry, romantic, euphoric, wistful, uplifting, dreamy, festive and rebellious

I think the current catalog has a fairly wide range of songs for such a small dataset. However, adding more songs to the catalog would be very helpful. It's hard to gauge how good a recommendation system is when there aren't a lot of the same artist, genre, mood, etc.

---

## 5. Strengths  

- **Works well for users with clear, consistent tastes**: The chill (lofi/jazz) and rock profiles got top results that matched on genre, mood, energy and artist.
- **Artist acts as a suggestion, not an override**: Artist is weighted below genre and mood. When I temporarily raised it above both for testing, the classics user's #1 became an upbeat song they hadn't asked for, so I kept it at 5.
- **Transparent**: Each recommendation lists exactly which features contributed, which made it easy to see why results changed.

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

- Adding a UI to prompt the user to fill in their prefences.
- Letting a user add songs they like. This would give a simulated 'listening history.' This can also give the users the opportunity to be more direct with the type of recommendation they want to get from the model.
- Add more songs to the catalog. Having 22 songs is very limiting.

---

## 9. Personal Reflection  

I was assigned a very similar project in high school and funnily enough, my approach back then wasn't too far off from what I ended up doing here.

I also really enjoyed research exisiting recommendation systsms and seeing what happens "under the hood" for apps I use daily. The biggest thing I learned is how much small choices matter: raising the artist weight from 5 to 8 only changed one score by 0.01, but it flipped the top pick for the classics user to a song that didn't fit the mood they asked for. I also didn't expect a tiny 22-song catalog to produce such clear filter bubbles. It makes me wonder how much of what feels like an app "knowing my taste" is really it reinforcing what I already listen to.
