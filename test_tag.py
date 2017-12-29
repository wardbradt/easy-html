from unittest import TestCase
from PrettyBowl import PrettyBowl
from Tag import Tag


class TestTag(TestCase):

    def test_insert(self):
        markup = """<div><div><p>I like to eat <strong class="foo_class">apples. I</strong> am bananas. 
        <strong>T<i>h<b>i</b>s </i>is</strong> it.</p><p id='foo'>This is it. Goodbye.</p><p>Noo.</p></div></div>"""
        bowl = PrettyBowl(markup).contents[0]
        div = Tag("div")
        bowl_two = bowl
        bowl.insert(1, div)
        bowl_two.insert(1, div)
        self.assertEqual(bowl, bowl_two)

    def test_append(self):
        tag = Tag("div")
        p = Tag("p")

    def test_string_setter(self):
        p = Tag("p")
        self.assertEqual(str(p), "<p></p>")
        p.string = "Hello"
        self.assertEqual(str(p).replace("\n", ""), "<p>Hello</p>")

    def test_extract(self):
        tag = Tag("div")
        p = Tag("p")
        p.string = "Hello world"
        tag._append(p)
        p_two = Tag("p")
        p_two.string = "Hello world"
        tag._append(p_two)

        self.assertEqual(tag.contents[0], p)
        self.assertEqual(tag.contents[1], p_two)

        p_two._extract(1)

        self.assertEqual(tag.contents[0], p)
        self.assertEqual(len(tag.contents), 1)
