from typing import override, Optional
import black
from pathlib import Path
from libcst import parse_module
from libcst.metadata import PositionProvider, CodePosition
from libcst import Module, Import, ImportFrom, ImportAlias
import libcst as cst


def _rename_any(
    source_code: str,
    rename_transformer_instance: cst.CSTTransformer,
) -> str:
    tree = cst.parse_module(source_code)
    tree = tree.visit(rename_transformer_instance)

    updated_code = tree.code

    return updated_code


def rename_all(source_code: str, old_name: str, new_name: str) -> str:
    @override
    class RenameAllTransformer(cst.CSTTransformer):
        def leave_Name(
            self, original_node: cst.Name, updated_node: cst.Name
        ) -> cst.Name:
            if original_node.value == old_name:
                updated_node = updated_node.with_changes(value=new_name)
            return updated_node

    return _rename_any(
        source_code=source_code,
        rename_transformer_instance=RenameAllTransformer(),
    )


def rename_function(source_code: str, old_name: str, new_name: str) -> str:
    @override
    class RenameFunctionTransformer(cst.CSTTransformer):
        def leave_FunctionDef(
            self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef
        ) -> cst.FunctionDef:
            if original_node.name.value == old_name:
                updated_node = updated_node.with_changes(
                    name=updated_node.name.with_changes(value=new_name)
                )
            return updated_node

    return _rename_any(
        source_code=source_code,
        rename_transformer_instance=RenameFunctionTransformer(),
    )


def _get_function_node(function_name: str, code_tree: cst.Module) -> cst.FunctionDef:
    function_node = None
    for node in code_tree.body:
        if isinstance(node, cst.FunctionDef) and node.name.value == function_name:
            function_node = node
            break

    if function_node is None:
        raise ValueError(f"Function '{function_name}' not found in the source code.")
    return function_node


def move_function_between_files(
    source_path: Path, destination_path: Path, function_name: str
) -> tuple[str, str]:
    source_tree = parse_module(source_path.read_text())

    function_node = _get_function_node(
        function_name=function_name, code_tree=source_tree
    )
    source_tree = source_tree.deep_remove(function_node)

    destination_tree = parse_module(destination_path.read_text())

    import_statement = ImportFrom(
        module=cst.Name(destination_path.stem),
        names=[ImportAlias(name=function_node.name, asname=None)],
    )

    destination_tree = destination_tree.with_changes(
        body=tuple([*destination_tree.body, function_node])
    )

    source_tree = source_tree.with_changes(
        body=tuple([import_statement, *source_tree.body])
    )

    updated_from_code = black.format_str(source_tree.code, mode=black.FileMode())
    updated_destination_code = black.format_str(
        destination_tree.code, mode=black.FileMode()
    )

    return updated_from_code, updated_destination_code
