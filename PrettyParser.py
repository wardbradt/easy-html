from html.parser import HTMLParser
from Tag import Tag
from NavigableString import NavigableString
from collections import deque


def _get_attrs_dict(attrs):
    # handle the formatting of attrs
    attrs_dict = {}
    for i in attrs:
        # if i == ('class', 'foo bar'), attrs_dict['class'] = ['foo', 'bar']
        attrs_dict[i[0]] = i[1].split()
    return attrs_dict


class PrettyParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.iterating_deque = deque()
        self.iterating_deque.append(Tag('document_root'))
        # how many nested pre/ textarea tags deep the feed is
        self.whitespace_count = 0

    def reset(self):
        """Reset this instance.  Loses all unprocessed data."""
        super().reset()
        self.iterating_deque = deque()
        self.iterating_deque.append(Tag('document_root'))

    def handle_starttag(self, tag, attrs):
        if tag in {'pre', 'textarea'}:
            self.whitespace_count += 1

        attrs_dict = _get_attrs_dict(attrs)

        new_tag = Tag(tag, attrs_dict)
        new_tag.parent = self.iterating_deque[-1]

        self.iterating_deque.append(new_tag)

    def handle_endtag(self, tag):
        if tag in {'pre', 'textarea'}:
            self.whitespace_count -= 1

        # contents is equal to the elements at the beginning whose parent is self.iterating_deque[-1]

        # the tag we instantiated when parsing this endtag's corresponding starttag
        popped_tag_to_be_closed = self.iterating_deque[-1]

        while self.iterating_deque[0].parent is popped_tag_to_be_closed:
            popped_tag_to_be_closed.contents.insert(0, self.iterating_deque.popleft())

        # if the first element in self.iterating_deque is the previous sibling of popped_tag_to_be_closed
        if self.iterating_deque[0].parent is popped_tag_to_be_closed.parent \
                and self.iterating_deque[0] is not popped_tag_to_be_closed:
            self.iterating_deque[0].next_sibling = popped_tag_to_be_closed
            popped_tag_to_be_closed.previous_sibling = self.iterating_deque[0]

        self.iterating_deque.pop()

        self.iterating_deque.appendleft(popped_tag_to_be_closed)

    def handle_data(self, data):
        # if this string is not the child of a pre or textarea tag
        if self.whitespace_count == 0:
            data = data.strip()
            # todo: faster way to do this? is len(stripped_data) calculated or does python optimize it?
            if len(data) == 0:
                return
        new_string = NavigableString(data)
        new_string.parent = self.iterating_deque[-1]
        if self.iterating_deque[0].parent is new_string.parent:
            self.iterating_deque[0].next_sibling = new_string
            new_string.previous_sibling = self.iterating_deque[0]

        self.iterating_deque.appendleft(new_string)

    def handle_startendtag(self, tag, attrs):
        attrs_dict = _get_attrs_dict(attrs)

        new_tag = Tag(tag, attrs_dict)
        new_tag.parent = self.iterating_deque[-1]
        
        if self.iterating_deque[0].parent is new_tag.parent:
            self.iterating_deque[0].next_sibling = new_tag
            new_tag.previous_sibling = self.iterating_deque[0]

        self.iterating_deque.appendleft(new_tag)

    def feed(self, data):
        super().feed(data + "\n</document_root>")
        return self.iterating_deque.pop()

    def error(self, message):
        pass
