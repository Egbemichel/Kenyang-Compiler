"""Tests for the semantic analyser (Area 3)."""

from __future__ import annotations

from src.compiler import compile_source
from tests.helpers import EXAMPLES


def errors_for(body: str, extra: str = "") -> list[str]:
    source = f"{extra}\nkʉ main() : ngwɔ {{\n{body}\n}}"
    result = compile_source(source, "t.ken")
    return result.errors


def one_error(body: str, extra: str = "") -> str:
    errors = errors_for(body, extra)
    assert len(errors) == 1, errors
    return errors[0]


def test_valid_programs_have_no_errors() -> None:
    for path in sorted(EXAMPLES.glob("*.ken")):
        result = compile_source(path.read_text(encoding="utf-8"), path.name)
        assert result.ok, f"{path.name}: {result.errors}"


def test_undeclared_name_with_suggestion() -> None:
    message = one_error("pɨ count = 1; sɔ(cuont);")
    assert "'cuont' is not declared" in message
    assert "Did you mean 'count'?" in message


def test_redeclaration_in_same_scope() -> None:
    assert "already declared" in one_error("pɨ x = 1; pɨ x = 2;")


def test_inner_scope_may_reuse_a_name() -> None:
    assert errors_for("pɨ x = 1; yat (x == 1) { pɨ x = 2; sɔ(x); } sɔ(x);") == []


def test_variable_is_not_visible_after_its_block() -> None:
    assert "not declared" in one_error("yat (tɛtɛp) { pɨ y = 1; } sɔ(y);")


def test_type_mismatch_in_declaration_and_assignment() -> None:
    assert "cannot store string in 'x', which is int" in one_error('pɨ x = "no";')
    assert "cannot store int in 's'" in one_error('bɛyɔŋ s = "a"; s = 5;')


def test_condition_must_be_bool() -> None:
    assert "must be bool" in one_error("yat (1) { }")
    assert "must be bool" in one_error("kʉ_te (2 + 2) { }")


def test_operator_types() -> None:
    assert "needs two ints" in one_error("pɨ x = tɛtɛp + 1;")
    assert "needs two bools" in one_error("tɛp b = 1 ne 2;")
    assert "needs a bool" in one_error("tɛp b = ka 3;")
    assert "needs an int" in one_error("pɨ x = -tɛtɛp;")
    assert "same type" in one_error("tɛp b = 1 == tɛtɛp;")


def test_string_operations_that_are_not_supported() -> None:
    assert "comparing strings" in one_error('tɛp b = "a" == "b";')
    assert "needs two ints" in one_error('bɛyɔŋ s = "a" + "b";')


def test_call_checks() -> None:
    helper = "kʉ add(pɨ a, pɨ b) : pɨ { piti a + b; }"
    assert "takes 2 argument(s) but 1" in one_error("sɔ(add(1));", helper)
    assert "argument 2 of 'add' should be int" in one_error("sɔ(add(1, tɛtɛp));", helper)
    assert "is not defined" in one_error("sɔ(nothing(1));", helper)


def test_void_function_has_no_value() -> None:
    helper = "kʉ hush() : ngwɔ { piti; }"
    assert "no value" in one_error("sɔ(hush());", helper)
    assert errors_for("hush();", helper) == []


def test_return_rules() -> None:
    result = compile_source("kʉ f() : pɨ { piti tɛtɛp; } kʉ main() : ngwɔ { }", "t.ken")
    assert any("returns int" in e for e in result.errors)
    result = compile_source("kʉ f() : pɨ { piti; } kʉ main() : ngwɔ { }", "t.ken")
    assert any("must return a int" in e for e in result.errors)
    result = compile_source("kʉ main() : ngwɔ { piti 1; }", "t.ken")
    assert any("void function cannot return" in e for e in result.errors)


def test_function_must_return_on_every_path() -> None:
    bad = "kʉ f(pɨ n) : pɨ { yat (n > 0) { piti 1; } } kʉ main() : ngwɔ { }"
    assert any("may end without returning" in e for e in compile_source(bad, "t.ken").errors)
    good = "kʉ f(pɨ n) : pɨ { yat (n > 0) { piti 1; } rɔ { piti 2; } } kʉ main() : ngwɔ { }"
    assert compile_source(good, "t.ken").ok


def test_break_and_continue_need_a_loop() -> None:
    assert "inside a loop" in one_error("kati;")
    assert "inside a loop" in one_error("chak;")
    assert errors_for("kʉ_te (tɛtɛp) { kati; }") == []


def test_read_needs_an_int_variable() -> None:
    assert "only fill an int" in one_error('bɛyɔŋ s = "a"; pay(s);')
    assert "not declared" in one_error("pay(zzz);")


def test_main_rules() -> None:
    assert "no 'main'" in compile_source("kʉ f() : ngwɔ { }", "t.ken").errors[0]
    result = compile_source("kʉ main(pɨ a) : ngwɔ { }", "t.ken")
    assert any("must not take parameters" in e for e in result.errors)


def test_duplicate_function() -> None:
    result = compile_source("kʉ f() { } kʉ f() { } kʉ main() { }", "t.ken")
    assert any("already defined" in e for e in result.errors)


def test_unsupported_types_and_huge_numbers() -> None:
    assert "not supported" in one_error("pɨ_kati x;")
    assert "too large" in one_error("pɨ x = 9223372036854775808;")


def test_var_keyword_needs_a_value_and_takes_its_type() -> None:
    assert "needs a starting value" in one_error("ŋati x;")
    assert errors_for('ŋati s = "a"; bɛyɔŋ t = s;') == []


def test_several_errors_are_all_reported() -> None:
    result = compile_source(
        "kʉ main() : ngwɔ { pɨ a = tɛtɛp; pɨ b = \"x\"; sɔ(c); }", "t.ken")
    assert len(result.errors) == 3


def test_expression_types_are_written_on_the_tree() -> None:
    result = compile_source("kʉ main() : ngwɔ { sɔ(1 < 2); }", "t.ken")
    write = result.program.functions[0].body.stmts[0]
    assert write.value.ty == "bool"
