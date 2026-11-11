# The Soul Chords: weekly social run

This repository holds the media and the engine for The Soul Chords' social posts. Images pushed here are served publicly at
`https://raw.githubusercontent.com/thesoulchords/soulchords-media/main/<path>`, and Metricool takes them from those addresses.
Nothing personal belongs here: no names, emails or private notes. The repo is public.

## The run, every week

A scheduled session runs on Sunday evening and prepares the coming Monday to Sunday.

1. **Set up.** `cd engine && npm install --silent` (fonts), `pip install --break-system-packages numpy pillow` if missing. Playwright and ffmpeg are already installed.
2. **Read `log.md`** to see what has already been posted, so nothing repeats and the rotations continue.
3. **Plan the week** from the schedule below. Write all captions in the voice (see Rules).
4. **Build.** Make `weeks/<monday-date>/build.py`. Copy the helpers you need (`ring`, `BASE`, `page`, `note_carousel`, etc.) from `engine/grid.py`, and `engine/reel.py`, `engine/pins.py`, `engine/stories.py` for Reels, pins and covers. Keep their look exactly. Render feed slides at 1080×1350, Reels at 1080×1920 (H.264 `-preset veryfast -crf 20`, AAC), pins at 1000×1500. Write images as JPEG quality 92 into `media/<monday-date>/`.
5. **Check every image** by looking at it: fonts loaded (Cormorant, Figtree, EB Garamond italic; render from a file URL, never `set_content`, or the fonts fall back to Times), no text overflow, nothing in the bottom 340px of a Reel.
6. **Push** `media/<monday-date>/` and the build script. Commit as `Claude <noreply@anthropic.com>`. Confirm one raw URL returns 200.
7. **Preview.** Publish one artifact page for the week from `engine/preview_template.html`: each day, its channel, slides, caption with a copy button, Reel inline. Send the preview and ask for approval.
8. **On approval only**, schedule in Metricool (brand blogId `7963420`, timezone `America/Toronto`). If changes are asked for, make them, re-push, re-publish the preview, ask again. Never schedule feed posts before approval.
9. **Update `log.md`** with every post scheduled (date, channel, series, title, media path) and push.

## Schedule

Times: Monday Reel at 8:00 am; feed posts at 12:00 pm; Facebook at 12:15 pm; pins at 9:10 am and 8:10 pm. After four weeks, move times using Metricool's best-time data.

### Weeks 1–4 (Nov 16 to Dec 13, 2026): four Instagram posts a week

| Week of | Monday | Tuesday | Thursday | Saturday |
|---|---|---|---|---|
| Nov 16 | Morning Attunement: C, the Wildling (already rendered: `media/attunements/morning_attunement_C_wildling.mp4`) | The Notes: the Keystone | The Twelve at a dinner party | Ancient Voices: Ptolemy on the melody at dawn |
| Nov 23 | Morning Attunement: the open fifth, C + G | The Notes: the Beacon | The Twelve on a hard day | Harmonize: Keystone + Portal |
| Nov 30 | Morning Attunement: C♯, the Keystone | The Notes: the Mirror | The Twelve as teachers | Chord Geometry: the Cluster (its own 5-slide feature) |
| Dec 7 | Morning Attunement: the open fifth, C + G | The Notes: the Wayshower | The Twelve in the group chat | Mathematics: 2:1, 3:2, 4:3 |

In week 4, read Metricool's numbers per series and propose stepping up to the daily rhythm.

### From week 5: daily

| Day | Instagram | Facebook | Pinterest |
|---|---|---|---|
| Mon | Morning Attunement Reel | The Reel | 1–2 pins (ritual how-to) |
| Tue | The Notes (colour carousel) | The week's note with a link to its note page | 1–2 pins (note) |
| Wed | Ancient Voices carousel | The carousel | 1–2 pins (quote) |
| Thu | The Twelve as… carousel | The carousel | 1–2 pins (which one are you?) |
| Fri | Harmonize pairing | The pairing, linking both note pages | 1–2 pins (reference chart) |
| Sat | Mathematics of Harmony or Chord Geometry | The carousel | The same post re-made tall |
| Sun | Ancient Voices carousel | The carousel | 1–2 pins (quote) |

**Pinterest every week:** 10–14 fresh pins (two a day), made for search. Kinds: note pins (link `/note/<slug>`), reference charts, "which one are you?", ritual how-to, palettes, tall ancient quotes, and Instagram Mathematics / Chord Geometry posts re-made tall. Titles use search phrases ("soul archetype", "sound meditation", "music of the spheres", "morning ritual", "spiritual quotes"). Boards: Music of the Spheres · Sound and the Soul · The 12 Soul Archetypes · Morning Rituals · Ancient Wisdom Quotes · Find Your Soul Chord (Metricool resolves the board name). Design fresh images; don't re-pin the same image.

## Series rules

- **Morning Attunement (Reel, 25 s, sound on).** The approved template is `engine/reel.py`. Alternate: one single note (rotating through the twelve in pitch order, C to B) one week, the open fifth C + G (264 and 395.56 Hz) the next. Every one opens with "At dawn, the Pythagoreans / tuned the soul with sound." and the caption tells that the Pythagoreans played a gentle melody at dawn. Cues: Inhale / Exhale with a small line under each (vary the lines week to week), closing "Every soul has a sound." over "Listen to yours." Ring order: C at the top, clockwise in pitch order; the week's note(s) lit in colour. Caption ends "Find your chord · link in bio". Schedule with `instagramData.type: "REEL"` and `facebookData.type: "REEL"`.
- **The Notes.** Colour background in the note's colour, text in its contrast colour (table below). 4 slides, as `note_carousel` in grid.py. Text comes from the note pages (`engine/note_page.html`) and canon; never invent new traits.
- **Ancient Voices.** Black background, carousels of 3–5 slides. Quotes are our own short renderings from the Latin or Greek, or a public-domain translation. Start from the verified lines below; check any new line in Source Library and keep the page link in `log.md`.
- **The Twelve as…** White background, cover + 12 slides (one per note, pitch order) + closing. One short, warm, specific line per note, true to its gift.
- **Harmonize.** Two notes side by side: both colours, both names, how they meet. No ranking, no "compatibility" scores.
- **Chord Geometry** (formerly Chord Shapes). Always say "geometry", never "shape", in every graphic, caption and pin: "the 13 geometries", "what geometry is your chord?". Each of the 13 geometries gets its own 5-slide feature first; later it returns with new example chords. Triangle drawn on the ring.
- **Mathematics of Harmony.** Pythagoras, ratios, the monochord, the music of the spheres. White or ivory.

## Brand canon

| Note | Archetype | Hz | Colour | Text on colour |
|---|---|---|---|---|
| C | Wildling | 264 | #74854A | white |
| C♯ | Keystone | 279.70 | #B06F57 | black |
| D | Beacon | 296.33 | #D4935A | black |
| D♯ | Manifestor | 313.96 | #C4A15A | black |
| E | Wayshower | 332.62 | #A9483A | white |
| F | Noble | 352.40 | #6E9C87 | black |
| F♯ | Mirror | 373.36 | #6F93AE | black |
| G | Visionary | 395.56 | #5B6591 | white |
| G♯ | Alchemist | 419.08 | #7E6A9A | white |
| A | Architect | 444 | #6E7780 | white |
| A♯ | Activator | 470.40 | #A35C7A | white |
| B | Portal | 498.37 | #5E9EA3 | black |

Logo at the foot of every graphic: `THE` *Soul* `CHORDS` set tight (see `.mark` in grid.py).

## Rules

- **No hashtags.** No asking readers to tag, share or repost. The account stays anonymous: no personal names, faces or locations.
- **Captions:** two to four short lines in a warm, plain voice, one question near the end, then "Find your chord · link in bio". On Facebook replace "link in bio" with "thesoulchords.com", or a note page `thesoulchords.com/note/<slug>` when the post is about one note.
- **Public content is sound-only:** notes, frequencies, colours, music. Elements, animal allies and chakras belong to the readings, not to posts.
- Instagram carousels: up to 20 slides; Instagram posts must have media. Facebook gets the same images as an album post.
- Story highlights are posted by hand by the owner; covers are in `engine/covers4.py` (staff lines, the wave always enters and leaves on the middle line).

## Ancient Voices: verified lines to start from

- Boethius, *Fundamentals of Music* I.2: human music is understood by anyone who descends into themselves. (Used Nov 9.)
- Ptolemy, *Harmonics*: the Pythagoreans urged people to touch only a pleasant melody upon rising at dawn, before beginning any activity.
- Macrobius, quoted by Pierre d'Ailly: every soul is captivated by musical sounds.
- Agrippa, *Occult Philosophy* II.28: the consonance of the soul consists in the due temperament and proportion of its faculties.
- Iamblichus, *Life of Pythagoras* (Taylor, 1818, public domain): how Pythagoras found the harmonic ratios.

## Metricool call shapes

Feed post (Instagram):
`{"providers":[{"network":"instagram"}],"media":[<raw urls>],"text":<caption>,"publicationDate":{"dateTime":"YYYY-MM-DDTHH:MM:SS","timezone":"America/Toronto"},"instagramData":{"type":"POST"},"autoPublish":true,"draft":false,"descendants":[],"smartLinkData":{"ids":[]}}`

Facebook: same with `"providers":[{"network":"facebook"}]`, `"facebookData":{"type":"POST"}` and the Facebook caption.

Pin: `"providers":[{"network":"pinterest"}]`, one image, `"pinterestData":{"boardId":"<board name>","pinTitle":<title>,"pinLink":<url>,"pinNewFormat":true}`, text = the pin description.
