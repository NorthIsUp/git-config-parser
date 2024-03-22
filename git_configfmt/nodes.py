import logging
from dataclasses import dataclass
from typing import Iterable

from tree_sitter import Node, Tree

standard_node = set(dir(Node))

logger = logging.getLogger(__name__)


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


@dataclass
class Visitor:
    tree: Tree

    def walk(self):
        for node in self.nodes:
            if hasattr(self, f"visit_{node.type}"):
                getattr(self, f"visit_{node.type}")(node)

    @property
    def nodes(self) -> Iterable[Node]:
        cursor = self.tree.walk()

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

    def visit_config(self, node: Node):
        logger.debug("visiting config")

    def visit_section(self, node: Node):
        logger.debug("visiting section")
        print(f"config: {node.text.decode()}")

    def visit_section_header(self, node: Node):
        logger.debug("visiting section_header")

    def visit_section_name(self, node: Node):
        logger.debug("visiting section_name")
        print(f"section_name: {node.text.decode()}")

    def visit__section_body(self, node: Node):
        logger.debug("visiting _section_body")

    def visit_subsection_name(self, node: Node):
        logger.debug("visiting subsection_name")

    def visit_variable(self, node: Node):
        logger.debug("visiting variable")

    def visit_name(self, node: Node):
        logger.debug("visiting name")

    def visit__value(self, node: Node):
        logger.debug("visiting _value")

    def visit__boolean(self, node: Node):
        logger.debug("visiting _boolean")

    def visit_true(self, node: Node):
        logger.debug("visiting true")

    def visit_false(self, node: Node):
        logger.debug("visiting false")

    def visit_integer(self, node: Node):
        logger.debug("visiting integer")

    def visit_string(self, node: Node):
        logger.debug("visiting string")

    def visit__quoted_string(self, node: Node):
        logger.debug("visiting _quoted_string")

    def visit__unquoted_string(self, node: Node):
        logger.debug("visiting _unquoted_string")

    def visit_escape_sequence(self, node: Node):
        logger.debug("visiting escape_sequence")

    def visit_comment(self, node: Node):
        logger.debug("visiting comment")
