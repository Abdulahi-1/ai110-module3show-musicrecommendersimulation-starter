# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

This version, called **MelodyMap**, scores every song in a small curated catalog against a user profile that captures a favorite genre, a preferred mood, and a target energy level. Each song earns up to 90 points: 20 for a genre match, 30 for a mood match, and up to 40 for how closely its energy level matches the user's target. The top five songs are returned with a plain-language explanation of which features matched. Compared to the starter defaults, the genre and energy weights were deliberately swapped (genre 40→20, energy 20→40) to test whether energy proximity could carry more of the ranking signal when a user's preferred genre is thin in the catalog. Six user profiles — three normal and three adversarial — were used to evaluate the system.

---

## How The System Works

Real-world recommenders like Spotify or YouTube analyze patterns across millions of songs and users, matching what you listen to against item attributes, listening history, and the behavior of similar users. This simulation focuses on the content-based side of that: it scores each song directly against what a user says they like, without needing any data from other users. The system prioritizes the three features that carry the most signal in a small catalog, genre, mood, and energy because together they capture both the style of a song and the context it fits (working out, studying, relaxing). A song earns points for matching the user's preferred genre, matching their mood, and having an energy level close to their target. The top-scoring songs become the recommendations.

### Song Features

| Feature | Type | Role |
|---|---|---|
| `genre` | categorical | Primary style signal (pop, lofi, rock, ambient, jazz, synthwave, indie pop) |
| `mood` | categorical | Context signal (happy, chill, intense, relaxed, focused, moody) |
| `energy` | float 0.0–1.0 | Intensity match against user's target energy |

### UserProfile Fields

| Field | Type | Role |
|---|---|---|
| `favorite_genre` | string | Matched against `song.genre` for the largest score contribution |
| `favorite_mood` | string | Matched against `song.mood` for the second-largest score contribution |
| `target_energy` | float 0.0–1.0 | Compared to `song.energy`; closer = higher score |

### Algorithm Recipe

Each song is scored out of 100 points using three steps applied in order:

**Step 1 — Genre match (40 pts)**
```
if song.genre == user.favorite_genre:
    score += 40
```

**Step 2 — Mood match (30 pts)**
```
if song.mood == user.favorite_mood:
    score += 30
```

**Step 3 — Energy proximity (0–20 pts)**
```
score += (1 - abs(song.energy - user.target_energy)) * 20
```

After all songs are scored, they are sorted by score descending and the top K are returned with an explanation of which features matched.

### Potential Biases

- **Genre dominance** — genre carries 40% of the total score, so a perfect genre match with the wrong mood will still rank higher than a perfect mood match with the wrong genre. A great song in an adjacent genre (e.g. indie pop when the user asked for pop) will be penalized even if it fits the mood and energy perfectly.
- **Binary genre and mood matching** — genre and mood are either a full match or zero; there is no partial credit for related categories (e.g. lofi and ambient are both chill but score differently). This makes the system brittle at genre boundaries.
- **Energy as a tiebreaker only** — with a maximum of 20 pts, energy can never overcome a genre or mood mismatch on its own, so the system may miss songs that are a near-perfect energy fit but differ in genre.
- **Catalog imbalance** — if the catalog has more songs in one genre than another, users who prefer that genre will always have more candidates to draw from, making their recommendations appear stronger.

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

## Experiments You Tried

**Weight shift — genre 40→20, energy 20→40**
Halving the genre weight and doubling the energy weight caused a visible rank change in the High-Energy Pop profile: *Rooftop Lights* jumped from third to second because its mood match outweighed *Gym Hero*'s genre match once genre became cheaper. This confirmed that the relative weight of each feature has a real, traceable effect on results.

**Adversarial profile — non-existent mood (`sad`)**
Requesting `mood: sad` (a label not present in the catalog) meant the mood branch never fired. Genre and energy alone shaped every result, which revealed how silently the system degrades when a user's preference has no match — no error, just subtly wrong rankings.

**Adversarial profile — lofi genre at max energy (`energy: 1.0`)**
Lofi songs cluster around energy 0.3–0.4. Requesting `energy: 1.0` imposed a heavy energy penalty on every lofi track, narrowing the gap between the lofi genre-and-mood matches and unrelated pop songs to as little as 30 points. This showed that energy can override genre loyalty when the two signals pull in opposite directions.

**Adversarial profile — genre absent from catalog (`classical`)**
When the requested genre does not appear at all, the genre bonus never fires and the entire ranking is decided by mood and energy proximity alone. The top results in this case were musically unrelated to classical; the system had no fallback for stylistic similarity.

**Six-profile sweep (3 normal + 3 adversarial)**
Testing all six profiles side-by-side made the catalog depth problem concrete: a lofi listener gets a genre bonus on three songs, while a rock or jazz listener gets it on exactly one, so positions 2–5 for niche-genre users are filled by energy proximity rather than actual genre affinity.

---

## Limitations and Risks

- **Tiny catalog** — the base dataset has 10 songs and most genres appear only once or twice, so the system frequently falls back to energy proximity rather than true genre affinity for positions 2–5.
- **Binary genre and mood matching** — a song either matches exactly or scores zero; there is no partial credit for adjacent categories (e.g., "chill" and "relaxed" are treated as completely different even though they overlap in practice).
- **Unused features** — `tempo_bpm`, `valence`, `danceability`, and `acousticness` are stored in the CSV but the scoring function ignores them entirely, meaning a large portion of each song's description is invisible to the recommender.
- **Unsigned energy gap** — "too quiet" and "too loud" are penalized equally, so a gym user asking for energy 0.95 can still receive a quiet ambient track in their top 5 if no genre or mood match exists.
- **No personalization over time** — the profile is static; the system has no way to learn from skips, replays, or listening history.
- **Silent degradation on missing labels** — if a user requests a genre or mood that does not appear in the catalog, the system returns results without any warning, and the recommendations can look plausible while being completely unrelated to what the user actually wanted.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

The biggest lesson from building MelodyMap is that scoring weights are a design decision, not a neutral technical choice. Changing genre from 40 points to 20 and energy from 20 to 40 was a small edit in one function, but it visibly reshuffled the top-5 results for multiple profiles. Real recommenders make the same kind of choice at much larger scale every weight, threshold, and feature selection encodes an assumption about what listeners care about and those assumptions can quietly disadvantage users whose preferences don't fit the dominant pattern.

The adversarial profiles made the fairness dimension concrete. A user whose preferred genre doesn't appear in the catalog gets results that look confident but are essentially random with respect to genre. A user whose favorite mood label is absent loses 30 points on every song without any indication that something went wrong. In a production system, those silent failures would show up as churn or disengagement rather than an error message, making them easy to overlook. Building even a toy recommender made it clear why diverse training data, partial-match credit for related categories, and explicit feedback mechanisms all matter not as nice-to-haves, but as the difference between a system that serves most users well and one that serves only the users whose tastes already match the catalog's assumptions.


---

## MelodyMap In Action

<img width="1036" height="364" alt="Screenshot 2026-04-12 at 7 46 52 PM" src="https://github.com/user-attachments/assets/1f986eaf-8517-4830-9580-ae4ee376c9a0" />

<img width="1036" height="364" alt="Screenshot 2026-04-12 at 7 53 39 PM" src="https://github.com/user-attachments/assets/13f517e6-ffb1-430b-a314-d3d753c60734" />


