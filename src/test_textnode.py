import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        a = TextNode("This is a text node", TextType.BOLD)
        b = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(a, b)

    def test_not_eq(self):
        a = TextNode("This is a text node", TextType.BOLD)
        b = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(a, b)

    def test_url_default_is_none(self):
        a = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(a.url, None)

    def test_url_isset(self):
        a = TextNode("This is a text node", TextType.BOLD, "http://example.com")
        self.assertEqual(a.url, "http://example.com")

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("lorem ipsum", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "lorem ipsum")
        self.assertEqual(html_node.to_html(), "<b>lorem ipsum</b>")

    def test_italic(self):
        node = TextNode("lorem ipsum", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "lorem ipsum")
        self.assertEqual(html_node.to_html(), "<i>lorem ipsum</i>")

    def test_code(self):
        node = TextNode("lorem ipsum", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "lorem ipsum")
        self.assertEqual(html_node.to_html(), "<code>lorem ipsum</code>")

    def test_link(self):
        node = TextNode("lorem ipsum", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "lorem ipsum")
        self.assertEqual(
            html_node.to_html(), '<a href="https://example.com">lorem ipsum</a>'
        )

    def test_image(self):
        node = TextNode("lorem ipsum", TextType.IMAGE, "https://example.com/foo.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.to_html(),
            '<img src="https://example.com/foo.png" alt="lorem ipsum" />',
        )


if __name__ == "__main__":
    unittest.main()
