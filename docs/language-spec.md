# Lower Kenyang Language Specification (v0.1 Draft)

**Implementation Language:** Python 3.14+ (using **Lark** parser/lexer generator)  
**Target Platform:** Windows (development) → x86-64 / VM target (Stage 6–7)

---

## 1. Lexical Rules

1. **Encoding & Normalization:**
   - Source files are UTF-8 (`.ken` extension recommended).
   - Keywords accept **both** Lower Kenyang UTF-8 spelling (with or without tone diacritics) and the standardized **ASCII fallback** (`ɛ`→`eh`, `ɔ`→`oh`, `ɨ`→`ih`, `ʉ`→`uh`, `ŋ`→`ng`).
2. **Identifiers (`IDENT`):**
   - Start with an ASCII letter or `_`, followed by letters, digits, or `_`: `[a-zA-Z_][a-zA-Z0-9_]*`.
   - Keywords are matched case-sensitively (lowercase) before `IDENT`.
3. **Literals:**
   - `INT_LIT`: `[0-9]+`
   - `FLOAT_LIT`: `[0-9]+\.[0-9]+` *(Standard tier)*
   - `STRING_LIT`: `"([^"\\\n]|\\.)*"` (supports `\"`, `\\`, `\n`, `\t`)
   - `BOOL_LIT`: `KW_TRUE` (`tɛtɛp` / `tehtehp`), `KW_FALSE` (`nse`)
4. **Comments & Whitespace:**
   - Single-line comment: `// ...` to end of line (ignored by lexer).
   - Multi-line comment: `/* ... */` (ignored by lexer).
   - Spaces, tabs, `\r`, `\n` are ignored (line & column tracked for errors).

---

## 2. Operators & Punctuation

| Category | Symbols |
|---|---|
| Arithmetic | `+`, `-`, `*`, `/`, `%` |
| Comparison | `==`, `!=`, `<`, `<=`, `>`, `>=` |
| Assignment | `=` |
| Logical (Keywords) | `ne` (`and`), `kɛ` (`or`), `ka` (`not`) |
| Delimiters | `(`, `)`, `{`, `}`, `,`, `;` |

### Operator Precedence (Highest to Lowest)
1. Primary: literals, identifiers, `( expr )`, function calls `f(args)`
2. Unary: `-`, `ka` (`not`)
3. Multiplicative: `*`, `/`, `%`
4. Additive: `+`, `-`
5. Relational: `<`, `<=`, `>`, `>=`
6. Equality: `==`, `!=`
7. Logical AND: `ne` (`and`)
8. Logical OR: `kɛ` (`or`)
9. Assignment: `=`

---

## 3. Core Grammar (EBNF)

```ebnf
program     ::= (func_decl | stmt)*

func_decl   ::= KW_FUNC IDENT "(" param_list? ")" (":" type)? block
param_list  ::= param ("," param)*
param       ::= type IDENT

block       ::= "{" stmt* "}"

stmt        ::= var_decl
              | assign_stmt
              | if_stmt
              | while_stmt
              | return_stmt
              | write_stmt
              | read_stmt
              | expr_stmt

var_decl    ::= type IDENT ("=" expr)? ";"
assign_stmt ::= IDENT "=" expr ";"
if_stmt     ::= KW_IF "(" expr ")" block (KW_ELSE block)?
while_stmt  ::= KW_WHILE "(" expr ")" block
return_stmt ::= KW_RETURN expr? ";"
write_stmt  ::= KW_WRITE "(" expr ")" ";"
read_stmt   ::= KW_READ "(" IDENT ")" ";"
expr_stmt   ::= expr ";"

type        ::= KW_INT | KW_BOOL | KW_STRING | KW_VOID
```

---

## 4. Example Program (Valid in Both UTF-8 & ASCII Fallback)

**UTF-8 Lower Kenyang:**
```text
kʉ main() : ngwɔ {
    pɨ x = 2 + 3 * 4;
    sɔ(x);
    piti;
}
```

**ASCII Fallback:**
```text
kuh main() : ngwoh {
    pih x = 2 + 3 * 4;
    soh(x);
    piti;
}
```

---

## 5. Handover Contract for Member 2 (Parser)

The lexer exposes:
- `tokenize(source: str) -> list[Token]` where each `Token` has:
  - `type: str` (e.g., `KW_INT`, `KW_WRITE`, `IDENT`, `INT_LIT`, `PLUS`, `SEMI`)
  - `lexeme: str` (exact text matched)
  - `line: int` (1-based)
  - `column: int` (1-based)
- CLI command `python -m src.lexer <file.ken> --json` to dump tokens as JSON for independent parser testing.
