# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

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

Where the system struggles or behaves unfairly. 

The most significant bias in the current system is that genre scoring is both binary and catalog-depth-dependent: a genre match awards a flat 20–40 points regardless of how many songs of that genre exist in the catalog, so a lofi fan receives a genre bonus on three songs while a rock or jazz fan receives it on exactly one. This creates a filter bubble for niche-genre users—after their single genre match, positions 2–5 are filled entirely by energy proximity, meaning a rock fan will consistently receive pop, synthwave, or ambient recommendations simply because those songs share a similar energy level, not because they are musically related. The same hard cliff appears in mood scoring: emotionally adjacent labels like "chill," "relaxed," and "focused" score zero against each other, so a user requesting "relaxed" loses all 30 mood points on every chill or focused track and can be outranked by a high-energy song that happens to be close in energy. Additionally, because the energy gap is calculated as an absolute unsigned distance, the system treats "too quiet" and "too loud" as equally bad penalties—a gym user asking for energy=0.95 gives an energy score of 11/40 to a quiet ambient track at 0.28, high enough to push it into the top 5 when no genre or mood match exists. Taken together, these binary thresholds mean the recommender silently ignores the partial similarity that a human listener would immediately recognise, and systematically under-serves users whose preferred genres or moods appear fewer than two times in the catalog.

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Six user profiles were tested in total: three normal taste profiles (High-Energy Pop, Chill Lofi, Deep Intense Rock) and three adversarial profiles designed to expose edge cases (a pop fan who wants a mood the catalog does not contain, a lofi fan requesting maximum energy, and a user whose genre does not exist in the catalog at all). For each profile, the top 5 results were inspected to check whether the score breakdown genre, mood, and energy matched the reasoning behind each recommendation. The normal profiles behaved as expected: when genre and mood both matched, the top result scored in the high 80s out of 90, which felt right. The most surprising result came from the Deep Intense Rock profile: after the single rock track took the top spot, every other recommendation was a non-rock song ranked purely by how close its energy was to 0.95 meaning the system effectively stopped thinking about genre after position 1. A second surprise was the Lofi Lover at Max Energy profile: even though genre and mood matched perfectly on two songs, requesting energy=1.0 penalised those songs so heavily that the gap between the lofi tracks and unrelated pop tracks narrowed to just 30 points, which felt like the energy signal was doing more work than intended. The weight-shift experiment (doubling energy from 20 to 40 points, halving genre from 40 to 20) caused a rank swap in the High-Energy Pop profile — Rooftop Lights jumped from third to second because its mood match outweighed Gym Hero's genre match once genre became cheaper — confirming that the relative weight of each feature has a real and observable effect on results.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

The most urgent fix would be replacing binary genre and mood matching with graduated similarity scores. Right now a song either matches your genre completely or scores zero — there is no middle ground for closely related genres like pop and indie pop, or adjacent moods like chill and relaxed. A simple lookup table of related genres and moods could award partial credit (say, 10 out of 20 points for a near-match) and would immediately make the fallback recommendations feel more relevant instead of just energetically close. A second improvement would be making the energy gap directional. Rather than treating "too loud" and "too quiet" as equal penalties, the scorer could accept an energy range (for example, minimum: 0.7, maximum: 1.0) so that a gym user never gets a quiet ambient track in their top 5 regardless of what else is happening with genre and mood. Third, the catalog itself needs more depth and balance — at ten songs, any genre with a single entry is structurally under-served no matter how well the scoring logic works. Adding at least three to five songs per genre and ensuring every mood label appears on more than one song would make the diversity problem less severe without touching the algorithm at all. Longer term, it would be worth tracking implicit signals like skips and replays to adjust a user's weights automatically over time, so someone who always skips high-energy suggestions gradually sees their energy preference drift downward without having to update their profile manually.

## 9. Personal Reflection  

My biggest learning moment was realising that the scoring logic matters just as much as the data. I assumed good recommendations would follow naturally from accurate song labels, but small decisions like whether genre is worth 20 points or 40 points visibly changed which songs appeared in the top 5. The adversarial profiles showed this most clearly — swapping genre and energy weights caused a rank change in the High-Energy Pop profile that I could trace directly back to a single number in the code.

Using AI tools helped me move quickly through the setup and get profiles running without getting stuck on boilerplate, but I still had to double-check the outputs manually. The "sad" mood profile is a good example: the system ran without errors and produced a confident-looking top 5, but the results were quietly wrong because the mood branch had silently stopped working. No error message told me that — I had to read the scores and reason through why they looked the way they did.

What surprised me most is how much the results can feel like real recommendations even when the algorithm is just adding up three numbers. When Library Rain appeared at the top for the Chill Lofi profile with a 89/90 score, it genuinely felt like a good pick — quiet, focused, low energy. The illusion of understanding breaks down fast with adversarial profiles, but for a typical user with common preferences, a weighted sum over three features is apparently enough to seem plausible.

If I extended this project, I would add mood affinity groups so that chill, relaxed, and focused can score partial points against each other, and I would try replacing the fixed weights with a small set of user-adjustable sliders — something like "how much does genre matter to you, on a scale of 1 to 5" — so the system can be tuned without changing any code.
