import unittest
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
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

      
   
   def test_extract_markdown_images(self):
    matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
    self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
   
   def test_extract_multiple_markdown_images(self):
    matches = extract_markdown_images(
        "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    )
    self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)
   
   def test_extract_mixed_markdown_images(self):
      matches = extract_markdown_images(
         "This is text with a link [to boot dev](https://www.boot.dev) and a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
      )
      self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif")], matches)

   def test_extract_markdown_links(self):
      matches = extract_markdown_links(
         "This is text with a link [to boot dev](https://www.boot.dev)"
      )
      self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)
   
   def test_extract_multiple_markdown_links(self):
      matches = extract_markdown_links(
         "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
      )
      self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)
   
   def test_extract_mixed_markdown_links(self):
      matches = extract_markdown_links(
         "This is text with a link [to boot dev](https://www.boot.dev) and a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
      )
      self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)
   
   def test_extract_markdown_images_rejects_brackets(self):
    matches = extract_markdown_images(
        "This is text with an ![[image]]((https://i.imgur.com/zjjcJKZ.png))"
    )
    self.assertListEqual([], matches)

   def test_extract_markdown_links_rejects_brackets(self):
      matches = extract_markdown_links(
         "This is text with a link [to []boot dev](https://www.boot.()dev)"
      )
      self.assertListEqual([], matches)

   def test_extract_markdown_missing_link(self):
      matches = extract_markdown_links(
         "This is just text with no link"
      )
      self.assertListEqual([], matches)

   def test_extract_markdown_missing_image(self):
      matches = extract_markdown_images(
         "This is just text with no image"
      )
      self.assertListEqual([], matches)
   
   def test_extract_markdown_just_link(self):
      matches = extract_markdown_links(
         "[alt](url)"
      )
      self.assertListEqual([("alt", "url")], matches)

   def test_extract_markdown_just_images(self):
      matches = extract_markdown_images(
         "![alt](url)"
      )
      self.assertListEqual([("alt", "url")], matches)
   
   def test_extract_markdown_touching_links(self):
      matches = extract_markdown_links(
         "[a](url1)[b](url2)"
      )
      self.assertListEqual([("a", "url1"), ("b", "url2")], matches)

   def test_extract_markdown_touching_images(self):
      matches = extract_markdown_images(
         "![a](url1)![b](url2)"
      )
      self.assertListEqual([("a", "url1"), ("b", "url2")], matches)

   def test_extract_markdown_whitespace_images(self):
      matches = extract_markdown_images(
         "![ alt text ]( https://example.com )"
      )
      self.assertListEqual([(" alt text ", " https://example.com ")], matches)
   
   def test_extract_markdown_whitespace_links(self):
      matches = extract_markdown_links(
         "[ alt text ]( https://example.com )"
      )
      self.assertListEqual([(" alt text ", " https://example.com ")], matches)



   def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes
        )

   def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes
        )

   def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes
        )
   
   def test_split_no_image(self):
      node = TextNode(
         "This is just a text node with no image", TextType.TEXT
      )
      new_nodes = split_nodes_image([node])
      self.assertListEqual(
         [
            TextNode("This is just a text node with no image", TextType.TEXT)
         ],
         new_nodes
      )
   
   def test_split_image_non_text_input(self):
      node = TextNode(
         "This is a **non text input node**", TextType.BOLD
      )
      new_nodes = split_nodes_image([node])
      self.assertListEqual(
         [
            TextNode("This is a **non text input node**", TextType.BOLD)
         ],
         new_nodes
      )

   def test_split_image_multiple_nodes(self):
      nodes = [
         TextNode("This is a **non text input node**", TextType.BOLD),
         TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",TextType.TEXT),
         TextNode("[link](https://boot.dev)", TextType.TEXT)
      ]
      new_nodes = split_nodes_image(nodes)
      self.assertListEqual(
         [
         TextNode("This is a **non text input node**", TextType.BOLD),
         TextNode("This is text with an ", TextType.TEXT),
         TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
         TextNode(" and another ", TextType.TEXT),
         TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
         TextNode("[link](https://boot.dev)", TextType.TEXT)
         ],
         new_nodes
      )

   def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes
        )
      
   def test_split_just_link(self):
      node = TextNode("[alt](url)", TextType.TEXT)
      new_nodes = split_nodes_link([node])
      self.assertListEqual(
         [TextNode("alt", TextType.LINK, "url")],
         new_nodes
      )

   def test_split_link_image_input(self):
      node = TextNode("![image](url)", TextType.TEXT)
      new_nodes = split_nodes_link([node])
      self.assertListEqual(
         [TextNode("![image](url)", TextType.TEXT)],
         new_nodes
      )
   
   def test_split_link_non_text_input(self):
      node = TextNode("This is a **bold** node", TextType.BOLD)
      new_nodes = split_nodes_link([node])
      self.assertListEqual(
         [TextNode("This is a **bold** node", TextType.BOLD)],
         new_nodes
      )
    
   def test_split_links_multiple_nodes(self):
      nodes = [
         TextNode("This is a **non text input node**", TextType.BOLD),
         TextNode("This is text with a [link](https://google.com) and another [second link](https://boot.dev)",TextType.TEXT),
         TextNode("![image](url)", TextType.TEXT)
      ]
      new_nodes = split_nodes_link(nodes)
      self.assertListEqual(
         [
         TextNode("This is a **non text input node**", TextType.BOLD),
         TextNode("This is text with a ", TextType.TEXT),
         TextNode("link", TextType.LINK, "https://google.com"),
         TextNode(" and another ", TextType.TEXT),
         TextNode("second link", TextType.LINK, "https://boot.dev"),
         TextNode("![image](url)", TextType.TEXT)
         ],
         new_nodes
      )
   
   def test_text_to_nodes(self):
      text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
      new_nodes = text_to_textnodes(text)
      self.assertListEqual(
         [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
         ],
         new_nodes
      )
   
   def test_text_to_nodes_plain_text(self):
      text = "Just plain text"
      new_nodes = text_to_textnodes(text)
      self.assertListEqual(
         [TextNode("Just plain text", TextType.TEXT)],
         new_nodes
      )

   def test_text_to_nodes_bold_only(self):
      text = "this is **bold** text"
      new_nodes = text_to_textnodes(text)
      self.assertListEqual(
         [
            TextNode("this is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
         ],
         new_nodes
      )

   def test_text_to_nodes_italic_only(self):
      text = "this is _italic_ text"
      new_nodes = text_to_textnodes(text)
      self.assertListEqual(
         [
            TextNode("this is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT)
         ],
         new_nodes
      )

   def test_text_to_nodes_code_only(self):
      text = "this is `code` text"
      new_nodes = text_to_textnodes(text)
      self.assertListEqual(
         [
            TextNode("this is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT)
         ],
         new_nodes
      )

   def test_text_to_nodes_image_only(self):
      text = "![alt text](https://example.com/image.png)"
      new_nodes = text_to_textnodes(text)
      self.assertListEqual(
         [TextNode("alt text", TextType.IMAGE, "https://example.com/image.png")],
         new_nodes
      )

   def test_text_to_nodes_link_only(self):
      text = "[alt text](https://example.com)"
      new_nodes = text_to_textnodes(text)
      self.assertListEqual(
         [TextNode("alt text", TextType.LINK, "https://example.com")],
         new_nodes
      )
   
   def test_text_to_nodes_back_to_back(self):
      text = "[alt text](https://example.com)`code`![alt text](https://example.com/image.png)**bold**_italics_"
      new_nodes = text_to_textnodes(text)
      self.assertListEqual(
         [
            TextNode("alt text", TextType.LINK, "https://example.com"),
            TextNode("code", TextType.CODE),
            TextNode("alt text", TextType.IMAGE, "https://example.com/image.png"),
            TextNode("bold", TextType.BOLD),
            TextNode("italics", TextType.ITALIC)
         ],
         new_nodes
      )