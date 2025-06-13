

class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("In future")

    def props_to_html(self):
        if isinstance(self.props, dict):
            props_list = []
            for prop in self.props:
                props_list.append(f' {prop}="{self.props[prop]}"')
            return "".join(props_list)
        else:
            return ""
        
    def __eq__(self, other):
        if (self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props):
            return True
        else:
            return False
        
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props=props)

    def to_html(self):
        if self.tag == "img":
            return f'<img{self.props_to_html()} />'
        elif self.value == "" or self.value == None:
            raise ValueError("All leaf nodes must have a value")
        elif self.tag == None or str(self.tag).strip() == "":
            return self.value
        else:
            return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("invalid HTML: no tag")
        if self.children is None:
            raise ValueError("invalid HTML: no children")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"