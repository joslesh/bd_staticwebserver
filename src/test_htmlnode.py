from htmlnode import HTMLNode, LeafNode, ParentNode
import unittest



class TestHTMLNode(unittest.TestCase):
    def test_htmlnode_repr(self):
        test_node = HTMLNode("h", "value", None, None)
        expected = f"HTMLNode(h, value, None, None)"
        self.assertEqual(repr(test_node), expected)
        
    def test_props_to_html(self):
        test_node = HTMLNode("a", "link", None, {"href": "https://www.google.com"})
        expected = ' href="https://www.google.com"'
        self.assertEqual(test_node.props_to_html(), expected)

    def test_htmlnode_eq(self):
        test_node = HTMLNode("p", "value", None, None)
        test_node2 = HTMLNode("p", "value", None, None)
        self.assertEqual(test_node, test_node2)


class TestLeafNode(unittest.TestCase):
    def test_leafnode_repr(self):
        test_leafnode = LeafNode("p", "Paragraph!")
        expected = f'LeafNode(p, Paragraph!, None)'
        self.assertEqual(repr(test_leafnode), expected)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_with_attr(self):
        node = LeafNode("a", "Click me!", {"href":"www.google.com"})
        self.assertEqual(node.to_html(), '<a href="www.google.com">Click me!</a>')
        
class TestParentNode(unittest.TestCase):
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
        "<div><span><b>grandchild</b></span></div>")

    def test_to_html_with_multiple_children(self):
        child_node = LeafNode("span", "child1")
        child_node2 = LeafNode("b", "bolded text")
        child_node3 = LeafNode(None, "plain")
        parent_node = ParentNode("div", [child_node, child_node2, child_node3])
        self.assertEqual(parent_node.to_html(), "<div><span>child1</span><b>bolded text</b>plain</div>")

if __name__ == "__main__":
    unittest.main()
