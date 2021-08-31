import ast

from pattern_mining.helper import find_method, CallVisitor, function_name


class TorchModelDiff:
    def __init__(self, model_class: ast.ClassDef):
        self.model_class = model_class

    def get_diff(self) -> [ast.Call]:
        init = find_method(self.model_class, "__init__")
        assignments = filter(lambda stm: isinstance(stm, ast.Assign), init.body)
        targets = set(map(lambda asg: function_name(asg.targets[0]), assignments))

        forward = find_method(self.model_class, "forward")
        calls = CallVisitor(forward).find_calls()

        diff = list(filter(lambda c: function_name(c.func) not in targets, calls))
        return diff
