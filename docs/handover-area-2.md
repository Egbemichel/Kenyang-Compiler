# Handover Guide for Member 2 (Grammar & Parser)

Welcome to **Area 2**!  
Area 1 (Language Design, Lower Kenyang Vocabulary, and the Lexer) is finished and tested. This guide explains everything that was built, the tools used, and how to plug your **Parser** directly into our work.

---

## 1. What Was Done in Area 1 (In Plain Words)

1. **We designed the language rules** (`docs/language-spec.md`):
   - Data types (`int`, `bool`, `string`, `void`, plus extra types like `float`).
   - Statements (variables, `if`/`else`, `while`, functions, `return`, `read`, `write`).
   - Operators and their order of priority (precedence), such as `*` before `+`.
2. **We built a 70-word Lower Kenyang dictionary** (`keywords.json` & `docs/speaker-keywords-master.md`):
   - Words come from documented Lower Kenyang sources (*Kenyang Lexicon*, *ManyuDictionary*, SIL/CABTAL).
   - Every keyword works in **both** real Lower Kenyang letters (UTF-8, like `kʉ`, `pɨ`, `sɔ`) **and** plain English-keyboard spelling (`kuh`, `pih`, `soh`).
   - Tone marks (like `sɔ́` vs `sɔ`) are automatically stripped so programmers do not have to type accents.
3. **We built and tested the Lexer** (`src/lexer.py` & `grammar/kenyang.lark`):
   - Reads any `.ken` file, skips spaces and comments (`//` and `/* ... */`), and turns the text into a clean list of **Tokens**.
   - Catches bad characters or unclosed quotes, prints clear error messages with the exact line and column number, and keeps going so all mistakes are shown at once.

---

## 2. Tools & Python Packages Used

You do **not** need Linux or any C compiler—everything runs natively on **Windows**:

| Tool / Package | Version | What it does |
|---|---|---|
| **Python** | `3.14.0` (3.14+ recommended) | The programming language we are writing the compiler in |
| **Lark** (`lark`) | `1.3.1` | Lexer & parser generator for Python (handles UTF-8 cleanly) |
| **Pytest** (`pytest`) | `9.0.3` | Runs our automated tests |

### How to Set Up on Your Computer

Open PowerShell in the project folder and run:

```powershell
pip install -r requirements.txt
python -m pytest -v
```

You should see **9 passed**.

---

## 3. How to Use the Lexer (Your Input)

You have **two ways** to get tokens from Area 1 into your Parser:

### Option A: Call it directly in Python (Recommended)

```python
from pathlib import Path
from src.lexer import KenyangLexer

lexer = KenyangLexer()
result = lexer.tokenize_file(Path("examples/factorial_utf8.ken"))

if not result.ok:
    for err in result.errors:
        print(err.format("factorial_utf8.ken"))
else:
    for tok in result.tokens:
        print(tok.type, tok.lexeme, tok.line, tok.column)
```

### Option B: Run it from the Command Line as JSON

If you want to test your parser with a saved JSON file of tokens:

```powershell
python -m src.lexer examples/factorial_utf8.ken --json
```

---

## 4. The Token Format (What You Receive)

Every item in `result.tokens` is a `Token` object with these fields:

| Field | Type | Example | Meaning |
|---|---|---|---|
| `type` | `str` | `"KW_WRITE"` or `"IDENT"` | The token category (see list below) |
| `lexeme` | `str` | `"sɔ"` or `"x"` | The exact text from the source file |
| `line` | `int` | `14` | Line number (starts at 1) |
| `column` | `int` | `5` | Column number (starts at 1) |
| `end_line` | `int` | `14` | Ending line number |
| `end_column` | `int` | `7` | Ending column number |
| `normalized` | `str \| None` | `"sɔ"` | Only set if tone marks were stripped |

### Token Types You Will See in Your Grammar

- **Keywords (`KW_*`):**
  - Core types: `KW_INT` (`pɨ`/`pih`), `KW_BOOL` (`tɛp`/`tehp`), `KW_STRING` (`bɛyɔŋ`/`behyohng`), `KW_VOID` (`ngwɔ`/`ngwoh`)
  - Literals: `KW_TRUE` (`tɛtɛp`/`tehtehp`), `KW_FALSE` (`nse`)
  - Control flow: `KW_IF` (`yat`), `KW_ELSE` (`rɔ`/`roh`), `KW_WHILE` (`kʉ_te`/`kuh_te`)
  - Functions & vars: `KW_FUNC` (`kʉ`/`kuh`), `KW_RETURN` (`piti`), `KW_VAR` (`ŋati`/`ngati`)
  - Logic: `KW_AND` (`ne`), `KW_OR` (`kɛ`/`keh`), `KW_NOT` (`ka`)
  - I/O: `KW_WRITE` (`sɔ`/`soh`), `KW_READ` (`pay`)
  - *(All 70 keywords are listed in `keywords.json`.)*
- **Identifiers & Literals:** `IDENT`, `INT_LIT`, `FLOAT_LIT`, `STRING_LIT`
- **Operators:** `PLUS` (`+`), `MINUS` (`-`), `STAR` (`*`), `SLASH` (`/`), `PERCENT` (`%`), `ASSIGN` (`=`), `EQ` (`==`), `NEQ` (`!=`), `LT` (`<`), `LE` (`<=`), `GT` (`>`), `GE` (`>=`)
- **Punctuation:** `LPAREN` (`(`), `RPAREN` (`)`), `LBRACE` (`{`), `RBRACE` (`}`), `COMMA` (`,`), `SEMI` (`;`), `COLON` (`:`)

---

## 5. What Member 2 Needs to Build Next

1. **Read `docs/language-spec.md`:** It already has the starter **EBNF grammar** and **operator precedence** table you need.
2. **Build the Parser (`src/parser.py`) & Syntax Tree (`src/ast_nodes.py`):**
   - Take `result.tokens` from `KenyangLexer` (or parse with Lark) and check that tokens follow the grammar rules.
   - Build a clean **Syntax Tree (AST)** made of Python `@dataclass` nodes (e.g., `Program`, `FuncDecl`, `VarDecl`, `IfStmt`, `WhileStmt`, `ReturnStmt`, `BinaryOp`, `CallExpr`).
   - Remember to copy `line` and `column` onto each AST node so **Member 3 (Semantic Analyser)** can report line numbers on type errors!
   - If the program has a grammar mistake (like a missing `;` or `}`), print a clear error message with the line number.
3. **Test against our sample programs in `examples/`:**
   - `examples/factorial_utf8.ken` & `examples/factorial_ascii.ken`
   - `examples/fibonacci.ken`
   - `examples/gcd.ken`
   - `examples/prime_check.ken`

---

## 6. Helpful Files to Read First

- [docs/language-spec.md](language-spec.md) — Start here! Contains the grammar and operator rules.
- [keywords.json](../keywords.json) — Full list of all 70 keyword token names.
- [src/lexer.py](../src/lexer.py) — Shows how `Token` and `LexError` are structured.
- [examples/factorial_utf8.ken](../examples/factorial_utf8.ken) — Example of a complete program.
