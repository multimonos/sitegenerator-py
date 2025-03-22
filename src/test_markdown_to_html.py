from inspect import markcoroutinefunction
import unittest
from parameterized import parameterized
from html import markdown_to_html_node

from constants import RENDER_BLOCKQUOTE_WITH_INNER_HTML


class MarkdownToHtmlTest(unittest.TestCase):
    @parameterized.expand(
        [
            (1),
            (2),
            (3),
            (4),
            (5),
            (6),
        ]
    )
    def test_headings(self, n: int):
        prefix = "#" * n
        md = f"\n\n\n{prefix} level {n} **lorem** ipsum\n\n"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, f"<div><h{n}>level {n} <b>lorem</b> ipsum</h{n}></div>")

    def test_blockquote(self):
        md = """
> "I am in fact a **Hobbit** in all but size."
>
> -- J.R.R. Tolkien
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        if RENDER_BLOCKQUOTE_WITH_INNER_HTML:
            self.assertEqual(
                html,
                '<div><blockquote><p>"I am in fact a <b>Hobbit</b> in all but size."</p><p>-- J.R.R. Tolkien</p></blockquote></div>',
            )
        else:
            self.assertEqual(
                html,
                '<div><blockquote>"I am in fact a <b>Hobbit</b> in all but size."\n-- J.R.R. Tolkien</blockquote></div>',
            )

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

    # @unittest.skip("")
    def test_glorfindel_bold(self):
        md = """
        In J.R.R. Tolkien's legendarium, characterized by its rich tapestry of noble heroes and epic deeds, two Elven luminaries stand out: **Glorfindel**, the stalwart warrior returned from the Halls of Mandos, and **Legolas**, the prince of the Woodland Realm. While both possess grace and valor beyond mortal ken, it is Glorfindel who emerges as the more compelling figure, a beacon of heroism whose legacy spans ages.
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>In J.R.R. Tolkien's legendarium, characterized by its rich tapestry of noble heroes and epic deeds, two Elven luminaries stand out: <b>Glorfindel</b>, the stalwart warrior returned from the Halls of Mandos, and <b>Legolas</b>, the prince of the Woodland Realm. While both possess grace and valor beyond mortal ken, it is Glorfindel who emerges as the more compelling figure, a beacon of heroism whose legacy spans ages.</p></div>",
        )


if __name__ == "__main__":
    unittest.main()
