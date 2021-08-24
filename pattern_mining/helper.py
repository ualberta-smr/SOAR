import ast
from typing import Optional


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
