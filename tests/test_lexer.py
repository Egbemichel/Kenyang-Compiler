"""Comprehensive test suite for the Lower Kenyang Lexer (Area 1)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.lexer import (
    DEFAULT_KEYWORDS_PATH,
    KenyangLexer,
    main as lexer_main,
    strip_tone_diacritics,
    validate_keyword_table,
)


ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def lexer() -> KenyangLexer:
    return KenyangLexer()


def test_keyword_table_has_70_entries_and_zero_collisions() -> None:
    data = json.loads(DEFAULT_KEYWORDS_PATH.read_text(encoding="utf-8"))
    assert len(data["keywords"]) == 70
    issues = validate_keyword_table()
    assert issues == []


def test_all_70_keywords_utf8_and_ascii(lexer: KenyangLexer) -> None:
    data = json.loads(DEFAULT_KEYWORDS_PATH.read_text(encoding="utf-8"))
    for entry in data["keywords"]:
        expected = entry["token"]
        res_ken = lexer.tokenize(entry["kenyang"])
        assert res_ken.ok, f"Errors lexing {entry['kenyang']}: {res_ken.errors}"
        assert [t.type for t in res_ken.tokens] == [expected]

        res_asc = lexer.tokenize(entry["ascii"])
        assert res_asc.ok, f"Errors lexing {entry['ascii']}: {res_asc.errors}"
        assert [t.type for t in res_asc.tokens] == [expected]


def test_tone_diacritics_stripped_for_keywords(lexer: KenyangLexer) -> None:
    src = "sɔ́ páy kátí búrɛ́ tɛ́tɛ́p"
    res = lexer.tokenize(src)
    assert res.ok
    assert [t.type for t in res.tokens] == [
        "KW_WRITE",
        "KW_READ",
        "KW_BREAK",
        "KW_CONST",
        "KW_TRUE",
    ]
    assert strip_tone_diacritics("sɔ́") == "sɔ"


def test_utf8_and_ascii_factorial_produce_identical_token_types(lexer: KenyangLexer) -> None:
    utf8_res = lexer.tokenize_file(ROOT / "examples" / "factorial_utf8.ken")
    ascii_res = lexer.tokenize_file(ROOT / "examples" / "factorial_ascii.ken")

    assert utf8_res.ok
    assert ascii_res.ok
    assert [t.type for t in utf8_res.tokens] == [t.type for t in ascii_res.tokens]


def test_operators_literals_and_comments(lexer: KenyangLexer) -> None:
    src = """
    // line comment
    pɨ x = 42;
    /* multi-line
       comment */
    pɨ_kati y = 3.14;
    bɛyɔŋ msg = "hello \\"kenyang\\"";
    yat (x >= 10 ne y != 0.0) { sɔ(msg); }
    """
    res = lexer.tokenize(src)
    assert res.ok
    types = [t.type for t in res.tokens]
    assert types == [
        "KW_INT", "IDENT", "ASSIGN", "INT_LIT", "SEMI",
        "KW_FLOAT", "IDENT", "ASSIGN", "FLOAT_LIT", "SEMI",
        "KW_STRING", "IDENT", "ASSIGN", "STRING_LIT", "SEMI",
        "KW_IF", "LPAREN", "IDENT", "GE", "INT_LIT", "KW_AND",
        "IDENT", "NEQ", "FLOAT_LIT", "RPAREN", "LBRACE",
        "KW_WRITE", "LPAREN", "IDENT", "RPAREN", "SEMI", "RBRACE",
    ]
    # Verify exact line tracking after multi-line comment
    y_tok = [t for t in res.tokens if t.lexeme == "y"][0]
    assert y_tok.line == 6


def test_multi_error_recovery_and_positions(lexer: KenyangLexer) -> None:
    src = 'pɨ x = @ 10;\nsɔ("unterminated\npɨ $ = 5;'
    res = lexer.tokenize(src)
    assert not res.ok
    assert len(res.errors) == 3

    assert res.errors[0].line == 1
    assert res.errors[0].column == 8
    assert "@" in res.errors[0].message

    assert res.errors[1].line == 2
    assert "Unterminated string literal" in res.errors[1].message

    assert res.errors[2].line == 3
    assert res.errors[2].column == 4
    assert "$" in res.errors[2].message

    # Valid tokens around errors were still recovered
    assert "INT_LIT" in [t.type for t in res.tokens]
    formatted = res.errors[0].format("test.ken")
    assert "test.ken:1:8" in formatted
    assert "^" in formatted


def test_invalid_non_ascii_identifier_reports_helpful_error(lexer: KenyangLexer) -> None:
    res = lexer.tokenize("pɨ xɛ = 1;")
    assert not res.ok
    assert len(res.errors) == 1
    assert "Invalid identifier 'xɛ'" in res.errors[0].message
    assert res.errors[0].hint is not None


def test_cli_check_keywords_and_json_output(capsys: pytest.CaptureFixture[str]) -> None:
    rc = lexer_main(["--check-keywords"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "70 keywords validated" in out

    rc_json = lexer_main([str(ROOT / "examples" / "factorial_utf8.ken"), "--json"])
    assert rc_json == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["ok"] is True
    assert len(payload["tokens"]) > 20


def test_all_example_programs_lex_cleanly(lexer: KenyangLexer) -> None:
    examples = sorted((ROOT / "examples").glob("*.ken"))
    assert len(examples) >= 5
    for path in examples:
        res = lexer.tokenize_file(path)
        assert res.ok, f"{path.name} failed to lex: {res.errors}"
        assert len(res.tokens) > 0
