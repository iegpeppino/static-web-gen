from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode

def main():
    node1 = TextNode("thisistext", "bold", "httpsblablabla")
    print(node1) 

if __name__ == "__main__":
    main()
