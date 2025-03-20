import unittest

from htmlnode import HTMLNode
from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_children_none_by_default(self):
        n = LeafNode()
        self.assertEqual(n.children, None)

    def test_children_cannot_be_set(self):
        children = [
            HTMLNode(),
            HTMLNode(),
            HTMLNode(),
        ]
        n = LeafNode("foo", "bar", children)
        self.assertEqual(n.children, None)

    def test_to_html(self):
        n = LeafNode("p", "hello world", None, {"style": "color:red;"})
        html = n.to_html()
        self.assertEqual(html, '<p style="color:red;">hello world</p>')


if __name__ == "__main__":
    unittest.main()
