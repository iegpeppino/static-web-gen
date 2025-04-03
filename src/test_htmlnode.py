import unittest

from htmlnode import HTMLNode, ParentNode, LeafNode


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

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        
    def test_leaf_to_html_with_props(self):
        node = LeafNode("p", "Hello, world!", {"href":"https://www.google.com"})
        self.assertEqual(node.to_html(), '<p href="https://www.google.com" >Hello, world!</p>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    # def test_none_url(self):
    #     node = HTMLNode()
    #     node2 = HTMLNode()
    #     self.assertEqual(node, node2)
    

if __name__ == "__main__":
    unittest.main()