import unittest
from blocks import block_to_blocktype, markdown_to_blocks, BlockType


class Test_markdown_to_blocks(unittest.TestCase):
    def test_split(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_split_with_blanks(self):
        md = """


    This is **bolded** paragraph


    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line


    - This is a list
    - with items



    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


class Test_BlockTypes(unittest.TestCase):
    def test_is_paragraph_multiline(self):
        self.assertEqual(
            block_to_blocktype("\none\ntwo\nthree\nfour  "), BlockType.PARAGRAPH
        )

    def test_is_paragraph(self):
        self.assertEqual(block_to_blocktype("foobar  "), BlockType.PARAGRAPH)
        self.assertEqual(block_to_blocktype("1foobar  "), BlockType.PARAGRAPH)
        self.assertEqual(block_to_blocktype("?foobar  "), BlockType.PARAGRAPH)
        self.assertEqual(block_to_blocktype("foobar  "), BlockType.PARAGRAPH)
        self.assertEqual(block_to_blocktype("foobar  "), BlockType.PARAGRAPH)
        self.assertEqual(block_to_blocktype("foobar  "), BlockType.PARAGRAPH)

    def test_is_heading(self):
        self.assertEqual(block_to_blocktype("# foobar  "), BlockType.HEADING)
        self.assertEqual(block_to_blocktype("## foobar  "), BlockType.HEADING)
        self.assertEqual(block_to_blocktype("### foobar  "), BlockType.HEADING)
        self.assertEqual(block_to_blocktype("#### foobar  "), BlockType.HEADING)
        self.assertEqual(block_to_blocktype("##### foobar  "), BlockType.HEADING)
        self.assertEqual(block_to_blocktype("###### foobar  "), BlockType.HEADING)

    def test_is_code(self):
        self.assertEqual(
            block_to_blocktype("```foobar is codebar\ncodebar is foobar```"),
            BlockType.CODE,
        )

    def test_is_quote(self):
        self.assertEqual(
            block_to_blocktype("> quotebar is quote bam   "), BlockType.QUOTE
        )

    def test_is_unordered_list(self):
        self.assertEqual(
            block_to_blocktype("- list bar\n- is listbam\n- so foo ya"),
            BlockType.UNORDERED_LIST,
        )

    def test_is_bad_unordered_list(self):
        self.assertEqual(
            block_to_blocktype("- list bar\n- is listbam\n- so foo ya\n1. asdfasdf"),
            BlockType.PARAGRAPH,
        )

    def test_is_ordered_list(self):
        self.assertEqual(
            block_to_blocktype("1. list bar is\n2. listbam\n3. fooooooooon   "),
            BlockType.ORDERED_LIST,
        )


if __name__ == "__main__":
    unittest.main()
