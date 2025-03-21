import unittest
from textnode import TextType, TextNode
from parsing import split_nodes_image, split_nodes_link


class Test_SplitImagesAndLinks(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image",
                    TextType.IMAGE,
                    "https://i.imgur.com/3elNhQu.png",
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [first link](https://example.com/first) and another [second link](https://example.com/second)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("first link", TextType.LINK, "https://example.com/first"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://example.com/second"),
            ],
            new_nodes,
        )

    def test_split_only_one_link(self):
        node = TextNode(
            "This is text with an ![image alt](https://example.com/image.png) and another [anchor tag](https://example.com/anchor)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode(
                    "This is text with an ![image alt](https://example.com/image.png) and another ",
                    TextType.TEXT,
                ),
                TextNode("anchor tag", TextType.LINK, "https://example.com/anchor"),
            ],
            new_nodes,
        )

    def test_split_only_one_image(self):
        node = TextNode(
            "This is text with an ![image alt](https://example.com/image.png) and another [anchor tag](https://example.com/anchor)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode(
                    "This is text with an ",
                    TextType.TEXT,
                ),
                TextNode("image alt", TextType.IMAGE, "https://example.com/image.png"),
                TextNode(
                    " and another [anchor tag](https://example.com/anchor)",
                    TextType.TEXT,
                ),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
