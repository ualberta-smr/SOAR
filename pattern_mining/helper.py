import ast
from typing import Optional, Union, Any

import torch


class CallVisitor(ast.NodeVisitor):
    def __init__(self, init_method: ast.FunctionDef,):
        self.init_method = init_method
        self.calls: [ast.Call] = []

    def find_calls(self) -> [ast.Call]:
        self.visit(self.init_method)
        return self.calls

    def visit_Call(self, call: ast.Call) -> Any:
        self.calls.append(call)
        self.generic_visit(call)


def is_torch_model_class(cls: ast.ClassDef):
    is_model = any(extends_module(base_class) for base_class in cls.bases)
    is_model = is_model and (find_method(cls, 'forward') is not None)
    is_model = is_model and (find_method(cls, '__init__') is not None)
    return is_model


def find_method(cls: ast.ClassDef, method_name: str) -> Optional[ast.FunctionDef]:
    method = next((func for func in cls.body if isinstance(func, ast.FunctionDef) and func.name == method_name), None)
    return method


def extends_module(cls) -> bool:
    if isinstance(cls, ast.Attribute):
        return 'Module' in cls.attr
    if isinstance(cls, ast.Name):
        return 'Module' in cls.id
    return False


def function_name(func: Union[ast.Attribute, ast.Name]) -> str:
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return None


def function_name_from_assignment(assignment: ast.stmt):
    name = ''
    if isinstance(assignment, ast.Assign):
        val = assignment.value

        if isinstance(val, ast.Call):
            name = function_name(val.func)
        elif isinstance(val, ast.Lambda) and isinstance(val.body, ast.Call):
            name = "lambda:" + function_name(val.body.func)
        else:
            name = 'unknown'

    name = name or ''
    is_torch = hasattr(torch.nn, name)

    if is_torch:
        name = 'torch.nn' + name

    return name, is_torch



