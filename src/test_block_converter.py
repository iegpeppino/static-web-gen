import unittest

from block_converter import markdown_to_blocks

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