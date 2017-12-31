from Tag import Tag
from PrettyParser import PrettyParser


class PrettyBowl(Tag):

    def __init__(self, data):
        parsed_tags = PrettyParser().feed(data)
        Tag.__init__(self, 'document_root', None, parsed_tags.contents)

    def __str__(self):
        return self.decode_contents()
