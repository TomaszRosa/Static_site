import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = HTMLNode("p", "test", [], {"id": "main", "class": "container"})
        node2 = HTMLNode("p", "test", [], {"id": "main", "class": "container"})
        self.assertEqual(node, node2)

    def test_props_to_html(self):
        node = HTMLNode("p", "test", [], {"href": "example.com", "title": "Example"})
        example1 = ' href="example.com" title="Example"'
        example2 = ' title="Example" href="example.com"'
        self.assertIn(node.props_to_html(), [example1, example2])
    
    def test_none(self):
        node = HTMLNode("p", "test", [], {})
        node2 = HTMLNode("p", "test", [], {"href": "example.com", "title": "Example"})
        self.assertNotEqual(node, node2)

    def test_props_to_html_none(self):
        node = HTMLNode("p", "test", [], None)
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty_dict(self):
        node = HTMLNode("p", "test", [], {})
        self.assertEqual(node.props_to_html(), "")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_no_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_no_value(self):
        node = LeafNode("p", "", {})
        with self.assertRaises(ValueError):
            node.to_html()
        
    def test_no_tag(self):
        node = LeafNode("", "test", {})
        self.assertEqual(node.to_html(), "test")

    def test_whitespace(self):
        node = LeafNode(" ", "test", {})
        self.assertEqual(node.to_html(), "test")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")



if __name__ == "__main__":
    unittest.main()