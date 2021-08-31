import ast
import csv
import logging
import os
import sys
import urllib
import zipfile
from pathlib import Path
from typing import List

from pattern_mining.helper import *
from pattern_mining.torch_model_diff import TorchModelDiff

logging.basicConfig(filename='out.txt',
                    filemode='a',
                    # format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    format='%(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))


class PatternMiner:
    def __init__(self, repo_list):
        self.repo_list = repo_list
        self.frequencies = {}

    def mine(self):
        for n, repo_name in enumerate(self.repo_list, start=1):
            self.mine_repo(repo_name, n)

    def mine_repo(self, repo_name, n):
        logger.info(f'Repo {n}: {repo_name}')
        try:
            repo_root = download_repo(repo_name)
        except:
            logger.error('FAILED')
            return
        for path in Path(repo_root).rglob('*.py'):
            try:
                self.mine_file(path, repo_name)
            except SyntaxError:
                logger.error('Syntax error')

    def mine_file(self, file_path, repo: str):
        with open(file_path, "r") as source:
            code = source.read()
            tree = ast.parse(code)
            classes = [item for item in tree.body if isinstance(item, ast.ClassDef)]
            code_lines = code.splitlines()
            for cls in classes:
                self.mine_class(cls, repo, file_path, code_lines)

    def mine_class(self, cls: ast.ClassDef, repo: str, file_path: str, code_lines) -> Any:
        is_model = is_torch_model_class(cls)
        if is_model:
            call_diff: List[ast.Call] = TorchModelDiff(cls).get_diff()
            for c in call_diff:
                out_writer.writerow([
                    function_name(c.func),
                    repo,
                    file_path,
                    c.lineno,
                    code_lines[c.lineno - 1].strip(),
                ])


repo_folder = '/media/mohayemin/Work/PhD/LibMigProto-Data/clients'
repo_folder = '/home/mohayemin/Desktop/client_repositories'


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
    repos.sort()
    return repos


if __name__ == '__main__':
    with open('all_diffs.csv', 'w') as file:
        out_writer = csv.writer(file)
        out_writer.writerow(["API", "repository", "file", "line", "code"])
        # root = '/media/mohayemin/Work/PhD/soar-fork/autotesting/benchmarks_tf'
        # root = '/media/mohayemin/Work/PhD/LibMigProto-Data/ocr_kor'
        # root = '/media/mohayemin/Work/PhD/LibMigProto-Data/Bringing-Old-Photos-Back-to-Life'

        # file_path = '/media/mohayemin/Work/PhD/soar-fork/autotesting/benchmarks_tf/auto_encoder.py'
        # file_miner = FileMiner(file_path, '/media/mohayemin/Work/PhD/soar-fork/autotesting/', 'SOAR Benchmarks')
        # file_miner.mine()

        logger.info('start mining')
        list_of_repos = [
            '__soar_benchmarks/benchmarks'
        ]
        list_of_repos = get_repo_list()

        logger.info(f'{len(list_of_repos)} repositories')
        PatternMiner(list_of_repos).mine()
        logger.info('done mining')
