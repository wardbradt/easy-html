from html.parser import HTMLParser
from Tag import Tag
from NavigableString import NavigableString
from collections import deque


class OpeningTag:
    def __init__(self, tag_name, attributes):
        self.tag_name = tag_name
        self.attributes = attributes

    def __str__(self):
        attribute_string = ""
        for i in self.attributes:
            attribute_string += " " + i[0] + '=' + i[1]
        return '<%s%s>' % (self.tag_name, attribute_string)


class PrettyParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.iterating_deque = deque()
        self.depth_level_iterator = 0
        # how many nested pre/ textarea tags deep the feed is
        self.whitespace_count = 0

    def reset(self):
        """Reset this instance.  Loses all unprocessed data."""
        super().reset()
        self.iterating_deque = deque()

    def handle_starttag(self, tag, attrs):
        if tag in {'pre', 'textarea'}:
            self.whitespace_count += 1

        self.iterating_deque.append((OpeningTag(tag, attrs), self.depth_level_iterator))
        self.depth_level_iterator += 1

    def handle_endtag(self, tag):
        if tag in {'pre', 'textarea'}:
            self.whitespace_count -= 1

        self.depth_level_iterator -= 1
        # popped_pretty_tag = the opening tag at the leftmost index of self.iterating_deque
        popped_pretty_tag = self.iterating_deque[-1][0]
        new_tag = Tag(popped_pretty_tag.tag_name, popped_pretty_tag.attributes)
        # avoids edge case where, when handling the last tag, typically '</body>,' self.iterating_deque is empty by
        # popping after this while loop
        while self.iterating_deque[0][1] > self.depth_level_iterator:
            new_tag.insert(0, self.iterating_deque.popleft()[0])
        self.iterating_deque.pop()

        self.iterating_deque.appendleft((new_tag, self.depth_level_iterator))

    def handle_data(self, data):
        if self.whitespace_count == 0:
            stripped_data = data.strip()
            if len(stripped_data) == 0:
                return
            self.iterating_deque.appendleft((NavigableString(stripped_data), self.depth_level_iterator))
        else:
            self.iterating_deque.appendleft((NavigableString(data), self.depth_level_iterator))

    def handle_startendtag(self, tag, attrs):
        self.iterating_deque.appendleft((Tag(tag, attrs)))

    def feed(self, data):
        super().feed(data)
        result_list = []
        for i in self.iterating_deque:
            result_list.insert(0, i[0])
        return result_list

    def error(self, message):
        pass
