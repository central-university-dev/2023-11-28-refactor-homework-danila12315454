from pathlib import Path

import pytest

from renamer.entry import rename_all, rename_function, move_function


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


def test_move_function(
    from_codes: tuple[str, str] = get_codes("3_from"),
    destination_codes: tuple[str, str] = get_codes("3_destination"),
) -> None:
    from_code_input, from_code_expected = from_codes
    destination_code_input, destination_code_expected = destination_codes

    from_code_got, destination_code_got = move_function(
        function_name="func",
        from_code=from_code_input,
        destination_code=destination_code_input,
    )

    assert (
        from_code_got == from_code_expected
        and destination_code_got == destination_code_expected
    )


def test_move_function_exception(
    from_codes: tuple[str, str] = get_codes("3_from"),
    destination_codes: tuple[str, str] = get_codes("3_destination"),
) -> None:
    from_code_input, from_code_expected = from_codes
    destination_code_input, destination_code_expected = destination_codes

    with pytest.raises(ValueError):
        from_code_got, destination_code_got = move_function(
            function_name="func1",
            from_code=from_code_input,
            destination_code=destination_code_input,
        )
