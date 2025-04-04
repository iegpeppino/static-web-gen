import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from inline_converter import split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://url")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://url")
        self.assertEqual(node, node2)
    
    def test_not_eq(self):
        node = TextNode("This is the first node", TextType.BOLD, "https://url1")
        node2 = TextNode("Something else", TextType.CODE, "https://url2")
        self.assertNotEqual(node, node2)
    
    def test_min_diff(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://url")
        node2 = TextNode("This is a text node2", TextType.BOLD, "https://url")
        self.assertNotEqual(node, node2)

    def test_none_url(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node, node2)
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        
if __name__ == "__main__":
    unittest.main()