import unittest

from html import markdown_to_html_node


class MarkdownToHtmlTest(unittest.TestCase):
    # @unittest.skip("")
    def test_ol(self):
        md = """

        1. one
        2. two **bolded** twize
        3. three
        4. four yo
        5. five foo

        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>one</li><li>two <b>bolded</b> twize</li><li>three</li><li>four yo</li><li>five foo</li></ol></div>",
        )

    # @unittest.skip("")
    def test_ul(self):
        md = """

        - one
        - two **bolded** twize
        - three
        - four yo
        - five foo

        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>one</li><li>two <b>bolded</b> twize</li><li>three</li><li>four yo</li><li>five foo</li></ul></div>",
        )

    # @unittest.skip("")
    def test_paragraph_multiline(self):
        md = """
        This is **bolded** paragraph
        text in a p
        tag here
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph\ntext in a p\ntag here</p></div>",
        )

    # @unittest.skip("")
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph\ntext in a p\ntag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    # @unittest.skip("fo")
    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


if __name__ == "__main__":
    unittest.main()
