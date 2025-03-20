import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_default_values(self):
        n = HTMLNode()
        self.assertEqual(n.tag, None)
        self.assertEqual(n.value, None)
        self.assertEqual(n.children, None)
        self.assertEqual(n.props, None)

    def test_props_set_ints(self):
        props: dict[str, str | int] = {"width": 1, "height": 2}
        n = HTMLNode(props=props)
        self.assertEqual('width="1" height="2"', n.props_to_html())

    def test_props_set_str(self):
        props: dict[str, str | int] = {"href": "https://example.com", "title": "foobar"}
        n = HTMLNode(props=props)
        self.assertEqual('href="https://example.com" title="foobar"', n.props_to_html())


if __name__ == "__main__":
    unittest.main()
