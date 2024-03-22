import argparse
from pathlib import Path

from git_configfmt.formatter import format_tree, get_language, parse_tree
from git_configfmt.nodes import Visitor


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("gitconfig", type=Path)
    parser.add_argument("--clean", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    print(args.gitconfig)
    if args.clean:
        get_language(clean=True)
    tree = parse_tree(args.gitconfig)
    visitor = Visitor(tree)
    visitor.walk()
