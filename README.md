# Lower Kenyang Compiler

A compiler for a programming language whose keywords are based on **Lower Kenyang** (ISO 639-3: `ken`), built for the Fall 2026 Compiler Construction course.

---

## Quick Start (Windows / Python 3.14+)

```powershell
pip install -r requirements.txt
python -m pytest -v
```

### Lexer CLI (Area 1)

```powershell
# Validate the 70-keyword table for collisions
python -m src.lexer --check-keywords

# Tokenize a Lower Kenyang source file
python -m src.lexer examples/factorial_utf8.ken

# Export tokens as JSON for Member 2 (Parser)
python -m src.lexer examples/factorial_utf8.ken --json
```

---

## Project Structure

- [project-plan.md](project-plan.md) — Overall 4-member project plan and 7-stage pipeline
- [CONTRIBUTING.md](CONTRIBUTING.md) — Branching rules, Git workflow, and PR checklist for teammates
- [keywords.json](keywords.json) — Machine-readable 70-keyword Lower Kenyang + ASCII fallback table
- [grammar/kenyang.lark](grammar/kenyang.lark) — Lark lexical grammar
- [src/lexer.py](src/lexer.py) — Lark-backed lexer with tone-stripping & multi-error recovery
- [tests/test_lexer.py](tests/test_lexer.py) — Automated lexer test suite
- `examples/` — Sample `.ken` programs (UTF-8 and ASCII fallback)
- `docs/`
  - [kenyang-research-dossier.md](docs/kenyang-research-dossier.md) — Linguistic sources, AGLC alphabet, Unicode & tone rules
  - [speaker-keywords-master.md](docs/speaker-keywords-master.md) — Full 70-keyword reference table
  - [language-spec.md](docs/language-spec.md) — Language specification, precedence, EBNF, and Token contract
  - [handover-area-2.md](docs/handover-area-2.md) — Simple-English handover guide for Member 2 (Parser & AST)
