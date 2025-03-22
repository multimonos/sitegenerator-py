import unittest

from parsing import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
)
from textnode import TextNode, TextType


class TestParsing(unittest.TestCase):
    def test_split_code_one(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_split_code_many(self):
        a = TextNode("This is text with a `code block` word", TextType.TEXT)
        b = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([a, b], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 6)
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[3].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[4].text_type, TextType.CODE)
        self.assertEqual(new_nodes[5].text_type, TextType.TEXT)

    def test_split_bold(self):
        node = TextNode("This **bolded** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_split_multiple(self):
        n = TextNode(
            "This is the **first** instance and this is **second** instance and the **last**",
            TextType.TEXT,
        )
        nodes = split_nodes_delimiter([n], "**", TextType.BOLD)
        self.assertEqual(len(nodes), 6)
        self.assertEqual(nodes[0].text, "This is the ")
        self.assertEqual(nodes[1].text, "first")
        self.assertEqual(nodes[2].text, " instance and this is ")
        self.assertEqual(nodes[3].text, "second")
        self.assertEqual(nodes[4].text, " instance and the ")
        self.assertEqual(nodes[5].text, "last")

    def test_extract_markdown_images_one(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertEqual(len(matches), 2)

    def test_extract_markdown_images_nomatch(self):
        text = "This is text with no links"
        matches = extract_markdown_images(text)
        self.assertEqual(len(matches), 0)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertEqual(len(matches), 2)

    def test_extract_markdown_links_nomatch(self):
        text = "This is text with no links"
        matches = extract_markdown_links(text)
        self.assertEqual(len(matches), 0)

    def test_extract_markdown_image_only(self):
        text = "This is text with a ![first is image](https://i.imgur.com/aKaOqIh.gif) and [second is link](https://.example.com)"
        matches = extract_markdown_images(text)
        self.assertEqual(len(matches), 1)

    def test_extract_markdown_link_only(self):
        text = "This is text with a ![first is image](https://i.imgur.com/aKaOqIh.gif) and [second is link](https://.example.com)"
        matches = extract_markdown_links(text)
        self.assertEqual(len(matches), 1)

    if __name__ == "__main__":
        unittest.main()
