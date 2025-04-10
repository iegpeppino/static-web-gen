import re
from enum import Enum
from .textnode import TextNode, TextType, text_node_to_html_node
from .htmlnode import HTMLNode, ParentNode, LeafNode
from .inline_converter import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    """Splits markdown text to blocks disregarding any empty lines"""
    no_ws = markdown.strip()
    sentences = no_ws.split("\n\n")
    for i in range(len(sentences)):
        if sentences[i] == "":
            sentences.pop(i)
        else: 
            sentences[i] = sentences[i].strip()
            sentences[i] = re.sub(r'\n\s+', '\n', sentences[i]) # Replaces line breaks followed by whitespace with just a line break character
    return sentences


def block_to_blocktype(block):
    """Using regex to find if the blocks start
    with a markdown element and return their
    respective BlockType. If if doesn't match any of the cases 
    it is identified as a Paragraph type of block
    """
    lines = block.split("\n")
    if re.search(r'^#{1,6}\s', block):
        return BlockType.HEADING
    if re.search(r'^```[\s\S]*```$', block):
        return BlockType.CODE
    if re.search(r'^>{1}', block):
        for line in lines:
            if not re.search(r"^>", line):
                return BlockType.PARAGRAPH
        return  BlockType.QUOTE
    if re.search(r'^-\s', block):
        for line in lines:
            if not re.search(r'^-\s', line):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if re.search(r'^1\.\s', block):
        for line in lines:
            if not re.search(r'^\d+\.\s', line):
                return BlockType.PARAGRAPH
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    """This function separetes the markdown text into blocks
    then uses the helper function block_to_html_node
    to identify the type of block and create appropriately
    taged children from these blocks and finally
    enclose them into a div tag through a ParentNode object
    """
    blocks =  markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)



def block_to_html_node(block):
    """Helper function to return block's type
    through the previously declared function
    block_to_blocktype. Then it matches the block_type
    with a function that creates a ParentNode with the 
    necessary tag and children for the block
    """
    block_type = block_to_blocktype(block)
    match(block_type):
        case(BlockType.HEADING):
            return h_to_htmlnode(block)
        case(BlockType.CODE):
            return code_to_htmlnode(block)
        case(BlockType.QUOTE):
            return quote_to_htmlnode(block)
        case(BlockType.ORDERED_LIST):
            return ol_to_htmlnode(block)
        case(BlockType.UNORDERED_LIST):
            return ul_to_htmlnode(block)
        case(BlockType.PARAGRAPH):
            return p_to_htmlnode(block)
        case _:
            raise ValueError('unidentified block type')




def text_to_children(text):
    """ This helper function creates a list of children
    using the text_to_text node to first create nodes
    based on text modifiers such as bold or italic and
    then iterates over each node and converts it into 
    a html_node using the text_node_to_html_node function
    """
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children

def h_to_htmlnode(block):
    h_size = 0
    for char in block[:6]:  # Check how many "#" the heading has
        if char == "#":     # and assings the h# size for the tag
            h_size +=1
        else:
            break
    text = block[h_size + 1:] # Separates text from heading mark
    children = text_to_children(text)
    return ParentNode(f"h{h_size}", children= children)

def code_to_htmlnode(block):
    text = re.search(r'(?<=^```\s)([\s\S]*?)(?=```$)', block).group() # Regex to exclude the backticks and starting newlines
    inner_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(inner_text_node)
    code_node = ParentNode("code", children= [child])
    return ParentNode("pre", children= [code_node])

def quote_to_htmlnode(block):
    sentences = block.split("\n")
    quote_lines = []
    for sentence in sentences:
        if re.match(r'^(?!>).*', sentence): # If the sentence doesn't start 
            raise ValueError("invalid quote block")
        quote_lines.append(sentence.lstrip(">").strip())
    quote_block = " ".join(quote_lines)
    children = text_to_children(quote_block)
    return ParentNode("blockquote", children= children)

def ol_to_htmlnode(block):
    items = block.split("\n")
    list_items = []             # Each list item goes into this py list
    for item in items:          # Then it is added as a children
        list_text = item[3:]    # to a "ol" parent node
        children = text_to_children(list_text)
        list_items.append(ParentNode(tag="li", children= children))
    return ParentNode(tag="ol", children=list_items)

def ul_to_htmlnode(block):
    items = block.split("\n")
    list_items = []             
    for item in items:
        list_text = item[2:]
        children = text_to_children(list_text)
        list_items.append(ParentNode(tag="li", children= children))
    return ParentNode(tag="ul", children=list_items)

def p_to_htmlnode(block):
    sentences = block.split("\n")    
    p_block = " ".join(sentences)
    children = text_to_children(p_block)
    return ParentNode("p", children= children)

def extract_title(markdown):
    """Extracts the first H1 present in the markdown text"""
    title = re.search(r'^#{1}\s+.*$', markdown, re.MULTILINE) #return only matches at beggining of line
    if title:
        return title.group()
    else:
        raise Exception("No h1 heading found")
