from PageElement import PageElement


class NavigableString(str, PageElement):

    def __init__(self, value, *args):
        self.value = str(value)
        PageElement.__init__(self, *args)

    @property
    def name(self):
        return None

    @name.setter
    def name(self, name):
        raise AttributeError("A NavigableString cannot be given a name.")

    def __str__(self):
        return self.value
