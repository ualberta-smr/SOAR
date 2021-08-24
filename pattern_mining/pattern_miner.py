import ast
import os
import urllib
import zipfile
from pathlib import Path
from typing import Any

from pattern_mining.helper import *


class InitVisitor(ast.NodeVisitor):
    def __init__(self, init_method: ast.FunctionDef, full_code: str):
        self.surrounding_api_calls: [ast.Call] = []
        self.init_method = init_method
        self.full_code = full_code

    def do_visit(self):
        self.visit(self.init_method)

    def visit_Call(self, call: ast.Call) -> Any:
        func: ast.Attribute = call.func
        if isinstance(func, ast.Attribute):
            func_name = str(func.attr)
            if any(func in func_name for func in ['permute', 'long', 'view']):
                self.surrounding_api_calls.append(call)

        self.generic_visit(call)

    def print(self, file_path):
        if self.surrounding_api_calls:
            code_lines = self.full_code.splitlines()
            print(f'=== {file_path} ===')
            for call in self.surrounding_api_calls:
                start = call.func.lineno - 3
                end = start + 4
                if start < 0:
                    start = 0
                print(f'line {call.func.lineno}: {call.func.attr}')
                print(*code_lines[start: end], sep='\n')


class PatternMiner:
    def __init__(self, repo_list):
        self.repo_list = repo_list

    def mine(self):
        for repo_name in self.repo_list:
            self.mine_repo(repo_name)

    def mine_repo(self, repo_name):
        print(f'----{repo_name}----')
        try:
            repo_root = download_repo(repo_name)
        except:
            print('FAILED')
            return
        for path in Path(repo_root).rglob('*.py'):
            file_miner = FileMiner(path)
            file_miner.mine()


class FileMiner:
    def __init__(self, filepath):
        self.surrounding_api_calls = []
        self.filepath = filepath
        with open(self.filepath, "r") as source:
            self.code = source.read()

        tree = ast.parse(self.code)
        self.classes = [item for item in tree.body if isinstance(item, ast.ClassDef)]

    def mine(self):
        for cls in self.classes:
            self.mine_class(cls)

    def mine_class(self, cls: ast.ClassDef) -> Any:
        is_model = is_torch_model_class(cls)
        if is_model:
            init_method = find_method(cls, '__init__')
            init_visitor = InitVisitor(init_method, self.code)
            init_visitor.do_visit()
            init_visitor.print(self.filepath)



repo_folder = '/media/mohayemin/Work/PhD/LibMigProto-Data/clients'


def download_repo(repo_fullname):
    owner_name, repo_name = repo_fullname.split('/')
    extract_to = f'{repo_folder}/{owner_name}'
    repo_path = f'{extract_to}/{repo_name}'
    if os.path.exists(repo_path):
        return repo_path

    main_branch = 'master'
    try:
        url = f'https://github.com/{repo_fullname}/archive/refs/heads/{main_branch}.zip'
        filepath, headers = urllib.request.urlretrieve(url)
    except:
        main_branch = 'main'
        url = f'https://github.com/{repo_fullname}/archive/refs/heads/{main_branch}.zip'
        filepath, headers = urllib.request.urlretrieve(url)

    with zipfile.ZipFile(filepath, 'r') as zip_ref:
        zip_ref.extractall(f'{extract_to}')

    os.rename(f'{repo_path}-{main_branch}', repo_path)
    os.remove(filepath)
    return repo_path


def get_repo_list():
    with open('./repositories.txt') as file:
        repos = file.read().splitlines()
    return repos


if __name__ == '__main__':
    # root = '/media/mohayemin/Work/PhD/soar-fork/autotesting/benchmarks_tf'
    # root = '/media/mohayemin/Work/PhD/LibMigProto-Data/ocr_kor'
    # root = '/media/mohayemin/Work/PhD/LibMigProto-Data/Bringing-Old-Photos-Back-to-Life'

    file_path = '/media/mohayemin/Work/PhD/soar-fork/autotesting/benchmarks_tf/alexnet.py'
    file_miner = FileMiner(file_path)
    file_miner.mine()

    # list_of_repos = get_repo_list()
    # PatternMiner(list_of_repos).mine()
