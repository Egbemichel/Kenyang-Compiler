"""Lexical analyser for the Lower Kenyang programming language.

Uses Lark for tokenization, supports both UTF-8 Lower Kenyang orthography
(with automatic tone-diacritic normalization) and standardized ASCII
fallbacks, and provides multi-error recovery with source-caret diagnostics.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import io
import json
from pathlib import Path
import re
import sys
import unicodedata
from typing import Iterable

from lark import Lark
from lark.exceptions import UnexpectedCharacters


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_GRAMMAR_PATH = PROJECT_ROOT / "grammar" / "kenyang.lark"
DEFAULT_KEYWORDS_PATH = PROJECT_ROOT / "keywords.json"

ASCII_IDENT_RE = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")
VALID_TIERS = ("CORE", "STANDARD", "EXTENDED")


@dataclass(frozen=True, slots=True)
class Token:
    """A single lexical token handed over to the parser (Member 2)."""

    type: str
    lexeme: str
    line: int
    column: int
    end_line: int
    end_column: int
    normalized: str | None = None

    def to_dict(self) -> dict[str, object]:
        """Serialize token to a JSON-compatible dictionary."""
        data = asdict(self)
        if data["normalized"] is None:
            del data["normalized"]
        return data


@dataclass(frozen=True, slots=True)
class LexError:
    """A structured lexical error with source context."""

    message: str
    line: int
    column: int
    source_line: str
    hint: str | None = None

    def format(self, filename: str = "<input>") -> str:
        """Render a compiler-style diagnostic with line pointer."""
        caret_pad = " " * max(0, self.column - 1)
        lines = [
            f"LexError [{filename}:{self.line}:{self.column}]: {self.message}",
            f"  {self.line:>4} | {self.source_line}",
            f"       | {caret_pad}^",
        ]
        if self.hint:
            lines.append(f"  hint: {self.hint}")
        return "\n".join(lines)


@dataclass(frozen=True, slots=True)
class LexResult:
    """Complete output of lexing a source string or file."""

    tokens: list[Token]
    errors: list[LexError]

    @property
    def ok(self) -> bool:
        return len(self.errors) == 0


def strip_tone_diacritics(text: str) -> str:
    """Normalize Unicode and strip combining tone diacritics (e.g., sɔ́ -> sɔ)."""
    decomposed = unicodedata.normalize("NFD", text)
    stripped = "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")
    return unicodedata.normalize("NFC", stripped)


def load_keyword_table(
    keywords_path: Path = DEFAULT_KEYWORDS_PATH,
    tiers: Iterable[str] | None = None,
) -> dict[str, str]:
    """Load keyword -> TokenType mapping for both UTF-8 Kenyang and ASCII fallback."""
    data = json.loads(keywords_path.read_text(encoding="utf-8"))
    allowed_tiers = {t.upper() for t in tiers} if tiers is not None else set(VALID_TIERS)

    table: dict[str, str] = {}
    for entry in data["keywords"]:
        if entry["tier"].upper() not in allowed_tiers:
            continue
        token_type = entry["token"]
        ken_word = strip_tone_diacritics(entry["kenyang"])
        ascii_word = entry["ascii"]

        for form in (ken_word, ascii_word):
            if form in table and table[form] != token_type:
                raise ValueError(
                    f"Keyword collision for '{form}': {table[form]} vs {token_type}"
                )
            table[form] = token_type
    return table


def validate_keyword_table(keywords_path: Path = DEFAULT_KEYWORDS_PATH) -> list[str]:
    """Return a list of any collisions or malformed entries in keywords.json."""
    data = json.loads(keywords_path.read_text(encoding="utf-8"))
    seen: dict[str, tuple[int, str]] = {}
    issues: list[str] = []

    for entry in data["keywords"]:
        kid = entry["id"]
        token_type = entry["token"]
        ken_norm = strip_tone_diacritics(entry["kenyang"])
        ascii_form = entry["ascii"]

        if not ASCII_IDENT_RE.match(ascii_form):
            issues.append(f"#{kid} ({token_type}): invalid ASCII fallback '{ascii_form}'")

        for label, form in (("kenyang", ken_norm), ("ascii", ascii_form)):
            if form in seen and seen[form][1] != token_type:
                prev_id, prev_tok = seen[form]
                issues.append(
                    f"Collision on {label} form '{form}': "
                    f"#{prev_id} {prev_tok} vs #{kid} {token_type}"
                )
            else:
                seen[form] = (kid, token_type)

    return issues


class KenyangLexer:
    """Lark-backed lexer for the Lower Kenyang programming language."""

    def __init__(
        self,
        grammar_path: Path = DEFAULT_GRAMMAR_PATH,
        keywords_path: Path = DEFAULT_KEYWORDS_PATH,
        tiers: Iterable[str] | None = None,
    ) -> None:
        self.grammar_path = grammar_path
        self.keywords_path = keywords_path
        self.keywords = load_keyword_table(keywords_path, tiers=tiers)
        self._lark = Lark.open(
            str(grammar_path),
            parser="lalr",
            lexer="basic",
            propagate_positions=True,
        )

    def tokenize(self, source: str) -> LexResult:
        """Lex source text into Tokens and LexErrors with multi-error recovery."""
        tokens: list[Token] = []
        errors: list[LexError] = []
        source_lines = source.splitlines() or [""]

        pos = 0
        base_line = 1
        base_col = 1
        length = len(source)

        while pos <= length:
            chunk = source[pos:]
            if not chunk:
                break
            try:
                for raw_tok in self._lark.lex(chunk):
                    tok_line = raw_tok.line if raw_tok.line is not None else 1
                    tok_col = raw_tok.column if raw_tok.column is not None else 1
                    tok_end_line = (
                        raw_tok.end_line if raw_tok.end_line is not None else tok_line
                    )
                    tok_end_col = (
                        raw_tok.end_column if raw_tok.end_column is not None else tok_col
                    )

                    abs_line = base_line + (tok_line - 1)
                    abs_col = base_col + tok_col - 1 if tok_line == 1 else tok_col
                    abs_end_line = base_line + (tok_end_line - 1)
                    abs_end_col = (
                        base_col + tok_end_col - 1 if tok_end_line == 1 else tok_end_col
                    )

                    tok_type = raw_tok.type
                    lexeme = raw_tok.value
                    normalized: str | None = None

                    if tok_type == "WORD":
                        norm_word = strip_tone_diacritics(lexeme)
                        if norm_word in self.keywords:
                            tok_type = self.keywords[norm_word]
                            if norm_word != lexeme:
                                normalized = norm_word
                        elif ASCII_IDENT_RE.match(lexeme):
                            tok_type = "IDENT"
                        else:
                            src_line = self._get_line(source_lines, abs_line)
                            errors.append(
                                LexError(
                                    message=f"Invalid identifier '{lexeme}'",
                                    line=abs_line,
                                    column=abs_col,
                                    source_line=src_line,
                                    hint=(
                                        "Non-ASCII Kenyang letters and tone marks are only "
                                        "allowed in keywords and string literals; use ASCII "
                                        "letters for variable/function names."
                                    ),
                                )
                            )
                            continue

                    tokens.append(
                        Token(
                            type=tok_type,
                            lexeme=lexeme,
                            line=abs_line,
                            column=abs_col,
                            end_line=abs_end_line,
                            end_column=abs_end_col,
                            normalized=normalized,
                        )
                    )
                break
            except UnexpectedCharacters as err:
                err_line = err.line if err.line is not None else 1
                err_col = err.column if err.column is not None else 1
                err_pos = err.pos_in_stream if err.pos_in_stream is not None else 0

                abs_line = base_line + (err_line - 1)
                abs_col = base_col + err_col - 1 if err_line == 1 else err_col
                src_line = self._get_line(source_lines, abs_line)
                bad_char = err.char

                if bad_char == '"':
                    msg = "Unterminated string literal"
                    hint = 'Add a closing `"` before the end of the line.'
                    # Recover by skipping to the end of the current line
                    newline_idx = source.find("\n", pos + err_pos)
                    next_pos = len(source) if newline_idx == -1 else newline_idx
                elif bad_char == "/" and source[pos + err_pos : pos + err_pos + 2] == "/*":
                    msg = "Unterminated block comment"
                    hint = "Add a closing `*/`."
                    next_pos = len(source)
                else:
                    msg = f"Unexpected character '{bad_char}' (U+{ord(bad_char):04X})"
                    hint = None
                    next_pos = pos + err_pos + 1

                errors.append(
                    LexError(
                        message=msg,
                        line=abs_line,
                        column=abs_col,
                        source_line=src_line,
                        hint=hint,
                    )
                )

                # Update base_line / base_col up to next_pos
                skipped = source[pos:next_pos]
                base_line, base_col = self._advance_position(base_line, base_col, skipped)
                pos = next_pos

        return LexResult(tokens=tokens, errors=errors)

    def tokenize_file(self, path: Path) -> LexResult:
        """Read a UTF-8 source file and tokenize it."""
        content = path.read_text(encoding="utf-8")
        return self.tokenize(content)

    @staticmethod
    def _get_line(lines: list[str], line_no: int) -> str:
        if 1 <= line_no <= len(lines):
            return lines[line_no - 1]
        return ""

    @staticmethod
    def _advance_position(line: int, col: int, text: str) -> tuple[int, int]:
        if "\n" not in text:
            return line, col + len(text)
        parts = text.split("\n")
        return line + len(parts) - 1, len(parts[-1]) + 1


def _build_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="kenyang-lexer",
        description="Lower Kenyang Lexer (Area 1 - Lark-based)",
    )
    parser.add_argument("file", nargs="?", type=Path, help="Path to .ken source file")
    parser.add_argument("--json", action="store_true", help="Output tokens as JSON")
    parser.add_argument(
        "--tier",
        choices=["core", "standard", "extended"],
        default="extended",
        help="Maximum keyword tier to enable (default: extended)",
    )
    parser.add_argument(
        "--check-keywords",
        action="store_true",
        help="Validate keywords.json for collisions and exit",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding="utf-8")
    if isinstance(sys.stderr, io.TextIOWrapper):
        sys.stderr.reconfigure(encoding="utf-8")

    args = _build_cli().parse_args(argv)

    if args.check_keywords:
        issues = validate_keyword_table()
        if issues:
            for issue in issues:
                print(f"ERROR: {issue}", file=sys.stderr)
            return 1
        data = json.loads(DEFAULT_KEYWORDS_PATH.read_text(encoding="utf-8"))
        print(f"OK: {len(data['keywords'])} keywords validated with 0 collisions.")
        return 0

    if args.file is None:
        print("Error: please provide a .ken source file or --check-keywords.", file=sys.stderr)
        return 2

    tier_map = {
        "core": ("CORE",),
        "standard": ("CORE", "STANDARD"),
        "extended": ("CORE", "STANDARD", "EXTENDED"),
    }
    lexer = KenyangLexer(tiers=tier_map[args.tier])
    result = lexer.tokenize_file(args.file)

    if args.json:
        payload = {
            "ok": result.ok,
            "tokens": [t.to_dict() for t in result.tokens],
            "errors": [asdict(e) for e in result.errors],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for tok in result.tokens:
            print(f"{tok.line:>3}:{tok.column:<3}  {tok.type:<14}  {tok.lexeme!r}")
        if result.errors:
            print("", file=sys.stderr)
            for err in result.errors:
                print(err.format(str(args.file)), file=sys.stderr)

    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
