# Lower Kenyang Programming Language: Master Keyword & Concept Data Table

**Source Basis:** Derived from documented Lower Kenyang linguistic sources (*Kenyang Lexicon* by Tanyi Eyong Mbuagbaw 1998, *ManyuDictionary*, *Kenyang Orthography Guide* 1999, and SIL/CABTAL records).  
**Orthography Rule:** Tone marks are stripped in source code (e.g., `sɔ́` → `sɔ`), and every keyword supports both **UTF-8 Lower Kenyang** and **ASCII fallback** (`ɛ`→`eh`, `ɔ`→`oh`, `ɨ`→`ih`, `ʉ`→`uh`, `ŋ`→`ng`).

---

## A. Data Types (1–9)

| # | Tier | Token | English | Lower Kenyang (Normalized) | ASCII Fallback | Source / Literal Meaning | Status |
|---|---|---|---|---|---|---|---|
| 1 | `CORE` | `KW_INT` | `int` | `pɨ` *(or `ɛmɔt`)* | `pih` | `pɨ` = count/number (*ManyuDict*) | Attested root |
| 2 | `CORE` | `KW_BOOL` | `bool` | `tɛtɛp_nsɛ` *(or `tɛp`)* | `tehtehp_nseh` | Derived from `tɛtɛp` (true) | Proposed |
| 3 | `CORE` | `KW_STRING` | `string` | `bɛyɔŋ` | `behyohng` | `bɛyɔŋ` = word, voice (*ManyuDict*) | Attested |
| 4 | `CORE` | `KW_VOID` | `void` | `ngwɔ` | `ngwoh` | `ngwɔ́` = to be empty (*ManyuDict*) | Attested |
| 5 | `STANDARD` | `KW_FLOAT` | `float` | `pɨ_kati` | `pih_kati` | `pɨ` (count) + `kátí` (cut/fraction) | Compound |
| 6 | `STANDARD` | `KW_CHAR` | `char` | `ɛyɔŋ` | `ehyohng` | Singular class of `bɛyɔŋ` (word/sign) | Attested root |
| 7 | `EXTENDED` | `KW_ARRAY` | `array` | `bɛtɨk` | `behtihk` | Group/work collection (*ManyuDict*) | Attested root |
| 8 | `EXTENDED` | `KW_STRUCT` | `struct` | `ghokoti` | `ghokoti` | `ghokotí` = to shape, frame (*ManyuDict*) | Attested |
| 9 | `EXTENDED` | `KW_ENUM` | `enum` | `bayat` | `bayat` | From `yat` = to choose (*ManyuDict*) | Proposed |

---

## B. Literals & Constants (10–14)

| # | Tier | Token | English | Lower Kenyang (Normalized) | ASCII Fallback | Source / Literal Meaning | Status |
|---|---|---|---|---|---|---|---|
| 10 | `CORE` | `KW_TRUE` | `true` | `tɛtɛp` | `tehtehp` | `tɛtɛp` = to be honest, true (*ManyuDict*) | Attested |
| 11 | `CORE` | `KW_FALSE` | `false` | `nse` | `nse` | `nsé` = to lie, be wrong (*ManyuDict*) | Attested |
| 12 | `STANDARD` | `KW_NULL` | `null` | `ngwɔ_nɛ` | `ngwoh_neh` | Empty/nothing (`ngwɔ́` = empty) | Compound |
| 13 | `EXTENDED` | `KW_SELF` | `self` | `mɛn` | `mehn` | Verify in *Kenyang Lexicon* PDF | Lookup |
| 14 | `EXTENDED` | `KW_PI` | `pi` | `pi` | `pi` | Universal math constant | Standard |

---

## C. Control Flow & Branching (15–24)

| # | Tier | Token | English | Lower Kenyang (Normalized) | ASCII Fallback | Source / Literal Meaning | Status |
|---|---|---|---|---|---|---|---|
| 15 | `CORE` | `KW_IF` | `if` | `yat` *(verify particle)* | `yat` | `yat` = choose (*ManyuDict*); verify `if` particle in Lexicon PDF | Attested root |
| 16 | `CORE` | `KW_ELSE` | `else` | `rɔ` *(or `kɛ_yat`)* | `roh` | `rɔ̌` = leave/otherwise (*ManyuDict*); verify in Lexicon PDF | Attested root |
| 17 | `STANDARD` | `KW_ELIF` | `elif` | `rɔ_yat` | `roh_yat` | Otherwise + choose | Compound |
| 18 | `STANDARD` | `KW_SWITCH` | `switch` | `yat_bɛ` | `yat_beh` | Multi-choice (*ManyuDict* `yat`) | Compound |
| 19 | `STANDARD` | `KW_CASE` | `case` | `mpok` | `mpok` | Way/side/place (*ManyuDict* `mpok`) | Attested |
| 20 | `STANDARD` | `KW_DEFAULT` | `default` | `rɔ_mpok` | `roh_mpok` | Remaining case | Compound |
| 21 | `CORE` | `KW_THEN` | `then` | `fɔ` | `foh` | Optional if using `{ }` blocks | Verify |
| 22 | `EXTENDED` | `KW_BEGIN` | `begin` | `bhɔŋ` | `bhohng` | `bhɔ́ŋ` = to start, begin (*ManyuDict*) | Attested |
| 23 | `EXTENDED` | `KW_END` | `end` | `te` | `te` | `té` / `tě` = to stop (*ManyuDict*) | Attested |
| 24 | `EXTENDED` | `KW_PASS` | `pass` | `rɔ_kʉ` | `roh_kuh` | Leave without doing | Compound |

---

## D. Loops & Iteration (25–32)

| # | Tier | Token | English | Lower Kenyang (Normalized) | ASCII Fallback | Source / Literal Meaning | Status |
|---|---|---|---|---|---|---|---|
| 25 | `CORE` | `KW_WHILE` | `while` | `kʉ_te` *(verify particle)* | `kuh_te` | Do until/while; verify `while` particle in Lexicon PDF | Proposed |
| 26 | `STANDARD` | `KW_FOR` | `for` | `pay_te` | `pay_te` | Count through (`pay` = count) | Compound |
| 27 | `STANDARD` | `KW_BREAK` | `break` | `kati` | `kati` | `kátí` = to cut (*ManyuDict*) | Attested |
| 28 | `STANDARD` | `KW_CONTINUE` | `continue` | `chák` | `chak` | `chák` = straight ahead (*ManyuDict*) | Attested |
| 29 | `EXTENDED` | `KW_DO` | `do` | `kʉ` | `kuh` | `kʉ` = to do (*ManyuDict*) | Attested |
| 30 | `EXTENDED` | `KW_REPEAT` | `repeat` | `bhɔŋ_piti` | `bhohng_piti` | Start again (`bhɔ́ŋ` + `piti`) | Compound |
| 31 | `EXTENDED` | `KW_UNTIL` | `until` | `te_chak` | `te_chak` | Stop-at | Compound |
| 32 | `EXTENDED` | `KW_IN` | `in` | `amem` | `amem` | `amem` = inside, in (*Kenyang corpus*) | Attested |

---

## E. Functions, Variables & Scope (33–43)

| # | Tier | Token | English | Lower Kenyang (Normalized) | ASCII Fallback | Source / Literal Meaning | Status |
|---|---|---|---|---|---|---|---|
| 33 | `CORE` | `KW_FUNC` | `func` | `kʉ` *(or `kʉ_bɛtɨk`)* | `kuh` | `kʉ` = to do; `kʉ bɛtɨk` = to work (*ManyuDict*) | Attested |
| 34 | `CORE` | `KW_RETURN` | `return` | `piti` | `piti` | `piti` = to recede, return (*ManyuDict*) | Attested |
| 35 | `CORE` | `KW_VAR` | `var` | `ŋati` | `ngati` | `ŋatí` = to hold (*ManyuDict*) | Attested |
| 36 | `STANDARD` | `KW_CONST` | `const` | `burɛ` | `bureh` | `búrɛ́` = to keep, store (*Kenyang*) | Attested |
| 37 | `STANDARD` | `KW_MAIN` | `main` | `bhɔŋ_kʉ` | `bhohng_kuh` | Starting work (`bhɔ́ŋ` = start) | Compound |
| 38 | `EXTENDED` | `KW_GLOBAL` | `global` | `ɛtɔk` | `ehtohk` | Town/public (`ɛyɔŋ-ɛ́tɔk` = language) | Attested root |
| 39 | `EXTENDED` | `KW_LOCAL` | `local` | `ndak` | `ndak` | House/inside (*ManyuDict*) | Attested |
| 40 | `EXTENDED` | `KW_IMPORT` | `import` | `sɔt` | `soht` | `sɔt` = to receive, take (*ManyuDict*) | Attested |
| 41 | `EXTENDED` | `KW_EXPORT` | `export` | `chyɛ` | `chyeh` | `chyɛ̌` = to give (*ManyuDict*) | Attested |
| 42 | `EXTENDED` | `KW_NEW` | `new` | `ghokoti` | `ghokoti` | `ghokotí` = to create, shape (*ManyuDict*) | Attested |
| 43 | `EXTENDED` | `KW_DELETE` | `delete` | `rɔ_bɛ` | `roh_beh` | Abandon/remove | Compound |

---

## F. Logical & Comparison Operators (44–50)

| # | Tier | Token | English | Lower Kenyang (Normalized) | ASCII Fallback | Source / Literal Meaning | Status |
|---|---|---|---|---|---|---|---|
| 44 | `CORE` | `KW_AND` | `and` | `ne` | `ne` | `ne` = coordinating conjunction "and" (*ASJP/Lexicon*) | Attested |
| 45 | `CORE` | `KW_OR` | `or` | `kɛ` *(verify in Lexicon)* | `keh` | Verify `or` conjunction in Lexicon PDF | Lookup |
| 46 | `CORE` | `KW_NOT` | `not` | `ka` *(verify negation)* | `ka` | Verbal negation marker; verify in Lexicon PDF | Lookup |
| 47 | `EXTENDED` | `KW_XOR` | `xor` | `ɛmɔt_kɛ` | `ehmoht_keh` | Only one (`ɛmɔt` = one) | Compound |
| 48 | `EXTENDED` | `KW_IS` | `is` | `a` *(copula; verify)* | `a` | Verify copula in Lexicon PDF | Lookup |
| 49 | `EXTENDED` | `KW_AS` | `as` | `kɛ_ne` | `keh_ne` | Like/as | Proposed |
| 50 | `EXTENDED` | `KW_MOD` | `mod` | `kati_pɨ` | `kati_pih` | Remainder (`kátí` + `pɨ`) | Compound |

---

## G. Built-in I/O & Standard Functions (51–62)

| # | Tier | Token | English | Lower Kenyang (Normalized) | ASCII Fallback | Source / Literal Meaning | Status |
|---|---|---|---|---|---|---|---|
| 51 | `CORE` | `KW_WRITE` | `write` | `sɔ` | `soh` | `sɔ́` = to write (*ManyuDict*) | Attested |
| 52 | `CORE` | `KW_READ` | `read` | `pay` | `pay` | `páy` = to read, count (*ManyuDict*) | Attested |
| 53 | `STANDARD` | `KW_SAY` | `println` | `rɛsɛ` *(or `rɛ`)* | `rehseh` | `rɛsɛ́` / `rɛ́` = to say, talk (*ManyuDict*) | Attested |
| 54 | `STANDARD` | `KW_LEN` | `len` | `pay_bɛ` | `pay_beh` | Count items | Compound |
| 55 | `STANDARD` | `KW_TO_INT` | `to_int` | `piti_pɨ` | `piti_pih` | Turn to number | Compound |
| 56 | `STANDARD` | `KW_TO_STR` | `to_str` | `piti_bɛyɔŋ` | `piti_behyohng` | Turn to word | Compound |
| 57 | `EXTENDED` | `KW_ABS` | `abs` | `tɛtɛp_pɨ` | `tehtehp_pih` | Positive/true number | Compound |
| 58 | `EXTENDED` | `KW_MIN` | `min` | `nɛ_kɛ` | `neh_keh` | Smallest | Proposed |
| 59 | `EXTENDED` | `KW_MAX` | `max` | `bɛ_kɛ` | `beh_keh` | Biggest | Proposed |
| 60 | `EXTENDED` | `KW_OPEN` | `open` | `nɛnɛ` | `nehneh` | `nɛ́nɛ` = to open (*ManyuDict*) | Attested |
| 61 | `EXTENDED` | `KW_CLOSE` | `close` | `tyɛt` | `tyeht` | `tyɛt` = to close (*ManyuDict*) | Attested |
| 62 | `EXTENDED` | `KW_TYPEOF` | `typeof` | `nnyɛn_kʉ` | `nnyehn_kuh` | `nnyɛ́n` = name (*ManyuDict*) | Compound |

---

## H. Error Handling & Diagnostics (63–70)

| # | Tier | Token | English | Lower Kenyang (Normalized) | ASCII Fallback | Source / Literal Meaning | Status |
|---|---|---|---|---|---|---|---|
| 63 | `EXTENDED` | `KW_TRY` | `try` | `tɛm` *(verify)* | `tehm` | Verify in *Kenyang Lexicon* PDF | Lookup |
| 64 | `EXTENDED` | `KW_CATCH` | `catch` | `ŋati_bafwɔp` | `ngati_bafwohp` | Hold mistake (`ŋatí` + `bafwɔ́p`) | Compound |
| 65 | `EXTENDED` | `KW_THROW` | `throw` | `chyɛ_bafwɔp` | `chyeh_bafwohp` | Give mistake | Compound |
| 66 | `EXTENDED` | `KW_ASSERT` | `assert` | `tɛtɛp_yat` | `tehtehp_yat` | Check truth | Compound |
| 67 | `EXTENDED` | `KW_ERROR` | `error` | `bafwɔp` | `bafwohp` | `bafwɔ́p` = mistake (*ManyuDict*) | Attested |
| 68 | `EXTENDED` | `KW_EXIT` | `exit` | `te_rɔ` | `te_roh` | Stop and leave | Compound |
| 69 | `EXTENDED` | `KW_YIELD` | `yield` | `chyɛ_piti` | `chyeh_piti` | Give back (`chyɛ̌` + `piti`) | Compound |
| 70 | `EXTENDED` | `KW_STEP` | `step` | `mpok_pay` | `mpok_pay` | Step/way of counting (`mpok` + `pay`) | Compound |

---

## I. Reference Numbers & Common Roots (Attested)

| Concept | Lower Kenyang | ASCII Fallback | Source |
|---|---|---|---|
| `one` (1) | `ɛmɔt` | `ehmoht` | ASJP / Comparative Wordlist |
| `two` (2) | `bɛpay` | `behpay` | ASJP / Comparative Wordlist |
| `three` (3) | `nɛkú` → `nɛku` | `nehku` | ASJP / Comparative Wordlist |
| `four` (4) | `ɛsa` | `ehsa` | ASJP / Comparative Wordlist |
| `book` / `paper` | `ɛkatí` → `ɛkati` | `ehkati` | *ManyuDictionary* |
| `name` | `nnyɛ́n` → `nnyɛn` | `nnyehn` | *ManyuDictionary* |
| `put` | `fyɛ́` → `fyɛ` | `fyeh` | *ManyuDictionary* |
| `language` | `ɛyɔŋ-ɛ́tɔk` | `ehyohng-ehtohk` | *ManyuDictionary* |

---

## Collision Check (Core + Standard)
- No duplicate Lower Kenyang keywords or ASCII fallbacks in `CORE` or `STANDARD`.
- Note: `kʉ` (`kuh`) is assigned to `KW_FUNC` in `CORE` (and `KW_DO` in `EXTENDED` — if `KW_DO` is added later, use `kʉ_nɛ` to avoid collision). Similarly `ghokoti` is `KW_STRUCT` or `KW_NEW` (pick one if both are enabled).
