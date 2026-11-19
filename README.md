# Lower Kenyang Compiler (`kenyang-compiler`)

![Python](https://img.shields.io/badge/Python-3.14%2B-3776AB?logo=python&logoColor=white)
![Lexer](https://img.shields.io/badge/Lexer-Lark%201.3-2ea44f)
![Language](https://img.shields.io/badge/Language-Lower%20Kenyang%20(ken)-orange)
![Course](https://img.shields.io/badge/Course-Compiler%20Construction%20Fall%202026-blue)

A compiler for a programming language whose keywords are rooted in **Lower Kenyang** (ISO 639-3: `ken`), the language of the Bayangi people of Cameroon. Built in Python using **Lark**.

---

## Language Preview

Programs can be written in **UTF-8 Lower Kenyang orthography** (with or without tone marks) or in **plain ASCII fallback** on any standard keyboard—both produce the exact same token stream:

<table>
<tr>
<th>UTF-8 Lower Kenyang</th>
<th>ASCII Fallback</th>
</tr>
<tr>
<td>

```text
kʉ factorial(pɨ n) : pɨ {
    yat (n <= 1) {
        piti 1;
    } rɔ {
        piti n * factorial(n - 1);
    }
}

kʉ main() : ngwɔ {
    pɨ ans = factorial(5);
    sɔ(ans);
    piti;
}
```

</td>
<td>

```text
kuh factorial(pih n) : pih {
    yat (n <= 1) {
        piti 1;
    } roh {
        piti n * factorial(n - 1);
    }
}

kuh main() : ngwoh {
    pih ans = factorial(5);
    soh(ans);
    piti;
}
```

</td>
</tr>
</table>

---

## Compiler Pipeline & Progress

```text
  [.ken source] ──▶ [1. Lexer (Lark)] ──▶ [2. Parser & AST] ──▶ [3. Semantic Analyser]
                          ✅ DONE               🔜 NEXT               ⏳ PLANNED
                                                                            │
  [Executable]  ◀── [6. Codegen & Runtime] ◀── [5. Optimiser] ◀── [4. IR / 3-Address]
      ⏳ PLANNED           ⏳ PLANNED             ⏳ PLANNED            ⏳ PLANNED
```

| Area | Owner | Scope | Status |
|---|---|---|---|
| **Area 1** | Member 1 | Language Design, 70-Word Kenyang Lexicon, Lark Lexer | **Done** |
| **Area 2** | Member 2 | Grammar, Parser, Abstract Syntax Tree (AST) | **Up Next** |
| **Area 3** | Member 3 | Symbol Table, Semantic Analyser, Optimiser | Planned |
| **Area 4** | Member 4 | Intermediate Code, Code Generator, Runtime | Planned |

---

## Quick Start (Windows / Python 3.14+)

```powershell
git clone https://github.com/Sirchella/Kenyang-Compiler.git
cd Kenyang-Compiler
pip install -r requirements.txt
python -m pytest -v
```

### Lexer CLI

```powershell
# Validate all 70 Lower Kenyang keywords for zero collisions
python -m src.lexer --check-keywords

# Tokenize a program (line:col, token type, lexeme)
python -m src.lexer examples/factorial_utf8.ken

# Export token stream as JSON (handover format for Member 2)
python -m src.lexer examples/factorial_utf8.ken --json
```

---

## Repository Map

| Path | Description |
|---|---|
| [`src/lexer.py`](src/lexer.py) | Lark-backed lexer with tone-diacritic normalization & multi-error recovery |
| [`grammar/kenyang.lark`](grammar/kenyang.lark) | Lexical grammar supporting UTF-8 Lower Kenyang & ASCII fallback |
| [`keywords.json`](keywords.json) | Machine-readable table of 70 Lower Kenyang keywords (`CORE`, `STANDARD`, `EXTENDED`) |
| [`tests/test_lexer.py`](tests/test_lexer.py) | Automated `pytest` suite (9 tests covering keywords, tones, recovery, CLI) |
| [`examples/`](examples/) | Sample `.ken` programs (`factorial`, `fibonacci`, `gcd`, `prime_check`) |
| [`docs/handover-area-2.md`](docs/handover-area-2.md) | Plain-English handover guide for Member 2 (Parser & AST) |
| [`docs/language-spec.md`](docs/language-spec.md) | Language specification, operator precedence, and EBNF grammar |
| [`docs/kenyang-research-dossier.md`](docs/kenyang-research-dossier.md) | Linguistic bibliography (19 sources), AGLC alphabet, and Unicode rules |
| [`docs/speaker-keywords-master.md`](docs/speaker-keywords-master.md) | Full 70-keyword reference table with lexicon citations |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Branching rules, Git workflow, and PR checklist |
| [`project-plan.md`](project-plan.md) | Overall 4-member semester project plan |
