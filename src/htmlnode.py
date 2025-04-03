class HTMLNode():
    def __init__(self, tag, value, children, props):
        self.tag = tag if tag else None
        self.value = value if value else None
        self.children = children if children else None
        self.props = props if props else None

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        props_str = ""
        if self.props is not None:
            for prop in self.props.items():
                props_str += f'{prop[0]}="{prop[1]}" '
        return props_str

    def __repr__(self):
        return (f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})")

    def __eq__(self, OtherNode):
        if (self.tag == OtherNode.tag
            and self.value == OtherNode.value
            and self.children == OtherNode.children
            and self.props == OtherNode.props):
            return True
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        self.tag = tag              # tag and children args are not optional
        self.children = children

    def to_html(self):
        if not self.tag:
            raise ValueError("tag is missing")
        elif not self.children:
            raise ValueError("must define children")
        elif self.props:
            return f"<{self.tag} {self.props_to_html()}>{"".join(map(lambda x: x.to_html(), self.children))}</{self.tag}>"
            #return f"<{self.tag} {self.props_to_html()}>{map(self.to_html(),self.children).join()}</{self.tag}>"
        else:
            return f"<{self.tag}>{"".join(map(lambda x: x.to_html(), self.children))}</{self.tag}>"
            #return f"<{self.tag}>{map(self.to_html(),self.children).join()}</{self.tag}>"

class LeafNode(HTMLNode):
    def  __init__(self, tag, value, props=None):                 # There can be no children in Leaf so I pass "None"          
        super().__init__(tag, value, None ,props)           # to the super constructor on the children arg     

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        elif self.tag is None:
            return f"{self.value}"
        elif self.props is None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return (f"LeafNode({self.tag}, {self.value}, {self.props})")   