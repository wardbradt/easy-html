from bs4 import BeautifulSoup
import time
from PrettyBowl import PrettyBowl

markup = """
<body>
    <div>
        <a>Hello</a>
        <p>This is a <strong>very</strong> simple HTML document</p>
        <p>It only has two paragraphs</p>
    </div>
</body>
"""

bowl = ""

# at the beginning:
start_time = time.time()

bowl = PrettyBowl(markup)

for i in range(1000):
    bowl = PrettyBowl(markup)

print("Pretty took %f seconds" % (time.time() - start_time))

bowl = ""

start_time = time.time()

bowl = BeautifulSoup(markup, 'html.parser')

for i in range(1000):
    bowl = BeautifulSoup(markup, 'html.parser')

print("Beautiful took %f seconds" % (time.time() - start_time))