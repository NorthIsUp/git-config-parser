import logging
from functools import lru_cache
from pathlib import Path

from tree_sitter import Language, Parser, Tree

logger = logging.getLogger(__name__)


def get_language(clean: bool = False):
    logger.info("building library")
    dst = "build/tree-sitter.so"
    if clean and Path(dst).exists():
        Path(dst).unlink()

    Language.build_library(
        # Store the library in the `build` directory
        "build/tree-sitter.so",
        # Include one or more languages
        [
            "vendor/tree-sitter-git-config",
        ],
    )
    logger.info("built library")
    return Language("build/tree-sitter.so", "git_config")


@lru_cache()
def get_parser():
    parser = Parser()
    parser.set_language(get_language())
    return parser


def parse_tree(gitconfig: Path):
    return get_parser().parse(gitconfig.read_bytes())


def format_tree(tree: Tree):
    for node in traverse_tree(tree):
        print(node)


def traverse_tree(tree: Tree):
    cursor = tree.walk()

    reached_root = False
    while reached_root == False:
        yield cursor.node

        if cursor.goto_first_child():
            continue

        if cursor.goto_next_sibling():
            continue

        retracing = True
        while retracing:
            if not cursor.goto_parent():
                retracing = False
                reached_root = True

            if cursor.goto_next_sibling():
                retracing = False
