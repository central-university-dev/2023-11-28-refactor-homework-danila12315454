from pathlib import Path

import pytest

from renamer.entry import (
    rename_all,
    rename_function,
    move_function_between_files,
)


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


def test_move_function_between_files() -> None:
    output_from_code = Path(__file__).parent / "fixtures" / "output3_from.py"
    output_destination_code = (
        Path(__file__).parent / "fixtures" / "output3_destination.py"
    )
    from_code_got, destination_code_got = move_function_between_files(
        function_name="func",
        source_path=Path(__file__).parent / "fixtures" / "input3_from.py",
        destination_path=Path(__file__).parent / "fixtures" / "input3_destination.py",
    )

    assert (
        from_code_got == output_from_code.read_text()
        and destination_code_got == output_destination_code.read_text()
    )


def test_move_function_between_files_exception() -> None:
    with pytest.raises(ValueError):
        from_code_got, destination_code_got = move_function_between_files(
            function_name="func1",
            source_path=Path(__file__).parent / "fixtures" / "input3_from.py",
            destination_path=Path(__file__).parent / "fixtures" / "input3_destination.py",
        )
