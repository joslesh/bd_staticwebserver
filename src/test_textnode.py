import unittest
from textnode import TextNode, TextType



class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_none_case(self):
        node = TextNode("This is a node with a url", TextType.LINK, "www.google.com")
        node2 = TextNode("This is a node with a url", TextType.LINK, "www.google.com")
        self.assertEqual(node, node2)

    def text_none_case_noteq(self):
        node = TextNode("This is a node with a url", TextType.LINK, "www.google.com")
        node2 = TextNode("This is a node without a url", TextType.PLAIN)
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
