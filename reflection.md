# Profile Comparison Reflections

Comparing pairs of user profiles and what their outputs reveal about the scoring logic.

---

## Pair 1: High-Energy Pop vs. Chill Lofi

The High-Energy Pop profile (genre: pop, mood: happy, energy: 0.9) and the Chill Lofi profile
(genre: lofi, mood: chill, energy: 0.3) are almost mirror images of each other in terms of
energy. Both profiles found a strong match at position 1 — Sunrise City for pop, Library Rain
for lofi — and the scores were nearly identical (88.4 vs 89.0). What is interesting is how
different the "fallback" tracks look. The pop fan's positions 3-5 are medium-high energy songs
from synthwave and rock, because the catalog has no more pop tracks near that energy level.
The lofi fan's fallback is Spacewalk Thoughts (ambient, chill), which is a genuinely similar
listening experience even though the genre does not match. The lofi fan gets luckier because
the chill mood exists on an ambient track too, while the pop fan has no happy songs outside
pop and indie pop. This shows that users of popular genres benefit more from mood overlap
than users of genres that happen to share a mood label with other genres.

---

## Pair 2: Deep Intense Rock vs. Chill Lofi

These two profiles are opposites in almost every dimension — genre, mood, and energy. The
rock profile wants loud, aggressive, high-tempo music (energy: 0.95, mood: intense). The lofi
profile wants quiet, focused background sound (energy: 0.3, mood: chill). Both profiles had
two songs in the catalog that matched their mood — rock had Storm Runner and Gym Hero
marked intense; lofi had Library Rain and Midnight Coding marked chill. The rock fan's top 2
are both intense but come from different genres (rock and pop), while the lofi fan's top 2 are
both the same genre and mood. What is surprising about the rock profile is how quickly the
recommendations go off-genre: positions 3, 4, and 5 are all pop or synthwave tracks with no
mood or genre match at all. The lofi fan never falls that far off — even at position 4, Spacewalk
Thoughts shares the chill mood. This difference comes down to catalog depth: lofi has three
entries, rock has one. One song is never enough to fill five recommendation slots.

---

## Pair 3: High-Energy Pop vs. Adversarial — High Energy + Non-existent Mood ("sad")

Both profiles ask for the same genre (pop) and the same energy (0.9), but the normal profile
asks for mood: happy and the adversarial profile asks for mood: sad. Since "sad" does not
exist anywhere in the catalog, the mood branch never fires for the adversarial user. The
practical effect is that both profiles get the same two pop songs in their top 2, but the order
flips: in the normal profile, Sunrise City (happy) ranks above Gym Hero (intense) because it
gets the mood bonus. In the adversarial profile, Gym Hero scores higher because it is
slightly closer in energy (0.93 vs 0.82). This swap is a clean example of what happens when
a meaningful preference disappears — the system does not say "I cannot find a sad song," it
just silently re-orders by the remaining signals. A real user asking for sad music would have
no idea they are getting results that ignore their mood entirely.

---

## Pair 4: Adversarial — Lofi Lover at Max Energy vs. Normal Chill Lofi

Both profiles want lofi and chill, but the adversarial version asks for energy: 1.0 instead of
0.3. The catalog's lofi songs all sit between 0.35 and 0.42 in energy — completely the
opposite end of the scale from 1.0. In the normal profile, Library Rain scores 89/90 because
genre, mood, and energy all align closely. In the adversarial profile, the same song scores only
64/90 because the energy gap penalty wipes out more than 25 points. What is revealing is
that Gym Hero (pop, intense, energy: 0.93) creeps into position 5 for the adversarial user. A
pop song about going to the gym is appearing on a list for someone who said they want lofi
and chill music — purely because it happens to be loud. This is a real filter bubble problem:
the energy signal drags in completely wrong-context music just because of a number. The
two profiles are asking for the same genre and mood, but the energy conflict is enough to
produce a top 5 that feels like a completely different recommendation.

---

## Pair 5: Deep Intense Rock vs. Adversarial — Unknown Genre + Zero Energy

The rock profile wants genre: rock, mood: intense, energy: 0.95. The adversarial profile wants
genre: classical (not in catalog), mood: intense, energy: 0.0. Both profiles want the "intense"
mood, but they are asking for opposite energy levels. In the rock profile, Storm Runner scores
88.4 because it matches genre, mood, and has nearly the right energy. In the adversarial profile,
Storm Runner still appears at position 1 with 33.6 — but only because the mood match keeps
it ahead of ambient tracks despite having energy: 0.91 when the user asked for energy: 0.0.
What is strange here is that the two "intense" songs (Storm Runner and Gym Hero) score almost
identically (33.6 vs 32.8) even though the user wanted zero energy. A quiet ambient song
(Spacewalk Thoughts, energy: 0.28) comes in right behind them at 28.8. From a human
perspective, a classical listener wanting calm intense music should probably get the ambient track
first. But because mood is worth 30 points and energy is only worth 0–40 points, the mood
match on an almost maximally wrong-energy song still beats a no-mood-match song that is
energetically much closer to what was requested. This shows that when genre is missing from
the catalog, mood can override energy even when energy is the more important dimension for
that particular user.

---

## Pair 6: Normal Chill Lofi vs. Adversarial — Unknown Genre + Zero Energy

These two profiles share almost the same energy target (0.3 vs 0.0) but want completely
different genres and moods. The lofi fan gets highly relevant results because genre and mood
both match — Library Rain and Midnight Coding are genuinely good picks. The classical/zero-
energy fan gets recommendations dominated by two intense rock and pop tracks they would
almost certainly dislike, because the mood match on those songs outweighs the energy penalty.
The contrast makes clear that the weakest position to be in is a user whose genre is absent
from the catalog — not because their top recommendation is terrible, but because the system
has no genre signal to fall back on, so mood ends up steering everything. A chill-lofi user and
a zero-energy-classical user who both want quiet music end up with almost nothing in common
in their top 5, which is the correct outcome but for fragile reasons: the lofi fan benefits from
catalog depth, and the classical fan is effectively abandoned by the genre dimension entirely.
