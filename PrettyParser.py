from html.parser import HTMLParser
from Tag import Tag
from NavigableString import NavigableString
from collections import deque


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

        new_tag = Tag(tag, attrs)
        new_tag.parent = self.iterating_deque[-1]

        self.iterating_deque.append(new_tag)

    def handle_endtag(self, tag):
        if tag in {'pre', 'textarea'}:
            self.whitespace_count -= 1

        # contents is equal to the elements at the beginning whose parent is self.iterating_deque[-1]

        # the tag we instantiated when parsing this endtag's corresponding starttag
        tag_to_be_closed = self.iterating_deque.pop()
        print(len(self.iterating_deque))
        while self.iterating_deque[0].parent is tag_to_be_closed:
            tag_to_be_closed.contents.insert(0, self.iterating_deque.popleft())

        self.iterating_deque.appendleft(tag_to_be_closed)

    def handle_data(self, data):
        # if this string is not the child of a pre or textarea tag
        if self.whitespace_count == 0:
            data = data.strip()
            # todo: faster way to do this? is len(stripped_data) calculated or does python optimize it?
            if len(data) == 0:
                return
        new_string = NavigableString(data)
        new_string.parent = self.iterating_deque[-1]

        self.iterating_deque.appendleft(new_string)

    def handle_startendtag(self, tag, attrs):
        new_tag = Tag(tag, attrs)
        new_tag.parent = self.iterating_deque[-1]

        self.iterating_deque.appendleft(new_tag)

    def feed(self, data):
        super().feed(data + "\n</document_root>")
        return self.iterating_deque[-1]

    def error(self, message):
        pass
