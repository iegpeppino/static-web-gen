import unittest
from src.block_converter import BlockType, markdown_to_blocks, block_to_blocktype, markdown_to_html_node

class TestBlockConverter(unittest.TestCase):

    def test_mkdown_to_blocks(self):
        markdown = """
            This is **bolded** paragraph

            This is another paragraph with _italic_ text and `code` here
            This is the same paragraph on a new line

            - This is a list
            - with items
            """
        md = markdown_to_blocks(markdown)
        block = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items"
        ]
        self.assertEqual(md, block)

    def test_mkdown_to_blocks(self):
        text = """
            Hello, I'm testing this function
            I would like to include an image: ![alt_text](img_url)        

            
            - But that Would be too much of a _hassle_
            - Not unlike this project...

            """
        md = markdown_to_blocks(text)
        block = [
            "Hello, I'm testing this function\nI would like to include an image: ![alt_text](img_url)",
            "- But that Would be too much of a _hassle_\n- Not unlike this project..."
        ]
        self.assertEqual(md, block)
    
    def test_btb_heading(self):
        type_1 = block_to_blocktype("# Heading 1")
        type_2 = block_to_blocktype("## Heading 2")
        type_3 = block_to_blocktype("#### Heading 3")
        type_4 = block_to_blocktype("###### Heading 6")
        self.assertEqual([type_1, type_2, type_3, type_4],
                          [BlockType.HEADING,
                            BlockType.HEADING, 
                            BlockType.HEADING, 
                            BlockType.HEADING]
                            )
    
    def test_btb_code(self):
        code_type = block_to_blocktype("""```
                                   
                                   This is a block
                                   a code block```""")
        self.assertEqual(code_type, BlockType.CODE)
    
    def test_btb_quote(self):
        quote_type = block_to_blocktype(">You are very Cool - Albert Einstein")
        self.assertEqual(quote_type, BlockType.QUOTE)
    
    def test_btb_ol(self):
        ol_type = block_to_blocktype("1. First item\n2. Second Item\n3. Third Item")
        self.assertEqual(ol_type, BlockType.ORDERED_LIST)
    
    def test_btb_ul(self):
        ul_type = block_to_blocktype("- Third\n- First\n- No I was first")
        self.assertEqual(ul_type, BlockType.UNORDERED_LIST)
    
    def test_btb_mixed(self):
        mixed_type = block_to_blocktype("- something\nIn the way she moves\n1. Atracts me like\n>No other lover```")
        self.assertEqual(mixed_type, BlockType.PARAGRAPH)

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
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

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
        
