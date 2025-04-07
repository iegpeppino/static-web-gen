import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from inline_converter import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_images

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
    
    # TESTING MARKDOWN IMAGE AND LINK EXTRACTORS 

    def test_ext_markdown_img(self):
        text = "![alt_text](https://www.google.com)"
        self.assertEqual(extract_markdown_images(text), [("alt_text", "https://www.google.com")])
    
    def test_ext_full_sentence_markdown_img(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        self.assertEqual(extract_markdown_images(text), [("image", "https://i.imgur.com/zjjcJKZ.png")])

    # Multiple image links in text
    def test_ext_multiple_links(self):
        text = "Cute puppy img : ![doggy](https://cutedogpic.com) and cool guitar img : ![guitar](https://coolguitar.com)"
        self.assertEqual(extract_markdown_images(text), [("doggy", "https://cutedogpic.com"), ("guitar", "https://coolguitar.com")])

    # Input is a regular link and not an img link
    def test_ext_mkdown_imgurl_from_link(self):
        text = "[to google](https://www.google.com)"
        self.assertNotEqual(extract_markdown_images(text), [("to google", "https://www.google.com")])

    # Both a image link and regular link are present in the text
    def test_ext_mkdown_img_diff_links(self):
        text = "link to web [webpage](https://12lkasmfa.com) and link to img ![image](https://i.imgur.com/zjjcJKZ.png)"
        self.assertEqual(extract_markdown_images(text), [("image", "https://i.imgur.com/zjjcJKZ.png")])

    def test_ext_markdown_link(self):
        text = "[to google](https://www.google.com)"
        self.assertEqual(extract_markdown_links(text), [("to google", "https://www.google.com")])
    
    def test_ext_full_sentence_markdown_link(self):
        text = "This link points to google's webpage: [to google](https://www.google.com)"
        self.assertEqual(extract_markdown_links(text), [("to google", "https://www.google.com")])
    
    # Text has multiple links
    def test_ext_multiple_markdown_links(self):
        text = "This link points to google [google](https://google.com) this other one poinst to nurgle [nurgle](https://www.nurgle.com)"
        self.assertEqual(extract_markdown_links(text), [("google","https://google.com"), ("nurgle","https://www.nurgle.com")])

    # Gives an img url instead of a regular link as input
    def test_ext_mkdown_link_with_img(self):
        text = "![alt_text](https://www.google.com)"
        self.assertNotEqual(extract_markdown_links(text), [("to google", "https://www.google.com")])

    # Both a image link and regular link are present in the text
    def test_ext_mkdown_link_diff_links(self):
        text = "link to web [webpage](https://12lkasmfa.com) and link to img ![image](https://i.imgur.com/zjjcJKZ.png)"
        self.assertEqual(extract_markdown_links(text), [("webpage", "https://12lkasmfa.com")])

    def test_split_node_img(self):
        node = TextNode("This textnode contains an image ![image_alt](https://image.url)", TextType.TEXT)
        self.assertEqual(
            split_nodes_images([node]),
            [TextNode("This textnode contains an image ", TextType.TEXT),
            TextNode("image_alt", TextType.IMG, "https://image.url"),]
            )

if __name__ == "__main__":
    unittest.main()