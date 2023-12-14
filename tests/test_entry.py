from pathlib import Path

from renamer.entry import rename_all, rename_function


def get_codes(test_postfix: str) -> tuple[str, str]:
    source_path = Path(__file__).parent / "fixtures" / f"input{test_postfix}.py"
    expected_path = Path(__file__).parent / "fixtures" / f"output{test_postfix}.py"
    return source_path.read_text(), expected_path.read_text()


def test_rename_all(codes: tuple[str, str] = get_codes("1")):
    source_code, expected_code = codes
    got = rename_all(
        source_code,
        "arg1",
        "arg3",
    )
    got = rename_all(
        got,
        "func",
        "func1",
    )
    got = rename_all(
        got,
        "TestClass",
        "TestClass1",
    )

    assert got == expected_code


def test_rename_function(codes: tuple[str, str] = get_codes("2")):
    source_code, expected_code = codes
    got = rename_function(
        source_code,
        "arg1",
        "arg3",
    )
    got = rename_function(
        got,
        "func",
        "func1",
    )
    got = rename_function(
        got,
        "function",
        "function1",
    )
    got = rename_function(
        got,
        "TestClass",
        "TestClass1",
    )

    assert got == expected_code
