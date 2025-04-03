import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        self.childnode1 = HTMLNode("I'm child1", "p", None, None)
        self.childnode2 = HTMLNode("I'm child2", "p", None, None)
        self.child_nodes = [self.childnode1, self.childnode2]
        self.prop_dict = {"href":"https://www.google.com",
             "target":"blank"}
    
    def test_eq(self):
        node = HTMLNode(value="text", tag="tag", children= self.child_nodes, props= self.prop_dict)
        node2 = HTMLNode(value="text", tag="tag", children= self.child_nodes, props= self.prop_dict)
        self.assertEqual(node, node2)
    
    def test_not_eq(self):
        node = HTMLNode(value= "text", tag= "tag", children= self.child_nodes, props= self.prop_dict)
        node2 = HTMLNode(value= "text", tag= "tag", children= None, props= None)
        self.assertNotEqual(node, node2)

    def test_min_diff(self):
        node = HTMLNode(value= "text", tag= "tag", children= self.child_nodes, props= self.prop_dict)
        node2 = HTMLNode(value= "text", tag= "tag", children= self.child_nodes , props= {"junk":"junkref"})
        self.assertNotEqual(node, node2)

    def test_props_to_html(self):
        node = HTMLNode(value= "text", tag= "tag", children= self.child_nodes, props= self.prop_dict)
        node2 = HTMLNode(value= "text", tag= "tag", children= self.child_nodes, props= self.prop_dict)
        self.assertEqual(node.props_to_html(), node2.props_to_html())

    # def test_none_url(self):
    #     node = HTMLNode()
    #     node2 = HTMLNode()
    #     self.assertEqual(node, node2)
    

if __name__ == "__main__":
    unittest.main()