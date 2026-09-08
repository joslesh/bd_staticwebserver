from htmlnode import HTMLNode, LeafNode
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
        
