import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from inline_converter import split_nodes_delimiter

class TestInlineConverter(unittest.TestCase):

    def test_bold_word(self):
        node = TextNode("Some text with **bolded** words", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("Some text with ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" words", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_multiple_bolded(self):
        node = TextNode("This text has **multiple** words that are **bolded**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This text has ", TextType.TEXT),
                TextNode("multiple", TextType.BOLD),
                TextNode(" words that are ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD)
            ],
            new_nodes,
        )
    
    def test_section_bolded(self):
        node = TextNode("This text contains **an entire section** that is bolded.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This text contains ", TextType.TEXT),
                TextNode("an entire section", TextType.BOLD),
                TextNode(" that is bolded.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_entire_bolded(self):
        node = TextNode("**This entire text is bolded**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This entire text is bolded", TextType.BOLD)
            ],
            new_nodes,
        )
    
    def test_italics(self):
        node = TextNode("This text has words in _italics_ but it is not _italian_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This text has words in ", TextType.TEXT),
                TextNode("italics", TextType.ITALIC),
                TextNode(" but it is not ", TextType.TEXT),
                TextNode("italian", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_code_delimiter(self):
        node = TextNode("This text has some code that could `hack the matrix`.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This text has some code that could ", TextType.TEXT),
                TextNode("hack the matrix", TextType.CODE),
                TextNode(".", TextType.TEXT),
            ],
            new_nodes,
        )
        
if __name__ == "__main__":
    unittest.main()