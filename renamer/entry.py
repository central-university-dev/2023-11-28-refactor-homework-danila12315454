from typing import override

import libcst as cst


def _rename_any(
    source_code: str,
    old_name: str,
    new_name: str,
    rename_transformer_instance: cst.CSTTransformer,
):
    tree = cst.parse_module(source_code)
    tree = tree.visit(rename_transformer_instance)

    updated_code = tree.code

    return updated_code


def rename_all(source_code: str, old_name: str, new_name: str):
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
        old_name=old_name,
        new_name=new_name,
        rename_transformer_instance=RenameAllTransformer(),
    )


def rename_function(source_code: str, old_name: str, new_name: str):
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
        old_name=old_name,
        new_name=new_name,
        rename_transformer_instance=RenameFunctionTransformer(),
    )


# def move_function(source_code, function_name, destination_module):
#     tree = cst.parse_module(source_code)
#
#     # Find the function to be moved
#     function_node = None
#     for node in tree.body:
#         if isinstance(node, cst.FunctionDef) and node.name.value == function_name:
#             function_node = node
#             break
#
#     if function_node is None:
#         raise ValueError(f"Function '{function_name}' not found in the source code.")
#
#     # Remove the function from its current location
#     tree.with_changes(body=[node for node in tree.body if node is not function_node])
#
#     # Add the function to the destination module
#     destination_tree = cst.parse_module(destination_module)
#     destination_tree.body.append(function_node)
#
#     # Serialize the updated CST back to source code
#     updated_code = destination_tree.code
#
#     return updated_code
