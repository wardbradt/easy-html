from ps1.easyHTML.PageElement import PageElement


class NavigableString(str, PageElement):

    def __init__(self, value, *args):
        self.value = str(value)
        PageElement.__init__(self, *args)

    def _last_descendant(self, is_initialized=True, accept_self=True):
        """Finds the last element beneath this object to be parsed."""
        if is_initialized and self.next_sibling:
            last_child = self.next_sibling.previous_element
        else:
            last_child = self
        if not accept_self and last_child is self:
            last_child = None
        return last_child

    @property
    def name(self):
        return None

    @name.setter
    def name(self, name):
        raise AttributeError("A NavigableString cannot be given a name.")

    def __str__(self):
        return self.value
