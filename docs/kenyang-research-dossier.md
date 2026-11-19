# Lower Kenyang Linguistic & Orthographic Dossier

**Language:** Kenyang (Lower Kenyang dialect)  
**Alternate Names:** Banyang, Banyangi, Nyang, Manyang  
**ISO 639-3:** `ken` | **Glottocode:** `keny1279`  
**Classification:** Niger-Congo → Atlantic-Congo → Bantoid → Southern Bantoid → Mamfe (Nyang)  
**Region:** South-West Region, Cameroon (Manyu & Meme Divisions; centered around Mamfe)

---

## 1. Complete Bibliography & Digital Sources

### Lexicons & Dictionaries
1. **Mbuagbaw, Tanyi Eyong (1998).** *Kenyang Lexicon* (Provisional Edition, 46 pp., 2,500+ entries anchored on Lower Kenyang). Society for Kenyang Literature (SKL) & CABTAL.  
   - *Where to find:* SIL Cameroon Language & Culture Archives; Internet Archive (Rosetta Project / Long Now Foundation collection).
2. **ManyuDictionary** (`manyudictionary.firebaseapp.com`) — Online searchable database covering Kenyang, Ejagham, and Denya with English glosses, parts of speech, and plurals.
3. **EyaLingo** (`eyalingo.com`) — Bilingual English–Kenyang / Kenyang–English vocabulary tool.
4. **ASJP Database** (`clld.org`) — Comparative phonetic wordlist for Kenyang (numbers, pronouns, core nouns/verbs).

### Orthography & Literacy
5. **Mbuagbaw, Tanyi Eyong (1999).** *Kenyang Orthography Guide*. Yaoundé: CABTAL / SIL Cameroon. (Covers alphabet, tone marking, word division, subject markers, noun phrases, associative phrases, and compound nouns.)
6. **Mbuagbaw, Tanyi Eyong (2000).** *Kenyang Literacy Program*. *Notes on Literacy*, vol. 26, pp. 57–63.
7. **Mbuagbaw, Tanyi Eyong (2008).** *The Standardization and Modernization of Kenyang*. SIL Cameroon.

### Phonology & Tone
8. **Mbuagbaw, Tanyi Eyong (1994).** *Kenyang Phonology*. Cameroon Bible Translation Association (CABTA).
9. **Mbuagbaw, Tanyi Eyong (2000).** *Kenyang Segmental Phonology*. CABTAL / SIL.
10. **Tyhurst, James J. (1985).** *Tone in Kenyang Noun Phrases*. M.A. thesis, UCLA. (Autosegmental tone analysis based on Lower Kenyang data from Mamfe.)

### Grammar, Syntax & Vocabulary Expansion
11. **Bakia, Joan Achre (1988).** *An Introduction to Kenyang Syntax*. M.A. thesis, University of Jos.
12. **Ramirez, Christi (1998).** *The Kenyang Noun Phrase*. Yaoundé: SIL (unpublished manuscript, 37 pp.).
13. **Enoachuo, Emilisco Jones (2002).** *The Development of Scientific Vocabulary for Kenyang*. M.A. thesis, University of Buea. *(Directly relevant for adapting/coining technical programming terms.)*
14. **Voorhoeve, Jan (1977).** "Kenyang." In L. Hyman & J. Voorhoeve (eds.), *L'expansion Bantoue*, Vol. 1, pp. 275–285. Paris.
15. **Ojong, M. B. (2005).** *A Proto-reconstruction of the Nyang Languages*. DEA dissertation, University of Yaoundé I.

### Sociolinguistics, Ethnography & Corpora
16. **Tyhurst, James J. (1983).** *A Sociolinguistic Appraisal of Kenyang and Denya*. SIL, Yaoundé.
17. **Ruel, Malcolm (1969).** *Leopards and Leaders: Constitutional Politics among a Cross River People*. London: Tavistock.
18. **Ittmann, Johannes (1935–1936).** *Kęnyaṅ, die Sprache der Nyang*. *Zeitschrift für Eingeborenen-Sprachen* (early colonial grammar & folktales).
19. **Kenyang New Testament (2010).** Wycliffe Bible Translators & CABTAL. Available digitally via **ScriptureEarth** (`scriptureearth.org`, ePub/SWORD) and **YouVersion / Bible.com** — provides a large UTF-8 text corpus in standardized Kenyang orthography.

### Portals
- **SIL Cameroon Archives:** `https://www.silcameroon.org`
- **Glottolog (`keny1279`):** `https://glottolog.org/resource/languoid/id/keny1279`
- **OLAC (Open Language Archives Community):** Aggregates metadata for `ken`.

---

## 2. Standardized Alphabet (AGLC)

Kenyang follows the **General Alphabet of Cameroon Languages (AGLC)**:

```text
a, b, bh, ch, d, e, ɛ, f, g, gb, gh, i, ɨ, j, k, kp, m, n, ŋ, ny, o, ɔ, p, r, s, t, u, ʉ, w, y
```

### Non-ASCII Characters & Unicode Specification

| Lowercase | Uppercase | Unicode (Lower / Upper) | Phonetic Description | Standard ASCII Fallback |
|---|---|---|---|---|
| `ɛ` | `Ɛ` | `U+025B` / `U+0190` | Open-mid front unrounded vowel | `eh` |
| `ɔ` | `Ɔ` | `U+0254` / `U+0186` | Open-mid back rounded vowel | `oh` |
| `ɨ` | `Ɨ` | `U+0268` / `U+0197` | Close central unrounded vowel | `ih` |
| `ʉ` | `Ʉ` | `U+0289` / `U+0244` | Close central rounded vowel | `uh` |
| `ŋ` | `Ŋ` | `U+014B` / `U+014A` | Velar nasal ("ng" in *sing*) | `ng` |

> **Why `eh`, `oh`, `ih`, `uh` instead of `e`, `o`, `i`, `u`?**  
> Standard `e`, `o`, `i`, `u` are distinct phonemes in Kenyang. Using `-h` digraphs prevents accidental collisions between two different words (e.g., `e` vs `ɛ`) when typing on an English keyboard.

---

## 3. Tone, Normalization & Word Division Rules for the Compiler

1. **Tone Marking in Orthography vs. Source Code:**
   - Standard Kenyang marks High (`á`), Low (unmarked or `à`), Rising (`ǎ`), and Falling (`â`) tones.
   - Programmers should not have to type tone diacritics. Therefore:
     - **Lexer Rule 1:** All source files are read as **UTF-8** and Unicode-normalized (**NFD → strip combining diacritics → NFC**) when matching keywords, so both `sɔ́` and `sɔ` (and `soh`) resolve to the same `WRITE` token.
     - **Design Rule 2:** **Never** assign two different keywords to Kenyang words that differ *only* by tone.
2. **Word Division:**
   - Kenyang separates analytic particles (conjunctions, tense/aspect markers, negation) as independent words, and uses compounding/hyphenation for compound nouns.
   - For programming keywords, prefer **single short words**. If a concept requires a two-word phrase (e.g., *to work* = `kʉ bɛtɨk`), join with an underscore (`kʉ_bɛtɨk`) or pick the single root (`kʉ`).
3. **Key Digraphs to Preserve:**
   - `bh`, `ch`, `gb`, `gh`, `kp`, `ny` are valid consonant digraphs in Kenyang and remain unchanged in ASCII fallback.
