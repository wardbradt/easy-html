from Tag import Tag
from PrettyParser import PrettyParser


class PrettyBowl(Tag):

    def __init__(self, data):
        parsed_tags = PrettyParser().feed(data)
        # self = parsed_tags
        # Tag.__init__(self, 'document_root')

    def __str__(self):
        return self.decode_contents()


markup = """
    <body>
        <div>
            <a>Hello</a>
            <p>This is a <strong>very</strong> simple HTML document</p>
            <p>It only has two paragraphs</p>
        </div>
    </body>
    """

# b = PrettyBowl(markup)

p = PrettyParser()
bowl = p.feed(markup)

for i in bowl:
    print(i)
    print("\n")
# print(bowl)
