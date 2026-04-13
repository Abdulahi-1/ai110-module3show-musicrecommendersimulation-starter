# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeFinder 1.0**  

---

## 2. Intended Use  

VibeFinder 1.0 is a music recommendation simulation built for classroom exploration of how algorithmic recommenders work. Given a user profile that captures a favorite genre, a preferred mood, and a target energy level, the system returns the five songs from a small curated catalog that best match those preferences.

It is not a production product. There are no real users, no login data, and no streaming history. The system assumes that a person can accurately describe their taste with three fields — genre, mood, and energy — and that those three signals are sufficient to rank a catalog of songs. This is a deliberate simplification intended to make the mechanics of scoring and ranking visible and easy to reason about, rather than to reflect the full complexity of real listening behavior.  

---

## 3. How the Model Works  

Every song in the catalog has three features that matter for scoring: its genre label (such as "pop" or "lofi"), its mood label (such as "chill" or "intense"), and a number between 0 and 1 that captures how energetic the song feels, where 0 is very quiet and calm and 1 is very loud and driving.

A user profile carries the same three fields: a favorite genre, a favorite mood, and a target energy level. To rank the catalog, the system gives each song a score out of 90 points by checking three things in order. First, if the song's genre matches the user's favorite genre exactly, the song earns 20 points. Second, if the song's mood matches the user's favorite mood exactly, it earns another 30 points. Third, the system measures how close the song's energy is to the user's target energy — a perfect match gives 40 points, and the score scales down the further the song's energy drifts from the target. The three sub-scores are added together and the five highest-scoring songs are returned as the recommendation.

Compared to the original starter code, the genre and energy weights were swapped: genre was reduced from 40 points to 20, and energy was increased from 20 points to 40. This change was made to test whether energy proximity could carry more of the ranking signal when a user's preferred genre is barely represented in the catalog. The mood weight stayed at 30 points throughout.

---

## 4. Data  

The base catalog contains 10 songs stored in a CSV file with one row per song. Each row records the song's title, artist, genre, mood, energy level (0–1), tempo in beats per minute, valence, danceability, and acousticness. A second extended catalog adds 8 more songs for a combined total of 18, though the main simulation runs against the 10-song base catalog unless the extended file is loaded explicitly.

The 10 base songs span seven genres — pop, lofi, rock, ambient, jazz, synthwave, and indie pop — and six moods: happy, chill, intense, relaxed, moody, and focused. The 8 extended songs add hip-hop, R&B, classical, country, EDM, metal, folk, and soul, along with moods like sad, romantic, peaceful, nostalgic, energetic, angry, melancholic, and uplifting.

Both files were hand-authored for this classroom project, meaning the attribute values are plausible estimates rather than data pulled from a real music service. No songs were removed from the starter dataset; the extended file was added to give adversarial test profiles something to match against.

Several gaps remain. No genre appears more than twice in the base catalog, so users with niche tastes have at most two real matches before the system falls back entirely to energy proximity. Mood coverage is similarly thin — most mood labels appear on only one song. Acoustic attributes like valence, danceability, and acousticness are present in the data but are not used by the current scoring function at all, which means a significant share of each song's description is invisible to the recommender.  

---

## 5. Strengths  

The system works best for users whose preferred genre and mood both appear multiple times in the catalog. A chill lofi listener is the clearest example: the catalog contains three lofi tracks and two of them also carry the chill mood label, so when genre and mood both match, those songs land at the top of the ranking with scores in the high 80s out of 90, which feels genuinely right. The combination of a strong genre signal and a strong mood signal leaves almost no ambiguity about which songs belong at the top.

The energy scoring also behaves sensibly when it is playing a supporting role rather than the primary signal. For a high-energy pop listener, energy proximity correctly separated Gym Hero (energy 0.93) and Sunrise City (energy 0.82) from lower-energy tracks, and the rank order within the pop songs matched intuition. The continuous nature of the energy score means the system can distinguish between a song that is slightly off-target and one that is very far away, which binary scoring alone could not do.

The scoring is also transparent enough to reason about manually. Because there are only three additive components, it is straightforward to look at any result and explain exactly why it ranked where it did — a quality that matters a lot in a classroom setting where the goal is to understand how recommenders work, not just to use one.  

---

## 6. Limitations and Bias 


The most significant bias in the current system is that genre scoring is both binary and catalog-depth-dependent: a genre match awards a flat 20–40 points regardless of how many songs of that genre exist in the catalog, so a lofi fan receives a genre bonus on three songs while a rock or jazz fan receives it on exactly one. This creates a filter bubble for niche-genre users—after their single genre match, positions 2–5 are filled entirely by energy proximity, meaning a rock fan will consistently receive pop, synthwave, or ambient recommendations simply because those songs share a similar energy level, not because they are musically related. The same hard cliff appears in mood scoring: emotionally adjacent labels like "chill," "relaxed," and "focused" score zero against each other, so a user requesting "relaxed" loses all 30 mood points on every chill or focused track and can be outranked by a high-energy song that happens to be close in energy. Additionally, because the energy gap is calculated as an absolute unsigned distance, the system treats "too quiet" and "too loud" as equally bad penalties—a gym user asking for energy=0.95 gives an energy score of 11/40 to a quiet ambient track at 0.28, high enough to push it into the top 5 when no genre or mood match exists. Taken together, these binary thresholds mean the recommender silently ignores the partial similarity that a human listener would immediately recognise, and systematically under-serves users whose preferred genres or moods appear fewer than two times in the catalog.

---

## 7. Evaluation  


Six user profiles were tested in total: three normal taste profiles (High-Energy Pop, Chill Lofi, Deep Intense Rock) and three adversarial profiles designed to expose edge cases (a pop fan who wants a mood the catalog does not contain, a lofi fan requesting maximum energy, and a user whose genre does not exist in the catalog at all). For each profile, the top 5 results were inspected to check whether the score breakdown genre, mood, and energy matched the reasoning behind each recommendation. The normal profiles behaved as expected: when genre and mood both matched, the top result scored in the high 80s out of 90, which felt right. The most surprising result came from the Deep Intense Rock profile: after the single rock track took the top spot, every other recommendation was a non-rock song ranked purely by how close its energy was to 0.95 meaning the system effectively stopped thinking about genre after position 1. A second surprise was the Lofi Lover at Max Energy profile: even though genre and mood matched perfectly on two songs, requesting energy=1.0 penalised those songs so heavily that the gap between the lofi tracks and unrelated pop tracks narrowed to just 30 points, which felt like the energy signal was doing more work than intended. The weight-shift experiment (doubling energy from 20 to 40 points, halving genre from 40 to 20) caused a rank swap in the High-Energy Pop profile Rooftop Lights jumped from third to second because its mood match outweighed Gym Hero's genre match once genre became cheaper confirming that the relative weight of each feature has a real and observable effect on results.

---

## 8. Future Work  
  

The most urgent fix would be replacing binary genre and mood matching with graduated similarity scores. Right now a song either matches your genre completely or scores zero there is no middle ground for closely related genres like pop and indie pop, or adjacent moods like chill and relaxed. A simple lookup table of related genres and moods could award partial credit (say, 10 out of 20 points for a near-match) and would immediately make the fallback recommendations feel more relevant instead of just energetically close. A second improvement would be making the energy gap directional. Rather than treating "too loud" and "too quiet" as equal penalties, the scorer could accept an energy range (for example, minimum: 0.7, maximum: 1.0) so that a gym user never gets a quiet ambient track in their top 5 regardless of what else is happening with genre and mood. Third, the catalog itself needs more depth and balance at ten songs, any genre with a single entry is structurally under-served no matter how well the scoring logic works. Adding at least three to five songs per genre and ensuring every mood label appears on more than one song would make the diversity problem less severe without touching the algorithm at all. Longer term, it would be worth tracking implicit signals like skips and replays to adjust a user's weights automatically over time, so someone who always skips high-energy suggestions gradually sees their energy preference drift downward without having to update their profile manually.

## 9. Personal Reflection  

My biggest learning moment was realizing that the scoring logic matters just as much as the data. I assumed good recommendations would follow naturally from accurate song labels, but small decisions like whether genre is worth 20 points or 40 points visibly changed which songs appeared in the top 5. The adversarial profiles showed this most clearly, swapping genre and energy weights caused a rank change in the High-Energy Pop profile that I could trace directly back to a single number in the code.

Using AI tools helped me move quickly through the setup and get profiles running without getting stuck on boilerplate, but I still had to double-check the outputs manually. The "sad" mood profile is a good example: the system ran without errors and produced a confident-looking top 5, but the results were quietly wrong because the mood branch had silently stopped working. No error message told me that, I had to read the scores and reason through why they looked the way they did.

What surprised me most is how much the results can feel like real recommendations even when the algorithm is just adding up three numbers. When Library Rain appeared at the top for the Chill Lofi profile with a 89/90 score, it genuinely felt like a good pick quiet, focused, low energy. The illusion of understanding breaks down fast with adversarial profiles, but for a typical user with common preferences, a weighted sum over three features is apparently enough to seem plausible.

If I extended this project, I would add mood affinity groups so that chill, relaxed, and focused can score partial points against each other, and I would try replacing the fixed weights with a small set of user-adjustable sliders something like "how much does genre matter to you, on a scale of 1 to 5" so the system can be tuned without changing any code.
