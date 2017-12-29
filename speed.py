from Tests.calculate_time import calculate_time
from PrettyParser import PrettyParser

markup = """
    <body>
        <div>
            <a>Hello</a>
            <p>This is a <strong>very</strong> simple HTML document</p>
            <p>It only has two paragraphs</p>
        </div>
    </body>
    """


def test_parse():
    p = PrettyParser()
    print(p.feed(markup))


time = 0
range_loops = 10
for i in range(range_loops):
    time += calculate_time(test_parse)

time /= range_loops
with open('speed.txt', 'a') as f:
    f.write(str(time) + "\n")
