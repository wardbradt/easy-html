from ps1.easyHTML.Tag import Tag
from ps1.easyHTML.PrettyParser import PrettyParser


class PrettyBowl(Tag):

    def __init__(self, data):
        parsed_tags = PrettyParser().feed(data)
        Tag.__init__(self, 'document_root')
        self.contents = parsed_tags
        self.parent = None

    def __str__(self):
        return self.decode_contents()
