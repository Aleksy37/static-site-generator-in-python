import unittest
from inline_markdown import split_nodes_delimiter
from textnode import TextNode, TextType

class TestSplitDelimiter(unittest.TestCase):
    def test_single_bold(self):
       old_nodes = [TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)]
       result = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
       expected = [
                    TextNode("This is text with a ", TextType.TEXT),
                    TextNode("bolded phrase", TextType.BOLD),
                    TextNode(" in the middle", TextType.TEXT),
                    ]
       self.assertEqual(result, expected)
    
    def test_double_bold(self):
       old_nodes = [TextNode("This is **text** with two **bolded phrase** in the middle", TextType.TEXT)]
       result = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
       expected = [
                    TextNode("This is ", TextType.TEXT),
                    TextNode("text", TextType.BOLD),
                    TextNode(" with two ", TextType.TEXT),
                    TextNode("bolded phrase", TextType.BOLD),
                    TextNode(" in the middle", TextType.TEXT),
                    ]
       self.assertEqual(result, expected)

    def test_single_italic(self):
        old_nodes = [TextNode("This is text with an _italic phrase_ in the middle", TextType.TEXT)]
        result = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
        expected = [
                    TextNode("This is text with an ", TextType.TEXT),
                    TextNode("italic phrase", TextType.ITALIC),
                    TextNode(" in the middle", TextType.TEXT),
                    ]
        self.assertEqual(result, expected)
    
    def test_double_italics(self):
       old_nodes = [TextNode("This is _text_ with two _bolded phrase_ in the middle", TextType.TEXT)]
       result = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
       expected = [
                    TextNode("This is ", TextType.TEXT),
                    TextNode("text", TextType.ITALIC),
                    TextNode(" with two ", TextType.TEXT),
                    TextNode("bolded phrase", TextType.ITALIC),
                    TextNode(" in the middle", TextType.TEXT),
                    ]
       self.assertEqual(result, expected)

    def test_single_code(self):
       old_nodes = [TextNode("This is text with a `code phrase` in the middle", TextType.TEXT)]
       result = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
       expected = [
                    TextNode("This is text with a ", TextType.TEXT),
                    TextNode("code phrase", TextType.CODE),
                    TextNode(" in the middle", TextType.TEXT),
                    ]
       self.assertEqual(result, expected)
    
    def test_double_code(self):
       old_nodes = [TextNode("This is `text` with two `code phrase` in the middle", TextType.TEXT)]
       result = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
       expected = [
                    TextNode("This is ", TextType.TEXT),
                    TextNode("text", TextType.CODE),
                    TextNode(" with two ", TextType.TEXT),
                    TextNode("code phrase", TextType.CODE),
                    TextNode(" in the middle", TextType.TEXT),
                    ]
       self.assertEqual(result, expected)
    
    def test_missing_closure(self):
        old_nodes = [TextNode("This is text with a **missing closure in the middle", TextType.TEXT)]
        with self.assertRaises(ValueError) as cm:
            split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertIn("invalid markdown, formatted section not closed", str(cm.exception))

    def test_input_not_type_text(self):
       old_nodes = [TextNode("This is text with a **bolded phrase** in the middle", TextType.CODE)]
       result = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
       expected = [TextNode("This is text with a **bolded phrase** in the middle", TextType.CODE)]
       self.assertEqual(result, expected)
    
    def test_input_contains_no_delimiter(self):
       old_nodes = [TextNode("This is text with a bolded phrase in the middle", TextType.TEXT)]
       result = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
       expected = [TextNode("This is text with a bolded phrase in the middle", TextType.TEXT)]
       self.assertEqual(result, expected)
    
    def test_input_entirely_within_delimiter(self):
       old_nodes = [TextNode("**This text is a bolded phrase**", TextType.TEXT)]
       result = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
       expected = [TextNode("This text is a bolded phrase", TextType.BOLD)]
       self.assertEqual(result, expected)
        
    def test_input_has_edge_delimiters(self):
       old_nodes = [TextNode("**This** is text with a normal phrase in the **middle**", TextType.TEXT)]
       result = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
       expected = [
          TextNode("This", TextType.BOLD),
          TextNode(" is text with a normal phrase in the ", TextType.TEXT),
          TextNode("middle", TextType.BOLD)
          ]
       self.assertEqual(result, expected)