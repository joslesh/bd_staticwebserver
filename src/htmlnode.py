

class HTMLNode():
    def __init__(self, tag= None, value= None, children= None, props= None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def __eq__(self, other) -> bool:
        tag_bool = self.tag == other.tag
        value_bool = self.value == other.value
        children_bool = self.children == other.children
        props_bool = self.props == other.props
        return tag_bool and value_bool and children_bool and props_bool

    def to_html(self):
        raise Exception(NotImplementedError)

    def props_to_html(self) -> str | None:
        if self.props == None:
            return None
        result_string = ""
        for name, prop in self.props.items():
            result_string += f' {name}="{prop}"'
        return result_string

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props= None) -> None:
        super().__init__(tag, value, None, props)
        
    def to_html(self) -> str:
        if self.tag == None:
            return self.value
        if self.props == None:
            return f'<{self.tag}>{self.value}</{self.tag}>'
        else:
            return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

    def __repr__(self) -> str:
        return f'LeafNode({self.tag}, {self.value}, {self.props})'

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("Missing HTML tag")
        elif self.children is None:
            raise ValueError("No children in parent node")
        else:
            html_string = f"<{self.tag}>"
            for node in self.children:
                html_string += node.to_html()
            html_string += f"</{self.tag}>"
            return html_string
