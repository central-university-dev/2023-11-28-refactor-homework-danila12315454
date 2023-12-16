from typing import override, Optional
import black

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


def move_function(
    function_name: str, from_code: str, destination_code: str
) -> tuple[str, str]:
    tree = cst.parse_module(from_code)

    function_node = _get_function_node(function_name=function_name, code_tree=tree)

    tree = tree.with_changes(
        body=[node for node in tree.body if node is not function_node]
    )

    destination_tree = cst.parse_module(destination_code)
    destination_tree = destination_tree.with_changes(
        body=tuple([*destination_tree.body, function_node])
    )

    updated_from_code = black.format_str(tree.code, mode=black.FileMode())
    updated_destination_code = black.format_str(
        destination_tree.code, mode=black.FileMode()
    )

    return updated_from_code, updated_destination_code
